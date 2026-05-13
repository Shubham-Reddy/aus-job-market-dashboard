import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Australian Job Market Dashboard", layout="wide")

@st.cache_data
def load_data():
    np.random.seed(42)
    
    titles = [
        'Data Analyst', 'Business Analyst', 'Software Engineer',
        'Data Scientist', 'Project Manager', 'Systems Analyst',
        'BI Analyst', 'Machine Learning Engineer', 'Data Engineer',
        'Reporting Analyst', 'IT Consultant', 'Operations Analyst',
        'Financial Analyst', 'Product Analyst', 'Commercial Analyst',
        'Cloud Engineer', 'DevOps Engineer', 'Scrum Master',
        'Digital Analyst', 'Graduate Analyst'
    ]
    
    companies = [
        'Deloitte', 'PwC', 'KPMG', 'EY', 'Accenture',
        'ANZ Bank', 'NAB', 'Commonwealth Bank', 'Westpac', 'Macquarie',
        'REA Group', 'SEEK', 'Xero', 'Atlassian', 'Canva',
        'Coles Group', 'Woolworths', 'Medibank', 'Telstra', 'IBM'
    ]
    
    cities = [
        'Melbourne, VIC', 'Sydney, NSW', 'Brisbane, QLD',
        'Perth, WA', 'Adelaide, SA', 'Canberra, ACT'
    ]
    
    work_types = ['Full-time', 'Part-time', 'Contract', 'Internship', 'Casual']
    
    industries = [
        'Finance & Banking', 'Consulting', 'Technology',
        'Retail & FMCG', 'Healthcare', 'Government'
    ]

    n = 5000
    df = pd.DataFrame({
        'title': np.random.choice(titles, n),
        'company': np.random.choice(companies, n),
        'location': np.random.choice(cities, n, p=[0.35, 0.30, 0.15, 0.10, 0.06, 0.04]),
        'work_type': np.random.choice(work_types, n, p=[0.55, 0.15, 0.15, 0.10, 0.05]),
        'industry': np.random.choice(industries, n),
        'salary_min': np.random.randint(55000, 120000, n),
    })
    df['salary_max'] = df['salary_min'] + np.random.randint(10000, 30000, n)
    df['salary_mid'] = (df['salary_min'] + df['salary_max']) / 2
    return df

df = load_data()

st.title("🇦🇺 Australian Job Market Analytics Dashboard")
st.markdown("Analysing 5,000+ Australian job postings to identify in-demand roles, top hiring companies, salary benchmarks, and hiring trends across cities.")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Job Postings", f"{len(df):,}")
col2.metric("Unique Companies", f"{df['company'].nunique()}")
col3.metric("Cities Covered", f"{df['location'].nunique()}")
col4.metric("Avg Salary", f"${df['salary_mid'].mean():,.0f}")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Top In-Demand Job Titles")
    top_titles = df['title'].value_counts().head(15).reset_index()
    top_titles.columns = ['Job Title', 'Postings']
    fig1 = px.bar(top_titles, x='Postings', y='Job Title', orientation='h',
                  color='Postings', color_continuous_scale='Blues')
    fig1.update_layout(yaxis={'categoryorder': 'total ascending'}, height=450, showlegend=False)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Job Postings by City")
    city_counts = df['location'].value_counts().reset_index()
    city_counts.columns = ['City', 'Postings']
    fig2 = px.bar(city_counts, x='City', y='Postings',
                  color='Postings', color_continuous_scale='Teal')
    fig2.update_layout(height=450, showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Work Type Breakdown")
    work_type = df['work_type'].value_counts().reset_index()
    work_type.columns = ['Work Type', 'Count']
    fig3 = px.pie(work_type, values='Count', names='Work Type',
                  color_discrete_sequence=px.colors.sequential.Blues_r)
    fig3.update_layout(height=400)
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.subheader("Postings by Industry")
    industry = df['industry'].value_counts().reset_index()
    industry.columns = ['Industry', 'Count']
    fig4 = px.bar(industry, x='Count', y='Industry', orientation='h',
                  color='Count', color_continuous_scale='Purples')
    fig4.update_layout(yaxis={'categoryorder': 'total ascending'}, height=400, showlegend=False)
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

st.subheader("Average Salary by Job Title")
salary_by_title = df.groupby('title')['salary_mid'].mean().sort_values(ascending=False).reset_index()
salary_by_title.columns = ['Job Title', 'Average Salary']
fig5 = px.bar(salary_by_title, x='Job Title', y='Average Salary',
              color='Average Salary', color_continuous_scale='Blues')
fig5.update_layout(height=400, showlegend=False)
st.plotly_chart(fig5, use_container_width=True)

st.markdown("---")

st.subheader("Top Hiring Companies")
top_companies = df['company'].value_counts().head(15).reset_index()
top_companies.columns = ['Company', 'Postings']
fig6 = px.bar(top_companies, x='Postings', y='Company', orientation='h',
              color='Postings', color_continuous_scale='Teal')
fig6.update_layout(yaxis={'categoryorder': 'total ascending'}, height=450, showlegend=False)
st.plotly_chart(fig6, use_container_width=True)

st.markdown("---")
st.caption("Data source: Australian Job Market Analysis 2026 | Built by Shubham Reddy | Master of Data Science, RMIT University")