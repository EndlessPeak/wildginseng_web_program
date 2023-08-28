import os
import cv2
import time
import uuid
import hashlib
import threading

# 声明语义上的全局变量，在视图模块中也导入该模块
# 为确保视图模块能正确访问，这里必须写完整导入路径
from App.utils import shared_vars

camera = None
# camera_lock = threading.Lock()

'''
初始化摄像头，该函数在主函数中以线程方式启动，减少加载时间
'''
def camera_init():
    global camera
    # 添加互斥锁避免潜在的线程安全问题
    # 在下面的函数中，互斥锁持有不释放将会导致无法退出解释器的问题，故暂时停用
    # with camera_lock:
    print("start init")
    camera = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    # 初始化参数包含以下几种：
    # 1. 无，此时启动速度最慢
    # 2. cv2.CAP_DSHOW 启动最快
    # 3. cv2.CAP_MSMF 启动与不带参数类似
    width = 1024
    height = 768
    camera.set(cv2.CAP_PROP_FRAME_WIDTH,width)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
    print("end init")

'''
获得本地摄像头图像字节流传输
'''
def camera_ginseng_frames():
    global camera
    
    while True:
        if camera == None:
            time.sleep(5)
            continue

        ret,frame = camera.read()
        if not ret:
            break
        # 把获取到的图像格式转换(编码)成流数据，赋值到内存缓存中;
        # 主要用于图像数据格式的压缩，方便网络传输

        frame = cv2.rotate(frame,cv2.ROTATE_90_COUNTERCLOCKWISE)

        ret,buffer = cv2.imencode('.jpg',frame)
        # 如果无法将帧编码为 JPEG 格式，将会重新读取下一帧并尝试编码。
        # 如果认为该错误严重程度高，也可以改为 break
        if not ret:
            continue 
            
        # 将缓存里的流数据转成字节流
        image_data_bytes = buffer.tobytes()

        if(shared_vars.capture):
            shared_vars.capture = False
            print("capture flag captured!")
            
            # 根据 frame_bytes 内容进行哈希运算
            file_hash = hashlib.sha1(image_data_bytes).hexdigest()
            file_id = str(uuid.uuid5(uuid.NAMESPACE_DNS,file_hash))

            # 得到文件名
            file_name = file_id +'.jpg'
            current_dir = os.getcwd()
            relative_path = os.path.join('App/sources/upload_image/', file_name)
            file_path = os.path.abspath(os.path.join(current_dir,relative_path))

            print(file_path)

            # 保存JPG格式的图片
            with open(file_path,'wb') as f:
                f.write(buffer)
            
            # 保存文件名到公共变量文件
            shared_vars.file_name = file_name
            shared_vars.save_finished = True

            # 注意若保存frame则是以PNG格式无损保存
            #cv2.imwrite(file_path,frame)

            print("picture saved at",file_path)
            

        # 指定字节流类型image/jpeg
        yield  (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + image_data_bytes + b'\r\n')
        
def testCamera():
    # 创建摄像头对象
    cap = cv2.VideoCapture(0)  # 0表示第一个摄像头，如果连接了多个摄像头，可以尝试不同的索引值
    while True:
        # 逐帧捕获图像
        ret, frame = cap.read()
        # 显示图像
        cv2.imshow('Camera', frame)
        # 按下 'q' 键退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # 释放摄像头资源
    cap.release()
    # 关闭窗口
    cv2.destroyAllWindows()