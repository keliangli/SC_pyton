#目的：实现接口处氨基酸分子形状的分析
#实现内容：1，在excel表格中填写计算得到的残基所处形状

import os
import xlrd
import xlwt
import re
import numpy
import math
from xlutils.copy import copy




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


def Print_PDB_content(pdb_file_name,interface_content):

    file_name = pdb_file_name +'.txt'
    Write_file_handle = open(file_name,'a')
    Write_file_handle.write(interface_content[:-1])
    Write_file_handle.write('\n')
    Write_file_handle.close()


def calcu_dis(coord_1,coord_2):

    coord_1_X = float(coord_1[0])
    coord_1_Y = float(coord_1[1])
    coord_1_Z = float(coord_1[2])
    coord_2_X = float(coord_2[0])
    coord_2_Y = float(coord_2[1])
    coord_2_Z = float(coord_2[2])


    Euclid_Dis = numpy.sqrt(((coord_1_X-coord_2_X)**2)+((coord_1_Y-coord_2_Y)**2)+((coord_1_Z-coord_2_Z)**2))

    return Euclid_Dis


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





def Calcu_PDB_CA_FC(Valid_ATOM_Num,interface_ACC_sum):

    Vint   = Valid_ATOM_Num * 20.1
    FC = interface_ACC_sum/Vint
    return FC




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
            atom_counter_8 = 0
            atom_counter_10 = 0
            atom_counter_12 = 0
            for key in atom_content_dir:
                coord_2 = (atom_content_dir[key][30:38],atom_content_dir[key][38:46],atom_content_dir[key][46:54])
                dis = calcu_dis(atom_ca_cood, coord_2)
                if dis < 8:
                    atom_counter_8 = atom_counter_8 + 1
                if dis < 10:
                    atom_counter_10 = atom_counter_10 + 1
                if dis < 12:
                    atom_counter_12 = atom_counter_12 + 1

            AA_interface_sum_8 = 0
            AA_interface_sum_10 = 0
            AA_interface_sum_12 = 0

            for j in range(nrows):
                AA_cell = table.row_values(j)
                if AA_cell[0] == 'ATOM' and \
                        AA_cell[1] != ' DA' and \
                        AA_cell[1] != ' DT' and \
                        AA_cell[1] != ' DG' and \
                        AA_cell[1] != ' DC' and \
                        AA_cell[1] != '  A' and \
                        AA_cell[1] != '  C' and \
                        AA_cell[1] != '  G' and \
                        AA_cell[1] != '  T' and \
                        AA_cell[1] != '  U' and \
                        AA_cell[1] != '  I':
                        AA_coordinate = (AA_cell[4], AA_cell[5], AA_cell[6])
                        dis = calcu_dis(atom_ca_cood, AA_coordinate)
                        if dis < 8:
                            AA_interface_sum_8 = AA_interface_sum_8 + float(AA_cell[9])
                        if dis < 10:
                            AA_interface_sum_10 = AA_interface_sum_10 + float(AA_cell[9])
                        if dis < 12:
                            AA_interface_sum_12 = AA_interface_sum_12 + float(AA_cell[9])

            FC_8  = Calcu_PDB_CA_FC(atom_counter_8,AA_interface_sum_8)
            FC_10 = Calcu_PDB_CA_FC(atom_counter_10,AA_interface_sum_10)
            FC_12 = Calcu_PDB_CA_FC(atom_counter_12,AA_interface_sum_12)

            # print(FC_12)

            if FC_12 < 0.3:
                shape_12 = "valley"
            elif FC_12 < 0.5:
                shape_12 = "flat"
            else:
                shape_12 = "peak"
            # print(shape_12)



            write_excel(file_name, i,14,(FC_12+FC_8+FC_10)/3)




