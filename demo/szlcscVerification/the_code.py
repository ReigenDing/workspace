#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Vin on 2017/9/28
import glob
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'D:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
tessdata_dir_config = '--tessdata-dir "D:\\Program Files (x86)\\Tesseract-OCR\\tessdata"'


def main():
    pics = glob.glob('*.jpg')
    for p in pics:
        image = Image.open(p)
        code = pytesseract.image_to_string(image, lang='eng', config=tessdata_dir_config)
        print(code, p)


if __name__ == '__main__':
    main()
