from langchain_community.agent_toolkits.file_management.toolkit import FileManagementToolkit

file_toolkit = FileManagementToolkit(
    root_dir="creating_files"
)
file_tools = file_toolkit.get_tools()
TOOLS = file_tools
