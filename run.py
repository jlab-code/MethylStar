import imp
import sys
import os
import subprocess
import shutil
import pwd

def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)

def get_username():
    return pwd.getpwuid( os.getuid() )[ 0 ]

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

    ToNULL = open(os.devnull, 'w')
    try:
        detected_parallel_location = subprocess.check_output(['which', 'parallel'])
    except subprocess.CalledProcessError:
        #subprocess.Popen(["nohup", './src/bash/ins_parallel.sh', " > /dev/null 2>&1"], stdout=ToNULL, stderr=subprocess.STDOUT)
        user=get_username()
        subprocess.call(["cp", "./src/bash/ins_parallel.sh", '/home/'+user+'/'])
        subprocess.call(['chmod', '0755', '/home/'+user+'/ins_parallel.sh'])
        subprocess.call(['sh','/home/'+user+'/ins_parallel.sh'])
        os.remove('/home/'+user+'/ins_parallel.sh')

    try:
        os.remove('/home/'+user+'/parallel-20190122.tar.bz2')
        os.remove('/home/'+user+'/parallel-20190122.tar.bz2.sig')
        shutil.rmtree('/home/'+user+'/parallel-20190122')
        shutil.rmtree('/home/'+user+'/share')
    except Exception as e:
        pass

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
