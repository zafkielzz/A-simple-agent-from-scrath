import os
import subprocess
import sys

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))  
    if not abs_file_path.lower().startswith(abs_working_dir.lower()):
        return f'Error: Access denied. "{file_path}" is outside the working directory.'
    if not os.path.isfile(abs_file_path):
        return f'Error: {file_path} is not a file'
    if not file_path.endswith(".py"):
        return f'Error: {file_path} is not a Python file'   
    try:
        cmd = [sys.executable, file_path]
        if args:
            cmd.extend(args)
        output = subprocess.run(
            cmd,
            cwd=abs_working_dir,
            capture_output=True,
            text=True,
            timeout=30
        )
        final_string= f"""
STDOUT: {output.stdout}
STDERR: {output.stderr or 'None'}
"""
        if output.stdout == "" and output.stderr=="":
            final_string= "No output proceed. \n"
        if not output.returncode ==0:
            final_string += f"Process exited with code  {output.returncode}"
        return final_string
    
    except Exception as e:
        return f'Error: Executing Python file : {e}'
    