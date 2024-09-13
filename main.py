import streamlit as st
import pymysql
import pandas as pd
import plotly.express as px

TABLE_NAME = "donate_transactions"

# Database connection
connection = pymysql.connect(**st.secrets.db_credentials)
cursor = connection.cursor()

# App title
st.title("Search Transactions")

tab1, tab2 = st.tabs(["Search Transactions", "Credit Chart"])

with tab1:
    st.subheader("Search Transactions by Content")

    # User input
    search_text = st.text_input("Enter text to search in transactions:")

    # Query and display results only if there is input
    if search_text:
        query = f"SELECT * FROM {TABLE_NAME} WHERE content LIKE %s"
        cursor.execute(query, (f"%{search_text}%",))  # Use SQL parameterized queries to prevent SQL injection
        results = cursor.fetchall()

        # Check if any results are found
        if results:
            # Convert results into a pandas DataFrame
            df = pd.DataFrame(results, columns=["transaction_date", "credit", "content", "transaction_code"])
            
            # Display matching transactions
            st.write(f"Found {len(results)} matching transactions:")
            st.dataframe(df)
        else:
            st.write("No transactions found matching your search.")


with tab2:
    st.subheader("Credit Chart")

    query = f"SELECT credit FROM {TABLE_NAME}"
    cursor.execute(query)
    chart_data = cursor.fetchall()

    # Convert chart data into a pandas DataFrame
    df_chart = pd.DataFrame(chart_data, columns=["credit"])

    # Define the bins and labels for credit amounts
    bins = [0, 10000, 20000, 50000, 100000, 200000, 500000, 1000000, 5000000, 10000000, 50000000, 100000000, 500000000, 1000000000]
    labels = ["(1, 10k)", "[10k, 20k]", "[20k, 50k]", "[50k, 100k]", "[100k, 200k]", "[200k, 500k]", "[500k, 1M]", "[1M, 5M]", "[5M, 10M]", "[10M, 50M]", "[50M, 100M]", "[100M, 500M]", "[500M, 1B]"]

    # Categorize credit amounts into bins
    df_chart['credit_category'] = pd.cut(df_chart['credit'], bins=bins, labels=labels)

    # Count the occurrences in each bin
    credit_distribution = df_chart['credit_category'].value_counts().sort_index()

    # Convert to DataFrame for plotting
    df_distribution = pd.DataFrame({'Credit Range': credit_distribution.index, 'Count': credit_distribution.values})

    # Plot the distribution
    fig = px.bar(df_distribution, x='Credit Range', y='Count', title="Distribution of Credit Amounts",
                labels={"Credit Range": "Amount", "Count": "Number of Transactions"})

    st.plotly_chart(fig)
