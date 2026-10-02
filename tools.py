from langchain_community.agent_toolkits.file_management.toolkit import FileManagementToolkit
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine, text, URL
from sqlalchemy.exc import SQLAlchemyError
from llm import qwen_3_8_27b, local_qwen2_5_coder_latest, local_qwen3_8b, gpt_oss_20b
import os

file_toolkit = FileManagementToolkit(
    root_dir="creating_files"
)
file_tools = file_toolkit.get_tools()
TOOLS = file_tools
