#!/usr/bin/env python
__author__ = "Yadollah Shahryary Dizaji"
__title__ = "setup.py"
__description__ = "Setup file for Pipeline."
__license__ = "GPL"
__version__ = "1.0.0"
__email__ = "shahryary@gmail.com"

from globalParameters import *

def info_trimmomatic():
    s = gcolor("Configuration Summary: ")+"\n\n"\
    "Configured Java location: " + mcolor(read_config("Trimmomatic", "java_path")) + "\n" \
    "Trimmomatic path: " + mcolor(read_config("Trimmomatic", "trim_path")) + "\n" \
    "Trimmomatic Adapter: " + mcolor(read_config("Trimmomatic", "name_adap")) + "\n" \
    "Trimmomatic Running mode: " + mcolor(read_config("Trimmomatic", "end_mode")) + "\n" \
    "Trimmomatic ILLUMINACLIP: " + mcolor(read_config("Trimmomatic", "ill_clip")) + "\n" \
    "Trimmomatic LEADING: " + mcolor(read_config("Trimmomatic", "LEADING")) + "\n" \
    "Trimmomatic TRAILING: " + mcolor(read_config("Trimmomatic", "TRAILING")) + "\n" \
    "Trimmomatic SLIDINGWINDOW: " + mcolor(read_config("Trimmomatic", "SLIDINGWINDOW")) + "\n" \
    "Trimmomatic MINLEN: " + mcolor(read_config("Trimmomatic", "MINLEN")) + "\n" \
    "Trimmomatic Threading: " + mcolor(read_config("Trimmomatic", "n_th")) + "\n" \
    "Parallel mode is: " + mcolor(true_false_fields_config(read_config("GENERAL", "parallel_mode"))) + "\n\n" \

    status = int(read_config("STATUS", "st_trim"))
    pairs_mode = read_config("GENERAL", "pairs_mode")

    if status == 1:
        s += ycolor("--> Please ensure that folder is empty, otherwise it will overwrite the files ...")
    elif status == 2:
        if len(check_empty_dir("trimmomatic-files", "*.gz")) > 0:
            s += "\nIt seems you have results for Trimmomatic part."
            s += "You can re-run this part, but we recommend move the files to another folder and run again. \n"
            s += ycolor("WARNING: The directory is not empty, re-running this part might end up with loss of the existing data!")
        pass

    if pairs_mode == "true" and read_config("Trimmomatic", "end_mode") == "SE":
        s += ycolor("WARNING: You're running Trimmomatic in 'Single End' mode, but you have pair file!")

    return s


def run(pairs_mode):
    txt = "Trimmomatic Part finished."
    try:
        if pairs_mode == 'true':
            subprocess.call(['./src/bash/trimmomatic_pair.sh'])
        else:
            subprocess.call(['./src/bash/trimmomatic.sh'])

        if read_config("EMAIL", "active") == "true":
            parmEmail(txt)

    except Exception as e:
        logging.error(traceback.format_exc())
        print(rcolor(e.message))
        txt = e.message
        # email part
        if read_config("EMAIL", "active") == "true":
            parmEmail(txt)
        message(2, "something is going wrong... please run again. ")
        # set 1 to resuming
        replace_config("STATUS", "st_trim", "1")


def run_trimmomatic(status):
    # running preparing files
    try:
        preparing_part()
        print(info_trimmomatic())
        '''
        gen_type = read_config("GENERAL", "genome_type")
        if (gen_type in ["Human", "Maize"]):
            replace_config("GENERAL", "parallel_mode", "false")
        '''

        pairs_mode = read_config("GENERAL", "pairs_mode")
        # checking using SE but pair file
        if pairs_mode == "true" and read_config("Trimmomatic", "end_mode") == "SE":
            print ycolor("WARNING: You're running Trimmomatic in 'Single End' mode, but you have pair file!")

        # creating list of file
        list_dataset = find_file_pattern(read_config("GENERAL", "raw_dataset"), "*.gz")
        # writing all list to the file
        res_loc = read_config("GENERAL", "result_pipeline")
        with open(res_loc+"/trimmomatic-files/"+'list-files.lst', 'wb') as f:
            for item in list_dataset:
                f.write('%s\n' % item)

        if status:
            run(pairs_mode)
        else:
            if confirm_run():
                print qucolor("\nRunning Trimmomatic Part...")
                run(pairs_mode)
                message(0, "Processing files is finished, You can check the log files in Menu, part 'Trimmomatic-log' ")

    except Exception as e:
        logging.error(traceback.format_exc())
        print(rcolor(e.message))
        txt = e.message
        # email part
        if read_config("EMAIL", "active") == "true":
            parmEmail(txt)
        message(2, "something is going wrong... please run again. ")
        # set 1 to resuming
        replace_config("STATUS", "st_trim", "1")


    return



