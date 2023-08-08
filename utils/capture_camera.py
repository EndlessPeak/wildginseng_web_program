import cv2

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