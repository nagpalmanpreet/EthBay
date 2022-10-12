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

owner_address = contract.functions.owner().call()
st.write(f"The Owner is {owner_address}")

################################################################################
# Register Selller
################################################################################
st.title("Register Seller")
#accounts = w3.eth.accounts

# Use a Streamlit component to get the address of the artwork owner from the user
seller_address = st.text_input("Enter Seller Address")

# Use a Streamlit component to get the artwork's URI
#artwork_uri = st.text_input("The URI to the artwork")

if st.button("Register Seller"):

    # Check if seller is already registered
    is_seller = contract.functions.isStoreOwner(seller_address).call()
    if is_seller:
        st.write("Seller already registered.")
    else:
        # Use the contract to send a transaction to the registerArtwork function
        tx_hash = contract.functions.addStoreOwner(
            seller_address,
        ).transact({'from': owner_address, 'gas': 1000000})
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        st.write("Seller Registered")
        st.write(dict(receipt))

################################################################################
# Get Contract Balance
################################################################################
st.title("Check EthBay Balance")


contract_balance = contract.functions.balance().call()

if st.button("Get Balance"):

    # Use the contract to send a transaction to the registerArtwork function
    contract_balance = contract.functions.balance().call()   
    st.write(f"Contract Balance :  {contract_balance} Wei")

################################################################################
# Withdraw Balance
################################################################################
st.title("Withdraw Balance")


"""


################################################################################
# Display a Token
################################################################################
st.markdown("## Check Balance of an Account")

selected_address = st.selectbox("Select Account", options=accounts)

tokens = contract.functions.balanceOf(selected_address).call()

st.write(f"This address owns {tokens} tokens")

st.markdown("## Check  Ownership and Display Token")

total_token_supply = contract.functions.totalSupply().call()

token_id = st.selectbox("Artwork Tokens", list(range(total_token_supply)))

if st.button("Display"):

    # Get the art token owner
    owner = contract.functions.ownerOf(token_id).call()
    
    st.write(f"The token is registered to {owner}")

    # Get the art token's URI
    token_uri = contract.functions.tokenURI(token_id).call()

    st.write(f"The tokenURI is {token_uri}")
    st.image(token_uri)

"""