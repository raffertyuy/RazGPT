# Import necessary libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Function to load data
@st.cache_data
def load_data(file):
    df = pd.read_csv(file)
    return df

# Function to preprocess data
def preprocess_data(df):
    df['Age'] = df['Age'].astype(int)
    bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    labels = ['0-10', '10-20', '20-30', '30-40', '40-50', '50-60', '60-70', '70-80', '80-90', '90-100']
    df['AgeGroup'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)
    grouped = df.groupby('AgeGroup').size()
    return grouped

# Function to plot bar graph
def plot_graph(grouped):
    fig, ax = plt.subplots()
    grouped.plot(kind='bar', ax=ax)
    ax.set_xlabel('Age Group')
    ax.set_ylabel('Number of People')
    ax.set_title('Number of People by Age Group')
    return fig

# Create a file uploader for the user to upload a CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    df = load_data(uploaded_file)
    grouped = preprocess_data(df)
    fig = plot_graph(grouped)
    st.write("# People by Age Group")
    st.dataframe(df)
    st.pyplot(fig)
else:
    st.write("Please upload a CSV file.")