import npyscreen
import curses
import os,fnmatch,sys
import traceback
import logging
from os import listdir
from os.path import isfile, join
import ConfigParser
import subprocess
import re
import time
import textwrap
from distutils.util import strtobool

class runTaskName(npyscreen.FixedText):
    _contained_widget = npyscreen.FixedText

class CustomMultiLineEdit_RP(npyscreen.MultiLineEdit):
    def update(self, clear=True,):
        super(CustomMultiLineEdit_RP, self).update(clear=clear)
        self.color = 'CAUTION'

class InputBoxInfoRP(npyscreen.BoxTitle):
    _contained_widget = CustomMultiLineEdit_RP
    def update(self, clear=True,):
        super(InputBoxInfoRP, self).update(clear=clear)
        self.color = 'CURSOR'

class GrumpyConfigParser(ConfigParser.ConfigParser):
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

class FixedText0_RP(npyscreen.FixedText):
    def update(self, clear=True,):
        super(FixedText0_RP, self).update(clear=clear)
        self.show_bold = True
        self.color = 'CURSOR'
    def display(self):
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_editedP0"))

class FixedText1_RP(npyscreen.FixedText):
    def update(self, clear=True,):
        super(FixedText1_RP, self).update(clear=clear)
        self.show_bold = True
        self.color = 'CURSOR'
    def display(self):
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_editedP1"))
        new_handlers = {
            curses.ascii.NL: self.switchForm
        }
        self.add_handlers(new_handlers)

    def switchForm(self, _input):
        self.parent.parentApp.RP = "Run Trimommatic"
        self.parent.parentApp.switchForm('Run_popup')

class FixedText2_RP(npyscreen.FixedText):
    def update(self, clear=True,):
        super(FixedText2_RP, self).update(clear=clear)
        self.show_bold = True
        self.color = 'CURSOR'
    def display(self):
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_editedP2"))
        new_handlers = {
            curses.ascii.NL: self.switchForm
        }
        self.add_handlers(new_handlers)

    def switchForm(self, _input):
        self.parent.parentApp.RP = "Run QC-Fastq-report"
        self.parent.parentApp.switchForm('Run_popup')

class FixedText3_RP(npyscreen.FixedText):
    def update(self, clear=True,):
        super(FixedText3_RP, self).update(clear=clear)
        self.show_bold = True
        self.color = 'CURSOR'
    def display(self):
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_editedP3"))
        new_handlers = {
            curses.ascii.NL: self.switchForm
        }
        self.add_handlers(new_handlers)

    def switchForm(self, _input):
        self.parent.parentApp.RP = "Run Bismark Mapper"
        self.parent.parentApp.switchForm('Run_popup')

class FixedText4_RP(npyscreen.FixedText):
    def update(self, clear=True,):
        super(FixedText4_RP, self).update(clear=clear)
        self.show_bold = True
        self.color = 'CURSOR'
    def display(self):
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_editedP4"))
        new_handlers = {
            curses.ascii.NL: self.switchForm
        }
        self.add_handlers(new_handlers)

    def switchForm(self, _input):
        self.parent.parentApp.RP = "Run QC-Bam report"
        self.parent.parentApp.switchForm('Run_popup')

class FixedText5_RP(npyscreen.FixedText):
    def update(self, clear=True,):
        super(FixedText5_RP, self).update(clear=clear)
        self.show_bold = True
        self.color = 'CURSOR'
    def display(self):
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_editedP5"))
        new_handlers = {
            curses.ascii.NL: self.switchForm
        }
        self.add_handlers(new_handlers)

    def switchForm(self, _input):
        self.parent.parentApp.RP = "Run Bismark-deduplicate"
        self.parent.parentApp.switchForm('Run_popup')

class FixedText6_RP(npyscreen.FixedText):
    def update(self, clear=True,):
        super(FixedText6_RP, self).update(clear=clear)
        self.show_bold = True
        self.color = 'CURSOR'
    def display(self):
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_editedP6"))
        new_handlers = {
            curses.ascii.NL: self.switchForm
        }
        self.add_handlers(new_handlers)

    def switchForm(self, _input):
        self.parent.parentApp.RP = "Run Bismark Meth. Extractor"
        self.parent.parentApp.switchForm('Run_popup')

class FixedText7_RP(npyscreen.FixedText):
    def update(self, clear=True,):
        super(FixedText7_RP, self).update(clear=clear)
        self.show_bold = True
        self.color = 'CURSOR'
    def display(self):
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_editedP7"))
        new_handlers = {
            curses.ascii.NL: self.switchForm
        }
        self.add_handlers(new_handlers)

    def switchForm(self, _input):
        self.parent.parentApp.RP = "Generate CX reports"
        self.parent.parentApp.switchForm('Run_popup')

class FixedText8_RP(npyscreen.FixedText):
    def update(self, clear=True,):
        super(FixedText8_RP, self).update(clear=clear)
        self.show_bold = True
        self.color = 'CURSOR'
    def display(self):
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_editedP8"))
        new_handlers = {
            curses.ascii.NL: self.switchForm
        }
        self.add_handlers(new_handlers)

    def switchForm(self, _input):
        self.parent.parentApp.RP = "Run Methimpute"
        self.parent.parentApp.switchForm('Run_popup')

def checkDirectoryExists(dirpath_to_check):
    if os.path.isdir(dirpath_to_check):
        return True
    else:
        return False

class OK_Button_RP_run_popup(npyscreen.ButtonPress):
    def whenPressed(self):
        self.parent.parentApp.queue_event(npyscreen.Event("OK_Button_RP_run_popup_pressed"))

def formatted_run_box_RP(log_path):
    with open(log_path, 'r') as myfile:
        log_raw = myfile.readlines()

    log_new = ""
    for a in log_raw:
        log_new += (textwrap.fill(a, 140))
        log_new += "\n\n"

    return log_new.splitlines()

class Pager_custom(npyscreen.Pager):
    def h_scroll_line_down(self, input):
        self.start_display_at += 1
        #original if self.scroll_exit and self.start_display_at >= len(self.values)-self.start_display_at+1:
        if self.scroll_exit and self.start_display_at >= len(self.values) - self.parent.parentApp.numLinesPager+2:
            self.editing = False
            self.how_exited = 1

class RunBox(npyscreen.BoxTitle):
    _contained_widget = Pager_custom
    def display(self):
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_edited_RP_popup"))

class del_inter_file_select(npyscreen.TitleSelectOne):
    def update(self, clear = True):
        if clear: self.clear()
        if self.hidden: return False
        if self.editing: 
            self.label_widget.show_bold = True
            self.label_widget.color = 'LABELBOLD'
        else: 
            self.label_widget.show_bold = False
            self.label_widget.color = 'CURSOR'
        self.label_widget.update()
        self.entry_widget.update()
    def display(self):
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_edited_RP_del_inter_file"))

class run_item(npyscreen.FixedText):
    def update(self, clear=True,):
        super(run_item, self).update(clear=clear)
        self.show_bold = True
        self.color = 'CURSOR'
        
    def set_up_handlers(self):
        super(run_item, self).set_up_handlers()
        self.handlers.update({
                           curses.ascii.NL: self.run_shell
                           })

    def run_shell(self, _input):
        self.parent.parentApp.subprocess_handling_count = 1
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_edited_RP_popup"))
    def display(self):
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_edited_RP_run_item"))

def true_false_fields_config(read_config_str, negated_bool):
    val_true_false = "unset"
    try:
        if str(bool(strtobool(read_config_str))):
            if negated_bool:
                val_true_false = str(not bool(strtobool(read_config_str)))
            else:
                val_true_false = str(bool(strtobool(read_config_str)))
    except ValueError:
        pass
    if val_true_false == "True":
        val_true_false = "Enabled"
    elif val_true_false == "False":
        val_true_false = "Disabled"
    return val_true_false

class Run_popup(npyscreen.Popup):
    DEFAULT_LINES = 46
    DEFAULT_COLUMNS = 150

    #on OK
    def afterEditing(self):
        self.RunBox.values = []
        self.del_inter_file_select.editable= True
        self.run_item.editable= True
        self.parentApp.RP == "Unset"
        self.parentApp.subprocess_handling_count = 0
        self.parentApp.setNextForm("Run_pipeline")
        self.parentApp.RP_on_run_popup = 0
        self.del_inter_file_select.hidden = True
        self.del_inter_file_select.editable = False
        self.RunBox.editable = False

    def create(self):
        self.add_event_hander("event_value_edited_RP_popup", self.event_value_edited_RP_popup)
        self.add_event_hander("event_value_edited_RP_del_inter_file", self.event_value_edited_RP_del_inter_file)
        self.add_event_hander("event_value_edited_RP_popup", self.event_value_edited_RP_popup)
        self.add_event_hander("event_value_edited_RP_run_item", self.event_value_edited_RP_run_item)

        y, x = self.useable_space()

        self.add(npyscreen.FixedText, value= "", editable=False)

        self.del_inter_file_select = self.add(del_inter_file_select, max_height=4, name = "Delete intermediate file", scroll_exit=True, values = ["Yes","No"],editable = False, hidden=True)
        
        self.RunBox = self.add(RunBox, max_height=self.parentApp.numLinesPager,scroll_exit = True, select_exit=True,editable = False)

        self.run_item = self.add(run_item, value="RUN...")

        new_handlers = {
            #Set ctrl+Q to exit
            "^Q": self.exit_func
        }
        self.add_handlers(new_handlers)
        
        self.display()


    def event_value_edited_RP_del_inter_file(self, event):
        try:
            if self.del_inter_file_select.value[0] == 0:
                replace_config("Bismark", "del_inter_file", "true")
            elif self.del_inter_file_select.value[0] == 1:
                replace_config("Bismark", "del_inter_file", "false")
        except (IndexError, TypeError) as e:
            config_del_inter_file_Value = read_config("Bismark", "del_inter_file")
            if config_del_inter_file_Value == "true":
                self.del_inter_file_select.value = 0
            if config_del_inter_file_Value == "false":
                self.del_inter_file_select.value = 1

        config_del_inter_file_Value = read_config("Bismark", "del_inter_file")
        if config_del_inter_file_Value == "true":
            self.del_inter_file_select.value = 0
        if config_del_inter_file_Value == "false":
            self.del_inter_file_select.value = 1


        self.RunBox.name = self.parentApp.RP

        if self.parentApp.RP == "Run Bismark Meth. Extractor":
            self.del_inter_file_select.hidden = False
            self.del_inter_file_select.editable = True
        else:
            self.del_inter_file_select.hidden = True
            self.run_item.edit()

        self.display()


    def initiate_run(self):
        self.RunBox.editable = True
        self.RunBox.display()
        self.display()
        self.run_item.editing = False
        self.run_item.how_exited = -1
        self.RunBox.editing = True
        self.RunBox.display()
        self.display()

    def event_value_edited_RP_run_item(self, event):
        try:
            if self.del_inter_file_select.value[0] == 0:
                replace_config("Bismark", "del_inter_file", "true")
            elif self.del_inter_file_select.value[0] == 1:
                replace_config("Bismark", "del_inter_file", "false")
        except (IndexError, TypeError) as e:
            config_del_inter_file_Value = read_config("Bismark", "del_inter_file")
            if config_del_inter_file_Value == "true":
                self.del_inter_file_select.value = 0
            if config_del_inter_file_Value == "false":
                self.del_inter_file_select.value = 1

        config_del_inter_file_Value = read_config("Bismark", "del_inter_file")
        if config_del_inter_file_Value == "true":
            self.del_inter_file_select.value = 0
        if config_del_inter_file_Value == "false":
            self.del_inter_file_select.value = 1


        self.RunBox.name = self.parentApp.RP

        if self.parentApp.RP == "Run Bismark Meth. Extractor" and self.parentApp.RP_on_run_popup == 0:
            self.parentApp.RP_on_run_popup = 1
            self.del_inter_file_select.hidden = False
            self.del_inter_file_select.editable = True
            self.run_item.editing = False
            self.run_item.how_exited = -1

        self.display()



    def event_value_edited_RP_popup(self, event):


        if self.parentApp.subprocess_handling_count == 0 or self.parentApp.subprocess_handling_count == 3:
            self.display()


        #Trimommatic
        if self.parentApp.RP == "Run Trimommatic":
            #subprocess has not begun
            if self.parentApp.subprocess_handling_count == 1:
                self.initiate_run()

                success = None

                pairs_mode = read_config("GENERAL", "pairs_mode")
                
                # creating list of file
                list_dataset = find_file_pattern(read_config("GENERAL", "raw_dataset"), "*.gz")
                # writing all list to the file
                res_loc=read_config("GENERAL", "result_pipeline")
                if checkDirectoryExists(res_loc+"/trimmomatic-files/"):
                    with open(res_loc+"/trimmomatic-files/"+'list-files.lst', 'wb') as f:
                        for item in list_dataset:
                            f.write('%s\n' % item)

                    pairs_mode = read_config("GENERAL", "pairs_mode")
                    ToNULL = open(os.devnull, 'w')
                    
                    if pairs_mode == 'true':
                        subprocess.Popen(["nohup", './src/bash/trimmomatic_pair.sh', " > /dev/null 2>&1"], stdout=ToNULL, stderr=subprocess.STDOUT)
                        replace_config("STATUS", "st_trim", "2")
                    else:
                        subprocess.Popen(["nohup", './src/bash/trimmomatic.sh', " > /dev/null 2>&1"], stdout=ToNULL, stderr=subprocess.STDOUT)
                        replace_config("STATUS", "st_trim", "2")
                    success = True
                else:
                    success = False

                time.sleep(1)
                if success:
                    self.RunBox.values = formatted_run_box_RP(read_config("GENERAL", "result_pipeline")+"/logs/trimmomatic.log")
                    self.RunBox.display()

                    self.del_inter_file_select.editable= False
                    self.run_item.editable= False

                else:
                    self.RunBox.values = ["Something went wrong with running Trimommatic."]
                    self.RunBox.display()
                    self.display
                    self.parentApp.subprocess_handling_count = 3
                    #self.OK_Button_RP_run_popup.edit()


                self.parentApp.subprocess_handling_count = 2

            elif self.parentApp.subprocess_handling_count == 2:
                content = formatted_run_box_RP(read_config("GENERAL", "result_pipeline")+"/logs/trimmomatic.log")
                finished_process = []
                if int(read_config("STATUS", "st_trim")) == 3:
                    finished_process = ["finished trimmomatic"]
                    self.RunBox.values = content + finished_process
                    self.parentApp.subprocess_handling_count = 3
                    self.RunBox.edit()
                    self.RunBox.display()
                    self.display()
                self.RunBox.values = content + finished_process
                self.RunBox.display()


        #QC-Fastq
        if self.parentApp.RP == "Run QC-Fastq-report":

            #subprocess has not begun
            if self.parentApp.subprocess_handling_count == 1:
                self.initiate_run()

                success = None

                ToNULL = open(os.devnull, 'w')
                try:
                    subprocess.Popen(["nohup", './src/bash/qc-fastq-report.sh', " > /dev/null 2>&1 "], stdout=ToNULL, stderr=subprocess.STDOUT)
                    replace_config("STATUS", "st_fastq", "2")
                    success = True

                    
                except Exception as e:
                    replace_config("STATUS", "st_fastq", "1")
                    success = False

                time.sleep(1)
                if success:
                    self.RunBox.values = formatted_run_box_RP(read_config("GENERAL", "result_pipeline")+"/logs/qc-fastq.log")
                    self.RunBox.display()

                    self.del_inter_file_select.editable= False
                    self.run_item.editable= False

                else:
                    self.RunBox.values = ["Something went wrong with running QC-Fastq-report."]
                    self.RunBox.display()
                    self.display
                    self.parentApp.subprocess_handling_count = 3
                    #self.OK_Button_RP_run_popup.edit()


                self.parentApp.subprocess_handling_count = 2

            elif self.parentApp.subprocess_handling_count == 2:
                content = formatted_run_box_RP(read_config("GENERAL", "result_pipeline")+"/logs/qc-fastq.log")
                finished_process = []
                if int(read_config("STATUS", "st_fastq")) == 3:
                    finished_process = ["finished qcfastqreport"]
                    self.RunBox.values = content + finished_process
                    self.parentApp.subprocess_handling_count = 3
                    self.RunBox.edit()
                    self.RunBox.display()
                    self.display()
                self.RunBox.values = content + finished_process
                self.RunBox.display()


        #Bismark Mapper
        if self.parentApp.RP == "Run Bismark Mapper":
            #subprocess has not begun
            if self.parentApp.subprocess_handling_count == 1:
                self.initiate_run()
                success = None
 
                # running preparing files
                try:
                    ToNULL = open(os.devnull, 'w')
                    subprocess.Popen(["nohup", './src/bash/path-export.sh', " > /dev/null 2>&1"], stdout=ToNULL, stderr=subprocess.STDOUT)
                    pairs_mode = read_config("GENERAL", "pairs_mode")

                    
                    if pairs_mode == 'true' and read_config("GENERAL", "parallel_mode") == "true":
                        subprocess.Popen(["nohup", './src/bash/bismark-mapper-pair-parallel.sh', " > /dev/null 2>&1"], stdout=ToNULL, stderr=subprocess.STDOUT)
                        replace_config("STATUS", "st_bismark", "2")
                    elif pairs_mode == 'true' and read_config("GENERAL", "parallel_mode") == "false":
                        subprocess.Popen(["nohup", './src/bash/bismark-mapper-pair.sh', " > /dev/null 2>&1"], stdout=ToNULL, stderr=subprocess.STDOUT)
                        replace_config("STATUS", "st_bismark", "2")
                    else:
                        subprocess.Popen(["nohup", './src/bash/bismark-mapper.sh', " > /dev/null 2>&1"], stdout=ToNULL, stderr=subprocess.STDOUT)
                        replace_config("STATUS", "st_bismark", "2")
                    success = True
                except Exception as e:
                    # set 1 to resuming
                    replace_config("STATUS", "st_bismark", "1")
                    success = False

                time.sleep(1)
                if success:
                    self.RunBox.values = formatted_run_box_RP(read_config("GENERAL", "result_pipeline")+"/logs/bismark-mapper.log")
                    self.RunBox.display()

                    self.del_inter_file_select.editable= False
                    self.run_item.editable= False

                else:
                    self.RunBox.values = ["Something went wrong with running Bismark Mapper."]
                    self.RunBox.display()
                    self.display
                    self.parentApp.subprocess_handling_count = 3
                    #self.OK_Button_RP_run_popup.edit()


                self.parentApp.subprocess_handling_count = 2

            elif self.parentApp.subprocess_handling_count == 2:
                content = formatted_run_box_RP(read_config("GENERAL", "result_pipeline")+"/logs/bismark-mapper.log")
                finished_process = []
                if int(read_config("STATUS", "st_bismark")) == 3:
                    finished_process = ["finished Bismark Mapper"]
                    self.RunBox.values = content + finished_process
                    self.parentApp.subprocess_handling_count = 3
                    self.RunBox.edit()
                    self.RunBox.display()
                    self.display()
                self.RunBox.values = content + finished_process
                self.RunBox.display()


        #QC-Bam report
        if self.parentApp.RP == "Run QC-Bam report":
            if self.parentApp.subprocess_handling_count == 1:
                self.initiate_run()
                success = None
 
                try:
                    ToNULL = open(os.devnull, 'w')
                    subprocess.Popen(["nohup", './src/bash/qc-bam-report.sh', " > /dev/null 2>&1"], stdout=ToNULL, stderr=subprocess.STDOUT)
                    replace_config("STATUS", "st_fastqbam", "2")
                    success =  True
                except Exception as e:
                    logging.error(traceback.format_exc())
                    # set 1 to resuming
                    replace_config("STATUS", "st_fastqbam", "1")
                    success = False

                time.sleep(1)
                if success:
                    self.RunBox.values = formatted_run_box_RP(read_config("GENERAL", "result_pipeline")+"/logs/qc-bam.log")
                    self.RunBox.display()

                    self.del_inter_file_select.editable= False
                    self.run_item.editable= False

                else:
                    self.RunBox.values = ["Something went wrong with running QC-Bam report."]
                    self.RunBox.display()
                    self.display
                    self.parentApp.subprocess_handling_count = 3


                self.parentApp.subprocess_handling_count = 2

            elif self.parentApp.subprocess_handling_count == 2:
                content = formatted_run_box_RP(read_config("GENERAL", "result_pipeline")+"/logs/qc-bam.log")
                finished_process = []
                if int(read_config("STATUS", "st_fastqbam")) == 3:
                    finished_process = ["finished QC-Bam report"]
                    self.RunBox.values = content + finished_process
                    self.parentApp.subprocess_handling_count = 3
                    self.RunBox.edit()
                    self.RunBox.display()
                    self.display()
                self.RunBox.values = content + finished_process
                self.RunBox.display()


        #Bismark-deduplicate
        if self.parentApp.RP == "Run Bismark-deduplicate":

            if self.parentApp.subprocess_handling_count == 1:
                self.initiate_run()
                success = None
 
                try:
                    ToNULL = open(os.devnull, 'w')
                    subprocess.Popen(["nohup", './src/bash/path-export.sh', " > /dev/null 2>&1"], stdout=ToNULL, stderr=subprocess.STDOUT)
        
                    # if pair then set to -p
                    if read_config("GENERAL", "pairs_mode") == 'true':
                        replace_config("Bismark", "deduplicate", "-p")
                    else:
                        replace_config("Bismark", "deduplicate", "-s")

                    
                    subprocess.Popen(["nohup", './src/bash/bismark-deduplicate.sh', " > /dev/null 2>&1"], stdout=ToNULL, stderr=subprocess.STDOUT)
                    replace_config("STATUS", "st_bisdedup", "2")
                    success = True
                except Exception as e:
                    logging.error(traceback.format_exc())
                    # set 1 to resuming
                    replace_config("STATUS", "st_bisdedup", "1")
                    success = False

                time.sleep(1)
                if success:
                    self.RunBox.values = formatted_run_box_RP(read_config("GENERAL", "result_pipeline")+"/logs/bismark-deduplicate.log")
                    self.RunBox.display()

                    self.del_inter_file_select.editable= False
                    self.run_item.editable= False

                else:
                    self.RunBox.values = ["Something went wrong with running Bismark-deduplicate."]
                    self.RunBox.display()
                    self.display
                    self.parentApp.subprocess_handling_count = 3
                    #self.OK_Button_RP_run_popup.edit()


                self.parentApp.subprocess_handling_count = 2

            elif self.parentApp.subprocess_handling_count == 2:
                content = formatted_run_box_RP(read_config("GENERAL", "result_pipeline")+"/logs/bismark-deduplicate.log")
                finished_process = []
                if int(read_config("STATUS", "st_bisdedup")) == 3:
                    finished_process = ["finished Bismark-deduplicate"]
                    self.RunBox.values = content + finished_process
                    self.parentApp.subprocess_handling_count = 3
                    self.RunBox.edit()
                    self.RunBox.display()
                    self.display()
                    #self.OK_Button_RP_run_popup.edit()
                self.RunBox.values = content + finished_process
                self.RunBox.display()


        #Bismark Meth. Extractor
        if self.parentApp.RP == "Run Bismark Meth. Extractor":
            if self.parentApp.subprocess_handling_count == 1:
                self.initiate_run()
                success = None
 
                try:
                    ToNULL = open(os.devnull, 'w')
                    subprocess.Popen(["nohup", './src/bash/path-export.sh', " > /dev/null 2>&1"], stdout=ToNULL, stderr=subprocess.STDOUT)

                    if read_config("GENERAL", "pairs_mode") == 'true':
                        replace_config("Bismark", "methextractor", "-p")
                    else:
                        replace_config("Bismark", "methextractor", "-s")

                    
                    subprocess.Popen(["nohup", './src/bash/bismark-meth-extractor.sh', " > /dev/null 2>&1"], stdout=ToNULL, stderr=subprocess.STDOUT)

                    
                    subprocess.Popen(["nohup", './src/bash/cx-generator.sh', " > /dev/null 2>&1"], stdout=ToNULL, stderr=subprocess.STDOUT)
                    replace_config("STATUS", "st_bismeth", "2")
                    replace_config("STATUS", "st_cx", "2")

                    success = True

                except Exception as e:
                    logging.error(traceback.format_exc())
                    # set 1 to resuming
                    replace_config("STATUS", "st_bismeth", "1")
                    success = False

                time.sleep(1)
                if success:
                    self.RunBox.values = formatted_run_box_RP(read_config("GENERAL", "result_pipeline")+"/logs/bismark-meth-extract.log")
                    self.RunBox.display()

                    self.del_inter_file_select.editable= False
                    self.run_item.editable= False

                else:
                    self.RunBox.values = ["Something went wrong with running Bismark methextractor."]
                    self.RunBox.display()
                    self.display
                    self.parentApp.subprocess_handling_count = 3


                self.parentApp.subprocess_handling_count = 2

            elif self.parentApp.subprocess_handling_count == 2:
                content = formatted_run_box_RP(read_config("GENERAL", "result_pipeline")+"/logs/bismark-meth-extract.log")
                finished_process = []
                if int(read_config("STATUS", "st_bismeth")) == 3:
                    finished_process = ["finished Bismark-methextractor"]
                    self.RunBox.values = content + finished_process
                    self.parentApp.subprocess_handling_count = 3
                    self.RunBox.edit()
                    self.RunBox.display()
                    self.display()
                self.RunBox.values = content + finished_process
                self.RunBox.display()


        #CX reports
        if self.parentApp.RP == "Generate CX reports":
            if self.parentApp.subprocess_handling_count == 1:
                self.initiate_run()
                success = None
 
                # running preparing files
                try:
                    replace_config("GENERAL", "parallel_mode", "false")

                    ToNULL = open(os.devnull, 'w')

                    subprocess.Popen(["nohup", './src/bash/cx-generator.sh', " > /dev/null 2>&1"], stdout=ToNULL, stderr=subprocess.STDOUT)
                    replace_config("STATUS", "st_cx", "2")
                    success = True
                except Exception as e:
                    logging.error(traceback.format_exc())
                    # set 1 to resuming
                    replace_config("STATUS", "st_cx", "1")
                    success = False

                time.sleep(1)
                if success:
                    self.RunBox.values = formatted_run_box_RP(read_config("GENERAL", "result_pipeline")+"/logs/cx-report.log")
                    self.RunBox.display()

                    self.del_inter_file_select.editable= False
                    self.run_item.editable= False
                else:
                    self.RunBox.values = ["Something went wrong with running CX reports."]
                    self.RunBox.display()
                    self.display
                    self.parentApp.subprocess_handling_count = 3


                self.parentApp.subprocess_handling_count = 2

            elif self.parentApp.subprocess_handling_count == 2:
                content = formatted_run_box_RP(read_config("GENERAL", "result_pipeline")+"/logs/cx-report.log")
                finished_process = []
                if int(read_config("STATUS", "st_cx")) == 3:
                    finished_process = ["finished CX reports"]
                    self.RunBox.values = content + finished_process
                    self.parentApp.subprocess_handling_count = 3
                    self.RunBox.edit()
                    self.RunBox.display()
                    self.display()
                    #self.OK_Button_RP_run_popup.edit()
                self.RunBox.values = content + finished_process
                self.RunBox.display()


        #Methimpute
        if self.parentApp.RP == "Run Methimpute":
            if self.parentApp.subprocess_handling_count == 1:
                self.initiate_run()
                success = None
 
                try:
                    ToNULL = open(os.devnull, 'w')
                    replace_config("GENERAL", "parallel_mode", "false")
                    subprocess.Popen(["nohup", "./src/bash/gen-rdata.sh", " > /dev/null 2>&1"], stdout=ToNULL, stderr=subprocess.STDOUT) # yadi line
                    subprocess.Popen(["nohup", "./src/bash/methimpute.sh", " > /dev/null 2>&1"], stdout=ToNULL, stderr=subprocess.STDOUT) # yadi line
                    replace_config("STATUS", "st_methimpute", "2")

                    success = True
                except Exception as e:
                    logging.error(traceback.format_exc())
                    # set 1 to resuming
                    replace_config("STATUS", "st_methimpute", "1")
                    success = False

                time.sleep(1)
                if success:
                    self.RunBox.values = formatted_run_box_RP(read_config("GENERAL", "result_pipeline")+"/logs/methimpute.log")
                    self.RunBox.display()

                    self.del_inter_file_select.editable= False
                    self.run_item.editable= False

                else:
                    self.RunBox.values = ["Something went wrong with running Methimpute."]
                    self.RunBox.display()
                    self.display
                    self.parentApp.subprocess_handling_count = 3
                    #self.OK_Button_RP_run_popup.edit()


                self.parentApp.subprocess_handling_count = 2

            elif self.parentApp.subprocess_handling_count == 2:
                content = formatted_run_box_RP(read_config("GENERAL", "result_pipeline")+"/logs/methimpute.log")
                finished_process = []
                if int(read_config("STATUS", "st_methimpute")) == 3:
                    finished_process = ["finished Methimpute"]
                    self.RunBox.values = content + finished_process
                    self.parentApp.subprocess_handling_count = 3
                    self.RunBox.edit()
                    self.RunBox.display()
                    self.display()
                self.RunBox.values = content + finished_process
                self.RunBox.display()


    def on_cancel(self, _input):
        self.parentApp.setNextForm("Run_pipeline")

    def on_ok(self):
        self.parentApp.setNextForm("Run_pipeline")

    def exit_func(self, _input):
        exit(0)


def check_empty_dir(path, pattern):
    try:
        files = list(find_file_pattern(read_config("GENERAL", "result_pipeline")+"/"+path, pattern))
        if files:
            for item in find_file_pattern(read_config("GENERAL", "result_pipeline")+"/"+path, pattern):
                files.append(item)
        else:
            files = []

        return files

    except Exception as e:
        logging.error(traceback.format_exc())
        message(2, "something is going wrong... please run again. ")


def Trimmomatic_info():
    s = "If you need to change the following Trimmomatic settings then please go back to configuration. \n\n" \
    "Configured Java location: " + read_config("Trimmomatic", "java_path") + "\n" \
    "Trimmomatic path: " + read_config("Trimmomatic", "trim_path") + "\n" \
    "Trimmomatic Adapter: " + read_config("Trimmomatic", "name_adap") + "\n" \
    "Trimmomatic Running mode: " + read_config("Trimmomatic", "end_mode") + "\n" \
    "Trimmomatic ILLUMINACLIP: " + read_config("Trimmomatic", "ill_clip") + "\n" \
    "Trimmomatic LEADING: " + read_config("Trimmomatic", "LEADING") + "\n" \
    "Trimmomatic TRAILING: " + read_config("Trimmomatic", "TRAILING") + "\n" \
    "Trimmomatic SLIDINGWINDOW: " + read_config("Trimmomatic", "SLIDINGWINDOW") + "\n" \
    "Trimmomatic MINLEN: " + read_config("Trimmomatic", "MINLEN") + "\n" \
    "Trimmomatic Threading: " + read_config("Trimmomatic", "n_th") + "\n" \
    "Parallel mode is: " + true_false_fields_config(read_config("GENERAL", "parallel_mode"), False) + "\n\n" \

    status = int(read_config("STATUS", "st_trim"))
    pairs_mode = read_config("GENERAL", "pairs_mode")

    if status == 1:
        s += "It seems last time got problem during running..."
    elif status == 2:
        if len(check_empty_dir("trimmomatic-files", "*.gz")) > 0:
            s += "\nIt seems you have results for Trimmomatic part."
            s += "You can re-run this part, but we recommend move the files to another folder and run again. \n"
            s += "WARNING: The directory is not empty, re-running this part might end up with loss of the existing data!"
        pass

    if pairs_mode == "true" and read_config("Trimmomatic", "end_mode") == "SE":
        s += "WARNING: You're running Trimmomatic in 'Single End' mode, but you have pair file!"

    res_loc=read_config("GENERAL", "result_pipeline")
    if not checkDirectoryExists(res_loc+"/trimmomatic-files/"):
        s += "\nWARNING: Directory does not exist - please configure it correctly."

    return s

def QC_FastQ_report_info():
    s = "If you need to change please back to the configuration part. \n\n" \
    "- Fastq Path: " + read_config("GENERAL", "fastq_path") + " \n" \
    "- Parallel mode is: " + true_false_fields_config(read_config("GENERAL", "parallel_mode"), False) + "  \n\n" \
    "You can access to the quality control reports under menu, 'Reports' part."

    status = int(read_config("STATUS", "st_fastq"))
    if status == 1:
        s += "\n It seems last time got problem during running..."

    if status == 2:
        if len(check_empty_dir("qc-fastq-reports", "*.html")) > 0:
            s += "\nIt seems you have results for QCFastq part."
            s += "You can re-run this part, but we recommend move the files to another folder and run again. \n"
            s += "WARNING: The directory is not empty, re-running this part might loosing the existing data!"
    return s

def Bismark_mapper_info():
    s = "If you need to change please back to the configuration part. \n\n" \
    "- Bismark location: " + read_config("Bismark", "bismark_path") + "\n" \
    "   -- Nucleotide: " + true_false_fields_config(read_config("Bismark", "nucleotide"), False) + "\n" \
    "   -- Buffer size: " +  read_config("Bismark", "buf_size") + "\n" \
    "   -- Number of Parallel: " + read_config("Bismark", "bis_parallel") + " \n" \
    "- Reference Genome is: " + read_config("GENERAL", "genome_ref") + "/" + read_config("GENERAL", "genome_name") + "\n" \
    "- Parallel mode: " + true_false_fields_config(read_config("GENERAL", "parallel_mode"), False)  + "\n" \
    "- Bismark run pair: " + true_false_fields_config(read_config("Bismark", "run_pair_bismark"), False) +"\n" \

    status = int(read_config("STATUS", "st_bismark"))

    if status == 1:
        s += ("\nIt seems last time got problem during running...")
    elif status == 2:
        if len(check_empty_dir("bismark-mappers", "*.bam")) > 0:
            s += "\n It seems you have results for Trimmomatic part."
            s += "You can re-run this part, but we recommend move the files to another folder and run again. \n"
            s += ("WARNING: The directory is not empty, re-running this part might loosing the existing data!")

    return s

def QC_BAM_report_info():
    s = "If you need to change please back to the configuration part.\n\n" \
    "- Fastq Path: " + read_config("GENERAL", "fastq_path") + "\n" \
    "- Parallel mode: " +  true_false_fields_config(read_config("GENERAL", "parallel_mode"), False) + " \n\n" \
    "You can access to the quality control reports under menu, 'Reports' part. \n "

    status = int(read_config("STATUS", "st_fastqbam"))

    if status == 1:
        s += "\nIt seems last time got problem during running..."

    if status == 2:
        if len(check_empty_dir("qc-bam-reports", "*.html")) > 0:
            s += "\nIt seems you have results for quality control for Bismark-aligned bam files."
            s += "You can re-run this part, but we recommend move the files to another folder and run again. \n"
            s += "WARNING: The directory is not empty, re-running this part might loosing the existing data!"

    return s

def Bismark_deduplication_info():
    s = "If you need to change please back to the configuration part. \n\n" \
    "- Bismark location: " + read_config("Bismark", "bismark_path") + "  \n" \
    "- Parallel mode: " + true_false_fields_config(read_config("GENERAL", "parallel_mode"), False) + " \n " \
    "     -- Number of Parallel Jobs: " + read_config("GENERAL", "npar") + "\n" 

    status = int(read_config("STATUS", "st_bisdedup"))

    if status == 1:
        s += "\nIt seems last time got problem during running..."

    if status == 2:
        if len(check_empty_dir("bismark-deduplicate", "*.bam")) > 0:
            s +=  "\nIt seems you have results for quality control for Bismark-aligned bam files."
            s += "You can re-run this part, but we recommend move the files to another folder and run again. \n"
            s += "WARNING: The directory is not empty,re-running this part might loosing the existing data!"

    return s


def Bismark_meth_extractor_info():
    s = "If you need to change please back to the configuration part. \n\n" \
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

def Generate_CX_reports_info():
    s = "CpG (CX) context report. \n\n"
    s += "Note: by default we're generating CX-reports, so you can skip the 'Generate CX reports' from the run Menu. \n"
    status = int(read_config("STATUS", "st_cx"))

    if status == 1:
        s +=  "\nIt seems last time got problem during running..."

    if status == 2:
        if len(check_empty_dir("cx-reports", "*.txt")) > 0:
            s +=  "\nIt seems you generated cx reports before."
            s +=  "You can re-run this part, but we recommend move the files to another folder and run again. \n"
            s +=  "WARNING: The directory is not empty,re-running this part might loosing the existing data!"
    return s

def Methimpute_info():
    s = "Run Methimpute. \n\n"

    # cheking Rdata in folder
    if len(check_empty_dir("rdata", "*.RData")) > 0:
        s += "found RData files."
    else:
        s += "There are no '.RData' files inside the r-data folder, please copy the files."

    status = int(read_config("STATUS", "st_methimpute"))

    if status == 1:
        s += "\nIt seems last time got problem during running..."

    if status == 2:
        if len(check_empty_dir("methimpute-out", "*.txt")) > 0:
            s +=  "\nIt seems you have results for Methimpute."
            s +=  "You can re-run this part, but we recommend move the files to another folder and run again. \n"
            s += "WARNING: The directory is not empty, re-running this part may lose existing data!"

    return s


class OK_Button_run_pipeline(npyscreen.ButtonPress):
    def display(self):
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_edited_ok_run_pipeline"))
    def whenPressed(self):
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_edited_ok_run_pipeline_pressed"))

class Run_pipeline(npyscreen.FormBaseNew):

    def create(self):

        status = int(read_config("STATUS", "st_prep"))
        if status:
            # list all *.gz files inside the directory and sub folders
            subprocess.call(['./src/bash/preparing.sh'])
            replace_config("STATUS", "st_prep", "1")
        else:
            pass

        y, x = self.useable_space()


        self.add_event_hander("event_value_editedP0", self.event_value_editedP0)
        self.add_event_hander("event_value_editedP1", self.event_value_editedP1)
        self.add_event_hander("event_value_editedP2", self.event_value_editedP2)
        self.add_event_hander("event_value_editedP3", self.event_value_editedP3)
        self.add_event_hander("event_value_editedP4", self.event_value_editedP4)
        self.add_event_hander("event_value_editedP5", self.event_value_editedP5)
        self.add_event_hander("event_value_editedP6", self.event_value_editedP6)
        self.add_event_hander("event_value_editedP7", self.event_value_editedP7)
        self.add_event_hander("event_value_editedP8", self.event_value_editedP8)
        self.add_event_hander("event_value_edited_ok_run_pipeline", self.event_value_edited_ok_run_pipeline)
        self.add_event_hander("event_value_edited_ok_run_pipeline_pressed", self.event_value_edited_ok_run_pipeline_pressed)
        

        self.FixedText0_RP = self.add(FixedText0_RP, value= "", editable= True, rely=1)
        self.add(FixedText1_RP, value = "1. Run Trimommatic")
        self.add(FixedText2_RP, value = "2. Run QC-Fastq-report")
        self.add(FixedText3_RP, value = "3. Run Bismark Mapper")
        self.add(FixedText4_RP, value = "4. Run QC-Bam report")
        self.add(FixedText5_RP, value = "5. Run Bismark-deduplicate")
        self.add(FixedText6_RP, value = "6. Run Bismark Meth. Extractor")
        self.add(FixedText7_RP, value = "7. Generate CX reports")
        self.add(FixedText8_RP, value = "8. Run Methimpute")

        new_handlers = {
            #Set ctrl+Q to exit
            "^Q": self.exit_func,

            #Set ctrl+B to go back to the main form
            "^B": self.back_to_main_form
        }
        self.add_handlers(new_handlers)

        self.InputBoxInfoRP = self.add(InputBoxInfoRP, name="Information", editable=False, max_height=y // 2, rely=16)

        self.OK_Button_run_pipeline = self.add(OK_Button_run_pipeline, name="OK", relx=-12, rely=-3)


    def event_value_editedP0(self, event):
        self.FixedText0_RP.editing = 0
        self.FixedText0_RP.how_exited = True

    def event_value_editedP1(self, event):
        self.InputBoxInfoRP.value = Trimmomatic_info()
        self.InputBoxInfoRP.display()
        self.display()
        self.FixedText0_RP.editable = False

    def event_value_editedP2(self, event):
        self.InputBoxInfoRP.value = QC_FastQ_report_info()
        self.InputBoxInfoRP.display()
        self.display()

    def event_value_editedP3(self, event):
        self.InputBoxInfoRP.value = Bismark_mapper_info()
        self.InputBoxInfoRP.display()
        self.display()

    def event_value_editedP4(self, event):
        self.InputBoxInfoRP.value = QC_BAM_report_info()
        self.InputBoxInfoRP.display()
        self.display()

    def event_value_editedP5(self, event):
        self.InputBoxInfoRP.value = Bismark_deduplication_info()
        self.InputBoxInfoRP.display()
        self.display()

    def event_value_editedP6(self, event):
        self.InputBoxInfoRP.value = Bismark_meth_extractor_info()
        self.InputBoxInfoRP.display()
        self.display()

    def event_value_editedP7(self, event):
        self.InputBoxInfoRP.value = Generate_CX_reports_info()
        self.InputBoxInfoRP.display()
        self.display()

    def event_value_editedP8(self, event):
        self.InputBoxInfoRP.value = Methimpute_info()
        self.InputBoxInfoRP.display()
        self.display()

    def event_value_edited_ok_run_pipeline(self, event):
        self.InputBoxInfoRP.value = "Proceed back to the main form."
        self.InputBoxInfoRP.display()
        self.display()

    def event_value_edited_ok_run_pipeline_pressed(self, event):
        self.parentApp.switchForm("MAIN")
        self.editw = 0

    def exit_func(self, _input):
        exit(0)

    def back_to_main_form(self, _input):
        self.parentApp.switchForm("MAIN")

