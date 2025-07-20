from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QLineEdit, QTextEdit, QMessageBox, 
                             QGridLayout, QComboBox, QScrollArea, QSlider,
                             QSpinBox, QDoubleSpinBox, QTabWidget, QFrame,
                             QGroupBox, QCheckBox, QRadioButton)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont, QPainter, QPen, QBrush, QColor
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import random

class InteractiveSimulation(QWidget):
    """Base class for interactive simulations"""
    
    def __init__(self, parent_app):
        super().__init__()
        self.parent_app = parent_app
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_simulation)
        self.is_running = False
        
    def start_simulation(self):
        """Start the simulation"""
        self.is_running = True
        self.timer.start(50)  # Update every 50ms
        
    def stop_simulation(self):
        """Stop the simulation"""
        self.is_running = False
        self.timer.stop()
        
    def update_simulation(self):
        """Update simulation state - to be overridden"""
        pass

class ProjectileMotionSimulation(InteractiveSimulation):
    """Interactive projectile motion simulation"""
    
    def __init__(self, parent_app):
        super().__init__(parent_app)
        self.setup_ui()
        self.reset_simulation()
        
    def setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Projectile Motion Simulation")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Control panel
        control_group = QGroupBox("Simulation Controls")
        control_layout = QGridLayout(control_group)
        
        # Initial velocity
        control_layout.addWidget(QLabel("Initial Velocity (m/s):"), 0, 0)
        self.velocity_input = QDoubleSpinBox()
        self.velocity_input.setRange(1, 100)
        self.velocity_input.setValue(20)
        control_layout.addWidget(self.velocity_input, 0, 1)
        
        # Angle
        control_layout.addWidget(QLabel("Angle (degrees):"), 1, 0)
        self.angle_input = QDoubleSpinBox()
        self.angle_input.setRange(0, 90)
        self.angle_input.setValue(45)
        control_layout.addWidget(self.angle_input, 1, 1)
        
        # Gravity
        control_layout.addWidget(QLabel("Gravity (m/s²):"), 2, 0)
        self.gravity_input = QDoubleSpinBox()
        self.gravity_input.setRange(1, 20)
        self.gravity_input.setValue(9.81)
        control_layout.addWidget(self.gravity_input, 2, 1)
        
        # Buttons
        self.fire_button = QPushButton("Fire!")
        self.fire_button.clicked.connect(self.fire_projectile)
        control_layout.addWidget(self.fire_button, 3, 0)
        
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_simulation)
        control_layout.addWidget(self.reset_button, 3, 1)
        
        layout.addWidget(control_group)
        
        # Results display
        self.results_text = QTextEdit()
        self.results_text.setMaximumHeight(100)
        layout.addWidget(self.results_text)
        
        # Canvas for drawing
        self.canvas = ProjectileCanvas()
        layout.addWidget(self.canvas)
        
    def fire_projectile(self):
        """Fire the projectile"""
        self.reset_simulation()
        
        # Get parameters
        v0 = self.velocity_input.value()
        angle = math.radians(self.angle_input.value())
        g = self.gravity_input.value()
        
        # Calculate components
        self.v0x = v0 * math.cos(angle)
        self.v0y = v0 * math.sin(angle)
        self.g = g
        
        # Calculate trajectory
        self.time_of_flight = 2 * self.v0y / self.g
        self.range_distance = self.v0x * self.time_of_flight
        self.max_height = (self.v0y ** 2) / (2 * self.g)
        
        # Update canvas
        self.canvas.set_trajectory(v0, angle, g)
        
        # Display results
        results = f"""
Projectile Motion Results:
Initial Velocity: {v0:.2f} m/s
Angle: {self.angle_input.value():.1f}°
Time of Flight: {self.time_of_flight:.2f} s
Range: {self.range_distance:.2f} m
Maximum Height: {self.max_height:.2f} m
        """
        self.results_text.setText(results)
        
        # Start animation
        self.start_simulation()
        
    def reset_simulation(self):
        """Reset the simulation"""
        self.stop_simulation()
        self.canvas.clear()
        self.results_text.clear()
        
    def update_simulation(self):
        """Update simulation animation"""
        if self.is_running:
            self.canvas.update_animation()

class ProjectileCanvas(QWidget):
    """Canvas for drawing projectile motion"""
    
    def __init__(self):
        super().__init__()
        self.setMinimumSize(400, 300)
        self.trajectory_points = []
        self.current_time = 0
        self.time_step = 0.05
        
    def set_trajectory(self, v0, angle, g):
        """Set trajectory parameters"""
        self.v0 = v0
        self.angle = angle
        self.g = g
        self.v0x = v0 * math.cos(angle)
        self.v0y = v0 * math.sin(angle)
        self.time_of_flight = 2 * self.v0y / self.g
        self.current_time = 0
        
        # Calculate trajectory points
        self.trajectory_points = []
        t = 0
        while t <= self.time_of_flight:
            x = self.v0x * t
            y = self.v0y * t - 0.5 * self.g * t * t
            self.trajectory_points.append((x, y))
            t += self.time_step
            
    def update_animation(self):
        """Update animation frame"""
        if self.current_time <= self.time_of_flight:
            self.current_time += self.time_step
            self.update()
            
    def clear(self):
        """Clear the canvas"""
        self.trajectory_points = []
        self.current_time = 0
        self.update()
        
    def paintEvent(self, event):
        """Paint the canvas"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Set up coordinate system
        width = self.width()
        height = self.height()
        
        # Find scale factors
        if self.trajectory_points:
            max_x = max(point[0] for point in self.trajectory_points)
            max_y = max(point[1] for point in self.trajectory_points)
            scale_x = (width - 50) / max_x if max_x > 0 else 1
            scale_y = (height - 50) / max_y if max_y > 0 else 1
            scale = min(scale_x, scale_y)
        else:
            scale = 1
            
        # Draw ground
        painter.setPen(QPen(QColor(0, 0, 0), 2))  # Black
        painter.drawLine(25, height - 25, width - 25, height - 25)
        
        # Draw axes
        painter.setPen(QPen(QColor(0, 0, 0), 2))  # Black
        painter.drawLine(25, height - 25, width - 25, height - 25)  # X-axis
        painter.drawLine(25, 25, 25, height - 25)  # Y-axis
        
        # Draw trajectory
        if self.trajectory_points:
            painter.setPen(QPen(QColor(0, 0, 255), 2))  # Blue
            for i in range(1, len(self.trajectory_points)):
                x1, y1 = self.trajectory_points[i-1]
                x2, y2 = self.trajectory_points[i]
                painter.drawLine(
                    int(x1 * scale_x + 25),
                    int(height - (y1 * scale_y + 25)),
                    int(x2 * scale_x + 25),
                    int(height - (y2 * scale_y + 25))
                )
        
        # Draw projectile
        if self.current_time <= self.time_of_flight:
            x = self.v0x * self.current_time
            y = self.v0y * self.current_time - 0.5 * self.g * self.current_time * self.current_time
            
            painter.setPen(QPen(QColor(255, 0, 0), 1))  # Red
            painter.setBrush(QBrush(QColor(255, 0, 0)))  # Red
            painter.drawEllipse(
                int(x * scale_x + 25 - 5),
                int(height - (y * scale_y + 25) - 5),
                10, 10
            )

class PendulumSimulation(InteractiveSimulation):
    """Simple pendulum simulation"""
    
    def __init__(self, parent_app):
        super().__init__(parent_app)
        self.setup_ui()
        self.reset_simulation()
        
    def setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Simple Pendulum Simulation")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Control panel
        control_group = QGroupBox("Pendulum Parameters")
        control_layout = QGridLayout(control_group)
        
        # Length
        control_layout.addWidget(QLabel("Length (m):"), 0, 0)
        self.length_input = QDoubleSpinBox()
        self.length_input.setRange(0.1, 10)
        self.length_input.setValue(1.0)
        self.length_input.valueChanged.connect(self.update_period)
        control_layout.addWidget(self.length_input, 0, 1)
        
        # Initial angle
        control_layout.addWidget(QLabel("Initial Angle (degrees):"), 1, 0)
        self.angle_input = QDoubleSpinBox()
        self.angle_input.setRange(0, 90)
        self.angle_input.setValue(30)
        control_layout.addWidget(self.angle_input, 1, 1)
        
        # Gravity
        control_layout.addWidget(QLabel("Gravity (m/s²):"), 2, 0)
        self.gravity_input = QDoubleSpinBox()
        self.gravity_input.setRange(1, 20)
        self.gravity_input.setValue(9.81)
        self.gravity_input.valueChanged.connect(self.update_period)
        control_layout.addWidget(self.gravity_input, 2, 1)
        
        # Buttons
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_pendulum)
        control_layout.addWidget(self.start_button, 3, 0)
        
        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_pendulum)
        control_layout.addWidget(self.stop_button, 3, 1)
        
        layout.addWidget(control_group)
        
        # Results display
        self.results_text = QTextEdit()
        self.results_text.setMaximumHeight(100)
        layout.addWidget(self.results_text)
        
        # Canvas for drawing
        self.canvas = PendulumCanvas()
        layout.addWidget(self.canvas)
        
        # Initialize results
        self.update_period()
        
    def update_period(self):
        """Update period calculation"""
        length = self.length_input.value()
        g = self.gravity_input.value()
        
        # Period = 2π√(L/g)
        period = 2 * math.pi * math.sqrt(length / g)
        frequency = 1 / period
        
        results = f"""
Pendulum Results:
Length: {length:.2f} m
Period: {period:.3f} s
Frequency: {frequency:.3f} Hz
        """
        self.results_text.setText(results)
        
    def start_pendulum(self):
        """Start pendulum simulation"""
        length = self.length_input.value()
        angle = math.radians(self.angle_input.value())
        g = self.gravity_input.value()
        
        self.canvas.set_pendulum(length, angle, g)
        self.start_simulation()
        
    def stop_pendulum(self):
        """Stop pendulum simulation"""
        self.stop_simulation()
        
    def update_simulation(self):
        """Update pendulum animation"""
        if self.is_running:
            self.canvas.update_animation()

class PendulumCanvas(QWidget):
    """Canvas for drawing pendulum"""
    
    def __init__(self):
        super().__init__()
        self.setMinimumSize(400, 400)
        self.length = 1.0
        self.angle = 0
        self.angular_velocity = 0
        self.g = 9.81
        self.time = 0
        
    def set_pendulum(self, length, initial_angle, g):
        """Set pendulum parameters"""
        self.length = length
        self.angle = initial_angle
        self.angular_velocity = 0
        self.g = g
        self.time = 0
        
    def update_animation(self):
        """Update pendulum animation"""
        # Simple harmonic motion approximation
        omega = math.sqrt(self.g / self.length)
        self.time += 0.05
        
        # Angular displacement: θ = θ₀ cos(ωt)
        self.angle = self.angle * math.cos(omega * self.time)
        self.update()
        
    def paintEvent(self, event):
        """Paint the pendulum"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        width = self.width()
        height = self.height()
        
        # Pivot point (center top)
        pivot_x = width // 2
        pivot_y = 50
        
        # Scale factor
        scale = min(width, height) * 0.3
        
        # Bob position
        bob_x = pivot_x + scale * self.length * math.sin(self.angle)
        bob_y = pivot_y + scale * self.length * math.cos(self.angle)
        
        # Draw string
        painter.setPen(QPen(QColor(0, 0, 0), 2))  # Black
        painter.drawLine(int(pivot_x), int(pivot_y), int(bob_x), int(bob_y))
        
        # Draw pivot
        painter.setBrush(QBrush(QColor(128, 128, 128)))  # Gray
        painter.setPen(QPen(QColor(0, 0, 0), 1))  # Black
        painter.drawEllipse(int(pivot_x - 10), int(pivot_y - 10), 20, 20)
        
        # Draw bob
        painter.setBrush(QBrush(QColor(255, 0, 0)))  # Red
        painter.setPen(QPen(QColor(0, 0, 0), 1))  # Black
        painter.drawEllipse(int(bob_x - 15), int(bob_y - 15), 30, 30)

class CircuitSimulation(InteractiveSimulation):
    """Electric circuit simulation"""
    
    def __init__(self, parent_app):
        super().__init__(parent_app)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Electric Circuit Simulation")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Circuit type selection
        circuit_group = QGroupBox("Circuit Type")
        circuit_layout = QVBoxLayout(circuit_group)
        
        self.series_radio = QRadioButton("Series Circuit")
        self.parallel_radio = QRadioButton("Parallel Circuit")
        self.series_radio.setChecked(True)
        
        circuit_layout.addWidget(self.series_radio)
        circuit_layout.addWidget(self.parallel_radio)
        layout.addWidget(circuit_group)
        
        # Component values
        values_group = QGroupBox("Component Values")
        values_layout = QGridLayout(values_group)
        
        # Voltage
        values_layout.addWidget(QLabel("Voltage (V):"), 0, 0)
        self.voltage_input = QDoubleSpinBox()
        self.voltage_input.setRange(1, 100)
        self.voltage_input.setValue(12)
        self.voltage_input.valueChanged.connect(self.calculate_circuit)
        values_layout.addWidget(self.voltage_input, 0, 1)
        
        # Resistors
        values_layout.addWidget(QLabel("R₁ (Ω):"), 1, 0)
        self.r1_input = QDoubleSpinBox()
        self.r1_input.setRange(0.1, 1000)
        self.r1_input.setValue(10)
        self.r1_input.valueChanged.connect(self.calculate_circuit)
        values_layout.addWidget(self.r1_input, 1, 1)
        
        values_layout.addWidget(QLabel("R₂ (Ω):"), 2, 0)
        self.r2_input = QDoubleSpinBox()
        self.r2_input.setRange(0.1, 1000)
        self.r2_input.setValue(20)
        self.r2_input.valueChanged.connect(self.calculate_circuit)
        values_layout.addWidget(self.r2_input, 2, 1)
        
        values_layout.addWidget(QLabel("R₃ (Ω):"), 3, 0)
        self.r3_input = QDoubleSpinBox()
        self.r3_input.setRange(0.1, 1000)
        self.r3_input.setValue(30)
        self.r3_input.valueChanged.connect(self.calculate_circuit)
        values_layout.addWidget(self.r3_input, 3, 1)
        
        layout.addWidget(values_group)
        
        # Results display
        self.results_text = QTextEdit()
        self.results_text.setMaximumHeight(150)
        layout.addWidget(self.results_text)
        
        # Canvas for circuit diagram
        self.canvas = CircuitCanvas()
        layout.addWidget(self.canvas)
        
        # Connect radio buttons
        self.series_radio.toggled.connect(self.calculate_circuit)
        self.parallel_radio.toggled.connect(self.calculate_circuit)
        
        # Initial calculation
        self.calculate_circuit()
        
    def calculate_circuit(self):
        """Calculate circuit parameters"""
        voltage = self.voltage_input.value()
        r1 = self.r1_input.value()
        r2 = self.r2_input.value()
        r3 = self.r3_input.value()
        
        if self.series_radio.isChecked():
            # Series circuit
            total_resistance = r1 + r2 + r3
            current = voltage / total_resistance
            power = voltage * current
            
            results = f"""
Series Circuit Results:
Voltage: {voltage:.2f} V
R₁: {r1:.2f} Ω
R₂: {r2:.2f} Ω
R₃: {r3:.2f} Ω
Total Resistance: {total_resistance:.2f} Ω
Current: {current:.3f} A
Power: {power:.3f} W

Voltage drops:
V₁ = {current * r1:.2f} V
V₂ = {current * r2:.2f} V
V₃ = {current * r3:.2f} V
            """
        else:
            # Parallel circuit
            total_resistance = 1 / (1/r1 + 1/r2 + 1/r3)
            current = voltage / total_resistance
            power = voltage * current
            
            # Individual currents
            i1 = voltage / r1
            i2 = voltage / r2
            i3 = voltage / r3
            
            results = f"""
Parallel Circuit Results:
Voltage: {voltage:.2f} V
R₁: {r1:.2f} Ω
R₂: {r2:.2f} Ω
R₃: {r3:.2f} Ω
Total Resistance: {total_resistance:.2f} Ω
Total Current: {current:.3f} A
Power: {power:.3f} W

Individual currents:
I₁ = {i1:.3f} A
I₂ = {i2:.3f} A
I₃ = {i3:.3f} A
            """
        
        self.results_text.setText(results)
        
        # Update canvas
        self.canvas.set_circuit(self.series_radio.isChecked(), voltage, r1, r2, r3)

class CircuitCanvas(QWidget):
    """Canvas for drawing circuit diagrams"""
    
    def __init__(self):
        super().__init__()
        self.setMinimumSize(400, 200)
        self.is_series = True
        self.voltage = 12
        self.r1 = 10
        self.r2 = 20
        self.r3 = 30
        
    def set_circuit(self, is_series, voltage, r1, r2, r3):
        """Set circuit parameters"""
        self.is_series = is_series
        self.voltage = voltage
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3
        self.update()
        
    def paintEvent(self, event):
        """Paint the circuit diagram"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        width = self.width()
        height = self.height()
        
        if self.is_series:
            self.draw_series_circuit(painter, width, height)
        else:
            self.draw_parallel_circuit(painter, width, height)
            
    def draw_series_circuit(self, painter, width, height):
        """Draw series circuit"""
        # Battery
        painter.setPen(QPen(QColor(0, 0, 0), 2))  # Black
        painter.drawLine(50, height//2, 80, height//2)
        painter.drawLine(80, height//2 - 20, 80, height//2 + 20)
        painter.drawLine(90, height//2 - 20, 90, height//2 + 20)
        painter.drawLine(90, height//2, 120, height//2)
        
        # Resistors
        painter.drawLine(120, height//2, 180, height//2)
        painter.drawRect(180, height//2 - 10, 40, 20)
        painter.drawText(190, height//2 + 5, f"R₁={self.r1}Ω")
        
        painter.drawLine(220, height//2, 280, height//2)
        painter.drawRect(280, height//2 - 10, 40, 20)
        painter.drawText(290, height//2 + 5, f"R₂={self.r2}Ω")
        
        painter.drawLine(320, height//2, 380, height//2)
        painter.drawRect(380, height//2 - 10, 40, 20)
        painter.drawText(390, height//2 + 5, f"R₃={self.r3}Ω")
        
        painter.drawLine(420, height//2, 450, height//2)
        
        # Voltage label
        painter.drawText(60, height//2 - 30, f"V={self.voltage}V")
        
    def draw_parallel_circuit(self, painter, width, height):
        """Draw parallel circuit"""
        # Battery
        painter.setPen(QPen(QColor(0, 0, 0), 2))  # Black
        painter.drawLine(50, height//2, 80, height//2)
        painter.drawLine(80, height//2 - 20, 80, height//2 + 20)
        painter.drawLine(90, height//2 - 20, 90, height//2 + 20)
        painter.drawLine(90, height//2, 120, height//2)
        
        # Main line
        painter.drawLine(120, height//2, 450, height//2)
        
        # Parallel branches
        # Branch 1
        painter.drawLine(200, height//2, 200, height//2 - 40)
        painter.drawRect(200, height//2 - 50, 40, 20)
        painter.drawText(210, height//2 - 35, f"R₁={self.r1}Ω")
        painter.drawLine(240, height//2 - 40, 240, height//2)
        
        # Branch 2
        painter.drawLine(300, height//2, 300, height//2 - 40)
        painter.drawRect(300, height//2 - 50, 40, 20)
        painter.drawText(310, height//2 - 35, f"R₂={self.r2}Ω")
        painter.drawLine(340, height//2 - 40, 340, height//2)
        
        # Branch 3
        painter.drawLine(400, height//2, 400, height//2 - 40)
        painter.drawRect(400, height//2 - 50, 40, 20)
        painter.drawText(410, height//2 - 35, f"R₃={self.r3}Ω")
        painter.drawLine(440, height//2 - 40, 440, height//2)
        
        # Voltage label
        painter.drawText(60, height//2 - 30, f"V={self.voltage}V")

class Simulations:
    """Main simulations class"""
    
    def __init__(self, parent_app):
        self.parent_app = parent_app
        
    def show_simulations_menu(self):
        """Show simulations menu"""
        self.parent_app.clear_layout()
        
        # Title
        title_label = QLabel("Interactive Simulations")
        title_label.setFont(QFont("Arial", 36, QFont.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.parent_app.main_layout.addWidget(title_label)
        
        # Simulations buttons
        sim_widget = QWidget()
        sim_layout = QVBoxLayout(sim_widget)
        
        # Physics simulations
        physics_label = QLabel("Physics Simulations")
        physics_label.setFont(QFont("Arial", 20, QFont.Bold))
        sim_layout.addWidget(physics_label)
        
        projectile_button = QPushButton("Projectile Motion")
        projectile_button.setFont(QFont("Arial", 16))
        projectile_button.clicked.connect(self.show_projectile_simulation)
        sim_layout.addWidget(projectile_button)
        
        pendulum_button = QPushButton("Simple Pendulum")
        pendulum_button.setFont(QFont("Arial", 16))
        pendulum_button.clicked.connect(self.show_pendulum_simulation)
        sim_layout.addWidget(pendulum_button)
        
        circuit_button = QPushButton("Electric Circuit")
        circuit_button.setFont(QFont("Arial", 16))
        circuit_button.clicked.connect(self.show_circuit_simulation)
        sim_layout.addWidget(circuit_button)
        
        self.parent_app.main_layout.addWidget(sim_widget)
        
        # Back button
        back_button = QPushButton("Back to Main Menu")
        back_button.clicked.connect(self.parent_app.show_main_menu)
        self.parent_app.main_layout.addWidget(back_button)
        
    def show_projectile_simulation(self):
        """Show projectile motion simulation"""
        self.parent_app.clear_layout()
        
        simulation = ProjectileMotionSimulation(self.parent_app)
        self.parent_app.main_layout.addWidget(simulation)
        
        # Back button
        back_button = QPushButton("Back to Simulations")
        back_button.clicked.connect(self.show_simulations_menu)
        self.parent_app.main_layout.addWidget(back_button)
        
    def show_pendulum_simulation(self):
        """Show pendulum simulation"""
        self.parent_app.clear_layout()
        
        simulation = PendulumSimulation(self.parent_app)
        self.parent_app.main_layout.addWidget(simulation)
        
        # Back button
        back_button = QPushButton("Back to Simulations")
        back_button.clicked.connect(self.show_simulations_menu)
        self.parent_app.main_layout.addWidget(back_button)
        
    def show_circuit_simulation(self):
        """Show circuit simulation"""
        self.parent_app.clear_layout()
        
        simulation = CircuitSimulation(self.parent_app)
        self.parent_app.main_layout.addWidget(simulation)
        
        # Back button
        back_button = QPushButton("Back to Simulations")
        back_button.clicked.connect(self.show_simulations_menu)
        self.parent_app.main_layout.addWidget(back_button) 