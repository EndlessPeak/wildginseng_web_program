import os
import cv2

def crop_ginseng_image_backend(input_dir,output_dir,s_height=0.2,e_height=0.8,s_col=0.2,e_col=0.8):
    # 检查文件路径是否存在
    if not os.path.exists(input_dir):
        print("File or folder don't exists!")
        return
    
    # 读取野山参图片
    ginseng_image = cv2.imread(input_dir)

    if ginseng_image is not None:
        print("Crop Read ginseng_image success!")
    else:
        print("Crop Read ginseng_image failed!")
        return
    
    # 检查图片大小并将其裁剪到指定大小
    # 以后可以考虑依赖注入该部分
    height, width = ginseng_image.shape[:2]
    start_row = int(height * s_height)
    end_row = int(height * e_height)
    start_col = int(width * s_col)
    end_col = int(width * e_col)

    # 裁剪野山参图片
    ginseng_image = ginseng_image[start_row:end_row, start_col:end_col]
    print("cropp ginseng_image success.")

    # 保存野山参图片
    cv2.imwrite(output_dir,ginseng_image)
    print("crop ginseng_image saved.")