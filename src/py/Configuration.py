import npyscreen
import curses
import ConfigParser
import os,fnmatch,sys
from os import listdir
from os.path import isfile, join
import subprocess
from distutils.util import strtobool
import re
import collections
import textwrap

class CustomMultiLineEdit(npyscreen.MultiLineEdit):
    def update(self, clear=True,):
        super(CustomMultiLineEdit, self).update(clear=clear)
        self.color = 'CAUTION'

class InputBoxInfoConfig(npyscreen.BoxTitle):
    _contained_widget = CustomMultiLineEdit
    def update(self, clear=True,):
        super(InputBoxInfoConfig, self).update(clear=clear)
        self.color = 'CURSOR'

class TitleSelectOne_custom(npyscreen.TitleSelectOne):
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



class title_text_pattern(npyscreen.TitleText):
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


class TitleFilenameCombo_custom(npyscreen.TitleFilenameCombo):
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


class java_path_select(npyscreen.TitleText):
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


class bismark_buffer_size_select(npyscreen.FixedText):
    def update(self, clear=True,):
        super(bismark_buffer_size_select, self).update(clear=clear)
        self.color = 'CURSOR'

    def set_up_handlers(self):
        super(bismark_buffer_size_select, self).set_up_handlers()
        self.handlers.update({curses.KEY_LEFT:    self.h_cursor_left,
                           curses.KEY_RIGHT:   self.h_cursor_right,
                           ord('k'):    self.h_exit_up,
                           ord('j'):    self.h_exit_down,
                           curses.ascii.NL: self.switchForm
                           })

    def switchForm(self, _input):
        self.parent.parentApp.switchForm('Bismark_buffer_size_popup')

class bismark_buffer(npyscreen.TitleText):
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
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_edited_Bismark_buffer_size_popup"))

class Bismark_buffer_size_popup(npyscreen.ActionPopup):
    def create(self):

        self.add_event_hander("event_value_edited_Bismark_buffer_size_popup", self.event_value_edited_Bismark_buffer_size_popup)

        new_handlers = {
            #Set ctrl+Q to exit
            "^Q": self.exit_func
        }
        self.add_handlers(new_handlers)

        y, x = self.useable_space()
        self.add(npyscreen.FixedText, value= "", editable=False)
        self.bismark_buffer = self.add(bismark_buffer, name = "Trimmomatic leading parameter", value =read_config("Bismark", "buf_size"), rely = 2)
        self.InputBoxInfo_Bismark_buffer_size_popup = self.add(InputBoxInfoConfig, name="Information", editable=False, max_height=y // 20)  

    def on_ok(self):
        if self.bismark_buffer.value.isdigit():
            if int(self.bismark_buffer.value) < 81 and int(self.bismark_buffer.value) > 9:
                replace_config("Bismark", "buf_size", self.bismark_buffer.value)
        self.parentApp.switchForm("ConfigurationPopup_Bismark_parameters")

    def on_cancel(self):
        self.parentApp.switchForm("ConfigurationPopup_Bismark_parameters")

    def exit_func(self, _input):
        exit(0)

    def event_value_edited_Bismark_buffer_size_popup(self, event):
        self.InputBoxInfo_Bismark_buffer_size_popup.value = "Bismark buffer size parameter: "+ read_config("Bismark", "buf_size") + "\n"\
        "only digits 10 to 80 are accepted"
        self.InputBoxInfo_Bismark_buffer_size_popup.display()
        self.display()

class bismark_parallel_select(npyscreen.FixedText):
    def update(self, clear=True,):
        super(bismark_parallel_select, self).update(clear=clear)
        #self.show_bold = True
        self.color = 'CURSOR'
    def set_up_handlers(self):
        super(bismark_parallel_select, self).set_up_handlers()
        self.handlers.update({curses.KEY_LEFT:    self.h_cursor_left,
                           curses.KEY_RIGHT:   self.h_cursor_right,
                           ord('k'):    self.h_exit_up,
                           ord('j'):    self.h_exit_down,
                           curses.ascii.NL: self.switchForm
                           })

    def switchForm(self, _input):
        self.parent.parentApp.switchForm('Bismark_parallel_popup')

class Bismark_par(npyscreen.TitleText):
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
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_edited_Bismark_parallel_popup"))

class Bismark_parallel_popup(npyscreen.ActionPopup):
    def create(self):

        self.add_event_hander("event_value_edited_Bismark_parallel_popup", self.event_value_edited_Bismark_parallel_popup)

        new_handlers = {
            #Set ctrl+Q to exit
            "^Q": self.exit_func
        }
        self.add_handlers(new_handlers)

        y, x = self.useable_space()
        self.add(npyscreen.FixedText, value= "", editable=False)
        self.Bismark_par = self.add(Bismark_par, name = "Bismark multi-processes parameter", value = read_config("Bismark", "bis_parallel"), rely = 2)
        self.InputBoxInfo_Bismark_parallel_popup = self.add(InputBoxInfoConfig, name="Information", editable=False, max_height=y // 20)  

    def on_ok(self):
        if self.Bismark_par.value.isdigit():
            if int(self.Bismark_par.value) < 41 and int(self.Bismark_par.value) > 1:
                replace_config("Bismark", "bis_parallel", self.Bismark_par.value)
        self.parentApp.switchForm("ConfigurationPopup_Bismark_parameters")

    def on_cancel(self):
        self.parentApp.switchForm("ConfigurationPopup_Bismark_parameters")

    def exit_func(self, _input):
        exit(0)

    def event_value_edited_Bismark_parallel_popup(self, event):
        self.InputBoxInfo_Bismark_parallel_popup.value = "Bismark multi-processes parameter: "+ read_config("Bismark", "bis_parallel") + "\n"\
        "only digits 2 to 40 are accepted"
        self.InputBoxInfo_Bismark_parallel_popup.display()
        self.display()

class trim_trailing_select(npyscreen.FixedText):
    def update(self, clear=True,):
        super(trim_trailing_select, self).update(clear=clear)
        self.color = "CURSOR"
    def set_up_handlers(self):
        super(trim_trailing_select, self).set_up_handlers()
        self.handlers.update({curses.KEY_LEFT:    self.h_cursor_left,
                           curses.KEY_RIGHT:   self.h_cursor_right,
                           ord('k'):    self.h_exit_up,
                           ord('j'):    self.h_exit_down,
                           curses.ascii.NL: self.switchForm
                           })

    def switchForm(self, _input):
        self.parent.parentApp.switchForm('Trimmomatic_trailing_popup')

class Trimmomatic_trailing_popup(npyscreen.ActionPopup):
    def create(self):

        self.add_event_hander("event_value_edited_Trimmomatic_trailing_popup", self.event_value_edited_Trimmomatic_trailing_popup)

        new_handlers = {
            #Set ctrl+Q to exit
            "^Q": self.exit_func
        }
        self.add_handlers(new_handlers)

        y, x = self.useable_space()
        self.add(npyscreen.FixedText, value= "", editable=False)
        self.Trimmomatic_trailing = self.add(Trimmomatic_trailing, name = "Trimmomatic trailing parameter", value = read_config("Trimmomatic", "TRAILING"), rely = 2)
        self.InputBoxInfo_Trimmomatic_trailing_popup = self.add(InputBoxInfoConfig, name="Information", editable=False, max_height=y // 20)  

    def on_ok(self):
        if self.Trimmomatic_trailing.value.isdigit():
            if int(self.Trimmomatic_trailing.value) < 100:
                replace_config("Trimmomatic", "TRAILING", self.Trimmomatic_trailing.value)
        self.parentApp.switchForm("ConfigurationPopup_trimmomatic")

    def on_cancel(self):
        self.parentApp.switchForm("ConfigurationPopup_trimmomatic")

    def exit_func(self, _input):
        exit(0)

    def event_value_edited_Trimmomatic_trailing_popup(self, event):
        self.InputBoxInfo_Trimmomatic_trailing_popup.value = "Trailing_parameters: "+ read_config("Trimmomatic", "TRAILING") + "\n"\
        "only digits 0 to 99 are accepted"
        self.InputBoxInfo_Trimmomatic_trailing_popup.display()
        self.display()

class Trimmomatic_trailing(npyscreen.TitleText):
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
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_edited_Trimmomatic_trailing_popup"))

class trim_minlen_select(npyscreen.FixedText):
    def update(self, clear=True,):
        super(trim_minlen_select, self).update(clear=clear)
        self.color = "CURSOR"
    def set_up_handlers(self):
        super(trim_minlen_select, self).set_up_handlers()
        self.handlers.update({curses.KEY_LEFT:    self.h_cursor_left,
                           curses.KEY_RIGHT:   self.h_cursor_right,
                           ord('k'):    self.h_exit_up,
                           ord('j'):    self.h_exit_down,
                           curses.ascii.NL: self.switchForm
                           })

    def switchForm(self, _input):
        self.parent.parentApp.switchForm('Trimmomatic_minlen_popup')

class Trimmomatic_minlen_popup(npyscreen.ActionPopup):
    def create(self):

        self.add_event_hander("event_value_edited_Trimmomatic_minlen_popup", self.event_value_edited_Trimmomatic_minlen_popup)

        new_handlers = {
            #Set ctrl+Q to exit
            "^Q": self.exit_func
        }
        self.add_handlers(new_handlers)

        y, x = self.useable_space()
        self.add(npyscreen.FixedText, value= "", editable=False)
        self.Trimmomatic_minlen = self.add(Trimmomatic_minlen, name = "Trimmomatic minlen parameter", value = read_config("Trimmomatic", "MINLEN"), rely = 2)
        self.InputBoxInfo_Trimmomatic_minlen_popup = self.add(InputBoxInfoConfig, name="Information", editable=False, max_height=y // 20)  

    def on_ok(self):
        if self.Trimmomatic_minlen.value.isdigit():
            if int(self.Trimmomatic_minlen.value) < 100:
                replace_config("Trimmomatic", "MINLEN", self.Trimmomatic_minlen.value)
        self.parentApp.switchForm("ConfigurationPopup_trimmomatic")

    def on_cancel(self):
        self.parentApp.switchForm("ConfigurationPopup_trimmomatic")

    def exit_func(self, _input):
        exit(0)

    def event_value_edited_Trimmomatic_minlen_popup(self, event):
        self.InputBoxInfo_Trimmomatic_minlen_popup.value = "Minlen_parameters: "+ read_config("Trimmomatic", "MINLEN") + "\n"\
        "only digits 0 to 99 are accepted"
        self.InputBoxInfo_Trimmomatic_minlen_popup.display()
        self.display()

class Trimmomatic_minlen(npyscreen.TitleText):
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
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_edited_Trimmomatic_minlen_popup"))

class trim_leading_select(npyscreen.FixedText):
    def update(self, clear=True,):
        super(trim_leading_select, self).update(clear=clear)
        self.color = "CURSOR"
    def set_up_handlers(self):
        super(trim_leading_select, self).set_up_handlers()
        self.handlers.update({curses.KEY_LEFT:    self.h_cursor_left,
                           curses.KEY_RIGHT:   self.h_cursor_right,
                           ord('k'):    self.h_exit_up,
                           ord('j'):    self.h_exit_down,
                           curses.ascii.NL: self.switchForm
                           })

    def switchForm(self, _input):
        self.parent.parentApp.switchForm('Trimmomatic_leading_popup')

class Trimmomatic_leading_popup(npyscreen.ActionPopup):
    def create(self):

        self.add_event_hander("event_value_edited_Trimmomatic_leading_popup", self.event_value_edited_Trimmomatic_leading_popup)

        new_handlers = {
            #Set ctrl+Q to exit
            "^Q": self.exit_func
        }
        self.add_handlers(new_handlers)

        y, x = self.useable_space()
        self.add(npyscreen.FixedText, value= "", editable=False)
        self.Trimmomatic_leading = self.add(Trimmomatic_leading, name = "Trimmomatic leading parameter", value = read_config("Trimmomatic", "LEADING"), rely = 2)
        self.InputBoxInfo_Trimmomatic_leading_popup = self.add(InputBoxInfoConfig, name="Information", editable=False, max_height=y // 20)  

    def on_ok(self):
        if self.Trimmomatic_leading.value.isdigit():
            if int(self.Trimmomatic_leading.value) < 100:
                replace_config("Trimmomatic", "LEADING", self.Trimmomatic_leading.value)
        self.parentApp.switchForm("ConfigurationPopup_trimmomatic")

    def on_cancel(self):
        self.parentApp.switchForm("ConfigurationPopup_trimmomatic")

    def exit_func(self, _input):
        exit(0)

    def event_value_edited_Trimmomatic_leading_popup(self, event):
        self.InputBoxInfo_Trimmomatic_leading_popup.value = "Leading_parameter: "+ read_config("Trimmomatic", "LEADING") + "\n"\
        "only digits 0 to 99 are accepted"
        self.InputBoxInfo_Trimmomatic_leading_popup.display()
        self.display()

class Trimmomatic_leading(npyscreen.TitleText):
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
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_edited_Trimmomatic_leading_popup"))

class trim_threading_select(npyscreen.FixedText):
    def update(self, clear=True,):
        super(trim_threading_select, self).update(clear=clear)
        self.color = "CURSOR"
    def set_up_handlers(self):
        super(trim_threading_select, self).set_up_handlers()
        self.handlers.update({curses.KEY_LEFT:    self.h_cursor_left,
                           curses.KEY_RIGHT:   self.h_cursor_right,
                           ord('k'):    self.h_exit_up,
                           ord('j'):    self.h_exit_down,
                           curses.ascii.NL: self.switchForm
                           })

    def switchForm(self, _input):
        self.parent.parentApp.switchForm('Trimmomatic_threading_popup')

class Trimmomatic_threading_popup(npyscreen.ActionPopup):
    def create(self):

        self.add_event_hander("event_value_edited_Trimmomatic_threading_popup", self.event_value_edited_Trimmomatic_threading_popup)

        new_handlers = {
            #Set ctrl+Q to exit
            "^Q": self.exit_func
        }
        self.add_handlers(new_handlers)

        y, x = self.useable_space()
        self.add(npyscreen.FixedText, value= "", editable=False)
        self.Trimmomatic_threading = self.add(Trimmomatic_threading, name = "Trimmomatic threading parameter", value = read_config("Trimmomatic", "n_th"), rely = 2)
        self.InputBoxInfo_Trimmomatic_threading_popup = self.add(InputBoxInfoConfig, name="Information", editable=False, max_height=y // 20)  

    def on_ok(self):
        if self.Trimmomatic_threading.value.isdigit():
            if int(self.Trimmomatic_threading.value) < 100:
                replace_config("Trimmomatic", "n_th", self.Trimmomatic_threading.value)
        self.parentApp.switchForm("ConfigurationPopup_trimmomatic")

    def on_cancel(self):
        self.parentApp.switchForm("ConfigurationPopup_trimmomatic")

    def exit_func(self, _input):
        exit(0)

    def event_value_edited_Trimmomatic_threading_popup(self, event):
        self.InputBoxInfo_Trimmomatic_threading_popup.value = "Threading_parameters: "+ read_config("Trimmomatic", "n_th") + "\n"\
        "only digits 0 to 99 are accepted"
        self.InputBoxInfo_Trimmomatic_threading_popup.display()
        self.display()

class Trimmomatic_threading(npyscreen.TitleText):
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
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_edited_Trimmomatic_threading_popup"))




class trim_illuminaclip_select(npyscreen.FixedText):
    def update(self, clear=True,):
        super(trim_illuminaclip_select, self).update(clear=clear)
        self.color = "CURSOR"
    def set_up_handlers(self):
        super(trim_illuminaclip_select, self).set_up_handlers()
        self.handlers.update({curses.KEY_LEFT:    self.h_cursor_left,
                           curses.KEY_RIGHT:   self.h_cursor_right,
                           ord('k'):    self.h_exit_up,
                           ord('j'):    self.h_exit_down,
                           curses.ascii.NL: self.switchForm
                           })

    def switchForm(self, _input):
        self.parent.parentApp.switchForm('Illum_parameters_popup')


class trim_slidingwindow_select(npyscreen.FixedText):
    def update(self, clear=True,):
        super(trim_slidingwindow_select, self).update(clear=clear)
        self.color = "CURSOR"
    def set_up_handlers(self):
        super(trim_slidingwindow_select, self).set_up_handlers()
        self.handlers.update({curses.KEY_LEFT:    self.h_cursor_left,
                           curses.KEY_RIGHT:   self.h_cursor_right,
                           ord('k'):    self.h_exit_up,
                           ord('j'):    self.h_exit_down,
                           curses.ascii.NL: self.switchForm
                           })

    def switchForm(self, _input):
        self.parent.parentApp.switchForm('SlidingWindow_parameters_popup')

class FixedText0_conf(npyscreen.FixedText):
    def update(self, clear=True,):
        super(FixedText0_conf, self).update(clear=clear)
        self.show_bold = True
        self.color = "CURSOR"
    def display(self):
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_editedC0"))


class FixedText1_conf(npyscreen.FixedText):
    def update(self, clear=True,):
        super(FixedText1_conf, self).update(clear=clear)
        self.show_bold = True
        self.color = "CURSOR"
    def display(self):
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_editedC1"))
        new_handlers = {
            curses.ascii.NL: self.switchForm
        }
        self.add_handlers(new_handlers)

    def switchForm(self, _input):
        self.parent.parentApp.configurationPopup_patterns_event_handling = True
        self.parent.parentApp.switchForm('ConfigurationPopup_raw_files')


class FixedText2_conf(npyscreen.FixedText):
    def update(self, clear=True,):
        super(FixedText2_conf, self).update(clear=clear)
        self.show_bold = True
        self.color = "CURSOR"
    def display(self):
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_editedC2"))
        new_handlers = {
            curses.ascii.NL: self.switchForm
        }
        self.add_handlers(new_handlers)

    def switchForm(self, _input):
        self.parent.parentApp.switchForm('ConfigurationPopup_result_files')

class FixedText3_conf(npyscreen.FixedText):
    def update(self, clear=True,):
        super(FixedText3_conf, self).update(clear=clear)
        self.show_bold = True
        self.color = "CURSOR"
    def display(self):
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_editedC3"))
        new_handlers = {
            curses.ascii.NL: self.switchForm
        }
        self.add_handlers(new_handlers)

    def switchForm(self, _input):
        self.parent.parentApp.switchForm('ConfigurationPopup_genome')

class FixedText4_conf(npyscreen.FixedText):
    def update(self, clear=True,):
        super(FixedText4_conf, self).update(clear=clear)
        self.show_bold = True
        self.color = "CURSOR"
    def display(self):
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_editedC4"))
        new_handlers = {
            curses.ascii.NL: self.switchForm
        }
        self.add_handlers(new_handlers)

    def switchForm(self, _input):
        self.parent.parentApp.switchForm('ConfigurationPopup_trimmomatic')

class FixedText5_conf(npyscreen.FixedText):
    def update(self, clear=True,):
        super(FixedText5_conf, self).update(clear=clear)
        self.show_bold = True
        self.color = "CURSOR"
    def display(self):
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_editedC5"))
        new_handlers = {
            curses.ascii.NL: self.switchForm
        }
        self.add_handlers(new_handlers)

    def switchForm(self, _input):
        self.parent.parentApp.switchForm('ConfigurationPopup_QC_fastq_path')

class FixedText6_conf(npyscreen.FixedText):
    def update(self, clear=True,):
        super(FixedText6_conf, self).update(clear=clear)
        self.show_bold = True
        self.color = "CURSOR"
    def display(self):
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_editedC6"))
        new_handlers = {
            curses.ascii.NL: self.switchForm
        }
        self.add_handlers(new_handlers)

    def switchForm(self, _input):
        self.parent.parentApp.switchForm('ConfigurationPopup_Bismark_parameters')

class FixedText7_conf(npyscreen.FixedText):
    def update(self, clear=True,):
        super(FixedText7_conf, self).update(clear=clear)
        self.show_bold = True
        self.color = "CURSOR"
    def display(self):
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_editedC7"))
        new_handlers = {
            curses.ascii.NL: self.switchForm
        }
        self.add_handlers(new_handlers)

    def switchForm(self, _input):
        self.parent.parentApp.switchForm('ConfigurationPopup_Methimpute')

class FixedText8_conf(npyscreen.FixedText):
    def update(self, clear=True,):
        super(FixedText8_conf, self).update(clear=clear)
        self.show_bold = True
        self.color = "CURSOR"
    def display(self):
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_editedC8"))
        new_handlers = {
            curses.ascii.NL: self.switchForm
        }
        self.add_handlers(new_handlers)

    def switchForm(self, _input):
        self.parent.parentApp.switchForm('ConfigurationPopup_Parallel_mode')

class FixedText9_conf(npyscreen.FixedText):
    def update(self, clear=True,):
        super(FixedText9_conf, self).update(clear=clear)
        self.show_bold = True
        self.color = "CURSOR"
    def display(self):
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_editedC9"))

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


def parallel_mode_info():


    detected_parallel_location = "Parallel PATH not detected - please install parallel and export to PATH."
    try:
        detected_parallel_location = subprocess.check_output(['which', 'parallel'])
    except subprocess.CalledProcessError:
        pass
    s = "Auto detected PATH to Parallel: " + detected_parallel_location +  "\n" \
    "Parallel mode (can only be selected true if the PATH to Parallel is auto-detected): " + read_config("GENERAL", "parallel_mode") + "\n" \
    "Number of parallel jobs: " + read_config("GENERAL", "npar")
    return s

def bismark_parameters_info():

    bismark_path_dir = "This is not configured properly."
    if os.path.isdir(read_config("Bismark", "bismark_path")):
        bismark_path_dir = read_config("Bismark", "bismark_path")

    s = "Bismark path: " + bismark_path_dir + "\n" \
    "Bismark multi-processing: " + read_config("Bismark", "bis_parallel") + "\n" \
    "Bismark buffer size: " + read_config("Bismark", "buf_size") + "\n" \
    "Bismark nucleotide coverage report: " + read_config("Bismark", "nucleotide") + "\n" \
    "Bismark paired-end: " + read_config("Bismark", "run_pair_bismark") + "\n"
    return s


def fastq_path_info():
    fastq_path_dir = "This is not configured properly"
    if os.path.isfile(read_config("GENERAL", "fastq_path")):
        fastq_path_dir = read_config("GENERAL", "fastq_path")

    s = "Fastq path: " + fastq_path_dir
    return s


def Trimmomatic_info():

    detected_java_path = "Not Detected - Please make sure that Java is installed and exported to the PATH."
    try:
        detected_java_path = subprocess.check_output(['which', 'java']).strip()
    except subprocess.CalledProcessError, e:
        pass
    
    list_jar = []
    for jarfile in find_file_pattern(read_config("Trimmomatic", "trim_path"), "*.jar"):
        list_jar.append(jarfile)

    jar_file_path = "Not Detected."
    if len(list_jar) == 1:
        replace_config("Trimmomatic", "trim_jar", list_jar[0])
        jar_file_path = read_config("Trimmomatic", "trim_jar")
    elif len(list_jar) > 1:
        jar_file_path = "Multiple Jar files found in the Trimmomatic Software Directory. Please make sure that the correct directory is provided."


    trim_path_dir = "This is not configured correctly."
    if os.path.isdir(read_config("Trimmomatic", "trim_path")):
        trim_path_dir = read_config("Trimmomatic", "trim_path")

    trim_adap_dir = "This is not configured correctly."
    if os.path.isfile(read_config("Trimmomatic", "name_adap")):
        trim_adap_dir = read_config("Trimmomatic", "name_adap")


    s = "Make sure that Java is installed and exported to the PATH. \n" \
    "Auto detected Java program in location: " + detected_java_path + "\n" \
    "Configured Java location: " + read_config("Trimmomatic", "java_path") + "\n\n" \
    "Jar file (auto-detected): " + jar_file_path + "\n" \
    "Trimmomatic path: " + trim_path_dir + "\n" \
    "Trimmomatic Adapter: " + trim_adap_dir + "\n" \
    "Trimmomatic Running mode: " + read_config("Trimmomatic", "end_mode") + "\n" \
    "Trimmomatic ILLUMINACLIP: " + read_config("Trimmomatic", "ill_clip") + "\n" \
    "Trimmomatic LEADING: " + read_config("Trimmomatic", "LEADING") + "\n" \
    "Trimmomatic TRAILING: " + read_config("Trimmomatic", "TRAILING") + "\n" \
    "Trimmomatic SLIDINGWINDOW: " + read_config("Trimmomatic", "SLIDINGWINDOW") + "\n" \
    "Trimmomatic MINLEN: " + read_config("Trimmomatic", "MINLEN") + "\n" \
    "Trimmomatic Threading: " + read_config("Trimmomatic", "n_th")
    return s

def Genome_info():
    di_tosearch = (read_config("GENERAL", "genome_ref"))
    onlyfiles = "N/A"
    if os.path.isdir(di_tosearch):
        onlyfiles = [f for f in listdir(di_tosearch) if isfile(join(di_tosearch, f))]

    genome_dir = "This is not configured properly."
    if os.path.isdir(read_config("GENERAL", "genome_ref")):
        genome_dir = read_config("GENERAL", "genome_ref")

    genome_name = "This is not configured properly."
    if not onlyfiles == "N/A":
        genome_name = read_config("GENERAL", "genome_name")

    s = "Current genome directory location: " + genome_dir + "\n" \
    "Selected genome file: " + genome_name + "\n" \
    "All files in current directory: " + str(onlyfiles)
    return s

def raw_dataset_info():

    list_dataset = find_file_pattern(str(read_config("GENERAL", "raw_dataset")), "*.gz")
    raw_size = ""
    if os.path.isdir(str(read_config("GENERAL", "raw_dataset"))):
        raw_size = subprocess.check_output(['du', '-h', str(read_config("GENERAL", "raw_dataset"))]).split()[-2].decode('utf-8')

    first_pairs = []
    secd_pairs = []
    for file_one in find_file_pattern(read_config("GENERAL", "raw_dataset"), "*"+read_config("GENERAL", "first_pattern")):
        first_pairs.append(file_one)
    for file_two in find_file_pattern(read_config("GENERAL", "raw_dataset"), "*" + read_config("GENERAL", "secnd_pattern")):
        secd_pairs.append(file_two)
    first_pairs=sorted(first_pairs)
    secd_pairs=sorted(secd_pairs)
    first_secd_pairs = []
    for item in range(len(first_pairs)):
        first_secd_pairs.append(first_pairs[item])
        first_secd_pairs.append(secd_pairs[item])

    first_secd_pairs_joined =  "\n".join(first_secd_pairs)

    raw_files_loc = "This is not configured correctly."
    if os.path.isdir(read_config("GENERAL", "raw_dataset")):
        raw_files_loc = read_config("GENERAL", "raw_dataset")

    firstPairText = read_config("GENERAL", "first_pattern")
    secondPairText = read_config("GENERAL", "secnd_pattern")

    if not bool(strtobool(read_config("GENERAL", "pairs_mode"))):
        first_secd_pairs_joined = "These are only relevent in pairs mode and the above patterns must be correct."
        firstPairText = "Only relevant in pairs mode (when paired-end is enabled)."
        secondPairText = "Only relevant in pairs mode (when paired-end is enabled)."

    s = "Current raw files location: " + raw_files_loc + "\n" + \
    "Paired-end: " + str(bool(strtobool(read_config("GENERAL", "pairs_mode")))) + "\n" + \
    "Single-end: " + str(not bool(strtobool(read_config("GENERAL", "pairs_mode")))) + "\n" + \
    "pattern for First pair: " + firstPairText + "\n" + \
    "pattern for second pair: " + secondPairText + "\n\n" + \
    "Number of relevant files in directory: " + str(len(list_dataset)) + "\n" + \
    "Data-set size: "+ str(raw_size) + "\n\n" + \
    "Listed pairs: \n" + \
    first_secd_pairs_joined

    return s

def result_dataset_info():
    size = ["N/A"]
    if os.path.isdir(str(read_config("GENERAL", "result_pipeline"))):
        size = subprocess.check_output(['df', '-Bm', read_config("GENERAL", "result_pipeline")]).split()[-3].decode('utf-8')
        size = [float(s) for s in re.findall(r'-?\d+\.?\d*', size)]
    number_of_dataset=float(read_config("GENERAL", "number_of_dataset"))
    dataset_size = float(read_config("GENERAL", "dataset_size"))
    # size per file
    per_file = round(dataset_size/number_of_dataset)

    result_pipeline_loc = "This is not configured properly."
    if os.path.isdir(read_config("GENERAL", "result_pipeline")):
            result_pipeline_loc = read_config("GENERAL", "result_pipeline")

    s = "Current result files location: " + result_pipeline_loc + "\n\n" + \
    str(size[0]) + " M.byte of free space is available on disk. \n\n" + \
    "Below is a recommendation list regarding the free space on disk (calculation is based on data-set size): \n" + \
    "Free space for Trimmomaatic part: " + str(round(per_file * number_of_dataset * 1.2)) + " Gig.\n" + \
    "Free space for Qc-Fastq reports: " + str(round(2 * number_of_dataset)) + " MB.\n" + \
    "Free space for Bismark-mapper part: " + str(round(per_file * number_of_dataset * 1.8)) + " Gig.\n" + \
    "Free space for Qc-Fastq Bam reports: " + str(round(2 * number_of_dataset)) + " MB.\n" + \
    "Free space for Bismark deduplicate: " + str(round(per_file * number_of_dataset * 1.1)) + " Gig.\n" + \
    "Free space for Bismark-Meth-Extractor:" + str(round(per_file * number_of_dataset * 6)) + " Gig.\n" + \
    "Free space for Methimpute: " + str(round(per_file * number_of_dataset * 1.4)) + " Gig.\n" + \
    "Free space for Other reports: " + str(round(per_file * number_of_dataset * 100)) + " MB.\n" + \
    "Note: We recommended at least " \
          + str(number_of_dataset * 10) + " Gigabyte free space."

    return s

def show_config():
    s = "- RAW files location: " + str(read_config("GENERAL", "raw_dataset")) + "\n" + \
    "- Number and Size of the data-set: " + str(read_config("GENERAL", "number_of_dataset"))\
          + " files and Total size: " + str(read_config("GENERAL", "dataset_size"))+" Gigabyte \n" + \
    "- The directory of results: " + str(read_config("GENERAL", "result_pipeline")) + "\n" + \
    "- Genome folder location: " + str(read_config("GENERAL", "genome_ref")) + "\n" + \
    "     -- Genome Reference name: " + str(read_config("GENERAL", "genome_name")) + "\n" + \
    "- Trimmomatic location: "+ str(read_config("Trimmomatic", "trim_path")) + "\n" + \
    "     -- JAVA path: " + str(read_config("Trimmomatic", "java_path")) + "\n" + \
    "     -- ILLUMINACLIP: " + str(read_config("Trimmomatic", "name_adap"))\
       +":"+str(read_config("Trimmomatic", "ill_clip")) + "\n" + \
    "     -- LEADING: " + str(read_config("Trimmomatic", "LEADING")) + "\n" + \
    "     -- TRAILING: " + str(read_config("Trimmomatic", "TRAILING")) + "\n" + \
    "     -- SLIDINGWINDOW: " + str(read_config("Trimmomatic", "SLIDINGWINDOW")) + "\n" + \
    "     -- MINLEN: " + str(read_config("Trimmomatic", "MINLEN")) + "\n" + \
    "     -- Number of Threads: " + str(read_config("Trimmomatic", "n_th")) + "\n" + \
    "- QC-Fastq path: "+ str(read_config("GENERAL", "fastq_path")) + "\n" + \
    "- Bismark parameters: "+ str(read_config("Bismark", "bismark_path")) + "\n" + \
    "     -- Nucleotide status: " + str(read_config("Bismark", "nucleotide")) + "\n" + \
    "     -- Number of Parallel: " + str(read_config("Bismark", "bis_parallel"))+" Threads. \n" + \
    "     -- Buffer size: " + str(read_config("Bismark", "buf_size"))+" Gigabyte. \n" + \
    "- Parallel mode is: " + str(read_config("GENERAL", "parallel_mode"))  + "\n" + \
    "     -- Parallel jobs configured: " + str(read_config("GENERAL", "npar"))

    return s


def methimpute_info():
    "Methimpute intermediate: " + read_config("Bismark", "nucleotide") + "\n" \

    return s

class Illum_Parameter_Selection(npyscreen.TitleText):
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
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_edited_Illum_parameters_popup"))

class Illum_parameters_popup(npyscreen.ActionPopup):
    def create(self):

        self.add_event_hander("event_value_edited_Illum_parameters_popup", self.event_value_edited_Illum_parameters_popup)

        new_handlers = {
            #Set ctrl+Q to exit
            "^Q": self.exit_func
        }
        self.add_handlers(new_handlers)

        y, x = self.useable_space()
        self.add(npyscreen.FixedText, value= "", editable=False)
        self.Illum_Parameter_Selection = self.add(Illum_Parameter_Selection, name= "Illum_Parameter_Selection", value = read_config("Trimmomatic", "ill_clip"), rely = 2)
        self.InputBoxInfo_Illum_parameters_popup = self.add(InputBoxInfoConfig, name="Information", editable=False, max_height=y // 20)  
        self.InputBoxInfo_Illum_parameters_popup.value = "Illum_parameters (configured): "+ read_config("Trimmomatic", "ill_clip") + "\n" \
        "example format: int:int:int"

    def on_ok(self):
        str_split = self.Illum_Parameter_Selection.value.split(':')

        tester = False
        if len(str_split) == 3:
            counter_str_split = 0
            for e in str_split:
                if e.isdigit():
                    counter_str_split += 1
            if counter_str_split == 3:
                tester = True
        if tester == True:
            replace_config("Trimmomatic", "ill_clip", self.Illum_Parameter_Selection.value)
        self.parentApp.switchForm("ConfigurationPopup_trimmomatic")

    def on_cancel(self):
        self.parentApp.switchForm("ConfigurationPopup_trimmomatic")

    def exit_func(self, _input):
        exit(0)

    def event_value_edited_Illum_parameters_popup(self, event):
        self.InputBoxInfo_Illum_parameters_popup.value = "Illum_parameters (configured): "+ read_config("Trimmomatic", "ill_clip") + "\n" \
        "example format: int:int:int"
        self.InputBoxInfo_Illum_parameters_popup.display()
        self.display()




class SlidingWindow_Parameter(npyscreen.TitleText):
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
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_edited_SlidingWindow_parameters_popup"))


class SlidingWindow_parameters_popup(npyscreen.ActionPopup):
    def create(self):

        self.add_event_hander("event_value_edited_SlidingWindow_parameters_popup", self.event_value_edited_SlidingWindow_parameters_popup)

        new_handlers = {
            #Set ctrl+Q to exit
            "^Q": self.exit_func
        }
        self.add_handlers(new_handlers)

        y, x = self.useable_space()
        self.add(npyscreen.FixedText, value= "", editable=False)
        self.SlidingWindow_Parameter = self.add(SlidingWindow_Parameter, name = "SlidingWindow Parameter", value = read_config("Trimmomatic", "SLIDINGWINDOW"), rely = 2)
        self.InputBoxInfo_SlidingWindow_parameters_popup = self.add(InputBoxInfoConfig, name="Information", editable=False, max_height=y // 20)  
        self.InputBoxInfo_SlidingWindow_parameters_popup.value = "SlidingWindow_parameters: "+ read_config("Trimmomatic", "SLIDINGWINDOW")+ "\n" \
        "example format: int:int"

    def on_ok(self):
        str_split = self.SlidingWindow_Parameter.value.split(':')

        tester = False
        if len(str_split) == 2:
            counter_str_split = 0
            for e in str_split:
                if e.isdigit():
                    counter_str_split += 1
            if counter_str_split == 2:
                tester = True
        if tester == True:
            replace_config("Trimmomatic", "SLIDINGWINDOW", self.SlidingWindow_Parameter.value)
        self.parentApp.switchForm("ConfigurationPopup_trimmomatic")

    def on_cancel(self):
        self.parentApp.switchForm("ConfigurationPopup_trimmomatic")

    def exit_func(self, _input):
        exit(0)

    def event_value_edited_SlidingWindow_parameters_popup(self, event):
        self.InputBoxInfo_SlidingWindow_parameters_popup.value = "SlidingWindow_parameters: "+ read_config("Trimmomatic", "SLIDINGWINDOW")+ "\n" \
        "example format: int:int"
        self.InputBoxInfo_SlidingWindow_parameters_popup.display()
        self.display()

class parallel_jobs_value(npyscreen.TitleText):
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
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_edited_Parallel_jobs_popup"))

class Parallel_jobs_popup(npyscreen.ActionPopup):
    def create(self):

        self.add_event_hander("event_value_edited_Parallel_jobs_popup", self.event_value_edited_Parallel_jobs_popup)

        new_handlers = {
            #Set ctrl+Q to exit
            "^Q": self.exit_func
        }
        self.add_handlers(new_handlers)

        y, x = self.useable_space()
        self.add(npyscreen.FixedText, value= "", editable=False)
        self.parallel_jobs_value = self.add(parallel_jobs_value, name = "Parallel jobs value", value =read_config("GENERAL", "npar"), rely = 2)
        self.InputBoxInfo_Parallel_jobs_popup = self.add(InputBoxInfoConfig, name="Information", editable=False, max_height=y // 20)  

    def on_ok(self):
        if self.parallel_jobs_value.value.isdigit():
            if int(self.parallel_jobs_value.value) < 51 and int(self.parallel_jobs_value.value) > 1:
                replace_config("GENERAL", "npar", self.parallel_jobs_value.value)
        self.parentApp.switchForm("ConfigurationPopup_Parallel_mode")

    def on_cancel(self):
        self.parentApp.switchForm("ConfigurationPopup_Parallel_mode")

    def exit_func(self, _input):
        exit(0)

    def event_value_edited_Parallel_jobs_popup(self, event):
        self.InputBoxInfo_Parallel_jobs_popup.value = "Parallel jobs value: "+ read_config("GENERAL", "npar")  + "\n"\
        "only digits 2 to 50 are accepted"
        self.InputBoxInfo_Parallel_jobs_popup.display()
        self.display()

class parallel_jobs_select(npyscreen.FixedText):
    def update(self, clear=True,):
        super(parallel_jobs_select, self).update(clear=clear)
        self.color = 'CURSOR'

    def set_up_handlers(self):
        super(parallel_jobs_select, self).set_up_handlers()
        self.handlers.update({curses.KEY_LEFT:    self.h_cursor_left,
                           curses.KEY_RIGHT:   self.h_cursor_right,
                           ord('k'):    self.h_exit_up,
                           ord('j'):    self.h_exit_down,
                           curses.ascii.NL: self.switchForm
                           })

    def switchForm(self, _input):
        self.parent.parentApp.switchForm('Parallel_jobs_popup')

class ConfigurationPopup_Parallel_mode(npyscreen.ActionPopup):
    def create_control_buttons(self):
        self._add_button('ok_button', 
                        self.__class__.OKBUTTON_TYPE, 
                        self.__class__.OK_BUTTON_TEXT,
                        0 - self.__class__.OK_BUTTON_BR_OFFSET[0],
                        0 - self.__class__.OK_BUTTON_BR_OFFSET[1] - len(self.__class__.OK_BUTTON_TEXT),
                        None
                        )

    #on OK
    def afterEditing(self):
        try:
            subprocess.check_output(['which', 'parallel'])
            if self.parallel_mode_option.value[0] == 0:
                replace_config("GENERAL", "parallel_mode", "true")
            else:
                replace_config("GENERAL", "parallel_mode", "false")
        except subprocess.CalledProcessError:
            replace_config("GENERAL", "parallel_mode", "false")


    def create(self):
        y, x = self.useable_space()

        parallel_mode_option_toSet = 0
        parallel_mode_option_config = read_config("GENERAL", "parallel_mode")
        if parallel_mode_option_config == "true":
            parallel_mode_option_toSet = 0
        if parallel_mode_option_config == "false":
            parallel_mode_option_toSet = 1

        self.add(npyscreen.FixedText, value= "", editable=False)
        self.parallel_mode_option = self.add(TitleSelectOne_custom, name = "Parallel mode option", max_height=4, value = [parallel_mode_option_toSet,], values = ["True","False"], scroll_exit=True, rely = 2)
        self.parallel_jobs = self.add(parallel_jobs_select, value = "Parallel jobs")

        new_handlers = {
            #Set ctrl+Q to exit
            "^Q": self.exit_func
        }
        self.add_handlers(new_handlers)

    def on_ok(self):
        self.parentApp.setNextForm("Configuration")

    def exit_func(self, _input):
        exit(0)


class ConfigurationPopup_Methimpute(npyscreen.ActionPopup):
    DEFAULT_LINES = 26
    DEFAULT_COLUMNS = 100

    def create_control_buttons(self):
        self._add_button('ok_button', 
                        self.__class__.OKBUTTON_TYPE, 
                        self.__class__.OK_BUTTON_TEXT,
                        0 - self.__class__.OK_BUTTON_BR_OFFSET[0],
                        0 - self.__class__.OK_BUTTON_BR_OFFSET[1] - len(self.__class__.OK_BUTTON_TEXT),
                        None
                        )

    #on OK
    def afterEditing(self):
        if self.intermediate_select.value[0] == 0:
            replace_config("Methimpute", "intermediate", "true")
        else:
            replace_config("Methimpute", "intermediate", "false")

        if self.fit_output_select.value[0] == 0:
            replace_config("Methimpute", "fit_output", "true")
        else:
            replace_config("Methimpute", "fit_output", "false")

        if self.enrichment_plot_select.value[0] == 0:
            replace_config("Methimpute", "enrichment_plot", "true")
        else:
            replace_config("Methimpute", "enrichment_plot", "false")

        if self.TES_report_select.value[0] == 0:
            replace_config("Methimpute", "TES_report", "true")
        else:
            replace_config("Methimpute", "TES_report", "false")

        if self.genes_report_select.value[0] == 0:
            replace_config("Methimpute", "genes_report", "true")
        else:
            replace_config("Methimpute", "genes_report", "false")


    def create(self):
        y, x = self.useable_space()


        intermediate_value = 0
        try:
            if read_config("Methimpute", "intermediate") == "true":
                intermediate_value = 0
            elif read_config("Methimpute", "intermediate") == "false":
                intermediate_value = 1
        except IndexError:    
            pass

        fit_output_value = 0
        try:
            if read_config("Methimpute", "fit_output") == "true":
                fit_output_value = 0
            elif read_config("Methimpute", "fit_output") == "false":
                fit_output_value = 1
        except IndexError:    
            pass

        enrichment_plot_value = 0
        try:
            if read_config("Methimpute", "enrichment_plot") == "true":
                enrichment_plot_value = 0
            elif read_config("Methimpute", "enrichment_plot") == "false":
                enrichment_plot_value = 1
        except IndexError:    
            pass

        TES_report_value = 0
        try:
            if read_config("Methimpute", "TES_report") == "true":
                TES_report_value = 0
            elif read_config("Methimpute", "TES_report") == "false":
                TES_report_value = 1
        except IndexError:    
            pass

        genes_report_value = 0
        try:
            if read_config("Methimpute", "genes_report") == "true":
                genes_report_value = 0
            elif read_config("Methimpute", "genes_report") == "false":
                genes_report_value = 1
        except IndexError:    
            pass

        self.add(npyscreen.FixedText, value= "", editable=False)
        self.intermediate_select = self.add(TitleSelectOne_custom, name = "Intermediate", max_height=4, value = [intermediate_value,], values = ["True","False"], scroll_exit=True, rely = 2)
        self.fit_output_select = self.add(TitleSelectOne_custom, name = "Fit output", max_height=4, value = [fit_output_value,], values = ["True","False"], scroll_exit=True)
        self.enrichment_plot_select = self.add(TitleSelectOne_custom, name = "Enrichment plot", max_height=4, value = [enrichment_plot_value,], values = ["True","False"], scroll_exit=True)
        self.TES_report_select = self.add(TitleSelectOne_custom, name = "TES report", max_height=4, value = [TES_report_value,], values = ["True","False"], scroll_exit=True)
        self.genes_report_select = self.add(TitleSelectOne_custom, name = "Genes report", max_height=4, value = [genes_report_value,], values = ["True","False"], scroll_exit=True)

        new_handlers = {
            #Set ctrl+Q to exit
            "^Q": self.exit_func
        }
        self.add_handlers(new_handlers)

    def on_ok(self):
        self.parentApp.setNextForm("Configuration")

    def exit_func(self, _input):
        exit(0)



class ConfigurationPopup_Bismark_parameters(npyscreen.ActionPopup):
    DEFAULT_LINES = 23

    def create_control_buttons(self):
        self._add_button('ok_button', 
                        self.__class__.OKBUTTON_TYPE, 
                        self.__class__.OK_BUTTON_TEXT,
                        0 - self.__class__.OK_BUTTON_BR_OFFSET[0],
                        0 - self.__class__.OK_BUTTON_BR_OFFSET[1] - len(self.__class__.OK_BUTTON_TEXT),
                        None
                        )

    def create(self):
        y, x = self.useable_space()

        self.add(npyscreen.FixedText, value= "", editable=False)
        self.bismark_path = self.add(TitleFilenameCombo_custom, name = "Bismark Path", value = read_config("Bismark", "bismark_path"), rely = 2)
        self.bismark_parallel = self.add(bismark_parallel_select, value = "Bismark multi-processes")
        self.bismark_buffer_size = self.add(bismark_buffer_size_select, value = "Bismark buffer_size")
        self.bismark_nucleotide_option = self.add(TitleSelectOne_custom, name = "Bismark nucleotide coverage report", max_height=4, value = [strtobool(str(not read_config("Bismark", "nucleotide"))),], values = ["True","False"], scroll_exit=True)
        self.bismark_run_pair_option = self.add(TitleSelectOne_custom, name = "Bismark run paired-end", max_height=4, value = [strtobool(str(not read_config("Bismark", "run_pair_bismark"))),], values = ["True","False"], scroll_exit=True)

        new_handlers = {
            #Set ctrl+Q to exit
            "^Q": self.exit_func
        }
        self.add_handlers(new_handlers)

    def on_cancel(self):
        self.parentApp.setNextForm("Configuration")

    def on_ok(self):
        if os.path.isdir(self.bismark_path.value):
            replace_config("Bismark", "bismark_path", self.bismark_path.value)

        if self.bismark_run_pair_option.value[0] == 0:
            replace_config("Bismark", "run_pair_bismark", "true")
        else:
            replace_config("Bismark", "run_pair_bismark", "false")

        if self.bismark_nucleotide_option.value[0] == 0:
            replace_config("Bismark", "nucleotide", "true")
        else:
            replace_config("Bismark", "nucleotide", "false")

        self.parentApp.setNextForm("Configuration")

    def exit_func(self, _input):
        exit(0)



class ConfigurationPopup_QC_fastq_path(npyscreen.Popup):
    #on OK
    def afterEditing(self):
        if os.path.isfile(self.QC_fastq_path.value):
            replace_config("GENERAL", "fastq_path", self.QC_fastq_path.value)
        self.parentApp.setNextForm("Configuration")


    def create(self):
        y, x = self.useable_space()

        self.add(npyscreen.FixedText, value= "", editable=False)
        self.QC_fastq_path = self.add(TitleFilenameCombo_custom, name = "Fastq Path", value = read_config("GENERAL", "fastq_path"), rely = 2)
  
                                                
        new_handlers = {
            #Set ctrl+Q to exit
            "^Q": self.exit_func
        }
        self.add_handlers(new_handlers)

    def on_cancel(self, _input):
        self.parentApp.setNextForm("Configuration")

    def exit_func(self, _input):
        exit(0)




class ConfigurationPopup_trimmomatic(npyscreen.ActionPopup):
    DEFAULT_LINES = 20

    #on OK
    def afterEditing(self):
        detected_java_path = ""
        try:
            detected_java_path = subprocess.check_output(['which', 'java']).strip()
        except subprocess.CalledProcessError, e:
            pass
        
        if isinstance(self.entered_java_path.value, collections.Sized):
            if len(self.entered_java_path.value) > 0:
                if os.path.isdir(self.entered_java_path.value):
                    replace_config("Trimmomatic", "java_path", self.entered_java_path.value)
            else:
                replace_config("Trimmomatic", "java_path", detected_java_path)
        else:
            replace_config("Trimmomatic", "java_path", detected_java_path)

        if os.path.isdir(self.trim_path.value):
            replace_config("Trimmomatic", "trim_path",  self.trim_path.value)
        if os.path.isfile(self.trim_adapter.value):
            replace_config("Trimmomatic", "name_adap",  self.trim_adapter.value)
        
        if self.trim_run_mode.value[0] == 0:
            replace_config("Trimmomatic", "end_mode",  "SE")
        else:
            replace_config("Trimmomatic", "end_mode",  "PE")

    def create_control_buttons(self):
        self._add_button('ok_button', 
                        self.__class__.OKBUTTON_TYPE, 
                        self.__class__.OK_BUTTON_TEXT,
                        0 - self.__class__.OK_BUTTON_BR_OFFSET[0],
                        0 - self.__class__.OK_BUTTON_BR_OFFSET[1] - len(self.__class__.OK_BUTTON_TEXT),
                        None
                        )

    def create(self):
        y, x = self.useable_space()

        trim_run_mode_config_value = 0
        try:
            if read_config("Trimmomatic", "end_mode") == "SE":
                trim_run_mode_config_value = 0
            elif read_config("Trimmomatic", "end_mode") == "PE":
                trim_run_mode_config_value = 1
        except IndexError:    
            pass

        self.add(npyscreen.FixedText, value= "", editable=False)
        self.entered_java_path = self.add(java_path_select, name = "Type Java Path or leave blank for auto selection", value = read_config("Trimmomatic", "java_path"), rely=2)
        self.trim_path = self.add(TitleFilenameCombo_custom, name = "Select Trimmomatic path", value = read_config("Trimmomatic", "trim_path"))
        self.trim_adapter = self.add(TitleFilenameCombo_custom, name = "Select Trimmomatic adapter", value = read_config("Trimmomatic", "name_adap"))
        self.trim_run_mode = self.add(TitleSelectOne_custom, name = "Select run mode", values = ["Single end","Paired end"], scroll_exit=True,max_height=4, value = [trim_run_mode_config_value,] )
        self.trim_illuminaclip = self.add(trim_illuminaclip_select, value = "Select Illuminaclip parameters")
        self.trim_leading = self.add(trim_leading_select, value = "Select Trimmomatic Leading")
        self.trim_trailing = self.add(trim_trailing_select, value = "Select Trimmomatic Trailing")
        self.trim_slidingwindow = self.add(trim_slidingwindow_select, value = "Select Trimmomatic sliding window")
        self.trim_minlen = self.add(trim_minlen_select, value = "Select Trimmomatic minlen")
        self.trim_threading = self.add(trim_threading_select, value = "Select Trimmomatic Threading")

        

        new_handlers = {
            #Set ctrl+Q to exit
            "^Q": self.exit_func
        }
        self.add_handlers(new_handlers)

        self.display()

    def on_ok(self):
        self.parentApp.switchForm("Configuration")

    def exit_func(self, _input):
        exit(0)



class ConfigurationPopup_genome(npyscreen.Popup):
    #on OK
    def afterEditing(self):
        
        if os.path.isfile(self.genome_directory_files.value):
            head, tail = os.path.split(self.genome_directory_files.value)
            replace_config("GENERAL", "genome_name", tail)
            replace_config("GENERAL", "genome_ref", head)
        
        self.parentApp.setNextForm("Configuration")


    def create(self):
        #event_value_edited_configurationPopup_genome
        y, x = self.useable_space()

        self.add(npyscreen.FixedText, value= "", editable=False)
        genome_file_location = str(read_config("GENERAL", "genome_ref")) + "/" + str(read_config("GENERAL", "genome_name"))
        self.genome_directory_files = self.add(TitleFilenameCombo_custom, name = "Genome file name", value = genome_file_location, rely=2)

        new_handlers = {
            #Set ctrl+Q to exit
            "^Q": self.exit_func
        }
        self.add_handlers(new_handlers)

        self.display()

    def on_cancel(self, _input):
        self.parentApp.setNextForm("Configuration")

    def on_okay(self):
        self.parentApp.setNextForm("Configuration")

    def exit_func(self, _input):
        exit(0)


class mode_singles_pairs(npyscreen.TitleSelectOne):
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
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_edited_configurationPopup_raw_files"))


class genome_directory(npyscreen.TitleFilenameCombo):
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
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_edited_configurationPopup_raw_files"))


class ConfigurationPopup_raw_files(npyscreen.Popup):
    #on OK
    def afterEditing(self):
        if os.path.isdir(self.genome_directory.value):
            replace_config("GENERAL", "raw_dataset", self.genome_directory.value)
        replace_config("GENERAL", "pairs_mode", str(bool(self.mode_singles_pairs.value[0])).lower() )
        replace_config("GENERAL", "first_pattern", self.pattern_1.value)
        replace_config("GENERAL", "secnd_pattern", self.pattern_2.value)
        self.parentApp.configurationPopup_patterns_event_handling = False
        self.parentApp.setNextForm("Configuration")


    def create(self): 
        self.lines = 14

        y, x = self.useable_space()
        self.add_event_hander("event_value_edited_configurationPopup_raw_files", self.event_value_edited_configurationPopup_raw_files)

        try:
            bool_num_value_mode_singles_pairs = strtobool(read_config("GENERAL", "pairs_mode"))
        except ValueError:  
            bool_num_value_mode_singles_pairs = 0
        
        self.add(npyscreen.FixedText, value= "", editable=False)
        self.genome_directory = self.add(genome_directory, name = "Directory Path", value = read_config("GENERAL", "raw_dataset"), rely=2)
        self.mode_singles_pairs = self.add(mode_singles_pairs, max_height=4, value = [bool_num_value_mode_singles_pairs,], name="Select from the following:",
                values = ["Single-end","Paired-end"], scroll_exit=True)
        self.pattern_1 = self.add(title_text_pattern, name="1st pair pattern:", value = read_config("GENERAL", "first_pattern"))
        self.pattern_2 = self.add(title_text_pattern, name="2nd pair pattern:", value = read_config("GENERAL", "secnd_pattern"))

        new_handlers = {
            #Set ctrl+Q to exit
            "^Q": self.exit_func
        }
        self.add_handlers(new_handlers)

    def event_value_edited_configurationPopup_raw_files(self, event):
        if self.parentApp.configurationPopup_patterns_event_handling == True:
            self.display()
            if self.mode_singles_pairs.value[0] == 0:
                self.pattern_1.hidden = True
                self.pattern_2.hidden = True
                self.mode_singles_pairs.display()
                self.display()
            elif self.mode_singles_pairs.value[0] == 1:
                self.pattern_1.hidden = False
                self.pattern_2.hidden = False
                self.mode_singles_pairs.display()
                self.display()


    def on_cancel(self, _input):
        self.parentApp.setNextForm("Configuration")

    def on_okay(self):
        self.parentApp.setNextForm("Configuration")

    def exit_func(self, _input):
        exit(0)


class ConfigurationPopup_result_files(npyscreen.Popup):
    #on OK
    def afterEditing(self):
        if os.path.isdir(self.result_files_location.value):
            replace_config("GENERAL", "result_pipeline", self.result_files_location.value)
        self.parentApp.setNextForm("Configuration")


    def create(self):
        y, x = self.useable_space()

        self.add(npyscreen.FixedText, value= "", editable=False)
        self.result_files_location = self.add(TitleFilenameCombo_custom, name = "Directory Path", value = read_config("GENERAL", "result_pipeline"), rely=2)
  
                                                
        new_handlers = {
            #Set ctrl+Q to exit
            "^Q": self.exit_func
        }
        self.add_handlers(new_handlers)

        

    def on_cancel(self, _input):
        self.parentApp.setNextForm("Configuration")

    def on_okay(self):
        self.parentApp.setNextForm("Configuration")

    def exit_func(self, _input):
        exit(0)

class OK_Button_configuration(npyscreen.ButtonPress):
    def display(self):
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_edited_ok_configuration"))
    def whenPressed(self):
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_edited_ok_configuration_pressed"))


class Configuration(npyscreen.FormBaseNew):
    def create(self):
        self.add_event_hander("event_value_editedC0", self.event_value_editedC0)
        self.add_event_hander("event_value_editedC1", self.event_value_editedC1)
        self.add_event_hander("event_value_editedC2", self.event_value_editedC2)
        self.add_event_hander("event_value_editedC3", self.event_value_editedC3)
        self.add_event_hander("event_value_editedC4", self.event_value_editedC4)
        self.add_event_hander("event_value_editedC5", self.event_value_editedC5)
        self.add_event_hander("event_value_editedC6", self.event_value_editedC6)
        self.add_event_hander("event_value_editedC7", self.event_value_editedC7)
        self.add_event_hander("event_value_editedC8", self.event_value_editedC8)
        self.add_event_hander("event_value_editedC9", self.event_value_editedC9)
        self.add_event_hander("event_value_edited_ok_configuration", self.event_value_edited_ok_configuration)
        self.add_event_hander("event_value_edited_ok_configuration_pressed", self.event_value_edited_ok_configuration_pressed)

        new_handlers = {
            # Set ctrl+Q to exit
            "^Q": self.exit_func,
        }
        self.add_handlers(new_handlers)

        y, x = self.useable_space()

        self.FixedText0_conf = self.add(FixedText0_conf, value= "", editable= True, rely=1)
        self.add(FixedText1_conf, value = "Path: RAW files")
        self.add(FixedText2_conf, value = "Path: Export results")
        self.add(FixedText3_conf, value = "Path: Reference Genome")
        self.add(FixedText4_conf, value = "Read-trimming parameters")
        self.add(FixedText5_conf, value = "Path: QC-Fastq")
        self.add(FixedText6_conf, value = "Alignment parameters")
        self.add(FixedText7_conf, value = "Methimpute parameters")
        self.add(FixedText8_conf, value = "Parallel mode")
        self.add(FixedText9_conf, value = "Configuration Summary", rely=11)

        self.InputBoxInfoConfig = self.add(InputBoxInfoConfig, name="Information", editable=False, max_height=y // 2, rely=16)

        self.OK_Button_configuration = self.add(OK_Button_configuration, name="OK", relx=-12, rely=-3)

    def event_value_editedC0(self, event):
        self.FixedText0_conf.editing = 0
        self.FixedText0_conf.how_exited = True

    def event_value_editedC1(self, event):
        self.InputBoxInfoConfig.value = raw_dataset_info()
        self.InputBoxInfoConfig.display()
        self.display()
        self.FixedText0_conf.editable = False

    def event_value_editedC2(self, event):
        self.InputBoxInfoConfig.value = result_dataset_info()
        self.InputBoxInfoConfig.display()
        self.display()

    def event_value_editedC3(self, event):
        self.InputBoxInfoConfig.value = Genome_info()
        self.InputBoxInfoConfig.display()
        self.display()

    def event_value_editedC4(self, event):
        self.InputBoxInfoConfig.value = Trimmomatic_info()
        self.InputBoxInfoConfig.display()
        self.display()

    def event_value_editedC5(self, event):
        self.InputBoxInfoConfig.value = fastq_path_info()
        self.InputBoxInfoConfig.display()
        self.display()

    def event_value_editedC6(self, event):
        self.InputBoxInfoConfig.value = bismark_parameters_info()
        self.InputBoxInfoConfig.display()
        self.display()
  
    def event_value_editedC7(self, event):
        self.InputBoxInfoConfig.value = "Methimpute"
        self.InputBoxInfoConfig.display()
        self.display()

    def event_value_editedC8(self, event):
        self.InputBoxInfoConfig.value = parallel_mode_info()
        self.InputBoxInfoConfig.display()
        self.display()
  
    def event_value_editedC9(self, event):
        self.InputBoxInfoConfig.value = show_config()
        self.InputBoxInfoConfig.display()
        self.display()

    def event_value_edited_ok_configuration(self, event):
        self.InputBoxInfoConfig.value = "Accept changes that were made and proceed back to the main form."
        self.InputBoxInfoConfig.display()
        self.display()

    def event_value_edited_ok_configuration_pressed(self, event):
        self.parentApp.switchForm("MAIN")
        self.editw = 0

    def exit_func(self, _input):
        exit(0)