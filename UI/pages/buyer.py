import os
import json
from web3 import Web3
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
import streamlit as st
from PIL import Image

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

st.title("Eth Bay")

accounts = w3.eth.accounts

buyer_address = st.selectbox("Select buyer address", options=accounts)


################################################################################
# Display Products
################################################################################
try:
    total_stores = contract.functions.nextStoreFrontId().call()
    stores = []
    iterator = 0
    for iterator in range(total_stores):   
        stores.append(contract.functions.storeFronts(iterator).call()[0])


    products_info=[]

    for iterator in range(len(stores)):
        store_products = contract.functions.getProductsForStore(iterator).call()
        for inner_iterator in range(len(store_products)):
            products_info.append(contract.functions.products(store_products[inner_iterator]).call())
    products = []
    products_dict = {}
    products_name_dict = {}
    for iterator in range(len(products_info)):
        products.append(products_info[iterator][2])
        products_dict[iterator] = products_info[iterator]
        products_name_dict[products_info[iterator][2]] = iterator

    buyer_product = st.selectbox("Select Product", options=products)
    product_code = products_name_dict[buyer_product]
    product_info = products_dict[product_code]
    product_price = product_info[5]

    #temp = {}
    #temp[product_info[2]] = product_info
   # st.write(temp)
    #print(temp)
    #st.table(pd.DataFrame.from_dict(temp))
    product_price_eth = w3.fromWei(product_info[5], "ether")
    st.write(product_price_eth)
    df = pd.DataFrame({
                        'Seller': [product_info[1]],
                        'Description': [product_info[3]],
                        'Items Available': [product_info[4]],
                        'Price(in Wei)': [product_info[5]],
                        'Image': [product_info[6]]
        },
        index=[product_info[2]])
    st.table(df)
except:
    st.write('in error')

try:
    # Display  Image
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(' ')
    with col2:
        st.image(product_info[6])
    with col3:
        st.write(' ')
    
except:
    ''

input_quantity = st.number_input('Quantity',min_value=1,step=1)

if st.button("Buy"):
    value = input_quantity * product_price
    tx_hash = contract.functions.buyProduct(
                    product_code,
                    input_quantity
                    ).transact({'from': buyer_address,'value':value, 'gas': 1000000})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Payment Succesful")
    st.write(dict(receipt))