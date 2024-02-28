import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd 
import os
import warnings
from text_in_box import text_boxs
from PIL import Image

warnings.filterwarnings('ignore')
st.set_page_config(page_title="Bike Sales", page_icon=":bike:",layout="wide")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
image = Image.open('sepeda-logo.jpg')

col1, col2 = st.columns([0.1,0.9])
with col1:
    st.image(image,width=100)

html_title = """
    <style>
    .title-test {
    font-weight:bold;
    padding:5px;
    border-radius:6px;
    }
    </style>
    <center><h1 class="title-test">Bike Sales</h1></center>"""
with col2:
    st.markdown(html_title, unsafe_allow_html=True)

raw_dataset = pd.read_excel("Bike Sales.xlsx", sheet_name='Sheet1')

df = raw_dataset.copy()

df['Month'] = pd.DatetimeIndex(df['Month']).month_name()

st.sidebar.header("Choose your filter: ")

Quaters = st.sidebar.multiselect("Pick Quarters:",df['Quarter'].unique())
Months = []
if Quaters:
    df1 = df[df['Quarter'].isin(Quaters)]
    Months = df1['Month'].unique()
else:        
    Months = df['Month'].unique()
    df1 = df.copy()
    

Select_Months = st.sidebar.multiselect("Pick the Motnhs",Months)

if Select_Months:
    df2 = df[df['Month'].isin(Select_Months)]
else:
    df2 = df1.copy()
Select_Region = st.sidebar.multiselect("Pick The Region",df['Region'].unique())

if Select_Region:
    df2 = df2[df2['Region'].isin(Select_Region)]
    

col1, col2, col3 = st.columns(3)
with col1:
    Sum_Sales = df2['Sales'].sum()
    text_boxs(label_box='Total Sales', value_box=Sum_Sales,currency_format=True)
with col2:
    Sum_profit = df2['Profit'].sum()
    text_boxs(label_box='Total Profit', value_box=Sum_profit,currency_format=True)
with col3:
    Sum_customer = df2['Customers'].sum()
    text_boxs(label_box='Total Customer', value_box=Sum_customer)

col1, col2 = st.columns(2)
df2["Month_index"] = pd.to_datetime(df2.Month, format='%B', errors='coerce').dt.month

category_df = df2.groupby(by = ["Month_index","Month"], as_index = False)[["Sales","Profit","Customers"]].sum()

with col1:
    st.subheader("Total Sales Per Month")
    fig = px.bar(category_df, x = "Month", y = "Sales", text = ['${:,.2f}'.format(x) for x in category_df["Sales"]],
                 template = "seaborn")
    st.plotly_chart(fig,use_container_width=True, height = 200)

with col2:
    st.subheader("Average Sales Completion Rate")
    Sales_Rate = df2['Sales Completion Rate'].mean()
    fig = go.Figure(data=[go.Pie(labels=['Sales Incompletion','Sales Completion'], values=[1-Sales_Rate,Sales_Rate], hole=.8,rotation =50)])
    st.plotly_chart(fig,use_container_width=True, height = 200)
    


with col1:
    st.subheader("Total Profit Per Month")
    fig = px.bar(category_df, x = "Month", y = "Profit", text = ['${:,.2f}'.format(x) for x in category_df["Profit"]],
                 template = "seaborn")
    st.plotly_chart(fig,use_container_width=True, height = 200)

with col2:
    st.subheader("Average Profit Completion Rate")
    Profit_Rate = df2['Profit Completion Rate'].mean()
    fig = go.Figure(data=[go.Pie(labels=['Profit Incompletion','Profit Completion'], values=[1-Profit_Rate,Profit_Rate], hole=.8,rotation =50)])
    st.plotly_chart(fig,use_container_width=True, height = 200)

with col1:
    st.subheader("Total Customer Per Month")
    fig = px.bar(category_df, x = "Month", y = "Customers", text = ['{} People'.format(x) for x in category_df["Customers"]],
                 template = "seaborn")
    st.plotly_chart(fig,use_container_width=True, height = 200)

with col2:
    st.subheader("Average Customers Completion Rate")
    Customers_Rate = df2['Profit Completion Rate'].mean()
    fig = go.Figure(data=[go.Pie(labels=['Profit Incompletion','Profit Completion'], values=[1-Profit_Rate,Profit_Rate], hole=.8,rotation =50)])
    st.plotly_chart(fig,use_container_width=True, height = 200)


with st.expander("Total Profit, Sales, and Customers Per Month View Data"):
    st.write(category_df.style.background_gradient(cmap="Blues"))
    csv = category_df.to_csv(index = False).encode('utf-8')
    st.download_button("Download Data", data = csv, file_name = "Category.csv", mime = "text/csv",
                            help = 'Click here to download the data as a CSV file')
    
cl1, cl2, cl3 = st.columns(3)
df_most = df2.groupby(by = ["Region"], as_index = False)[["Sales","Profit","Customers"]].sum()
with cl1:
    st.subheader("Order Regions Based on Total Sales")
    fig = px.bar(df_most.sort_values(by=['Sales'],ascending=True), x="Sales", y="Region",text_auto='$.2f', orientation='h')
    st.plotly_chart(fig,use_container_width=True, height = 200)
with cl2:
    st.subheader("Order Regions Based on Total Profit")
    fig = px.bar(df_most.sort_values(by=['Profit'],ascending=True), x="Profit", y="Region",text_auto='$.2f',  orientation='h')
    st.plotly_chart(fig,use_container_width=True, height = 200)
with cl3:
    st.subheader("Order Regions Based on Total Customers")
    fig = px.bar(df_most.sort_values(by=['Customers'],ascending=True), x="Customers", y="Region", orientation='h')
    st.plotly_chart(fig,use_container_width=True, height = 200)
