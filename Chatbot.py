import streamlit as st
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

# Function to initialize the LLM model dynamically
def initialize_llm(model_name="deepseek-r1:7b"):
    return Ollama(model=model_name)

# Function to create a structured chat template
def get_chat_prompt():
    return ChatPromptTemplate.from_messages([
        ("system", "You are DeepSeek Chat Model, an AI with a unique perspective. "
                    "You provide insightful, witty, and helpful responses while maintaining honesty. "
                    "If unsure, you admit it."),
        ("human", "{user_input}"),
        ("ai", "")
    ])

# Function to initialize the chat LLM chain
def initialize_chat_chain(llm):
    prompt = get_chat_prompt()
    return LLMChain(llm=llm, prompt=prompt)

# Streamlit UI Setup
st.set_page_config(page_title="DeepSeek Chatbot", page_icon="🤖", layout="wide")
st.title("🤖 DeepSeek Chat Model Chatbot")

# Sidebar for settings
with st.sidebar:
    st.header("⚙️ Chatbot Settings")
    model_choice = st.selectbox("Select Model:", ["deepseek-r1:7b", "deepseek-r1:14b", "deepseek-r1:32b"], index=0)
    llm = initialize_llm(model_choice)
    chain = initialize_chat_chain(llm)

    st.markdown("**Model:** " + model_choice)
    st.markdown("**Developer:** Inspired by DeepSeek AI")
    st.markdown("**Version:** 1.0.0")
    
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.experimental_rerun()
    
    st.markdown("---")
    st.markdown("### About This Chatbot")
    st.markdown(
        "This chatbot is powered by the DeepSeek R1 model running locally via Ollama. "
        "It provides insightful and witty responses while maintaining honesty and accuracy. "
        "Built using Streamlit and LangChain, this chatbot is designed for interactive AI conversations."
    )

# Store chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history on rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input area
if user_input := st.chat_input("Ask DeepSeek Chat Model anything:"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Generate and display response
    response = chain.invoke({"user_input": user_input})
    assistant_reply = response["text"]
    
    with st.chat_message("assistant"):
        st.markdown(assistant_reply)
    
    # Store assistant response
    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
    
    # Add interactive response regeneration button
    if st.button("🔄 Regenerate Response", key="regenerate"):
        new_response = chain.invoke({"user_input": user_input})
        st.session_state.messages[-1]["content"] = new_response["text"]
        st.experimental_rerun()
