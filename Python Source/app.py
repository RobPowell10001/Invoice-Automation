import tkinter as tk
from tkinter import messagebox
from UncheckRechecker import *

def on_submit():
    user_input = input_box.get()
    if user_input:
        # Do something with the input (replace this with your program's logic)

        statusCode = fixTaskCompletionOrder(user_input)
        if (statusCode == 0):
            messagebox.showinfo("Result", f"Successfully fixed order for Project {user_input}")
        elif (statusCode == 1):
            messagebox.showinfo("Result", f"Failed, there were API errors")
        elif (statusCode == 2):
            messagebox.showinfo("Result", f"Failed, there were ViewData fetching errors")
        elif (statusCode == 3):
            messagebox.showinfo("Result", f"Failed, there were both API and ViewData errors (impressive)")
        elif (statusCode == 4):
            messagebox.showinfo("Result", f"Failed, could not find Project with number {user_input}")
    else:
        messagebox.showwarning("Warning", "Input cannot be empty!")


# Create the main window
root = tk.Tk()
root.title("Task Completion Fixer")

# Create a label
label = tk.Label(root, text="Project Number to fix:")
label.pack(pady=5)

# Create a text box
input_box = tk.Entry(root, width=40)
input_box.pack(pady=5)

# Create a submit button
submit_button = tk.Button(root, text="Submit", command=on_submit)
submit_button.pack(pady=10)

# Run the application
root.mainloop()
