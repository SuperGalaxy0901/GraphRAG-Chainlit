# 🌟 Chainlit Chatbot with GraphRAG, Query Expansion & Document Segmentation 🌟

Welcome to the Chainlit-based chatbot project! This project leverages cutting-edge technologies like GraphRAG, query expansion, document segmentation, and embedding using OpenAI's text-embedding-3-small model to deliver exceptional conversational AI capabilities.

## 🚀 Features

- **GraphRAG Integration**: Enhance response generation using Graph-based Retrieval-Augmented Generation.
- **Query Expansion**: Improve search accuracy by expanding user queries with related terms.
- **Document Segmentation**: Efficiently handle large documents by breaking them down into manageable segments.
- **Embedding with OpenAI**: Leverage OpenAI's state-of-the-art text-embedding-3-small model for effective semantic understanding.

## 📜 Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [Configuration](#configuration)

## 🔧 Installation

Follow these steps to set up the project on your local machine:

1. **Clone the Repo**
   ```bash
   git clone https://github.com/SuperGalaxy0901/GraphRAG-Chainlit.git
   cd chainlit-chatbot
   ```

2. **Install Dependencies**
   - Make sure you have Python installed on your system. This project requires Python 3.7 or higher.

3. **Set up Environment Variables**
   - Ensure your API keys and necessary credentials are correctly set in your environment variables. You might need `OPENAI_API_KEY`, etc.

## 🏃 Usage

After installation, you can start the chatbot with the following command:

```bash
python app.py
```

### Interacting with the Chatbot

- Open your browser and navigate to `http://localhost:8000` to start chatting! 🤖
- You can type your queries in the chatbox, and the chatbot will respond by leveraging the powerful combination of GraphRAG, query expansion, and document segmentation.

## ⚙️ Configuration

You can configure various settings of the chatbot by editing the `settings.yaml` file.

### Key Configuration Options

- **API Keys**: Set your OpenAI and other service API keys.
- **Segmentation Parameters**: Adjust how documents are segmented to suit your use case.
- **Model Settings**: Customize the embedding model parameters per your needs.
