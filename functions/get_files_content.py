import os
from config import MAX_CHARS

def get_files_content(working_directory: str, file_path) -> str:
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path=  os.path.abspath(os.path.join(working_directory, file_path))  
    print(abs_file_path)
    if not abs_file_path.lower().startswith(abs_working_dir.lower()):
        return f'Error: Access denied. "{file_path}" is outside the working directory.'
    if not os.path.exists(abs_file_path):
        return f'Error: "{file_path}" does not exist.'
    if  not os.path.isfile(abs_file_path): 
        return f'Error: "{file_path}" is not a file.'
    file_content_string=""
    try:
        with open(abs_file_path,"r", encoding="utf-8") as f:
            file_content_string = f.read(MAX_CHARS+1)
            if len(file_content_string)>MAX_CHARS:
                file_content_string = file_content_string[:MAX_CHARS] + f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters...]'
        return file_content_string
    except Exception as e:
        return f"Exception reading file: {e}"