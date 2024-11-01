import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

INPUT_FIELD_MAX_HEIGHT = 5
DEFAULT_WINDOW_SIZE = "500x600"
MAIN_FONT = "Helvetica"
SHIFT_KEYCODE = 0x0001

GPT_MODEL = "gpt-3.5-turbo"

LMSTUDIO_MODEL=os.environ.get("LMSTUDIO_MODEL")

mode = None # chatgpt or lmstudio

conversation_history = [
    {"role": "system", "content": "You are a helpful assistant."}
]

client = None
def reload_client():
    global client
    if mode == "chatgpt":
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"),
                        )
    elif mode == "lmstudio":
        client = OpenAI(base_url="http://localhost:8626/v1",
                        api_key="lm-studio")

def send_message_to_gpt():
    chat_completion = client.chat.completions.create(
        messages=conversation_history,
        model=GPT_MODEL,
    )
    return chat_completion.choices[0].message.content

def send_message_to_lmstudio():
    chat_completion = client.chat.completions.create(
        model="LMSTUDIO_MODEL",
        messages=conversation_history,
        temperature=0.7,
    )
    return chat_completion.choices[0].message.content

def send_message():
    user_message = input_box.get("1.0", tk.END).strip()  # Get the text from the Text widget
    if user_message:  # Reject empty message
        # Update chat history in the UI
        chat_history.config(state=tk.NORMAL)  # Enable editing in the text area
        chat_history.insert(tk.END, f"You:\n{user_message}\n\n")

        # Append user message to conversation history
        conversation_history.append({"role": "user", "content": user_message})

        response = "No mode selected."
        if mode == "chatgpt":
            response = send_message_to_gpt()
        elif mode == "lmstudio":
            response = send_message_to_lmstudio()

        # Append GPT response to conversation history
        conversation_history.append({"role": "assistant", "content": response})

        # Display GPT's response in the UI
        chat_history.insert(tk.END, f"GPT:\n{response}\n\n")  # Display GPT's response
        chat_history.config(state=tk.DISABLED)  # Disable editing
        chat_history.see(tk.END)  # Scroll to the end
        input_box.delete("1.0", tk.END)  # Clear the input box

# Function to handle enter/shift+enter for sending message or adding newline
def on_enter(event):
    if event.state & SHIFT_KEYCODE:  # Check if Shift key is pressed
        input_box.insert(tk.INSERT, "")  # Insert a newline
    else:
        send_message()  # Send the message if Enter is pressed without Shift
        return "break"  # Prevent default newline behavior after sending

# Function to toggle the sidebar visibility
def toggle_sidebar():
    if sidebar_frame.winfo_ismapped():  # Check if the sidebar is visible
        sidebar_frame.grid_remove()  # Hide the sidebar
        toggle_button.config(text="☰")
    else:
        sidebar_frame.grid()  # Show the sidebar
        toggle_button.config(text="<☰")

# Mode set
def set_mode_chatgpt():
    global mode
    mode = "chatgpt"
    root.title("cGPTGUI: ChatGPT")
    reload_client()

def set_mode_lmstudio():
    global mode
    mode = "lmstudio"
    root.title("cGPTGUI: LM Studio")
    reload_client()

# Window settings
root = tk.Tk()
style = Style(theme='darkly')
root.title("cGPTGUI: Select Mode")
root.geometry(DEFAULT_WINDOW_SIZE)

# Sidebar frame (hidden by default)
sidebar_frame = ttk.Frame(root, width=200, padding=(10, 10))
sidebar_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")  # Sidebar on the left
sidebar_frame.grid_remove()  # Initially hidden

# Sidebar widgets
sidebar_label = ttk.Label(sidebar_frame, text="Select mode", font=(MAIN_FONT, 14))
sidebar_label.pack(pady=20)
sidebar_button1 = ttk.Button(sidebar_frame, command=set_mode_chatgpt, text="ChatGPT")
sidebar_button1.pack(fill="x", pady=5)
sidebar_button2 = ttk.Button(sidebar_frame, command=set_mode_lmstudio, text="LM Studio")
sidebar_button2.pack(fill="x", pady=5)

# Function to toggle the 'always on top' state
is_always_on_top = False  # Track the state

def toggle_always_on_top():
    global is_always_on_top
    if is_always_on_top:
        root.attributes("-topmost", False)
        always_on_top_button.config(text="pin")
        is_always_on_top = False
    else:
        root.attributes("-topmost", True)
        always_on_top_button.config(text="*pin*")
        is_always_on_top = True

# Adding the toggle 'always on top' button to the sidebar, positioned at the bottom
always_on_top_button = ttk.Button(sidebar_frame, text="pin", command=toggle_always_on_top, width=5)
always_on_top_button.pack(side=tk.BOTTOM, pady=5)  # Positioned at the bottom of the sidebar

# Frame to hold the chat history (Text + Scrollbar)
chat_frame = ttk.Frame(root)
chat_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)  # Main chat window

# Scrollbar for the text area
scrollbar = ttk.Scrollbar(chat_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Scrollable text area for displaying chat history
chat_history = tk.Text(chat_frame, height=20, wrap="word", state=tk.DISABLED, bg="#2c2f33", fg="#ffffff",
                       font=(MAIN_FONT, 12), yscrollcommand=scrollbar.set)
chat_history.pack(side=tk.LEFT, expand=True, fill="both")

scrollbar.config(command=chat_history.yview)

# Frame to hold the input box and send button
input_frame = ttk.Frame(root)
input_frame.grid(row=1, column=1, sticky="ew", padx=10, pady=10)

# Send button
send_button = ttk.Button(input_frame, text="Send", command=send_message)
send_button.pack(side=tk.RIGHT)

# Multiline input box using Text widget
input_box = tk.Text(input_frame, font=(MAIN_FONT, 12), height=1, wrap="word")
input_box.pack(side=tk.LEFT, expand=True, fill="x", padx=(50, 10))

# Autofocus on input field when the window is loaded
input_box.focus_set()

# Bind the ENTER key to trigger the send button (without Shift) or insert newline (with Shift)
input_box.bind("<Return>", on_enter)

# Dynamically adjust input box height
def auto_resize(event):
    lines = int(input_box.index('end-1c').split('.')[0])  # Get current number of lines
    if lines <= INPUT_FIELD_MAX_HEIGHT:
        input_box.config(height=lines)  # Adjust the height to the number of lines

input_box.bind("<KeyRelease>", auto_resize)

# Floating button to toggle the sidebar (left side)
toggle_button = ttk.Button(root, text="☰", command=toggle_sidebar, width=3)
toggle_button.grid(row=1, column=1, sticky="nw", padx=10, pady=10)  # Position to the left of input

# Configure grid to make the chat frame expandable
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)

# Start the Tkinter main loop
root.mainloop()
