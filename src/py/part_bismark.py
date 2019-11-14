#!/usr/bin/env python2
__author__ = "Yadollah Shahryary Dizaji"
__title__ = "setup.py"
__description__ = "Setup file for Pipeline."
__license__ = "GPL"
__version__ = "1.0.0"
__email__ = "shahryary@gmail.com"

from globalParameters import *

def info_bismark_mapper():
    title("Running Bismark Mapper Part")
    s = gcolor("Configuration summary: \n")+\
        "" + "\n"\
    "- Bismark location: " + mcolor(read_config("Bismark", "bismark_path")) + "\n" \
    "   -- Nucleotide: " + mcolor(true_false_fields_config(read_config("Bismark", "nucleotide"))) + "\n" \
    "   -- Buffer size: " +  mcolor(read_config("Bismark", "buf_size")) + "\n" \
    "   -- Number of Parallel: " + mcolor(read_config("Bismark", "bis_parallel")) + " \n" \
    "- Reference Genome is: " + read_config("GENERAL", "genome_ref") + "/" + mcolor(read_config("GENERAL", "genome_name")) + "\n" \
    "- Parallel mode: " + mcolor(true_false_fields_config(read_config("GENERAL", "parallel_mode"))) + "\n" \
    "- Bismark run in pair mode: " + mcolor(true_false_fields_config(read_config("Bismark", "run_pair_bismark"))) +"\n" \
        + gcolor("Note: Fastq bam report will be start after bismark mapper.")

    status = int(read_config("STATUS", "st_bismark"))
    if status == 1:
        s += ycolor("\n --> Please ensure that folder is empty, otherwise it will overwrite the files ...")
    elif status == 2:
        if len(check_empty_dir("bismark-mappers", "*.bam")) > 0:
            s += ycolor("WARNING: The directory is not empty, re-running this part might loosing the existing data!\n")
            s += "It seems you have results for Trimmomatic part.\n"
            s += "You can re-run this part, but we recommend move the files to another folder and run again.\n"

    return s


def run():
    try:

        '''
        gen_type = read_config("GENERAL", "genome_type")
        if (gen_type in ["Human", "Maize"]):
            replace_config("GENERAL", "parallel_mode", "false")
        '''
        pairs_mode = read_config("GENERAL", "pairs_mode")

        subprocess.call(['./src/bash/path-export.sh'])
        subprocess.call(['./src/bash/pre-bismark.sh'])

        if pairs_mode == 'true' and read_config("GENERAL", "parallel_mode") == "true":
            subprocess.call(['./src/bash/bismark-mapper-pair-parallel.sh'])
        elif pairs_mode == 'true' and read_config("GENERAL", "parallel_mode") == "false":
            subprocess.call(['./src/bash/bismark-mapper-pair.sh'])
        else:
            subprocess.call(['./src/bash/bismark-mapper.sh'])

        #replace_config("GENERAL", "parallel_mode", "true")
        # start to run fastqc bam report
        subprocess.call(['./src/bash/qc-bam-report.sh'])
        print("Sorting bam files & generating coverage report...  ")
        #subprocess.call(['./src/bash/bam-sort-cov.sh', "mapper"])
        # generating sort then coverage after bismark
        #subprocess.call(['./src/bash/gen-rdata.sh'])
        #subprocess.call(['./src/bash/bam-sort-cov.sh'])
        #subprocess.call(['./src/bash/coverage-reports.sh'])

    except Exception as e:
        logging.error(traceback.format_exc())
        print(rcolor(e.message))
        txt = e.message
        if read_config("EMAIL", "active") == "true":
            parmEmail(txt)
        message(2, "something is going wrong... please run again. ")
        # set 1 to resuming
        replace_config("STATUS", "bismark", "1")


def run_bimark_mapper(status):

    txt = "Bismark Mapper Part finished."
    try:
        preparing_part()
        print(info_bismark_mapper())
        if status:
            run()
        else:
            if confirm_run():
                print qucolor("\nRunning Bismark Mapper ...")
                run()
                if read_config("EMAIL", "active") == "true":
                    parmEmail(txt)
                message(0, "Processing files is finished, You can check the logs in Menu, part 'Bismark-log' ")

    except Exception as e:
        logging.error(traceback.format_exc())
        print(rcolor(e.message))

    return
