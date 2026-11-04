
import streamlit as st
import pandas as pd
import numpy as np

# 1. Page configuration
st.set_page_config(
    page_title="Streamlit Learning App",
    page_icon="🚀",
    layout="wide"
)

# 2. Main heading
st.title("🚀 My First Streamlit App")
st.write("Learn Streamlit by building interactive features.")

# 3. Sidebar navigation
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Choose a page",
    ["Home", "Widgets", "Data Dashboard", "CSV Upload", "Counter"]
)

# 4. Home page
if page == "Home":
    st.header("Welcome to Streamlit!")

    st.markdown("""
    ### What can Streamlit do?
    - Build interactive web applications
    - Create data science dashboards
    - Visualize datasets
    - Build AI/ML interfaces
    """)

    name = st.text_input("Enter your name")

    if st.button("Say Hello"):
        if name.strip():
            st.success(f"Hello {name}! Welcome to Streamlit.")
        else:
            st.warning("Please enter your name.")

# 5. Widgets page
elif page == "Widgets":
    st.header("Learn Streamlit Widgets")

    age = st.slider("Select your age", 1, 100, 25)

    language = st.selectbox(
        "Choose your programming language",
        ["Python", "Java", "JavaScript", "Go"]
    )

    experience = st.radio(
        "Your experience level",
        ["Beginner", "Intermediate", "Advanced"]
    )

    agree = st.checkbox("I want to learn Streamlit")

    st.write("Your age:", age)
    st.write("Language:", language)
    st.write("Experience:", experience)

    if agree:
        st.success("Great! Keep learning.")

# 6. Data dashboard
elif page == "Data Dashboard":
    st.header("Interactive Data Dashboard")

    rows = st.slider("Number of records", 5, 100, 20)

    # Reproducible sample data
    rng = np.random.default_rng(42)

    df = pd.DataFrame({
        "Sales": rng.integers(100, 1000, rows),
        "Profit": rng.integers(10, 300, rows)
    })

    st.subheader("Dataset")
    st.dataframe(df)

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Sales", int(df["Sales"].sum()))

    with col2:
        st.metric("Total Profit", int(df["Profit"].sum()))

    st.subheader("Line Chart")
    st.line_chart(df)

    st.subheader("Bar Chart")
    st.bar_chart(df)

# 7. CSV upload
elif page == "CSV Upload":
    st.header("CSV File Analyzer")

    uploaded_file = st.file_uploader(
        "Upload a CSV file",
        type=["csv"]
    )

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)

            st.success("File uploaded successfully!")

            st.subheader("Preview")
            st.dataframe(df.head(20))

            st.write("Rows:", df.shape[0])
            st.write("Columns:", df.shape[1])

            st.subheader("Statistical Summary")
            st.dataframe(df.describe(include="all"))

            numeric_columns = df.select_dtypes(
                include="number"
            ).columns.tolist()

            if numeric_columns:
                selected_column = st.selectbox(
                    "Select column for chart",
                    numeric_columns
                )

                st.line_chart(df[selected_column])
            else:
                st.info("No numeric columns available.")

        except Exception as e:
            st.error(f"Could not read CSV: {e}")

# 8. Session state counter
elif page == "Counter":
    st.header("Session State Example")

    if "count" not in st.session_state:
        st.session_state.count = 0

    st.metric("Current Count", st.session_state.count)

    if st.button("Increment"):
        st.session_state.count += 1
        st.rerun()

    if st.button("Reset"):
        st.session_state.count = 0
        st.rerun()
