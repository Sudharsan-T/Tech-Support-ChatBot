import streamlit as st
import time
import sys
import subprocess

# Check if ollama is installed
try:
    import ollama
except ImportError:
    st.error("The 'ollama' package is not installed. Installing it now...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "ollama"])
    import ollama

from config import (
    CHATBOT_NAME,
    CHATBOT_AVATAR,
    USER_AVATAR,
    MODEL_NAME,
    TECH_SUPPORT_PROMPT,
    PAGE_TITLE,
    PAGE_ICON,
    LAYOUT,
    INITIAL_MESSAGE
)

# Page configuration
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=LAYOUT,
)

# Check if Ollama is running and TinyLlama model is available
try:
    # Use subprocess to directly check available models
    import subprocess
    result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
    output = result.stdout

    # Add debug information in the sidebar
    with st.sidebar.expander("Debug Info", expanded=False):
        st.write(f"Looking for model: {MODEL_NAME}")
        st.write("Raw output from 'ollama list':")
        st.code(output)

    # Check if our model is in the output
    if "tinyllama" in output.lower():
        st.success(f"Found TinyLlama model! The chatbot is ready to use.")
        # Force the model name to be what we know works
        MODEL_NAME = "tinyllama:latest"
    else:
        # Try to pull the model automatically
        st.warning("TinyLlama model not found. Attempting to pull it automatically...")
        try:
            pull_result = subprocess.run(['ollama', 'pull', 'tinyllama'],
                                        capture_output=True, text=True, timeout=60)
            if pull_result.returncode == 0:
                st.success("Successfully pulled TinyLlama model! The chatbot is ready to use.")
                MODEL_NAME = "tinyllama:latest"
            else:
                st.error(f"Failed to pull TinyLlama model: {pull_result.stderr}")
                st.info("Please run 'ollama pull tinyllama' in your terminal manually.")
        except Exception as pull_error:
            st.error(f"Error pulling TinyLlama model: {str(pull_error)}")
            st.info("Please run 'ollama pull tinyllama' in your terminal manually.")

except Exception as e:
    st.error(f"Error connecting to Ollama: {str(e)}")
    st.info("Please make sure Ollama is installed and running. Visit https://ollama.com/download for installation instructions.")

# Custom CSS for better appearance
st.markdown("""
<style>
    .stChatMessage {
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    .stChatMessage[data-testid="stChatMessageContent"] {
        background-color: #f0f2f6;
    }
    .main-header {
        text-align: center;
        padding: 20px;
        color: #2e6fdf;
    }
    .sub-header {
        text-align: center;
        font-size: 1.2em;
        color: #666;
        margin-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)

# App header
st.markdown(f"<h1 class='main-header'>{CHATBOT_NAME}</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>Your AI-powered technical support assistant</p>", unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": INITIAL_MESSAGE}
    ]

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=CHATBOT_AVATAR if message["role"] == "assistant" else USER_AVATAR):
        st.markdown(message["content"])

# Function to generate response using Ollama
def generate_response(prompt, history):
    try:
        # Format the prompt with the user's question
        formatted_prompt = TECH_SUPPORT_PROMPT.format(question=prompt)

        # Create messages for the chat
        messages = [{"role": "system", "content": "You are a helpful tech support assistant."}]

        # Add chat history
        for msg in history:
            messages.append(msg)

        # Add the current prompt
        messages.append({"role": "user", "content": prompt})

        # Get response from Ollama
        try:
            # First try the chat API which is more modern
            # Use a hardcoded model name that we know works
            model_to_use = "tinyllama:latest"
            response = ollama.chat(
                model=model_to_use,
                messages=messages,
                stream=True
            )
            return response
        except Exception as chat_error:
            st.warning(f"Chat API error: {str(chat_error)}. Trying fallback method...")
            # Fallback to the generate API which works with older models
            response = ollama.generate(
                model=model_to_use,
                prompt=formatted_prompt,
                stream=True
            )
            return response
    except Exception as e:
        st.error(f"Error generating response: {str(e)}")
        return None

# User input
if prompt := st.chat_input("Ask your tech support question..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message in chat
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(prompt)

    # Display assistant response in chat
    with st.chat_message("assistant", avatar=CHATBOT_AVATAR):
        message_placeholder = st.empty()
        full_response = ""

        # Get streaming response
        response_stream = generate_response(prompt, st.session_state.messages[:-1])

        if response_stream:
            for chunk in response_stream:
                # Handle different response formats
                if 'message' in chunk:
                    # Chat API format
                    content_chunk = chunk.get('message', {}).get('content', '')
                elif 'response' in chunk:
                    # Generate API format
                    content_chunk = chunk.get('response', '')
                else:
                    content_chunk = ''

                full_response += content_chunk
                message_placeholder.markdown(full_response + "▌")
                time.sleep(0.01)

            message_placeholder.markdown(full_response)
        else:
            message_placeholder.markdown("I'm having trouble connecting to the model. Please check if Ollama is running with the TinyLlama model loaded.")

    # Add assistant response to chat history
    if full_response:
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# Sidebar with information
with st.sidebar:
    st.title("About")
    st.markdown("""
    This tech support chatbot is powered by:
    - TinyLlama (1.1B parameter model)
    - Ollama (for local model hosting)
    - Streamlit (for the user interface)

    ## How to use
    1. Make sure Ollama is running
    2. Ensure TinyLlama model is downloaded (`ollama pull tinyllama`)
    3. Ask your tech support questions

    ## Tips
    - Be specific about your technical issue
    - Include relevant error messages
    - Mention your operating system or device
    """)

    # Add a clear chat button
    if st.button("Clear Chat"):
        st.session_state.messages = [
            {"role": "assistant", "content": INITIAL_MESSAGE}
        ]
        st.rerun()
