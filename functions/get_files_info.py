import os

def get_files_info(working_directory: str, directory=".") -> str:
    abs_working_dir = os.path.abspath(working_directory)    
    if directory is None:
        abs_directory = abs_working_dir
    else:
        if not os.path.isabs(directory):
            directory = os.path.join(working_directory, directory)
        abs_directory = os.path.abspath(directory)
    if not abs_directory.lower().startswith(abs_working_dir.lower()):
        return f'Error: Access denied. "{directory}" is outside the working directory.'
    if not os.path.exists(abs_directory):
        return f'Error: "{directory}" does not exist.'
    if not os.path.isdir(abs_directory):
        return f'Error: "{directory}" is a file, not a directory.'
    final_response = ""
    try:
        contents = os.listdir(abs_directory)
        print("contents:",contents)
        for content in contents:
            content_path = os.path.join(abs_directory, content)
            is_dir = os.path.isdir(content_path)
            size = os.path.getsize(content_path)
            # Thêm \n để xuống dòng cho từng file
            final_response += f"- {content}: file_size={size} bytes, is_dir={is_dir}\n"
    except Exception as e:
        return f"Error reading directory: {e}"
        
    return final_response