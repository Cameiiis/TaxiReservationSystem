# Name: Buisan, Mary Iana Bennel B.
# Date: 12/11/2025
# Description:
# Class List Manager using Object-Oriented Programming (OOP),
# File Handling, and a clean PyQt6 GUI with green Add button and blue Load button.
# Features centered layout with improved styling.

import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


# OOP Classes

class Student:
    def __init__(self, student_id, name, course):
        self.student_id = student_id
        self.name = name
        self.course = course

    def to_string(self):
        return f"{self.student_id},{self.name},{self.course}"


class StudentManager:
    def __init__(self, filename="students.txt"):
        self.filename = filename

    def save_student(self, student):
        # Uses print() to automatically handle line breaks
        with open(self.filename, "a") as file:
            print(student.to_string(), file=file)

    def load_students(self):
        try:
            with open(self.filename, "r") as file:
                return file.read().splitlines()
        except FileNotFoundError:
            return []


# GUI Class

class StudentApp(QWidget):
    def __init__(self):
        super().__init__()
        self.manager = StudentManager()
        self.setWindowTitle("Class List Manager")
        self.setMinimumSize(500, 700)
        
        # Set white background
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """)
        
        self.setup_ui()

    def setup_ui(self):
        """Initialize and setup all UI components"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(15)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        
        # Style for input fields - matching the reference image
        input_style = """
            QLineEdit {
                padding: 15px;
                border: 2px solid #d0d0d0;
                border-radius: 8px;
                background-color: white;
                font-size: 15px;
                color: #333333;
            }
            QLineEdit:focus {
                border: 2px solid #5cb85c;
            }
        """
        
        # Student ID - with green border when focused
        self.txt_id = QLineEdit()
        self.txt_id.setPlaceholderText("Student ID:")
        self.txt_id.setStyleSheet(input_style)
        self.txt_id.setFixedWidth(400)
        self.txt_id.setFixedHeight(50)
        
        # Name
        self.txt_name = QLineEdit()
        self.txt_name.setPlaceholderText("Name:")
        self.txt_name.setStyleSheet(input_style)
        self.txt_name.setFixedWidth(400)
        self.txt_name.setFixedHeight(50)
        
        # Course/Section
        self.txt_course = QLineEdit()
        self.txt_course.setPlaceholderText("Course / Section:")
        self.txt_course.setStyleSheet(input_style)
        self.txt_course.setFixedWidth(400)
        self.txt_course.setFixedHeight(50)
        
        # Add Student Button - GREEN
        self.btn_add = QPushButton("Add Student")
        self.btn_add.setFixedSize(400, 50)
        self.btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_add.setStyleSheet("""
            QPushButton {
                background-color: #5cb85c;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4cae4c;
            }
            QPushButton:pressed {
                background-color: #449d44;
            }
        """)
        
        # Load Students Button - BLUE
        self.btn_load = QPushButton("Load Students")
        self.btn_load.setFixedSize(400, 50)
        self.btn_load.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_load.setStyleSheet("""
            QPushButton {
                background-color: #5cb8e6;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #46a8d6;
            }
            QPushButton:pressed {
                background-color: #3498db;
            }
        """)
        
        # Text display area
        self.display = QTextEdit()
        self.display.setReadOnly(True)
        self.display.setFixedSize(400, 300)
        self.display.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.display.setStyleSheet("""
            QTextEdit {
                border: 3px solid #d0d0d0;
                border-radius: 8px;
                padding: 15px;
                background-color: white;
                font-size: 14px;
                color: #333333;
                line-height: 1.5;
            }
            QScrollBar:vertical {
                border: none;
                background: #f0f0f0;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #5cb8e6;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #3498db;
            }
        """)
        
        # Add all widgets to layout
        main_layout.addWidget(self.txt_id)
        main_layout.addWidget(self.txt_name)
        main_layout.addWidget(self.txt_course)
        main_layout.addWidget(self.btn_add)
        main_layout.addWidget(self.btn_load)
        main_layout.addWidget(self.display)
        
        main_layout.addStretch()
        
        self.setLayout(main_layout)
        
        # Connect signals
        self.btn_add.clicked.connect(self.add_student)
        self.btn_load.clicked.connect(self.load_students)

    def add_student(self):
        """Add a student"""
        student = Student(
            self.txt_id.text(),
            self.txt_name.text(),
            self.txt_course.text()
        )

        self.manager.save_student(student)

        # Clear inputs after saving
        self.txt_id.clear()
        self.txt_name.clear()
        self.txt_course.clear()

    def load_students(self):
        """Load and display students"""
        self.display.clear()
        students = self.manager.load_students()
        
        # Add decorative top border
        self.display.append("╔" + "═" * 48 + "╗")
        self.display.append("║" + " " * 16 + "STUDENT RECORDS" + " " * 17 + "║")
        self.display.append("╠" + "═" * 48 + "╣")
        
        for student in students:
            self.display.append("║ " + student.ljust(46) + " ║")
        
        # Add decorative bottom border
        self.display.append("╚" + "═" * 48 + "╝")


# Main

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StudentApp()
    window.show()
    sys.exit(app.exec())