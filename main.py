import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style

# Fake conversation for debug
def send_message():
    user_message = input_box.get()
    if user_message.strip() != "":  # Reject empty message
        chat_history.config(state=tk.NORMAL)  # Enable editing in the text area (without this text area won't change)
        chat_history.insert(tk.END, f"You:\n{user_message}\n\n")
        chat_history.insert(tk.END, f"GPT:\nTotally legit response!\n\n")  # Fake response
        chat_history.config(state=tk.DISABLED)  # Disable editing
        chat_history.see(tk.END)  # Scroll to the end
        input_box.delete(0, tk.END)  # Clear the input box

# Window settings
root = tk.Tk()
style = Style(theme='darkly')
root.title("cGPTGUI: ChatGPT")
root.geometry("500x600")

# Frame to hold the chat history (Text + Scrollbar)
chat_frame = ttk.Frame(root)
chat_frame.pack(expand=True, fill="both", padx=10, pady=10)

# Scrollbar for the text area
scrollbar = ttk.Scrollbar(chat_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Scrollable text area for displaying chat history
chat_history = tk.Text(chat_frame, height=20, wrap="word", state=tk.DISABLED, bg="#2c2f33", fg="#ffffff",
                       font=("Helvetica", 12), yscrollcommand=scrollbar.set)
chat_history.pack(side=tk.LEFT, expand=True, fill="both")

scrollbar.config(command=chat_history.yview)

# Frame to hold the input box and send button
input_frame = ttk.Frame(root)
input_frame.pack(fill="x", padx=10, pady=10)

# User input box
input_box = ttk.Entry(input_frame, font=("Helvetica", 12))
input_box.pack(side=tk.LEFT, expand=True, fill="x", padx=(0, 10))

# Send button
send_button = ttk.Button(input_frame, text="Send", command=send_message)
send_button.pack(side=tk.RIGHT)

# Start the Tkinter main loop
root.mainloop()
