#!/usr/bin/env python
__author__ = "Yadollah Shahryary Dizaji"
__title__ = "setup.py"
__description__ = "Setup file for Pipeline."
__license__ = "GPL"
__version__ = "1.0.0"
__email__ = "shahryary@gmail.com"

from globalParameters import *

def info_methimpute():

    title("Running Methimpute Part")
    s = gcolor("Configuration Summary:\n ")+\
        "" + "\n"\
    "- Intermediate: " + mcolor(true_false_fields_config(read_config("Methimpute", "intermediate"))) + "\n" \
    "- Fit reports: " + mcolor(true_false_fields_config(read_config("Methimpute", "fit_output"))) + "\n"\
    "- Enrichment reports: " +mcolor(true_false_fields_config(read_config("Methimpute", "enrichment_plot")))+ "\n"\
    "- Full reports: " +mcolor(true_false_fields_config(read_config("Methimpute", "full_report")))+ "\n"

    status = int(read_config("STATUS", "st_methimpute"))

    if status == 1:
        s += "\n--> Please ensure that folder is empty, otherwise it will overwrite the files ..."

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
        print(info_methimpute())
        txt = "Methimpute part finished."
        if confirm_run():
            print(info_methimpute())
            print "==" * 40
            print qucolor("\nRunning Methimpute Part...")
            replace_config("GENERAL", "parallel_mode", "false")
            subprocess.call(['./src/bash/gen-rdata.sh'])
            subprocess.call(['./src/bash/methimpute.sh'])
            if read_config("EMAIL", "active") == "true":
                parmEmail(txt)

            message(0, "Processing files is finished, You can check the logs in Menu, part 'Bismark-log' ")

    except Exception as e:
        logging.error(traceback.format_exc())
        print(rcolor(e.message))
        txt = e.message
        # email part
        if read_config("EMAIL", "active") == "true":
            parmEmail(txt)
        message(2, "something is going wrong... please run again. ")
        # set 1 to resuming
        replace_config("STATUS", "st_methimpute", "1")

    return
