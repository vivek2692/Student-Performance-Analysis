import streamlit as st
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import io
import warnings
warnings.filterwarnings('ignore')

def app():
    # st.set_page_config(page_title="Dashboard", page_icon=":bar_chart:", layout="wide")

    st.title(" :bar_chart: Student Performance Analysis")
    st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

    df = pd.read_excel("./2017_Batch.xlsx")

    st.sidebar.header("Choose Your Filter : ")

    # Create for Department
    dept = st.sidebar.multiselect("Choose Department", df["DEPARTMENT (ABBR.)"].unique())

    if not dept:
        df2 = df.copy()
    else:
        df2 = df[df["DEPARTMENT (ABBR.)"].isin(dept)]

    # Create for Board
    board = st.sidebar.multiselect("Choose Class XII Board", df2["NAME OF BOARD/COUNCIL - CLASS XII"].unique())

    if not board:
        df3 = df2.copy()
    else:
        df3 = df2[df2["NAME OF BOARD/COUNCIL - CLASS XII"].isin(board)]

    # Create for State
    state = st.sidebar.multiselect("Choose State", df3["PERMANENT LOCATION (STATE)"].unique())

    # if not board:
    #     df4 = df3.copy()
    # else:
    #     df4 = df3[df3["PERMANENT LOCATION (STATE)"].isin(state)]
    # dept, board, state
    # regi, state, city

    if not dept and not board and not state:
        filtered_df = df
    elif not board and not state:
        filtered_df = df[df["DEPARTMENT (ABBR.)"].isin(dept)]
    elif not dept and not state:
        filtered_df = df[df["NAME OF BOARD/COUNCIL - CLASS XII"].isin(board)]
    elif board and state:
        filtered_df = df3[df["NAME OF BOARD/COUNCIL - CLASS XII"].isin(board) & df3["PERMANENT LOCATION (STATE)"].isin(state)]
    elif dept and state:
        filtered_df = df3[df["DEPARTMENT (ABBR.)"].isin(dept) & df3["PERMANENT LOCATION (STATE)"].isin(state)]
    elif dept and board:
        filtered_df = df3[df["DEPARTMENT (ABBR.)"].isin(dept) & df3["NAME OF BOARD/COUNCIL - CLASS XII"].isin(board)]
    elif state:
        filtered_df = df3[df3["PERMANENT LOCATION (STATE)"].isin(state)]
    else:
        filtered_df =  df3[df3["DEPARTMENT (ABBR.)"].isin(dept) & df3["NAME OF BOARD/COUNCIL - CLASS XII"].isin(board) & df3["PERMANENT LOCATION (STATE)"].isin(state)]

    # filtered_df = df4

    col1, col2 = st.columns((2))

    department_df = df.groupby(by = ["DEPARTMENT (ABBR.)"], as_index = False)["SL.NO."].count()
    department_df.columns = ["Department", "No. of Students"]

    with col1:
        st.subheader("Department Wise Students")
        fig = px.bar(department_df, x = "Department", y = "No. of Students", text = ['{:,d}'.format(x) for x in department_df["No. of Students"]],template="seaborn")
        st.plotly_chart(fig, use_container_width=True, height=200)

    gender_df = filtered_df.groupby(by = ["GENDER (M/F)"], as_index = False)["SL.NO."].count()
    gender_df.columns = ["Gender", "Count"]

    # print(gender_df)

    with col2:
        st.subheader("Gender Wise Students")
        # fig = px.pie(gender_df, names="Gender", values="Count", hole = 0.5)
        # fig.update_traces(text = gender_df["Gender"], textposition="outside")
        fig = px.pie(gender_df, names="Gender", values="Count", hole=0.5)
        fig.update_traces(text=gender_df["Gender"], textposition="outside")

        # Display the pie chart using Streamlit
        st.plotly_chart(fig, use_container_width=True)

    cl1, cl2 = st.columns((2))

    excel_writer = pd.ExcelWriter(
        'output_data.xlsx',
        engine='xlsxwriter',  # Engine for writing (xlsxwriter or openpyxl)
        mode='w',             # Write mode (w for new file, a for append)
        options={'strings_to_numbers': True}  # Engine-specific options
    )

    with cl1:
        with st.expander("Department_ViewData"):
            st.write(department_df.style.background_gradient(cmap="Blues"))
            excel_file_path = "Department-wise students.xlsx"
            excel_file = io.BytesIO()
            department_df.to_excel(excel_file, index=False)
            st.download_button(label="Download Department Data", key="download_data", data=excel_file, file_name="Department-wise students.xlsx")
            # st.download_button(label="Download Department Data", key="download_data", on_click=None, args=(excel_file_path,))
            # st.download_button("Download Data", label="Download Department Data", key="download_data", on_click=None, args=(excel_file_path,))
            # excel = department_df.to_excel(index=False, excel_writer=excel_writer)
            # st.download_button("Download Data", data = excel, file_name = "Department-wise students.xlsx")

    with cl2:
        with st.expander("Gender_ViewData"):
            st.write(gender_df.style.background_gradient(cmap="Oranges"))
            excel_file_path = "Gender-wise students.xlsx"
            excel_file = io.BytesIO()
            gender_df.to_excel(excel_file, index=False)
            st.download_button(label="Download Gender Data", key="download_gender_data", data=excel_file, file_name="Gender-wise students.xlsx")
            # st.write(gender_df.style.background_gradient(cmap="Oranges"))
            # excel = gender_df.to_excel(index=False,excel_writer=excel_writer)
            # st.download_button("Download Data", data = excel, file_name = "Gender-wise students.xlsx")




    if not dept:
        st.subheader("Department Wise Highest CGPA")

        linechart = pd.DataFrame(filtered_df.groupby(filtered_df["DEPARTMENT (ABBR.)"])["SEM AVG"].max()).reset_index()
        linechart['SEM AVG'] = linechart['SEM AVG'].round(2)

        column_name_mapping = {
            'DEPARTMENT (ABBR.)': 'Department',
            'SEM AVG': 'Highest CGPA'
        }

        linechart.rename(columns=column_name_mapping, inplace=True)
        # print(linechart)

        fig2 = px.line(linechart, x = "Department", y = "Highest CGPA", height=500, width=1000,template="gridon")
        st.plotly_chart(fig2, use_container_width=True)

        with st.expander("View Data of Highest CGPA"):
            st.write(linechart.T.style.background_gradient(cmap="Blues"))
            excel_file = io.BytesIO()
            linechart.to_excel(excel_file, index=False, float_format="%.2f")
            st.download_button(label="Download CGPA Data", key="download_cgpa_data", data=excel_file, file_name="Department Wise Highest CGPA.xlsx")

    else:
        st.subheader("Department Wise CGPA")
        linechart = pd.DataFrame(df[df["DEPARTMENT (ABBR.)"].isin(dept)][["STUDENT'S COLLEGE ID", "SEM AVG"]]).reset_index()
        # print(linechart)
        # linechart = pd.DataFrame(filtered_df.groupby(filtered_df["DEPARTMENT (ABBR.)"])["SEM AVG"].max()).reset_index()
        linechart['SEM AVG'] = linechart['SEM AVG'].round(2)

        column_name_mapping = {
            "STUDENT'S COLLEGE ID": 'Enrollment No.',
            'SEM AVG': 'CGPA'
        }

        linechart.rename(columns=column_name_mapping, inplace=True)
        # print(linechart)

        linechart = linechart.drop('index', axis=1)

        fig2 = px.line(linechart, x = "Enrollment No.", y = "CGPA",height=500, width=2000,template="gridon")
        fig2.update_xaxes(
        tickvals=df["STUDENT'S COLLEGE ID"],  # Use the original Enrollment No. values as tick values
        ticktext=df["STUDENT'S COLLEGE ID"].astype(str),  # Convert to string for tick labels
        type='category',  # Use category type for x-axis
        tickangle=90
        )   
        fig2.update_layout(
        autosize=True,          # Automatically adjust the chart size
        width=1500              # Set a width for the chart (you can adjust this based on your needs)
        )
        st.plotly_chart(fig2, use_container_width=True)

        with st.expander("View Data of CGPA"):
            st.write(linechart.T.style.background_gradient(cmap="Blues"))
            excel_file = io.BytesIO()
            linechart.to_excel(excel_file, index=False, float_format="%.2f")
            st.download_button(label="Download Department CGPA Data", key="download_dept_cgpa_data", data=excel_file, file_name="Department Wise CGPA.xlsx")







    # toppers = df.groupby('DEPARTMENT (ABBR.)')['SEM AVG'].transform(max) == df['SEM AVG']

    # print(df[toppers][['DEPARTMENT (ABBR.)', 'SEM AVG','ACTUAL % OF CLASS XII','NAME OF BOARD/COUNCIL - CLASS XII']])

    highest_avg_df = df.loc[df.groupby('DEPARTMENT (ABBR.)')['SEM AVG'].idxmax()]
    # print("Hiii")
    highest_avg_df = highest_avg_df[["DEPARTMENT (ABBR.)","SEM 1", "SEM 2", "SEM 3", "SEM 4", "SEM 5", "SEM AVG"]]
    # print(highest_avg_df)

    color=['#81c784','#0288d1','#0288d1','#9575cd','#f44336','#ffb74d','#6d4c41','#f50057']

    st.title('Changes in grades of the toppers over time')
    st.subheader('Semester-wise Grades')

    fig = go.Figure()

    for i, c in zip(range(len(highest_avg_df)), color):
        department_data = highest_avg_df.iloc[i]
        department_name = department_data['DEPARTMENT (ABBR.)']
        sem_grades = department_data[['SEM 1', 'SEM 2', 'SEM 3', 'SEM 4', 'SEM 5']]

        fig.add_trace(go.Scatter(
            x=['SEM 1', 'SEM 2', 'SEM 3', 'SEM 4', 'SEM 5'],
            y=sem_grades,
            mode='lines',
            line=dict(color=c, width=3),
            name=department_name
        ))

    fig.update_layout(
        xaxis_title='Semesters',
        yaxis_title='Grades',
        # legend=dict(x=500, y=-0.2),
        width=1000,
        height=600
    )

    st.plotly_chart(fig)










    new_df = filtered_df[["STUDENT'S COLLEGE ID", "DEPARTMENT (ABBR.)", "STANDARD % OF CLASS X", "STANDARD % OF CLASS XII", "SEM 1", "SEM 2", "SEM 3", "SEM 4", "SEM 5", "SEM AVG", "CORE TECHNICAL STRENGTH"]]
    # print(new_df.head())
    new_df["STUDENT'S COLLEGE ID"] = new_df["STUDENT'S COLLEGE ID"].round(0)

    column_name_mapping2 = {
        'DEPARTMENT (ABBR.)': 'Department',
        "STUDENT'S COLLEGE ID": 'Enrollment No.',
        "STANDARD % OF CLASS X": "Class 10 Percentage",
        "STANDARD % OF CLASS XII": "Class 12 Percentage",
    }

    new_df.rename(columns=column_name_mapping2, inplace=True)

    with st.expander("View Students Data"):
        st.write(new_df[:50].style.background_gradient(cmap="Oranges"))
        excel_file = io.BytesIO()
        new_df.to_excel(excel_file, index=False, float_format="%.2f")
        st.download_button(label="Download Students Data", key="download_students_data", data=excel_file, file_name="Students Data.xlsx")


    colum1, colum2 = st.columns((2))

    df['IF YES, MENTION NUMBER OF BACKLOG(S)'] = pd.to_numeric(df['IF YES, MENTION NUMBER OF BACKLOG(S)'], errors='coerce')

    students_with_backlogs = df[df['IF YES, MENTION NUMBER OF BACKLOG(S)'] > 0]

    department_backlog_counts = students_with_backlogs.groupby('DEPARTMENT (ABBR.)')['IF YES, MENTION NUMBER OF BACKLOG(S)'].count().reset_index()

    department_backlog_counts.columns = ["Department", "No. of Backlogs"]

    # print(department_backlog_counts)

    with colum1:
        st.subheader("Department Wise Students having Backlogs")
        fig = px.bar(department_backlog_counts, x = "Department", y = "No. of Backlogs", text = ['{:,d}'.format(x) for x in department_backlog_counts["No. of Backlogs"]],template="seaborn")
        st.plotly_chart(fig, use_container_width=True, height=200)


    if not dept :

        back_count = students_with_backlogs.groupby(by = ["IF YES, MENTION NUMBER OF BACKLOG(S)"], as_index = False)["SL.NO."].count()
        back_count.columns = ["Backlog", "Count"]   

        with colum2:
            st.subheader("Backlog Wise Students")
            # fig = px.pie(gender_df, names="Gender", values="Count", hole = 0.5)
            # fig.update_traces(text = gender_df["Gender"], textposition="outside")
            fig7 = px.pie(back_count, names="Backlog", values="Count", hole=0.5)
            fig7.update_traces(text=back_count["Backlog"], textinfo="label+value", textposition="outside")

            # Display the pie chart using Streamlit
            st.plotly_chart(fig7, use_container_width=True)

    else:
        students_with_backlogs = students_with_backlogs[students_with_backlogs["DEPARTMENT (ABBR.)"].isin(dept)]
        back_count2 = students_with_backlogs.groupby(["DEPARTMENT (ABBR.)", "IF YES, MENTION NUMBER OF BACKLOG(S)"]).size().reset_index(name="Count")
        back_count2.columns = ["Department", "Backlog", "Count"]   

        # print(back_count)

        with colum2:
            st.subheader("Backlog Wise Students in Department")
            # fig = px.pie(gender_df, names="Gender", values="Count", hole = 0.5)
            # fig.update_traces(text = gender_df["Gender"], textposition="outside")
            fig8 = px.pie(back_count2, names="Backlog", values="Count", hole=0.5)
            fig8.update_traces(text=back_count2["Backlog"], textinfo="label+value", textposition="outside")

            # Display the pie chart using Streamlit
            st.plotly_chart(fig8, use_container_width=True)
