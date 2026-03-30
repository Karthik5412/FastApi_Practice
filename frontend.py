import streamlit as st 
import pandas as pd
import requests

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
base_url = 'http://127.0.0.1:8000/product'
col1, extra, search = st.columns([20,30, 40])

with col1:
    with st.container(border= True ):
        response = requests.get("http://127.0.0.1:8000")
        data = response.json()
        count = 0        
        if data :
            count = len(data)
        st.subheader(f'Total : {count}')
        
with search:
    pro_id = st.text_input('', placeholder='Search For Product by id')
    response = requests.get(f'{base_url}/{pro_id}')
    if pro_id : 
        st.success(response.json()['name'])

left1, right1 = st.columns([70, 30])

with left1 :
    with st.container(border= True) :
        
        st.subheader('Add OR Update Product')
        
        col1, col2, col3, col4 = st.columns(4)
        with col1 :
            id = st.text_input('',placeholder='ID')
        with col2 :
            name =st.text_input('',placeholder='NAME')
        with col3 :
            describ = st.text_input('',placeholder='DESCRIPTION')
        with col4 :
            price = st.text_input('',placeholder='PRICE')
        payload = {'id' : id, 'name' : name, 'describ' : describ, 'price' : price}
        add_btn = st.button('Add')
        up_btn = st.button('Update')
        
        if add_btn :
            response = requests.post(base_url, json= payload)
            
            st.success(response.json())
            
        if up_btn :
            response = requests.put(f'{base_url}?id={id}', json=payload)
            
            st.success(response.json())
            
        st.subheader('Delete Product')
        
        del_id = st.text_input('',placeholder='Item ID')
        delete_btn = st.button('Delete')
        if delete_btn:
            response = requests.delete(f'{base_url}?id={del_id}')
            
            st.success(response.json())
    
left2, right2 = st.columns([70, 30])

with left2 :
    with st.container(border= True) :
        
        response = requests.get("http://127.0.0.1:8000")
        data = response.json()
        
        st.subheader('Products')
        df= pd.DataFrame(data)
        st.dataframe(df, hide_index= True)