#!/usr/bin/env python
__author__ = "Yadollah Shahryary Dizaji"
__title__ = "setup.py"
__description__ = "Setup file for Pipeline."
__license__ = "GPL"
__version__ = "1.0.0"
__email__ = "shahryary@gmail.com"


import os, glob
from globalParameters import *

# =======================
#     MENUS FUNCTIONS
# =======================
menu_remove = {}


# Main menu
def rem_menu():
    print "=="*25
    print "Please choose from the menu:\n"
    print ycolor("\t1.")+" Clean Trimmomatic/log file(s)."
    print ycolor("\t2.")+" Clean Qc-fastq-report/log file(s)."
    print ycolor("\t3.")+" Clean bismark mapper/log file(s)."
    print ycolor("\t4.")+" Clean qc-bam report Directory log file(s)."
    print ycolor("\t5.")+" Clean Bismark deduplicate/log file(s)."
    print ycolor("\t6.")+" Clean Bismark Meth. Extractor/log file(s)."
    print ycolor("\t7.")+" Clean Cx reports/log file(s)."
    print ycolor("\t8.")+" Clean Methimpute/log file(s)."
    print ycolor("\t9.")+" Clean DMR Directory/log file(s)."
    print ycolor("\t10.")+" Clean bedgraph/log file(s)."
    print ycolor("\t11.")+" Clean methylkit/log file(s)."
    print ycolor("\t12.")+" Clean bigwig/log file(s)."
    print rcolor("B.")+" Back to main Menu\n"
    choice = raw_input(">>  ")
    exec_menu(choice)
    return


# Execute menu
def exec_menu(choice):
    # os.system('clear')
    ch = choice     # .lower()
    if ch == '':
        menu_remove['rem_menu']()
    else:
        try:
            menu_remove[ch]()
        except KeyError:
            print "Invalid selection, please try again.\n"
            menu_remove['rem_menu']()
    return


# removing the directory
def purge(dir, pat):
    for f in glob.glob(dir+pat):
        os.remove(f)


# main directory
result_dir = read_config("GENERAL", "result_pipeline")


def removeRef(str_dir, str_status):
    try:
        directory = result_dir + str_dir
        list_files = len([name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))])
        print("\nYou are deleting directory: " + mcolor(directory))
        print("Total files: " + mcolor(list_files))
        print("Size of directory: " +
              mcolor(subprocess.check_output(['du', '-h', directory]).split()[-2].decode('utf-8')))
        if confirm_run():
            purge(directory, "*")
            replace_config("STATUS", str_status, "0")
            message(0, "Removed all the files!")
    except Exception as e:
        logging.error(traceback.format_exc())
        print(rcolor(e.message))
        message(2, "something is going wrong... please run again. ")
        # set 1 to resuming
        replace_config("STATUS", str_status, "1")


def remTrim():
    removeRef("/trimmomatic-files/", "st_trim")
    removeRef("/trimmomatic-logs/", "st_trim")
    exec_menu('')


def remFastqc():
    removeRef("/qc-fastq-reports/", "st_fastq")
    exec_menu('')


def remBismark():
    removeRef("/bismark-mappers/", "st_bismark")
    exec_menu('')


def remQcbam():
    removeRef("/qc-bam-reports/", "st_fastqbam")
    exec_menu('')


def remBismarkdedup():
    removeRef("/bismark-deduplicate/", "st_bisdedup")
    exec_menu('')


def remBismarkmeth():
    removeRef("/bismark-meth-extractor/", "st_bismeth")
    exec_menu('')


def remCx():
    removeRef("/cx-reports/", "st_cx")
    exec_menu('')


def remMethimpute():
    removeRef("/methimpute-out/", "st_methimpute")
    removeRef("/tes-reports/", "st_methimpute")
    removeRef("/gen-reports/", "st_methimpute")
    removeRef("/fit-reports/", "st_methimpute")
    exec_menu('')


def remDmr():
    removeRef("/dmrcaller-format/", "st_dmrcaller")
    exec_menu('')


def remMethbed():
    removeRef("/bedgraph-fromat/", "st_bedgraph")
    exec_menu('')


def remMethkit():
    removeRef("/methylkit-format/", "st_methykit")
    exec_menu('')


def remBigwig():
    removeRef("/bigwig-fromat/", "st_bigwig")
    exec_menu('')


# Back to main menu
def exit():
     pass


# =======================
#    MENUS DEFINITIONS
# =======================

# Menu definition
menu_remove = {
    'rem_menu': rem_menu,
    '1': remTrim,
    '2': remFastqc,
    '3': remBismark,
    '4': remQcbam,
    '5': remBismarkdedup,
    '6': remBismarkmeth,
    '7': remCx,
    '8': remMethimpute,
    '9': remDmr,
    '10': remMethbed,
    '11': remMethkit,
    '12': remBigwig,
    'b': exit,
}


def __removing__():
    rem_menu()
