import npyscreen

class FixedText1_jbrowser(npyscreen.FixedText):
    def update(self, clear=True,):
        super(FixedText1_jbrowser, self).update(clear=clear)
        self.show_bold = True
        self.color = 'CURSOR'

class FixedText2_jbrowser(npyscreen.FixedText):
    def update(self, clear=True,):
        super(FixedText2_jbrowser, self).update(clear=clear)
        self.show_bold = True
        self.color = 'CURSOR'

class JBrowser(npyscreen.ActionFormV2):
    # def afterEditing(self):
    #     self.parentApp.setNextForm(None)

    def create_control_buttons(self):
        self._add_button('ok_button', 
                        self.__class__.OKBUTTON_TYPE, 
                        self.__class__.OK_BUTTON_TEXT,
                        0 - self.__class__.OK_BUTTON_BR_OFFSET[0],
                        0 - self.__class__.OK_BUTTON_BR_OFFSET[1] - len(self.__class__.OK_BUTTON_TEXT),
                        None
                        )

    def create(self):
        self.add(npyscreen.FixedText, value= "", editable=False)
        self.add(FixedText1_jbrowser, value = "JBrowse", rely=2)
        self.add(FixedText2_jbrowser, value = "All plots")

        new_handlers = {
            # Set ctrl+Q to exit
            "^Q": self.exit_func,
        }
        self.add_handlers(new_handlers)

    def on_ok(self):
        self.parentApp.setNextForm("MAIN")

    def exit_func(self, _input):
        exit(0)