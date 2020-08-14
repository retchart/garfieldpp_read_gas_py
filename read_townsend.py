'''
Title:      read_townsend.py
Author:     Liu Lixing, PhD, 
            Tsinghua University
            liulx18@mails.tsinghua.edu.cn
Abstract:   Read the electron's townsend coefficient of the gas file generated by 
            garfield++.
'''

import numpy as np
import matplotlib.pyplot as plt
import re
import math

# read gas file
def read_gas(file):
    f0 = open(file, 'r')
    lines = f0.readlines()
    f0.close()

    # parse gas charactors
    temparature = 300.
    pressure = 760.
    tab2d = 0
    nE = 1
    nB = 1
    nA = 1
    nexitation = 1
    nionisation = 1
    len_data_one = 0
    len_data = 0
    data = []
    data_flag = 0
    ndata_row = 0

    # read data array
    for i in range(len(lines)):
        if(not data_flag):
            tmp_list = lines[i].strip().split(':')
            if(tmp_list[0].strip() == "Identifier"):
                print(tmp_list[1])
                tmp_list1 = tmp_list[1].split(",")
                for j in range(len(tmp_list1)):
                    if(tmp_list1[j].strip()[0] == 'T'):
                        tmp_list2 = tmp_list1[j].split('=')
                        tmp_list3 = tmp_list2[1].split()
                        val = float(tmp_list3[0])
                        unit = tmp_list3[1]
                        temparature = val
                    if(tmp_list1[j].strip()[0] == 'p'):
                        tmp_list2 = tmp_list1[j].split('=')
                        tmp_list3 = tmp_list2[1].split()
                        val = float(tmp_list3[0])
                        unit = tmp_list3[1]
                        if(unit == "torr"):
                            pressure = val
                        elif(unit == "atm"):
                            pressure = val * 760.
            if(tmp_list[0].strip() == "Dimension"):
                tmp_list1 = tmp_list[1].split()
                if(tmp_list1[0] == "F"):
                    tab2d = 0
                elif(tmp_list1[0] == "T"):
                    tab2d = 1
                nE = int(tmp_list1[1])
                nA = int(tmp_list1[2])
                nB = int(tmp_list1[3])
                nexitation = int(tmp_list1[4])
                nionisation = int(tmp_list1[5])
                len_data = nE * nA * nB
                if(tab2d):
                    len_data_one = 3 + 5 + 3 + 6 * 2 + nexitation * 2 \
                        + nionisation * 2 
                else:
                    len_data_one = 6 + 9 + 6 + 6 * 2 + nexitation * 2 \
                        + nionisation * 2
                print("tab2d=%d, nE=%d, nA=%d, nB=%d\n" %(tab2d, nE, nA, nB))
            if(tmp_list[0].strip() == "E fields"):
                efield = np.zeros((nE))
                efield_data = []
                n_columns_efield = 5
                segment_length = 15
                for j in range(math.ceil(nE / n_columns_efield)):
                    tmp_list1 = re.findall(r".{15}", lines[i + j + 1])
                    efield_data += tmp_list1
                for j in range(nE):
                    efield[j] = float(efield_data[j].strip())
            if(tmp_list[0].strip() == "E-B angles"):
                e_b_angles = np.zeros((nA))
                e_b_data = []
                n_columns_e_b = 5
                segment_length = 15
                for j in range(math.ceil(nA / n_columns_e_b)):
                    tmp_list1 = re.findall(r".{15}", lines[i + j + 1])
                    e_b_data += tmp_list1
                for j in range(nA):
                    e_b_angles[j] = float(e_b_data[j].strip())
            if(tmp_list[0].strip() == "B fields"):
                bfield = np.zeros((nB))
                bfield_data = []
                n_columns_bfield = 5
                segment_length = 15
                for j in range(math.ceil(nB / n_columns_bfield)):
                    tmp_list1 = re.findall(r".{15}", lines[i + j + 1])
                    bfield_data += tmp_list1
                for j in range(nB):
                    bfield[j] = float(bfield_data[j].strip())

            if(tmp_list[0].strip() == "The gas tables follow"):
                data_flag = 1
                len_data_one_tmp = 0
                len_data_tmp = 0
                data_one = []
        else:
            segment_length = 15
            tmp_list = re.findall(r".{15}", lines[i])
            for j in range(len(tmp_list)):
                data_one.append(float(tmp_list[j]))
            len_data_one_tmp += len(tmp_list)
            if(len_data_one_tmp >= len_data_one):
                data.append(data_one)
                data_one = []
                len_data_tmp += 1
                len_data_one_tmp = 0
                if(len_data_tmp >= len_data):
                    break

    # parse data
    velocitye = np.zeros((nE, nA, nB), dtype=float)
    diffusionl = np.zeros((nE, nA, nB), dtype=float)
    diffusiont = np.zeros((nE, nA, nB), dtype=float)
    alpha = np.zeros((nE, nA, nB), dtype=float)
    alpha0 = np.zeros((nE, nA, nB), dtype=float)
    eta = np.zeros((nE, nA, nB), dtype=float)
    for l in range(nE):
        for m in range(nA):
            for n in range(nB):
                if(tab2d):
                    velocitye[l][m][n] = data[l* nA * nB + m * nB + n][0]
                    diffusionl[l][m][n] = data[l* nA * nB + m * nB + n][3]
                    diffusiont[l][m][n] = data[l* nA * nB + m * nB + n][4]
                    alpha[l][m][n] = data[l* nA * nB + m * nB + n][5]
                    alpha0[l][m][n] = data[l* nA * nB + m * nB + n][6]
                    eta[l][m][n] = data[l* nA * nB + m * nB + n][7]
                else:
                    velocitye[l][m][n] = data[l* nA * nB + m * nB + n][0]
                    diffusionl[l][m][n] = data[l* nA * nB + m * nB + n][6]
                    diffusiont[l][m][n] = data[l* nA * nB + m * nB + n][8]
                    alpha[l][m][n] = data[l* nA * nB + m * nB + n][10]
                    alpha0[l][m][n] = data[l* nA * nB + m * nB + n][12]
                    eta[l][m][n] = data[l* nA * nB + m * nB + n][13]

    return pressure, efield, velocitye, diffusionl, diffusiont, alpha, alpha0, eta

gas_file = ["ar_1atm.gas", "ch4_1atm.gas", "ic4h10_1atm.gas", "dme_1atm.gas", "co2_1atm.gas", "cf4_1atm.gas", "bf3_1atm.gas"]
pressure = [0. for i in range(len(gas_file))]
efield = [[]for i in range(len(gas_file))]
efield_plot = [[]for i in range(len(gas_file))]
velocitye = [[]for i in range(len(gas_file))]
diffusionl = [[]for i in range(len(gas_file))]
diffusiont = [[]for i in range(len(gas_file))]
diffusiont_plot = [[]for i in range(len(gas_file))]
alpha = [[]for i in range(len(gas_file))]
alpha0 = [[]for i in range(len(gas_file))]
eta = [[]for i in range(len(gas_file))]
alpha_plot = [[]for i in range(len(gas_file))]
alpha0_plot = [[]for i in range(len(gas_file))]

for i in range(len(gas_file)):
    (pressure[i], efield[i], velocitye[i], diffusionl[i], diffusiont[i], alpha[i], alpha0[i], eta[i]) = \
        read_gas(gas_file[i])

    # convert data from torr to atm
    efield_plot[i] = efield[i] * 760.
    alpha_plot[i] = np.exp(alpha[i][:,0,0] + math.log(760))
    alpha0_plot[i] = np.exp(alpha0[i][:,0,0] + math.log(760))
    # plot data
    plt.plot(efield_plot[i], alpha_plot[i], "-o", label="%s" %(gas_file[i]))
plt.xlabel("Reduced electric field (E/cm/atm)")
plt.xscale("log")
plt.xlim(1e3, 1e5)
plt.ylabel("Townsend coefficient (1/cm)")
plt.yscale("log")
plt.ylim(1, 1e4)
plt.legend()
plt.show()

# save data 
f1 = open("read_townsend.txt", "w")
f1.write("E/p")
for i in range(len(gas_file)):
    f1.write("," + gas_file[i])
f1.write("\n")
for i in range(len(efield_plot[0])):
    f1.write("%.2e" %(efield_plot[0][i]))
    for j in range(len(gas_file)):
        f1.write(", %.2e" %(alpha_plot[j][i]))
    f1.write("\n")
    
f1.close()

print("OK")

x = [143.8, 100]
y = [0.02098, 0.02402]
x_interp = np.interp(0.02, y, x)
print(x_interp)