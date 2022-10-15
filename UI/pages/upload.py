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
                    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiJiZDdlNGE3YS04YjI1LTQyM2EtYmQ0Ni04NzU5YmE3YTYwNGMiLCJlbWFpbCI6Im5hZ3BhbG1hbnByZWV0QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJwaW5fcG9saWN5Ijp7InJlZ2lvbnMiOlt7ImlkIjoiRlJBMSIsImRlc2lyZWRSZXBsaWNhdGlvbkNvdW50IjoxfSx7ImlkIjoiTllDMSIsImRlc2lyZWRSZXBsaWNhdGlvbkNvdW50IjoxfV0sInZlcnNpb24iOjF9LCJtZmFfZW5hYmxlZCI6ZmFsc2UsInN0YXR1cyI6IkFDVElWRSJ9LCJhdXRoZW50aWNhdGlvblR5cGUiOiJzY29wZWRLZXkiLCJzY29wZWRLZXlLZXkiOiJiNzljYzBmMTY3OTRkYWQwYjU1NiIsInNjb3BlZEtleVNlY3JldCI6ImIwYzU4Njg1YTFlNDJlY2QzMzBhM2Q2NThjMjlkNzUzNjFlZTU2ODhhOTVlYTA4NTBmYTEzOWZjNzkxMmMxMzkiLCJpYXQiOjE2NjU4MjEyMTN9.C5Uf8DpNIT9BajHtlpPZxqZDjTi5UrYYwlxrvjHkcK8'
                 }
        response = requests.request("POST", url, headers=headers, files=files)
        url = 'https://gateway.pinata.cloud/ipfs/' + response.json()['IpfsHash']
        st.write(url)
        st.image(url)



