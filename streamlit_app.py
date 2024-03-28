from itertools import zip_longest
import streamlit as st
from streamlit_chat import message
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

openapi_key = st.secrets["OPENAI_API_KEY"]

#set streamlit page configuration
st.set_page_config(page_title="basics of AI")
st.title("AI Mentor")

#initialize session state variables
if 'generated' not in st.session_state:
    st.session_state['generated'] =[] #store AI generated message
if 'past' not in st.session_state:
    st.session_state['past'] =[] #store past user input
if  'entered_promt' not in st.session_state:
    st.session_state['entered_promt'] ="" 

#initialize the chatgpt model
chat=ChatOpenAI(
    temperature=0.5,
    model_name = "gpt-3.5-turbo",
    openai_api_key = openapi_key
)

def build_message_list():
    """
    Build a list of messages including system, human and AI messages.
    """

    #start zipped_messages with the System message
    zipped_messages  = [SystemMessage(
        content = """your name is AI Mentor. you are an AI Technical Expert for Artificial Intelligence, Ask User about their Name before starting and you are here to guide and assist the students with their AI-related questions.
        
        1. Greet the user politely ask user name and how you can assist them with AI-related queries. 
        2. Provide informative and relevant responses to questions about artificial intelligence, machine learning, deep learnning, natural language processing, computer vision, and related topics.
        3. You must Avoid discussing sensitive, offensive, or harmful content. Refrain from engaging in any form of discrimination, harassment, or inappropriate behavior.
        4. If the user asks about a topic unrelated to AI, politely steer the conversation back to AI or inform them that the topic is outside the scope of this conversation.
        5. Be patient and considerate when responding to user quaries, and provide clear explanations.
        6. If the user expresses graditude and indicates the end of the conversation, respond with a polite farewell.
        7. Do not generate the long paragraphs in response. Maximum Words should be 100.
        
        Remember, your primary goal is to assist and educate students in the field of artificial """
    )]

    #zip together the past and generated messages
    for human_msg, ai_msg in zip_longest(st.session_state['past'], st.session_state['generated']):
        if human_msg is not None:
            zipped_messages.append(HumanMessage(
                content=human_msg #add user message
            ))
        if ai_msg is not None:
            zipped_messages.append(AIMessage(
                content=ai_msg #add user message
            ))
    return zipped_messages

def generate_response():
    """Generate AI response using the ChatOpenAI model."""
    
    #build the list of messages
    zipped_messages =build_message_list()

    #generate response using the chat model
    ai_response = chat(zipped_messages)
    return ai_response.content

#define function to submit user input
def submit():
    #set entered_prompt to the current value of the prompt_input
    st.session_state.entered_prompt = st.session_state.prompt_input
    #clear prompt_input
    st.session_state.prompt_input = ""

#create a text input for user
st.text_input('YOU: ', key='prompt_input',on_change=submit)

if st.session_state.entered_prompt != "":
    #get user query
    user_query = st.session_state.entered_prompt

    #append user query to pass queries
    st.session_state.past.append(user_query)

    #generate response
    output = generate_response()

    #append AI response to generated responses 
    st.session_state.generated.append(output)

#display the chat history 
if st.session_state['generated']:
    for i in range(len(st.session_state['generated']) - 1, -1, -1):
        #display ai response
        message(st.session_state["generated"][i], key=str(i))
        #display user message
        message(st.session_state['past'][i],
                is_user=True, key=str(i) + '_user')