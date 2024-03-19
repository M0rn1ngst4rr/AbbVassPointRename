#read in file
import os
import re
import time

start_path=os.getcwd()
path = os.path.join(start_path, 'Modules')
p_declare_list = ['    !**********************************************************\n', '    !*            Fuegepunkt-Deklarationen\n', '    !**********************************************************\n']
r_declare_list = ['    !**********************************************************\n', '    !*            Raumpunkt-Deklarationen\n', '    !**********************************************************\n']

class pointClass:
    spaces = "    "
    prename = "LOCAL CONST robtarget"
    name = ""
    coordinates = ""

def getProcessPoints(lines):
    # SM, KE, CZ, KL, KE, RE, SearchLine, Off, pInPos, Move
    pattern = r"[N|C|K|S][Z|E|M][_][P|L][T|I][P|N]"
    pattern2 = r"Move"
    pattern3 = r"[S][e][a][r][c][h][L][I][N][_][M]"
    pattern4 = r"[O][f|F][f|F]"
    pattern5 = r"pInPos"
    pattern6 = r"[K][L][_][P|L][T|I][P|N]"
    pattern7 = r"[R][E][_][P|L][T|I][P|N]"
    points = list()
    for line in lines:
        if re.search(pattern, line, re.IGNORECASE) != None:
            # trim spaces at the start
            line = line.strip()
            # get after space
            splitted = line.split(" ")
            name = splitted[1].split(",")[0].split("\\")[0]
            if not points.__contains__(name):
                    points.append(name)
        elif re.search(pattern2, line, re.IGNORECASE) != None:
            test = re.search(pattern4, line, re.IGNORECASE)
            test2 = re.search(pattern5, line, re.IGNORECASE)
            if test != None:
                # trim spaces at the start
                line = line.strip()
                # get after space
                splitted = line.split(" ")
                name = splitted[1].split(",")[0].split("(")[1].split("\\")[0]
                if not points.__contains__(name):
                    points.append(name) 
            elif test2 != None:
                # trim spaces at the start
                line = line.strip()
                # get after space
                splitted = line.split(" ")
                name = splitted[1].split(",")[0].split("\\")[0]
                if not points.__contains__(name):
                    points.append(name) 
        elif re.search(pattern3, line, re.IGNORECASE) != None:
            # trim spaces at the start
            line = line.strip()
            # get after space
            splitted = line.split(" ")
            name = splitted[1].split(",")[0].split("\\")[0]
            if not points.__contains__(name):
                    points.append(name)
        elif re.search(pattern6, line, re.IGNORECASE):
            # trim spaces at the start
            line = line.strip()
            # get after space
            try:
                splitted = line.split(" ")
                test123 = splitted[1]
            except:
                splitted = line.split(",")
            name = splitted[1].split(",")[0].split("\\")[0]
            if not points.__contains__(name):
                    points.append(name)
        elif re.search(pattern7, line, re.IGNORECASE) != None:
            # trim spaces at the start
            line = line.strip()
            # get after space
            splitted = line.split(" ")
            # check if it has \start \end else do normal
            if len(splitted) > 1:
                name = splitted[1].split(",")[0].split("\\")[0]
                if not points.__contains__(name):
                    points.append(name)
            else:
                splitted2 = line.split(",")
                name = splitted2[1]
                if not points.__contains__(name):
                    points.append(name)
    return points

def getPoints(lines):
    pattern = "Move"
    pattern2 = r"[O][F][F][S]"
    pattern3 = r"pinpos"
    points = list()
    for line in lines:
        if re.search(pattern, line, re.IGNORECASE) != None:
            test1 = re.search(pattern2, line, re.IGNORECASE)
            test2 = re.search(pattern3, line, re.IGNORECASE)
            if test1 == None and test2 == None:
                # trim spaces at the start
                line = line.strip()
                # get after space
                splitted = line.split(" ")
                name = splitted[1].split(",")[0]
                if not points.__contains__(name):
                    points.append(name) 
    return points               

def getCoordiantes(lines):
    pattern = "LOCAL CONST robtarget"
    pattern2 = "LOCAL VAR robtarget"
    coordianteslist = list()
    for line in lines:
        if re.search(pattern, line, re.IGNORECASE) != None:
            # trim spaces at the start
            line = line.strip()
            spacesplited = line.split(" ")
            name = spacesplited[3].split(":")[0]
            coords = spacesplited[3].split(":")[1].replace("=","")
            point = pointClass()
            point.name = name
            point.coordinates = coords
            coordianteslist.append(point)
        elif re.search(pattern2, line, re.IGNORECASE) != None:
            # trim spaces at the start
            line = line.strip()
            spacesplited = line.split(" ")
            name = spacesplited[3].split(":")[0]
            coords = spacesplited[3].split(":")[1].replace("=","")
            point = pointClass()
            point.name = name
            point.coordinates = coords
            point.prename = "LOCAL VAR robtarget"
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

def sort(file, p_declare, r_declare, p_points, r_points, coordiantes):
    new_file = list()
    start_line = 0
    stop_line = 0
    start_pattern = r'[!][*]'
    stop_pattern = r'[p|!][r|#]'
    f_done = False
    r_done = False
    for i, line in enumerate(file):
        if bool(re.search(start_pattern, line, re.IGNORECASE)):
            if start_line == 0:
                start_line = i
        if bool(re.search(stop_pattern, line, re.IGNORECASE)):
            if stop_line == 0:
                stop_line = i - 1
                break
    for i, line in enumerate(file):
        if i >= start_line and i <= stop_line:
            if f_done == False:
                for l in p_declare:
                    new_file.append(l)
                for p in p_points:
                    for coord in coordiantes:
                        if bool(re.search(p, coord.name, re.IGNORECASE)):
                            new_file.append(f'{coord.spaces}{coord.prename} {coord.name}:={coord.coordinates}\n')
                            break
                new_file.append("\n")
                f_done = True
            elif r_done == False:
                for l in r_declare:
                    new_file.append(l)
                for r in r_points:
                    for coord in coordiantes:
                        if bool(re.search(r, coord.name, re.IGNORECASE)):
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
        
def findUnused(ppoints, rpoints, coords):
    unused = list()
    for coord in coords:
        found = False
        for p in ppoints:
            if coord.name == p:
                found = True
                break
        for p in rpoints:
            if coord.name == p:
                found = True
                break
        if not found:
            unused.append(coord.name)
    return unused

def cleanup(org_file, unused):
    new_file = list()
    for line in org_file:
        found = False
        for p in unused:
            if line.__contains__(p):
                found = True
        if not found:
            new_file.append(line)
    return new_file
    
for file in os.listdir(path):
    if file.endswith(".mod"):
        try:
            filepath = os.path.join(path, file)
            org_file = readfile(filepath)
            points = getPoints(org_file)
            coordiantes = getCoordiantes(org_file)
            p_points = getProcessPoints(org_file)
            unused = findUnused(p_points, points, coordiantes)
            cleaned_up = cleanup(org_file, unused)
            new_x_file = renameRPoints(cleaned_up, points,"x",10,10)
            x_points = getPoints(new_x_file)
            new_file = renameRPoints(new_x_file, x_points,"p",10,10)
            new_points = getPoints(new_file)
            new_coordiantes = getCoordiantes(new_file)
            test_file = sort(new_file, p_declare_list, r_declare_list, p_points, new_points, new_coordiantes)
            writeNewFile(path, file, test_file)
            print("done")
        except Exception as e:
            print(f"Problem in File: {file} -> {e}")
            try:
                os.makedirs(f"{start_path}/logs")
            except:
                print("logs allready exists")
            timestr = time.strftime("%Y%m%d_%H%M%S")
            with open(f"{start_path}/logs/{timestr}_error.txt", 'a') as f:
                f.write(f"Problem in File: {file} -> {e}\n")
