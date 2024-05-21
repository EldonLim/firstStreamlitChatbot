import streamlit as st
import numpy as np
import random 
import time
from langchain.llms import openai
from openai import OpenAI
import wandb
import pathlib # required by generativeai
import textwrap
import google.generativeai as genai
from langchain_openai import AzureChatOpenAI                                    ## This object is a connector/wrapper for ChatOpenAI engine
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage      ## These are the commonly used chat messages
import os

llm = AzureChatOpenAI(
    openai_api_version=os.environ['AZURE_OPENAI_API_VERSION'],
    azure_endpoint=os.environ['AZURE_OPENAI_ENDPOINT'],
    api_key=os.environ['AZURE_OPENAI_APIKEY'],
    azure_deployment=os.environ['DEPLOYMENT_NAME'],
    temperature=1
)

def response_generator():
    response = random.choice(
        [
        "Hello there! How can I assist you today?",
        "Hi, human! Is there anything I can help you with?",
        "Do you need help?",
        ]
    )
    for word in response.split():
        yield word + " "
        time.sleep(0.05)

st.title("ChatGPT-like clone")

# Set OpenAI API key from Streamlit secrets
# client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Set a default model
# if "openai_model" not in st.session_state:
#     st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
# := operator is used to assign the user's input to the prompt variable and check if it's none in the same time
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = f"Assistant: {prompt}"

    # Display assistant response in chat message container
    # with st.chat_message("assistant"):
    #     stream = client.chat.completions.create(
    #         model=st.session_state["openai_model"],
    #         messages=[
    #             {"role": m["role"], "content": m["content"]}
    #             for m in st.session_state.messages
    #         ],
    #         stream = True,
    #     )
    #     response = st.write_stream(stream)
        
    chatinput = "You are a Malaysian helping Malaysian students who are studying abroad in Singapore to ease their lives in Singapore."

    response = llm.invoke(chatinput)
    print(response.content)
    
    # Add assistant message to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
