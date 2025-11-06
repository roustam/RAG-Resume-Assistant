"""
Gradio chat interface definition.

This module defines the complete UI layout for the chat application,
including the chat window, thinking display, and document manager.
"""

import gradio as gr
from handlers.chat_handlers import add_message, bot_response, show_history_size
from handlers.document_handlers import (
    handle_file_upload,
    format_document_display,
    clear_documents
)




def create_chat_interface(ollama_client, chat_fn) -> gr.Blocks:
    """
    Create the complete Gradio chat interface.
    
    This function builds the entire UI including:
    - Chat interface with message input
    - Thinking process display panel
    - Document upload and management section
    
    Args:
        ollama_client: Ollama client instance for LLM communication
        chat_fn: Chat function from chat_config module
        
    Returns:
        Gradio Blocks interface ready to launch
    """
    with gr.Blocks() as interface:
        # Initialize document store state
        document_store_state = gr.State(value={})

        # Init token usage state
        token_usage_state = gr.State(value={'prompt':0, 'response':0})
        
        # Header
        gr.Markdown("# Chat with LLM")
        
        # Main chat layout
        with gr.Row():
            # Left column: Chat interface
            with gr.Column():
                chatbot = gr.Chatbot(
                    type="messages",
                    elem_id="chatbot",
                )
                chat_msg_input = gr.MultimodalTextbox(
                    label="Send chat message or upload files",
                    interactive=True,
                    file_count="multiple",
                    sources=["upload"],
                    autofocus=True,
                    placeholder="Enter your message here",
                )
            
            # Right column: Thinking display and history
            with gr.Column():
                thoughts = gr.Chatbot(
                    label="Thoughts", 
                    value=[], 
                    height=400, 
                    type='messages'
                )
                token_usage_stats = gr.Markdown("Token usage stats will appear here once available.")
        
        # Document upload section below chat
        with gr.Accordion("Document Manager", open=True):
            with gr.Row():
                with gr.Column(scale=1):
                    file_upload = gr.File(
                        label="Upload Documents",
                        file_count="multiple",
                        type="filepath"
                    )
                    clear_docs_btn = gr.Button(
                        "🗑️ Clear All Documents", 
                        variant="secondary"
                    )
                with gr.Column(scale=2):
                    documents_display = gr.Dataframe(
                        headers=["Filename", "Size (KB)", "Upload Date", "Status"],
                        datatype=["str", "number", "str", "str"],
                        interactive=False,
                        label="Uploaded Documents",
                        value=[]
                    )
        
        # ====================================================================
        # Event Handlers
        # ====================================================================
        
        def update_token_usage_stats(token_counts):
            """Render a friendly summary of the latest token accounting."""
            if not isinstance(token_counts, dict):
                return "Token usage unavailable."

            prompt = token_counts.get('prompt', 0)
            response = token_counts.get('response', 0)
            total = prompt + response

            return f"Total tokens: {total} (Prompt: {prompt}, Response: {response})"

        def bot_response_wrapper(history, doc_store, token_counts_state):
            """Wrapper to bind ollama_client and chat_fn to bot_response."""
            for h, t, tokens in bot_response(history, doc_store, ollama_client, chat_fn):
                yield h, t, tokens

        # Chat message submission
        chat_msg = chat_msg_input.submit(
            add_message, 
            [chatbot, chat_msg_input], 
            [chatbot, chat_msg_input]
        )
        
        # Bot response generation
        bot_msg = chat_msg.then(
            bot_response_wrapper,
            [chatbot, document_store_state, token_usage_state], 
            [chatbot, thoughts, token_usage_state], 
            api_name="bot_response"
        )
        
        # Re-enable input after bot response
        bot_msg.then(
            lambda: gr.MultimodalTextbox(interactive=True), 
            None, 
            [chat_msg_input]
        )
        
        # Document upload handler
        file_upload.change(
            handle_file_upload,
            [file_upload, document_store_state],
            [document_store_state, documents_display]
        )
        
        # Clear documents button handler
        clear_docs_btn.click(
            clear_documents,
            document_store_state,
            [document_store_state, documents_display]
        )

        # get token usage
        bot_msg.then(
            update_token_usage_stats,
            [token_usage_state],  # Read from state
            [token_usage_stats]   # Update display
        )   

    
    return interface
