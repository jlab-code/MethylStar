#!/usr/bin/env python
__author__ = "Yadollah Shahryary Dizaji"
__title__ = "setup.py"
__description__ = "Setup file for Pipeline."
__license__ = "GPL"
__version__ = "1.0.0"
__email__ = "shahryary@gmail.com"




import os, glob
import traceback
import logging
from configuration import rcolor,qucolor,ycolor,gcolor,mcolor,query_yes_no,confirm,read_config, \
    find_file_pattern,bcolors,replace_config, inputNumber
import subprocess



# =======================
#     MENUS FUNCTIONS
# =======================
menu_dmr = {}


# Main menu
def dmr_menu():
    print "=="*25
    print "\nWelcome,\n"
    print "Please choose the menu you want to start:\n"
    print ycolor("1.")+" Run DMRcaller"
    print ycolor("2.")+" Run Methylkit..."

    print rcolor("B.")+" Back to main Menu\n"
    choice = raw_input(">>  ")
    exec_menu(choice)
    return


# Execute menu
def exec_menu(choice):
    #os.system('clear')
    ch = choice #.lower()
    if ch == '':
        menu_dmr['dmr_menu']()
    else:
        try:
            menu_dmr[ch]()
        except KeyError:
            print "Invalid selection, please try again.\n"
            menu_dmr['dmr_menu']()
    return


def message(msg_code, msg):

    if msg_code == 0:
        print "\n"+bcolors.OKBLUE + msg + bcolors.ENDC+"\n"
        raw_input("Please, press ENTER to continue ...")
        exec_menu('')
    elif msg_code == 1:
        print bcolors.FAIL + msg + bcolors.ENDC+"\n"
    elif msg_code == 2:
        print bcolors.WARNING + msg + bcolors.ENDC+"\n"
        raw_input("Please, press ENTER to continue ...")
        exec_menu('')
    elif msg_code == 3:
        print bcolors.OKGREEN + msg + bcolors.ENDC+"\n"
    elif msg_code == 4:
        print bcolors.NOTE + msg + bcolors.ENDC+"\n"
    return


def check_empty_dir(path, pattern):

    try:

        files = list(find_file_pattern(read_config("GENERAL", "result_pipeline")+"/"+path, pattern))
        if files:
            for item in find_file_pattern(read_config("GENERAL", "result_pipeline")+"/"+path, pattern):
                files.append(item)
        else:
            files = []

        return files

    except Exception as e:
        logging.error(traceback.format_exc())
        message(2, "something is going wrong... please run again. ")


def check_before_run(part, status):

    if part == "prep":
        '''
        0=run preparing shell
        1=already did
        '''
        status = int(read_config("STATUS", "prep"))
        if status:
            print "Preparing folders and directories ..."
            # list all *.gz files inside the directory and sub folders

            subprocess.call(['./src/bash/preparing.sh'])
            replace_config("STATUS", "prep", "1")

        else:
            pass

    if part == "trim":
        '''
        0= first time 
        1= on pause- resuming 
        2= finished 
        '''

        # check if directory is empty then it's ok otherwise it's not first time running
        print "Here, you can find the summary of configuration for Trimmomatic part"
        message(4,"If you need to change please back to the configuration part.")

        print "- Trimmomatic location: " + mcolor(read_config("Trimmomatic", "trim_path"))
        print "   -- JAVA path: " + mcolor(read_config("Trimmomatic", "java_path"))
        print "   -- Running Mode 'Single End' or 'Pair End' : " + mcolor(read_config("Trimmomatic", "end_mode"))
        print "   -- ILLUMINACLIP: " + mcolor(read_config("Trimmomatic", "name_adap")) \
                  + ":" + mcolor(read_config("Trimmomatic", "ill_clip"))
        print "   -- LEADING: " + mcolor(read_config("Trimmomatic", "LEADING"))
        print "   -- TRAILING: " + mcolor(read_config("Trimmomatic", "TRAILING"))
        print "   -- SLIDINGWINDOW: " + mcolor(read_config("Trimmomatic", "SLIDINGWINDOW"))
        print "   -- MINLEN: " + mcolor(read_config("Trimmomatic", "MINLEN"))
        print "   -- Number of Threads: " + mcolor(read_config("Trimmomatic", "n_th"))
        print "- Parallel mode is: " + mcolor(read_config("GENERAL", "parallel_mode"))

        if status == 1:
            print ycolor("\nIt seems last time got problem during running...")
        elif status == 2:
            if len(check_empty_dir("trimmomatic-files", "*.gz")) > 0:
                print "\nIt seems you have results for Trimmomatic part."
                print "You can re-run this part, but we recommend move the files to another folder and run again. \n"
                print ycolor("WARNING: The directory is not empty,"
                             "re-running this part might loosing the existing data!")
            pass
        return status

    if part == "qcfastq":
        print "Here, you can find the summary of configuration to running QCFastq reports."
        message(4, "If you need to change please back to the configuration part.")
        print "- Fastq Path: " + mcolor(read_config("GENERAL", "fastq_path"))
        print "- Parallel mode is: " + mcolor(read_config("GENERAL", "parallel_mode"))+"\n"
        message(4, "You can access to the quality control reports under menu, 'Reports' part. ")

        if status == 1:
            print ycolor("\nIt seems last time got problem during running...")

        if status == 2:
            if len(check_empty_dir("qc-fastq-reports", "*.html")) > 0:
                print "\nIt seems you have results for QCFastq part."
                print "You can re-run this part, but we recommend move the files to another folder and run again. \n"
                print ycolor("WARNING: The directory is not empty,"
                             "re-running this part might loosing the existing data!")
            pass
        return status

    if part == "bismark":
        '''
        0= first time 
        1= on pause- resuming 
        2= finished 
        '''
        # check if directory is empty then it's ok otherwise it's not first time running
        print "\nHere, you can find the summary of configuration for Bismark mapper"
        message(4, "For any change, please back to the configuration part.")

        print "- bismark location: " + mcolor(read_config("Bismark", "bismark_path"))
        print "   -- Nucleotide Enabled?: " + mcolor(read_config("Bismark", "nucleotide"))
        print "   -- Buffer size: " + mcolor(read_config("Bismark", "buf_size"))
        print "   -- Number of Parallel: " + mcolor(read_config("Bismark", "bis_parallel"))
        print "- Reference Genome is: " + mcolor(read_config("GENERAL", "genome_ref"))\
              + "/" + mcolor(read_config("GENERAL", "genome_name"))

        print "- Parallel mode is: " + mcolor(read_config("GENERAL", "parallel_mode"))

        if status == 1:
            print ycolor("\nIt seems last time got problem during running...")
        elif status == 2:
            if len(check_empty_dir("bismark-mappers", "*.bam")) > 0:
                print "\nIt seems you have results for Trimmomatic part."
                print "You can re-run this part, but we recommend move the files to another folder and run again. \n"
                print ycolor("WARNING: The directory is not empty,"
                             "re-running this part might loosing the existing data!")
            pass
        return status

    if part == "qcfastqbam":
        print "Here, you can find the summary of configuration to running Bismark-aligned bam files."
        message(4, "If you need to change please back to the configuration part.")
        print "- Fastq Path: " + mcolor(read_config("GENERAL", "fastq_path"))
        print "- Parallel mode is: " + mcolor(read_config("GENERAL", "parallel_mode"))+"\n"
        message(4, "You can access to the quality control reports under menu, 'Reports' part. ")

        if status == 1:
            print ycolor("\nIt seems last time got problem during running...")

        if status == 2:
            if len(check_empty_dir("qc-bam-reports", "*.html")) > 0:
                print "\nIt seems you have results for quality control for Bismark-aligned bam files."
                print "You can re-run this part, but we recommend move the files to another folder and run again. \n"
                print ycolor("WARNING: The directory is not empty,"
                             "re-running this part might loosing the existing data!")
            pass
        return status



def confirm_run():
        answer = query_yes_no("\nDo you want continue to run?", None)
        if answer:
                return True
        else:
            message(2, "Canceled!")



# Menu 2
def DMRcaller():
    # running preparing files
    try:
        check_before_run("prep", 0)
        status = int(read_config("STATUS", "bismark"))
        pairs_mode = read_config("GENERAL", "pairs_mode")

        check_before_run("bismark", status)
        # we don't need parallel in bismark mapper
        replace_config("GENERAL", "parallel_mode", "false")

        if confirm_run():
            if pairs_mode == 'true':
                # ask for paired_1 unpaire_1
                print message(4, "The default parameter for running Bismark is "
                                 "paired_1/unpaired_1 and paired_2/unpaired_2.")
                print "You can select running case for Bismark.\n"

                print ycolor("1") + "- Default running (ex: paired_1/unpaired_1 and paired_2/unpaired_2."
                print ycolor("2") + "- Just pairs case. (ex: paired_1/paired_2.)"

                answer = inputNumber("\nPlease enter the number to select:")
                while not int(answer) in range(1, 3):
                    answer = inputNumber("Please enter the valid number:")
                if int(answer) == 1:
                    replace_config("Bismark", "run_pair_bismark", "false")
                else:
                    replace_config("Bismark", "run_pair_bismark", "true")
                subprocess.call(['./src/bash/bismark-mapper-pair.sh'])
                replace_config("STATUS", "bismark", "2")
            else:
                subprocess.call(['./src/bash/bismark-mapper.sh'])
                replace_config("STATUS", "bismark", "2")

            message(0, "Processing files is finished, You can check the logs in Menu, part 'Bismark-log' ")
    except Exception as e:
        logging.error(traceback.format_exc())
        message(2, "something is going wrong... please run again. ")
        # set 1 to resuming
        replace_config("STATUS", "bismark", "1")
    return




def purge(dir,pat):
    for f in glob.glob(dir+pat):
        os.remove(f)




def Methylkit():
    # running preparing files
    try:
        check_before_run("prep", 0)
        #status = int(read_config("STATUS", "methimpute"))
        #check_before_run("methimpute", status)

        if confirm_run():
            option = ["DefaultDMB","DefaultDMR","Fishers.testDMB","Fishers.testDMR"]
            for item in option:
                print (ycolor(str(option.index(item))) + " : " + item)

            answer = inputNumber("\nPlease select statistic for Methylkit:")
            while not int(answer) in range(0, len(option)):
                answer = inputNumber("Please enter the valid number:")
            statics = option[int(answer)]
            replace_config("DMR", "statistic", statics)

            subprocess.call(['./src/bash/methylkit.sh'])



            message(0, "Task finished!")
    except Exception as e:
        logging.error(traceback.format_exc())
        message(2, "something is going wrong... please run again. ")
        # set 1 to resuming
        replace_config("STATUS", "bismeth", "1")
    return




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

    'b': exit,
}

def __dmr__():
    dmr_menu()