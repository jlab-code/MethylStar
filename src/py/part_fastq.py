#!/usr/bin/env python
__author__ = "Yadollah Shahryary Dizaji"
__title__ = "setup.py"
__description__ = "Setup file for Pipeline."
__license__ = "GPL"
__version__ = "1.0.0"
__email__ = "shahryary@gmail.com"

from globalParameters import *

def info_fastQC():
    s = gcolor("* If you need to change please back to the configuration part.") + "\n\n" \
    "- Fastq Path: " + mcolor(read_config("GENERAL", "fastq_path")) + " \n" \
    "- Parallel mode is: " + mcolor(true_false_fields_config(read_config("GENERAL", "parallel_mode"), False)) + "\n\n"
    gcolor("You can access to the quality control reports under menu, 'Reports' part.")

    status = int(read_config("STATUS", "st_fastq"))
    if status == 1:
        s += ycolor("\n It seems last time got problem during running...")

    if status == 2:
        if len(check_empty_dir("qc-fastq-reports", "*.html")) > 0:
            s += "It seems you have results for QCFastq part."
            s += "You can re-run this part, but we recommend move the files to another folder and run again. \n"
            s += ycolor("WARNING: The directory is not empty, re-running this part might loosing the existing data!")
    return s


def run_fastQC(status):
    try:
        preparing_part()
        print(info_fastQC())
        if status:
            subprocess.call(['./src/bash/qc-fastq-report.sh'])
        else:
            if confirm_run():
                subprocess.call(['./src/bash/qc-fastq-report.sh'])
                #replace_config("STATUS", "fastq", "2")
                message(0, "Task finished!")
    except Exception as e:
        #logging.error(traceback.format_exc())
        print(rcolor(e.message))
        message(2, "something is going wrong... please run again. ")
        # set 1 to resuming
        replace_config("STATUS", "fastq", "1")
    return