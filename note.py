import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, 
    QTextEdit, QLabel, QListWidget, QSizePolicy, QMessageBox
)
from PyQt5.QtCore import Qt

# Database setup
db = sqlite3.connect("notes.db")
cursor = db.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL
)
""")
db.commit()

class NoteApp(QWidget):
    def __init__(self):
        super().__init__()        
        self.initUI()

    def initUI(self):
        # Get rid of window frame
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        
        self.move(45, 30)
        self.setStyleSheet("background-color: rgb(20, 20, 20); color: white;")
        
        # Compact taskbar layout
        self.taskbar = QHBoxLayout()
        self.new_btn = QPushButton("New")
        self.load_btn = QPushButton("Load")
        self.taskbar.addWidget(self.new_btn)
        self.taskbar.addWidget(self.load_btn)

        # Dynamic sections
        self.new_note_section = QWidget()
        self.new_note_section.hide()
        self.load_note_section = QWidget()
        self.load_note_section.hide()

        # New Note Layout
        new_layout = QVBoxLayout()
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Title")
        self.content_input = QTextEdit()
        self.content_input.setPlaceholderText("Write your note here...")
        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.save_note)
        new_layout.addWidget(self.title_input)
        new_layout.addWidget(self.content_input)
        new_layout.addWidget(self.save_btn)
        self.new_note_section.setLayout(new_layout)

        # Load Notes Layout
        load_layout = QVBoxLayout()
        self.note_list = QListWidget()
        self.note_list.itemClicked.connect(self.show_note_options)
        load_layout.addWidget(self.note_list)
        self.load_note_section.setLayout(load_layout)

        # Main Layout
        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.taskbar)
        self.main_layout.addWidget(self.new_note_section)
        self.main_layout.addWidget(self.load_note_section)
        self.setLayout(self.main_layout)

        # Button connections
        self.new_btn.clicked.connect(self.show_new_note_section)
        self.load_btn.clicked.connect(self.show_load_note_section)

        # Window properties
        self.setWindowTitle("Compact Note App")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.resize(50, 25)

    def show_new_note_section(self):
        """Show or hide the new note section."""
        self.new_note_section.setVisible(not self.new_note_section.isVisible())
        self.load_note_section.hide()
        self.adjustSize()

    def show_load_note_section(self):
        """Show or hide the load note section."""
        self.load_note_section.setVisible(not self.load_note_section.isVisible())
        self.new_note_section.hide()
        self.refresh_note_list()
        self.adjustSize()

    def save_note(self):
        """Save the note to the database."""
        title = self.title_input.text().strip()
        content = self.content_input.toPlainText().strip()
        if title and content:
            cursor.execute("INSERT INTO notes (title, content) VALUES (?, ?)", (title, content))
            db.commit()
            self.title_input.clear()
            self.content_input.clear()
            self.new_note_section.hide()
            self.adjustSize()

    def refresh_note_list(self):
        """Refresh the list of notes."""
        self.note_list.clear()
        cursor.execute("SELECT id, title FROM notes")
        for note_id, title in cursor.fetchall():
            self.note_list.addItem(f"{note_id}: {title}")

    def show_note_options(self, item):
        """Show options to load (edit) or delete a note."""
        note_id = item.text().split(":")[0]

        # Create a custom QMessageBox instance
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Note Options")
        msg_box.setText("Do you want to edit or delete this note?")

        # Set the window flags to remove the frame
        msg_box.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)  # Frameless and dialog style

        # Adding custom buttons (Edit, Delete, Cancel)
        edit_button = msg_box.addButton("Edit", QMessageBox.ActionRole)
        delete_button = msg_box.addButton("Delete", QMessageBox.ActionRole)
        cancel_button = msg_box.addButton("Cancel", QMessageBox.RejectRole)

        # Show the QMessageBox and get the user's choice
        msg_box.exec_()

        # Check which button was clicked
        if msg_box.clickedButton() == edit_button:  # Edit the note
            self.edit_note(note_id)
        elif msg_box.clickedButton() == delete_button:  # Delete the note
            self.delete_note(note_id)
        else:  # Cancel the action
            return


    def edit_note(self, note_id):
        """Load the note for editing."""
        cursor.execute("SELECT title, content FROM notes WHERE id = ?", (note_id,))
        title, content = cursor.fetchone()
        self.title_input.setText(title)
        self.content_input.setText(content)
        self.new_note_section.show()
        self.load_note_section.hide()
        self.save_btn.disconnect()  # Disconnect old signal
        self.save_btn.clicked.connect(lambda: self.update_note(note_id))
        self.adjustSize()

    def update_note(self, note_id):
        """Update the note in the database."""
        title = self.title_input.text().strip()
        content = self.content_input.toPlainText().strip()
        if title and content:
            cursor.execute("UPDATE notes SET title = ?, content = ? WHERE id = ?", (title, content, note_id))
            db.commit()
            self.title_input.clear()
            self.content_input.clear()
            self.new_note_section.hide()
            self.refresh_note_list()
            self.save_btn.disconnect()
            self.save_btn.clicked.connect(self.save_note)
            self.adjustSize()

    def delete_note(self, note_id):
        """Delete the note from the database."""
        cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        db.commit()
        self.refresh_note_list()

    def mousePressEvent(self, event):
        """Start dragging the window."""
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_start_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        """Move the window while dragging."""
        if self.dragging and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_start_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        """Stop dragging the window."""
        if event.button() == Qt.LeftButton:
            self.dragging = False
            event.accept()
    
    def keyPressEvent(self, event):
        """Close the app when the Esc key is pressed."""
        if event.key() == Qt.Key_Escape:
            self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NoteApp()
    window.show()
    sys.exit(app.exec_())