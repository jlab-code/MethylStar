#!/usr/bin/env python
__author__ = "Yadollah Shahryary Dizaji"
__title__ = "setup.py"
__description__ = "Setup file for Pipeline."
__license__ = "GPL"
__version__ = "1.0.0"
__email__ = "shahryary@gmail.com"


from globalParameters import *


def info_bismark_meth():
    title("Running Bismark Methylation Extractor")
    s = gcolor("Configuration Summary: \n ")+\
        ""+ "\n"\
    "- Bismark location: " + read_config("Bismark", "bismark_path") + "\n" \
    + gcolor("Note: Cytosine Calls (cx-reports) will start automatically after Methylation Extractor")

    status = int(read_config("STATUS", "st_bismeth"))

    if status == 1:
        s += "\n--> Please ensure that folder is empty, otherwise it will overwrite the files ..."

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
        txt = "Bismark meth extractor part finished."
        '''
        gen_type = read_config("GENERAL", "genome_type")
        if (gen_type in ["Human", "Maize"]):
            replace_config("GENERAL", "parallel_mode", "false")
        '''
        if read_config("GENERAL", "pairs_mode") == 'true':
            replace_config("Bismark", "methextractor", "-p")
        else:
            replace_config("Bismark", "methextractor", "-s")


        if (read_config("GENERAL", "genome_type") == "scBS-Seq" or read_config("Bismark", "single_cell") == "true"):
            replace_config("Bismark", "methextractor", "-s")

        if confirm_run():
            print qucolor("\nRunning Bismark Meth Extractor ...")
            subprocess.call(['./src/bash/path-export.sh'])
            subprocess.call(['./src/bash/bismark-meth-extractor.sh'])
            if read_config("EMAIL", "active") == "true":
                parmEmail(txt)
            # running methimpute
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
        replace_config("STATUS", "st_bismeth", "1")



    return
