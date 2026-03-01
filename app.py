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
    .upload-box { border: 2px dashed #644ef1; padding: 20px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# Navigation Setup
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'
if 'tool' not in st.session_state:
    st.session_state.tool = None

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
        
        # Tool Selection Logic
        if st.session_state.tool is None:
            st.header("Services")
            if st.button("Flipkart Label & Invoice Separator"):
                st.session_state.tool = "flipkart"
                st.rerun()
            if st.button("Dropbox JPG Image Link Generator"):
                st.session_state.tool = "dropbox"
                st.rerun()
            if st.button("iPhone Image Converter"):
                st.session_state.tool = "iphone"
                st.rerun()
            if st.button("⬅ Back to Home"):
                st.session_state.page = 'welcome'
                st.rerun()
        
        # --- IF FLIPKART TOOL SELECTED ---
        elif st.session_state.tool == "flipkart":
            st.header("Flipkart PDF Cropper")
            uploaded_file = st.file_uploader("Apni Flipkart PDF Upload Karein", type=['pdf'])
            
            if uploaded_file:
                st.success("File Upload Ho Gayi!")
                # Yahan logic trigger hoga
                if st.button("Process & Download"):
                    st.write("Processing... (Abhi hum iska logic connect kar rahe hain)")
            
            if st.button("⬅ Back to Services"):
                st.session_state.tool = None
                st.rerun()

    with col_r:
        if os.path.exists("Secondpageartwork.png"):
            st.image("Secondpageartwork.png")
