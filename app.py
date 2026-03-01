import streamlit as st
import os

# Page Settings
st.set_page_config(page_title="Leeon E-Commerce Dashboard", layout="wide")

# Styling for Dark Theme
st.markdown("""
    <style>
    .stApp { background-color: #0f1123; color: white; }
    .stButton>button { 
        background-color: #644ef1; color: white; border-radius: 20px; 
        width: 100%; height: 50px; border: none; font-weight: bold;
    }
    .stButton>button:hover { background-color: #a34ef1; color: white; }
    </style>
    """, unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state.page = 'welcome'

# --- PAGE 1: WELCOME ---
if st.session_state.page == 'welcome':
    col1, col2 = st.columns([1, 1])
    with col1:
        if os.path.exists("LeeonLogo.png"):
            st.image("LeeonLogo.png", width=200)
        st.markdown("<h1 style='font-size: 50px;'>Welcome to Leeon<br>E-Commerce</h1>", unsafe_allow_html=True)
        st.write("One stop for all E-Commerce Solutions")
        if st.button("Let's Start"):
            st.session_state.page = 'services'
            st.rerun()
    with col2:
        if os.path.exists("Firstpageartwork.png"):
            st.image("Firstpageartwork.png")

# --- PAGE 2: SERVICES ---
else:
    col_l, col_r = st.columns([1.5, 1])
    with col_l:
        if os.path.exists("LeeonLogo.png"):
            st.image("LeeonLogo.png", width=120)
        st.header("Services")
        
        # Service Buttons (Logic integration will be next)
        if st.button("Flipkart Label & Invoice Separator"):
            st.info("Tool is ready. Integration starting...")
            
        if st.button("Dropbox JPG Image Link Generator"):
            st.write("Link Generator Active")

        if st.button("iPhone Image Converter"):
            st.write("HEIC to JPG Active")
            
        if st.button("⬅ Back"):
            st.session_state.page = 'welcome'
            st.rerun()

    with col_r:
        if os.path.exists("Secondpageartwork.png"):
            st.image("Secondpageartwork.png")