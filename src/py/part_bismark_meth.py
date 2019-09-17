#!/usr/bin/env python
__author__ = "Yadollah Shahryary Dizaji"
__title__ = "setup.py"
__description__ = "Setup file for Pipeline."
__license__ = "GPL"
__version__ = "1.0.0"
__email__ = "shahryary@gmail.com"


from globalParameters import *


def info_bismark_meth():
    s = gcolor("* If you need to change please back to the configuration part. ")+\
        "" + gcolor("* Methimpute will be start after Cx-report.") + "\n\n"\
    "- Bismark location: " + read_config("Bismark", "bismark_path") + "\n" \

    status = int(read_config("STATUS", "st_bismeth"))

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


def run_bimark_meth():

    try:
        preparing_part()
        print(info_bismark_meth())

        gen_type = read_config("GENERAL", "genome_type")
        if (gen_type in ["Human", "Maize"]):
            replace_config("GENERAL", "parallel_mode", "false")

        if read_config("GENERAL", "pairs_mode") == 'true':
            replace_config("Bismark", "methextractor", "-p")
        else:
            replace_config("Bismark", "methextractor", "-s")

        if confirm_run():
            subprocess.call(['./src/bash/path-export.sh'])
            subprocess.call(['./src/bash/bismark-meth-extractor.sh'])
            # running methimpute
            message(0, "Processing files is finished, You can check the logs in Menu, part 'Bismark-log' ")

    except Exception as e:
        logging.error(traceback.format_exc())
        print(rcolor(e.message))
        message(2, "something is going wrong... please run again. ")
        # set 1 to resuming
        replace_config("STATUS", "st_bismeth", "1")
    return
