#-*- coding: utf-8 -*-
import os
import cv2
import time
import json
import numpy as np

from paddle.inference import Config
from paddle.inference import PrecisionType
from paddle.inference import create_predictor

from PIL import Image, ImageDraw

# ——————————————————————模型配置、预测相关函数—————————————————————————— #
def resize(img, target_size):
    """resize to target size"""
    if not isinstance(img, np.ndarray):
        raise TypeError('image type is not numpy.')
    im_shape = img.shape
    im_size_min = np.min(im_shape[0:2])
    im_size_max = np.max(im_shape[0:2])
    im_scale_x = float(target_size) / float(im_shape[1])
    im_scale_y = float(target_size) / float(im_shape[0])
    img = cv2.resize(img, None, None, fx=im_scale_x, fy=im_scale_y)
    return img


def normalize(img, mean, std):
    img = img / 255.0
    mean = np.array(mean)[np.newaxis, np.newaxis, :]
    std = np.array(std)[np.newaxis, np.newaxis, :]
    img -= mean
    img /= std
    return img


def preprocess(img, img_size):
    mean = [0.485, 0.456, 0.406]
    std = [0.229, 0.224, 0.225]
    img = resize(img, img_size)
    img = img[:, :, ::-1].astype('float32')  # bgr -> rgb
    img = normalize(img, mean, std)
    img = img.transpose((2, 0, 1))  # hwc -> chw
    return img[np.newaxis, :]


def draw_bbox(img, result,label_dict, out_path,threshold=0.3):
    draw = ImageDraw.Draw(img)

    for res in result:
        cat_id, score, bbox = res[0], res[1], res[2:]
        # print("score:", score)
        if score < threshold:
            continue
        xmin, ymin, xmax, ymax = bbox
        
        # 绘制推理区域和推理结果
        draw.rectangle((int(xmin), int(ymin), int(xmax), int(ymax)), None, 'red')
        draw.text((xmin, ymin), '{},score={:.2f}'.format(label_dict[int(cat_id)], score), (0, 0, 0))
        print('category id is {},score is {}, bbox is {}'.format(label_dict[int(cat_id)], score, bbox))
    img.save(out_path, quality=95)

def write_result(result,label_dict,output_dir,threshold=0.3):
    results = [] # 初始化空列表
    for res in result:
        cat_id, score, bbox = res[0], res[1], res[2:]
        # print("score:", score)
        if score < threshold:
            continue
        
        if label_dict[int(cat_id)] == 'GradeA':
            category = "一等参"
        elif label_dict[int(cat_id)] == 'GradeB':
            category = "二等参"
        elif label_dict[int(cat_id)] == 'DY':
            category = "等外参"
        else:
            continue

        print('category id is {},score is {}, bbox is {}'.format(label_dict[int(cat_id)], score, bbox))
        
        # bbox 内的数据是 ndarray 格式，不能进行JSON序列化
        result_info = {
            'category': category,
            'score': float(score),
        }

        # 向列表添加字典
        results.append(result_info)

    with open(output_dir,'w',encoding='utf-8') as f:
        json.dump(results,f,ensure_ascii=False,indent=4)

def init_predictor(model_file, params_file):
    '''
        函数功能:初始化预测模型predictor
        函数输入:模型结构文件，模型参数文件
        函数输出:预测器predictor
    '''
    # 根据预测部署的实际情况，设置Config
    config = Config()
    # 读取模型文件
    config.set_prog_file(model_file)
    config.set_params_file(params_file)
    # Config默认是使用CPU预测，若要使用GPU预测，需要手动开启，设置运行的GPU卡号和分配的初始显存。
    config.enable_use_gpu(1000, 0)
    # 去除 Paddle Inference 运行中的 LOG
    config.disable_glog_info()
    # 开启内存 / 显存复用,优化
    config.enable_memory_optim()

    config.set_cpu_math_library_num_threads(4)
    #config.enable_mkldnn()
    # TensorRT加速
    # config.enable_tensorrt_engine(workspace_size=1 << 30, precision_mode=PrecisionType.Float32, max_batch_size=1,
    #                               min_subgraph_size=5, use_static=False, use_calib_mode=False)
    predictor = create_predictor(config)
    return predictor


def run(predictor, img):
    # copy img data to input tensor
    input_names = predictor.get_input_names()
    # print("input_names:", input_names)
    for i, name in enumerate(input_names):
        input_tensor = predictor.get_input_handle(name)
        input_tensor.reshape(img[i].shape)
        # print("img[i].shape:", img[i].shape)
        input_tensor.copy_from_cpu(img[i].copy())

    # do the inference
    predictor.run()

    results = []
    # get out data from output tensor
    # 获取输出 Tensor
    output_names = predictor.get_output_names()

    for i, name in enumerate(output_names):
        output_tensor = predictor.get_output_handle(name)
        # # 获取 Tensor 的维度信息
        out_shape = output_tensor.shape()
        # print("out_shape:", out_shape)
        # # 获取 Tensor 的数据类型
        # output_type = output_tensor.type()
        # print("output_type:", output_type)
        output_data = output_tensor.copy_to_cpu()
        # print("output_data:", output_data)
        results.append(output_data)
    return results

def infer_ginseng_image_backend(input_dir,output_dir,current_app):
    # 配置模型参数
    model_file = current_app.static_folder + "./output_inference/ppyoloe_plus_crn_x_80e_coco/model.pdmodel"
    params_file = current_app.static_folder + "./output_inference/ppyoloe_plus_crn_x_80e_coco/model.pdiparams"
    
    # 检查图片是否存在
    if not os.path.exists(input_dir):
        print("File or folder don't exists.")
        return
    
    # 读图片
    image = cv2.imread(input_dir)
    if image is not None:
        print("Infer image source read success.")
    else:
        print("Infer image source read failed.")
        return

    # 开始预测
    im_size = 640
    print("Prepare model.")
    time_start = time.time()
    # 初始化预测模型
    # args = parse_args()
    
    # 预测
    predictor = init_predictor(model_file, params_file)

    print('Prepare model cost {}'.format(time.time() - time_start), "s")
    
    data = preprocess(image, im_size)

    scale_factor = np.array([im_size * 1. / image.shape[0], im_size * 1. / image.shape[1]]).reshape((1, 2)).astype(np.float32)
    
    result = run(predictor, [data, scale_factor])

    print('Predict End')
    # print("result: ", result)
    # 类别定义
    label_dict = {0: 'DY', 1: 'GradeA', 2: 'MYL', 3: 'YL', 4: 'Ding', 5: 'GradeB'}

    # 图片结果绘制
    # img = Image.open(input_dir).convert('RGB')
    # draw_bbox(img, result[0], label_dict,out_path=output_dir)
    
    # 文字结果显示
    write_result(result[0],label_dict,output_dir=output_dir)
