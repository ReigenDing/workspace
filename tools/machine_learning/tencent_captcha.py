#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Vin on 2017/7/24


import glob
import numpy as np

from keras.applications.xception import Xception, preprocess_input
from keras.layers import Input, Dense, Dropout
from keras.models import Model

from scipy import misc

# 评价模型的全对率
from tqdm import tqdm

samples = glob.glob('sample/*.jpg')

np.random.shuffle(samples)  # 打乱训练样本

nb_train = 90000  # 共有10万样本，9万用于训练，1万用于测试
train_samples = samples[:nb_train]
test_samples = samples[nb_train:]

img_size = (50, 120)  # 全体图片都resize成这个尺寸
input_image = Input(shape=(img_size[0], img_size[1], 3))
base_model = Xception(input_tensor=input_image, weights='imagenet', include_top=False, pooling='avg')
predicts = [Dense(26, activation='softmax')(Dropout(0.5)(base_model.output)) for i in range(4)]

model = Model(inputs=input_image, outputs=predicts)
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.summary()


def data_generator(data, batch_size):  # 样本生成器，节省内存
    while True:
        batch = np.random.choice(data, batch_size)
        x, y = [], []
        for img in batch:
            x.append(misc.imresize(misc.imread(img), img_size))
            y.append([ord(i) - ord('a') for i in img[7:11]])
        x = preprocess_input(np.array(x).astype(float))
        y = np.array(y)
        yield x, [y[:, i] for i in range(4)]


# 训练过程终会显示逐标签的准确率
model.fit_generator(data_generator(train_samples, 100), steps_per_epoch=1000, epochs=10,
                    validation_data=data_generator(test_samples, 100), validation_steps=100)


total = 0.
right = 0.
step = 0
for x, y in tqdm(data_generator(test_samples, 100)):
    _ = model.predict(x)
    _ = np.array([i.argmax(axis=1) for i in _]).T
    y = np.array(y).T
    total += len(x)
    right += ((_ == y).sum(axis=1) == 4).sum()
    if step < 100:
        step += 1
    else:
        break

print u'模型全对率：%s' % (right / total)
# serialize model to JSON
model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("model.h5")
print("Saved model to disk")
