from langchain.agents import create_agent
from tools import TOOLS
from prompts import AGENT_PROMPT
from hashing_password import generate_session_id, verify_password, hashing_password
from llm import gemini3_8_flash, gpt_oss_120b, gpt_oss_20b, gemini3_7_flash, local_qwen2_5_coder_latest, \
    gemini3_5_flash, llama_3_1_8b, openrouter_qwen_3_8, openrouter_apodex_1_1_mini
from langgraph.checkpoint.postgres import PostgresSaver
from pydantic import BaseModel, Field
from typing import Literal
from db_conn import get_database
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
import os


class AgentResponse(BaseModel):
    answer: str = Field(description="Foydalanuvchiga beriladigan javob")
    chart_type: Literal["bar", "line", "pie", "none"]
    data: list[dict] = Field(default_factory=list)
    sql: str | None = None
    file_name: str = Field(description="Actual generated filename. Empty string if no file was created.")


llm_with_output = gemini3_8_flash.with_structured_output(AgentResponse)


def chat_agent(request: str, database_url: str, session_id: str):
    with PostgresSaver.from_conn_string(os.environ.get("DB_URL_AGENT")) as checkpoint:
        checkpoint.setup()

        sql_toolkit = SQLDatabaseToolkit(
            db=get_database(database_url),
            llm=local_qwen2_5_coder_latest
        )
        sql_tools = sql_toolkit.get_tools()
        agent = create_agent(model=openrouter_apodex_1_1_mini, system_prompt=AGENT_PROMPT, tools=TOOLS + sql_tools,
                             checkpointer=checkpoint)

        response = agent.invoke({"messages": [{"role": "user", "content": f"{request}"}]},
                                config={"configurable": {"thread_id": session_id}})
        # print(100*"-")
        # print(response['messages'][-1].content)
        # print(100*"-")
        structed_response = llm_with_output.invoke(response['messages'][-1].content)
        return structed_response


def get_chat_history(session_id: str, ):
    config = {"configurable": {"thread_id": session_id}}
    with PostgresSaver.from_conn_string(
            conn_string=os.environ.get("DB_URL_AGENT")) as checkpoint:
        agent = create_agent(model=openrouter_apodex_1_1_mini, system_prompt=AGENT_PROMPT, tools=TOOLS,
                             checkpointer=checkpoint)
        state = agent.get_state(config)
        return state.values['messages']
