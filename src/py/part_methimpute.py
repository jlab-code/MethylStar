#!/usr/bin/env python
__author__ = "Yadollah Shahryary Dizaji"
__title__ = "setup.py"
__description__ = "Setup file for Pipeline."
__license__ = "GPL"
__version__ = "1.0.0"
__email__ = "shahryary@gmail.com"

from globalParameters import *

def info_methimpute():
    # @todo print all parameters from config to here

    s = gcolor("* If you need to change please back to the configuration part. ")+"\n"
    "- Intermediate: " + mcolor(true_false_fields_config(read_config("Methimpute", "intermediate"), False)) + "\n" \
    "- Fit reports: " + mcolor(true_false_fields_config(read_config("Methimpute", "fit_output"), False)) + "\n"\
    "- Enrichment reports: " +mcolor(true_false_fields_config(read_config("Methimpute", "enrichment_plot"), False))+ "\n"\
    "- TEs reports: " +mcolor(true_false_fields_config(read_config("Methimpute", "TES_report"), False))+ "\n"\
    "- genes reports: " +mcolor(true_false_fields_config(read_config("Methimpute", "genes_report"), False))+ "\n\n"\

    status = int(read_config("STATUS", "st_methimpute"))

    if status == 1:
        s += "\nIt seems last time got problem during running..."

    if status == 2:
        if len(check_empty_dir("methimpute-out", "*.txt")) > 0:
            s += ycolor("WARNING: The directory is not empty,re-running this part might loosing the existing data!\n")
            s += "It seems you have results for Methimpute part.\n"
            s += "You can re-run this part, but we recommend move the files to another folder and run again.\n"
        else:
            s += "Couldn't find any CX file starting to run the Methimpute .. "

    return s

def run_methimpute():
    try:
        preparing_part()
        '''
        pipeline.conf
        0: not yet run 
        1: bug during run 
        2: successfully run  
        '''
        print(info_methimpute())
        if int(read_config("STATUS", "st_bissort")) == 2:
            print "==" * 40
            print qucolor("Running Methimpute Part...")
            replace_config("GENERAL", "parallel_mode", "false")
            subprocess.call(['./src/bash/gen-rdata.sh'])
            subprocess.call(['./src/bash/methimpute.sh'])

            message(0, "Processing files are finished.")
    except Exception as e:
        logging.error(traceback.format_exc())
        print(rcolor(e.message))
        message(2, "something is going wrong... please run again. ")
        # set 1 to resuming
        replace_config("STATUS", "st_methimpute", "1")
    return