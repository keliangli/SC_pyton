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




def Calcu_PDB_CA_SI(Valid_ATOM_Num,r):

    Vint   = Valid_ATOM_Num * 20.1
    Vsphere= 4*math.pi*r**3/3
    Vext   = Vsphere - Vint
    CX = (Vext-Vint)/Vsphere
    return CX



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
            atom_4_counter = 0
            atom_6_counter = 0
            atom_8_counter = 0
            atom_10_counter = 0
            atom_12_counter = 0
            atom_14_counter = 0
            atom_16_counter = 0
            atom_18_counter = 0
            atom_20_counter = 0
            atom_22_counter = 0
            atom_24_counter = 0
            atom_26_counter = 0
            for key in atom_content_dir:
                coord_2 = (atom_content_dir[key][30:38],atom_content_dir[key][38:46],atom_content_dir[key][46:54])
                dis = calcu_dis(atom_ca_cood, coord_2)
                if dis < 4:
                    atom_4_counter = atom_4_counter + 1
                if dis < 6:
                    atom_6_counter = atom_6_counter + 1
                if dis < 8:
                    atom_8_counter = atom_8_counter + 1
                if dis < 10:
                    atom_10_counter = atom_10_counter + 1
                if dis < 12:
                    atom_12_counter = atom_12_counter + 1
                if dis < 14:
                    atom_14_counter = atom_14_counter + 1
                if dis < 16:
                    atom_16_counter = atom_16_counter + 1
                if dis < 18:
                    atom_18_counter = atom_18_counter + 1
                if dis < 20:
                    atom_20_counter = atom_20_counter + 1
                if dis < 22:
                    atom_22_counter = atom_22_counter + 1
                if dis < 24:
                    atom_24_counter = atom_24_counter + 1
                if dis < 26:
                    atom_26_counter = atom_26_counter + 1
            CX_4 = Calcu_PDB_CA_SI(atom_12_counter, 4)
            CX_6 = Calcu_PDB_CA_SI(atom_10_counter, 6)
            CX_8 = Calcu_PDB_CA_SI(atom_8_counter, 8)
            CX_10 = Calcu_PDB_CA_SI(atom_12_counter, 10)
            CX_12 = Calcu_PDB_CA_SI(atom_10_counter, 12)
            CX_14 = Calcu_PDB_CA_SI(atom_8_counter, 14)
            CX_16 = Calcu_PDB_CA_SI(atom_12_counter, 16)
            CX_18 = Calcu_PDB_CA_SI(atom_10_counter, 18)
            CX_20 = Calcu_PDB_CA_SI(atom_8_counter, 20)
            CX_22 = Calcu_PDB_CA_SI(atom_12_counter, 22)
            CX_24 = Calcu_PDB_CA_SI(atom_10_counter, 24)
            CX_26 = Calcu_PDB_CA_SI(atom_8_counter, 26)

            write_excel(file_name, i, 19, CX_4)
            write_excel(file_name, i, 20, CX_6)
            write_excel(file_name, i, 21, CX_8)
            write_excel(file_name, i, 22, CX_10)
            write_excel(file_name, i, 23, CX_12)
            write_excel(file_name, i, 24, CX_14)
            write_excel(file_name, i, 25, CX_16)
            write_excel(file_name, i, 26, CX_18)
            write_excel(file_name, i, 27, CX_20)
            write_excel(file_name, i, 28, CX_22)
            write_excel(file_name, i, 29, CX_24)
            write_excel(file_name, i, 30, CX_26)



            # if CX_12 < -0.2:
            #     shape_12 = "valley"
            # elif CX_12 < 0.2:
            #     shape_12 = "flat"
            # else:
            #     shape_12 = "peak"
            #
            # if CX_10 < -0.2:
            #     shape_10 = "valley"
            # elif CX_10 < 0.2:
            #     shape_10 = "flat"
            # else:
            #     shape_10 = "peak"
            #
            #
            # if CX_8 < -0.2:
            #     shape_8 = "valley"
            # elif CX_8 < 0.2:
            #     shape_8 = "flat"
            # else:
            #     shape_8 = "peak"



            #write_excel(file_name, i, 10,CX_12)
            # write_excel(file_name, i, 14,(CX_10+CX_12+CX_8)/3)
