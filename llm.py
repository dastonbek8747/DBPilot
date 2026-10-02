from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

gpt_oss_120b = ChatGroq(
    api_key=GROQ_API_KEY,
    model="openai/gpt-oss-120b"
)
gpt_oss_20b = ChatGroq(
    api_key=GROQ_API_KEY,
    model="openai/gpt-oss-20b"
)
qwen_3_8_27b = ChatGroq(
    api_key=GROQ_API_KEY,
    model="qwen/qwen3.8-27b"
)
llama_3_1_8b = ChatGroq(
    api_key=GROQ_API_KEY,
    model="llama-3.1-8b-instant"
)
llama_3_3_70b = ChatGroq(
    api_key=GROQ_API_KEY,
    model="llama-3.3-70b-versatile"
)

gemini3_8_flash = ChatGoogleGenerativeAI(
    api_key=GEMINI_API_KEY,
    model="gemini-3.8-flash"
)
gemini3_7_flash = ChatGoogleGenerativeAI(
    api_key=GEMINI_API_KEY,
    model="gemini-3.7-flash"
)
gemini3_5_flash = ChatGoogleGenerativeAI(
    api_key=GEMINI_API_KEY,
    model="gemini-3.5-flash-lite"
)
local_qwen2_5_coder_latest = ChatOllama(
    model="qwen2.5-coder:latest"
)
local_qwen3_8b = ChatOllama(
    model="qwen3:8b"
)
