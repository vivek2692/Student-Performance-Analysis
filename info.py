import streamlit as st
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

def app():

    st.title("Student Information")

    df = pd.read_excel("./2017_Batch.xlsx")

    # Input field for the roll number
    roll_number = st.text_input("Enter Enrollment Number:")

    if roll_number:
        try:
            roll_number = int(roll_number)
            st.write(f"You entered Enrollment Number: {roll_number}")
        except ValueError:
            st.error("Invalid input. Please enter a valid integer.")

    # Display the entered roll number
    if roll_number:
        # st.write(f"You entered Roll Number: {roll_number}")

        df = df[df["STUDENT'S COLLEGE ID"] == roll_number]
        df = df.T
        st.dataframe(df, height=550, width=1350)

        # st.markdown('<style>div.dvn-scroller{width:}</style>', unsafe_allow_html=True)
        # st.markdown('<style>div.glideDataEditor{width:850px; height:543px; cursor:default;}</style>', unsafe_allow_html=True)
        # st.markdown('<style>div.css-17b7mgn{width:850px; height:543px; cursor:default;}</style>', unsafe_allow_html=True)