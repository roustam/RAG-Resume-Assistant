"""
Document management handlers for file uploads and document store operations.

This module handles:
- File upload processing and validation
- Document store management
- Document display formatting
"""

import os
from datetime import datetime
from typing import Dict, List, Tuple


def handle_file_upload(files, document_store: dict) -> Tuple[dict, list]:
    """
    Handle file uploads and update document store.
    
    Processes uploaded files, extracts their content, and stores them
    with metadata. Automatically skips duplicate files.
    
    Args:
        files: List of file paths from Gradio file upload
        document_store: Dictionary storing document data
        
    Returns:
        Tuple of (updated document_store, formatted display data)
    """
    if not files:
        return document_store, format_document_display(document_store)
    
    for file_path in files:
        try:
            filename = os.path.basename(file_path)
            
            # Check if this file already exists in the store (skip duplicates)
            already_exists = any(
                doc_data["filename"] == filename 
                for doc_data in document_store.values()
            )
            
            if already_exists:
                print(f"Skipping duplicate file: {filename}")
                continue
            
            # Read file content
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Generate unique document ID
            doc_id = f"doc_{len(document_store) + 1}_{datetime.now().timestamp()}"
            
            # Get file metadata
            file_size = os.path.getsize(file_path) / 1024  # KB
            upload_date = datetime.now().strftime("%Y-%m-%d %H:%M")
            
            # Store document
            document_store[doc_id] = {
                "filename": filename,
                "content": content,
                "size_kb": round(file_size, 2),
                "upload_date": upload_date,
                "status": "Active"
            }
            print(f"Added new document: {filename}")
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            continue
    
    return document_store, format_document_display(document_store)


def format_document_display(document_store: dict) -> list:
    """
    Format document store for dataframe display.
    
    Converts the document store dictionary into a list of rows
    suitable for Gradio Dataframe component.
    
    Args:
        document_store: Dictionary containing document data
        
    Returns:
        List of rows, each containing [filename, size_kb, upload_date, status]
    """
    if not document_store:
        return []
    
    rows = []
    for doc_id, doc_data in document_store.items():
        rows.append([
            doc_data["filename"],
            doc_data["size_kb"],
            doc_data["upload_date"],
            doc_data["status"]
        ])
    return rows


def clear_documents(document_store: dict) -> Tuple[dict, list]:
    """
    Clear all documents from store.
    
    Args:
        document_store: Dictionary storing document data
        
    Returns:
        Tuple of (cleared document_store, empty display data)
    """
    document_store.clear()
    return document_store, format_document_display(document_store)
