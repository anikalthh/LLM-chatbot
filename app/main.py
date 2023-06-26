# standard library modules
import os
import re

# third-party modules
import streamlit as st
from streamlit_chat import message
from dotenv import (
    find_dotenv,
    load_dotenv
)
from langdetect import detect
from langdetect import DetectorFactory

# Lingua
# to support bahasa indonesian, thai, bengali, bahasa melayu, vietnamese, mandarin, tamil, burmese, tagalog
from lingua import Language, LanguageDetectorBuilder

# local modules
from function import (
    conversational_chat,
    start_conversation
)

load_dotenv(find_dotenv())

# To enforce consistent results for langdetect
DetectorFactory.seed = 0

# Lingua declare languages
languages = [Language.ENGLISH, Language.CHINESE, Language.KOREAN, Language.TAMIL, Language.BENGALI, Language.TAGALOG, Language.VIETNAMESE, Language.THAI]
detector = LanguageDetectorBuilder.from_languages(*languages).build()

# Default text
generated_session_text = "Hello! I'm your guide for migrant domestic workers. Ask me anything!"
past_session_text = "Hey ! 👋"
welcome_text = "How would you like us to help you today?"
button_text = "Send"

# Conditional response
default_response = "Respond with 'I am sorry but I do not have the information.' if you don't have the info."
mandarin_response = "Translate your output response to Mandarin."
malay_response = "Translate your output response to Bahasa Malay."
korean_response = "Translate your output response to Korean language."
burma_response = "Translate your output response to Burma language."
tamil_response = "Translate your output response to Tamil."
indo_response = "Translate your output response to Bahasa Indonesian language."
thai_response = "Translate your output response to Thai language."
bengali_response = "Translate your output response to Bengali language."
viet_response = "Translate your output response to Vietnamese language."
tagalog_response = "Translate your output response to the Tagalog language."

if 'history' not in st.session_state:
    st.session_state['history'] = []

if 'generated' not in st.session_state:
    st.session_state['generated'] = [generated_session_text]

if 'past' not in st.session_state:
    st.session_state['past'] = [past_session_text]

chain = start_conversation()

# container for the chat history
response_container = st.container()

# container for the user's text input
container = st.container()

with container:
    with st.form(key='sgwp', clear_on_submit=True):

        user_input = st.text_input(
            welcome_text,
            max_chars=200
        )
        send_button = st.form_submit_button(label=button_text)

        with st.spinner('loading...'):
            if send_button and user_input:
                lang = detector.detect_language_of(user_input)
                print(lang)
                if lang == Language.CHINESE:
                    response_text = f'{user_input}. {mandarin_response}'
                elif lang == Language.MALAY:
                    response_text = f'{user_input}. {malay_response}'
                elif lang == Language.KOREAN:
                    response_text = f'{user_input}, {korean_response}'
                elif lang == Language.TAMIL:
                    response_text = f'{user_input}. {tamil_response}'
                elif lang == Language.THAI:
                    response_text = f'{user_input}. {thai_response}'
                elif lang == Language.BENGALI:
                    response_text = f'{user_input}. {bengali_response}'
                elif lang == Language.VIETNAMESE:
                    response_text = f'{user_input}. {viet_response}'
                elif lang == Language.INDONESIAN:
                    response_text = f'{user_input}. {indo_response}'
                elif lang == Language.TAMIL:
                    response_text = f'{user_input}. {tamil_response}'
                elif lang == Language.TAGALOG:
                    response_text = f'{user_input}. {tagalog_response}'
                else:
                    response_text = f'{user_input}. {default_response}'
                print(response_text)
                output = conversational_chat(
                    chain,
                    response_text
                )
                st.session_state['past'].append(user_input)
                st.session_state['generated'].append(output)

    if st.button('Reset this conversation?'):
        st.session_state['history'] = []
        st.session_state['past'] = [past_session_text]
        st.session_state['generated'] = [generated_session_text]


if st.session_state['generated']:
    with response_container:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="personas")
            message(st.session_state["generated"][i], key=str(i), avatar_style="bottts")
