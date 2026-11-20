
import os
from pathlib import Path

import streamlit as st

st.set_page_config(
    page_title="S3 Files Manager",
    page_icon="📁",
    layout="wide"
)

S3_FILES_PATH = Path(
    os.getenv("S3_FILES_MOUNT", "/mnt/s3data")
)

st.title("Amazon S3 Files Manager")

if not S3_FILES_PATH.is_dir():
    st.error(f"S3 Files mount not found: {S3_FILES_PATH}")
    st.stop()

# Navigate directories
if "current_dir" not in st.session_state:
    st.session_state.current_dir = S3_FILES_PATH

current_dir = Path(st.session_state.current_dir)

# Prevent navigation outside mounted filesystem
if not current_dir.is_relative_to(S3_FILES_PATH):
    current_dir = S3_FILES_PATH
    st.session_state.current_dir = current_dir

st.caption(f"Location: {current_dir}")

if current_dir != S3_FILES_PATH:
    if st.button("⬆ Parent Directory"):
        st.session_state.current_dir = current_dir.parent
        st.rerun()

# Create directory
with st.expander("Create directory"):
    folder_name = st.text_input("Directory name")

    if st.button("Create"):
        if folder_name and Path(folder_name).name == folder_name:
            (current_dir / folder_name).mkdir(exist_ok=True)
            st.rerun()

# Upload
st.subheader("Upload File")

uploaded = st.file_uploader("Choose a file")

if uploaded and st.button("Upload"):
    destination = current_dir / Path(uploaded.name).name

    with destination.open("wb") as f:
        f.write(uploaded.getbuffer())

    st.success(f"Uploaded: {destination.name}")
    st.rerun()

# Browse files
st.divider()
st.subheader("Files and Directories")

for item in sorted(current_dir.iterdir()):
    col1, col2, col3 = st.columns([5, 2, 1])

    if item.is_dir():
        if col1.button(f"📁 {item.name}", key=str(item)):
            st.session_state.current_dir = item
            st.rerun()
    else:
        col1.write(f"📄 {item.name}")
        col2.write(f"{item.stat().st_size:,} bytes")

        col3.download_button(
            "Download",
            data=item.read_bytes(),
            file_name=item.name,
            key=f"download-{item}"
        )

        if st.button("Delete", key=f"delete-{item}"):
            item.unlink()
            st.rerun()
