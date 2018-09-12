import os
import xlrd
import xlwt
import re
import numpy
import math
from xlutils.copy import copy
import re
import os
import xlrd
from xlrd import open_workbook
from xlutils.copy import copy

path = r"E:\SV文件\1.xls"
def excel_write(row, column, content):
    rb = open_workbook(path)
    # 复制
    wb = copy(rb)
    # 选取表单
    s = wb.get_sheet(0)
    # 写入数据
    s.write(row, column, content)
    # 保存
    wb.save(path)



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
    row_num = 0
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

           os.chdir(PDB_excel_Path)
           racc = float(ATOM_cell[16])
           #if  ATOM_cell[7]:
           if racc >0.10:
               #写RACC
               excel_write(row_num, 0, ATOM_cell[16])
               #写ACC
               excel_write(row_num, 1, ATOM_cell[9])
               #写B_factor
               excel_write(row_num, 2, ATOM_cell[17])

               #3层
               for i in range(9):
                    FCX =  float(ATOM_cell[19+i]) + float(ATOM_cell[20+i]) + float(ATOM_cell[21+i])
                    excel_write(row_num, 4+i, FCX/3)
               #4层
               for i in range(8):
                    FCX =  float(ATOM_cell[19+i]) + float(ATOM_cell[20+i]) + float(ATOM_cell[21+i]) + float(ATOM_cell[22+i])
                    excel_write(row_num, 15+i, FCX/4)
               #5层
               for i in range(7):
                    FCX =  float(ATOM_cell[19+i]) + float(ATOM_cell[20+i]) + float(ATOM_cell[21+i]) + float(ATOM_cell[22+i]) + float(ATOM_cell[23+i])
                    excel_write(row_num, 24+i, FCX/5)
               #6层
               for i in range(6):
                    FCX =  float(ATOM_cell[19+i]) + float(ATOM_cell[20+i]) + float(ATOM_cell[21+i]) + float(ATOM_cell[22+i]) + float(ATOM_cell[23+i]) + float(ATOM_cell[24+i])
                    excel_write(row_num, 32+i, FCX/6)
               #7层
               for i in range(5):
                    FCX =  float(ATOM_cell[19+i]) + float(ATOM_cell[20+i]) + float(ATOM_cell[21+i]) + float(ATOM_cell[22+i]) + float(ATOM_cell[23+i]) + float(ATOM_cell[24+i]) + float(ATOM_cell[25+i])
                    excel_write(row_num, 39+i, FCX/7)
               #8层
               for i in range(4):
                    FCX =  float(ATOM_cell[19+i]) + float(ATOM_cell[20+i]) + float(ATOM_cell[21+i]) + float(ATOM_cell[22+i]) + float(ATOM_cell[23+i]) + float(ATOM_cell[24+i]) + float(ATOM_cell[25+i]) + float(ATOM_cell[26+i])
                    excel_write(row_num, 45+i, FCX/8)

               excel_write(row_num, 56, ATOM_cell[22])
               row_num = row_num + 1
               #if ATOM_ACC[1] :
                   #write_excel(file_name, i, 15, ATOM_ACC[1])