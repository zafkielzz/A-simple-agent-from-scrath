from functions.get_files_info import get_files_info
from functions.get_files_content import get_files_content
from functions.write_files import write_file
from functions.run_python_file import run_python_file
def main():
    working_dir= "calculator"
    print(run_python_file(working_dir,"asdad.py",["3 + 5"]))
    
   
main()