
#目的：实现接口处氨基酸分子形状的分析
#实现内容：1，在excel表格中填写计算得到的残基所处形状

import os
import xlrd
import xlwt
import re
import numpy
import math
from xlutils.copy import copy


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



def find_atom_pdb(file_excel_name):

    file_name = file_excel_name +'.pdb'
    file_handle = open(file_name, 'r')
    atom_content_dir = {}
    counter = 0
    for file_content in file_handle:
        if file_content[0:4] == 'ATOM'and \
            file_content[17:20] != ' DA' and \
            file_content[17:20] != ' DT' and \
            file_content[17:20] != ' DG' and \
            file_content[17:20] != ' DC' and \
            file_content[17:20] != '  A' and \
            file_content[17:20] != '  C' and \
            file_content[17:20] != '  G' and \
            file_content[17:20] != '  T' and \
            file_content[17:20] != '  U' and \
            file_content[17:20] != '  I':
            atom_content_dir[counter] = file_content
            counter = counter + 1

    return atom_content_dir



print("please input the pdb_excel path：")
PDB_excel_Path = input()
os.chdir(PDB_excel_Path)
print("you input pdb_excel path is :", os.getcwd())
Path_excel_listdir = os.listdir(PDB_excel_Path)



print("please input the pdb path：")
PDB_Path = input()
print("you input pdb_excel path is :", os.getcwd())
Path_pdb_listdir = os.listdir(PDB_Path)



for file_name in Path_excel_listdir:

    data = xlrd.open_workbook(file_name)
    table = data.sheets()[0]
    nrows = table.nrows
    file_counter = 0
    min_dis = 1000
    min_dis_atom_buff = 0

    print(file_name)
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
           ATOM_cell[1] != '  I' :
            atom_ca_cood = (ATOM_cell[4],ATOM_cell[5],ATOM_cell[6])
            os.chdir(PDB_Path)
            atom_content_dir = find_atom_pdb(file_name[0:4])
            os.chdir(PDB_excel_Path)
            b_factor_sum = 0
            b_factor_counter = 0
            for key in atom_content_dir:
                if (ATOM_cell[2] == atom_content_dir[key][21:22])and(ATOM_cell[3] == atom_content_dir[key][22:26]):
                    pdb_content = atom_content_dir[key][61:70]
                    b_factor_sum = b_factor_sum + float(pdb_content)
                    b_factor_counter = b_factor_counter + 1

            write_excel(file_name, i, 17, b_factor_sum/b_factor_counter)
