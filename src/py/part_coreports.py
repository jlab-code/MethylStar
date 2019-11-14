#!/usr/bin/env python
__author__ = "Yadollah Shahryary Dizaji"
__title__ = "setup.py"
__description__ = "Setup file for Pipeline."
__license__ = "GPL"
__version__ = "1.0.0"
__email__ = "shahryary@gmail.com"

from globalParameters import *

def info_coreports():
    title("Genome coverage & Sequencing depth")
    s = gcolor("Configuration Summary:\n") + "\n" \
    "- Bedtools Path: " + mcolor(read_config("Bismark", "bedtools_path")) + " \n" \
    "- Samtools Path: " + mcolor(read_config("Bismark", "samtools_path")) + " \n" \
    "- Parallel mode is: " + mcolor(true_false_fields_config(read_config("GENERAL", "parallel_mode"))) + "\n\n"

    status = int(read_config("STATUS", "st_coreport"))
    if status == 1:
        s += ycolor("\n It seems last time got problem during running...")

    if status == 2:
        if len(check_empty_dir("cov-seq-reports", "*.log")) > 0:
            s += "It seems you have results for coverage part."
            s += "You can re-run this part, but we recommend move the files to another folder and run again. \n"
            s += ycolor("WARNING: The directory is not empty, re-running this part might loosing the existing data!")
    return s


def run(part):
    try:
        subprocess.call(['./src/bash/bam-sort-cov.sh', part])
        subprocess.call(['./src/bash/coverage-reports.sh', part])
        txt = " calculate genome coverage and sequencing depth finished."
        # email part

        if read_config("EMAIL", "active") == "true":
            parmEmail(txt)

    except Exception as e:
        logging.error(traceback.format_exc())
        print(rcolor(e.message))
        txt = "Error: " + e.message
        # email part
        if read_config("EMAIL", "active") == "true":
            parmEmail(txt)
        message(2, "something is going wrong... please run again. ")
        # set 1 to resuming
        replace_config("STATUS", "st_coreport", "1")


def run_coreports(status, part):
    try:
        preparing_part()
        print(info_coreports())
        subprocess.call(['./src/bash/gen-rdata.sh'])

        if status:
            run(part)
        else:
            if confirm_run():
                print qucolor("\nRunning genome coverage and sequencing depth ...")
                run(part)
                message(0, "Sorting and creating reports finished!")

    except Exception as e:
        logging.error(traceback.format_exc())
        print(rcolor(e.message))

    return
