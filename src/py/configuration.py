#!/usr/bin/env python2
__author__ = "Yadollah Shahryary Dizaji"
__title__ = "configuration.py"
__description__ = "Configuration file for Pipeline."
__license__ = "GPL"
__version__ = "1.0.0"
__email__ = "shahryary@gmail.com"




# setup file for pipeline
import os,fnmatch,sys
import traceback
import logging
from os import listdir
from os.path import isfile, join
import ConfigParser
import subprocess
import re
from globalParameters import true_false_fields_config
class GrumpyConfigParser(ConfigParser.ConfigParser):
  """Virtually identical to the original method, but delimit keys and values with '=' instead of ' = '"""
  def write(self, fp):
    if self._defaults:
      fp.write("[%s]\n" % DEFAULTSECT)
      for (key, value) in self._defaults.items():
        fp.write("%s = %s\n" % (key, str(value).replace('\n', '\n\t')))
      fp.write("\n")
    for section in self._sections:
      fp.write("[%s]\n" % section)
      for (key, value) in self._sections[section].items():
        if key == "__name__":
          continue
        if (value is not None) or (self._optcre == self.OPTCRE):
          # This is the important departure from ConfigParser for what you are looking for
          key = "=".join((key, str(value).replace('\n', '\n\t')))

        fp.write("%s\n" % (key))
      fp.write("\n")

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[1;32m'
    NOTE = '\033[1;35m'
    WARNING = '\033[1;33m'
    UPDATE = '\033[0;36m'
    FAIL = '\033[91m'
    QUES = '\033[1;96m'
    RED = '\033[1;31m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



menu_act={}
stored_place={}


def conf_menu():
    print "=="*25
    print "\nConfiguration part,\n"
    print "Please choose from the option:\n"
    print ycolor("\t1.")+" Path: RAW files"
    print ycolor("\t2.")+" Path: Export results"
    print ycolor("\t3.")+" Path: Reference Genome"
    print ycolor("\t4.")+" Read-trimming parameters"
    print ycolor("\t5.")+" Path: QC-Fastq"
    print ycolor("\t6.")+" Alignment parameters"
    print ycolor("\t7.")+" Methimpute parameters"
    print ycolor("\t8.")+" Parallel mode"
    print ycolor("\t9.")+" See configured parameters"
    print rcolor("B.")+" Back to main Menu\n"
    choice = raw_input(">>  ")
    exec_menu(choice)
    return


# Execute menu
def exec_menu(choice):
    ch = choice
    if ch == '':
        menu_act['conf_menu']()
    else:
        try:
            menu_act[ch]()
        except KeyError:
            print "Invalid selection, please try again.\n"
            menu_act['conf_menu']()
    return


def replace_config(section, old_string, new_string):

    config = GrumpyConfigParser()
    config.optionxform = str
    config.read('config/pipeline.conf')
    config.set(section, old_string, new_string)
    with open('config/pipeline.conf', 'wb') as config_file:
        config.write(config_file)


def read_config(section, get_string):

    config = GrumpyConfigParser()
    config.optionxform = str
    config.read('config/pipeline.conf')
    val_str = config.get(section, get_string)
    return val_str



def query_yes_no(question, default):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(qucolor(question) + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


def inputNumber(message):
    while True:
        try:
            userInput = int(raw_input(message))
        except ValueError:
            print("Not an integer! Try again.")
            continue
        else:
            return userInput
            break


def message(msg_code, msg):

    if msg_code == 0:
        print "\n"+bcolors.OKBLUE + msg + bcolors.ENDC+"\n"
        raw_input("Please, press ENTER to continue ...")
        exec_menu('')
    elif msg_code == 1:
        print bcolors.FAIL + msg + bcolors.ENDC+"\n"
    elif msg_code == 2:
        print bcolors.WARNING + msg + bcolors.ENDC+"\n"
        raw_input("Please, press ENTER to continue ...")
        exec_menu('')
    elif msg_code == 3:
        print bcolors.OKGREEN + msg + bcolors.ENDC+"\n"
    elif msg_code == 4:
        print bcolors.NOTE + msg + bcolors.ENDC+"\n"
    return


def mcolor(txt):
    # colorize just location or some path
    return bcolors.OKBLUE + str(txt) + bcolors.ENDC


def ycolor(txt):
    # colorize just location or some path
    return bcolors.WARNING + str(txt) + bcolors.ENDC


def gcolor(txt):
    return "\n"+bcolors.UPDATE + str(txt) + bcolors.ENDC


def rcolor(txt):
    return "\n"+bcolors.RED + str(txt) + bcolors.ENDC


def qucolor(txt):
    return bcolors.QUES + str(txt) + bcolors.ENDC


def find_file_pattern(path, pattern):

    listOfFiles = list()
    for (dirpath, dirnames, filenames) in os.walk(path):
        listOfFiles += [os.path.join(dirpath, file) for file in filenames]

    # Print the files
    list_dataset = []
    for elem in listOfFiles:
        if fnmatch.fnmatch(elem, pattern):
            list_dataset.append(elem)
    return list_dataset



def confirm(config_section, config_value, mcode):
    str_conf = read_config(config_section, config_value)
    if not str_conf == '':
        if int(mcode == 33):
            if str_conf != "true":
                str_conf = "Currently your files are 'Single-end'."
                mcode = 3
            else:
                str_conf = "Currently your files are 'Paired-end'."
                mcode = 3

        print "You set the value to: " + mcolor(str_conf)+"\n"
        # it seems user configured before so asking again to re-config.
        answer = query_yes_no("Do you want to re-config this part?", None)
        if answer:
            return True
        else:
            message(mcode, "Keeping the default value.")
    else:
        print "This is the first time you are configuring this parameter ..."
        return True


def raw_dataset():
    print "\nIn this part you can specify your data-set location."
    print "If you have data-set in pair-end mode, you have to give the pattern of extension.\n"
    try:
        if confirm("GENERAL", "raw_dataset", 3):
                response = raw_input("\nPlease enter the RAW files directory: ")
                while not (os.path.isdir(response)):
                    message(1, "The directory is not exist!.")
                    response = raw_input("Please enter the RAW files directory: ")
                stored_place['raw_dataset'] = response
                # check if there is files & give the directory size
                list_dataset = find_file_pattern(response, "*.gz")
                print "\nFounded " + mcolor(len(list_dataset)) + " files in the directory."
                raw_size = subprocess.check_output(['du', '-h', response]).split()[-2].decode('utf-8')
                size = [float(s) for s in re.findall(r'-?\d+\.?\d*', raw_size)]
                replace_config("GENERAL", "dataset_size", size[0])
                replace_config("GENERAL", "raw_dataset", response)
                replace_config("GENERAL", "number_of_dataset", len(list_dataset))
                print "\nAlso, the size of your data-set almost: "+mcolor(raw_size)
                message(4, "Configuration for Raw files location updated!")
        else:
            pass
        # detect the pattern if there is pairs file
        print gcolor("--Configuration part for file Pattern--\n")

        if confirm("GENERAL", "pairs_mode", 33):
            # asking for enable /disable
            print "\nYou can change the default value for your files pattern."
            if read_config("GENERAL", "pairs_mode") == "true":
                print "Currently you have files in "+ ycolor("Pair-end case.\n")
            else:
                print "Currently you have files in "+ycolor("Single-end case.\n")

            # pring ask enable or disable it
            sys.stdout.write(ycolor("1") + " -You have files in Single-end case.\n")
            sys.stdout.write(ycolor("2") + " -You have files in Pairs-end case.\n")
            file_mode = inputNumber("\nPlease enter the number to select:")
            while not int(file_mode) in range(1, 3):
                file_mode = inputNumber("Please enter the valid number:")

            if int(file_mode) == 1:
                replace_config("GENERAL", "pairs_mode", "false")
                replace_config("GENERAL", "first_pattern", "")
                replace_config("GENERAL", "secnd_pattern", "")
            else:
                print "--" * 30
                print(mcolor("Please specify your data-set pattern."))
                print(mcolor("For ex: "))
                print(gcolor("XXXXX_1.fq.gz,\nXXXXX_2.fq.gz"))
                print("First pattern will be: "+mcolor("_1.fq.gz"))
                print("And the second pattern is: "+mcolor("_2.fq.gz"))
                print "--" * 30
                pattern_one = raw_input("\nPlease enter the pattern for First pair: ")
                pattern_two = raw_input("\nPlease enter the pattern for Second pair: ")
                replace_config("GENERAL", "pairs_mode", "true")
                replace_config("GENERAL", "first_pattern", pattern_one)
                replace_config("GENERAL", "secnd_pattern", pattern_two)
                # print list of files that we detected by pattern
                print("\nFirst pair"+"\t\t"+"Second pair")
                print "---"*10
                first_pairs = []
                secd_pairs = []
                for file_one in find_file_pattern(read_config("GENERAL", "raw_dataset"), "*"+pattern_one):
                    first_pairs.append(file_one)
                for file_two in find_file_pattern(read_config("GENERAL", "raw_dataset"), "*" + pattern_two):
                    secd_pairs.append(file_two)
                first_pairs=sorted(first_pairs)
                secd_pairs=sorted(secd_pairs)
                for item in range(len(first_pairs)):
                    print first_pairs[item] + "\t\t" + secd_pairs[item]
                print ycolor("\nPlease check the pairs that listed correctly, otherwise give the different pattern.")


        else:
            # skip configuration

            pass
        message(0, "Configuration updated!")
    except subprocess.CalledProcessError:
            message(2, "It seems you don't have permission, please change the directory.")
    except Exception as e:
        logging.error(traceback.format_exc())
        message(2, "Something is going wrong... please run again. ")


def result_pipeline():
    try:
        if confirm("GENERAL", "result_pipeline",0):
            response = raw_input("\nPlease enter the result directory."
                                 "\n(we will write all the results inside this folder)"
                                 "\n>> ")
            '''
            check for permission! is it writable?
            '''
            while not (os.access(response, os.W_OK)):
                message(1, "It seems you don't have permission to write in this directory")
                response = raw_input("Please enter another location: ")

            # checking space and warning to user
            size = subprocess.check_output(['df', '-Bm', response]).split()[-3].decode('utf-8')
            size = [float(s) for s in re.findall(r'-?\d+\.?\d*', size)]
            number_of_dataset=float(read_config("GENERAL", "number_of_dataset"))
            dataset_size = float(read_config("GENERAL", "dataset_size"))
            # size per file
            per_file = round(dataset_size/number_of_dataset)

            print "-----" * 20
            print "\nYou have " + mcolor(size[0]) + " M.byte free space in your disk."
            print "The list bellow is recommendation to have Free space in your disk."
            print "(This calculation based on your data-set size.)"
            print "\nFree space for Trimmomatic part: " + mcolor(round(per_file * number_of_dataset * 1.2)) + " Gig."
            print "Free space for QC-Fastq-report: " + mcolor(round(2 * number_of_dataset)) + " MB."
            print "Free space for Bismark Mapper part: " + mcolor(round(per_file * number_of_dataset * 1.8)) + " Gig."
            print "Free space for Qc-Fastq Bam report: " + mcolor(round(2 * number_of_dataset)) + " MB."
            print "Free space for Bismark Deduplication: " + mcolor(round(per_file * number_of_dataset * 1.1)) + " Gig."
            print "Free space for Bismark Methylation Extractor:" + mcolor(round(per_file * number_of_dataset * 6)) + " Gig."
            print "Free space for Methimpute: " + mcolor(round(per_file * number_of_dataset * 1.4)) + " Gig."
            print "Free space for Other report: " + mcolor(round(per_file * number_of_dataset * 100)) + " MB."
            print bcolors.WARNING + "Note: We recommended at least " \
                  + str(number_of_dataset * 10) + " Gigabyte free space." + bcolors.ENDC
            print "-----" * 20
            stored_place['result_pipeline'] = response
            replace_config("GENERAL", "result_pipeline", response)
            message(0, "Configuration updated! ")
        else:
            pass
    except Exception as e:
        logging.error(traceback.format_exc())
        message(2, "Something is going wrong... please run again. ")


def genome_ref():
    try:
        if confirm("GENERAL", "genome_ref",0):
            print "Please specify a reference genome location.\n"
            print "(We will generate the Bisulfite_Genome folder inside this folder.)\n"
            response = raw_input(">> ")
            while not (os.path.isdir(response)):
                message(1, "The directory is not exist!.")
                response = raw_input("Please specify a reference genome location:")
            stored_place['genome_ref'] = response
            # call immediately after folder to ask file
            genome_name()
        else:
            pass
    except Exception as e:
        logging.error(traceback.format_exc())
        message(2, "Something is going wrong... please run again. ")


def genome_name():
    '''
    searching for genome reference file name.
    by default user inputted the directory of ref.genome
    so we are looking for files then asking from user
    :return: name of genome
    '''
    di_tosearch = stored_place['genome_ref']
    onlyfiles = [f for f in listdir(di_tosearch) if isfile(join(di_tosearch, f))]

    if len(onlyfiles) == 0:
        message(1, "Could't find any Reference file under "+di_tosearch+" folder.")
        message(2, "Please, copy Ref. genome into "+di_tosearch+" and re-config again.")

    else:
        print("Found file(s) under the genome reference folder.\n")
        for file in onlyfiles:
            sys.stdout.write(ycolor(str(onlyfiles.index(file)))+" : "+file+"\n")
        response = inputNumber("\nPlease enter the number to select: ")
        while not int(response) in range(0, len(onlyfiles)):
            response = inputNumber("Please enter the valid number: ")

        response = onlyfiles[int(response)]
        replace_config("GENERAL", "genome_ref", di_tosearch)
        replace_config("GENERAL", "genome_name", response)
        message(0, "Configuration updated!")


def trimmomatic():
    # checking for java
    java_check()
    #
    try:
        if confirm("Trimmomatic", "trim_path",3):

            response = raw_input("Please enter the Trimmomatic location: ")
            while not (os.path.isdir(response)):
                message(1, "The directory is not exist!.")
                response = raw_input("Please enter the Trimmomatic location:")

            # searching for jar file!
            adap_tosearch = response
            list_jar = []
            for jarfile in find_file_pattern(adap_tosearch, "*.jar"):
                list_jar.append(jarfile)

            if len(list_jar) > 1:
                message(1, "There is more than one Jar file in "+adap_tosearch+" folder.")
                message(2, "Please check directory "+adap_tosearch+" and re-config again.")
            else:
                print("Found: "+ ycolor(list_jar[0])+" file.")
                replace_config("Trimmomatic", "trim_path", adap_tosearch)
                replace_config("Trimmomatic", "trim_jar", list_jar[0])
        else:
            pass
            # find all fasta file from adaptor folder

        print gcolor("--Configuration part for Adapter--")
        if confirm("Trimmomatic", "name_adap",3):
            adap_tosearch=read_config("Trimmomatic", "trim_path")
            list_adaptors = []
            for file in find_file_pattern(adap_tosearch+"/adapters/", "*.fa"):
                list_adaptors.append(file)

            if len(list_adaptors) == 0:
                message(1, "Could't find any Jar file under "+adap_tosearch+" folder.")
                message(2, "Please check directory "+adap_tosearch+" and re-config again.")

            else:
                print("List of adapters "+adap_tosearch+"/adapters/: \n")
                for file in list_adaptors:
                    sys.stdout.write(ycolor(str(list_adaptors.index(file)))+" : "+file+"\n")

                response = inputNumber("\nPlease enter the number to select:")
                while not int(response) in range(0, len(list_adaptors)):
                    response = inputNumber("Please enter the valid number:")

                response = list_adaptors[int(response)]

                replace_config("Trimmomatic","name_adap", response)
                message(4, "Configuration updated!")

        else:
            pass

        print gcolor("--Configuration part for running mode--")
        if confirm("Trimmomatic", "end_mode",3):
                '''
                 Paired End or Single End?
                '''
                sys.stdout.write(ycolor("1")+"-Single-End\n")
                sys.stdout.write(ycolor("2")+"-Paired-End\n")
                end_mode = inputNumber("\nPlease enter the number to select:")
                while not int(end_mode) in range(1, 3):
                    end_mode = inputNumber("Please enter the valid number:")
                mode = ""
                if int(end_mode) == 1:
                    mode = "SE"
                else:
                    mode = "PE"
                replace_config("Trimmomatic", "end_mode", mode)
                message(4, "Configuration updated!")
        else:
            pass

        print gcolor("--Configuration part for ILLUMINACLIP--")
        if confirm("Trimmomatic", "ill_clip", 3):
                '''
                 ILLUMINACLIP parameters 
                '''

                user_input = raw_input("\nPlease enter the number of ILLUMINACLIP[ "+
                                       read_config("Trimmomatic", "name_adap")+" ]: ")
                replace_config("Trimmomatic", "ill_clip", user_input)
                message(4, "Configuration updated!")

        else:
            pass

        print gcolor("--Configuration part for LEADING--")
        if confirm("Trimmomatic", "LEADING", 3):
                '''
                 LEADING parameters 
                '''
                user_input = inputNumber("\nPlease enter the value of LEADING: ")
                replace_config("Trimmomatic", "LEADING", user_input)
                message(4, "Configuration updated!")
        else:
            pass

        print gcolor("--Configuration part for TRAILING--")
        if confirm("Trimmomatic", "TRAILING", 3):
                '''
                 TRAILING parameters 
                '''

                user_input = inputNumber("\nPlease enter the value of TRAILING: ")
                replace_config("Trimmomatic", "TRAILING", user_input)
                message(4, "Configuration updated!")
        else:
            pass

        print gcolor("--Configuration part for SLIDINGWINDOW--")
        if confirm("Trimmomatic", "SLIDINGWINDOW", 3):
                '''
                 SLIDINGWINDOW parameters 
                '''
                user_input = raw_input("\nPlease enter the value of SLIDINGWINDOW: ")
                replace_config("Trimmomatic", "SLIDINGWINDOW", user_input)

        else:
            pass

        print gcolor("--Configuration part for MINLEN--")
        if confirm("Trimmomatic", "MINLEN", 3):
                '''
                 MINLEN parameters 
                '''
                user_input = inputNumber("\nPlease enter the value of MINLEN: ")
                replace_config("Trimmomatic", "MINLEN", user_input)

        else:
            pass

        print gcolor("--Configuration part for Threading--")
        if confirm("Trimmomatic", "n_th", 3):
                '''
                Number of thread to process. there is a default value.
                '''
                number_thread = inputNumber("\nPlease enter the number of thread:")
                replace_config("Trimmomatic", "n_th", number_thread)

        else:
            pass

        message(0, "Configuration Updated!")
    except Exception as e:
        logging.error(traceback.format_exc())
        message(2, "Something is going wrong... please run again. ")


def java_check():

    try:
        if read_config("Trimmomatic", "java_path").replace(" ", "") == '':
            location = subprocess.check_output(['which', 'java'])
        else:
            location=read_config("Trimmomatic", "java_path")
            print "You set the location to: " + mcolor(location)

        if location != None:
            print "Detected Java program in location: "+ mcolor(location)
            answer = query_yes_no("Do you want to change the Java Path?", None)
            if answer:
                location = raw_input("Please enter the Java location: ")
                while not (os.path.isfile(location)):
                    message(1, "Couldn't find any java program!.")
                    location = raw_input("Please try again: ")
                replace_config("Trimmomatic", "java_path", location)
            else:
                replace_config("Trimmomatic", "java_path", location)
                stored_place['java_path'] = location

    except subprocess.CalledProcessError:
        message(1, "\nIt seems you don't have Java in your PATH, Please install and export to the your PATH.")
        message(4, "Tip: you can export with following command.[ export PATH=JAVA_LOCATION/java:$PATH ]")
    except Exception as e:
        logging.error(traceback.format_exc())
        message(2, "Something is going wrong... please run again. ")


def fastq_path():

    try:
        if read_config("GENERAL", "fastq_path").replace(" ", "") == '':
            location = subprocess.check_output(['which', 'fastqc'])
            detected = True
        else:
            location=read_config("GENERAL", "fastq_path")
            print "You set the location to: " + mcolor(location)
            detected = False

        if location != None:
            if detected:
               print "Detected FastQC program in location: "+ mcolor(location)

            answer = query_yes_no("Do you want to change the location?", None)
            if answer:
                location = raw_input("Please enter the FastQC location: ")
                while not (os.path.isfile(location)):
                    message(1, "Fastq file not found!.")
                    location = raw_input("Please try again: ")
                replace_config("GENERAL", "fastq_path", location)
            else:
                replace_config("GENERAL", "fastq_path", location)
                stored_place['fastq_path'] = location

    except subprocess.CalledProcessError:
        message(1, "It seems you don't have FastQc in your PATH")
        fastq = raw_input("Please enter the FastQC location: ")
        while not (os.path.isdir(fastq)):
            message(1, "The directory is not exist!.")
            fastq = raw_input("Please try again: ")
        replace_config("GENERAL", "fastq_path", fastq)

    except Exception as e:
        logging.error(traceback.format_exc())
        message(2, "Something is going wrong... please run again. ")

    message(0, "Configuration updated for FastQC!")


def bismark_path():

    try:
        if read_config("Bismark", "bismark_path").replace(" ", "") == '':

            location_bis = subprocess.check_output(['which', 'bismark'])
            detected = True
        else:
            location_bis = read_config("Bismark", "bismark_path")
            print "You set the location to: " + mcolor(location_bis)
            detected = False

        if location_bis != None:

            if detected:
                print "Detected bismark program in location: " + mcolor(location_bis)

            answer = query_yes_no("Do you want to change the location?", None)
            if answer:
                location_bis = raw_input("Please enter the Bismark location: ")
                while not (os.path.isdir(location_bis)):
                    message(1, "The directory is not exist!.")
                    location_bis = raw_input("Please try again: ")
                replace_config("Bismark", "bismark_path", location_bis)
                message(4, "Configuration updated!")
            else:
                replace_config("Bismark", "bismark_path", location_bis)
                message(3, "We will keep the default value!")

    except subprocess.CalledProcessError:
        message(1, "It seems you don't have Bismark in your PATH")
        bismark = raw_input("Please enter the Bismark location: ")
        while not (os.path.isdir(bismark)):
            message(1, "The directory is not exist!.")
            bismark = raw_input("Please try again: ")
        replace_config("Bismark", "bismark_path", bismark)
        message(4, "Configuration updated!")

    except Exception as e:
        logging.error(traceback.format_exc())
        message(2, "Something is going wrong... please run again. ")

    '''
        Sets the number of parallel instances of Bismark to be run concurrently
    '''
    print gcolor("--Configuration part for Bismark Parallel--")
    if confirm("Bismark", "bis_parallel", 3):
        user_input = inputNumber("\nPlease set the number of parallel: ")
        replace_config("Bismark", "bis_parallel", user_input)
        message(4, "Configuration updated!")

    else:
        pass

    '''
        Sets buffer size!
    '''
    print gcolor("--Configuration part for Bismark buffer Size--")
    if confirm("Bismark", "buf_size", 3):
        user_input = inputNumber("\nPlease set the size of buffer (Gigabyte): ")
        replace_config("Bismark", "buf_size", user_input)
        message(4, "Configuration updated!")

    else:
        pass

    '''
        Sets nucleotide !
    '''
    print gcolor("--Configuration part for Bismark Nucleotide--")
    print ycolor("To change the Nucleotide report option please Enable it.")
    if confirm("Bismark", "nucleotide", 3):
        sys.stdout.write(ycolor("\n1")+"-Enable this option.\n")
        sys.stdout.write(ycolor("2")+"-Disable this option.\n")
        nu_mode = inputNumber("Please enter the number to select:")
        while not int(nu_mode) in range(1, 3):
            nu_mode = inputNumber("Please enter the valid number:")

        if int(nu_mode)==1:
            mode="true"
        else:
            mode="false"
        replace_config("Bismark", "nucleotide", mode)
        message(4, "Configuration updated!")

    else:
        pass

    message(0, "Configuration updated for Bismark Mapper!")

def en_di():

    sys.stdout.write(ycolor("\n1") + "-Enable this option.\n")
    sys.stdout.write(ycolor("2") + "-Disable this option.\n")
    nu_mode = inputNumber("Please enter the number to select:")
    while not int(nu_mode) in range(1, 3):
        nu_mode = inputNumber("Please enter the valid number:")

    if int(nu_mode) == 1:
        mode = "true"
    else:
        mode = "false"

    return mode

def methimpute():
    try:
        print gcolor("--Running with intermediate status--")
        if confirm("Methimpute", "intermediate", 3):
            val = en_di()
            replace_config("Methimpute", "intermediate", val)
            message(4, "Configuration updated!")
        else:
            pass

        print gcolor("--Generating quality reports (fit, model convergence, histogram,etc.)--")
        if confirm("Methimpute", "fit_output", 3):
            val = en_di()
            replace_config("Methimpute", "fit_output", val)
            message(4, "Configuration updated!")
        else:
            pass

        print gcolor("--Generating enrichment reports( pdf files )--")
        if confirm("Methimpute", "enrichment_plot", 3):
            val = en_di()
            replace_config("Methimpute", "enrichment_plot", val)
            message(4, "Configuration updated!")

        else:
            pass

        print gcolor("--Generating TEs reports--")
        if confirm("Methimpute", "TES_report", 3):
            val = en_di()
            replace_config("Methimpute", "TES_report", val)
            message(4, "Configuration updated!")

        else:
            pass

        print gcolor("--Generating genes reports--")
        if confirm("Methimpute", "genes_report", 3):
            val = en_di()
            replace_config("Methimpute", "genes_report", val)
            message(4, "Configuration updated!")

        else:
            pass

        print gcolor("--Minimum read coverage value (for quick run)--")
        if confirm("Methimpute", "mincov", 3):
            user_input = raw_input("\nPlease enter the value of min.coverage: ")
            replace_config("Methimpute", "mincov", user_input)
            message(4, "Configuration updated!")
        else:
            pass

        message(0, "Configuration Saved!")

    except Exception as e:
        logging.error(traceback.format_exc())
        print(rcolor(e.message))
        message(2, "Something is going wrong... please run again. ")

def parallel_mode():

    '''
        Set Parallel mode!
    '''
    try:
        print gcolor("Configuration part for running in Parallel mode")
        if confirm("GENERAL", "parallel_mode", 3):
                location = subprocess.check_output(['which', 'parallel'])
                print "Detected Parallel program in location: " + mcolor(location)
                answer = query_yes_no("Do you want to use Parallel mode?", None)
                if answer:
                    par = "true"
                    user_input = inputNumber("\nPlease set the number of Jobs:")
                    replace_config("GENERAL", "npar", user_input)
                else:
                    par = "false"
                replace_config("GENERAL", "parallel_mode", par)
        else:
            pass
        message(0, "Configuration updated!")
    except subprocess.CalledProcessError:
        message(2, "\nIt seems you don't have Parallel in your PATH, Please install and export to the your PATH.")

    except Exception as e:
        logging.error(traceback.format_exc())
        message(2, "Something is going wrong... please run again. ")


def show_config():
    print "\n"+"=="*30
    print "Here is summary of configuration parameters: \n"
    print "- RAW files location: " + mcolor(read_config("GENERAL", "raw_dataset"))
    print "- Number and Size of the data-set: " + mcolor(read_config("GENERAL", "number_of_dataset"))\
          + " Files and Total size: " + mcolor(read_config("GENERAL", "dataset_size"))+" Gigabyte"
    print "- The directory of results: " + mcolor(read_config("GENERAL", "result_pipeline"))
    print "- Genome folder location: " + mcolor(read_config("GENERAL", "genome_ref"))
    print "     -- Genome Reference name: " + mcolor(read_config("GENERAL", "genome_name"))
    print "- Paired End: " + mcolor(true_false_fields_config(read_config("GENERAL", "pairs_mode"),""))
    print "- Trimmomatic location: "+ mcolor(read_config("Trimmomatic", "trim_path"))
    print "     -- JAVA path: " + mcolor(read_config("Trimmomatic", "java_path"))
    print "     -- ILLUMINACLIP: " + mcolor(read_config("Trimmomatic", "name_adap"))\
          +":"+mcolor(read_config("Trimmomatic", "ill_clip"))

    print "     -- LEADING: " + mcolor(read_config("Trimmomatic", "LEADING"))
    print "     -- TRAILING: " + mcolor(read_config("Trimmomatic", "TRAILING"))
    print "     -- SLIDINGWINDOW: " + mcolor(read_config("Trimmomatic", "SLIDINGWINDOW"))
    print "     -- MINLEN: " + mcolor(read_config("Trimmomatic", "MINLEN"))
    print "     -- Number of Threads: " + mcolor(read_config("Trimmomatic", "n_th"))

    print "- QC-Fastq path: "+ mcolor(read_config("GENERAL", "fastq_path"))
    print "- Bismark parameters: "+ mcolor(read_config("Bismark", "bismark_path"))
    print "     -- Nucleotide status: " + mcolor(read_config("Bismark", "nucleotide"))
    print "     -- Number of Parallel: " + mcolor(read_config("Bismark", "bis_parallel"))+" Threads."
    print "     -- Buffer size: " + mcolor(read_config("Bismark", "buf_size"))+" Gigabyte."
    print "     -- Samtools Path: " + mcolor(read_config("Bismark", "samtools_path"))
    print "     -- Intermediate for MethExtractor: " +mcolor(true_false_fields_config(read_config("Bismark", "intermediate_files"),""))
    print "- Methylation extraction parameters( Only for quick run)"
    print "     -- Minimum read coverage: " + mcolor(read_config("Methimpute", "mincov"))
    print "- Methimpute Part:"
    print "     -- Methimpute Intermediate : " + mcolor(true_false_fields_config(read_config("Methimpute", "intermediate"), ""))
    print "     -- Methimpute Fit reports: " + mcolor(true_false_fields_config(read_config("Methimpute", "fit_output"), ""))
    print "     -- Methimpute Enrichment plots: " + mcolor(true_false_fields_config(read_config("Methimpute", "enrichment_plot"), ""))
    print "     -- Methimpute TEs reports: " + mcolor(true_false_fields_config(read_config("Methimpute", "TES_report"), ""))
    print "     -- Methimpute genes reports: " + mcolor(true_false_fields_config(read_config("Methimpute", "genes_report"), ""))
    print "     -- Methimpute Context: " + mcolor("All/CHG|CHH|CG")
    print "- Parallel mode is: " +mcolor(true_false_fields_config(read_config("GENERAL", "parallel_mode"),""))
    print "     -- Number of Parallel: " + mcolor(read_config("GENERAL", "npar"))+" Cores."

    message(0, "...")




# Back program
def exit():
     pass


# Menu definition
menu_act = {
    'conf_menu': conf_menu,
    '1': raw_dataset,
    '2': result_pipeline,
    '3': genome_ref,
    '4': trimmomatic,
    '5': fastq_path,
    '6': bismark_path,
    '7': methimpute,
    '8': parallel_mode,
    '9': show_config,

    'b': exit,
}


def __running__():
    conf_menu()
