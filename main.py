import sys
import sqlite3
import json
import uuid
from datetime import datetime
import threading
import webbrowser
import os

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QLineEdit, 
                             QTextEdit, QMessageBox, QFrame, QScrollArea,
                             QGridLayout, QComboBox, QSlider, QSpinBox)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QPalette, QColor
# Import modules
from subject_selection import SubjectSelection
from calculator import Calculator
from simulations import Simulations
from dotenv import load_dotenv
load_dotenv()

# Debug: Check if API key is loaded
api_key = os.environ.get('OPENAI_API_KEY')
# API key is loaded and available for use

class EducationalApp(QMainWindow):
    def __init__(self):
        super().__init__()
        try:
            self.setWindowTitle("Educational Application")
            self.setGeometry(100, 100, 1200, 800)
            self.setMinimumSize(1000, 600)
            
            # Set up the central widget
            self.central_widget = QWidget()
            self.setCentralWidget(self.central_widget)
            self.main_layout = QVBoxLayout(self.central_widget)
            
            # Initialize database
            self.init_database()
            
            # Load user preferences
            self.load_preferences()
            
            # Current user
            self.current_user = None
            
            # Instantiate modules
            self.subject_selection = SubjectSelection(self)
            self.calculator = Calculator(self)
            self.simulations = Simulations(self)
            
            # Show start screen
            self.show_start_screen()
            
        except Exception as e:
            print(f"Error in __init__: {e}")
            import traceback
            traceback.print_exc()
            raise
        
    def init_database(self):
        """Initialize SQLite database for users and data"""
        self.conn = sqlite3.connect('educational_app.db')
        self.db_cursor = self.conn.cursor()
        
        # Create users table
        self.db_cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                email TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create user_variables table
        self.db_cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_variables (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                variable_name TEXT,
                variable_value TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Create contact_messages table
        self.db_cursor.execute('''
            CREATE TABLE IF NOT EXISTS contact_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                message TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Create calculation_history table
        self.db_cursor.execute('''
            CREATE TABLE IF NOT EXISTS calculation_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                calculation TEXT,
                result TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        self.conn.commit()
        
    def load_preferences(self):
        """Load user preferences from file"""
        try:
            with open('preferences.json', 'r') as f:
                self.preferences = json.load(f)
        except FileNotFoundError:
            self.preferences = {
                'gui_preferences': {
                    'layout': 'default',
                    'theme': 'dark'
                },
                'accessibility': {
                    'colorblind_mode': 'none',
                    'text_size': 'medium',
                    'font_family': 'Arial'
                },
                'volume': 0.7
            }
            self.save_preferences()
            
    def save_preferences(self):
        """Save user preferences to file"""
        with open('preferences.json', 'w') as f:
            json.dump(self.preferences, f, indent=2)
            
    def clear_layout(self):
        """Clear all widgets from the main layout"""
        while self.main_layout.count():
            child = self.main_layout.takeAt(0)
            if child and hasattr(child, 'widget') and child.widget():
                widget = child.widget()
                if widget:
                    widget.deleteLater()
                
    def show_start_screen(self):
        """Display the main start screen"""
        try:
            self.clear_layout()
            
            # Title
            title_label = QLabel("Educational Application")
            title_label.setFont(QFont("Arial", 48, QFont.Bold))
            title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.main_layout.addWidget(title_label)
            
            subtitle_label = QLabel("A-Level Mathematics & Physics Learning Platform")
            subtitle_label.setFont(QFont("Arial", 20))
            subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.main_layout.addWidget(subtitle_label)
            
            # Add some spacing
            self.main_layout.addStretch()
            
            # Buttons frame
            buttons_widget = QWidget()
            buttons_layout = QVBoxLayout(buttons_widget)
            
            # Login/Signup button
            auth_button = QPushButton("Login / Sign Up")
            auth_button.setFont(QFont("Arial", 18))
            auth_button.clicked.connect(self.show_auth_screen)
            buttons_layout.addWidget(auth_button)
            
            # Settings button
            settings_button = QPushButton("Settings")
            settings_button.setFont(QFont("Arial", 18))
            settings_button.clicked.connect(self.show_settings_screen)
            buttons_layout.addWidget(settings_button)
            
            # Contact Us button
            contact_button = QPushButton("Contact Us")
            contact_button.setFont(QFont("Arial", 18))
            contact_button.clicked.connect(self.show_contact_screen)
            buttons_layout.addWidget(contact_button)
            
            self.main_layout.addWidget(buttons_widget)
            
            # Footer
            footer_label = QLabel("© 2024 Educational Application. All rights reserved.")
            footer_label.setFont(QFont("Arial", 12))
            footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.main_layout.addWidget(footer_label)
            
        except Exception as e:
            print(f"Error in show_start_screen: {e}")
            import traceback
            traceback.print_exc()
        
    def show_auth_screen(self):
        """Show authentication screen"""
        self.clear_layout()
        
        # Title
        title_label = QLabel("Login / Sign Up")
        title_label.setFont(QFont("Arial", 36, QFont.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(title_label)
        
        # Auth form
        auth_widget = QWidget()
        auth_layout = QVBoxLayout(auth_widget)
        
        # Username
        username_label = QLabel("Username:")
        self.username_entry = QLineEdit()
        auth_layout.addWidget(username_label)
        auth_layout.addWidget(self.username_entry)
        
        # Password
        password_label = QLabel("Password:")
        self.password_entry = QLineEdit()
        self.password_entry.setEchoMode(QLineEdit.Password)
        auth_layout.addWidget(password_label)
        auth_layout.addWidget(self.password_entry)
        
        # Email
        email_label = QLabel("Email (optional):")
        self.email_entry = QLineEdit()
        auth_layout.addWidget(email_label)
        auth_layout.addWidget(self.email_entry)
        
        # Buttons
        buttons_widget = QWidget()
        buttons_layout = QHBoxLayout(buttons_widget)
        
        login_button = QPushButton("Login")
        login_button.clicked.connect(lambda: self.login_user(
            self.username_entry.text(),
            self.password_entry.text()
        ))
        buttons_layout.addWidget(login_button)
        
        signup_button = QPushButton("Sign Up")
        signup_button.clicked.connect(lambda: self.signup_user(
            self.username_entry.text(),
            self.password_entry.text(),
            self.email_entry.text()
        ))
        buttons_layout.addWidget(signup_button)
        
        forgot_button = QPushButton("Forgot Password")
        forgot_button.clicked.connect(self.show_forgot_password_screen)
        buttons_layout.addWidget(forgot_button)
        
        auth_layout.addWidget(buttons_widget)
        self.main_layout.addWidget(auth_widget)
        
        # Back button
        back_button = QPushButton("Back to Start")
        back_button.clicked.connect(self.show_start_screen)
        self.main_layout.addWidget(back_button)
        
    def login_user(self, username, password):
        """Login user"""
        if not username or not password:
            QMessageBox.critical(self, "Error", "Please enter username and password")
            return
            
        self.db_cursor.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password)
        )
        user = self.db_cursor.fetchone()
        
        if user:
            self.current_user = {
                'id': user[0],
                'username': user[1],
                'email': user[3]
            }
            QMessageBox.information(self, "Success", f"Welcome back, {username}!")
            self.show_main_menu()
        else:
            QMessageBox.critical(self, "Error", "Invalid username or password")
            
    def signup_user(self, username, password, email):
        """Sign up new user"""
        if not username or not password:
            QMessageBox.critical(self, "Error", "Please enter username and password")
            return
            
        try:
            user_id = str(uuid.uuid4())
            self.db_cursor.execute(
                "INSERT INTO users (id, username, password, email) VALUES (?, ?, ?, ?)",
                (user_id, username, password, email)
            )
            self.conn.commit()
            
            self.current_user = {
                'id': user_id,
                'username': username,
                'email': email
            }
            
            QMessageBox.information(self, "Success", f"Account created successfully! Welcome, {username}!")
            self.show_main_menu()
            
        except sqlite3.IntegrityError:
            QMessageBox.critical(self, "Error", "Username already exists")
            
    def show_forgot_password_screen(self):
        """Show forgot password screen"""
        QMessageBox.information(self, "Info", "Password reset feature will be implemented")
        
    def show_main_menu(self):
        """Show main menu after login"""
        self.clear_layout()
        
        # Welcome message
        username = self.current_user.get('username', 'User') if self.current_user else 'User'
        welcome_label = QLabel(f"Welcome, {username}!")
        welcome_label.setFont(QFont("Arial", 32, QFont.Bold))
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(welcome_label)
        
        # Menu buttons
        menu_widget = QWidget()
        menu_layout = QVBoxLayout(menu_widget)
        
        # Subject/Topic Selection button
        subject_button = QPushButton("Subject / Topic Selection")
        subject_button.setFont(QFont("Arial", 18))
        subject_button.clicked.connect(self.show_subject_selection)
        menu_layout.addWidget(subject_button)
        
        # Calculator button
        calculator_button = QPushButton("Calculator")
        calculator_button.setFont(QFont("Arial", 18))
        calculator_button.clicked.connect(self.show_calculator_menu)
        menu_layout.addWidget(calculator_button)
        
        # Interactive Simulations button
        simulations_button = QPushButton("Interactive Simulations")
        simulations_button.setFont(QFont("Arial", 18))
        simulations_button.clicked.connect(self.show_simulations_menu)
        menu_layout.addWidget(simulations_button)
        
        # Help button
        help_button = QPushButton("Help")
        help_button.setFont(QFont("Arial", 18))
        help_button.clicked.connect(self.show_help_screen)
        menu_layout.addWidget(help_button)
        
        # Settings button
        settings_button = QPushButton("Settings")
        settings_button.setFont(QFont("Arial", 18))
        settings_button.clicked.connect(self.show_settings_screen)
        menu_layout.addWidget(settings_button)
        
        self.main_layout.addWidget(menu_widget)
        
        # Logout button
        logout_button = QPushButton("Logout")
        logout_button.clicked.connect(self.logout)
        self.main_layout.addWidget(logout_button)
        
    def logout(self):
        """Logout user"""
        self.current_user = None
        self.show_start_screen()
        
    def show_settings_screen(self):
        """Show settings screen"""
        self.clear_layout()
        
        # Title
        title_label = QLabel("Settings")
        title_label.setFont(QFont("Arial", 36, QFont.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(title_label)
        
        # Settings buttons
        settings_widget = QWidget()
        settings_layout = QVBoxLayout(settings_widget)
        
        # GUI Preferences button
        gui_button = QPushButton("GUI Preferences")
        gui_button.setFont(QFont("Arial", 18))
        gui_button.clicked.connect(self.show_gui_preferences)
        settings_layout.addWidget(gui_button)
        
        # Accessibility Settings button
        accessibility_button = QPushButton("Accessibility Settings")
        accessibility_button.setFont(QFont("Arial", 18))
        accessibility_button.clicked.connect(self.show_accessibility_settings)
        settings_layout.addWidget(accessibility_button)
        
        # Volume button
        volume_button = QPushButton("Volume")
        volume_button.setFont(QFont("Arial", 18))
        volume_button.clicked.connect(self.show_volume_settings)
        settings_layout.addWidget(volume_button)
        
        self.main_layout.addWidget(settings_widget)
        
        # Back button
        back_button = QPushButton("Back")
        back_button.clicked.connect(self.show_start_screen if not self.current_user else self.show_main_menu)
        self.main_layout.addWidget(back_button)
        
    def show_contact_screen(self):
        """Show contact us screen"""
        self.clear_layout()
        
        # Title
        title_label = QLabel("Contact Us")
        title_label.setFont(QFont("Arial", 36, QFont.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(title_label)
        
        # Contact form
        contact_widget = QWidget()
        contact_layout = QVBoxLayout(contact_widget)
        
        # Message label
        message_label = QLabel("Your Message:")
        contact_layout.addWidget(message_label)
        
        # Message text area
        self.message_text = QTextEdit()
        contact_layout.addWidget(self.message_text)
        
        # Send button
        send_button = QPushButton("Send Message")
        send_button.clicked.connect(lambda: self.send_contact_message(self.message_text.toPlainText()))
        contact_layout.addWidget(send_button)
        
        self.main_layout.addWidget(contact_widget)
        
        # Back button
        back_button = QPushButton("Back")
        back_button.clicked.connect(self.show_start_screen)
        self.main_layout.addWidget(back_button)
        
    def send_contact_message(self, message):
        """Send contact message to database"""
        if not message.strip():
            QMessageBox.critical(self, "Error", "Please enter a message")
            return
            
        user_id = self.current_user['id'] if isinstance(self.current_user, dict) else None
        
        self.db_cursor.execute(
            "INSERT INTO contact_messages (user_id, message) VALUES (?, ?)",
            (user_id, message)
        )
        self.conn.commit()
        
        QMessageBox.information(self, "Success", "Message sent successfully!")
        
    def show_subject_selection(self):
        """Show the subject/topic selection screen from the SubjectSelection module."""
        self.subject_selection.show_subject_selection()

    def show_calculator_menu(self):
        """Show the calculator menu from the Calculator module."""
        self.calculator.show_calculator_menu()

    def show_help_screen(self):
        """Stub for help screen navigation."""
        QMessageBox.information(self, "Help", "Help section will be implemented.")

    def show_gui_preferences(self):
        """Stub for GUI Preferences navigation."""
        QMessageBox.information(self, "GUI Preferences", "GUI Preferences section will be implemented.")

    def show_accessibility_settings(self):
        """Stub for Accessibility Settings navigation."""
        QMessageBox.information(self, "Accessibility Settings", "Accessibility Settings section will be implemented.")

    def show_volume_settings(self):
        """Stub for Volume Settings navigation."""
        QMessageBox.information(self, "Volume Settings", "Volume Settings section will be implemented.")

    def show_simulations_menu(self):
        """Show the simulations menu from the Simulations module."""
        self.simulations.show_simulations_menu()
        
    def closeEvent(self, event):
        """Handle application close"""
        if hasattr(self, 'conn'):
            self.conn.close()
        event.accept()

    def get_high_score(self, user_id, topic):
        """Get the high score for a user and topic from the database."""
        variable_name = f"highscore:{topic}"
        self.db_cursor.execute(
            "SELECT variable_value FROM user_variables WHERE user_id = ? AND variable_name = ?",
            (user_id, variable_name)
        )
        row = self.db_cursor.fetchone()
        if row:
            try:
                return int(row[0])
            except Exception:
                return 0
        return 0

    def set_high_score(self, user_id, topic, score):
        """Set the high score for a user and topic in the database."""
        variable_name = f"highscore:{topic}"
        # Check if entry exists
        self.db_cursor.execute(
            "SELECT id FROM user_variables WHERE user_id = ? AND variable_name = ?",
            (user_id, variable_name)
        )
        row = self.db_cursor.fetchone()
        if row:
            self.db_cursor.execute(
                "UPDATE user_variables SET variable_value = ? WHERE id = ?",
                (str(score), row[0])
            )
        else:
            self.db_cursor.execute(
                "INSERT INTO user_variables (user_id, variable_name, variable_value) VALUES (?, ?, ?)",
                (user_id, variable_name, str(score))
            )
        self.conn.commit()

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        
        window = EducationalApp()
        
        window.show()
        
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Error in main: {e}")
        import traceback
        traceback.print_exc() 