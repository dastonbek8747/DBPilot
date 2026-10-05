import time
import requests
import streamlit as st
from streamlit import session_state
import pandas as pd
import plotly.express as px

if "db_url" not in st.session_state:
    st.session_state.db_url = ""
if "db_conn" not in st.session_state:
    st.session_state.db_conn = False

if "register" not in st.session_state:
    st.session_state.register = False


def write_stream(text):
    for i in text:
        time.sleep(0.003)
        yield i


driver_name = ""

if st.session_state.register:

    with st.sidebar:
        st.title("Database Connection")
        database_type = st.selectbox("Database Type", ["PostgreSQL", "SQLite", "MySQL"])
        if database_type == "PostgreSQL":
            driver_name = "postgresql+psycopg2"
        elif database_type == "SQLite":
            driver_name = "sqlite"
        elif database_type == "MySQL":
            driver_name = "mysql+pymysql"
        db_name = st.sidebar.text_input("Database Name", placeholder="database name")
        db_user = st.sidebar.text_input("Database User", placeholder="username")
        db_password = st.sidebar.text_input("Database Password", placeholder="password")
        db_host = st.sidebar.text_input("Database Host", placeholder="localhost")
        db_port = st.sidebar.text_input("Database Port", placeholder="port : 5432")

        connection = st.button("Connect")
        # st.subheader(f"DB NAME {db_name}, USER {db_user}, PASSWORD {db_password}, HOST {db_host}, PORT {db_port},Driver name")
        if connection:
            response = requests.post(url="http://localhost:8000/check_db",
                                     json={"db_name": db_name, "db_user": db_user, "db_password": db_password,
                                           "db_host": db_host, "db_port": db_port, "driver_name": driver_name})
            # st.success(response.json())
            if response.json()['messages']['db_conn']:
                st.session_state.db_conn = True
                st.session_state.db_url = f"{driver_name}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

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
            st.divider()
            with st.chat_message("assistant"):
                response = requests.post(url="http://localhost:8000/chat_agent",
                                         json={"session_id": st.session_state.session_id, "request": user_request,
                                               "database_url": st.session_state.db_url})
                # st.info(response)
                st.markdown(response.json()['answer'])
                if response.json()['chart_type'] == "bar":
                    st.bar_chart(response.json()['data'])
                elif response.json()['chart_type'] == "line":
                    st.line_chart(response.json()['data'])
                elif response.json()['chart_type'] == "pie":
                    df = pd.DataFrame(response.json()['data'])

                    fig = px.pie(
                        df,
                        names="category",
                        values="value"
                    )

                    st.plotly_chart(fig, use_container_width=True)
                # if response.json()['sql'] != "None":
                #     st.info(response.json()["sql"])
                if response.json()['file_name'] != "":
                    st.link_button(label="Downloading file",
                                   url=f"http://localhost:8000/creating_files/{response.json()['file_name']}")

            st.divider()
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
        submit_sing_in = st.button("Sign Up", icon="🔑")
        if submit_sing_in:
            response = requests.post(url="http://localhost:8000/signin",
                                     json={"username": username, "email": email, "password": password})
            st.success(response.json())

            if response.json()['message'] == "User created successfully":
                st.session_state.session_id = response.json()['user']['session_id']
                st.session_state.register = True
                time.sleep(3)
                st.rerun()
            else:
                st.markdown("Sign Up failed" + f"{response}")
    with tab2:
        st.subheader("Login")
        email_login = st.text_input("Email", key="login_username", type="email")
        password_login = st.text_input("Password", key="login_password", type="password")
        submit = st.button("Login", icon="🔐")
        if submit:
            response = requests.post(url="http://localhost:8000/login",
                                     json={"email": email_login, "password": password_login})
            st.success(response.json())
            time.sleep(3)
            if response.json()['message'] == "Login successful":
                st.success(response.json())
                st.session_state.session_id = response.json()['user']['session_id']
                st.session_state.register = True
                st.rerun()
            else:
                st.markdown("Login failed" + f"{response}")
