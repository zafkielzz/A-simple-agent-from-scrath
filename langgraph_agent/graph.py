import os
import sys
from dotenv import load_dotenv

# Thêm đường dẫn cha vào sys.path để có thể import thư mục functions/ ở ngoài
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.tools import tool

# Import các hàm Python thực tế (Core logic không đổi)
from functions.get_files_info import get_files_info
from functions.get_files_content import get_files_content
from functions.write_files import write_file
from functions.run_python_file import run_python_file

load_dotenv()
api_key = os.environ.get("DEEPSEEK_API_KEY")

# 1. Khởi tạo LLM thông qua Langchain (Rất chuẩn xác và ngắn gọn)
llm = ChatOpenAI(
    model="deepseek-chat", 
    api_key=api_key, 
    base_url="https://api.deepseek.com",
    max_tokens=1024
)

# 2. Định nghĩa các Tool bằng decorator @tool của Langchain
# NHỜ CÓ @tool, CHÚNG TA KHÔNG CẦN VIẾT JSON SCHEMA BẰNG TAY NỮA! Langchain sẽ tự động đọc tham số của hàm và biến thành JSON Schema.
@tool
def get_files_info_tool(directory: str = "calculator") -> str:
    """Lists files in a specified directory relative to the working directory, providing file size and directory status"""
    return get_files_info(directory)

@tool
def get_files_content_tool(file_path: str) -> str:
    """Read the content of a file in the calculator directory"""
    return get_files_content(working_directory="calculator", file_path=file_path)

@tool
def write_file_tool(file_path: str, content: str) -> str:
    """Create a file with the specified content in the calculator directory"""
    return write_file(working_directory="calculator", file_path=file_path, content=content)

@tool
def run_python_file_tool(file_path: str, args: list = None) -> str:
    """Run a python file in the calculator directory and return its output"""
    return run_python_file(working_directory="calculator", file_path=file_path, args=args)

# Gộp các tool thành 1 danh sách
tools = [get_files_info_tool, get_files_content_tool, write_file_tool, run_python_file_tool]

# Khởi tạo bộ nhớ (Checkpointer)
memory = MemorySaver()

# 3. Khởi tạo Agent bằng LangGraph
# Truyền checkpointer=memory để LangGraph tự động ghi nhớ lịch sử hội thoại
agent_executor = create_react_agent(llm, tools, checkpointer=memory)

def main():
    print("🤖 LangGraph Agent đã sẵn sàng! (Nhập 'quit' để thoát)")
    
    # Vòng lặp này chỉ để chat liên tục với user, không phải vòng lặp function calling!
    while True:
        try:
            user_input = input("\nBạn: ")
            if user_input.lower() in ["quit", "exit", "q"]:
                break
                
            # Khởi chạy Graph
            # Cần cung cấp config chứa thread_id để định danh cuộc hội thoại
            config = {"configurable": {"thread_id": "1"}}
            
            for event in agent_executor.stream(
                {"messages": [("user", user_input)]},
                config=config,
                stream_mode="values"
            ):
                latest_msg = event["messages"][-1]
                role = latest_msg.type 
                
                # Nếu là AI trả lời bằng văn bản
                if role == "ai" and latest_msg.content:
                    print(f"\n🧠 AI Trả lời: {latest_msg.content}")
                    
                # Nếu AI yêu cầu gọi tool
                elif role == "ai" and latest_msg.tool_calls:
                    for t in latest_msg.tool_calls:
                        print(f"\n⚙️ [AI Yêu cầu Tool]: Gọi '{t['name']}' với tham số {t['args']}")
                        
                # Nếu là kết quả trả về từ tool
                elif role == "tool":
                    print(f"\n✅ [Kết quả Tool '{latest_msg.name}']: \n{latest_msg.content}")
                    
        except Exception as e:
            print(f"Lỗi: {e}")

if __name__ == "__main__":
    main()
