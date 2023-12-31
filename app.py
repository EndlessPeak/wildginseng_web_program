from App import create_app
from App.utils import capture_camera
from App.utils import connect_serial
import threading

app = create_app()

if __name__ == '__main__':
    host = '127.0.0.1'
    # 新开一个线程提前加载 camera 模块，设置该线程为守护线程
    camera_thread = threading.Thread(target=capture_camera.camera_init,daemon=True)
    camera_thread.start()

    serial_thread = threading.Thread(target=connect_serial.serial_init,daemon=True)
    serial_thread.start()
    app.run(host=host,debug=False)

    # camera_thread.join()