#!/usr/bin/env python
__author__ = "Yadollah Shahryary Dizaji"
__title__ = "setup.py"
__description__ = "Setup file for Pipeline."
__license__ = "GPL"
__version__ = "1.0.0"
__email__ = "shahryary@gmail.com"

from globalParameters import *

def info_bismark_dedup():
    title("Running Bismark Deduplication")
    s = gcolor("Configuration summary:\n ") + \
        "" + "\n"\
    "- Bismark location: " + mcolor(read_config("Bismark", "bismark_path")) + "  \n" \
    "- Parallel mode: " + mcolor(true_false_fields_config(read_config("GENERAL", "parallel_mode"))) + " \n" \
    + gcolor("-Sorting will be start after deduplication.\n")

    status = int(read_config("STATUS", "st_bisdedup"))

    if status == 1:
        s += ycolor("\n--> Please ensure that folder is empty, otherwise it will overwrite the files ...")

    if status == 2:
        if len(check_empty_dir("bismark-deduplicate", "*.bam")) > 0:
            s += ycolor("WARNING: The directory is not empty,re-running this part might loosing the existing data!\n")
            s += "It seems you have results for quality control for Bismark-aligned bam files.\n"
            s += "You can re-run this part, but we recommend move the files to another folder and run again.\n"

    return s


def run():

    try:
        txt = "Bismark deduplication is done."
        subprocess.call(['./src/bash/path-export.sh'])
        subprocess.call(['./src/bash/bismark-deduplicate.sh'])
        #subprocess.call(['./src/bash/bam-sorting.sh'])
        #subprocess.call(['./src/bash/bam-sort-cov.sh', 'deduplicate'])
        replace_config("STATUS", "st_bisdedup", "2")

        if read_config("EMAIL", "active") == "true":
            parmEmail(txt)


    except Exception as e:
        logging.error(traceback.format_exc())
        print(rcolor(e.message))
        txt = e.message
        if read_config("EMAIL", "active") == "true":
            parmEmail(txt)
        message(2, "something is going wrong... please run again. ")
        replace_config("STATUS", "st_bisdedup", "1")


def run_bimark_dedup(status):
    try:
        preparing_part()
        print(info_bismark_dedup())
        # if pair then set to -p
        if read_config("GENERAL", "pairs_mode") == 'true':
            replace_config("Bismark", "deduplicate", "-p")
        else:
            replace_config("Bismark", "deduplicate", "-s")
        
        if (read_config("GENERAL", "genome_type") == "scBS-Seq" or read_config("Bismark", "single_cell") == "true"):
            replace_config("Bismark", "deduplicate", "-s")
        if status:
            run()

        else:
            if confirm_run():
                print qucolor("\nRunning Bismark deduplication ...")
                run()
                message(0, "Processing files is finished, You can check the logs in Menu, part 'Bismark-log' ")

    except Exception as e:
        logging.error(traceback.format_exc())
        print(rcolor(e.message))
        txt = e.message
        if read_config("EMAIL", "active") == "true":
            parmEmail(txt)
        message(2, "something is going wrong... please run again. ")
        replace_config("STATUS", "st_bisdedup", "1")

    return
