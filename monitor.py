import os
import threading
import tkinter as tk
from tkinter import filedialog, scrolledtext
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

# Define a class to handle file system events
class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, textbox, lock):
        super().__init__()
        self.textbox = textbox
        self.lock = lock  # To ensure thread safety when updating the UI

    # Log file creation
    def on_created(self, event):
        with self.lock:
            self.textbox.insert(tk.END, f"File created: {event.src_path}\n")
            self.textbox.see(tk.END)  # Scroll to the bottom

    # Log file deletion
    def on_deleted(self, event):
        with self.lock:
            self.textbox.insert(tk.END, f"File deleted: {event.src_path}\n")
            self.textbox.see(tk.END)

    # Log file modification
    def on_modified(self, event):
        with self.lock:
            self.textbox.insert(tk.END, f"File modified: {event.src_path}\n")
            self.textbox.see(tk.END)

    # Log file movement
    def on_moved(self, event):
        with self.lock:
            self.textbox.insert(tk.END, f"File moved: from {event.src_path} to {event.dest_path}\n")
            self.textbox.see(tk.END)

# Define the main application class
class FileChangeMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Change Monitor")
        
        # Directory label and text entry
        self.label = tk.Label(root, text="Directory to Monitor:")
        self.label.pack(pady=10)
        
        self.directory_path = tk.Entry(root, width=50)
        self.directory_path.pack(pady=5)
        
        # Button to browse directory
        self.browse_button = tk.Button(root, text="Browse", command=self.browse_directory)
        self.browse_button.pack(pady=5)
        
        # Start/Stop button
        self.start_button = tk.Button(root, text="Start Monitoring", command=self.start_monitoring)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Stop Monitoring", state=tk.DISABLED, command=self.stop_monitoring)
        self.stop_button.pack(pady=10)
        
        # Scrolled text box to display file changes
        self.log_area = scrolledtext.ScrolledText(root, width=70, height=20, wrap=tk.WORD)
        self.log_area.pack(pady=10)
        
        self.observer = None
        self.lock = threading.Lock()  # For thread-safe UI updates

    # Browse directory function
    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.directory_path.delete(0, tk.END)
            self.directory_path.insert(0, directory)

    # Start monitoring the specified directory in a separate thread
    def start_monitoring(self):
        directory = self.directory_path.get()
        if os.path.isdir(directory):
            self.log_area.insert(tk.END, f"Monitoring started in: {directory}\n")
            self.log_area.see(tk.END)
            
            # Disable start button and enable stop button
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)

            # Initialize and start the observer in a separate thread
            self.event_handler = FileChangeHandler(self.log_area, self.lock)
            self.observer = Observer()
            self.observer.schedule(self.event_handler, directory, recursive=True)

            self.monitoring_thread = threading.Thread(target=self.run_observer, daemon=True)
            self.monitoring_thread.start()
        else:
            self.log_area.insert(tk.END, "Invalid directory. Please select a valid folder.\n")
            self.log_area.see(tk.END)

    # Function to run the observer in a separate thread
    def run_observer(self):
        self.observer.start()
        try:
            while self.observer.is_alive():
                self.observer.join(1)
        except KeyboardInterrupt:
            self.observer.stop()

    # Stop monitoring the directory
    def stop_monitoring(self):
        if self.observer is not None:
            self.observer.stop()
            self.observer.join()

            self.log_area.insert(tk.END, "Monitoring stopped.\n")
            self.log_area.see(tk.END)

            # Enable start button and disable stop button
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)

# Main application setup
if __name__ == "__main__":
    root = tk.Tk()
    app = FileChangeMonitorApp(root)
    root.protocol("WM_DELETE_WINDOW", app.stop_monitoring)
    root.geometry("600x400")
    root.mainloop()
