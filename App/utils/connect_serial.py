import serial
import struct
import crcmod
import time

ser = None # 串口变量
index_bytes = b"\x00\x00\x00\x00" # 索引起始为0

def serial_init():
    '''
    该函数用于初始化串口相关设置
    '''
    global ser
    print("start init serial")
    # 设置串口参数
    port = "COM2"  # 串口号
    baudrate = 115200  # 波特率
    bytesize = serial.serialutil.EIGHTBITS  # 数据位
    parity = serial.serialutil.PARITY_NONE  # 校验位
    stopbits = serial.serialutil.STOPBITS_ONE  # 停止位

    # 初始化串口
    ser = serial.Serial(port, baudrate, bytesize, parity, stopbits)
    print("end init serial")

def index_self_add():
    '''
    该函数用于操作索引，每次对索引值进行自增
    '''
    global index_bytes
    # 对索引进行自增操作
    index = struct.unpack('<I',index_bytes)[0]
    index += 1
    index_bytes = struct.pack('<I',index)

def crc_16_caculate(data_frame):
    # 计算 CRC
    crc16 = crcmod.predefined.mkPredefinedCrcFun('modbus')
    crc = crc16(data_frame)

    # 将 CRC 拆分成两个字节
    crc_bytes = struct.pack("<H", crc)
    #crc_bytes = b"\x47\x2D"
    #print(crc_bytes[0]);
    #print(crc_bytes[1]);

    return crc_bytes

'''
下列两个函数用于在控制台打印发送的数据帧和接收的数据帧
接收数据帧的处理是必要的，后续可将第二个函数的逻辑写在各通信函数中
'''
def debug_send_frame(send_frame):
    send_frame_hex = ' '.join([hex(byte)[2:].zfill(2) for byte in send_frame])
    print("send order: ",send_frame_hex)

def debug_receive_frame(receive_bytes):
    # print("start receive order.")
    receive_frame = ser.read(receive_bytes) # 读取收到的数据
    receive_frame_hex = ' '.join([hex(byte)[2:].zfill(2) for byte in receive_frame])
    print("receive order: ",receive_frame_hex)

'''
下列各函数用于与下位机通信
'''
def serial_turn_light(light_id,turn_action):
    '''
    本函数用于打开或关闭补光灯1和2
    '''
    global ser
    global index_bytes
    # 构造数据帧
    protocol_header = b"\xA5\x5A"
    length = b"\x22\x00"
    device_id = b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    reserved = b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    
    # index_bytes 计算
    index_self_add()

    command_type = b"\x10"
    command_id = b"\x04"

    # 判断灯ID
    if light_id==1:
        data_light_id = b"\x01"
    elif light_id==2:
        data_light_id = b"\x02"
    else:
        return

    # 判断动作
    if turn_action==0:
        data_light_action = b"\x00"
    elif turn_action==1:
        data_light_action = b"\x01"
    else:
        return

    data_frame = protocol_header + length + device_id + reserved + \
          index_bytes + command_type + command_id + data_light_id + data_light_action
    
    crc_bytes = crc_16_caculate(data_frame=data_frame)

    # 发送数据帧
    send_frame = data_frame + crc_bytes
    
    debug_send_frame(send_frame=send_frame)
    ser.write(send_frame)
    # 等待下位机回复消息
    # while ser.in_waiting == 0:
    #    pass
    debug_receive_frame(receive_bytes=33)

def set_motor_angle(angle):
    '''
    本函数用于设置电机旋转角度
    '''
    global ser
    # 构造数据帧
    protocol_header = b"\xA5\x5A"
    length = b"\x24\x00"
    device_id = b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    reserved = b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    
    # index_bytes 计算
    index_self_add()

    command_type = b"\x0A"
    command_id = b"\x02"

    # 旋转角度（默认为120）
    if angle == 120:
        data_angle = b"\x00\x00\xF0\x42"
    else:
        return

    data_frame = protocol_header + length + device_id + reserved + \
          index_bytes + command_type + command_id + data_angle
    
    crc_bytes = crc_16_caculate(data_frame=data_frame)

    # 发送数据帧
    send_frame = data_frame + crc_bytes
    
    debug_send_frame(send_frame=send_frame)
    ser.write(send_frame)
    debug_receive_frame(receive_bytes=33)

def let_motor_angle(direction):
    '''
    本函数用于令电机进行旋转
    '''
    global ser
    # 构造数据帧
    protocol_header = b"\xA5\x5A"
    length = b"\x21\x00"
    device_id = b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    reserved = b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"

    # index_bytes 计算
    index_self_add()

    command_type = b"\x10"
    command_id = b"\x01"

    # 电机正旋转
    if direction == 1:
        data_direction = b"\x01"
    # 电机反旋转
    elif direction == 2:
        data_direction = b"\x02"
    # 电机停止运动
    elif direction == 0:
        data_direction = b"\x00"
    else:
        return
    
    data_frame = protocol_header + length + device_id + reserved + \
          index_bytes + command_type + command_id + data_direction
    
    crc_bytes = crc_16_caculate(data_frame=data_frame)

    # 发送数据帧
    send_frame = data_frame + crc_bytes
    
    debug_send_frame(send_frame=send_frame)
    ser.write(send_frame)
    # 控制命令后先接收一次下位机命令
    debug_receive_frame(receive_bytes=33)

    # 线程等待下位机运行结束，再收一次下位机命令
    while ser.in_waiting == 0:
        pass
    debug_receive_frame(receive_bytes=34)
    after_let_motor_angle()

def after_let_motor_angle():
    '''
    本函数用于设备电机旋转后，平台回复下位机
    '''
    protocol_header = b"\xA5\x5A"
    length = b"\x20\x00"
    device_id = b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    reserved = b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    
    # index_bytes 计算
    index_self_add()

    command_type = b"\x81"
    command_id = b"\x04"

    data_frame = protocol_header + length + device_id + reserved + \
          index_bytes + command_type + command_id
    
    crc_bytes = crc_16_caculate(data_frame=data_frame)

    # 发送数据帧
    send_frame = data_frame + crc_bytes
    
    debug_send_frame(send_frame=send_frame)
    ser.write(send_frame)

def motor_angle_rotate(angle=120,direction=0):
    '''
    本函数用于设置电机旋转角度并进行旋转
    '''
    set_motor_angle(angle)
    let_motor_angle(direction)



def serial_close():
    global ser
    # 关闭串口连接
    ser.close()