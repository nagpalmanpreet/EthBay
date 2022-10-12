import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

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


################################################################################
# Add Store
################################################################################
st.title("Add Store")


################################################################################
# Add Products
################################################################################
st.title("Add Product")

################################################################################
# Check Balance
################################################################################
st.title("Check Balance")

# Use a Streamlit component to get the address of the artwork owner from the user
seller_address = st.text_input("Enter Seller Address")

# Use a Streamlit component to get the artwork's URI
#artwork_uri = st.text_input("The URI to the artwork")

if st.button("Check Balance"):

    # Check if seller is already registered
    seller = contract.functions.storeOwners(seller_address).call()
    st.write(f"Seller Balance :  {seller[1]} Wei")

################################################################################
# Withdraw Balance
################################################################################
st.title("Wthdraw Balance")