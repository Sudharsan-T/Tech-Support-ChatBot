# TinyLlama Tech Support Chatbot

A local tech support chatbot powered by TinyLlama, Ollama, and Streamlit. This application provides a user-friendly interface for interacting with the TinyLlama model to get technical support assistance.

![TinyLlama Tech Support Chatbot](https://img.shields.io/badge/TinyLlama-Tech%20Support-blue)

## Features

- 🤖 Local AI-powered tech support assistant
- 💬 Interactive chat interface with message history
- 🔄 Streaming responses for better user experience
- 🛠️ Specialized tech support prompting
- 🏠 Runs completely locally - no data sent to external servers

## Prerequisites

Before running the application, make sure you have the following installed:

1. **Python 3.8+**
2. **Ollama** - Download from [ollama.com](https://ollama.com/download)
3. **TinyLlama model** - After installing Ollama, run `ollama pull tinyllama`

## Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd tinyllama-tech-support
   ```

2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Make sure Ollama is running in the background.

2. Run the Streamlit application:
   ```
   streamlit run app.py
   ```

3. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501).

4. Start chatting with your tech support assistant!

## Configuration

You can customize the chatbot by modifying the `config.py` file:

- Change the model by updating `MODEL_NAME`
- Modify the system prompt in `TECH_SUPPORT_PROMPT`
- Adjust UI settings like `PAGE_TITLE`, `CHATBOT_NAME`, etc.

## How It Works

The application uses:

1. **Streamlit** for the web interface
2. **Ollama** for running the TinyLlama model locally
3. **TinyLlama** (1.1B parameter model) for generating responses

The tech support prompt is specifically designed to guide the model to provide helpful technical assistance.

## Limitations

- TinyLlama is a smaller model (1.1B parameters), so it may not handle complex queries as well as larger models
- The model's knowledge is limited to its training data
- Response quality depends on how well the query is formulated

## Troubleshooting

- **"Failed to connect to Ollama"**: Make sure Ollama is running in the background
- **"Model not found"**: Ensure you've downloaded the TinyLlama model with `ollama pull tinyllama`
- **Slow responses**: TinyLlama is optimized for efficiency, but response time depends on your hardware

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [TinyLlama](https://github.com/jzhang38/TinyLlama) for the compact yet capable language model
- [Ollama](https://ollama.com) for making it easy to run models locally
- [Streamlit](https://streamlit.io) for the interactive web framework
