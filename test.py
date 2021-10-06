import os
import base64
import streamlit as st


def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">点击下载 {file_label}</a>'
    return href

file_path = 'test.txt'
file_label = '测试文件'
st.markdown(get_binary_file_downloader_html(file_path, file_label),
            unsafe_allow_html=True)