"""
Chat handler functions for managing conversation flow and responses.

This module contains all chat-related business logic including:
- Message handling and history management
- Bot response streaming with thinking display
- Chat history utilities
"""

import gradio as gr
from gradio import ChatMessage
from typing import List, Dict, Generator, Tuple


def add_message(history: list, message) -> Tuple[list, gr.MultimodalTextbox]:
    """
    Add user message to chat history.
    
    Args:
        history: Current chat history as list of ChatMessage objects
        message: User message (can be dict with 'text' key or string)
        
    Returns:
        Tuple of (updated history, cleared textbox with interactive=False)
    """
    if isinstance(message, dict):
        user_content = message.get("text", "")
    else:
        user_content = str(message) if message else ""
    
    if user_content.strip():
        history.append(
            ChatMessage(
                role="user",
                content=user_content
            )
        )
    return history, gr.MultimodalTextbox(value=None, interactive=False)


def bot_response(
    history: list, 
    document_store: dict,
    ollama_client,
    chat_fn,
) -> Generator[Tuple[list, list, dict], None, None]:
    """
    Stream bot response with thinking steps displayed separately.
    
    This function processes LLM responses in chunks, separating the thinking
    process from the final response. Thinking steps are shown in real-time
    in a separate display panel.
    
    Args:
        history: Chat history as a list of ChatMessage objects
        document_store: Dictionary containing document embeddings and metadata
        ollama_client: Ollama client instance for LLM communication
        chat_fn: Chat function that generates responses
        
    Yields:
        Tuple of (updated_chat_history, thinking_messages_list)
    """
    # Convert ChatMessage objects to dictionary format for LLM processing
    history_for_llm = _extract_message_content(history)
    
    # Initialize state tracking
    response_generator = chat_fn(ollama_client, "", history_for_llm, document_store)
    response_msg_added = False
    thinking_messages = []
    current_thinking_content = ""
    
    # Initialize token counts
    token_counts = {'prompt': 0, 'response': 0}
    
    
    

    # Process streaming chunks from LLM
    for chunk in response_generator:
        thinking = chunk.get('thinking', '')
        response = chunk.get('response', '')
        thinking_complete = chunk.get('thinking_complete', False)

        # Capture token counts if available
        if 'prompt_eval_count' in chunk:
            token_counts['prompt'] = chunk['prompt_eval_count']
        if 'eval_count' in chunk:
            token_counts['response'] = chunk['eval_count']
        
        # Update thinking messages display
        thinking_messages = _update_thinking_messages(
            thinking_messages,
            thinking,
            thinking_complete,
            current_thinking_content
        )
        
        if thinking:
            current_thinking_content = thinking
        
        # Add or update response message in chat history
        history = _update_chat_response(history, response, response_msg_added)
        if response and not response_msg_added:
            response_msg_added = True
        
        yield history, thinking_messages, token_counts
    
    # Final yield with completion status
    if not thinking_messages:
        thinking_messages = _create_status_message("No thinking data available")
    
    yield history, thinking_messages, token_counts


def show_history_size(history: list) -> str:
    """
    Calculate total character count in chat history.
    
    Args:
        history: Chat history as list of ChatMessage objects or dicts
        
    Returns:
        Formatted string showing total character count
    """
    total = 0
    for message in history:
        if isinstance(message, ChatMessage):
            content = message.content
        elif isinstance(message, dict):
            content = message.get("content")
        else:
            continue

        if isinstance(content, str):
            total += len(content)
        elif isinstance(content, dict) and "text" in content:
            total += len(content["text"])

    return f"History size: {total}"


# ============================================================================
# Private Helper Functions
# ============================================================================


def _extract_message_content(history: list) -> list:
    """
    Extract message content from ChatMessage objects for LLM processing.
    
    Converts Gradio ChatMessage objects to simple dictionaries that can
    be passed to the LLM API.
    
    Args:
        history: List of ChatMessage objects or dictionaries
        
    Returns:
        List of message dictionaries with 'role' and 'content' keys
    """
    extracted = []
    for msg in history:
        if isinstance(msg, ChatMessage):
            extracted.append({
                "role": msg.role,
                "content": msg.content
            })
        else:
            extracted.append(msg)
    return extracted


def _update_thinking_messages(
    thinking_messages: list,
    thinking: str,
    thinking_complete: bool,
    current_thinking_content: str
) -> list:
    """
    Update the thinking messages list with new thinking content.
    
    This function manages the thinking display by:
    - Adding new thinking steps as separate messages
    - Updating the current thinking step as it streams
    - Marking completed thinking steps with a checkmark
    
    Args:
        thinking_messages: Current list of thinking message dictionaries
        thinking: New thinking content from current chunk
        thinking_complete: Whether the thinking phase is complete
        current_thinking_content: The current thinking content being streamed
        
    Returns:
        Updated list of thinking message dictionaries
    """
    if not thinking:
        # Show waiting status if no thinking data yet
        if not thinking_messages:
            return _create_status_message("Waiting for response...")
        return thinking_messages
    
    status_icon = "✓" if thinking_complete else "⏳"
    formatted_content = f"**{status_icon} Thinking**\n\n{thinking}"
    
    # Check if this is a new thinking step or an update to existing one
    if thinking_messages and thinking.startswith(current_thinking_content):
        # Update the last message (streaming the same thinking step)
        thinking_messages[-1] = {
            "role": "assistant",
            "content": formatted_content
        }
    else:
        # Add as a new thinking step
        thinking_messages.append({
            "role": "assistant",
            "content": formatted_content
        })
    
    return thinking_messages


def _update_chat_response(
    history: list,
    response: str,
    response_msg_added: bool
) -> list:
    """
    Add or update the assistant's response in chat history.
    
    Args:
        history: Current chat history
        response: Response content from the LLM
        response_msg_added: Whether a response message has already been added
        
    Returns:
        Updated chat history
    """
    if not response:
        return history
    
    response_message = ChatMessage(role="assistant", content=response)
    
    if not response_msg_added:
        # Add new response message
        history.append(response_message)
    else:
        # Update existing response message
        history[-1] = response_message
    
    return history


def _create_status_message(status_text: str) -> list:
    """
    Create a status message for the thinking display.
    
    Args:
        status_text: Status text to display
        
    Returns:
        List containing a single status message dictionary
    """
    return [{
        "role": "assistant",
        "content": f"*{status_text}*"
    }]
