# -*- coding: utf-8 -*
import os
import glob
import hashlib
import random
import shutil

from toolbox.imagetool import CaptchaTool
from PIL import Image
import numpy as np
from sklearn import cluster


def make_letter_set():
    """制作字母切片训练集"""
    images = glob.glob(r'D:\Documents\Databases\amazon_captcha\*.jpg')
    with CaptchaTool() as ct:
        for img in images:
            print(ct.image_split(img, save_dir=r'D:\Documents\Databases\letter_set',
                                 width_limit=10,
                                 color_threshold=3))


def images_filter():
    images = glob.glob(r'D:\Documents\Databases\letter_set\*.jpg')
    md5_dict = {}
    for img in images:
        with open(img, 'rb') as im:
            im_md5 = hashlib.md5(im.read()).hexdigest()
            md5_dict[im_md5] = img
        print(len(md5_dict))
    for img in images:
        if img not in md5_dict.values():
            print("remove: {0}".format(img))
            os.remove(img)
    print("remain {0}".format(len(md5_dict)))


def clustering_by_letter_width():
    width_dict = {}
    images = glob.glob(r'D:\Documents\Databases\letter_set\*.jpg')
    for img in images:
        with Image.open(img) as im:
            if str(im.width) not in width_dict:
                width_dict[str(im.width)] = [img]
            else:
                width_dict[str(im.width)].append(img)
        print("classify {0} class".format(len(width_dict)))
    for w, fs in width_dict.items():
        save_dir = os.path.join(r'D:\Documents\Databases\alphabet', w)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        for f in fs:
            print("move {0} to {1}".format(f, save_dir))
            shutil.copy(f, save_dir)
    print("finished, we have {0} class".format(len(width_dict)))


def agglomerative_model(target_dir, n):
    images = glob.glob(os.path.join(target_dir, '*.jpg'))
    data_set = [np.float32(Image.open(img).getdata()) / 255 for img in images]
    max_length = max(map(len, data_set))
    X_train = [np.pad(data, (0, max_length - len(data)), 'constant', constant_values=0) for data in data_set]
    print("training model...")
    cls = cluster.AgglomerativeClustering(n_clusters=n, linkage="average", affinity="cosine")
    print("clustering...")
    X = cls.fit(X_train)
    labels = list(X.labels_)
    for idx, img in enumerate(images):
        dst_dir = os.path.join(target_dir, str(labels[idx]))
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        print("copy {0} to {1}".format(img, dst_dir))
        shutil.copy(img, dst_dir)


def make_training_set():
    root_dir = r'D:\Documents\Databases\alphabet'
    training_set = r'D:\Documents\PinganGit\common\toolbox\TensorFlowTraining\data\test_data'
    alphabet = os.listdir(root_dir)
    with CaptchaTool() as lct:
        for x in range(100):
            words = [random.choice(alphabet), random.choice(alphabet), random.choice(alphabet), random.choice(alphabet),
                     random.choice(alphabet), random.choice(alphabet)]
            images = [random.choice(glob.glob(os.path.join(root_dir, x, "*.jpg"))) for x in words]
            _path = lct.images_stitch(images, size=(200, 70),
                                      save_path=os.path.join(training_set, "{}.jpg".format(''.join(words))))
            print(x, _path)


if __name__ == '__main__':
    pass
    # 将验证码分片
    # make_letter_set()
    # 过滤重复的切片
    # images_filter()
    # 根据切片的宽度分类
    # clustering_by_letter_width()
    # 使用聚类算法做聚类
    # agglomerative_model(r'D:\Documents\Databases\letter_set', 52)
    # 制作训练集
    make_training_set()
