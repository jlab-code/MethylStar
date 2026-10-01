#!/usr/bin/env python
__author__ = "Yadollah Shahryary Dizaji"
__title__ = "setup.py"
__description__ = "Setup file for Pipeline."
__license__ = "GPL"
__version__ = "1.0.0"
__email__ = "shahryary@gmail.com"

from globalParameters import *
from part_trimmomatic import run_trimmomatic
from part_fastq import run_fastQC
from part_bismark import run_bimark_mapper
from part_bismark_dedup import run_bimark_dedup
from part_methimpute import info_methimpute
from part_coreports import run_coreports


def run_quick():

    try:
        title("Running in Quick mode! ")
        preparing_part()
        is_snmc = ( read_config("Bismark", "single_cell") == "true" )
        if is_snmc:
            print rcolor("MethylStar does not support Quick Run for PBAT-based data. Please use Individual Run workflow.")
            replace_config("STATUS", "quickrun", "1")
            return
        if is_snmc and read_config("GENERAL", "pairs_mode") != "true":
            print rcolor("MethylStar does not support single-end mapping for the IDT snmC-Seq workflow right now.")
            replace_config("STATUS", "quickrun", "1")
            return
        '''
        pipeline.conf
        0: not yet run 
        1: bug during run 
        2: successfully run  
        '''
        txt = "Processing files are finished."
        if confirm_run():

            if int(read_config("STATUS", "st_trim")) != 2:
                print "==" * 40
                print qucolor("\nRunning Trimming Part...")
                run_trimmomatic(True)

            if int(read_config("STATUS", "st_fastq")) != 2:
                print "==" * 40
                print qucolor("\nRunning FastQC Part...")
                run_fastQC(True)

            if int(read_config("STATUS", "st_bismark")) != 2:
                print "==" * 40
                print qucolor("\nRunning Bismark-Mapper Part...")
                run_bimark_mapper(True)

            if int(read_config("STATUS", "st_bissort")) != 2:
                print "==" * 40
                print qucolor("\nRunning genome coverage and sequencing depth ...")
                run_coreports(True, "mapper")

            if int(read_config("STATUS", "st_bisdedup")) != 2:
                print "==" * 40
                print qucolor("\nRunning Bismark-deduplicate Part...")
                run_bimark_dedup(True)

            if int(read_config("STATUS", "st_dedsort")) != 2:
                print "==" * 40
                print qucolor("\nRunning genome coverage and sequencing depth...")
                run_coreports(True, "deduplicate")

            # if ==2 that's mean sorted
            if int(read_config("STATUS", "st_dedsort")) == 2:
                print "==" * 40
                print qucolor("\nRunning Methimpute Part...")
                subprocess.call(['./src/bash/gen-rdata.sh'])
                print(info_methimpute())
                subprocess.call(['./src/bash/methimpute-bam.sh'])
                #replace_config("STATUS", "st_trim", "0")
                #replace_config("STATUS", "st_fastq", "0")
                #replace_config("STATUS", "st_bismark", "0")
                #replace_config("STATUS", "st_bisdedup", "0")

            # email part
            if read_config("EMAIL", "active") == "true":
                parmEmail(txt)
            message(0, "Processing files are finished, results are in :"
                    + read_config("Others", "tmp_meth_out"))

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
