import tkinter as tk
from tkinter import messagebox, filedialog


def load_file():
    """Load a Python file and initialize the line counter."""
    global lines, current_line
    file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
    if file_path:
        with open(file_path, "r") as file:
            lines = file.read().splitlines()
        current_line = 0
        typed_code.config(state=tk.NORMAL)
        typed_code.delete(1.0, tk.END)
        typed_code.config(state=tk.DISABLED)
        line_entry.delete(0, tk.END)
        root.title(f"Memorizing: {file_path.split('/')[-1]}")
        check_skip_conditions()


def check_line():
    """Check the typed line against the current line in the file, ignoring case and whitespace,
    and automatically skip lines in the skip list or empty lines."""
    global current_line, attempt

    removed_comments = lines[current_line].split("#")[0]
    typed_line = line_entry.get().strip().replace(" ", "")
    correct_line = removed_comments.strip().replace(" ", "")

    if typed_line.lower() == correct_line.lower():
        line_entry.config(bg="green")
        add_line()
        current_line += 1
        line_entry.delete(0, tk.END)
        check_skip_conditions()
        attempt = 1
    else:
        line_entry.config(bg="red")
        attempt += 1
        if attempt == 2:
            display_hints()
        if attempt == 3:
            attempt = 1
            add_line()
            current_line += 1
            check_skip_conditions()

    if current_line > len(lines):
        messagebox.showinfo("Congratulations!", "You have finished typing the file.")


def check_skip_conditions():
    """Check and skip lines based on empty content or specific substrings."""
    global current_line

    # Define a list of strings that, if present in a line, should cause the line to be skipped.
    skip_list = ["def", '"""']

    # Check if the current line is empty or contains any skip phrases.
    while current_line < len(lines) and (
        not lines[current_line].strip()
        or any(skip_phrase in lines[current_line] for skip_phrase in skip_list)
    ):
        add_line(True)
        current_line += 1
        line_entry.delete(0, tk.END)

    if current_line > len(lines):
        messagebox.showinfo("Congratulations!", "You have finished typing the file.")


def add_line(highlight=False):
    """Add the current line to the typed_code widget and display it."""
    global current_line
    line = lines[current_line]
    removed = line.split("#")[0]  # Removing comments to display
    typed_code.config(state=tk.NORMAL)
    if highlight:
        typed_code.insert(tk.END, removed + "\n", "highlight")
    else:
        typed_code.insert(tk.END, removed + "\n")
    typed_code.config(state=tk.DISABLED)
    typed_code.see(tk.END)


def skip_line(event):
    """Skip the current line and display it in the typed_code window."""
    global current_line
    add_line()
    current_line += 1
    if current_line > len(lines):
        messagebox.showinfo("Congratulations!", "You have finished typing the file.")
    line_entry.delete(0, tk.END)


def display_hints():
    """Display hints or line information based on the current state."""
    if current_line < len(lines) and "#" in lines[current_line]:
        hint_label.config(text="Hint: " + lines[current_line].split("#")[1].strip())
    else:
        hint_label.config(text="No hints available.")


# Set up the main window
root = tk.Tk()
root.title("Code Memorization Helper")
root.configure(bg="#2E3440")
# Create a frame for text widgets to ensure resizing
frame = tk.Frame(root, bg="#2E3440")
frame.pack(fill=tk.BOTH, expand=True)

# Display box for typed code
typed_code = tk.Text(
    frame,
    wrap=tk.WORD,
    font=("Consolas", 12),
    bg="#3B4252",
    fg="#ECEFF4",
    insertbackground="#ECEFF4",
    state=tk.DISABLED,
)
typed_code.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 0))
typed_code.tag_configure("highlight", foreground="#8FBCBB")  # Nord highlight color
# Single-line entry for typing
line_entry = tk.Entry(
    frame, font=("Consolas", 12), bg="#4C566A", fg="#ECEFF4", insertbackground="#ECEFF4"
)
line_entry.pack(fill=tk.X, padx=10, pady=(0, 10))
line_entry.bind("<Return>", lambda event: check_line())
line_entry.bind("<Control-Return>", skip_line)  # Bind Ctrl-Enter to skip a line

# Label for hints
hint_label = tk.Label(
    frame,
    text="Load a file and start typing...",
    font=("Consolas", 10),
    bg="#434C5E",
    fg="#ECEFF4",
)
hint_label.pack(fill=tk.X, padx=10, pady=(0, 10))

# Load button
load_button = tk.Button(
    root, text="Load Python File", command=load_file, bg="#4C566A", fg="#ECEFF4"
)
load_button.pack(pady=(0, 10))

# Global variables
lines = []
current_line = 0
attempt = 1  # Initialize attempt counter

# Start the GUI loop
root.mainloop()
