import streamlit as st
import fitz  # PyMuPDF
import io
import os

st.set_page_config(page_title="Leeon Tools", layout="wide")

# Dashboard Styling
st.markdown("""
    <style>
    .stApp { background-color: #0f1123; color: white; }
    .stButton>button { background-color: #644ef1; color: white; border-radius: 20px; width: 100%; height: 50px; }
    </style>
    """, unsafe_allow_html=True)

# Main Logic
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'

if st.session_state.page == 'welcome':
    col1, col2 = st.columns(2)
    with col1:
        if os.path.exists("LeeonLogo.png"): st.image("LeeonLogo.png", width=200)
        st.title("Leeon E-Commerce Cloud")
        if st.button("Let's Start"):
            st.session_state.page = 'services'
            st.rerun()
    with col2:
        if os.path.exists("Firstpageartwork.png"): st.image("Firstpageartwork.png")

else:
    st.header("Flipkart Label & Invoice Separator")
    uploaded_file = st.file_uploader("Upload Flipkart Label PDF", type=['pdf'])

    if uploaded_file is not None:
        if st.button("Process PDF"):
            # PDF Processing Start
            doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            out_pdf = fitz.open()
            
            for page in doc:
                # Example: Sirf top half crop karna (Label ke liye)
                rect = page.rect
                new_rect = fitz.Rect(rect.x0, rect.y0, rect.x1, rect.y1 / 2) 
                page.set_cropbox(new_rect)
                out_pdf.insert_pdf(doc, from_page=page.number, to_page=page.number)
            
            # Download Button
            pdf_bytes = out_pdf.tobytes()
            st.download_button(label="Download Processed PDF", data=pdf_bytes, file_name="Flipkart_Labels.pdf", mime="application/pdf")
            st.success("PDF Tayyar hai! Download karein.")

    if st.button("Back"):
        st.session_state.page = 'welcome'
        st.rerun()