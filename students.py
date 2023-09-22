import streamlit as st
import pandas as pd

def app():

    data = pd.read_excel("./2017_Batch.xlsx")

    # Define the number of rows to display per page
    rows_per_page = st.slider('Rows per Page', min_value=1, max_value=100, value=50)

    # Get the current page number from the user
    current_page = st.number_input('Current Page', min_value=1, value=1)

    # Calculate the start and end indices for the current page
    start_idx = (current_page - 1) * rows_per_page
    end_idx = start_idx + rows_per_page

    # Display the data for the current page
    st.title('All Students')
    st.dataframe(data.iloc[start_idx:end_idx], height = 700,width = 1350)
    st.markdown(
    """
    <style>
    .dataframe { width: 1000px; }
    </style>
    """,
    unsafe_allow_html=True
    )

    # Calculate the total number of pages
    total_pages = len(data) // rows_per_page + (len(data) % rows_per_page > 0)

    # Display pagination information
    st.write(f'Page {current_page} of {total_pages}')

    # Store the current page in the session state
    st.session_state.current_page = current_page