#!/usr/bin/env python2
__author__ = "Yadollah Shahryary Dizaji"
__title__ = "run.py"
__description__ = "Running main menu."
__license__ = "GPL"
__version__ = "1.0.0"
__email__ = "shahryary@gmail.com"



import sys
import traceback
import logging
from src.py.pipeline import rcolor,ycolor
import imp
# Main definition - constants
menu_actions = {}


# =======================
#     checking lib packages
# =======================
try:
    import importlib
    from pip import main
except:
    from pip._internal import main

try:
    imp.find_module('npyscreen')
    found = True
except ImportError:
    found = False


try:
    if not found:
        main(['install', "npyscreen"])
except Exception as e:
    logging.error(traceback.format_exc())
finally:
    globals()["npyscreen"] = importlib.import_module("npyscreen")



# =======================
#     MENUS FUNCTIONS
# =======================

# Main menu
def main_menu():
    print "=="*25
    print "\nWelcome,\n"
    print "Please choose the menu you want to start:\n"
    print ycolor("1.")+" Run Pipeline"
    print ycolor("2.")+" Run DMR Calling"
    print ycolor("3.")+" Run Jbrowser"
    print ycolor("4.")+" Outputs/ Reports"
    print ycolor("5.")+" Help\n"
    print ycolor("C.")+ " Configuration"
    print rcolor("Q.")+" Quit\n"
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
            print "Invalid selection, please try again.\n"
            menu_actions['main_menu']()
    return

def run_pipeline():
    from src.py.pipeline import __pipeline__
    __pipeline__()
    menu_actions['main_menu']()


def run_dmr():

    from  src.py.dmr import __dmr__
    __dmr__()
    menu_actions['main_menu']()



# Menu 2
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
    '2': run_dmr,
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