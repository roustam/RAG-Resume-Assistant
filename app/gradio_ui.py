import gradio as gr
from chat_config import chat_fn
from init_llm import init_llm


def create_ui(client, model_name: str):
    """Create Gradio UI with ChatInterface and document upload support."""
    msg_num = 0

    def echo(message):
        return str(msg_num) + ": " + message

    with gr.Blocks(title=f"Chat with {model_name}", fill_height=True) as ui:
        gr.ChatInterface(
            chat_fn=echo,
            additional_inputs=[
                gr.Textbox(
                    label="System Prompt",
                    placeholder="Enter system prompt here...",
                )
            ],
            type="messages",
            title=None,
            autofocus=True,
        )

    # def check_health():
    #     try:
    #         v = client
    #         init_llm()
    #         return f"Connected to Ollama {v['version']}"
    #     except Exception as e:
    #         return f"Cannot reach LLM Service, check if service is running"

    # # Wrapper function that adapts chat_fn signature for ChatInterface
    # # ChatInterface expects fn(message, history) but chat_fn needs (client, message, history)
    # def chat_wrapper(message, history):
    #     """Wrapper that captures client in closure and calls chat_fn."""
    #     # chat_fn is a generator, so we need to yield from it for streaming
    #     yield from chat_fn(client, message, history)

    # with gr.Blocks(title=f"Chat with {model_name}", fill_height=True) as ui:
    #     gr.Markdown(f"# Chat with {model_name}")
    #     gr.Markdown("Client version: {}".format(check_health()))
    #     with gr.Row(scale=1, equal_height=True):
    #         with gr.Column(scale=1):
    #             gr.ChatInterface(
    #                 fn=chat_wrapper,
    #                 examples=[[
    #                     "Hello!",
    #                     "Show me current system settings",
    #                     "Tell me the current date",
    #                 ]],
    #                 type="messages",
    #                 title=None,
    #                 autofocus=True,
    #                 additional_inputs=[
    #                     gr.Textbox(
    #                         label="System Prompt",
    #                         placeholder="Enter system prompt here...",
    #                     )
    #                 ],
    #             )

    return ui
