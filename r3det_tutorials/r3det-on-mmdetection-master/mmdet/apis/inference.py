import warnings

import matplotlib.pyplot as plt
import mmcv
import torch
from mmcv.parallel import collate, scatter
from mmcv.runner import load_checkpoint

from mmdet.core import get_classes
from mmdet.datasets.pipelines import Compose
from mmdet.models import build_detector
from mmdet.ops import RoIAlign, RoIPool

import cv2
import math

blue = (255, 0, 0)
green = (0, 255, 0)
red = (0, 0, 255)
yellow = (0, 255, 255)


def draw_grasping(img, center_x, center_y, angel, color):
    x1 = int(60 * math.cos(angel) - 10 * math.sin(angel) + center_x)
    y1 = int(60 * math.sin(angel) + 10 * math.cos(angel) + center_y)

    x2 = int(40 * math.cos(angel) - 10 * math.sin(angel) + center_x)
    y2 = int(40 * math.sin(angel) + 10 * math.cos(angel) + center_y)

    x3 = int(40 * math.cos(angel) + 10 * math.sin(angel) + center_x)
    y3 = int(40 * math.sin(angel) - 10 * math.cos(angel) + center_y)

    x4 = int(60 * math.cos(angel) + 10 * math.sin(angel) + center_x)
    y4 = int(60 * math.sin(angel) - 10 * math.cos(angel) + center_y)

    cv2.line(img, (x1, y1), (x2, y2), color, 3)
    cv2.line(img, (x2, y2), (x3, y3), color, 3)
    cv2.line(img, (x3, y3), (x4, y4), color, 3)
    cv2.line(img, (x4, y4), (x1, y1), color, 3)


def init_detector(config, checkpoint=None, device='cuda:0'):
    """Initialize a detector from config file.

    Args:
        config (str or :obj:`mmcv.Config`): Config file path or the config
            object.
        checkpoint (str, optional): Checkpoint path. If left as None, the model
            will not load any weights.

    Returns:
        nn.Module: The constructed detector.
    """
    if isinstance(config, str):
        config = mmcv.Config.fromfile(config)
    elif not isinstance(config, mmcv.Config):
        raise TypeError('config must be a filename or Config object, '
                        f'but got {type(config)}')
    config.model.pretrained = None
    model = build_detector(config.model, test_cfg=config.test_cfg)
    if checkpoint is not None:
        checkpoint = load_checkpoint(model, checkpoint)
        if 'CLASSES' in checkpoint['meta']:
            model.CLASSES = checkpoint['meta']['CLASSES']
        else:
            warnings.simplefilter('once')
            warnings.warn('Class names are not saved in the checkpoint\'s '
                          'meta data, use COCO classes by default.')
            model.CLASSES = get_classes('coco')
    model.cfg = config  # save the config in the model for convenience
    model.to(device)
    model.eval()
    return model


class LoadImage(object):

    def __call__(self, results):
        if isinstance(results['img'], str):
            results['filename'] = results['img']
            results['ori_filename'] = results['img']
        else:
            results['filename'] = None
            results['ori_filename'] = None
        img = mmcv.imread(results['img'])
        results['img'] = img
        results['img_fields'] = ['img']
        results['img_shape'] = img.shape
        results['ori_shape'] = img.shape
        return results


def inference_detector(model, img):
    """Inference image(s) with the detector.

    Args:
        model (nn.Module): The loaded detector.
        imgs (str/ndarray or list[str/ndarray]): Either image files or loaded
            images.

    Returns:
        If imgs is a str, a generator will be returned, otherwise return the
        detection results directly.
    """
    cfg = model.cfg
    device = next(model.parameters()).device  # model device
    # build the data pipeline
    test_pipeline = [LoadImage()] + cfg.data.test.pipeline[1:]
    test_pipeline = Compose(test_pipeline)
    # prepare data
    data = dict(img=img)
    data = test_pipeline(data)
    data = collate([data], samples_per_gpu=1)
    if next(model.parameters()).is_cuda:
        # scatter to specified GPU
        data = scatter(data, [device])[0]
    else:
        # Use torchvision ops for CPU mode instead
        for m in model.modules():
            if isinstance(m, (RoIPool, RoIAlign)):
                if not m.aligned:
                    # aligned=False is not implemented on CPU
                    # set use_torchvision on-the-fly
                    m.use_torchvision = True
        warnings.warn('We set use_torchvision=True in CPU mode.')
        # just get the actual data from DataContainer
        data['img_metas'] = data['img_metas'][0].data

    # forward the model
    with torch.no_grad():
        result = model(return_loss=False, rescale=True, **data)
    return result


async def async_inference_detector(model, img):
    """Async inference image(s) with the detector.

    Args:
        model (nn.Module): The loaded detector.
        imgs (str/ndarray or list[str/ndarray]): Either image files or loaded
            images.

    Returns:
        Awaitable detection results.
    """
    cfg = model.cfg
    device = next(model.parameters()).device  # model device
    # build the data pipeline
    test_pipeline = [LoadImage()] + cfg.data.test.pipeline[1:]
    test_pipeline = Compose(test_pipeline)
    # prepare data
    data = dict(img=img)
    data = test_pipeline(data)
    data = scatter(collate([data], samples_per_gpu=1), [device])[0]

    # We don't restore `torch.is_grad_enabled()` value during concurrent
    # inference since execution can overlap
    torch.set_grad_enabled(False)
    result = await model.aforward_test(rescale=True, **data)
    return result


def show_result_pyplot(model, img, result, score_thr=0.3, fig_size=(15, 10)):
    """Visualize the detection results on the image.

    Args:
        model (nn.Module): The loaded detector.
        img (str or np.ndarray): Image filename or loaded image.
        result (tuple[list] or list): The detection result, can be either
            (bbox, segm) or just bbox.
        score_thr (float): The threshold to visualize the bboxes and masks.
        fig_size (tuple): Figure size of the pyplot figure.
    """
    if hasattr(model, 'module'):
        model = model.module
    img = model.show_result(img, result, score_thr=score_thr, show=False)

    for i in range(len(result)):
        for j in range(len(result[i])):
            if result[i][j][5] > score_thr:
                # print("Class: ", i)
                # print("center:", result[i][j][0], result[i][j][1])
                # print("Width, High:", result[i][j][2], result[i][j][3])
                # print("Angel: ", 180 / 3.1415926 * result[i][j][4], "\n")
                data = [str(round(result[i][j][0], 2)), ' ', str(round(result[i][j][1], 2)), ' ',
                        str(round(result[i][j][2], 2)), ' ', str(round(result[i][j][3], 2)), ' ',
                        str(round(result[i][j][4], 2)), ' ', str(round(result[i][j][5], 2)), ' ', str(i), ' \\ ']
                with open("/home/casso/data/data_pear&plastic&plastic.txt", "a") as f:
                    f.writelines(data)



                #cv2.circle(img, (result[i][j][0], result[i][j][1]), 2, yellow, 2)

                # if result[i][j][2] > 65 and result[i][j][3] > 65:
                #     for k in range(6):
                #         draw_grasping(img, result[i][j][0], result[i][j][1],
                #                       result[i][j][4] + 3.14159265 / 3 * k, red)
                # elif result[i][j][2] > 65:
                #     for k in range(6):
                #         if k == 0 or k == 3:
                #             draw_grasping(img, result[i][j][0], result[i][j][1],
                #                           result[i][j][4] + 3.14159265 / 3 * k, red)
                #         else:
                #             draw_grasping(img, result[i][j][0], result[i][j][1],
                #                           result[i][j][4] + 3.14159265 / 3 * k, green)
                # elif result[i][j][3] > 65:
                #     for k in range(6):
                #         if k == 1 or k == 4:
                #             draw_grasping(img, result[i][j][0], result[i][j][1],
                #                           result[i][j][4] + 3.14159265/6 + 3.14159265 / 3 * k, red)
                #         else:
                #             draw_grasping(img, result[i][j][0], result[i][j][1],
                #                           result[i][j][4] + 3.14159265/6 + 3.14159265 / 3 * k, green)
                # else:
                #     for k in range(6):
                #         draw_grasping(img, result[i][j][0], result[i][j][1],
                #                       result[i][j][4] + 3.14159265 / 3 * k, green)

    with open("/home/casso/data/data_pear&plastic&plastic.txt", "a") as f:
        f.writelines('\n')
    plt.figure(figsize=fig_size)
    plt.imshow(mmcv.bgr2rgb(img))
    plt.show()
