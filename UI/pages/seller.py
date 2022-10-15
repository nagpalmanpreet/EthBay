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
import requests

load_dotenv()

st.set_page_config(layout="wide",initial_sidebar_state='collapsed')

# Display  Image
col1, col2, col3 = st.columns(3)
with col1:
    st.write(' ')
with col2:
    image = Image.open('../Images/UI.webp')
    st.image(image)
with col3:
    st.write(' ')

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

################################################################################
# The Load_Contract Function
################################################################################


@st.cache(allow_output_mutation=True)
def load_contract():

    # Load the contract ABI
    with open(Path('../Contracts/Compiled/ethbay_abi.json')) as f:
        ethbay_abi = json.load(f)

    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    # Load the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=ethbay_abi
    )

    return contract

contract = load_contract()
store = []
accounts = w3.eth.accounts

seller_address = st.selectbox("Seller Account", options=accounts)
skip_add_store = False

if st.button("Proceed"):
    try:
        store_id = contract.functions.getStoreForSeller(seller_address).call()[0]
        store_info= contract.functions.storeFronts(store_id).call()
        store.append(store_info)
        df = pd.DataFrame(store, columns=['StoreID', 'Store Name','Store Description', 'Seller', 'Is Active'])
        df = df.drop(columns=['Seller', 'Is Active']) 
        st.write("Your Store")  
        st.table(df)
        store_products = contract.functions.getProductsForStore(store_id).call()
    
        products = []
        for iterator in range(len(store_products)):
            products.append(contract.functions.products(store_products[iterator]).call())
        df = pd.DataFrame(products, columns=['StoreID', 'Seller','Name', 'Description', 'Inventory','Price','Image'])
        df = df.drop(columns=['StoreID', 'Seller'])   
        st.write("Your Products")    
        st.write(df)  


        
    except:
        skip_add_store = True
        st.write("You don't have a store yet. Add a store to continue.")
        

################################################################################
        # Add Store
################################################################################
st.title("Add Store")
store_name = st.text_input("Store Name")
store_description = st.text_input("Store Description")


if st.button("Add Store"):
    # Check if seller is already registered
    is_seller = contract.functions.isStoreOwner(seller_address).call()
    if is_seller:
        #own_store = contract.functions.storeOwners(seller_address).call()[0]
        tx_hash = contract.functions.addStoreFront(
                    store_name,
                    store_description
                    ).transact({'from': seller_address, 'gas': 1000000})
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        st.write("Store Added")
        st.write(dict(receipt))
        total_stores = contract.functions.nextStoreFrontId().call()
        st.write(f"Total Stores on EthBay :  {total_stores}")
    else:
        st.write("You are not registered as a seller. Only seller can add a store")

################################################################################
# Add Products
################################################################################
st.title("Add Product")
product_name = st.text_input("Name")
product_description = st.text_input("Description")
product_inventory = st.number_input('Inventory',min_value=1,step=1)
product_price = st.text_input("Price (in wei)")
product_id = contract.functions.nextProductId().call() + 1
image_name = str(product_id) + '.jpg'

image_local_url = '../Images/' + image_name





auth = 'Bearer ' + os.getenv("PINATA_KEY")


uploaded_file = st.file_uploader("Upload Product Image",type="jpg")
if uploaded_file is not None:
    # To write file as bytes:

    content = uploaded_file.getvalue()

    with open(image_local_url, 'wb') as f:
        f.write(content)
        url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
        files=[
                ('file',(image_name,open(image_local_url,'rb'),'application/octet-stream'))
              ]
        headers = {
                    'Authorization': auth
                 }
        response = requests.request("POST", url, headers=headers, files=files)
        url = 'https://gateway.pinata.cloud/ipfs/' + response.json()['IpfsHash']


if st.button("Add Product"):
    try:
        if int(product_price) < 0:
          st.error('Enter a valid price')
    except:
        st.error('Enter a valid price')
    store_id = contract.functions.getStoreForSeller(seller_address).call()[0]
    st.write(store_id)
    tx_hash = contract.functions.addProduct(
                    store_id,
                    product_name,
                    product_description,
                    product_inventory,
                    int(product_price),
                    url
                    ).transact({'from': seller_address, 'gas': 1000000})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Product Added")
    st.write(dict(receipt))
    total_products = contract.functions.nextProductId().call()
    st.write(f"Total Products on EthBay :  {total_products}")
    
################################################################################
# Check Balance
################################################################################
st.title("Check Balance")

if st.button("Check Balance"):
    # Check if seller is already registered
    st.write(f"Checking Balance for  :  {seller_address}")
    seller = contract.functions.storeOwners(seller_address).call()
    st.write(f"Seller Balance :  {seller[1]} Wei")

################################################################################
# Withdraw Balance
################################################################################
st.title("Withdraw Balance")
if st.button("Withdraw Balance"):
    
    balance = contract.functions.storeOwners(seller_address).call()[1]
    tx_hash = contract.functions.storeOwnerWithdraw().transact({'from': seller_address, 'gas': 1000000})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write(f"{balance} Wei transferred to {seller_address}")
    st.write(dict(receipt))

