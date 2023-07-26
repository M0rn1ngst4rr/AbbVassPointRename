#read in file
import os
import re

path = 'C:/Projekte/AU40x_HK_Crashpaket_ARG3_Step2_VIBN/6590R01_Backup_test'
p_declare_list = ['    !**********************************************************\n', '    !*            Fuegepunkt-Deklarationen\n', '    !**********************************************************\n']
r_declare_list = ['    !**********************************************************\n', '    !*            Raumpunkt-Deklarationen\n', '    !**********************************************************\n']

class pointClass:
    spaces = "    "
    prename = "LOCAL CONST robtarget"
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
            # file deepcode ignore change_to_is: <please specify a reason of ignoring this>
            if re.search(pattern, line) != None:
                file1[i] = line.replace(point, p_name_new)
        p_number += step   
    return file1
        
 
def readfile(fpath):
    with open(fpath, 'r') as f:
        lines = f.readlines()
    return lines

def sort(file, p_declare, r_declare, p_points, r_points, coordiantes):
    new_file = list()
    start_line = 0
    stop_line = 0
    start_pattern = r'[!][*]'
    stop_pattern = r'[p|!][r|#]'
    f_done = False
    r_done = False
    for i, line in enumerate(file):
        if bool(re.search(start_pattern, line)):
            if start_line == 0:
                start_line = i
        if bool(re.search(stop_pattern, line)):
            if stop_line == 0:
                stop_line = i
                break
    for i, line in enumerate(file):
        if i >= start_line and i <= stop_line:
            if f_done == False:
                for l in p_declare:
                    new_file.append(l)
                for p in p_points:
                    for coord in coordiantes:
                        if bool(re.search(p, coord.name)):
                            new_file.append(f'{coord.spaces}{coord.prename} {coord.name}:={coord.coordinates}\n')
                            break
                new_file.append("\n")
                f_done = True
            elif r_done == False:
                for l in r_declare:
                    new_file.append(l)
                for r in r_points:
                    for coord in coordiantes:
                        if bool(re.search(r, coord.name)):
                            new_file.append(f'{coord.spaces}{coord.prename} {coord.name}:={coord.coordinates}\n')
                            break
                new_file.append("\n")
                r_done = True
        else:
            new_file.append(line)
    return new_file
            
def writeNewFile(prepath, path, lines):
    pre = f"{prepath}/new/"
    try:
        os.makedirs(pre)
    except:
        print("folder already exists")
    file = os.path.join(pre, path)
    with open(file, 'w') as f:
        f.writelines(lines)
    
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
        new_points = getPoints(new_file)
        new_coordiantes = getCoordiantes(new_file)
        test_file = sort(new_file, p_declare_list, r_declare_list, p_points, new_points, new_coordiantes)
        writeNewFile(path, file, test_file)
        print("done")
        

    