import tkinter as tk
from tkinter import ttk, messagebox
import keyboard
import pyautogui
import threading
import time
import subprocess
import os
import webbrowser

class MacroApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Code Macro Application")
        self.master.geometry("480x450")  # Set the window size
        self.master.configure(bg='#2a2a2a')  # Dark gray background

        # Initialize default paths
        self.default_vscode_path = r"C:\Users\pmwd\AppData\Local\Programs\Microsoft VS Code\Code.exe"
        self.default_folder_path = r"C:\Users\pmwd\Desktop\Live Macro"
        
        # Load default values into the settings
        self.vscode_path = self.default_vscode_path
        self.folder_path = self.default_folder_path

        # Set minimum size for the main window
        self.master.minsize(480, 450)  # Minimum size to prevent shrinkage below this point

        # Create rounded edges using a frame
        self.frame = tk.Frame(master, bg='#2a2a2a', bd=0)
        self.frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Settings button
        self.settings_button = tk.Button(self.frame, text="⚙️", command=self.open_settings, font=("Helvetica", 12), bg='black', fg='white', bd=0, relief='flat')
        self.settings_button.pack(side=tk.TOP, anchor='ne', padx=5, pady=5)  # Place settings button at the top right

        # Info button
        self.info_button = tk.Button(self.frame, text="❓", command=self.show_hotkeys_info, font=("Helvetica", 12), bg='black', fg='white', bd=0, relief='flat')
        self.info_button.pack(side=tk.TOP, anchor='ne', padx=5, pady=(5, 15))  # Place info button next to settings button

        # Create a frame to hold both line numbers and text entry
        self.text_frame = tk.Frame(self.frame, bg='#2a2a2a')
        self.text_frame.pack(padx=10, pady=(0, 5), expand=True, fill=tk.BOTH)

        # Line number text widget
        self.line_numbers = tk.Text(self.text_frame, width=4, bg='#1e1e1e', fg='gray', font=("Courier New", 12), bd=0, state='disabled', wrap=tk.NONE)
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        # Main text entry (decreased height)
        self.text_entry = tk.Text(self.text_frame, wrap=tk.WORD, height=10, font=("Courier New", 12), bg='#1e1e1e', fg='white', insertbackground='white', bd=0)
        self.text_entry.pack(padx=(0, 10), pady=5, expand=True, fill=tk.BOTH)

        # Bind scrolling of the text widget to the line numbers
        self.text_entry.bind("<KeyRelease>", self.update_line_numbers)
        self.text_entry.bind("<MouseWheel>", self.on_mouse_wheel)
        self.text_entry.bind("<Configure>", self.update_line_numbers)

        # Bind the Tab key event to custom function
        self.text_entry.bind("<Tab>", self.handle_tab)

        # Create a bottom frame for buttons
        self.bottom_frame = tk.Frame(self.frame, bg='#2a2a2a')
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.hotkey = 'f9'
        self.running = False
        self.interval = 6667  # Default to 6,667 microseconds (6.67 milliseconds)
        self.sent_input = False  # Flag to check if input has been sent

        # Define known values for tabbing
        self.known_values = ["function", "variable", "class", "if", "else", "for", "while"]

        # Bind F9 key to start macro
        keyboard.add_hotkey(self.hotkey, self.toggle_macro)
        # Bind F8 key to open VS Code and create folder
        keyboard.add_hotkey('f8', self.open_vs_code)
        # Bind F6 key to open CodePen
        keyboard.add_hotkey('f6', self.open_codepen)

    def update_line_numbers(self, event=None):
        # Update line numbers
        line_count = int(self.text_entry.index('end-1c').split('.')[0])
        self.line_numbers.configure(state='normal')
        self.line_numbers.delete('1.0', tk.END)  # Clear current line numbers

        for i in range(1, line_count + 1):
            self.line_numbers.insert(tk.END, str(i) + "\n")  # Insert line numbers

        self.line_numbers.configure(state='disabled')  # Disable editing

    def on_mouse_wheel(self, event):
        self.text_entry.yview_scroll(int(-1 * (event.delta / 120)), "units")  # Scroll text entry
        self.update_line_numbers()  # Update line numbers on scroll

    def handle_tab(self, event):
        # Get current cursor position
        cursor_index = self.text_entry.index(tk.INSERT)
        current_line = cursor_index.split('.')[0]
        current_text = self.text_entry.get(f"{current_line}.0", cursor_index).strip()
        
        if current_text in self.known_values:
            # Find the next known value
            next_index = (self.known_values.index(current_text) + 1) % len(self.known_values)
            next_value = self.known_values[next_index]
            self.text_entry.delete(f"{current_line}.0", cursor_index)  # Remove the current text
            self.text_entry.insert(f"{current_line}.0", next_value)  # Insert the next known value
            self.text_entry.mark_set(tk.INSERT, f"{current_line}.0 + {len(next_value)} chars")  # Move cursor to end of inserted text
            
            return "break"  # Prevent the default tab behavior

    def toggle_macro(self):
        if not self.running:
            self.start_macro()
        else:
            self.stop_macro()

    def open_settings(self):
        self.settings_window = tk.Toplevel(self.master)
        self.settings_window.title("Settings")
        self.settings_window.geometry("300x300")  # Decreased height for settings window
        self.settings_window.configure(bg='#2a2a2a')

        # Set minimum size for the settings window
        self.settings_window.minsize(800, 300)  # Minimum size for settings window

        # Interval input
        self.interval_label = tk.Label(self.settings_window, text="Set typing interval (µs):", bg='#2a2a2a', fg='white', font=("Helvetica", 12))
        self.interval_label.pack(anchor='w', padx=10, pady=5)

        self.interval_entry = tk.Entry(self.settings_window, font=("Helvetica", 12), bg='#1e1e1e', fg='white', insertbackground='white', bd=0)
        self.interval_entry.insert(0, str(self.interval))  # Set default interval to 6,667 µs
        self.interval_entry.pack(padx=10, pady=5, ipady=5)  # Added ipady for height
        self.interval_entry.config(width=200)  # Set minimum width

        # VS Code path input
        self.vscode_label = tk.Label(self.settings_window, text="VS Code Path:", bg='#2a2a2a', fg='white', font=("Helvetica", 12))
        self.vscode_label.pack(anchor='w', padx=10, pady=5)

        self.vscode_entry = tk.Entry(self.settings_window, font=("Helvetica", 12), bg='#1e1e1e', fg='white', insertbackground='white', bd=0)
        self.vscode_entry.insert(0, self.vscode_path)  # Set to current path
        self.vscode_entry.pack(padx=10, pady=5, ipady=5)
        self.vscode_entry.config(width=200)  # Set minimum width

        # Folder path input
        self.folder_label = tk.Label(self.settings_window, text="Folder Path:", bg='#2a2a2a', fg='white', font=("Helvetica", 12))
        self.folder_label.pack(anchor='w', padx=10, pady=5)

        self.folder_entry = tk.Entry(self.settings_window, font=("Helvetica", 12), bg='#1e1e1e', fg='white', insertbackground='white', bd=0)
        self.folder_entry.insert(0, self.folder_path)  # Set to current path
        self.folder_entry.pack(padx=10, pady=5, ipady=5)
        self.folder_entry.config(width=200)  # Set minimum width

        # Save settings button
        self.save_button = tk.Button(self.settings_window, text="Save", command=self.save_settings, font=("Helvetica", 12), bg='white', fg='black', bd=0, relief='flat', padx=10, pady=5)
        self.save_button.pack(pady=10)

    def show_hotkeys_info(self):
        info_window = tk.Toplevel(self.master)
        info_window.title("Hotkeys Info")
        info_window.geometry("250x150")
        info_window.configure(bg='#2a2a2a')

        info_text = "F9: Start/Stop Macro\nF8: Open VS Code & Create Folder\nF6: Open CodePen"
        info_label = tk.Label(info_window, text=info_text, bg='#2a2a2a', fg='white', font=("Helvetica", 12))
        info_label.pack(pady=10)

    def save_settings(self):
        try:
            # Get the values from the entries
            interval_value = int(self.interval_entry.get())
            vscode_path_value = self.vscode_entry.get().strip()
            folder_path_value = self.folder_entry.get().strip()

            # Validate the interval
            if interval_value <= 0:
                raise ValueError("Interval must be a positive integer.")

            # Save the settings
            self.interval = interval_value
            self.vscode_path = vscode_path_value if vscode_path_value else self.default_vscode_path  # Default if empty
            self.folder_path = folder_path_value if folder_path_value else self.default_folder_path  # Default if empty
            
            messagebox.showinfo("Settings Saved", "Settings have been saved successfully!")
            self.settings_window.destroy()
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))

    def open_vs_code(self):
        if not os.path.exists(self.vscode_path):
            messagebox.showerror("Error", f"VS Code path does not exist:\n{self.vscode_path}")
            return
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)  # Create the folder if it doesn't exist
        subprocess.Popen([self.vscode_path, self.folder_path])  # Open VS Code with the specified folder

    def open_codepen(self):
        webbrowser.open("https://codepen.io/")  # Open CodePen in a web browser

    def start_macro(self):
        self.running = True
        self.sent_input = False  # Reset flag
        self.thread = threading.Thread(target=self.run_macro)
        self.thread.start()

    def stop_macro(self):
        self.running = False
        if hasattr(self, 'thread'):
            self.thread.join()

    def run_macro(self):
        while self.running:
            if not self.sent_input:
                # Read input from text entry
                text = self.text_entry.get("1.0", tk.END).strip()
                if text:
                    pyautogui.write(text, interval=self.interval / 1000000)  # Convert µs to seconds
                    self.sent_input = True  # Mark as input sent

            time.sleep(0.1)  # Slight delay to prevent high CPU usage

if __name__ == "__main__":
    root = tk.Tk()
    app = MacroApp(root)
    root.mainloop()
