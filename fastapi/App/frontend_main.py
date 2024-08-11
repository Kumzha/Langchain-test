import requests
import streamlit as st
from io import StringIO
from backend_main import file_content

# Session state variables:

# Chat history and user input
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

# File upload content
if 'loaded_file_content' not in st.session_state:
    st.session_state.loaded_file_content = ""



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
        # Roundtrip not neccesary
        response = requests.post("http://localhost:5000/submitFile", json=payload)

        # Validate the submition of the file
        if response.status_code == 200:
            st.success("File submited successfully!")
        else:
            st.error("Failed to submit the file.")

# User input     
if promt:
    if uploaded_file is  None:
        st.warning("Please upload a file first.")
    else:    
        st.session_state['conversation'].append({"role": "user", "content": promt})

        # Send the message to the backend
        payload = {'history': st.session_state['conversation'], 'question': promt}

        response = requests.post("http://localhost:5000/submitMessage", json=payload)
    
        st.session_state['conversation'].append({"role": "assistant", "content": response.json()['text']})

for message in st.session_state['conversation']:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
    