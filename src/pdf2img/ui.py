import streamlit as st
import httpx
from pathlib import Path
import tempfile
import shutil
import zipfile
import io
from typing import Optional

# Page config
st.set_page_config(
    page_title="PDF2Img Converter",
    page_icon="🖼️",
    layout="wide"
)

st.title("📄 PDF to Image Converter")
st.markdown("Upload a PDF file to convert it into images using the PDF2Img Server.")

import os
# Sidebar for settings
with st.sidebar:
    st.header("Settings")
    default_url = os.environ.get("PDF2IMG_SERVER_URL", "http://localhost:8000")
    server_url = st.text_input("Server URL", value=default_url)
    fmt = st.selectbox("Output Format", ["png", "jpeg", "tiff"], index=0)
    dpi = st.slider("DPI (Quality)", min_value=72, max_value=600, value=200, step=10)

# Main area
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    st.info(f"Filename: {uploaded_file.name}")
    
    if st.button("Convert to Images", type="primary"):
        if not server_url:
            st.error("Please provide a Server URL.")
        else:
            # Progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                status_text.text("Sending to server...")
                progress_bar.progress(10)
                
                # Prepare request
                files = {'file': (uploaded_file.name, uploaded_file.getvalue(), 'application/pdf')}
                params = {'fmt': fmt, 'dpi': dpi}
                
                # Call API
                with httpx.Client(timeout=None) as client:
                    status_text.text("Processing on server (this may take a while)...")
                    progress_bar.progress(30)
                    
                    # Ensure URL has no trailing slash for consistency
                    base_url = server_url.rstrip("/")
                    response = client.post(f"{base_url}/convert", files=files, params=params)
                    
                    if response.status_code != 200:
                        st.error(f"Server Error: {response.status_code} - {response.text}")
                        progress_bar.progress(100)
                    else:
                        progress_bar.progress(80)
                        status_text.text("Processing response...")
                        
                        # Handle ZIP response
                        zip_content = io.BytesIO(response.content)
                        
                        # Create a temp dir to extract images for display
                        with tempfile.TemporaryDirectory() as temp_dir:
                            with zipfile.ZipFile(zip_content) as zip_ref:
                                zip_ref.extractall(temp_dir)
                                image_files = sorted(Path(temp_dir).glob(f"*.{fmt}"))
                            
                            progress_bar.progress(100)
                            status_text.text("Done!")
                            st.success(f"Converted successfully! Found {len(image_files)} images.")
                            
                            # Download button for the ZIP
                            st.download_button(
                                label="Download All Images (ZIP)",
                                data=response.content,
                                file_name=f"{Path(uploaded_file.name).stem}_images.zip",
                                mime="application/zip"
                            )
                            
                            # Display images
                            st.divider()
                            st.subheader("Preview")
                            
                            # Grid layout for images
                            cols = st.columns(3)
                            for i, img_path in enumerate(image_files):
                                with cols[i % 3]:
                                    st.image(str(img_path), caption=img_path.name, width="stretch")
                                    
            except httpx.ConnectError:
                st.error(f"Could not connect to server at {server_url}. Is it running?")
            except Exception as e:
                st.error(f"An error occurred: {e}")

st.markdown("---")
st.caption("Powered by PDF2Img")

