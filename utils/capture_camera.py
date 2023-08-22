import cv2
import uuid

'''
获得本地摄像头图像字节流传输
'''
def camera_ginseng_frames():
    # capture = False
    camera0 = cv2.VideoCapture(0)
    while True:
        ret,frame = camera0.read()
        if not ret:
            break
        # 把获取到的图像格式转换(编码)成流数据，赋值到内存缓存中;
        # 主要用于图像数据格式的压缩，方便网络传输

        # if(capture):
        #     capture=0
        #     global uid
        #     uid = str(uuid.uuid1())
        #     file_path = r'./static/yIMG/' + uid + '.JPG'
        #     cv2.imwrite(file_path,frame)

        ret,buffer = cv2.imencode('.jpg',frame)
        # 如果无法将帧编码为 JPEG 格式，将会重新读取下一帧并尝试编码。
        # 如果认为该错误严重程度高，也可以改为 break
        if not ret:
            continue 
            
        # 将缓存里的流数据转成字节流
        frame = buffer.tobytes()
        # 指定字节流类型image/jpeg
        yield  (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
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