import os
import json
import streamlit as st
import openai

#configuring openai api key
work=os.path.dirname(os.path.abspath(__file__))
config_data=json.load(open(f"{work}/config.json"))

OPENAI_API_KEY=config_data["OPENAI_API_KEY"] # Placing the API key into OPENAI_API_KEY variable
openai.api_key=OPENAI_API_KEY

#configuring streamlit page
st.set_page_config(
    page_title="ChatBot",
    page_icon="💬",
    layout="centered"
)

#initializing chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history=[]

st.title("🤖 ChatBot 🤖")

#display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#input field for user query
user_prompt=st.chat_input("Ask any queries here...")

if user_prompt:
    #add message to chat and display it
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role":"user","content":user_prompt})

    #send message to gpt and get response from it
    response=openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role":"system","content":"You are a helpful assistant."},
            *st.session_state.chat_history
        ]
    )

    assistant_response=response.choices[0].message.content
    st.session_state.chat_history.append({"role":"assistant","content":assistant_response})

    #display response of user from gpt-4o
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
