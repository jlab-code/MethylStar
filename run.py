import imp
import sys
import os
def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)


def main_run():
    try:
        import importlib
        from pip import main
    except:
        from pip._internal import main

    try:
        imp.find_module('npyscreen')
        found = True
    except ImportError:
        found = False


    try:
        if not found:
            main(['install', "--user", "npyscreen"])
            restart_program()
    except Exception as e:
        logging.error(traceback.format_exc())

    from src.py.main import App

    MyApp = App()
    MyApp.run()

# Main Program
if __name__ == "__main__":
    # Launch main menu
    main_run()