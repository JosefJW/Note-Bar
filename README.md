# Note Bar
## Overview

Note Bar is a compact, minimalistic note-taking application designed for quick note creation, loading, editing, and deletion. The app runs in the background and does not appear on the taskbar, providing a distraction-free environment for jotting down quick ideas. It stores your notes in a SQLite database, ensuring that your information is persistent even after you close the application.
## Features

    Create new notes with titles and content.
    Load and view saved notes.
    Edit or delete notes with simple options.
    Taskbar-free operation, always staying on top while being unobtrusive.
    Persistent note storage using an SQLite database.

## Installation
### Requirements

    Python 3.x
    PyQt5
    SQLite  

### Installation Steps:

    Clone the repository or download the application files.
    Install the required dependencies using pip:

    pip install PyQt5 sqlite3

Run the application by executing the following:

    python note.py

## Usage

    Creating a Note:
        Click the New button to create a new note.
        Enter a title and content for your note.
        Click Save to store your note.

    Loading a Note:
        Click the Load button to view the list of existing notes.
        Click on any note title to edit or delete it.

    Editing a Note:
        After clicking a note, a prompt will appear asking if you'd like to edit the note.
        Click Edit to load the note into the editor and make changes.

    Deleting a Note:
        Similarly, after clicking a note, a prompt will ask if you want to delete the note.
        Click Delete to delete the note permanently.

## Customization

    Window Appearance: You can customize the colors, font sizes, and borders in the code by modifying the PyQt5 styling.
    Taskbar Visibility: The application is designed to stay out of the taskbar by default. It can be configured to appear or hide from the taskbar using the Qt.Tool window flag.

## Troubleshooting

    SQLite database issues: If the database is corrupted or missing, the application will create a new notes.db file automatically when first launched.

## Contributing

Contributions are welcome! If you encounter bugs or have suggestions, feel free to submit issues or pull requests.
## License

This project is licensed under the MIT License.
