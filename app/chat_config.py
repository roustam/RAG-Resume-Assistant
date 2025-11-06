from settings import MODEL
from datetime import datetime


def chat_fn(client, message, history, document_store=None):
    """
    Chat function that sends messages to Ollama and streams responses.
    Parses thinking tokens from DeepSeek-R1 model and yields them separately.
    
    Args:
        client: Ollama client instance
        message: Additional message to append (usually empty string)
        history: List of message dicts with 'role' and 'content' keys
        document_store: Dict of uploaded documents with content and metadata
    
    Yields:
        dict: Dictionary with 'thinking' and 'response' keys for streaming display
    """
    # Build messages array with system prompt
    messages = []
    
    # Get current date and time for context
    current_date = datetime.now().strftime("%A, %B %d, %Y")
    current_time = datetime.now().strftime("%H:%M")
    
    # Build document context if documents are available
    document_context = ""
    if document_store and len(document_store) > 0:
        document_context = "\n\n**Available Documents:**\n"
        for doc_id, doc_data in document_store.items():
            document_context += f"\n---\n**Document: {doc_data['filename']}**\n"
            document_context += f"{doc_data['content'][:5000]}"  # Limit to first 5000 chars per doc
            if len(doc_data['content']) > 5000:
                document_context += "\n...(truncated)"
            document_context += "\n---\n"
    
    system_prompt = f"""\
        **Role**: HR Document Analyst
        **Task**: Analyze resumes and office documents to extract key information
        **Constraints**:
        1. NEVER provide fabricated information
        2. Don't make up names or details. If there's no context, answer as is
        3. ALWAYS use the information provided in the documents to answer the user's questions
        4. If unsure, say "Information not found in document"
        5. Focus on factual extraction, not creative interpretation
        6. Format responses clearly with bullet points
        7. Flag inconsistencies between documents
        
        Current date: {current_date}
        Current time: {current_time} (24-hour format)
        {document_context}
    """
    
    messages.append({"role": "system", "content": system_prompt})
    
    # Add conversation history
    # Filter out empty assistant messages and metadata
    for msg in history:
        role = msg.get("role")
        content = msg.get("content")
        
        if role and content:
            # Only add the actual content, not thinking metadata
            if role == "assistant" and not msg.get("metadata", {}).get("title"):
                messages.append({"role": role, "content": content})
            elif role == "user":
                messages.append({"role": role, "content": content})
    
    # Only add additional message if provided and not empty
    if message and message.strip():
        messages.append({"role": "user", "content": message})
    
    # Stream response from Ollama with thinking enabled
    try:
        response = client.chat(
            model=MODEL,
            messages=messages,
            stream=True,
            options={
                "think": True  # Enable thinking mode for DeepSeek-R1
            }
        )
        
        thinking_buffer = ""
        response_buffer = ""
        thinking_complete = False
        prompt_eval_count = 0
        eval_count = 0
        
        for chunk in response:
            should_yield = False

            if "prompt_eval_count" in chunk:
                prompt_eval_count = chunk["prompt_eval_count"]
                should_yield = True

            if "eval_count" in chunk:
                eval_count = chunk["eval_count"]
                should_yield = True

            if "message" in chunk:
                message = chunk["message"]
                
                # Extract thinking from separate field (Ollama native approach)
                if "thinking" in message and message["thinking"]:
                    thinking_chunk = message["thinking"]
                    thinking_buffer += thinking_chunk
                    should_yield = True
                
                # Extract response content
                if "content" in message and message["content"]:
                    content_chunk = message["content"]
                    response_buffer += content_chunk
                    should_yield = True
                    # If we're getting content, thinking is likely complete
                    if thinking_buffer and not thinking_complete:
                        thinking_complete = True
                        # print(f"[DEBUG] Thinking complete, total: {len(thinking_buffer)} chars")

            if should_yield:
                yield {
                    'thinking': thinking_buffer,
                    'response': response_buffer,
                    'thinking_complete': thinking_complete,
                    'prompt_eval_count': prompt_eval_count,
                    'eval_count': eval_count,
                }
                
    except Exception as e:
        error_message = f"Error communicating with Ollama: {str(e)}"
        print(error_message)
        yield {
            'thinking': '',
            'response': error_message,
            'thinking_complete': True
        }