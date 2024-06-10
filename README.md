# Self-Hosted LLMs with Custom data pipelines

## Introduction
This project aims to enhance information dissemination and administrative processes within BMS College of Engineering using a self-hosted infrastructure with Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG). The system integrates the Llama 3 8B model and Milvus vector store, providing tailored and accurate responses to user queries through a Streamlit-based frontend.

## Features
- Advanced Language Processing: Utilizes the Llama 3 8B model for accurate query responses.
- Efficient Data Retrieval: Employs Milvus vector store for fast and relevant data retrieval.
- User-Friendly Interface: Streamlit-based frontend for intuitive user interactions.
- Secure Authentication: Google Cloud Workspace integration for secure access.
- Continuous Learning: Incorporates Retrieval-Augmented Generation (RAG) for up-to-date information.

## Technologies Used
- Llama 3 8B Model: Self-hosted language model.
- Milvus: Vector store for efficient data management and retrieval.
- Streamlit: Frontend framework for building interactive user interfaces.
- Google Cloud Workspace: For secure authentication.
- LangChain: To streamline integration and development.

## Installation
To set up the project locally, follow these steps:

1. Clone the repository:
      ```bash
   git clone https://github.com/krishna1052/BMS-BOT.git
   cd BMS-BOT

2. Set up the virtual environment:
      ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Install dependencies:
      ```bash
   pip install -r requirements.txt

4. Start the backend server:
      ```bash
   python3 app.py

## Acknowledgements
We would like to thank BMS College of Engineering for their support and all contributors who have helped in the development of this project.
