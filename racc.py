import os
import xlrd
import xlwt
import re
import numpy
import math
from xlutils.copy import copy
from A相对溶剂可及性查询 import check_pdb_RACC


def write_excel(excel_file,row,cloumn,content):

    # 打开想要更改的excel文件
    old_excel = xlrd.open_workbook(excel_file)
    # 将操作文件对象拷贝，变成可写的workbook对象
    new_excel = copy(old_excel)
    # 获得第一个sheet的对象
    ws = new_excel.get_sheet(0)
    # 写入数据
    ws.write(row, cloumn, content)
    # 另存为excel文件，并将文件命名
    new_excel.save(excel_file)





print("please input the pdb_excel path：")
PDB_excel_Path = input()
os.chdir(PDB_excel_Path)
print("you input pdb_excel path is :", os.getcwd())
Path_excel_listdir = os.listdir(PDB_excel_Path)



for file_name in Path_excel_listdir:
    print(file_name)
    data = xlrd.open_workbook(file_name)
    table = data.sheets()[0]
    nrows = table.nrows
    # 第一个循环将核苷酸骨架上的原子存储
    for i in range(nrows):
        ATOM_cell = table.row_values(i)
        ATOM_coordinate = (ATOM_cell[4], ATOM_cell[5], ATOM_cell[6])
        if ATOM_cell[0] == 'ATOM'and \
           ATOM_cell[1] != ' DA' and \
           ATOM_cell[1] != ' DT' and \
           ATOM_cell[1] != ' DG' and \
           ATOM_cell[1] != ' DC' and \
           ATOM_cell[1] != '  A' and \
           ATOM_cell[1] != '  C' and \
           ATOM_cell[1] != '  G' and \
           ATOM_cell[1] != '  T' and \
           ATOM_cell[1] != '  U' and \
           ATOM_cell[1] != '  I':
           ATOM_ACC = check_pdb_RACC(ATOM_cell[2],ATOM_cell[3],file_name[0:4])
           os.chdir(PDB_excel_Path)

           if ATOM_ACC:
               #write_excel(file_name, i, 9, ATOM_ACC[0])
               write_excel(file_name, i, 16, ATOM_ACC[0])
               #if ATOM_ACC[1] :
                   #write_excel(file_name, i, 15, ATOM_ACC[1])
           else:
               #write_excel(file_name, i, 9, 0)
               write_excel(file_name, i, 16, 0)