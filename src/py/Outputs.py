import npyscreen
import textwrap
import curses
import ConfigParser
import os,fnmatch,sys
import traceback
import logging
from os import listdir
from os.path import isfile, join
import time
import subprocess

class run_item_OP(npyscreen.FixedText):
    def update(self, clear=True,):
        super(run_item_OP, self).update(clear=clear)
        self.show_bold = True
        self.color = 'CURSOR'
        
    def set_up_handlers(self):
        super(run_item_OP, self).set_up_handlers()
        self.handlers.update({
                           curses.ascii.NL: self.run_shell_OP
                           })

    def run_shell_OP(self, _input):
        self.editing = False
        self.how_exited = 1
        self.parent.parentApp.subprocess_handling_count_OP = 1
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_edited_OP_popup"))


class Pager_custom(npyscreen.Pager):
    def h_scroll_line_down(self, input):
        self.start_display_at += 1
        #original if self.scroll_exit and self.start_display_at >= len(self.values)-self.start_display_at+1:
        if self.scroll_exit and self.start_display_at >= len(self.values) - self.parent.parentApp.numLinesPager+2:
            self.editing = False
            self.how_exited = 1

class OutputBox(npyscreen.BoxTitle):
    _contained_widget = Pager_custom
    def display(self):
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_edited_OP_popup"))



class parallel_mode_OP(npyscreen.TitleSelectOne):
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
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_edited_OP_parallel_mode"))




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


class FixedText1_outputs(npyscreen.FixedText):
    def update(self, clear=True,):
        super(FixedText1_outputs, self).update(clear=clear)
        self.show_bold = True
        self.color = 'CURSOR'
    def display(self):
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_editedO1"))
        new_handlers = {
            curses.ascii.NL: self.switchForm
        }
        self.add_handlers(new_handlers)

    def switchForm(self, _input):
        self.parent.parentApp.OP = "DMR"
        self.parent.parentApp.switchForm('Outputs_popup')

class FixedText2_outputs(npyscreen.FixedText):
    def update(self, clear=True,):
        super(FixedText2_outputs, self).update(clear=clear)
        self.show_bold = True
        self.color = 'CURSOR'
    def display(self):
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_editedO2"))
        new_handlers = {
            curses.ascii.NL: self.switchForm
        }
        self.add_handlers(new_handlers)

    def switchForm(self, _input):
        self.parent.parentApp.OP = "Methylkit"
        self.parent.parentApp.switchForm('Outputs_popup')

class FixedText3_outputs(npyscreen.FixedText):
    def update(self, clear=True,):
        super(FixedText3_outputs, self).update(clear=clear)
        self.show_bold = True
        self.color = 'CURSOR'
    def display(self):
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_editedO3"))
        new_handlers = {
            curses.ascii.NL: self.switchForm
        }
        self.add_handlers(new_handlers)

    def switchForm(self, _input):
        self.parent.parentApp.OP = "BedGraph"
        self.parent.parentApp.switchForm('Outputs_popup')

class FixedText4_outputs(npyscreen.FixedText):
    def update(self, clear=True,):
        super(FixedText4_outputs, self).update(clear=clear)
        self.show_bold = True
        self.color = 'CURSOR'
    def display(self):
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_editedO4"))
        new_handlers = {
            curses.ascii.NL: self.switchForm
        }
        self.add_handlers(new_handlers)

    def switchForm(self, _input):
        self.parent.parentApp.OP = "BigWig"
        self.parent.parentApp.switchForm('Outputs_popup')



class Outputs_popup(npyscreen.Popup):
    DEFAULT_LINES = 46
    DEFAULT_COLUMNS = 150

    #on OK
    def afterEditing(self):
        self.OutputBox.values = []
        #self.RunBox_test.value = ""
        self.parallel_mode_OP.editable= True
        self.run_item_OP.editable= True
        self.parentApp.OP == "Unset"
        self.parentApp.subprocess_handling_count_OP = 0
        self.parentApp.setNextForm("Outputs")

    def create(self):
        self.add_event_hander("event_value_edited_OP_popup", self.event_value_edited_OP_popup)
        self.add_event_hander("OK_Button_OP_outputs_popup_pressed", self.OK_Button_OP_outputs_popup_pressed)
        self.add_event_hander("event_value_edited_OP_parallel_mode", self.event_value_edited_OP_parallel_mode)

        y, x = self.useable_space()

        self.add(npyscreen.FixedText, value= "", editable=False)
        self.parallel_mode_OP = self.add(parallel_mode_OP, name="Parallel mode",
                values = ["Enabled","Disabled"], scroll_exit=True, max_height=4, rely=2)
        # self.qsub_select = self.add(qsub_select, name="qsub",
        #         values = ["True","False"], scroll_exit=True, max_height=4)

        #self.del_inter_file_select = self.add(del_inter_file_select, max_height=4, name = "del_inter_file", scroll_exit=True, values = ["True","False"])
        #self.intermediate_select = self.add(intermediate_select, max_height=4, name = "intermediate", scroll_exit=True, values = ["True","False"])
        self.run_item_OP = self.add(run_item_OP, value="RUN...")
        
        self.OutputBox = self.add(OutputBox, max_height= self.parentApp.numLinesPager, scroll_exit = True, select_exit=True)


        #self.OK_Button_OP_run_popup = self.add(OK_Button_OP_run_popup, name="OKp", relx=-12, rely=-3)
        new_handlers = {
            #Set ctrl+Q to exit
            "^Q": self.exit_func
        }
        self.add_handlers(new_handlers)
        
        self.display()

    def OK_Button_OP_outputs_popup_pressed(self, event):
        self.OutputBox.values = []
        self.parallel_mode_OP.editable= True
        self.run_item_OP.editable= True
        self.parentApp.OP == "Unset"
        self.parentApp.subprocess_handling_count_OP = 0
        self.parentApp.switchForm("Outputs")

    def event_value_edited_OP_parallel_mode(self, event):
        try:
            if self.parallel_mode_OP.value[0] == 0:
                replace_config("GENERAL", "parallel_mode", "true")
            elif self.parallel_mode_OP.value[0] == 1:
                replace_config("GENERAL", "parallel_mode", "false")
        except IndexError:
            configParallelValue = read_config("GENERAL", "parallel_mode")
            if configParallelValue == "true":
                self.parallel_mode_OP.value = 0
            if configParallelValue == "false":
                self.parallel_mode_OP.value = 1


        self.OutputBox.name = self.parentApp.OP


        self.display()




    def event_value_edited_OP_popup(self, event):

        if self.parentApp.subprocess_handling_count_OP == 0 or self.parentApp.subprocess_handling_count_OP == 3:
            self.display()

        #DMR
        if self.parentApp.OP == "DMR":
            #subprocess has not begun
            if self.parentApp.subprocess_handling_count_OP == 1:
                success = None

                ToNULL = open(os.devnull, 'w')
                try:
                    subprocess.Popen(["nohup", './src/bash/dmr-caller.sh', " > /dev/null 2>&1 "], stdout=ToNULL, stderr=subprocess.STDOUT)
                    replace_config("STATUS", "st_dmrcaller", "2")
                    success = True
                    
                except Exception as e:
                    #logging.error(traceback.format_exc())
                    # set 1 to resuming
                    replace_config("STATUS", "st_dmrcaller", "1")
                    success = False

                time.sleep(1)
                if success:

                    with open(read_config("GENERAL", "result_pipeline")+"/logs/dmr.log") as f:
                        content = f.readlines()
                    content = [x.strip() for x in content]
                    #runBox_output.extend(content)
                    self.OutputBox.values = content
                    self.OutputBox.display()

                    self.parallel_mode_OP.editable= False
                    self.run_item_OP.editable= False

                else:
                    self.OutputBox.values = ["Something went wrong with running DMR."]
                    self.OutputBox.display()
                    self.display
                    self.parentApp.subprocess_handling_count_OP = 3
                    #self.OK_Button_OP_run_popup.edit()


                self.parentApp.subprocess_handling_count_OP = 2

            elif self.parentApp.subprocess_handling_count_OP == 2:
                with open(read_config("GENERAL", "result_pipeline")+"/logs/dmr.log") as f:
                    content = f.readlines()
                content = [x.strip() for x in content]
                finished_process = []
                if int(read_config("STATUS", "st_dmrcaller")) == 3:
                    finished_process = ["finished DMR"]
                    self.OutputBox.values = content + finished_process
                    self.parentApp.subprocess_handling_count_OP = 3
                    self.OutputBox.edit()
                    self.OutputBox.display()
                    self.display()
                    #self.OK_Button_OP_run_popup.edit()
                self.OutputBox.values = content + finished_process
                self.OutputBox.display()


        #Methylkit
        if self.parentApp.OP == "Methylkit":

            #subprocess has not begun
            if self.parentApp.subprocess_handling_count_OP == 1:
                success = None

                ToNULL = open(os.devnull, 'w')
                try:
                    subprocess.Popen(["nohup", './src/bash/methylkit.sh', " > /dev/null 2>&1 "], stdout=ToNULL, stderr=subprocess.STDOUT)
                    replace_config("STATUS", "st_methykit", "2")
                    success = True
                    
                except Exception as e:
                    #logging.error(traceback.format_exc())
                    # set 1 to resuming
                    replace_config("STATUS", "st_methykit", "1")
                    success = False

                time.sleep(1)
                if success:
                    with open(read_config("GENERAL", "result_pipeline")+"/logs/methylkit.log") as f:
                        content = f.readlines()                               
                    content = [x.strip() for x in content]
                    #runBox_output.extend(content)
                    self.OutputBox.values = content
                    self.OutputBox.display()

                    self.parallel_mode_OP.editable= False
                    self.run_item_OP.editable= False

                else:
                    self.OutputBox.values = ["Something went wrong with running Methylkit."]
                    self.OutputBox.display()
                    self.display
                    self.parentApp.subprocess_handling_count_OP = 3
                    #self.OK_Button_OP_run_popup.edit()


                self.parentApp.subprocess_handling_count_OP = 2

            elif self.parentApp.subprocess_handling_count_OP == 2:
                with open(read_config("GENERAL", "result_pipeline")+"/logs/methylkit.log") as f:
                    content = f.readlines()             
                content = [x.strip() for x in content]
                finished_process = []
                if int(read_config("STATUS", "st_methykit")) == 3:
                    finished_process = ["finished Methylkit"]
                    self.OutputBox.values = content + finished_process
                    self.parentApp.subprocess_handling_count_OP = 3
                    self.OutputBox.edit()
                    self.OutputBox.display()
                    self.display()
                    #self.OK_Button_OP_run_popup.edit()
                self.OutputBox.values = content + finished_process
                self.OutputBox.display()


        #BedGraph
        if self.parentApp.OP == "BedGraph":

            #subprocess has not begun
            if self.parentApp.subprocess_handling_count_OP == 1:
                success = None

                ToNULL = open(os.devnull, 'w')
                try:
                    subprocess.Popen(["nohup", './src/bash/meth-bedgraph.sh', " > /dev/null 2>&1 "], stdout=ToNULL, stderr=subprocess.STDOUT)
                    replace_config("STATUS", "st_bedgraph", "2")
                    success = True

                    
                except Exception as e:
                    #logging.error(traceback.format_exc())
                    # set 1 to resuming
                    replace_config("STATUS", "st_bedgraph", "1")
                    success = False

                time.sleep(1)
                if success:

                    with open(read_config("GENERAL", "result_pipeline")+"/logs/meth-bedgraph.log") as f:
                        content = f.readlines()
                    content = [x.strip() for x in content]
                    #runBox_output.extend(content)
                    self.OutputBox.values = content
                    self.OutputBox.display()

                    self.parallel_mode_OP.editable= False
                    self.run_item_OP.editable= False

                else:
                    self.OutputBox.values = ["Something went wrong with running BedGraph."]
                    self.OutputBox.display()
                    self.display
                    self.parentApp.subprocess_handling_count_OP = 3
                    #self.OK_Button_OP_run_popup.edit()


                self.parentApp.subprocess_handling_count_OP = 2

            elif self.parentApp.subprocess_handling_count_OP == 2:
                with open(read_config("GENERAL", "result_pipeline")+"/logs/meth-bedgraph.log") as f:
                    content = f.readlines()
                content = [x.strip() for x in content]
                finished_process = []
                if int(read_config("STATUS", "st_bedgraph")) == 3:
                    finished_process = ["finished BedGraph"]
                    self.OutputBox.values = content + finished_process
                    self.parentApp.subprocess_handling_count_OP = 3
                    self.OutputBox.edit()
                    self.OutputBox.display()
                    self.display()
                    #self.OK_Button_OP_run_popup.edit()
                self.OutputBox.values = content + finished_process
                self.OutputBox.display()


        #BigWig
        if self.parentApp.OP == "BigWig":

            #subprocess has not begun
            if self.parentApp.subprocess_handling_count_OP == 1:
                success = None

                ToNULL = open(os.devnull, 'w')
                try:
                    subprocess.Popen(["nohup", './src/bash/bigwig-format.sh', " > /dev/null 2>&1 "], stdout=ToNULL, stderr=subprocess.STDOUT)
                    replace_config("STATUS", "st_bigwig", "2")
                    success = True

                    
                except Exception as e:
                    #logging.error(traceback.format_exc())
                    # set 1 to resuming
                    replace_config("STATUS", "st_bigwig", "1")
                    success = False

                time.sleep(1)
                if success:

                    with open(read_config("GENERAL", "result_pipeline")+"/logs/bigwig.log") as f:
                        content = f.readlines()
                    content = [x.strip() for x in content]
                    #runBox_output.extend(content)
                    self.OutputBox.values = content
                    self.OutputBox.display()

                    self.parallel_mode_OP.editable= False
                    self.run_item_OP.editable= False

                else:
                    self.OutputBox.values = ["Something went wrong with running BigWig."]
                    self.OutputBox.display()
                    self.display
                    self.parentApp.subprocess_handling_count_OP = 3
                    #self.OK_Button_OP_run_popup.edit()


                self.parentApp.subprocess_handling_count_OP = 2

            elif self.parentApp.subprocess_handling_count_OP == 2:
                with open(read_config("GENERAL", "result_pipeline")+"/logs/bigwig.log") as f:
                    content = f.readlines()
                content = [x.strip() for x in content]
                finished_process = []
                if int(read_config("STATUS", "st_bigwig")) == 3:
                    finished_process = ["finished BigWig"]
                    self.OutputBox.values = content + finished_process
                    self.parentApp.subprocess_handling_count_OP = 3
                    self.OutputBox.edit()
                    self.OutputBox.display()
                    self.display()
                    #self.OK_Button_OP_run_popup.edit()
                self.OutputBox.values = content + finished_process
                self.OutputBox.display()



    def on_cancel(self, _input):
        self.parentApp.setNextForm("Outputs")

    def on_ok(self):
        self.parentApp.setNextForm("Outputs")

    def exit_func(self, _input):
        exit(0)


class CustomMultiLineEdit(npyscreen.MultiLineEdit):
    def update(self, clear=True,):
        super(CustomMultiLineEdit, self).update(clear=clear)
        self.color = 'CAUTION'

class InputBoxInfoOutputs(npyscreen.BoxTitle):
    _contained_widget = CustomMultiLineEdit
    def update(self, clear=True,):
        super(InputBoxInfoOutputs, self).update(clear=clear)
        self.color = 'CURSOR'


def formatted_info_box_str(info_path):
    with open(info_path, 'r') as myfile:
        info = myfile.read()

    infoList = info.split('\n\n')

    infoList_new = []
    for a in infoList:
        infoList_new.append(textwrap.fill(a, 150))

    infoSTR = ""
    for elem in infoList_new:
        infoSTR += elem
        infoSTR +=  "\n\n"

    return infoSTR

class FixedText0_Outputs(npyscreen.FixedText):
    def update(self, clear=True,):
        super(FixedText0_Outputs, self).update(clear=clear)
        self.show_bold = True
        self.color = 'CURSOR'
    def display(self):
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_editedO0"))

class OK_Button_outputs(npyscreen.ButtonPress):
    def display(self):
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_edited_ok_outputs"))
    def whenPressed(self):
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_edited_ok_outputs_pressed"))

class Outputs(npyscreen.FormBaseNew):
    # def afterEditing(self):
    #     self.parentApp.setNextForm(None)

    # def create_control_buttons(self):
    #     self._add_button('ok_button', 
    #                     self.__class__.OKBUTTON_TYPE, 
    #                     self.__class__.OK_BUTTON_TEXT,
    #                     0 - self.__class__.OK_BUTTON_BR_OFFSET[0],
    #                     0 - self.__class__.OK_BUTTON_BR_OFFSET[1] - len(self.__class__.OK_BUTTON_TEXT),
    #                     None
    #                     )

    def create(self):
        self.add_event_hander("event_value_editedO0", self.event_value_editedO0)
        self.add_event_hander("event_value_editedO1", self.event_value_editedO1)
        self.add_event_hander("event_value_editedO2", self.event_value_editedO2)
        self.add_event_hander("event_value_editedO3", self.event_value_editedO3)
        self.add_event_hander("event_value_editedO4", self.event_value_editedO4)
        self.add_event_hander("event_value_edited_ok_outputs", self.event_value_edited_ok_outputs)
        self.add_event_hander("event_value_edited_ok_outputs_pressed", self.event_value_edited_ok_outputs_pressed)
        
        new_handlers = {
            # Set ctrl+Q to exit
            "^Q": self.exit_func,

            #Set ctrl+B to go back to the main form
            "^B": self.back_to_main_form
        }
        self.add_handlers(new_handlers)

        y, x = self.useable_space()

        self.FixedText0_Outputs = self.add(FixedText0_Outputs, value= "", editable= True, rely=1)
        self.add(FixedText1_outputs, value = "1. Convert to DMR Format", rely=2)
        self.add(FixedText2_outputs, value = "2. Convert to Methylkit Format")
        self.add(FixedText3_outputs, value = "3. Convert to bedGraph format (output)")
        self.add(FixedText4_outputs, value = "4. Convert bedGraph to BigWig format")

        self.InputBoxInfoOutputs = self.add(InputBoxInfoOutputs, name="Information", editable=False, max_height=y // 2, rely=16)

        self.OK_Button_outputs = self.add(OK_Button_outputs, name="OK", relx=-12, rely=-3)

    def event_value_editedO0(self, event):
        self.FixedText0_Outputs.editing = 0
        self.FixedText0_Outputs.how_exited = True

    def event_value_editedO1(self, event):
        infoSTR = formatted_info_box_str('information_box/DMR')
        self.InputBoxInfoOutputs.value = infoSTR
        self.InputBoxInfoOutputs.display()
        self.display()

    def event_value_editedO2(self, event):
        self.InputBoxInfoOutputs.value = "Convert to Methylkit Format"
        self.InputBoxInfoOutputs.display()
        self.display()

    def event_value_editedO3(self, event):
        self.InputBoxInfoOutputs.value = "Convert to bedGraph format (output)"
        self.InputBoxInfoOutputs.display()
        self.display()

    def event_value_editedO4(self, event):
        self.InputBoxInfoOutputs.value = "Convert bedGraph BigWig format"
        self.InputBoxInfoOutputs.display()
        self.display()

    def event_value_edited_ok_outputs(self, event):
        self.InputBoxInfoOutputs.value = "Proceed back to the main form."
        self.InputBoxInfoOutputs.display()
        self.display()

    def event_value_edited_ok_outputs_pressed(self, event):
        self.parentApp.switchForm("MAIN")
        self.editw = 0

    def exit_func(self, _input):
        exit(0)

    def back_to_main_form(self, _input):
        self.parentApp.switchForm("MAIN")