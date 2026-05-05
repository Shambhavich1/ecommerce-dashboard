import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

st.markdown("<h2 style='text-align: center;'>📊 E-Commerce Sales Dashboard</h2>", unsafe_allow_html=True)
st.markdown("---")

st.markdown("Analyze sales performance and customer behavior")

@st.cache_data
def load_data():
    url = "https://drive.google.com/uc?id=1U3wVW3AVMVDcdDRteWc9DP79Asuvm0j1"
    df = pd.read_csv(url)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df = load_data()

#SIDEBAR FILTERS

st.sidebar.header("Filters")

start_date = st.sidebar.date_input("Start Date", df['Date'].min())
end_date = st.sidebar.date_input("End Date", df['Date'].max())

category = st.sidebar.multiselect("Category", df['Category'].unique())

filtered_df = df[
    (df['Date'] >= pd.to_datetime(start_date)) &
    (df['Date'] <= pd.to_datetime(end_date))
]

if category:
    filtered_df = filtered_df[filtered_df['Category'].isin(category)]

#KPI CARDS
     
total_revenue = filtered_df['Amount'].sum()
total_orders = filtered_df['Order ID'].count()
avg_order = filtered_df['Amount'].mean()

col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Revenue", f"{total_revenue:,.0f}")
col2.metric("📦 Total Orders", total_orders)
col3.metric("📊 Avg Order Value", f"{avg_order:.2f}")
col1, col2 = st.columns([2,1])

#Sales Trend
with col1:
    st.subheader("Monthly Sales Trend")

    daily_sales = filtered_df.groupby('Date')['Amount'].sum()

    fig, ax = plt.subplots(figsize = (8,3))
    ax.plot(daily_sales.index, daily_sales.values)
    plt.xlabel("Month")
    plt.ylabel("Revenue")

    st.pyplot(fig)

#CATEGORY WISE SALES
with col2:
    st.subheader("Top Categories")

    cat_sales = filtered_df.groupby('Category')['Amount'].sum().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize = (4,2))
    cat_sales.plot(kind='bar', ax=ax)

    st.pyplot(fig)


#Customer Segmentation
col3, col4 =  st.columns([3,1])

with col3:
    st.subheader("Customer Segmentation")

    filtered_df['Customer'] = (
        filtered_df['ship-city'].astype(str) + "_" +
        filtered_df['ship-state'].astype(str)
    )

    customer_data = filtered_df.groupby('Customer').agg({
        'Amount': 'sum',
        'Order ID': 'count'
    }).rename(columns={'Amount': 'Total_Spend', 'Order ID': 'Frequency'})

    fig, ax = plt.subplots(figsize=(4,2))
    ax.scatter(customer_data['Frequency'], customer_data['Total_Spend'])
    plt.xlabel("Number of Orders (Frequency)")
    plt.ylabel("Total Spending (Amount)")
    st.pyplot(fig)

#State-wise Sales

with col4:
    st.subheader("Top 10 States by Revenue")
    state_sales = filtered_df.groupby('ship-state')['Amount'].sum().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize = (4,2))
    state_sales.plot(kind='bar', ax=ax)
    plt.xlabel("State")
    plt.ylabel("Revenue")
    st.pyplot(fig)


st.subheader("Key Insights")

st.write("- Customers can be divided into high-value, frequent low spenders, and occasional high spenders.")
with st.expander("View Detailed Analysis"):
    st.write("-To retain High-value Customers.")
    st.write("-Frequent low spenders can be targeted for upselling.")
    st.write("-Occasional high spenders may require re-engagemenet strategies.")
st.write("- A small group of customers contributes a large portion of total revenue (High-Value Customers).")
st.write("- A few product categories generate the majority of revenue. ")
st.write("- There is a large segment of low-value customers that can be converted into high-value customers.")
st.write("- Sales are concentrated in specific states/cities. Target should be to focus on high-performing regions.")

st.write("Since the dataset lacks a unique customer ID, customer segmentation is approximated using location-based grouping.")
st.download_button(
    "Download Filtered Data",
    filtered_df.to_csv(index=False),
    "filtered_data.csv"
)
