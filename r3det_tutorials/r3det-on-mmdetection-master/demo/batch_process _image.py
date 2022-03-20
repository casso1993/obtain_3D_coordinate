# import asyncio
# import numpy as np
# from argparse import ArgumentParser
#
# from mmdet.apis import (async_inference_detector, inference_detector,
#                         init_detector, show_result_pyplot)
# import cv2
# import mmcv
# import os
#
# import warnings
#
# warnings.filterwarnings("ignore")
#
#
# def get_img_file(file_name):
#     imagelist = []
#     for parent, dirnames, filenames in os.walk(file_name):
#         for filename in filenames:
#             if filename.lower().endswith(
#                     ('.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff')):
#                 imagelist.append(os.path.join(parent, filename))
#
#         return imagelist
#
#
# def parse_args():
#     parser = ArgumentParser()
#     parser.add_argument('--img_dir', default='/home/casso/total_raw/egg/', help='Image file')
#     parser.add_argument('--out_dir', default='/home/casso/total_result/egg/', help='Image file')
#     parser.add_argument('--config', default='../configs/r3det/r3det_r50_fpn_2x_CustomizeImageSplit.py', help='Config file')
#     parser.add_argument('--checkpoint', default='../work_dirs/r3det_r50_fpn_2x_20200616/epoch_20.pth',
#                         help='Checkpoint file')
#     parser.add_argument(
#         '--device', default='cpu', help='Device used for inference')  # cuda:0
#     parser.add_argument(
#         '--score-thr', type=float, default=0.9, help='bbox score threshold')
#     parser.add_argument(
#         '--async-test',
#         action='store_true',
#         help='whether to set async options for async inference.')
#     args = parser.parse_args()
#     return args
#
#
# def main(args):
#     model = init_detector(args.config, args.checkpoint, device=args.device)
#
#     out_dir = args.out_dir
#     if not os.path.exists(out_dir):  # 判断是否存在文件夹如果不存在则创建为文件夹
#         os.makedirs(out_dir)
#
#     images = get_img_file(args.img_dir)
#
#     for image in images:
#         img = mmcv.imread(image)  # 或者 ，这样图片仅会被读一次 img = 'demo.jpg'
#         result = inference_detector(model, img)
#
#         # bboxes_scores = np.vstack(result)
#         # bboxes=bboxes_scores[:,:4]
#         # score=bboxes_scores[:,4]
#         # labels = [
#         #           np.full(bbox.shape[0], i, dtype=np.int32)
#         #           for i, bbox in enumerate(result)
#         #       ]
#         # labels = np.concatenate(labels)
#         # print(bboxes_scores)
#         # print(labels)
#         # print(result)
#         out_file = out_dir + image.split('/')[-1]
#         model.show_result(img, result, score_thr=args.score_thr, out_file=out_file)
#
#
# if __name__ == '__main__':
#     args = parse_args()
#     if args.async_test:
#         asyncio.run(async_main(args))
#     else:
#         main(args)


from argparse import ArgumentParser
import time
import cv2
import os

from mmdet.apis import inference_detector, init_detector, show_result_pyplot

def get_img_file(file_name):
    imagelist = []
    for parent, dirnames, filenames in os.walk(file_name):
        for filename in filenames:
            if filename.lower().endswith(
                    ('.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff')):
                imagelist.append(os.path.join(parent, filename))

        return imagelist


def main():
    time_start = time.time()

    parser = ArgumentParser()
    parser.add_argument('img', help='Image file')
    parser.add_argument('config', help='Config file')
    parser.add_argument('checkpoint', help='Checkpoint file')
    parser.add_argument(
        '--device', default='cuda:0', help='Device used for inference')
    parser.add_argument(
        '--score-thr', type=float, default=0.3, help='bbox score threshold')
    args = parser.parse_args()

    # build the model from a config file and a checkpoint file
    model = init_detector(args.config, args.checkpoint, device=args.device)
    images = get_img_file(args.img_dir)
    # test a single image
    result = inference_detector(model, args.img)
    time_end = time.time()
    print('time cost', time_end - time_start, 's')

    # show the results
    show_result_pyplot(model, args.img, result, score_thr=args.score_thr)

    # change: inference.py, rbbox_visualization.py


if __name__ == '__main__':
    main()