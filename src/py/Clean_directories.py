import npyscreen
import curses
import ConfigParser
import os, os.path

def del_files_in_dir(cleanDirName):
    if cleanDirName == "Clean Trimommatic":
        folders = [read_config("GENERAL", "result_pipeline")+"/trimmomatic-files", 
                  read_config("GENERAL", "result_pipeline")+"/trimmomatic-logs"]
    
    if cleanDirName == "Clean QC-Fastq-report":
        folders = [read_config("GENERAL", "result_pipeline")+"/qc-fastq-reports"]

    if cleanDirName == "Clean Bismark Mapper":
        folders = [read_config("GENERAL", "result_pipeline")+"/bismark-mappers"]

    if cleanDirName == "Clean QC-Bam report":
        folders = [read_config("GENERAL", "result_pipeline")+"/qc-bam-reports"]

    if cleanDirName == "Clean Bismark-deduplicate":
        folders = [read_config("GENERAL", "result_pipeline")+"/bismark-deduplicate"]

    if cleanDirName == "Clean Bismark Meth. Extractor":
        folders = [read_config("GENERAL", "result_pipeline")+"/bismark-meth-extractor"]

    if cleanDirName == "Clean CX reports":
        folders = [read_config("GENERAL", "result_pipeline")+"/cx-reports"]

    if cleanDirName == "Clean Methimpute":
        folders = [read_config("GENERAL", "result_pipeline")+"/methimpute-out", 
                  read_config("GENERAL", "result_pipeline")+"/tes-reports",
                  read_config("GENERAL", "result_pipeline")+"/gen-reports",
                  read_config("GENERAL", "result_pipeline")+"/fit-reports"]

    if cleanDirName == "Clean DMR":
        folders = [read_config("GENERAL", "result_pipeline")+"/dmrcaller-format"]

    if cleanDirName == "Clean Meth-bedgraph":
        folders = [read_config("GENERAL", "result_pipeline")+"/bedgraph-fromat"]

    if cleanDirName == "Clean methylkit":
        folders = [read_config("GENERAL", "result_pipeline")+"/methylkit-format"]

    if cleanDirName == "Clean bigwig":
        folders = [read_config("GENERAL", "result_pipeline")+"/bigwig-fromat"]

    #print folders
    try:
        for f in folders:
            #print f
            for the_file in os.listdir(f):
                file_path = os.path.join(f, the_file)
                
                if os.path.isfile(file_path):
                    os.unlink(file_path)
    except Exception as e:
        pass


class yesButton(npyscreen.FixedText):
    def update(self, clear=True):
        super(yesButton, self).update(clear=clear)
        #self.show_bold = True
        self.color = 'CURSOR'
    def display(self):
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_edited_CL_popup"))
    def set_up_handlers(self):
        super(yesButton, self).set_up_handlers()
        self.handlers.update({
                           curses.ascii.NL: self.delete_and_exit
                           })

    def delete_and_exit(self, _input):
        del_files_in_dir(self.parent.parentApp.CL)
        self.parent.parentApp.CL = "Unset"
        self.parent.parentApp.switchForm("Clean_directories")





class OK_Button_clean_directories(npyscreen.ButtonPress):
    def display(self):
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_edited_ok_clean_directories"))
    def whenPressed(self):
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_edited_ok_clean_directories_pressed"))


class CustomMultiLineEdit_CL(npyscreen.MultiLineEdit):
    def update(self, clear=True,):
        super(CustomMultiLineEdit_CL, self).update(clear=clear)
        self.color = 'CAUTION'

class InputBoxInfoCL(npyscreen.BoxTitle):
    _contained_widget = CustomMultiLineEdit_CL
    def update(self, clear=True,):
        super(InputBoxInfoCL, self).update(clear=clear)
        self.color = 'CURSOR'

class FixedText0_CL(npyscreen.FixedText):
    def update(self, clear=True,):
        super(FixedText0_CL, self).update(clear=clear)
        self.show_bold = True
        self.color = 'CURSOR'
    def display(self):
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_editedCL0"))

class FixedText1_CL(npyscreen.FixedText):
    def update(self, clear=True,):
        super(FixedText1_CL, self).update(clear=clear)
        self.show_bold = True
        self.color = 'CURSOR'
    def display(self):
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_editedCL1"))
        new_handlers = {
            curses.ascii.NL: self.switchForm
        }
        self.add_handlers(new_handlers)

    def switchForm(self, _input):
        self.parent.parentApp.CL = "Clean Trimommatic"
        self.parent.parentApp.switchForm('Clean_popup')

class FixedText2_CL(npyscreen.FixedText):
    def update(self, clear=True,):
        super(FixedText2_CL, self).update(clear=clear)
        self.show_bold = True
        self.color = 'CURSOR'
    def display(self):
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_editedCL2"))
        new_handlers = {
            curses.ascii.NL: self.switchForm
        }
        self.add_handlers(new_handlers)

    def switchForm(self, _input):
        self.parent.parentApp.CL = "Clean QC-Fastq-report"
        self.parent.parentApp.switchForm('Clean_popup')

class FixedText3_CL(npyscreen.FixedText):
    def update(self, clear=True,):
        super(FixedText3_CL, self).update(clear=clear)
        self.show_bold = True
        self.color = 'CURSOR'
    def display(self):
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_editedCL3"))
        new_handlers = {
            curses.ascii.NL: self.switchForm
        }
        self.add_handlers(new_handlers)

    def switchForm(self, _input):
        self.parent.parentApp.CL = "Clean Bismark Mapper"
        self.parent.parentApp.switchForm('Clean_popup')

class FixedText4_CL(npyscreen.FixedText):
    def update(self, clear=True,):
        super(FixedText4_CL, self).update(clear=clear)
        self.show_bold = True
        self.color = 'CURSOR'
    def display(self):
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_editedCL4"))
        new_handlers = {
            curses.ascii.NL: self.switchForm
        }
        self.add_handlers(new_handlers)

    def switchForm(self, _input):
        self.parent.parentApp.CL = "Clean QC-Bam report"
        self.parent.parentApp.switchForm('Clean_popup')

class FixedText5_CL(npyscreen.FixedText):
    def update(self, clear=True,):
        super(FixedText5_CL, self).update(clear=clear)
        self.show_bold = True
        self.color = 'CURSOR'
    def display(self):
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_editedCL5"))
        new_handlers = {
            curses.ascii.NL: self.switchForm
        }
        self.add_handlers(new_handlers)

    def switchForm(self, _input):
        self.parent.parentApp.CL = "Clean Bismark-deduplicate"
        self.parent.parentApp.switchForm('Clean_popup')

class FixedText6_CL(npyscreen.FixedText):
    def update(self, clear=True,):
        super(FixedText6_CL, self).update(clear=clear)
        self.show_bold = True
        self.color = 'CURSOR'
    def display(self):
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_editedCL6"))
        new_handlers = {
            curses.ascii.NL: self.switchForm
        }
        self.add_handlers(new_handlers)

    def switchForm(self, _input):
        self.parent.parentApp.CL = "Clean Bismark Meth. Extractor"
        self.parent.parentApp.switchForm('Clean_popup')

class FixedText7_CL(npyscreen.FixedText):
    def update(self, clear=True,):
        super(FixedText7_CL, self).update(clear=clear)
        self.show_bold = True
        self.color = 'CURSOR'
    def display(self):
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_editedCL7"))
        new_handlers = {
            curses.ascii.NL: self.switchForm
        }
        self.add_handlers(new_handlers)

    def switchForm(self, _input):
        self.parent.parentApp.CL = "Clean CX reports"
        self.parent.parentApp.switchForm('Clean_popup')

class FixedText8_CL(npyscreen.FixedText):
    def update(self, clear=True,):
        super(FixedText8_CL, self).update(clear=clear)
        self.show_bold = True
        self.color = 'CURSOR'
    def display(self):
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_editedCL8"))
        new_handlers = {
            curses.ascii.NL: self.switchForm
        }
        self.add_handlers(new_handlers)

    def switchForm(self, _input):
        self.parent.parentApp.CL = "Clean Methimpute"
        self.parent.parentApp.switchForm('Clean_popup')

class FixedText9_CL(npyscreen.FixedText):
    def update(self, clear=True,):
        super(FixedText9_CL, self).update(clear=clear)
        self.show_bold = True
        self.color = 'CURSOR'
    def display(self):
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_editedCL9"))
        new_handlers = {
            curses.ascii.NL: self.switchForm
        }
        self.add_handlers(new_handlers)

    def switchForm(self, _input):
        self.parent.parentApp.CL = "Clean DMR"
        self.parent.parentApp.switchForm('Clean_popup')


class FixedText10_CL(npyscreen.FixedText):
    def update(self, clear=True,):
        super(FixedText10_CL, self).update(clear=clear)
        self.show_bold = True
        self.color = 'CURSOR'
    def display(self):
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_editedCL10"))
        new_handlers = {
            curses.ascii.NL: self.switchForm
        }
        self.add_handlers(new_handlers)

    def switchForm(self, _input):
        self.parent.parentApp.CL = "Clean Meth-bedgraph"
        self.parent.parentApp.switchForm('Clean_popup')

class FixedText11_CL(npyscreen.FixedText):
    def update(self, clear=True,):
        super(FixedText11_CL, self).update(clear=clear)
        self.show_bold = True
        self.color = 'CURSOR'
    def display(self):
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_editedCL11"))
        new_handlers = {
            curses.ascii.NL: self.switchForm
        }
        self.add_handlers(new_handlers)

    def switchForm(self, _input):
        self.parent.parentApp.CL = "Clean methylkit"
        self.parent.parentApp.switchForm('Clean_popup')

class FixedText12_CL(npyscreen.FixedText):
    def update(self, clear=True,):
        super(FixedText12_CL, self).update(clear=clear)
        self.show_bold = True
        self.color = 'CURSOR'
    def display(self):
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_editedCL12"))
        new_handlers = {
            curses.ascii.NL: self.switchForm
        }
        self.add_handlers(new_handlers)

    def switchForm(self, _input):
        self.parent.parentApp.CL = "Clean bigwig"
        self.parent.parentApp.switchForm('Clean_popup')



class InputBoxInfoCL_popup(CustomMultiLineEdit_CL):
    #_contained_widget = CustomMultiLineEdit_CL
    def update(self, clear=True,):
        super(InputBoxInfoCL_popup, self).update(clear=clear)
        self.color = 'CURSOR'



class noButton(npyscreen.FixedText):
    def update(self, clear=True):
        super(noButton, self).update(clear=clear)
        #self.show_bold = True
        self.color = 'CURSOR'
    def display(self):
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_edited_CL_popup"))
    def set_up_handlers(self):
        super(noButton, self).set_up_handlers()
        self.handlers.update({
                           curses.ascii.NL: self.just_exit
                           })

    def just_exit(self, _input):
        self.parent.parentApp.CL = "Unset"
        self.parent.parentApp.switchForm("Clean_directories")


class Clean_popup(npyscreen.FormBaseNew):
    DEFAULT_LINES      = 13
    DEFAULT_COLUMNS    = 60
    SHOW_ATX           = 10
    SHOW_ATY           = 2


    def create(self):
        self.add_event_hander("event_value_edited_CL_popup", self.event_value_edited_CL_popup)

        y, x = self.useable_space()

        self.InputBoxInfoCL_popup = self.add(InputBoxInfoCL_popup, name="Information", editable=False, max_height=2)


        self.add(npyscreen.FixedText, value= "", editable=False)
        self.yesButton = self.add(yesButton, value="Yes")
        self.noButton = self.add(noButton, value="No")


        new_handlers = {
            #Set ctrl+Q to exit
            "^Q": self.exit_func
        }
        self.add_handlers(new_handlers)
        
        self.display()



    def event_value_edited_CL_popup(self, event):
        userQuestion = "Are you sure you want to " + str(self.parentApp.CL) +"?"
        self.InputBoxInfoCL_popup.value = userQuestion
        self.InputBoxInfoCL_popup.display()

        self.display()



    def exit_func(self, _input):
        exit(0)



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

def read_config(section, get_string):
    config = GrumpyConfigParser()
    config.optionxform = str
    config.read('config/pipeline.conf')
    val_str = config.get(section, get_string)
    return val_str



class CleanFiles(npyscreen.FormBaseNew):
    # def afterEditing(self):
    #     self.parentApp.setNextForm(None)
        
    def create(self):


        self.add_event_hander("event_value_editedCL0", self.event_value_editedCL0)
        self.add_event_hander("event_value_editedCL1", self.event_value_editedCL1)
        self.add_event_hander("event_value_editedCL2", self.event_value_editedCL2)
        self.add_event_hander("event_value_editedCL3", self.event_value_editedCL3)
        self.add_event_hander("event_value_editedCL4", self.event_value_editedCL4)
        self.add_event_hander("event_value_editedCL5", self.event_value_editedCL5)
        self.add_event_hander("event_value_editedCL6", self.event_value_editedCL6)
        self.add_event_hander("event_value_editedCL7", self.event_value_editedCL7)
        self.add_event_hander("event_value_editedCL8", self.event_value_editedCL8)
        self.add_event_hander("event_value_editedCL9", self.event_value_editedCL9)
        self.add_event_hander("event_value_editedCL10", self.event_value_editedCL10)
        self.add_event_hander("event_value_editedCL11", self.event_value_editedCL11)
        self.add_event_hander("event_value_editedCL12", self.event_value_editedCL12)
        self.add_event_hander("event_value_edited_ok_clean_directories", self.event_value_edited_ok_clean_directories)
        self.add_event_hander("event_value_edited_ok_clean_directories_pressed", self.event_value_edited_ok_clean_directories_pressed)

        self.FixedText0_CL = self.add(FixedText0_CL, value= "", editable= True, rely=1)
        self.add(FixedText1_CL, value = "Clean Trimmomatic Directory")
        self.add(FixedText2_CL, value = "Clean Qc-fasq-report Directory")
        self.add(FixedText3_CL, value = "Clean bismark mapper Directory")
        self.add(FixedText4_CL, value = "Clean qc-bam report Directory")
        self.add(FixedText5_CL, value = "Clean Bsmark deduplicate Directory")
        self.add(FixedText6_CL, value = "Clean Bismark Meth. Extractor Directory")
        self.add(FixedText7_CL, value = "Clean Cx reports Directory")
        self.add(FixedText8_CL, value = "Clean Methimpute Directory")
        self.add(FixedText9_CL, value = "Clean DMR Directory")
        self.add(FixedText10_CL, value = "Clean meth-bedgraph Directory")
        self.add(FixedText11_CL, value = "Clean methylkit Directory")
        self.add(FixedText12_CL, value = "Clean bigwig Directory")

        y, x = self.useable_space()
                                                
        new_handlers = {
            #Set ctrl+Q to exit
            "^Q": self.exit_func
        }
        self.add_handlers(new_handlers)

        self.InputBoxInfoCL = self.add(InputBoxInfoCL, name="Information", editable=False, max_height=y // 2, rely=16)

        self.OK_Button_clean_directories = self.add(OK_Button_clean_directories, name="OK", relx=-12, rely=-3)



        self.display()


    def event_value_editedCL0(self, event):
        self.FixedText0_CL.editing = 0
        self.FixedText0_CL.how_exited = True

    def event_value_editedCL1(self, event):

        try:
            DIR1 = read_config("GENERAL", "result_pipeline")+"/trimmomatic-files"
            trim_files1 = len([name for name in os.listdir(DIR1) if os.path.isfile(os.path.join(DIR1, name))])

            DIR2 = read_config("GENERAL", "result_pipeline")+"/trimmomatic-logs"
            trim_files2 = len([name for name in os.listdir(DIR2) if os.path.isfile(os.path.join(DIR2, name))])

            total_trim_files = trim_files1 + trim_files2
        except OSError as e:
            total_trim_files = 0

        self.InputBoxInfoCL.value = "Number of files in Trimommatic Directories (2 directories in total): " + str(total_trim_files)
        self.InputBoxInfoCL.display()
        self.display()
        self.FixedText0_CL.editable = False

    def event_value_editedCL2(self, event):
        try:
            DIR = read_config("GENERAL", "result_pipeline")+"/qc-fastq-reports"
            Qc_fasq_files = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
        except OSError as e:
            Qc_fasq_files = 0

        self.InputBoxInfoCL.value = "Number of files in Qc_fasq Directory: " + str(Qc_fasq_files)
        self.InputBoxInfoCL.display()
        self.display()

    def event_value_editedCL3(self, event):
        try:
            DIR = read_config("GENERAL", "result_pipeline")+"/bismark-mappers"
            bismark_mapper_files = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
        except OSError as e:
            bismark_mapper_files = 0

        self.InputBoxInfoCL.value = "Number of files in bismark_mapper Directory: " + str(bismark_mapper_files)
        self.InputBoxInfoCL.display()
        self.display()

    def event_value_editedCL4(self, event):
        try:
            DIR = read_config("GENERAL", "result_pipeline")+"/qc-bam-reports"
            qc_bam_files = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
        except OSError as e:
            qc_bam_files = 0

        self.InputBoxInfoCL.value = "Number of files in qc_bam Directory: " + str(qc_bam_files)
        self.InputBoxInfoCL.display()
        self.display()

    def event_value_editedCL5(self, event):
        try:
            DIR = read_config("GENERAL", "result_pipeline")+"/bismark-deduplicate"
            bismark_deduplicate_files = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
        except OSError as e:
            bismark_deduplicate_files = 0

        self.InputBoxInfoCL.value = "Number of files in bismark_deduplicate Directory: " + str(bismark_deduplicate_files)
        self.InputBoxInfoCL.display()
        self.display()

    def event_value_editedCL6(self, event):
        try:
            DIR = read_config("GENERAL", "result_pipeline")+"/bismark-meth-extractor"
            bismark_meth_files = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
        except OSError as e:
            bismark_meth_files = 0

        self.InputBoxInfoCL.value = "Number of files in bismark_meth Directory: " + str(bismark_meth_files)
        self.InputBoxInfoCL.display()
        self.display()

    def event_value_editedCL7(self, event):
        try:
            DIR = read_config("GENERAL", "result_pipeline")+"/cx-reports"
            cx_reports_files = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
        except OSError as e:
            cx_reports_files = 0

        self.InputBoxInfoCL.value = "Number of files in cx_reports Directory: " + str(cx_reports_files)
        self.InputBoxInfoCL.display()
        self.display()

    def event_value_editedCL8(self, event):
        try:
            DIR1 = read_config("GENERAL", "result_pipeline")+"/methimpute-out"
            methimpute_files1 = len([name for name in os.listdir(DIR1) if os.path.isfile(os.path.join(DIR1, name))])

            DIR2 = read_config("GENERAL", "result_pipeline")+"/tes-reports"
            methimpute_files2 = len([name for name in os.listdir(DIR2) if os.path.isfile(os.path.join(DIR2, name))])

            DIR3 = read_config("GENERAL", "result_pipeline")+"/gen-reports"
            methimpute_files3 = len([name for name in os.listdir(DIR3) if os.path.isfile(os.path.join(DIR3, name))])

            DIR4 = read_config("GENERAL", "result_pipeline")+"/fit-reports"
            methimpute_files4 = len([name for name in os.listdir(DIR4) if os.path.isfile(os.path.join(DIR4, name))])
        except OSError as e:
            total_methimpute_files = 0

        total_methimpute_files = methimpute_files1 + methimpute_files2 + methimpute_files3 + methimpute_files4
        self.InputBoxInfoCL.value = "Number of files in Methimpute Directories (4 directories in total): " + str(total_methimpute_files)
        self.InputBoxInfoCL.display()
        self.display()


    def event_value_editedCL9(self, event):
        try:
            DIR = read_config("GENERAL", "result_pipeline")+"/dmrcaller-format"
            dmr_files = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
        except OSError as e:
            dmr_files = 0

        self.InputBoxInfoCL.value = "Number of files in DMR Directory: " + str(dmr_files)
        self.InputBoxInfoCL.display()
        self.display()


    def event_value_editedCL10(self, event):
        try:
            DIR = read_config("GENERAL", "result_pipeline")+"/bedgraph-fromat"
            meth_bedgraph_files = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])

        except OSError as e:
            meth_bedgraph_files = 0

        self.InputBoxInfoCL.value = "Number of files in meth_bedgraph Directory: " + str(meth_bedgraph_files)
        self.InputBoxInfoCL.display()
        self.display()

    def event_value_editedCL11(self, event):
        try:
            DIR = read_config("GENERAL", "result_pipeline")+"/methylkit-format"
            methylkit_files = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])

        except OSError as e:
            methylkit_files = 0

        self.InputBoxInfoCL.value = "Number of files in methylkit Directory: " + str(methylkit_files)
        self.InputBoxInfoCL.display()
        self.display()

    def event_value_editedCL12(self, event):
        try:
            DIR = read_config("GENERAL", "result_pipeline")+"/bigwig-fromat"
            bigwig_files = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])

        except OSError as e:
            bigwig_files = 0

        self.InputBoxInfoCL.value = "Number of files in bigwig Directory: " + str(bigwig_files)
        self.InputBoxInfoCL.display()
        self.display()




    def event_value_edited_ok_clean_directories(self, event):
        self.InputBoxInfoCL.value = "Proceed back to the main form."
        self.InputBoxInfoCL.display()
        self.display()

    def event_value_edited_ok_clean_directories_pressed(self, event):
        self.parentApp.switchForm("MAIN")
        self.editw = 0


    def on_cancel(self):
        self.parentApp.setNextForm("MAIN")

    def exit_func(self, _input):
        exit(0)