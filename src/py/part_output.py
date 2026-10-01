#!/usr/bin/env python
__author__ = "Yadollah Shahryary Dizaji"
__title__ = "setup.py"
__description__ = "Setup file for Pipeline."
__license__ = "GPL"
__version__ = "1.0.0"
__email__ = "shahryary@gmail.com"



from globalParameters import *




# =======================
#     MENUS FUNCTIONS
# =======================
menu_dmr = {}


# Main menu
def dmr_menu():
    print "=="*25
    print "Please choose from the menu:\n"
    print ycolor("\t1.")+" Convert Methimpute output to DMRCaller Format"
    print ycolor("\t2.")+" Convert Methimpute output to Methylkit Format"
    print ycolor("\t3.") + " Convert Methimpute output to bedGraph Format"
    print ycolor("\t4.") + " Convert bedGraph to BigWig Format"
    #print ycolor("\t5.") + " Run jDMR Caller"
    print rcolor("B.")+" Back to main Menu\n"
    choice = raw_input(">>  ")
    exec_menu(choice)
    return


# Execute menu
def exec_menu(choice):
    ch = choice
    if ch == '':
        menu_dmr['dmr_menu']()
    else:
        try:
            menu_dmr[ch]()
        except KeyError:
            print "Invalid selection, please try again.\n"
            menu_dmr['dmr_menu']()
    return


def info_dmr():
    s = gcolor("* If you need to change please back to the configuration part. ")+\
        "" + gcolor("* You can run Methimpute after Cx-report.") + "\n\n"\
    "- Bismark location: " + read_config("Bismark", "bismark_path") + "\n" \

    status = int(read_config("STATUS", "st_cx"))

    if status == 1:
        s += "\nIt seems last time got problem during running..."

    if status == 2:
        if len(check_empty_dir("bismark-meth-extractor", "*.cov.gz")) > 0:
            s += "\nIt seems you have results for Bismark-aligned bam files."
            s += "You can re-run this part, but we recommend move the files to another folder and run again. \n"
            s += "WARNING: The directory is not empty,re-running this part might loosing the existing data!"
        else:
            s += "Couldn't find any coverage file starting to run the bismark meth extractor .. "

    return s


def DMRcaller():
    try:
        preparing_part()
        print "Converting to DMRCaller format ..."
        if confirm_run():
            subprocess.call(['./src/bash/dmr-caller.sh'])
            message(0, "Processing files is finished.")

    except Exception as e:
        logging.error(traceback.format_exc())
        print(rcolor(e.message))
        message(2, "something is going wrong... please run again. ")
        # set 1 to resuming
        replace_config("STATUS", "st_dmrcaller", "1")

    exec_menu('')


def Methylkit():
    try:
        preparing_part()
        print "Converting to Methykit format ..."
        if confirm_run():
            subprocess.call(['./src/bash/methylkit.sh'])
            message(0, "Processing files is finished.")

    except Exception as e:
        logging.error(traceback.format_exc())
        print(rcolor(e.message))
        message(2, "something is going wrong... please run again. ")
        # set 1 to resuming
        replace_config("STATUS", "st_methykit", "1")

    exec_menu('')


def bedGraph():
    try:
        preparing_part()
        print "converting to bedGraph format ..."
        if confirm_run():
            subprocess.call(['./src/bash/gen-rdata.sh'])
            subprocess.call(['./src/bash/meth-bedgraph.sh'])
            message(0, "Processing files is finished.")

    except Exception as e:
        logging.error(traceback.format_exc())
        print(rcolor(e.message))
        message(2, "something is going wrong... please run again. ")
        # set 1 to resuming
        replace_config("STATUS", "st_bedgraph", "1")

    exec_menu('')


def bedToBig():
    try:
        preparing_part()
        print "converting bedGraph format to Bigwig format ..."
        if confirm_run():
            subprocess.call(['./src/bash/bigwig-format.sh'])
            message(0, "Processing files is finished.")

    except Exception as e:
        logging.error(traceback.format_exc())
        print(rcolor(e.message))
        message(2, "something is going wrong... please run again. ")
        # set 1 to resuming
        replace_config("STATUS", "st_bigwig", "1")

    exec_menu('')

def jdmr():
    s = "\njDMR package will be available soon!\n"
    print(qucolor(s))
    exec_menu('')
    '''
    try:
        preparing_part()
        print "converting to DMRCaller format ..."
        if confirm_run():
            subprocess.call(['./src/bash/bigwig-format.sh'])
            message(0, "Processing files is finished.")

    except Exception as e:
        logging.error(traceback.format_exc())
        print(rcolor(e.message))
        message(2, "something is going wrong... please run again. ")
        # set 1 to resuming
        replace_config("STATUS", "st_bigwig", "1")

    exec_menu('')
    '''

# Back to main menu
def exit():
     pass


# =======================
#    MENUS DEFINITIONS
# =======================

# Menu definition
menu_dmr = {
    'dmr_menu': dmr_menu,
    '1': DMRcaller,
    '2': Methylkit,
    '3': bedGraph,
    '4': bedToBig,
    '5': jdmr,
    'b': exit,
}


def __dmr__():
    dmr_menu()
