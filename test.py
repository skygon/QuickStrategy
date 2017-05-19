# -*- coding: utf-8 -*-
import os
import xlrd

xlrd.Book.encoding = "utf8"
book = xlrd.open_workbook(r".\tmp_data\sh600010.xls")
sheet = book.sheet_by_index(0)

rows = sheet.nrows
cols = sheet.ncols

print rows, cols