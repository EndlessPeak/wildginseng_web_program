import serial
import struct
import crcmod

# 设置串口参数
port = "COM2"  # 串口号
baudrate = 115200  # 波特率
bytesize = serial.serialutil.EIGHTBITS  # 数据位
parity = serial.serialutil.PARITY_NONE  # 校验位
stopbits = serial.serialutil.STOPBITS_ONE  # 停止位

# 初始化串口
ser = serial.Serial(port, baudrate, bytesize, parity, stopbits)

# 构造数据帧
protocol_header = b"\xA5\x5A"
length = b"\x22\x00"
device_id = b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
reserved = b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
index = b"\x01\x00\x00\x00"
command_type = b"\x10"
command_id = b"\x04"
data = b"\x02\x00"

# 计算 CRC
crc16 = crcmod.predefined.mkPredefinedCrcFun('modbus')
crc = crc16(protocol_header + length + device_id + reserved + index + command_type + command_id + data)

# 将 CRC 拆分成两个字节
crc_bytes = struct.pack("<H", crc)
#crc_bytes = b"\x47\x2D"
#print(crc_bytes[0]);
#print(crc_bytes[1]);

# 发送数据帧
frame = protocol_header + length + device_id + reserved + index + command_type + command_id + data + crc_bytes
ser.write(frame)

# 关闭串口连接
ser.close()