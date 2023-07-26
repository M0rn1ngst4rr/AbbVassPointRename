#read in file
import os
import re

path = 'C:/Projekte/AU40x_HK_Crashpaket_ARG3_Step2_VIBN/6590R01_Backup_test'
p_declare_list = ['    !**********************************************************', '    !*            Fuegepunkt-Deklarationen', '    !**********************************************************']
r_declare_list = ['    !**********************************************************', '    !*            Raumpunkt-Deklarationen', '    !**********************************************************']

class pointClass:
    spaces = "    "
    prename = "    LOCAL CONST robtarget"
    name = ""
    coordinates = ""

def getProcessPoints(lines):
    pattern = r"[N|C|K][Z|E][_][P|L][T|I][P|N]"
    points = list()
    for line in lines:
        if re.search(pattern, line) != None:
            # trim spaces at the start
            line = line.strip()
            # get after space
            splitted = line.split(" ")
            name = splitted[1].split(",")[0].split("\\")[0]
            points.append(name)
    return points

def getPoints(lines):
    pattern = "Move"
    points = list()
    for line in lines:
        if re.search(pattern, line) != None:
            # trim spaces at the start
            line = line.strip()
            # get after space
            splitted = line.split(" ")
            name = splitted[1].split(",")[0]
            points.append(name) 
    return points               

def getCoordiantes(lines):
    pattern = "LOCAL CONST robtarget"
    coordianteslist = list()
    for line in lines:
        if re.search(pattern, line) != None:
            # trim spaces at the start
            line = line.strip()
            spacesplited = line.split(" ")
            name = spacesplited[3].split(":")[0]
            coords = spacesplited[3].split(":")[1].replace("=","")
            point = pointClass()
            point.name = name
            point.coordinates = coords
            coordianteslist.append(point)
    return coordianteslist
    
def renameRPoints(lines, r_points, pre="x", step=10, start=10):
    file1 = lines
    p_number = start
    for point in r_points:
        p_name_new = f'{pre}{p_number}'
        for i, line in enumerate(file1):
            pattern = rf'{point}[:|,]'
            if re.search(pattern, line) != None:
                file1[i] = line.replace(point, p_name_new)
        p_number += step   
    return file1
        
 
def readfile(fpath):
    with open(fpath, 'r') as f:
        lines = f.readlines()
    return lines

def sort(file, p_declare, r_declare, p_points, ):
    new_file = file
    start = False
    ii = 0
    p_declare_done = False
    for i, line in enumerate(file):
        if i == 3:
            start = True
        if start == True:
            if ii <= 2 & p_declare_done == False:
                new_file[i] = p_declare[ii]
                if ii == 2:
                    p_declare_done = True
                ii += 1
        if p_declare_done:
            for p_point in p_points:
                pass
    
for file in os.listdir(path):
    if file.endswith(".mod"):
        filepath = os.path.join(path, file)
        org_file = readfile(filepath)
        points = getPoints(org_file)
        coordiantes = getCoordiantes(org_file)
        p_points = getProcessPoints(org_file)
        new_x_file = renameRPoints(org_file, points,"x",10,10)
        x_points = getPoints(new_x_file)
        new_file = renameRPoints(new_x_file, x_points,"p",10,10)
        print("done")
        

    