#!/usr/bin/env python
__author__ = "Yadollah Shahryary Dizaji"
__title__ = "setup.py"
__description__ = "Setup file for Pipeline."
__license__ = "GPL"
__version__ = "1.0.0"
__email__ = "shahryary@gmail.com"

from globalParameters import *


def info_bismark_dedup():
    s = gcolor("* If you need to change please back to the configuration part. ") + \
        "" + gcolor("* Sorting will be start after deduplication.") + "\n\n"\
    "- Bismark location: " + mcolor(read_config("Bismark", "bismark_path")) + "  \n" \
    "- Parallel mode: " + mcolor(true_false_fields_config(read_config("GENERAL", "parallel_mode"), False)) + " \n " \
    "     -- Number of Parallel Jobs: " + mcolor(read_config("GENERAL", "npar")) + "\n\n"

    status = int(read_config("STATUS", "st_bisdedup"))

    if status == 1:
        s += ycolor("It seems last time got problem during running...")

    if status == 2:
        if len(check_empty_dir("bismark-deduplicate", "*.bam")) > 0:
            s += ycolor("WARNING: The directory is not empty,re-running this part might loosing the existing data!\n")
            s += "It seems you have results for quality control for Bismark-aligned bam files.\n"
            s += "You can re-run this part, but we recommend move the files to another folder and run again.\n"


    return s


def run_bimark_dedup(status):

    try:
        preparing_part()
        print(info_bismark_dedup())
        # if pair then set to -p
        if read_config("GENERAL", "pairs_mode") == 'true':
            replace_config("Bismark", "deduplicate", "-p")
        else:
            replace_config("Bismark", "deduplicate", "-s")

        if status:
            subprocess.call(['./src/bash/path-export.sh'])
            subprocess.call(['./src/bash/bismark-deduplicate.sh'])
            subprocess.call(['./src/bash/bam-sorting.sh'])
            #replace_config("STATUS", "st_bisdedup", "2")
        else:
            if confirm_run():
                subprocess.call(['./src/bash/path-export.sh'])
                subprocess.call(['./src/bash/bismark-deduplicate.sh'])
                # sorting is not accepting by meth-extractor
                #subprocess.call(['./src/bash/bam-sorting.sh'])
                message(0, "Processing files is finished, You can check the logs in Menu, part 'Bismark-log' ")
    except Exception as e:
        logging.error(traceback.format_exc())
        print(rcolor(e.message))
        message(2, "something is going wrong... please run again. ")
        # set 1 to resuming
        replace_config("STATUS", "st_bisdedup", "1")
    return
