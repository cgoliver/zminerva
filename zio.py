import pickle

import os, json
from os.path import isdir, abspath, isfile

def zprompt(text=""):
    i=""
    while not i:
        if text:
            print(text)
        i=input(": ")
    return i

def zread_json(path,verbose=1):
    data=zread(path,verbose)
    try:
        return json.loads(data)
    except:
        if verbose:
            print("Failed to convert file to json.")
        return 0

def zwrite_json(data,path,verbose=1):
    try:
        dump=json.dumps(data)
    except:
        if verbose:
            print("Failed to convert data into json.")
        return 0
    
    return zwrite(dump,path,verbose)

def zpickle(data,path,verbose=1):
    path=abspath(path)
    
    directory = "/".join(path.split("/")[:-1])
    
    if directory:
        zmkdir(directory)
    
    with open(path, "wb") as f:
        pickle.dump(data,f)
        
    if verbose:
        print("Wrote pickled object to:")
        print(path)

def zread(path,verbose=1):
    if not os.path.isfile(path):
        if verbose:
            print("File does not exist: %s"%path)
        return 0
    
    with open(path,"r") as f:
        return f.read()

def zwrite(data,path,verbose=0):
    path=abspath(path)
    
    directory = "/".join(path.split("/")[:-1])
    
    if directory:
        zmkdir(directory)
    
    with open(path, "w") as f:
        f.write(data)
        
    if verbose:
        print("Wrote data to:")
        print(path)
    return 1

def zmkdir(folderpath):
    try:
        os.makedirs(folderpath)
    except:
        pass
    
    if not isdir(folderpath):
        raise IOError("Could not create necessary directory for whatever reason...")

def zwrite_append(data,path,suffix="",verbose=0):
    """where path is /home/zulban/filename"""
    query=path.split("/")[-1]
    directory=path
    while directory and directory[-1]!="/":
        directory=directory[:-1]
    scandic=zscan_folder(query,directory)
    digit=scandic["digit"]
    filename=scandic["nextname"]
    zwrite(data,directory+filename+suffix,verbose=verbose)
    return digit+1

def zscan_folder(searchterm, path):
    """returns the filename of the file with the largest appended
    number that also contains searchterm"""
    try:
        paths = [i for i in os.listdir(path) if searchterm in i]
    except:
        paths=[]
    lastname = ""
    lastdigit = 0
    for p in paths:
        digit = p.split("-")[-1].split(".")[0]
        if digit.isdigit() and int(digit) > lastdigit:
            lastname = p
            lastdigit = int(digit)
    
    if not lastname:
        lastname=searchterm+"-1"
    
    nextname=lastname.split("-")[0]+"-%s"%(lastdigit+1)
    
    return {"lastname":lastname,"digit":lastdigit,"nextname":nextname}

def zcount_files(path):
    counter=0
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            counter+=1
        
    return counter
