import os
import sys
from dotenv import load_dotenv
from openai import OpenAI
from functions.get_files_info import get_files_info
from functions.get_files_content import get_files_content
from functions.write_files import write_file
from functions.run_python_file import run_python_file
from tools import ALL_TOOLS
import json
# Thiết lập encoding cho stdout trên Windows để in được Tiếng Việt / Emoji không bị lỗi
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

# Đọc lịch sử chat
HISTORY_FILE = "history.json"
system_prompt = "Bạn là trợ lý ảo hỗ trợ lập trình chuyên nghiệp. Bạn có quyền truy cập vào các công cụ để xem thư mục, đọc file, viết file và chạy file Python để giải quyết yêu cầu."

if os.path.exists(HISTORY_FILE):
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            messages = json.load(f)
    except json.JSONDecodeError:
        messages = []
else:
    messages = []

# Đảm bảo phần tử đầu tiên trong messages luôn là System Prompt
if not messages or messages[0].get("role") != "system":
    messages.insert(0, {"role": "system", "content": system_prompt})

# Ánh xạ tên hàm sang hàm Python thực tế
FUNCTION_MAP = {
    "get_files_info": get_files_info,
    "get_files_content": get_files_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
}

def execute_tool(name: str, args: dict) -> str:
    func = FUNCTION_MAP.get(name)
    if not func:
        return f"Error: Function {name} not found."
    
    # Luôn thiết lập working_directory là "calculator"
    args["working_directory"] = "calculator"
        
    try:
        return func(**args)
    except Exception as e:
        return f"Error executing {name}: {e}"

def main():
    load_dotenv()
    api_key = os.environ.get("DEEPSEEK_API_KEY")

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com"
    )
    if len(sys.argv) < 2: 
        sys.exit(1)
        
    verbose_flag = False
    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        verbose_flag = True
        
    prompt = sys.argv[1]
    messages.append({"role": "user", "content": prompt})
    
    # Vòng lặp gọi API và thực thi tool (Function Calling Loop)
    while True:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            tools=ALL_TOOLS,
            tool_choice="auto"
        )
        
        assistant_message = response.choices[0].message
        
        # In câu trả lời của AI nếu có nội dung văn bản
        if assistant_message.content:
            print(assistant_message.content)
            
        # Chuyển đổi đối tượng ChatCompletionMessage sang dict trước khi lưu vào lịch sử
        assistant_message_dict = assistant_message.model_dump(exclude_none=True)
        messages.append(assistant_message_dict)
        
        # Nếu AI không yêu cầu gọi thêm tool nào nữa, kết thúc vòng lặp
        if not assistant_message.tool_calls:
            break
            
        # Thực thi lần lượt từng tool được yêu cầu
        for tool_call in assistant_message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            if verbose_flag:
                print(f"\n[Verbose] AI requested tool: {function_name}({function_args})")
                
            # Chạy hàm thực tế
            result = execute_tool(function_name, function_args)
            
            # Thêm kết quả của tool vào lịch sử chat
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": function_name,
                "content": result
            })

    if verbose_flag and response.usage:
        print("\n--- Token Usage ---")
        print(f"Prompt tokens (Input): {response.usage.prompt_tokens}")
        print(f"Completion tokens (Output): {response.usage.completion_tokens}")
        print(f"Total tokens: {response.usage.total_tokens}")
        
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=4, ensure_ascii=False)

print(get_files_info("calculator"))
if __name__ == "__main__":
    main()