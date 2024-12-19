import tkinter as tk
from tkinter import messagebox
from UncheckRechecker import *

def on_submit():
    user_input = input_box.get()
    if user_input:
        # Check if the input number corresponds to a project number
        projectIDSearchResult = projectNumberToProjectID(user_input)
        if (projectIDSearchResult[0] == "-1"):
            messagebox.showerror("Error", f"Failed, could not find Project with number {user_input}")
            return #if not, short circuit
        else:
            #if it does, ask if they really want to edit the project with that name
            if messagebox.askyesno("Confirmation", f"Are you SURE you want to complete all tasks in {projectIDSearchResult[1]}"):
                statusCode = fixTaskCompletionOrder(projectID=projectIDSearchResult[0])
        
        if (statusCode == 0):
            messagebox.showinfo("Succes", f"Successfully fixed order for Project {user_input}")
        elif (statusCode == 1):
            messagebox.showerror("Error", f"Failed, there were API errors")
        elif (statusCode == 2):
            messagebox.showerror("Error", f"Failed, there were ViewData fetching errors")
        elif (statusCode == 3):
            messagebox.showerror("Error", f"Failed, there were both API and ViewData errors (impressive)")
    else:
        messagebox.showwarning("Warning", "Input cannot be empty!")


# Create the main window
root = tk.Tk()
root.title("TaskCompletionFixer")

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
