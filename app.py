import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout='wide',page_title="Startup Analysis")

df=pd.read_csv("startup_cleaned.csv")
df['date']=pd.to_datetime(df['date'],errors='coerce')
df['year']=df['date'].dt.year
df['month']=df['date'].dt.month
def load_startup_details(startup):
    st.title(startup)
    col9,col10,col11=st.columns(3)
    with col9:
        st.subheader("Related Industry")
        industry=df[df['startup'].str.contains(startup)]['vertical'].values[0]
        st.write(industry)
    with col10:
        st.subheader("Related  Sub-Industry")
        sub_industry = set(df[df['startup'].str.contains(startup)]['sub_vertical'].dropna().values)
        for s in sub_industry:
            st.write(s)
    with col11:
        st.subheader("Location")
        locations=set(df[df['startup'].str.contains(startup)]['city'].values)
        for location in locations:
            st.write(location)
    st.title("Fundings")
    col12,col13,col14=st.columns(3)
    with col12:
        st.subheader("Funding Stage")
        stage=df[df['startup'].str.contains(startup)]['round'].values
        st.write(stage)
    with col13:
        st.subheader("Funding Investors")
        stage = df[df['startup'].str.contains(startup)]['investors'].values
        st.write(stage)
    with col14:
        st.subheader("Funding Dates")
        stage = df[df['startup'].str.contains(startup)]['date'].dt.date.values
        st.write(stage)
    # Similar Company
    st.title("Similar Startups")
    col15,col16,col17=st.columns(3)
    with col15:
        st.subheader("Based on Verticals")
        startup_verticals = df[df['startup'].str.contains(startup, case=False)]['vertical'].str.split(
            ',').explode().str.strip()
        similar_startups= df[df['vertical'].isin(startup_verticals.unique())]['startup'].values
        st.write(similar_startups)
    with col16:
        st.subheader("Based on City")
        startup_cities = df[df['startup'].str.contains(startup)]['city'].str.split(",").explode().str.strip().unique()
        similar_startups = df[df['city'].isin(startup_cities)]['startup'].unique()
        st.write(similar_startups)
    with col17:
        st.subheader("Based on Investor")
        startup_investors = df[df['startup'].str.contains(startup)]['investors'].str.split(",").explode().str.strip().unique()
        similar_startups = df[df['investors'].isin(startup_investors)]['startup'].unique()
        st.write(similar_startups)






def load_overall_analysis():
    st.title("Overall Analysis")
    col1,col2,col3,col4=st.columns(4)
    # total invested amount
    total= round(df['amount'].sum())
    with col1:
        st.metric("Total",str(total)+'Cr')
    # max investment amount in a startup
    max_startup = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    with col2:
        st.metric("Max",str(round(max_startup))+"Cr")
    # Avg ticket size
    avg_funding=df.groupby('startup')['amount'].sum().mean()
    with col3:
        st.metric("Avg",str(round(avg_funding))+" Cr")
    # Total funded Startups
    num_startups=df['startup'].nunique()
    with col4:
        st.metric("Funded Startups",num_startups)

    st.header("MOM graph")
    selected_option=st.selectbox("Select Type",["total","Count"])
    if selected_option=="total":
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()
    temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')
    fig6, ax6 = plt.subplots()
    ax6.bar(temp_df['x_axis'],temp_df['amount'])
    st.pyplot(fig6)
    st.header("Sector Analysis")
    sector=st.selectbox("Select Type",['Count','sum'])
    if sector=="Count":
        sector_analysis=df.groupby('vertical')['amount'].count().sort_values(ascending=False).head()
    else:
        sector_analysis=df.groupby('vertical')['amount'].sum().sort_values(ascending=False).head()
    fig5, ax5 = plt.subplots()
    ax5.pie(sector_analysis,labels=sector_analysis.index,autopct="%0.01f%%")
    st.pyplot(fig5)
    col5,col6=st.columns(2)
    with col5:
        st.header("Types Of Fundings")
        type_of_fundings=df['round'].unique()
        st.write(type_of_fundings)
    with col6:
        st.header("City Wise Funding")
        city_fundings=pd.DataFrame(df.groupby('city')['amount'].sum().sort_index())
        st.dataframe(city_fundings)
    col7,col8=st.columns(2)
    with col7:
        st.header("Top Startup Year-Wise")
        top=pd.DataFrame(df.groupby('year').head(1)[['year','startup','amount']])
        st.dataframe(top)
    with col8:
        st.header("Overall Top Startups")
        overall=pd.DataFrame(df.head()[['startup','amount']])
        st.dataframe(overall)
    st.header("Top Investors")
    top_investors=df.groupby('investors')['amount'].max().sort_values(ascending=False).head()
    st.dataframe(top_investors)
    # Heatmap
    st.header("Heatmap")
    # Pivot the data to create a heatmap
    heatmap_data = df.pivot_table(index='year', columns='month', values='amount', aggfunc='sum', fill_value=0)

    # Create a heatmap
    plt.figure(figsize=(12, 8))
    sns.heatmap(heatmap_data, cmap='YlGnBu', annot=True, fmt="g")
    plt.title('Funding Heatmap (Year-Month)')
    plt.xlabel('Month')
    plt.ylabel('Year')

    # Display the heatmap in Streamlit
    st.pyplot(plt)


def load_investor_details(investor):
    st.title(investor)
    # last 5 invwestment details of investor
    last5_df= df[df['investors'].str.contains(investor)].head()[['date', 'startup', 'vertical', 'city', 'round', 'amount']]
    st.subheader("Recent Investment Details")
    st.dataframe(last5_df)
    col1,col2=st.columns(2)
    with col1:
        # Biggest  investment
        big_series=df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False)
        st.subheader("Biggest Investment Details")
        fig,ax=plt.subplots()
        ax.bar(big_series.index,big_series.values)
        st.pyplot(fig)
    with col2:
        vertical_series=df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
        st.subheader("Sector Invested In")
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series,labels=vertical_series.index,autopct="%0.01f%%")
        st.pyplot(fig1)
    col3,col4=st.columns(2)
    with col3:
        # stage wise funding deatils
        vertical_series1=df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum()
        st.subheader("Stage Wise Funding")
        fig2, ax2 = plt.subplots()
        ax2.pie(vertical_series1,labels=vertical_series1.index,autopct="%0.01f%%")
        st.pyplot(fig2)
    with col4:
        # city wise funding details
        vertical_series2 = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum()
        st.subheader("City Wise Funding")
        fig3, ax3 = plt.subplots()
        ax3.pie(vertical_series2, labels=vertical_series2.index, autopct="%0.01f%%")
        st.pyplot(fig3)
    # YOY investment
    df['year'] = df['date'].dt.year
    year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()

    # Plot YOY investment
    st.subheader("YOY Investment")
    fig3, ax3 = plt.subplots()
    ax3.plot(year_series.index, year_series.values)
    st.pyplot(fig3)
    # Extract the selected investor's verticals
    selected_verticals = df[df['investors'].str.contains(investor)]['vertical'].str.split(',').explode().str.strip()
    # Display the top 10 unique investors with the most similar verticals
    st.subheader("Top 10 Unique Investors with Similar Verticals:")
    similar_investors = df[df['vertical'].str.split(',').explode().str.strip().isin(selected_verticals)][
                            'investors'].value_counts().index[:10]
    for investor in similar_investors:
        st.write(investor)


st.sidebar.title("Indian Startup Funding Analysis")
option=st.sidebar.selectbox("Select One",["Overall Analysis","Startup","Investor"])
if option=="Overall Analysis":
    load_overall_analysis()


elif option=="Startup":
    select_startup=st.sidebar.selectbox("Select Startup",sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button("Find Startup Details")
    st.title("Startup Analysis")
    if btn1:
         load_startup_details(select_startup)
else:
    selected_investor=st.sidebar.selectbox("Select Investor",sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button("Find Investor Details")
    if btn2:
        load_investor_details(selected_investor)
