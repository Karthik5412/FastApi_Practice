import streamlit as st 
import pandas as pd

st.markdown("""
<style>
.stApp {
        background-color: #FFE5B4;
        color: black;
        # For Gradient:
        # background: linear-gradient(to right, #ff0099, #493240);
    }
    
[data-testid="stVerticalBlock"] {
    padding: 10px; 
    border-radius: 20px;
    border-color: brown;
    border-size : 5px;
}
    
.stButton button {
    background-color: darkgreen; 
    color: white; } </style> """, unsafe_allow_html= True)

st.set_page_config(page_title='FastApi', layout= 'wide', page_icon='⚡')

st.title('E-Commerse Website')

col1, extra, search = st.columns([20,30, 40])

with col1:
    with st.container(border= True ):
        count = 0         
        st.subheader(f'Total : {count}')
        
with search:
    st.text_input('', placeholder='Search For Product')

left1, right1 = st.columns([70, 30])

with left1 :
    with st.container(border= True) :
        
        st.subheader('Add Product')
        
        col1, col2, col3, col4 = st.columns(4)
        with col1 :
            st.text_input('',placeholder='ID')
            
        with col2 :
            st.text_input('',placeholder='NAME')
        with col3 :
            st.text_input('',placeholder='DESCRIPTION')
        with col4 :
            st.text_input('',placeholder='PRICE')
        
        btn = st.button('Add')
    
left2, right2 = st.columns([70, 30])

with left2 :
    with st.container(border= True) :
        
        st.subheader('Products')
        data = {'ID' : [],
                'NAME' : [],
                'DESCRIPTION' : [],
                'PRICE' : []}
        df= pd.DataFrame(data)
        st.dataframe(df)