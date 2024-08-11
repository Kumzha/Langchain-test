import requests
import streamlit as st
from io import StringIO
from backend_main import file_content

# API endpoints
API_MESSAGE_URL = "http://localhost:3000/api/v1/prediction/ba863175-2e49-450a-9e98-02cd7b738495"
API_UPSERT_URL = "http://localhost:3000/api/v1/vector/upsert/ba863175-2e49-450a-9e98-02cd7b738495"

# Session state variables

# Chat history and user input
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

# File upload content
if 'loaded_file_content' not in st.session_state:
    st.session_state.loaded_file_content = ""



def query(payload):
    response = requests.post(API_MESSAGE_URL, json=payload)
    return response.json()


# Streamlit app

st.title("Chat with an uploaded file")

uploaded_file = st.file_uploader("Choose a text file", accept_multiple_files=False, type=["txt"])  
promt = st.chat_input("Ask a question about the uploaded file")

if uploaded_file is not None:

    uploaded_file.seek(0)
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    payload = {'file_content': stringio.read()}   

    # Check if the file content has changed
    if st.session_state['loaded_file_content'] != payload:

        st.session_state['loaded_file_content'] = payload

        # Send the file content to the backend
        response = requests.post("http://localhost:5000/submitFile", json=payload)

        # Validate the response
        if response.status_code == 200:
            st.success("File submited successfully!")
        else:
            st.error("Failed to submit the file.")

        requests.post(API_UPSERT_URL)    

# User input     
if promt:
    if uploaded_file is  None:
        st.warning("Please upload a file first.")
    else:    
        st.session_state['conversation'].append({"role": "user", "content": promt})

        # Send the message to the backend
        payload = {'history': st.session_state['conversation'], 'question': promt}

        response = requests.post("http://localhost:5000/submitMessage", json=payload)
        print(response)
    
        st.session_state['conversation'].append({"role": "assistant", "content": response.json()['text']})

for message in st.session_state['conversation']:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
    