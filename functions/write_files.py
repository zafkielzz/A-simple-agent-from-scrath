import os

def write_file(working_directory: str, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path=  os.path.abspath(os.path.join(working_directory, file_path))  
    if not abs_file_path.lower().startswith(abs_working_dir.lower()):
        return f'Error: Access denied. "{file_path}" is outside the working directory.'
    parent_dir= os.path.dirname(abs_file_path)
    if not os.path.isdir(parent_dir):
        try:
            os.makedirs(parent_dir)
        except Exception as e:
            return f"Could not create parent dirs: {parent_dir} = {e}" 
    try:
        with open(abs_file_path,"w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully wrote to {file_path} ({len(content)}) characters"
    except Exception as e :
        return f"Failed to write to {file_path}, {e}"