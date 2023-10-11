import streamlit as st
import pandas as pd
import  time


st.title("Startup Dashboard")
st.header("I am learning Streamlit")
st.subheader("And i am loving it")
st.write("This is a normal text")
st.markdown("""
### My Favourite Movies
- Its a wonderful life
- Lucy
- Count of Monte Cristo
""")

st.code("""
def sq(x):
    return x**2
y=sq(5)
""")

st.latex("x^2+y^2+5=21")

df=pd.DataFrame({'name':['hk','gk','kk'],
                'Dgpa':[9.2,7.6,8.9],
                'package':[4,6,9]})
st.dataframe(df)
st.metric('revenue','Rs 3L','3%')
st.json({'name':['hk','gk','kk'],
                'Dgpa':[9.2,7.6,8.9],
                'package':[4,6,9]})
st.image('logo.jpg')
st.video('big_buck_bunny_720p_1mb.mp4')
st.sidebar.title("sbar")
col1,col2=st.columns(2)
with col1:
    st.image('logo.jpg')
with col2:
    st.image('taj hotel.jpg')

st.error("login failed")
st.success("registration done")
st.info("d0ne")
st.warning("warfg")

bar=st.progress(0)
for i in range(1,101):
    time.sleep(0.1)
    # bar.progress(i)

email=st.text_input("enter email")
age=st.number_input("enter age")
reg=st.date_input("enter reg date")

email=st.text_input("enter email")
password=st.text_input("enter password")
sex=st.selectbox("Select Gender",['male','female','others'])

btn=st.button("login")
if btn:
    if email=="hk@gmail.com" and password=="1234":
        st.success("login successful")
        st.balloons()
    else:
        st.error("login failed")

file=st.file_uploader('upload file')
if file is not None:
    df=pd.read_csv(file)
    st.dataframe(df.describe())