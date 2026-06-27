import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="E-Commerce Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# ======================
# LOAD DATA
# ======================

@st.cache_data
def load_data():
    df = pd.read_csv("ecommerce_sales_data.csv")

    df["TransactionDate"] = pd.to_datetime(df["TransactionDate"])

    df["Revenue"] = (
        df["Quantity"] *
        df["Price"] *
        (1 - df["Discount"]/100)
    )

    return df

df = load_data()

# ======================
# SIDEBAR
# ======================

st.sidebar.title("Dashboard Navigation")

page = st.sidebar.radio(
    "Select Page",
    [
        "Overview",
        "Customer Analytics",
        "Product Analytics",
        "Location Analytics",
        "Advanced Insights"
    ]
)

# ======================
# KPI
# ======================

total_revenue = df["Revenue"].sum()
total_orders = len(df)
avg_order = df["Revenue"].mean()
avg_discount = df["Discount"].mean()
avg_loyalty = df["CustomerLoyaltyScore"].mean()
unique_customers = df["CustomerID"].nunique()

# ======================
# OVERVIEW
# ======================

if page == "Overview":

    st.title("📊 E-Commerce Sales Dashboard")

    c1,c2,c3 = st.columns(3)

    c1.metric("Revenue", f"${total_revenue:,.0f}")
    c2.metric("Orders", total_orders)
    c3.metric("Customers", unique_customers)

    c4,c5,c6 = st.columns(3)

    c4.metric("Avg Order", f"${avg_order:.2f}")
    c5.metric("Avg Discount", f"{avg_discount:.2f}%")
    c6.metric("Loyalty Score", f"{avg_loyalty:.2f}")

    monthly = (
        df.groupby(
            df["TransactionDate"].dt.month_name()
        )["Revenue"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        monthly,
        x="TransactionDate",
        y="Revenue",
        markers=True,
        title="Monthly Revenue Trend"
    )

    st.plotly_chart(fig, use_container_width=True)

# ======================
# CUSTOMER ANALYTICS
# ======================

elif page == "Customer Analytics":

    st.title("👥 Customer Analytics")

    fig = px.histogram(
        df,
        x="CustomerAge",
        nbins=20,
        title="Age Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

    gender = df["CustomerGender"].value_counts()

    fig = px.pie(
        values=gender.values,
        names=gender.index,
        title="Gender Distribution"
    )

    st.plotly_chart(fig)

    income = (
        df.groupby("CustomerIncomeGroup")
        ["Revenue"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        income,
        x="CustomerIncomeGroup",
        y="Revenue",
        title="Revenue by Income Group"
    )

    st.plotly_chart(fig)

# ======================
# PRODUCT ANALYTICS
# ======================

elif page == "Product Analytics":

    st.title("📦 Product Analytics")

    category = (
        df.groupby("ProductCategory")
        ["Revenue"]
        .sum()
        .reset_index()
        .sort_values(
            by="Revenue",
            ascending=False
        )
    )

    fig = px.bar(
        category,
        x="ProductCategory",
        y="Revenue",
        color="Revenue"
    )

    st.plotly_chart(fig, use_container_width=True)

# ======================
# LOCATION ANALYTICS
# ======================

elif page == "Location Analytics":

    st.title("🌍 Location Analytics")

    location = (
        df.groupby("CustomerLocation")
        ["Revenue"]
        .sum()
        .reset_index()
        .sort_values(
            by="Revenue",
            ascending=False
        )
        .head(10)
    )

    fig = px.bar(
        location,
        x="CustomerLocation",
        y="Revenue",
        color="Revenue"
    )

    st.plotly_chart(fig, use_container_width=True)

# ======================
# ADVANCED INSIGHTS
# ======================

elif page == "Advanced Insights":

    st.title("📈 Advanced Insights")

    sample = df.sample(5000)

    fig = px.scatter(
        sample,
        x="CustomerLoyaltyScore",
        y="Revenue",
        color="CustomerIncomeGroup",
        title="Loyalty vs Revenue"
    )

    st.plotly_chart(fig)

    corr = df[
        [
            "Quantity",
            "Price",
            "Discount",
            "CustomerAge",
            "CustomerLoyaltyScore",
            "Revenue"
        ]
    ].corr()

    fig, ax = plt.subplots(figsize=(10,6))

    sns.heatmap(
        corr,
        annot=True,
        cmap="coolwarm",
        ax=ax
    )

    st.pyplot(fig)