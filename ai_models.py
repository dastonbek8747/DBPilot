from langchain.agents import create_agent
from tools import TOOLS
from prompts import AGENT_PROMPT
from hashing_password import generate_session_id, verify_password, hashing_password
from llm import gemini3_8_flash, gpt_oss_120b, gpt_oss_20b, gemini3_7_flash, local_qwen2_5_coder_latest, \
    gemini3_5_flash, llama_3_1_8b
from langgraph.checkpoint.postgres import PostgresSaver
from pydantic import BaseModel
from typing import Literal
from db_conn import get_database
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
import os


class AgentResponse(BaseModel):
    answer: str
    chart_type: Literal["bar", "line", "pie", "none"]
    data: list[dict]
    sql: str | None = None


def chat_agent(request: str, database_url: str, session_id: str):
    with PostgresSaver.from_conn_string(os.environ.get("DB_URL_AGENT")) as checkpoint:
        checkpoint.setup()

        sql_toolkit = SQLDatabaseToolkit(
            db=get_database(database_url),
            llm=local_qwen2_5_coder_latest
        )
        sql_tools = sql_toolkit.get_tools()
        agent = create_agent(model=gemini3_5_flash, system_prompt=AGENT_PROMPT, tools=TOOLS + sql_tools,
                             checkpointer=checkpoint)

        response = agent.invoke({"messages": [{"role": "user", "content": f"{request}"}]},
                                config={"configurable": {"thread_id": session_id}})

        return response['messages'][-1].content[0]['text']


def get_chat_history(session_id: str, ):
    config = {"configurable": {"thread_id": session_id}}
    with PostgresSaver.from_conn_string(
            conn_string=os.environ.get("DB_URL_AGENT")) as checkpoint:
        agent = create_agent(model=gemini3_5_flash, system_prompt=AGENT_PROMPT, tools=TOOLS, checkpointer=checkpoint)
        state = agent.get_state(config)
        return state.values['messages']
