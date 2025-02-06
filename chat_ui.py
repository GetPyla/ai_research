from openai import OpenAI
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv(override=True)

st.title("Je suis un assistant AI pas très utile")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []
    #st.session_state.messages = [
    #    {'role': 'system', 'content': 
    #        """Tu es un assistant virtuel. 
    #        A chaque réponse, si tu ne connais pas la réponse, commence par "Vous savez, je suis un assistant virtuel un peu idiot".
    #         Ensuite répond sur un ton humoristique"""}]




for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        

if prompt := st.chat_input("Quoi de neuf ?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[{'role': 'system', 'content': 
            """Tu es un assistant virtuel. 
            A chaque réponse, si tu ne connais pas la réponse, commence par "Vous savez, je suis un assistant virtuel un peu idiot".
             Ensuite répond sur un ton humoristique"""}] + [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})