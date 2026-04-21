"""
Interactive Streamlit Dashboard for Retail Sales EDA
Author: bishal531
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings

warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Retail Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load retail sales data"""
    df = pd.read_csv('data/retail_sales.csv')
    df['date'] = pd.to_datetime(df['date'])
    return df

@st.cache_data
def get_statistics(df):
    """Calculate key statistics"""
    return {
        'total_sales': df['total_sales'].sum(),
        'total_transactions': len(df),
        'avg_transaction': df['total_sales'].mean(),
        'total_quantity': df['quantity'].sum(),
        'num_stores': df['store_id'].nunique(),
        'num_customers': df['customer_age'].count(),
        'avg_customer_age': df['customer_age'].mean()
    }

# Load data
df = load_data()
stats = get_statistics(df)

# Sidebar filters
st.sidebar.title("🎛️ Filters")
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(df['date'].min(), df['date'].max()),
    min_value=df['date'].min(),
    max_value=df['date'].max()
)

selected_stores = st.sidebar.multiselect(
    "Select Stores",
    options=sorted(df['store_id'].unique()),
    default=sorted(df['store_id'].unique())
)

selected_categories = st.sidebar.multiselect(
    "Select Product Categories",
    options=df['product_category'].unique(),
    default=df['product_category'].unique()
)

selected_payment = st.sidebar.multiselect(
    "Select Payment Methods",
    options=df['payment_method'].unique(),
    default=df['payment_method'].unique()
)

# Apply filters
filtered_df = df[
    (df['date'].dt.date >= date_range[0]) &
    (df['date'].dt.date <= date_range[1]) &
    (df['store_id'].isin(selected_stores)) &
    (df['product_category'].isin(selected_categories)) &
    (df['payment_method'].isin(selected_payment))
]

# Main dashboard title
st.title("📊 Retail Sales Analytics Dashboard")
st.markdown("---")

# KPI Metrics Row 1
st.subheader("📈 Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Sales",
        f"${filtered_df['total_sales'].sum():,.2f}",
        f"{((filtered_df['total_sales'].sum() / stats['total_sales']) * 100):.1f}% of total"
    )

with col2:
    st.metric(
        "Total Transactions",
        f"{len(filtered_df):,}",
        f"{((len(filtered_df) / stats['total_transactions']) * 100):.1f}% of total"
    )

with col3:
    st.metric(
        "Average Transaction",
        f"${filtered_df['total_sales'].mean():,.2f}",
        f"${stats['avg_transaction']:,.2f} overall avg"
    )

with col4:
    st.metric(
        "Total Quantity Sold",
        f"{filtered_df['quantity'].sum():,}",
        f"Avg: {filtered_df['quantity'].mean():.1f} units"
    )

st.markdown("---")

# Row 2: Sales Trend and Category Distribution
col1, col2 = st.columns(2)

with col1:
    st.subheader("📅 Sales Trend Over Time")
    daily_sales = filtered_df.groupby(filtered_df['date'].dt.date)['total_sales'].sum().reset_index()
    daily_sales.columns = ['Date', 'Sales']
    
    fig_trend = px.line(
        daily_sales,
        x='Date',
        y='Sales',
        title='Daily Sales Trend',
        markers=True,
        color_discrete_sequence=['#1f77b4']
    )
    fig_trend.update_layout(
        hovermode='x unified',
        height=400,
        template='plotly_white'
    )
    st.plotly_chart(fig_trend, use_container_width=True)

with col2:
    st.subheader("🏷️ Sales by Product Category")
    category_sales = filtered_df.groupby('product_category')['total_sales'].sum().sort_values(ascending=False)
    
    fig_category = px.bar(
        x=category_sales.index,
        y=category_sales.values,
        title='Sales by Category',
        labels={'x': 'Category', 'y': 'Sales ($)'},
        color=category_sales.values,
        color_continuous_scale='Viridis'
    )
    fig_category.update_layout(height=400, template='plotly_white')
    st.plotly_chart(fig_category, use_container_width=True)

st.markdown("---")

# Row 3: Store Performance and Payment Methods
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏪 Sales by Store")
    store_sales = filtered_df.groupby('store_id').agg({
        'total_sales': 'sum',
        'quantity': 'sum'
    }).sort_values('total_sales', ascending=False)
    
    fig_store = px.bar(
        x=store_sales.index,
        y=store_sales['total_sales'],
        title='Sales by Store',
        labels={'x': 'Store ID', 'y': 'Sales ($)'},
        color=store_sales['total_sales'],
        color_continuous_scale='Blues'
    )
    fig_store.update_layout(height=400, template='plotly_white')
    st.plotly_chart(fig_store, use_container_width=True)

with col2:
    st.subheader("💳 Payment Method Distribution")
    payment_data = filtered_df['payment_method'].value_counts()
    
    fig_payment = px.pie(
        values=payment_data.values,
        names=payment_data.index,
        title='Transaction Distribution by Payment Method',
        hole=0.3
    )
    fig_payment.update_layout(height=400, template='plotly_white')
    st.plotly_chart(fig_payment, use_container_width=True)

st.markdown("---")

# Row 4: Customer Analysis
st.subheader("👥 Customer Analysis")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Average Customer Age",
        f"{filtered_df['customer_age'].mean():.1f} years",
        f"Range: {filtered_df['customer_age'].min()}-{filtered_df['customer_age'].max()}"
    )

with col2:
    gender_dist = filtered_df['customer_gender'].value_counts()
    male_pct = (gender_dist.get('M', 0) / len(filtered_df)) * 100
    st.metric(
        "Male Customers",
        f"{male_pct:.1f}%",
        f"{gender_dist.get('M', 0):,} transactions"
    )

with col3:
    female_pct = (gender_dist.get('F', 0) / len(filtered_df)) * 100
    st.metric(
        "Female Customers",
        f"{female_pct:.1f}%",
        f"{gender_dist.get('F', 0):,} transactions"
    )

col1, col2 = st.columns(2)

with col1:
    st.subheader("👥 Customer Age Distribution")
    fig_age = px.histogram(
        filtered_df,
        x='customer_age',
        nbins=20,
        title='Customer Age Distribution',
        labels={'customer_age': 'Age', 'count': 'Frequency'},
        color_discrete_sequence=['#ff6b6b']
    )
    fig_age.update_layout(height=400, template='plotly_white')
    st.plotly_chart(fig_age, use_container_width=True)

with col2:
    st.subheader("💰 Sales by Gender")
    gender_sales = filtered_df.groupby('customer_gender')['total_sales'].agg(['sum', 'mean', 'count'])
    
    fig_gender = px.bar(
        x=gender_sales.index,
        y=gender_sales['sum'],
        title='Total Sales by Gender',
        labels={'x': 'Gender', 'y': 'Sales ($)'},
        color=gender_sales['sum'],
        color_continuous_scale='RdYlGn'
    )
    fig_gender.update_layout(height=400, template='plotly_white')
    st.plotly_chart(fig_gender, use_container_width=True)

st.markdown("---")

# Row 5: Advanced Analytics
st.subheader("📊 Advanced Analytics")
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Quantity Sold by Category")
    category_qty = filtered_df.groupby('product_category')['quantity'].sum().sort_values(ascending=False)
    
    fig_qty = px.bar(
        x=category_qty.index,
        y=category_qty.values,
        title='Total Quantity Sold by Category',
        labels={'x': 'Category', 'y': 'Quantity'},
        color=category_qty.values,
        color_continuous_scale='Sunset'
    )
    fig_qty.update_layout(height=400, template='plotly_white')
    st.plotly_chart(fig_qty, use_container_width=True)

with col2:
    st.subheader("💵 Average Price by Category")
    avg_price = filtered_df.groupby('product_category')['unit_price'].mean().sort_values(ascending=False)
    
    fig_price = px.bar(
        x=avg_price.index,
        y=avg_price.values,
        title='Average Unit Price by Category',
        labels={'x': 'Category', 'y': 'Unit Price ($)'},
        color=avg_price.values,
        color_continuous_scale='Plasma'
    )
    fig_price.update_layout(height=400, template='plotly_white')
    st.plotly_chart(fig_price, use_container_width=True)

st.markdown("---")

# Summary Statistics
st.subheader("📋 Summary Statistics Table")
summary_stats = filtered_df.describe().T
st.dataframe(
    summary_stats,
    use_container_width=True,
    height=300
)

st.markdown("---")

# Data Table
st.subheader("📄 Detailed Data Table")
st.dataframe(
    filtered_df.sort_values('date', ascending=False),
    use_container_width=True,
    height=300
)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center'>
    <p>📊 Retail Sales Analytics Dashboard | Author: bishal531</p>
    <p>Created with Streamlit | Data Analysis & Visualization</p>
    </div>
    """, unsafe_allow_html=True)
