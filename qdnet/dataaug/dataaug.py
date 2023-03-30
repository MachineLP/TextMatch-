
import os
import cv2
import numpy as np
import pandas as pd
import albumentations
import torch
from torch.utils.data import Dataset

from tqdm import tqdm
import random

def get_transforms_(image_size):

    transforms_train = albumentations.Compose([
        albumentations.Transpose(p=0.5),
        albumentations.VerticalFlip(p=0.5),
        albumentations.HorizontalFlip(p=0.5),
        albumentations.RandomBrightness(limit=0.2, p=0.75),
        albumentations.RandomContrast(limit=0.2, p=0.75),
        albumentations.OneOf([
            albumentations.MotionBlur(blur_limit=5),
            albumentations.MedianBlur(blur_limit=5),
            albumentations.GaussianBlur(blur_limit=5),
            albumentations.GaussNoise(var_limit=(5.0, 30.0)),
        ], p=0.7),

        albumentations.OneOf([
            albumentations.OpticalDistortion(distort_limit=1.0),
            albumentations.GridDistortion(num_steps=5, distort_limit=1.),
            albumentations.ElasticTransform(alpha=3),
        ], p=0.7),

        albumentations.CLAHE(clip_limit=4.0, p=0.7),
        albumentations.HueSaturationValue(hue_shift_limit=10, sat_shift_limit=20, val_shift_limit=10, p=0.5),
        albumentations.ShiftScaleRotate(shift_limit=0.1, scale_limit=0.1, rotate_limit=15, border_mode=0, p=0.85),
        albumentations.Resize(image_size, image_size),
        albumentations.Cutout(max_h_size=int(image_size * 0.375), max_w_size=int(image_size * 0.375), num_holes=1, p=0.7),
        albumentations.Normalize()
    ])

    transforms_val = albumentations.Compose([
        albumentations.Resize(image_size, image_size),
        albumentations.Normalize()
    ])

    return transforms_train, transforms_val


def get_transforms(image_size):

    transforms_train = albumentations.Compose([
        albumentations.RandomBrightness(limit=0.2, p=0.5),
        albumentations.OneOf([
            albumentations.MotionBlur(blur_limit=5),
            albumentations.MedianBlur(blur_limit=5),
            albumentations.GaussianBlur(blur_limit=5),
            albumentations.GaussNoise(var_limit=(5.0, 30.0)),
        ], p=0.5),
        albumentations.ImageCompression(quality_lower=80, quality_upper=100, p=0.5),
        albumentations.ShiftScaleRotate(shift_limit=0.05, scale_limit=(-0.2, 0.5), rotate_limit=30, border_mode=1, p=0.5),
        # albumentations.Resize(int(image_size*random.uniform(0.8,1.2)), int(image_size*random.uniform(0.8,1.2))),
        # albumentations.CenterCrop(width=image_size, height=image_size, p=0.5), 
        # albumentations.RandomCrop(width=image_size, height=image_size, p=0.5), 
        albumentations.Resize(image_size, image_size),
        albumentations.Normalize()
    ])

    transforms_val = albumentations.Compose([
        albumentations.Resize(image_size, image_size),
        albumentations.Normalize()
    ])

    return transforms_train, transforms_val


if __name__ == '__main__':
    image = cv2.imread( 'img_name' )
    for i in range(200):
        image2 = albumentations.ShiftScaleRotate(shift_limit=0.05, scale_limit=(-0.2, 0.5), rotate_limit=30, border_mode=1, p=0.5)
        cv2.imwrite( "./test_img/test_{}.jpg".format(i), image2 )
