"""
RAG Chat Application - Main Entry Point

A Gradio-based chat interface with RAG (Retrieval-Augmented Generation) 
capabilities using Ollama LLM models. Supports document uploads and displays
the model's thinking process.

Author: Captain
"""

import sys
import ollama
from settings import OLLAMA_HOST, MODEL
from chat_config import chat_fn
from ui.chat_interface import create_chat_interface


def main():
    """
    Initialize and launch the chat application.
    
    This function:
    1. Displays system configuration
    2. Initializes the Ollama client
    3. Creates the Gradio interface
    4. Launches the web application
    """
    # Display system information
    print("=" * 60)
    print("RAG Chat Application Starting...")
    print("=" * 60)
    print(f"Python version: {sys.version}")
    print(f"Ollama Host: {OLLAMA_HOST}")
    print(f"Model: {MODEL}")
    print("=" * 60)
    
    # Initialize Ollama client
    ollama_client = ollama.Client(host=OLLAMA_HOST)
    
    # Create and launch the interface
    interface = create_chat_interface(ollama_client, chat_fn)
    interface.launch()


if __name__ == "__main__":
    main()
