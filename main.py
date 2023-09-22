import streamlit as st
from streamlit_option_menu import option_menu
import dashboard, students, info

st.set_page_config(page_title="Dashboard", page_icon=":bar_chart:", layout="wide")

class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, function):
        self.apps.append({
            "title": title,
            "function": function
        })

    def run():
        with st.sidebar:
            app = option_menu(
                menu_title = "Dashboard",
                options = ["Home", "Students", "Info"],
                icons = ["house-fill", "person-circle", "info-circle-fill"],
                menu_icon = "chat-text-fill",
                default_index = 0
            )

        if app == "Home":
            dashboard.app()
        if app == "Students":
            students.app()
        if app == "Info":
            info.app()

    run()