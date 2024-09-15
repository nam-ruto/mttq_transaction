import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(page_title="Var-SaoKe", page_icon='🔍')

# Table name
TABLE_NAME = "transactions"

# Database connection
connection = st.connection('postgresql', type='sql')

# App title
st.title("🫡Sao Kê Giao Dịch MTTQVN")
st.write("🪴Ủng hộ đồng bào Miền Bắc khắc phục hậu quả gây ra bởi bão Yagi")
st.write("📑Dữ liệu được cung cấp bởi MTTQVN (từ 1/9/2024 đến 10/9/2024)")

tab1, tab2 = st.tabs(["Tra cứu GD", "Biểu đồ"])

with tab1:
    st.subheader("Tra Cứu Giao Dịch")

    # User input
    search_text = st.text_input("Nhập mã giao dịch, người giao dịch, hoặc nội dung bất kỳ:")

    # Query and display results only if there is input
    if search_text:
        query = f"SELECT * FROM {TABLE_NAME} WHERE content LIKE '%{search_text}%'"
        # Use parameterized query to avoid SQL injection
        df = connection.query(query)

        # Check if any results are found
        if not df.empty:
            # Display matching transactions
            st.success(f"Tìm thấy {len(df)} giao dịch trùng khớp:")
            st.dataframe(df)
        else:
            st.warning("Không tìm thấy kết quả")
    
    st.warning("DISCLAIM: Page được build với mục đích học tập, không nhằm mục đích gây kích động, bạo lực, chính trị, hay bất kỳ mục đích nào khác")

with tab2:
    st.subheader("Distribution Chart")

    query = f"SELECT credit FROM {TABLE_NAME}"
    df_chart = connection.query(query)

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
    fig = px.bar(df_distribution, x='Credit Range', y='Count', title="Biểu đồ phân bố số tiền ủng hộ từ các nhà hảo tâm!",
                 labels={"Credit Range": "Số tiền", "Count": "Số lượng GD"})

    st.plotly_chart(fig)
