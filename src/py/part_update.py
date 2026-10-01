#!/usr/bin/env python2
__author__ = "Yadollah Shahryary Dizaji"
__title__ = "pipeline.py"
__description__ = "Running file for Pipeline."
__license__ = "GPL"
__version__ = "1.0.0"
__email__ = "shahryary@gmail.com"


import os, glob,logging
from configuration import rcolor, qucolor, ycolor
from globalParameters import *


def read_config_new(section, get_string,cfile):
    config = GrumpyConfigParser()
    config.optionxform = str
    config.read(cfile)
    val_str = config.get(section, get_string)
    return val_str


def replace_config_new(section, old_string, new_string,cfile):

    config = GrumpyConfigParser()
    config.optionxform = str
    config.read(cfile)
    config.set(section, old_string, new_string)
    with open(cfile, 'wb') as config_file:
        config.write(config_file)


def __update__():
    cwd = os.getcwd()
    currversion = read_config_new("GENERAL", "currversion","config/pipeline.conf")
    title("Checking for the new version...")
    print("\n")

    user = os.environ['HOME']

    cmd = 'wget -O '+user+'/tmpMeth.zip '+' https://github.com/jlab-code/MethylStar/archive/master.zip'
    unzip ='unzip -o '+user+'/tmpMeth.zip ' + '-d '+user+'/'
    #rename='mv '+user+'/MethylStar-master '+ user+'/tmpMtlStar'
    
    try:
        subprocess.call(cmd, shell=True)
        subprocess.call(unzip, shell=True)
        #subprocess.call(rename, shell=True)
    except Exception as e:
        logging.error(traceback.format_exc())
        message(2, "Something is going wrong... please run again. ")

    # checking version
    newConfig = user+'/MethylStar-master/config/pipeline.conf'
    newVer = read_config_new("GENERAL", "currversion", newConfig)

    if currversion == newVer:
        print(mcolor("The version of MethylStar is up-to-date."))
    else:
        print(mcolor("The new version of MethylStar is available.\n"))
        answer = query_yes_no("Do you want to update?", None)
        if answer:
            try:
                replace_config_new("GENERAL", "currversion", newVer, "config/pipeline.conf")
                cp = "cp " + cwd + "/config/pipeline.conf" + " " + newConfig
                subprocess.call(cp, shell=True)

                if read_config_new("GENERAL", "docker_mode", "config/pipeline.conf") == "true":
                    rm = "rm " + newConfig + ".Docker"
                    subprocess.call(rm, shell=True)

                cmd = "cp -rf " + user + "/MethylStar-master/*" + " " + cwd
                subprocess.call(cmd, shell=True)
                # ------------- remove files
                rm = "rm -r "+user+"/tmpMeth.zip"
                subprocess.call(rm, shell=True)
                # --------------------------
                print(ycolor("Restarting MethylStar ...\n"))
                print(qucolor("MethylStar updated. The new version is: "+newVer)+"\n")
                os.execl(sys.executable, sys.executable, *sys.argv)
            except Exception as e:
                logging.error(traceback.format_exc())
                message(2, "Something is going wrong... please run again. ")
        else:
            message(0, "Update canceled")
    message(0, ".....")