#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Vin on 2017/8/17

from PyPDF2 import PdfFileReader, PdfFileWriter


def main():
    pdf = PdfFileReader(file('tt.pdf', 'rb'), strict=False)
    print pdf.getFields({''})


if __name__ == '__main__':
    main()
