import time

import streamlit as st
from streamlit import session_state

from ai_models import chat_agent
from db_conn import check_conn_db

if "db_url" not in st.session_state:
    st.session_state.db_url = ""
if "db_conn" not in st.session_state:
    st.session_state.db_conn = False

if "register" not in st.session_state:
    st.session_state.register = True


def write_stream(text):
    for i in text:
        time.sleep(0.003)
        yield i


if st.session_state.register:

    with st.sidebar:
        st.title("Database Connection")

        db_name = st.sidebar.text_input("Database Name", placeholder="database name")
        db_user = st.sidebar.text_input("Database User", placeholder="username")
        db_password = st.sidebar.text_input("Database Password", placeholder="password")
        db_host = st.sidebar.text_input("Database Host", placeholder="localhost")
        db_port = st.sidebar.text_input("Database Port", placeholder="port : 5432")

        connection = st.button("Connect")
        if connection:
            response_conn = check_conn_db(db_password=db_password, db_host=db_host, db_name=db_name, db_user=db_user,
                                          db_port=db_port)
            st.session_state.db_url = response_conn['db_url']
            st.session_state.db_conn = response_conn['db_conn']
        if st.session_state.db_conn:
            st.success("🟢 Database Connected")
        else:
            st.warning("🔴 Database Disconnected")
        # file = st.file_uploader("Upload file 📁")
    if session_state.db_conn:
        st.title("Database Connection With AI Agent")
        st.subheader("Database Connection With AI Agent")
        user_request = st.chat_input(placeholder="Enter your request here")

        if user_request:
            with st.chat_message("user"):
                st.markdown(user_request)
            with st.chat_message("assistant"):
                response = chat_agent(user_request)["messages"][-1].content[0]['text']
                st.write_stream(write_stream(response))
                # if response.chart_type == "bar":
                #     st.bar_chart(response['data'])
                # elif response.chart_type == "line":
                #     st.line_chart(response['data'])
                # elif response.chart_type == "pie":
                #     st.bar_chart(response['data'])
    else:
        st.write_stream(
            write_stream("🧐🧐🧐 Could not connect to the database!\nPlease check the database settings!🧐🧐🧐"))
else:
    tab1, tab2 = st.tabs(["Sign in", "Login"])
    with tab1:
        st.title("Sign Up")
        username = st.text_input("Username", key="sing_up_username")
        email = st.text_input("Email", key="sing_up_email", type="email")
        password = st.text_input("Password", key="sing_up_password", type="password")
        submit = st.button("Sign Up", icon="🔑")
    with tab2:
        st.subheader("Login")
        username_login = st.text_input("Username", key="login_username")
        password_login = st.text_input("Password", key="login_password", type="password")
        submit = st.button("Login", icon="🔐")
