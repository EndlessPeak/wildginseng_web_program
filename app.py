from App import create_app
from App.utils import capture_camera
import threading

app = create_app()

if __name__ == '__main__':
    host = '127.0.0.1'
    
    # 新开一个线程提前加载 camera 模块
    camera_thread = threading.Thread(target=capture_camera.camera_init)
    camera_thread.start()

    app.run(host=host,debug=False)

    # camera_thread.join()