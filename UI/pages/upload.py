from asyncore import write
import os
import json
from tkinter.tix import INTEGER
from web3 import Web3
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
import streamlit as st
from PIL import Image
from io import StringIO
import requests

auth = 'Bearer ' + os.getenv("PINATA_KEY")
uploaded_file = st.file_uploader("Upload Product Image",type="jpg")
if uploaded_file is not None:
    # To write file as bytes:

    content = uploaded_file.getvalue()

    with open('ipad.jpg', 'wb') as f:
        f.write(content)
        url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
        files=[
                ('file',('ipad.jpg',open('ipad.jpg','rb'),'application/octet-stream'))
              ]
        headers = {
                    'Authorization': auth
                 }
        response = requests.request("POST", url, headers=headers, files=files)
        url = 'https://gateway.pinata.cloud/ipfs/' + response.json()['IpfsHash']
        st.write(url)
        st.image(url)



