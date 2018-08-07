import os
import math
import cv2
import time
import hashlib
import itertools

from PIL import Image
from matplotlib import pyplot as plt
from sklearn.metrics import pairwise_distances

import numpy as np

from toolbox.config import DEFAULT_LOGGER


class Colors(object):
    """常用颜色"""
    white = 255
    black = 0

    @staticmethod
    def is_black(color, threshold=15):
        """非bmp格式图片都会被压缩，颜色存在色差，
        用这个方法把阈值范围内的颜色都判断为黑色
        """
        return True if color <= Colors.black + threshold else False

    @staticmethod
    def is_white(color, threshold=15):
        return True if color >= Colors.white - threshold else False


def image_a_in_b(image_a, image_b, dev=False):
    """
    检测图片a是否在图片b中，若匹配到结果则返回坐标（元组）
    :param image_a: 图片a的路径
    :param image_b: 图片b的路径
    :param dev: 调试模式，显示图片
    :return: tuple
    """
    if os.path.exists(image_a) and os.path.exists(image_b):
        img_a = cv2.imread(image_a, 0)
        img_b = cv2.imread(image_b, 0)
        match = cv2.matchTemplate(img_a, img_b, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)
        if max_val >= 0.95:
            top_left = max_loc
            img_a_wight, img_a_hight = img_a.shape[::-1]
            bottom_right = (top_left[0] + img_a_wight,
                            top_left[1] + img_a_hight)
            if dev:
                # 将图片输出以供调试
                cv2.rectangle(img_b, top_left, bottom_right, 0, 2)
                plt.imshow(img_b, cmap='gray')
                plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
                plt.show()
            DEFAULT_LOGGER.info("图像匹配值：{}".format(max_val))
            return top_left, bottom_right
        else:
            DEFAULT_LOGGER.info("图像匹配值低于0.95，判定为无法从图片中匹配到准确位置")
            return None
    else:
        DEFAULT_LOGGER.info("图片路径不存在，请检查")
        return None


# 空间向量搜索引擎
class VectorCompare(object):
    @staticmethod
    def image_vector(img):
        """生成图片矢量"""
        src_img = Image.open(img)
        v, count = {}, 0
        for i in src_img.getdata():
            v[count] = i
            count += 1
        return v

    # 计算矢量大小
    @staticmethod
    def vector_norm(concordance):
        """计算向量的模"""
        total = 0
        for word, count in concordance.items():
            total += count ** 2
        return math.sqrt(total)

    def relation(self, concordance1, concordance2):
        """向量积公式：a · b = |a| * |b| * cos<a, b>"""
        inner_product = 0
        for word, count in concordance1.items():
            if word in concordance2:
                inner_product += count * concordance2[word]
        return inner_product / (self.vector_norm(concordance1) * self.vector_norm(concordance2))


class CaptchaTool(object):
    def __init__(self, image_path=None, **kwargs):
        """
        可以传入默认处理的图片路径，kwargs是自定义的需要在对象中维持的变量
        :param image_path:
        :param kwargs: {'save_mode': 'bmp'}
        """
        # image handle
        self.image_handle = None
        # image basic info
        self.image_path = ''
        self.default_save_dir = ''
        self.image_name = ''
        self.image_suffix = ''
        # init
        if image_path:
            self.set_image_handle(image_path)
        # self define variables
        for name, value in kwargs.items():
            self.__setattr__(name, value)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def __getattr__(self, item):
        if isinstance(self.image_handle, Image.Image):
            return self.image_handle.__getattribute__(item)

    @staticmethod
    def open(image_path):
        return Image.open(image_path)

    def close(self):
        if isinstance(self.image_handle, Image.Image):
            self.image_handle.close()

    def save(self, image_handle=None, **kwargs):
        image_handle = image_handle if image_handle else self.image_handle
        if kwargs.get('save_path'):
            image_handle.save(kwargs.get('save_path'))
            return os.path.realpath(kwargs.get('save_path'))
        elif kwargs.get('save_dir'):
            _save_path = os.path.join(kwargs.get('save_dir'), self.image_name)
        elif self.image_path:
            _save_path = self.image_path
        else:
            _image_name = "{}.jpg".format(hashlib.md5(str(time.time()).encode('utf-8')).hexdigest())
            _save_path = os.path.join('./', _image_name)
        if kwargs.get('prefix'):
            _save_path = _save_path.replace(self.image_name, "{0}{1}".format(kwargs.get('prefix'), self.image_name))
        if kwargs.get('save_mode'):
            _save_path = _save_path.replace(self.image_suffix, ".{0}".format(kwargs.get('save_mode')).lower())
        image_handle.save(_save_path)
        return os.path.realpath(_save_path)

    def set_image_handle(self, image_path):
        if isinstance(image_path, (str, bytes)):
            if image_path and self.image_path != image_path:
                self.close()
                self.image_handle = self.open(image_path)
                self._image_basic_info(image_path)
            elif image_path:
                self._image_basic_info(image_path)
            else:
                pass
        elif isinstance(image_path, Image.Image):
            self.image_handle = image_path
        else:
            pass

    def _image_basic_info(self, image_path):
        if isinstance(image_path, (str, bytes)):
            # 图片路径
            self.image_path = image_path
            # 图片的存储目录
            self.default_save_dir = os.path.split(image_path)[0]
            # 图片的格式
            self.image_suffix = os.path.splitext(image_path)[-1]
            # 图片名
            self.image_name = os.path.split(image_path)[-1]

    def color(self, x, y):
        return self.image_handle.getpixel((x, y))

    def image_binaryzation(self, image_path='', threshold=0, auto_update=True, **kwargs):
        """图片二值化"""
        self.set_image_handle(image_path)
        # 图片转灰度
        # 黑（灰度为0, 白（灰度为255）
        grey_img = self.convert('L')
        # 二值化
        # 新建同样大小的白灰度图
        _binary_img = Image.new("L", self.size, 255)
        # 利用k均值法，动态更新阈值threshold
        # 简而言之一直找阈值两边的像素个数，然后更新阈值（两边灰度的平均值），直到像素个数稳定
        lt_count, gt_count = [0, 0], [0, 0]
        while auto_update:
            for x in grey_img.getdata():
                if x >= threshold:
                    gt_count[0] += x
                    gt_count[1] += 1
                else:
                    lt_count[0] += x
                    lt_count[1] += 1
            lt_threshold = (lt_count[0] // lt_count[1]) if lt_count[1] > 0 else 0
            gt_threshold = (gt_count[0] // gt_count[1]) if gt_count[1] > 0 else 0
            new_threshold = (lt_threshold + gt_threshold) / 2
            if threshold == new_threshold:
                break
            threshold = new_threshold
        # print("计算阈值为:{}".format(threshold))
        # 从上到下扫描图片颜色
        black, white = 0, 0
        for x in range(grey_img.width):
            for y in range(grey_img.height):
                pix = grey_img.getpixel((x, y))
                # 将原图中的颜色，如果该颜色小于阈值将其填充为黑色
                if pix < threshold:
                    _binary_img.putpixel((x, y), Colors.black)
                    black += 1
                else:
                    _binary_img.putpixel((x, y), Colors.white)
                    white += 1
        # print(list(binary_img.getdata()))
        # 默认背景色填充为白色，所以背景色数目应该比较多，如果黑色占多数则执行反相操作
        if black > white:
            print("reverse!")
            _binary_img = Image.fromarray(255 - np.array(_binary_img))
        if not kwargs.get('overwrite', False):
            kwargs['prefix'] = kwargs.get('prefix', 'binaryzation_')
        save_path = self.save(_binary_img, **kwargs)
        return save_path

    def image_remove_noise(self, image_path='', threshold=1, **kwargs):
        """图片二值化之后可以使用这个方法移除图片上的噪点
        适用于清除零丁的散落分布的噪点。
        原理：如果黑色像素周围八个方向的黑像素数目少于阈值threshold，
        则判断该点噪点并将颜色设置为白色。
        """
        self.set_image_handle(image_path)
        if threshold >= 4:
            # 因为该像素位置周围只有八个方向作为判断标准，阈值设置超过4，就失去意义
            threshold = 3
        # 设置颜色判断允许的色差 color_threshold
        color_threshold = kwargs.get('color_threshold', 20)
        # 先把四周的噪点去了
        for x in range(self.width):
            self.putpixel((x, 0), Colors.white)
            self.putpixel((x, self.height - 1), Colors.white)
        for x in range(self.height):
            self.putpixel((0, x), Colors.white)
            self.putpixel((self.width - 1, 0), Colors.white)
        # 遍历验证码图片
        for x in range(1, self.width - 1):
            for y in range(1, self.height - 1):
                # 如果是黑色，统计该像素点周围8像素，黑色的像素的个数
                if Colors.is_black(self.color(x, y), color_threshold):
                    count_noise = 0
                    for m in [x - 1, x, x + 1]:
                        for n in [y - 1, y, y + 1]:
                            if Colors.is_black(self.color(m, n), color_threshold):
                                count_noise += 1
                    if count_noise - 1 <= threshold:
                        self.putpixel((x, y), Colors.white)
                else:
                    # 如果是白色，周边的几乎都是黑像素（大于7时），将该位置设置为黑色
                    count_noise = 0
                    for m in [x - 1, x, x + 1]:
                        for n in [y - 1, y, y + 1]:
                            if Colors.is_black(self.color(m, n), color_threshold):
                                count_noise += 1
                    if count_noise - 1 > 7:
                        self.putpixel((x, y), Colors.black)
        if not kwargs.get('overwrite', False):
            kwargs['prefix'] = kwargs.get('prefix', 'noise_')
        save_path = self.save(**kwargs)
        return save_path

    def image_remove_noise_by_contours(self, image_path='', threshold=1, **kwargs):
        """图片二值化之后可以使用这个方法移除图片上的噪点，该方法也叫漫水填充法
        适用于去除相互连通的一整片的噪点区域。
        原理：标记相互连通的区域，区域像素数目少于设定的阈值，标识为噪点区域
        将该片噪点区域颜色设置为白色。
        """
        self.set_image_handle(image_path)
        area_list = []
        footprint = []
        color_threshold = kwargs.get('color_threshold', 20)

        # 利用深度优先搜索遍历图，获取连通域
        def flood_fill(m, n, area_tmp=None):
            visited = []
            # 将起始点的相邻点加入访问序列
            visit_seq = list(itertools.product(range(m - 1, m + 2), range(n - 1, n + 2)))
            keep_going = True
            while visit_seq or keep_going:
                keep_going = False
                point = visit_seq.pop(0)
                visited.append(point)
                if 0 <= point[0] < self.width and 0 <= point[1] < self.height and Colors.is_black(self.color(*point),
                                                                                                  color_threshold):
                    keep_going = True
                    area_tmp.append(point)
                    # 把这个点相邻的点加入到访问序列
                    next_seq = list(
                        itertools.product(range(point[0] - 1, point[0] + 2), range(point[1] - 1, point[1] + 2)))
                    visit_seq.extend([ns for ns in next_seq if ns not in visited and ns not in visit_seq])
            return visited

        # 遍历图片像素
        for x in range(0, self.width):
            for y in range(0, self.height):
                if (x, y) in footprint:
                    continue
                if Colors.is_black(self.color(x, y), color_threshold):
                    area = []
                    footprint.extend(flood_fill(x, y, area))
                    if area:
                        area_list.append(area)
        # 遍历所有连通域，连通域内黑色像素少于阈值的被识别为噪点
        for each in area_list:
            if len(each) < threshold:
                for position in each:
                    self.putpixel(position, Colors.white)
        if not kwargs.get('overwrite', False):
            kwargs['prefix'] = kwargs.get('prefix', 'noise_')
        save_path = self.save(**kwargs)
        return save_path

    def image_split(self, image_path='', **kwargs):
        """图片切割
        利用广度优先搜索算法，从一个像素点的四个方向漫延，触及与自身像素不同的点就停止，
        从而将独立字符像素范围获取到，据此切分图片。主要用来切分验证码图片。
        （目前该方法只能切分由image_black_and_white方法生成二值图）
        :param image_path: 传入图片文件对象或者路径
        """
        self.set_image_handle(image_path)
        color_threshold = kwargs.get('color_threshold', 20)
        left_border = False
        right_border = False
        letters = list()
        start, end = 0, 0
        for x in range(self.width):
            for y in range(self.height):
                # 遇到黑色像素说明碰到了边界
                if Colors.is_black(self.color(x, y), color_threshold):
                    left_border = True
                    break
            if left_border is True and right_border is False:
                right_border = True
                start = x - 1  # 往前一列切割就不会切到字符边缘

            if right_border is True and left_border is False:
                right_border = False
                end = x
                letters.append([start, end])

            if start > end and x == self.width - 1:
                # 防止最后一个字符因为在图片边缘无法切割到
                letters.append([start, self.width - 1])
            left_border = False
        # print(letters)
        # 去除切片过小的片段
        # 图片宽度小于width_limit，判断为无效切片
        width_limit = kwargs.get('width_limit', 0)
        if not isinstance(width_limit, int):
            width_limit = 0
        letters = [w for w in letters if w[1] - w[0] > width_limit]
        # 保留字符之间的空白
        if kwargs.get('keep_the_blank'):
            for i in range(len(letters) - 1):
                letters[i][1] = letters[i + 1][0]
            else:
                letters[-1][1] = self.width
        img_list = []
        for idx, letter in enumerate(letters):
            save_path = self.save(prefix="{}_".format(idx), **kwargs)
            img_split = self.crop((letter[0], 0, letter[1], self.height))
            img_split.save(save_path)
            img_list.append(save_path)
        return img_list

    # def images_split_by_x_project(self, image_path='', **kwargs):
    #     """通过投影法切割粘连的字符
    #     统计x轴上所有黑色元素的个数，个数少的表示连接薄弱，即有可能时粘连的位置
    #     """
    #     self.set_image_handle(image_path)
    #     color_threshold = kwargs.get('color_threshold', 20)
    #     x_project_count = [0] * self.width
    #     for x in range(self.width):
    #         for y in range(self.height):
    #             if Colors.is_black(self.color(x, y), color_threshold):
    #                 x_project_count[x] += 1
    #     print(x_project_count)
    #     # 找出X轴投影数目上升和下降之间的位置
    #     weak_points = []
    #     up_down = [0, 0]
    #     value_keeper, up, down, full_up_down_flag = 0, 0, 1, False
    #     for idx in range(len(x_project_count)):
    #         # 记录上升点
    #         if x_project_count[idx] > value_keeper:
    #             if not up_down[up]:
    #                 up_down[up] = idx
    #             elif full_up_down_flag:
    #                 full_up_down_flag = False
    #                 weak_points.append(up_down)
    #                 up_down = [0, 0]
    #         # 记录下降点
    #         if value_keeper > x_project_count[idx]:
    #             full_up_down_flag = True
    #             up_down[down] = idx
    #         value_keeper = x_project_count[idx]
    #     # 计算每个区间的颜色总数
    #     cut_point = []
    #     for each in weak_points:
    #         cut_point.append(sum(x_project_count[each[0]:each[1] + 1]))
    #     print(cut_point)

    def images_stitch(self, images, **kwargs):
        """横向拼接图片"""
        src_images = [self.open(x) for x in images]
        # 新图片尺寸，宽度为拼接的图片之和 + 间隙（防止拼接后字符粘连），高度取去高度最大的图片
        gap = kwargs.get('gap', 0)
        new_images_size = (sum([i.width for i in src_images]) + len(src_images) * gap, max([i.height for i in src_images]))
        # 创建白底图片
        target_img = Image.new("L", new_images_size, Colors.white)
        left, right = 0, 0
        for im in src_images:
            offset = im.size[0]
            target_img.paste(im, (left, 0, right + offset, im.size[1]))
            left += im.size[0] + gap
            right += im.size[0] + gap
        if kwargs.get('size'):
            return self.image_resize(target_img, overwrite=True, **kwargs)
        if not kwargs.get('overwrite', False):
            kwargs['prefix'] = kwargs.get('prefix', 'stitch_')
        save_path = self.save(target_img, **kwargs)
        return save_path

    def image_resize(self, image_path="", size=None, align="center", **kwargs):
        """如果给定的尺寸小于原图的尺寸，就通过缩放缩小图片。
        如果给定的尺寸大于原图尺寸，就往周围填补空白
        :param size:
        :param image_path:
        :type align: ['center', 'top_left', 'lower_right']
        """
        self.set_image_handle(image_path)
        if size[0] < self.width or size[1] < self.height:
            new_image = self.crop((0, 0, size[0], size[1]))
            save_path = self.save(new_image, **kwargs)
            return save_path
        new_image = Image.new("L", size, Colors.white)
        if align == 'top_left':
            box = (0, 0)
        elif align == 'lower_right':
            box = (int(size[0] - self.width), int(size[1] - self.height))
        else:
            box = (int((size[0] - self.width) / 2), int((self.height - size[1]) / 2))
        new_image.paste(self.image_handle, box)
        save_path = self.save(new_image, **kwargs)
        return save_path

    def image_to_vector(self, image_path=""):
        self.set_image_handle(image_path)
        return np.array(self.getdata())

    @staticmethod
    def cosine(imv1, imv2):
        if len(imv1) > len(imv2):
            pad_width = len(imv1) - len(imv2)
            imv2 = np.pad(imv2, (0, pad_width), 'constant', constant_values=0)
        else:
            pad_width = len(imv2) - len(imv1)
            imv1 = np.pad(imv1, pad_width, 'constant', constant_values=0)
        return 1 - pairwise_distances(imv1.reshape(1, -1), imv2.reshape(1, -1), metric="cosine")[0][0]


if __name__ == '__main__':
    pass
    # 测试图像匹配
    # image_a_in_b('images/examples_for_image_match/a2.png',
    #              'images/examples_for_image_match/b2.png', dev=True)

    # 验证码处理流程测试
    with CaptchaTool('images/examples_for_captcha/eyzo.png') as ct:
        # 以下方法都可以通过传入参数 save_dir, save_mode 定义图片存储的位置和格式
        # 1. 二值化
        b_img = ct.image_binaryzation()
        # 2. 去噪点
        # 2.1 通过简单8邻域统计去除噪点，可设置阈值threshold调整效果
        without_noise_simple = ct.image_remove_noise(image_path=b_img, threshold=3, overwrite=True)
        # 2.2 通过连通域清除整片的噪点区域，可设置阈值threshold调整效果
        without_noise = ct.image_remove_noise_by_contours(image_path=without_noise_simple, threshold=30, overwrite=True)
        # 3. 切割验证码
        # width_limit去掉小碎块，keep_the_blank保留字符之间的空白间隔，便于拼接时还原图片
        split_list = ct.image_split(image_path=without_noise, width_limit=10, keep_the_blank=True, color_threshold=3)
        print(split_list)
        # 4. 拼接字符
        stitch_img = ct.images_stitch(split_list)
        # 5. 设置图片大小
        ct.image_resize(image_path=stitch_img, size=(241, 55), align="lower_right")
        # 6. 计算切片图之间的空间向量夹角cosine
        img_v1 = ct.image_to_vector('images/examples_for_captcha/0_binaryzation_eyzo.png')
        img_v2 = ct.image_to_vector('images/examples_for_captcha/0_binaryzation_eyzo.png')
        print(ct.cosine(img_v1, img_v2))

