#!/usr/bin/env python2
__author__ = "Yadollah Shahryary Dizaji"
__title__ = "run.py"
__description__ = "Running main menu."
__license__ = "GPL"
__version__ = "1.0.0"
__email__ = "shahryary@gmail.com"

import sys
import os
import subprocess
import shutil
import pwd

from src.py.pipeline import rcolor, ycolor, qucolor,mcolor
# Main definition - constants
menu_actions = {}


def get_username():
    return pwd.getpwuid(os.getuid())[0]
# =======================
#     checking lib packages
# =======================


ToNULL = open(os.devnull, 'w')
try:
    detected_parallel_location = subprocess.check_output(['which', 'parallel'])
except subprocess.CalledProcessError:
    user = get_username()
    subprocess.call(["cp", "./src/bash/ins_parallel.sh", '/home/' + user + '/'])
    subprocess.call(['chmod', '0755', '/home/' + user + '/ins_parallel.sh'])
    subprocess.call(['sh', '/home/' + user + '/ins_parallel.sh'])
    os.remove('/home/' + user + '/ins_parallel.sh')
try:
    os.remove('/home/' + user + '/parallel-20190122.tar.bz2')
    os.remove('/home/' + user + '/parallel-20190122.tar.bz2.sig')
    shutil.rmtree('/home/' + user + '/parallel-20190122')
    shutil.rmtree('/home/' + user + '/share')
except Exception as e:
    pass
'''
try:
    if not found:
        main(['install', "--user", "npyscreen"])
        #restart_program()
except Exception as e:
    logging.error(traceback.format_exc())
'''
# =======================
#     MENUS FUNCTIONS
# =======================


# Main menu
def main_menu():
    print("=="*25)
    print(ycolor("\n\tWelcome to MethylStar\n"))
    print("=="*25)
    print("Please choose from the menu:\n")
    print(ycolor("\t1.")+" Run Pipeline (WGBS)")
    print(ycolor("\t2.")+" Outputs/Reports")
    print(ycolor("\t3.")+" Access JBrowse")
    print(ycolor("\t4.")+" Clean-up files")
    print(ycolor("\t5.")+" Help\n")
    print(ycolor("\tC.")+" Configuration")
    print(rcolor("Q.")+" Quit\n")
    choice = raw_input(">>  ")
    exec_menu(choice)

    return


# Execute menu
def exec_menu(choice):
    #os.system('clear')
    ch = choice #.lower()
    if ch == '':
        menu_actions['main_menu']()
    else:
        try:
            menu_actions[ch]()
        except KeyError:
            print("Invalid selection, please try again.\n")
            menu_actions['main_menu']()
    return


def run_pipeline():
    from src.py.pipeline import __pipeline__
    __pipeline__()
    menu_actions['main_menu']()


def run_output():

    from src.py.part_output import __dmr__
    __dmr__()
    menu_actions['main_menu']()

def jbrowse():
    s = "\nAccess Jbrowse\n"
    s += "Please open the following URL in your web browser:\n"
    s += "http://jlabdata.org/jbrowse\n\n"
    print(qucolor(s))
    menu_actions['main_menu']()

def help_doc():
    s = "\nDocumentation:\n"
    s += "Please open the following URL in your web browser:\n"
    s += "https://github.com/jlab-code/MethylStar/blob/master/docs/runPipeline.md\n\n"
    print(qucolor(s))
    menu_actions['main_menu']()

def run_remove():
    from src.py.part_removing import __removing__
    __removing__()
    menu_actions['main_menu']()



def config():
    from src.py.configuration import __running__
    __running__()
    menu_actions['main_menu']()


# Back to main menu
def back():
    menu_actions['main_menu']()


# Exit program
def exit():
    sys.exit()


# =======================
#    MENUS DEFINITIONS
# =======================

# Menu definition
menu_actions = {
    'main_menu': main_menu,
    '1': run_pipeline,
    '2': run_output,
    '3': jbrowse,
    '4': run_remove,
    '5': help_doc,
    '9': back,
    'c': config,
    'q': exit,
}



# =======================
#      MAIN PROGRAM
# =======================

# Main Program
if __name__ == "__main__":
    # Launch main menu
    main_menu()
