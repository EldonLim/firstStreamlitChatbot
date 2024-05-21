import streamlit as st
import numpy as np
import random 
import time
from langchain.llms import openai
from openai import OpenAI
import google.generativeai as genai
from langchain_openai import AzureChatOpenAI                                    ## This object is a connector/wrapper for ChatOpenAI engine
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage      ## These are the commonly used chat messages
import os
from langchain_community.vectorstores import FAISS
from langchain_openai import AzureOpenAIEmbeddings

llm = AzureChatOpenAI(
    openai_api_version=os.environ['AZURE_OPENAI_API_VERSION'],
    azure_endpoint=os.environ['AZURE_OPENAI_ENDPOINT'],
    api_key=os.environ['AZURE_OPENAI_APIKEY'],
    azure_deployment=os.environ['DEPLOYMENT_NAME'],
    temperature=1
)

st.title("My own chatbot")

if "text_embedding" not in st.session_state:
    st.session_state['text_embedding'] =  AzureOpenAIEmbeddings(
        azure_endpoint=os.environ['AZURE_OPENAI_ENDPOINT'],
        api_key=os.environ['AZURE_OPENAI_APIKEY'],
        azure_deployment=os.environ["AZURE_TEXT_EMBEDDING"],
        model='text-embedding-ada-002'
    )
    # vectorDB = FAISS.load_local("db/sc1015", st.session_state['text_embedding'] , allow_dangerous_deserialization=True)
    # st.session_state['retrieval'] = vectorDB.as_retriever(search_kwargs={"k": 5})

    st.session_state['llm'] = AzureChatOpenAI(
        openai_api_version=os.environ['AZURE_OPENAI_API_VERSION'],
        azure_endpoint=os.environ['AZURE_OPENAI_ENDPOINT'],
        api_key=os.environ['AZURE_OPENAI_APIKEY'],
        azure_deployment=os.environ['DEPLOYMENT_NAME'],
        temperature=1
    )

    persona = "You are Eldon's personal assistant."
    task ="your task is to answer query."
    context = ""
    condition = "If user ask any query beyond your capabilities, tell the user you are not an expert of the topic the user is asking and say sorry. If you are unsure about certain query, say sorry and advise the user to contact the Eldon at eldo0001@e.ntu.edu.sg"
    ### any other things to add on

    ## Constructing initial system message
    sysmsg = f"{persona} {task} {context} {condition}"
    st.session_state['conversations'] = [SystemMessage(content=sysmsg)]

    greetings = '''Hello my name is Alice, and I am Eldon's personal assistant. I am here to help, feel free to ask any questions.
    '''
    st.session_state['conversations'].append(AIMessage(content=greetings))
    st.session_state['msgtypes'] = {HumanMessage: "Human", AIMessage:"AI", SystemMessage:"System"}

    for conv in st.session_state['conversations']:
        if isinstance(conv, SystemMessage):
            continue
        role = st.session_state.msgtypes[type(conv)]
        with st.chat_message(role):
            st.markdown(conv.content)

if query:= st.chat_input("Your Message"):
    st.chat_message("Human").markdown(query)
    st.session_state['conversations'].append(HumanMessage(content=query))

    templog = st.session_state['conversations']
    response = st.session_state['llm'].invoke(templog)
    # response = st.session_state['llm'].invoke(st.session_state['conversations'])
    st.chat_message("AI").markdown(response.content)
    st.session_state['conversations'].append(response)


# def response_generator():
#     response = random.choice(
#         [
#         "Hello there! How can I assist you today?",
#         "Hi, human! Is there anything I can help you with?",
#         "Do you need help?",
#         ]
#     )
#     for word in response.split():
#         yield word + " "
#         time.sleep(0.05)


# # Initialize chat history
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # Display chat messages from history on app rerun
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# # React to user input
# # := operator is used to assign the user's input to the prompt variable and check if it's none in the same time
# if prompt := st.chat_input("What is up?"):
#     # Display user message in chat message container
#     with st.chat_message("user"):
#         st.markdown(prompt)
    
#     # Add user message to chat history
#     st.session_state.messages.append({"role": "user", "content": prompt})

#     response = f"Assistant: {prompt}"

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
        
    # chatinput = "You are a Malaysian helping Malaysian students who are studying abroad in Singapore to ease their lives in Singapore."

    # response = llm.invoke(chatinput)
    # print(response.content)
    
    # # Add assistant message to chat history
    # st.session_state.messages.append({"role": "assistant", "content": response})
