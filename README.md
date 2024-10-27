# Real-time File Change Monitor with Tkinter and Watchdog

This project is a Python-based application that monitors changes in a specified directory and displays them in real-time using a graphical user interface (GUI) built with Tkinter. It can track file creation, modification, deletion, and movement in the selected folder, making it useful for monitoring logs or tracking changes during development.

## Features

- **Real-time Monitoring**: Tracks file changes (creation, modification, deletion, and movement) in a user-selected directory.
- **Threaded Operation**: Uses a separate thread to ensure that the UI remains responsive while monitoring the folder in real-time.
- **Simple GUI**: Built with Tkinter, the GUI allows users to select a folder, start monitoring, and view logs of file changes.

## Requirements

- Python 3.x
- Watchdog: `pip install watchdog`
- Tkinter (included by default with most Python installations)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/FileChangeMonitor.git
    cd FileChangeMonitor
    ```

2. Install the required dependency:
    ```bash
    pip install watchdog
    ```

3. Run the application:
    ```bash
    python monitor.py
    ```

## Usage

1. Open the application by running the `monitor.py` script.
2. Use the **Browse** button to select a directory you want to monitor.
3. Click **Start Monitoring** to begin tracking changes in the directory.
4. The log will display real-time updates when files are created, modified, deleted, or moved.
5. Click **Stop Monitoring** to stop the monitoring process.

## Example Workflow

1. Select a directory with files to monitor.
2. Add, modify, delete, or move files in the selected directory.
3. Watch the real-time log display updates for every file change event in the monitored folder.

## Files

- `monitor.py`: The main Python script that implements the file monitoring functionality.
- `README.md`: Project description and instructions.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
