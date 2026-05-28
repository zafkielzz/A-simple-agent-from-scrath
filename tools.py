# tools.py

tool_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                }
            }
        }
    }
}

tool_get_files_content = {
    "type": "function",
    "function": {
        "name": "get_files_content",
        "description": "Reads and returns the content of a specified file relative to the working directory, truncated if it exceeds maximum limits",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the file to read, relative to the working directory"
                }
            },
            "required": ["file_path"]
        }
    }
}

tool_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes text content to a specified file relative to the working directory, creating any missing parent directories automatically",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the file to write, relative to the working directory"
                },
                "content": {
                    "type": "string",
                    "description": "The text content to write into the file"
                }
            },
            "required": ["file_path", "content"]
        }
    }
}

tool_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs a specified Python file within a working directory, passing arguments if provided",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the Python file to run, relative to the working directory"
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional arguments to pass to the Python file"
                }
            },
            "required": ["file_path"]
        }
    }
}

# Gom tất cả các tool lại thành một danh sách để truyền vào API OpenAI
ALL_TOOLS = [
    tool_get_files_info,
    tool_get_files_content,
    tool_write_file,
    tool_run_python_file
]
