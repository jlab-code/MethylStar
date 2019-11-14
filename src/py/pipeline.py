#!/usr/bin/env python2
__author__ = "Yadollah Shahryary Dizaji"
__title__ = "pipeline.py"
__description__ = "Running file for Pipeline."
__license__ = "GPL"
__version__ = "1.0.0"
__email__ = "shahryary@gmail.com"


import os, glob
from configuration import rcolor, qucolor, ycolor
from globalParameters import *

# =======================
#     MENUS FUNCTIONS
# =======================
menu_pip = {}


# Main menu
def pip_menu():
    print("\n"+"=="*25)
    print("Please choose from the menu:\n")
    print(mcolor("A. Quick Run: \n"))
    print(ycolor("\t0.")+" Trimmomatic, QC-Fastq-report, Bismark(alignment, remove duplicates), Extract methylation calls, Methimpute.\n")
    print(mcolor("B. Individual Run: \n"))
    print(ycolor("\t1.")+" Run Trimommatic")
    print(ycolor("\t2.")+" Run QC-Fastq-report")
    print(ycolor("\t3.")+" Run Bismark Mapper")
    print(ycolor("\t4.")+" Run Genome coverage & Sequencing depth (After Mapping)")
    print(ycolor("\t5.")+" Run Bismark deduplication")
    print(ycolor("\t6.")+" Run Genome coverage & Sequencing depth (After deduplicate)")
    print(ycolor("\t7.")+" Run Bismark Methylation Extractor")
    print(ycolor("\t8.")+" Generate Cytosine Calls (cx-reports)")
    print(ycolor("\t9.")+" Run Methimpute")
    print(rcolor("B.")+" Back to main Menu\n")
    choice = raw_input(">>  ")
    exec_menu(choice)

    return

# which part user running
def dectect_run(ch):
    if ch == '0':
        replace_config("STATUS", "quickrun", "1")
    else:
        replace_config("STATUS", "quickrun", "0")


# Execute menu
def exec_menu(choice):
    #os.system('clear')
    ch = choice #.lower()
    dectect_run(ch)
    if ch == '':
        menu_pip['pip_menu']()
    else:
        try:
            menu_pip[ch]()
        except KeyError:
            print("Invalid selection, please try again.\n")
            menu_pip['pip_menu']()
    return


def quickRun():
    from part_quick import run_quick
    run_quick()
    exec_menu('')


def itemTrim():
    from part_trimmomatic import run_trimmomatic
    run_trimmomatic(False)
    exec_menu('')


def itemFastqc():
    from part_fastq import run_fastQC
    run_fastQC(False)
    exec_menu('')


def itemBismark():
    # running preparing files
    from part_bismark import run_bimark_mapper
    run_bimark_mapper(False)
    exec_menu('')


def itemCoverage():
    # running preparing files
    from part_coreports import run_coreports
    run_coreports(False, "mapper")
    exec_menu('')


def itemBismarkdedup():
    from part_bismark_dedup import run_bimark_dedup
    run_bimark_dedup(False)
    exec_menu('')

def itemCoverageDe():
    # running preparing files
    from part_coreports import run_coreports
    run_coreports(False, "deduplicate")
    exec_menu('')

def itemBismarkmeth():
    from part_bismark_meth import run_bimark_meth
    run_bimark_meth()
    exec_menu('')


def itemCx():
    from part_cx import run_cx
    run_cx()
    exec_menu('')


def methimpute():
    from part_methimpute import run_methimpute
    run_methimpute()
    exec_menu('')


# Back to main menu
def exit():
     pass


# =======================
#    MENUS DEFINITIONS
# =======================

# Menu definition
menu_pip = {
    'pip_menu': pip_menu,
    '0': quickRun,
    '1': itemTrim,
    '2': itemFastqc,
    '3': itemBismark,
    '4': itemCoverage,
    '5': itemBismarkdedup,
    '6': itemCoverageDe,
    '7': itemBismarkmeth,
    '8': itemCx,
    '9': methimpute,

    'b': exit,
}

def __pipeline__():
    firstrun = read_config("GENERAL", "firstRun")
    if firstrun == 'true':
        message(2, "\n You're running the Pipeline for the first time, Please configure it in 'Configuration Part' ")
        #exec_menu('b')
    else:
        pip_menu()
