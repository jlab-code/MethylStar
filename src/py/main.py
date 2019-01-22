import npyscreen
import curses
import subprocess
import Run_pipeline as RP
import Clean_directories as CD
import Jbrowser as J
import Outputs as O
import Help as H
import Configuration as C
import textwrap


class App(npyscreen.StandardApp):
    RP = "Unset"
    OP = "Unset"
    CL = "Unset"
    to_del_dir = "Unset"
    subprocess_handling_count = 0
    subprocess_handling_count_OP = 0
    numLinesPager = 28
    configurationPopup_patterns_event_handling = False

    def onStart(self):
        # Set the theme. DefaultTheme is used by default
        npyscreen.setTheme(npyscreen.Themes.ColorfulTheme)
        
        self.addForm("MAIN", MainForm, name="Methylstar")
        #self.addForm("DMR", D.DMR, name="DMR")
        self.addForm("JBrowser", J.JBrowser, name="JBrowser")
        self.addForm("Help", H.Help, name="Help")

        #forms and popups of Configuration
        self.addForm("Configuration", C.Configuration, name="Configuration")
        self.addForm("ConfigurationPopup_raw_files", C.ConfigurationPopup_raw_files, name="Raw Files Configuration")
        self.addForm("ConfigurationPopup_result_files", C.ConfigurationPopup_result_files, name="Result Files Configuration")
        self.addForm("ConfigurationPopup_genome", C.ConfigurationPopup_genome, name="Genome Configuration")
        self.addForm("ConfigurationPopup_trimmomatic", C.ConfigurationPopup_trimmomatic, name="Trimmomatic Configuration")
        self.addForm("ConfigurationPopup_QC_fastq_path", C.ConfigurationPopup_QC_fastq_path, name="QC fastq path Config")
        self.addForm("ConfigurationPopup_Bismark_parameters", C.ConfigurationPopup_Bismark_parameters, name="Bismark parameters Config")
        self.addForm("ConfigurationPopup_Parallel_mode", C.ConfigurationPopup_Parallel_mode, name="Parallel mode config")
        self.addForm("Illum_parameters_popup", C.Illum_parameters_popup, name="Illum parameters popup")
        self.addForm("SlidingWindow_parameters_popup", C.SlidingWindow_parameters_popup, name="SlidingWindow parameters popup")
        self.addForm("Trimmomatic_leading_popup", C.Trimmomatic_leading_popup, name="Trimmomatic leading popup")
        self.addForm("Trimmomatic_threading_popup", C.Trimmomatic_threading_popup, name="Trimmomatic threading popup")
        self.addForm("Trimmomatic_minlen_popup", C.Trimmomatic_minlen_popup, name="Trimmomatic minlen popup")
        self.addForm("Trimmomatic_trailing_popup", C.Trimmomatic_trailing_popup, name="Trimmomatic trailing popup")
        self.addForm("Bismark_parallel_popup", C.Bismark_parallel_popup, name="Bismark parallel popup")
        self.addForm("Bismark_buffer_size_popup", C.Bismark_buffer_size_popup, name="Bismark buffer size popup")
        self.addForm("Parallel_jobs_popup", C.Parallel_jobs_popup, name="Parallel jobs popup")
        self.addForm("ConfigurationPopup_Methimpute", C.ConfigurationPopup_Methimpute, name="Methimpute Configuration")

        #forms and popups of Run_pipeline
        self.addForm("Run_pipeline", RP.Run_pipeline, name="Run pipeline")
        self.addForm("Run_popup", RP.Run_popup, name="Run_popup")

        #forms and popups of Outputs
        self.addForm("Outputs", O.Outputs, name="Outputs")
        self.addForm("Outputs_popup", O.Outputs_popup, name="Outputs_popup")

        #forms and popups of Run_pipeline
        self.addForm("Clean_directories", CD.CleanFiles, name="Clean_directories")
        self.addForm("Clean_popup", CD.Clean_popup, name="Clean_popup")

class welcomeMessage(npyscreen.FixedText):
    def update(self, clear=True,):
        super(welcomeMessage, self).update(clear=clear)
        self.color = 'CURSOR'


class FixedText1(npyscreen.FixedText):
    def update(self, clear=True,):
        super(FixedText1, self).update(clear=clear)
        self.show_bold = True
        self.color = 'CURSOR'
    def display(self):
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_edited1"))
        new_handlers = {
            curses.ascii.NL: self.switchForm
        }
        self.add_handlers(new_handlers)

    def switchForm(self, _input):
        self.parent.parentApp.switchForm('Run_pipeline')

class FixedText2(npyscreen.FixedText):
    def update(self, clear=True,):
        super(FixedText2, self).update(clear=clear)
        self.show_bold = True
        self.color = 'CURSOR'
    def display(self):
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_edited2"))
        new_handlers = {
            curses.ascii.NL: self.switchForm
        }
        self.add_handlers(new_handlers)

    def switchForm(self, _input):
        self.parent.parentApp.switchForm('Clean_directories')

class FixedText3(npyscreen.FixedText):
    def update(self, clear=True,):
        super(FixedText3, self).update(clear=clear)
        self.show_bold = True
        self.color = 'CURSOR'
    def display(self):
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_edited3"))
        new_handlers = {
            curses.ascii.NL: self.switchForm
        }
        self.add_handlers(new_handlers)

    def switchForm(self, _input):
        self.parent.parentApp.switchForm('JBrowser')


class FixedText4(npyscreen.FixedText):
    def update(self, clear=True,):
        super(FixedText4, self).update(clear=clear)
        self.show_bold = True
        self.color = 'CURSOR'
    def display(self):
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_edited4"))
        new_handlers = {
            curses.ascii.NL: self.switchForm
        }
        self.add_handlers(new_handlers)

    def switchForm(self, _input):
        self.parent.parentApp.switchForm('Outputs')


class FixedText5(npyscreen.FixedText):
    def update(self, clear=True,):
        super(FixedText5, self).update(clear=clear)
        self.show_bold = True
        self.color = 'CURSOR'
    def display(self):
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_edited5"))
        new_handlers = {
            curses.ascii.NL: self.switchForm
        }
        self.add_handlers(new_handlers)

    def switchForm(self, _input):
        self.parent.parentApp.switchForm('Help')


class FixedText6(npyscreen.FixedText):
    def update(self, clear=True,):
        super(FixedText6, self).update(clear=clear)
        self.show_bold = True
        self.color = 'CURSOR'
    def display(self):
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_edited6"))
        new_handlers = {
            curses.ascii.NL: self.switchForm
        }
        self.add_handlers(new_handlers)

    def switchForm(self, _input):
        self.parent.parentApp.switchForm('Configuration')

class CustomMultiLineEdit(npyscreen.MultiLineEdit):
    def update(self, clear=True,):
        super(CustomMultiLineEdit, self).update(clear=clear)
        self.color = 'CAUTION'

class InputBoxInfo(npyscreen.BoxTitle):
    _contained_widget = CustomMultiLineEdit
    def update(self, clear=True,):
        super(InputBoxInfo, self).update(clear=clear)
        self.color = 'CURSOR'

class ExitButton(npyscreen.ButtonPress):
    def display(self):
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_edited_exit"))
    def whenPressed(self):
        exit(0)

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

class MainForm(npyscreen.FormBaseNew):
    def create(self):

        self.add_event_hander("event_value_edited1", self.event_value_edited1)
        self.add_event_hander("event_value_edited2", self.event_value_edited2)
        self.add_event_hander("event_value_edited3", self.event_value_edited3)
        self.add_event_hander("event_value_edited4", self.event_value_edited4)
        self.add_event_hander("event_value_edited5", self.event_value_edited5)
        self.add_event_hander("event_value_edited6", self.event_value_edited6)
        self.add_event_hander("event_value_edited_exit", self.event_value_edited_exit)

        new_handlers = {
            # Set ctrl+Q to exit
            "^Q": self.exit_func,
        }
        self.add_handlers(new_handlers)
        self.how_exited_handers[npyscreen.wgwidget.EXITED_ESCAPE] = self.exit_application

        y, x = self.useable_space()


        self.add(npyscreen.FixedText, value= "", editable=False)
        self.add(welcomeMessage, value= "Welcome to Methylstar: a comprehensive, fast and flexible analysis pipeline " \
        "specifically suited for processing large amounts of bisulfite sequencing data.", editable=False, rely=2)
        self.add(welcomeMessage, value= "Developed by the Jlab group at TUM.", editable=False)        
        
        self.FixedText1 = self.add(FixedText1, value = "Run Pipeline (WGBS)", rely=5)
        self.FixedText2 = self.add(FixedText2, value = "Clean-up files", rely=6)
        self.FixedText3 = self.add(FixedText3, value = "Access JBROWSE", rely=7)
        self.FixedText4 = self.add(FixedText4, value = "Outputs/Reports", rely=8)
        self.FixedText5 = self.add(FixedText5, value = "Help", rely=9)

        self.FixedText6 = self.add(FixedText6, value = "Configuration", rely=11)

        self.exitButton = self.add(ExitButton, name="Exit", relx=-12, rely=-3)

        self.InputBoxInfo = self.add(InputBoxInfo, name="Information", editable=False, max_height=y // 4, rely=16)

    def exit_application(self):
        self.parentApp.setNextForm(None)
        self.editing = False

    def event_value_edited1(self, event):
        infoSTR = formatted_info_box_str('information_box/Run_pipeline')
        self.InputBoxInfo.value = infoSTR

        self.InputBoxInfo.display()
        self.display()

    def event_value_edited2(self, event):
        infoSTR = "Clean up files"
        self.InputBoxInfo.value = infoSTR

        self.InputBoxInfo.display()
        self.display()

    def event_value_edited3(self, event):
        infoSTR = formatted_info_box_str('information_box/Access_JBROWSE')
        self.InputBoxInfo.value = infoSTR

        self.InputBoxInfo.display()
        self.display()

    def event_value_edited4(self, event):
        infoSTR = formatted_info_box_str('information_box/Outputs_Reports')
        self.InputBoxInfo.value = infoSTR

        self.InputBoxInfo.display()
        self.display()


    def event_value_edited5(self, event):
        infoSTR = formatted_info_box_str('information_box/Help')
        self.InputBoxInfo.value = infoSTR

        self.InputBoxInfo.display()
        self.display()


    def event_value_edited6(self, event):
        infoSTR = formatted_info_box_str('information_box/Configuration')
        self.InputBoxInfo.value = infoSTR

        self.InputBoxInfo.display()
        self.display()

    def event_value_edited_exit(self, event):
        self.InputBoxInfo.value = "Exit"
        self.InputBoxInfo.display()
        self.display()

    def exit_func(self, _input):
        exit(0)

