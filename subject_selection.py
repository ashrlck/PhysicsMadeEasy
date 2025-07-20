from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QLineEdit, QScrollArea, QMessageBox,
                             QTabWidget, QTextEdit, QFrame, QGridLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import json
import math
import os
try:
    import openai
    openai_available = True
except ImportError:
    openai_available = False

class SubjectSelection:
    def __init__(self, parent_app):
        self.parent_app = parent_app
        self.current_subject = None
        self.current_topic = None
        
        # A-Level Mathematics topics
        self.math_topics = {
            "Pure Mathematics": [
                "Algebra and Functions",
                "Coordinate Geometry",
                "Sequences and Series",
                "Differentiation",
                "Integration",
                "Trigonometry",
                "Exponentials and Logarithms",
                "Vectors",
                "Proof",
                "Numerical Methods"
            ],
            "Mechanics": [
                "Kinematics",
                "Forces and Newton's Laws",
                "Moments",
                "Energy and Work",
                "Collisions",
                "Circular Motion",
                "Simple Harmonic Motion"
            ],
            "Statistics": [
                "Data Presentation",
                "Probability",
                "Discrete Random Variables",
                "Binomial Distribution",
                "Normal Distribution",
                "Hypothesis Testing",
                "Correlation and Regression"
            ]
        }
        
        # A-Level Physics topics
        self.physics_topics = {
            "Mechanics": [
                "Motion and Forces",
                "Work, Energy and Power",
                "Momentum and Impulse",
                "Circular Motion",
                "Simple Harmonic Motion",
                "Gravitational Fields"
            ],
            "Electricity": [
                "Electric Current",
                "Resistance and Resistivity",
                "Kirchhoff's Laws",
                "Capacitors",
                "Magnetic Fields",
                "Electromagnetic Induction"
            ],
            "Waves": [
                "Wave Properties",
                "Interference and Diffraction",
                "Standing Waves",
                "Sound Waves",
                "Light and Optics",
                "Polarisation"
            ],
            "Thermal Physics": [
                "Temperature and Heat",
                "Ideal Gases",
                "Thermodynamics",
                "Heat Engines",
                "Entropy"
            ],
            "Modern Physics": [
                "Quantum Physics",
                "Photoelectric Effect",
                "Wave-Particle Duality",
                "Nuclear Physics",
                "Radioactivity",
                "Particle Physics"
            ]
        }
        
        # Topic-specific calculators and tools
        self.topic_tools = {
            "Differentiation": ["Derivative Calculator", "Tangent/Normal Finder", "Stationary Point Finder"],
            "Integration": ["Integral Calculator", "Area Under Curve Tool", "Volume of Revolution Calculator"],
            "Trigonometry": ["Trig Equation Solver", "Unit Circle Visualizer", "Triangle Calculator"],
            "Exponentials and Logarithms": ["Logarithm Calculator", "Exponential Equation Solver", "Growth/Decay Model Tool"],
            "Vectors": ["Vector Calculator", "Dot Product Calculator", "Vector Visualizer"],
            "Proof": ["Induction Proof Helper", "Divisibility Checker", "Inequality Verifier"],
            "Numerical Methods": ["Newton-Raphson Calculator", "Trapezium Rule Calculator", "Error Estimator"],
            "Sequences and Series": ["Arithmetic Series Calculator", "Geometric Series Calculator", "Sequence Visualizer"],
            "Motion and Forces": ["Kinematics Calculator", "Force Calculator", "Energy Calculator"],
            "Electricity": ["Circuit Calculator", "Ohm's Law Calculator", "Power Calculator"],
            "Waves": ["Wave Calculator", "Interference Calculator", "Doppler Effect"],
            "Statistics": ["Probability Calculator", "Distribution Calculator", "Hypothesis Test"],
            "Algebra and Functions": ["Quadratic Equation Solver", "Graph Plotter", "Simultaneous Equation Solver"],
            "Coordinate Geometry": ["Line Equation Calculator", "Distance Calculator", "Circle Equation Tool"]
        }
        
        # Mapping of tool names to their corresponding formulas
        self.tool_to_formula_mapping = {
            # Differentiation tools
            "Derivative Calculator": "Power Rule",
            "Tangent/Normal Finder": "Power Rule", 
            "Stationary Point Finder": "Power Rule",
            
            # Integration tools
            "Integral Calculator": "Power Rule",
            "Area Under Curve Tool": "Power Rule",
            "Volume of Revolution Calculator": "Power Rule",
            
            # Trigonometry tools
            "Trig Equation Solver": "Sine Rule",
            "Unit Circle Visualizer": "Sine Rule",
            "Triangle Calculator": "Sine Rule",
            
            # Exponentials and Logarithms tools
            "Logarithm Calculator": "Laws of Logs",
            "Exponential Equation Solver": "Laws of Logs",
            "Growth/Decay Model Tool": "Laws of Logs",
            
            # Vectors tools
            "Vector Calculator": "Magnitude",
            "Dot Product Calculator": "Magnitude",
            "Vector Visualizer": "Magnitude",
            
            # Proof tools
            "Induction Proof Helper": "Proof by Contradiction",
            "Divisibility Checker": "Proof by Contradiction",
            "Inequality Verifier": "Proof by Contradiction",
            
            # Numerical Methods tools
            "Newton-Raphson Calculator": "Newton-Raphson",
            "Trapezium Rule Calculator": "Newton-Raphson",
            "Error Estimator": "Newton-Raphson",
            
            # Sequences and Series tools
            "Arithmetic Series Calculator": "Arithmetic nth Term",
            "Geometric Series Calculator": "Arithmetic nth Term",
            "Sequence Visualizer": "Arithmetic nth Term",
            
            # Motion and Forces tools
            "Kinematics Calculator": "SUVAT (v = u + at)",
            "Force Calculator": "Newton's Second Law",
            "Energy Calculator": "Kinetic Energy",
            
            # Electricity tools
            "Circuit Calculator": "Ohm's Law",
            "Ohm's Law Calculator": "Ohm's Law",
            "Power Calculator": "Ohm's Law",
            
            # Waves tools
            "Wave Calculator": "Wave Speed",
            "Interference Calculator": "Double Slit",
            "Doppler Effect": "Wave Speed",
            
            # Statistics tools
            "Probability Calculator": "Probability",
            "Distribution Calculator": "Binomial Probability",
            "Hypothesis Test": "Test Statistic",
            
            # Algebra and Functions tools
            "Quadratic Equation Solver": "Quadratic Formula",
            "Graph Plotter": "Quadratic Formula",
            "Simultaneous Equation Solver": "Quadratic Formula",
            
            # Coordinate Geometry tools
            "Line Equation Calculator": "Distance Between Points",
            "Distance Calculator": "Distance Between Points",
            "Circle Equation Tool": "Distance Between Points"
        }
        
    def show_subject_selection(self):
        """Show subject selection screen"""
        self.parent_app.clear_layout()
        
        # Title
        title_label = QLabel("Select Subject")
        title_label.setFont(QFont("Arial", 36, QFont.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.parent_app.main_layout.addWidget(title_label)
        
        # Subject buttons
        subject_widget = QWidget()
        subject_layout = QVBoxLayout(subject_widget)
        
        # Mathematics button
        math_button = QPushButton("Mathematics")
        math_button.setFont(QFont("Arial", 24))
        math_button.clicked.connect(lambda: self.select_subject("Mathematics"))
        subject_layout.addWidget(math_button)
        
        # Physics button
        physics_button = QPushButton("Physics")
        physics_button.setFont(QFont("Arial", 24))
        physics_button.clicked.connect(lambda: self.select_subject("Physics"))
        subject_layout.addWidget(physics_button)
        
        self.parent_app.main_layout.addWidget(subject_widget)
        
        # Back button
        back_button = QPushButton("Back to Main Menu")
        back_button.clicked.connect(self.parent_app.show_main_menu)
        self.parent_app.main_layout.addWidget(back_button)
        
    def select_subject(self, subject):
        """Select a subject and show topics"""
        self.current_subject = subject
        self.show_topic_selection()
        
    def show_topic_selection(self):
        """Show topic selection screen"""
        self.parent_app.clear_layout()
        
        # Title
        title_label = QLabel(f"{self.current_subject} Topics")
        title_label.setFont(QFont("Arial", 36, QFont.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.parent_app.main_layout.addWidget(title_label)
        
        # Search frame
        search_widget = QWidget()
        search_layout = QHBoxLayout(search_widget)
        
        search_label = QLabel("Search Topics:")
        search_layout.addWidget(search_label)
        
        self.search_entry = QLineEdit()
        self.search_entry.textChanged.connect(self.filter_topics)
        search_layout.addWidget(self.search_entry)
        
        self.parent_app.main_layout.addWidget(search_widget)
        
        # Topics scroll area
        self.scroll_area = QScrollArea()
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        
        # Get topics based on subject
        if self.current_subject == "Mathematics":
            topics_dict = self.math_topics
        else:
            topics_dict = self.physics_topics
            
        # Create topic buttons
        for category, topics in topics_dict.items():
            # Category label
            category_title = category if isinstance(category, str) else ""
            category_label = QLabel(category_title)
            category_label.setFont(QFont("Arial", 20, QFont.Bold))
            category_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.scroll_layout.addWidget(category_label)
            
            # Topics in category
            for topic in topics:
                topic_button = QPushButton(topic)
                topic_button.clicked.connect(lambda checked, t=topic: self.select_topic(t))
                self.scroll_layout.addWidget(topic_button)
                
        self.scroll_area.setWidget(self.scroll_widget)
        self.parent_app.main_layout.addWidget(self.scroll_area)
        
        # Back button
        back_button = QPushButton("Back to Subjects")
        back_button.clicked.connect(self.show_subject_selection)
        self.parent_app.main_layout.addWidget(back_button)
    
    def filter_topics(self):
        """Filter topics based on search text"""
        search_text = self.search_entry.text().lower()
        
        # Clear existing widgets
        while self.scroll_layout.count():
            child = self.scroll_layout.takeAt(0)
            widget = child.widget() if child is not None else None
            if widget is not None:
                widget.deleteLater()
        
        # Get topics based on subject
        if self.current_subject == "Mathematics":
            topics_dict = self.math_topics
        else:
            topics_dict = self.physics_topics
            
        # Recreate topic buttons with filter
        for category, topics in topics_dict.items():
            # Check if category or any topic matches search
            category_matches = search_text in category.lower()
            matching_topics = [topic for topic in topics if search_text in topic.lower()]
            
            if category_matches or matching_topics:
                # Category label
                category_title = category if isinstance(category, str) else ""
                category_label = QLabel(category_title)
                category_label.setFont(QFont("Arial", 20, QFont.Bold))
                category_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.scroll_layout.addWidget(category_label)
                
                # Topics in category
                for topic in topics:
                    if search_text in topic.lower() or category_matches:
                        topic_button = QPushButton(topic)
                        topic_button.clicked.connect(lambda checked, t=topic: self.select_topic(t))
                        self.scroll_layout.addWidget(topic_button)
                
    def select_topic(self, topic):
        """Select a topic and show explanation"""
        self.current_topic = topic
        self.show_topic_explanation()
        
    def show_topic_explanation(self):
        """Show topic explanation screen with tabs"""
        self.parent_app.clear_layout()
        
        # Title
        title = self.current_topic if isinstance(self.current_topic, str) else ""
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 32, QFont.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.parent_app.main_layout.addWidget(title_label)
        
        # Create tab widget
        tab_widget = QTabWidget()
        
        # Theory tab
        theory_tab = QWidget()
        theory_layout = QVBoxLayout(theory_tab)
        
        # Explanation scroll area
        theory_scroll = QScrollArea()
        theory_content = QWidget()
        theory_content_layout = QVBoxLayout(theory_content)
        
        explanation_text = self.get_topic_explanation()
        explanation_label = QLabel(explanation_text)
        explanation_label.setWordWrap(True)
        explanation_label.setFont(QFont("Arial", 12))
        theory_content_layout.addWidget(explanation_label)
        
        theory_scroll.setWidget(theory_content)
        theory_layout.addWidget(theory_scroll)
        
        tab_widget.addTab(theory_tab, "Theory")
        
        # Examples tab
        examples_tab = QWidget()
        examples_layout = QVBoxLayout(examples_tab)
        
        examples_text = self.get_topic_examples()
        examples_label = QLabel(examples_text)
        examples_label.setWordWrap(True)
        examples_label.setFont(QFont("Arial", 12))
        examples_layout.addWidget(examples_label)
        
        tab_widget.addTab(examples_tab, "Examples")
        
        # Tools tab
        tools_tab = QWidget()
        tools_layout = QVBoxLayout(tools_tab)
        
        # Check if topic has specific tools
        if self.current_topic in self.topic_tools:
            tools_label = QLabel("Available Tools:")
            tools_label.setFont(QFont("Arial", 16, QFont.Bold))
            tools_layout.addWidget(tools_label)
            
            for tool in self.topic_tools[self.current_topic]:
                tool_button = QPushButton(tool)
                tool_button.clicked.connect(lambda checked, t=tool: self.open_topic_tool(t))
                tools_layout.addWidget(tool_button)
        else:
            no_tools_label = QLabel("No specific tools available for this topic.\nUse the general calculator instead.")
            tools_layout.addWidget(no_tools_label)
        
        # General calculator button
        calc_button = QPushButton("Open Calculator")
        calc_button.clicked.connect(self.open_topic_calculator)
        tools_layout.addWidget(calc_button)
        
        tab_widget.addTab(tools_tab, "Tools")
        
        # Practice tab
        practice_tab = QWidget()
        practice_layout = QVBoxLayout(practice_tab)

        api_key = os.environ.get('OPENAI_API_KEY', None)
        if not openai_available or not api_key:
            error_label = QLabel("AI-powered practice is unavailable. Please install the 'openai' package and set your OPENAI_API_KEY in a .env file.")
            error_label.setWordWrap(True)
            practice_layout.addWidget(error_label)
        else:
            practice_widget = InteractivePracticeWidget(practice_tab, self.current_topic)
            practice_layout.addWidget(practice_widget)

        tab_widget.addTab(practice_tab, "Practice")
        
        self.parent_app.main_layout.addWidget(tab_widget)
        
        # Back button
        back_button = QPushButton("Back to Topics")
        back_button.clicked.connect(self.show_topic_selection)
        self.parent_app.main_layout.addWidget(back_button)
    
    def open_topic_tool(self, tool_name):
        """Open a specific topic tool"""
        # Get the corresponding formula for this tool
        formula = self.tool_to_formula_mapping.get(tool_name, "")
        
        # Navigate to calculator with specific topic and formula
        self.parent_app.calculator.open_topic_calculator_with_formula(self.current_topic, formula)
    
    def open_topic_calculator(self):
        """Open calculator with current topic context"""
        self.parent_app.calculator.current_topic = self.current_topic
        self.parent_app.calculator.show_calculator_menu()
        
    def get_topic_explanation(self):
        """Get detailed explanation for the current topic"""
        explanations = {
            "Algebra and Functions": """
Algebra is the study of symbols and the rules for manipulating them. Functions describe relationships between variables, often written as f(x).
Key concepts:
- Expanding, factorising, and simplifying expressions
- Solving linear, quadratic, and simultaneous equations
- Understanding domains, ranges, and composite/inverse functions
- Graph transformations: translations, stretches, reflections
""",
            "Coordinate Geometry": """
Coordinate geometry uses algebra to study geometric properties and relationships of points, lines, and shapes in the coordinate plane.
Key concepts:
- Equation of a straight line: y = mx + c
- Midpoint and distance formulae
- Gradients and perpendicular lines
- Circles: (x - a)^2 + (y - b)^2 = r^2
""",
            "Sequences and Series": """
A sequence is an ordered list of numbers. A series is the sum of a sequence.
Key concepts:
- Arithmetic sequence: a_n = a + (n-1)d
- Geometric sequence: a_n = ar^{n-1}
- Sum of arithmetic series: S_n = n/2 [2a + (n-1)d]
- Sum of geometric series: S_n = a(1 - r^n)/(1 - r)
""",
            "Differentiation": """
Differentiation is the process of finding the derivative of a function, representing the rate of change or gradient at any point.
Key concepts:
- Derivative notation: f'(x), dy/dx
- Power, product, quotient, and chain rules
- Tangents, normals, stationary points, and curve sketching
- Applications: rates of change, optimization, kinematics
""",
            "Integration": """
Integration is the reverse of differentiation and is used to find areas, volumes, and accumulated quantities.
Key concepts:
- Indefinite and definite integrals
- Power rule, substitution, integration by parts, partial fractions
- Area under curves, between curves, and volumes of revolution
""",
            "Trigonometry": """
Trigonometry studies the relationships between angles and sides in triangles.
Key concepts:
- Sine, cosine, tangent functions and their graphs
- Trigonometric identities and equations
- Sine and cosine rules, area of triangle
- Radians, degrees, and unit circle
""",
            "Exponentials and Logarithms": """
Exponentials and logarithms are inverse functions used to model growth and decay.
Key concepts:
- Laws of indices and logarithms
- Exponential equations and graphs
- Natural logarithm (ln), base e
- Applications: compound interest, population growth, radioactive decay
""",
            "Vectors": """
Vectors have both magnitude and direction, and are used to represent quantities such as displacement, velocity, and force.
Key concepts:
- Vector notation, addition, and subtraction
- Scalar multiplication, magnitude, unit vectors
- Dot product, applications in geometry and mechanics
""",
            "Proof": """
Proof is the process of demonstrating the truth of a mathematical statement using logical reasoning.
Key concepts:
- Direct proof, proof by contradiction, proof by induction
- Common proofs: divisibility, inequalities, identities
- Writing clear, logical arguments
""",
            "Numerical Methods": """
Numerical methods are techniques for finding approximate solutions to mathematical problems.
Key concepts:
- Iterative methods for solving equations (e.g., Newton-Raphson)
- Numerical integration (trapezium rule, Simpson's rule)
- Error estimation and convergence
""",
            "Motion and Forces": """
Motion and Forces are fundamental topics in mechanics. Motion describes how objects move, while forces explain why they move.

Key Points:
- Displacement, velocity, and acceleration are vector quantities.
- Equations of motion (SUVAT) apply to constant acceleration:
  s = ut + ½at²
  v = u + at
  v² = u² + 2as
- Newton's Laws:
  1. An object remains at rest or in uniform motion unless acted on by a resultant force.
  2. F = ma (Force = mass × acceleration)
  3. For every action, there is an equal and opposite reaction.
- Free-body diagrams help analyze forces acting on an object.
- Weight = mg (g ≈ 9.81 m/s² on Earth)
- Friction, tension, normal contact force, and upthrust are common forces in problems.

Exam Tips:
- Draw clear diagrams for force problems.
- State assumptions (e.g., neglect air resistance).
- Use correct units and significant figures.
            """,
            "Electricity": """
Electricity involves the flow of electric charge and the behavior of electric and magnetic fields.

Key Concepts:
• Electric current, voltage, and resistance
• Ohm's Law and circuit analysis
• Electric and magnetic fields
• Electromagnetic induction

Ohm's Law:
• V = IR (Voltage = Current × Resistance)
• P = VI (Power = Voltage × Current)

Circuit Components:
• Resistors: Limit current flow
• Capacitors: Store electric charge
• Inductors: Store magnetic energy
• Diodes: Allow current in one direction

Circuit Analysis:
• Series circuits: R_total = R₁ + R₂ + R₃
• Parallel circuits: 1/R_total = 1/R₁ + 1/R₂ + 1/R₃
• Kirchhoff's Laws: Conservation of charge and energy

Applications:
• Electronics and computing
• Power generation and distribution
• Telecommunications
• Medical equipment
            """,
            "Waves": """
Waves are disturbances that transfer energy through a medium or through space.

Key Concepts:
• Wave properties: amplitude, frequency, wavelength, speed
• Wave types: transverse and longitudinal
• Wave phenomena: reflection, refraction, diffraction, interference

Wave Properties:
• Wave Speed: v = fλ (speed = frequency × wavelength)
• Frequency: f = 1/T (frequency = 1/period)
• Wave Energy: E = hf (energy = Planck's constant × frequency)

Wave Phenomena:
• Reflection: Waves bounce off surfaces
• Refraction: Waves change direction when entering different media
• Diffraction: Waves bend around obstacles
• Interference: Waves combine constructively or destructively

Applications:
• Sound and music
• Light and optics
• Radio and television
• Medical imaging (ultrasound, X-rays)
            """,
            "Statistics": """
Statistics is the science of collecting, analyzing, interpreting, and presenting data.

Key Concepts:
• Descriptive statistics: summarizing data
• Inferential statistics: drawing conclusions from samples
• Probability: likelihood of events occurring

Measures of Central Tendency:
• Mean: average of all values
• Median: middle value when ordered
• Mode: most frequent value

Measures of Spread:
• Range: difference between maximum and minimum
• Standard Deviation: measure of variability
• Variance: square of standard deviation

Probability Distributions:
• Binomial Distribution: discrete probability distribution
• Normal Distribution: continuous probability distribution
• Poisson Distribution: rare events

Applications:
• Scientific research
• Business and economics
• Medicine and healthcare
• Quality control and manufacturing
            """
        }
        key = self.current_topic if isinstance(self.current_topic, str) else ''
        return explanations.get(str(key), f"Detailed explanation for {key} will be available soon.")
    
    def get_topic_examples(self):
        """Get worked examples for the current topic"""
        examples = {
            "Algebra and Functions": """
Example: Solve 2x^2 - 3x - 5 = 0.
Solution: Use the quadratic formula:
x = [3 ± sqrt(9 + 40)] / 4 = [3 ± 7]/4
x = 2.5 or x = -1
""",
            "Coordinate Geometry": """
Example: Find the equation of the line through (1,2) and (3,8).
Solution: Gradient m = (8-2)/(3-1) = 3. So, y - 2 = 3(x - 1) ⇒ y = 3x - 1
""",
            "Sequences and Series": """
Example: Find the sum of the first 10 terms of the sequence 3, 7, 11, ...
Solution: a = 3, d = 4, n = 10
S_10 = 10/2 [2*3 + (10-1)*4] = 5[6 + 36] = 5*42 = 210
""",
            "Differentiation": """
Example: Differentiate f(x) = x^3 - 5x^2 + 4x - 7.
Solution: f'(x) = 3x^2 - 10x + 4
""",
            "Integration": """
Example: Find ∫(2x^3 - 3x^2 + 4) dx.
Solution: (1/2)x^4 - x^3 + 4x + C
""",
            "Trigonometry": """
Example: Solve sin(x) = 0.5 for 0 ≤ x ≤ 2π.
Solution: x = π/6, 5π/6
""",
            "Exponentials and Logarithms": """
Example: Solve 2^x = 16.
Solution: x = 4, since 2^4 = 16
""",
            "Vectors": """
Example: Find the magnitude of vector a = 3i + 4j.
Solution: |a| = sqrt(3^2 + 4^2) = 5
""",
            "Proof": """
Example: Prove that the sum of two even numbers is even.
Solution: Let 2a and 2b be even numbers. 2a + 2b = 2(a + b), which is even.
""",
            "Numerical Methods": """
Example: Use the Newton-Raphson method to solve x^2 - 2 = 0, starting at x0 = 1.
Solution: x1 = x0 - (x0^2 - 2)/(2x0) = 1 - (-1)/2 = 1.5
""",
            "Motion and Forces": """
Worked Example 1: A car accelerates from rest at 2 m/s² for 10 seconds. Find final velocity.

Solution:
v = u + at
v = 0 + 2 × 10 = 20 m/s

Worked Example 2: A 5kg mass is acted on by a force of 20N. Find acceleration.

Solution:
F = ma
a = F/m = 20/5 = 4 m/s²
            """,
            "Electricity": """
Worked Example 1: A circuit has voltage 12V and current 3A. Find resistance.

Solution:
V = IR
R = V/I = 12/3 = 4Ω

Worked Example 2: A device uses 2A at 120V. Find power.

Solution:
P = VI = 120 × 2 = 240W
            """,
            "Waves": """
Worked Example 1: A wave has frequency 50Hz and wavelength 4m. Find speed.

Solution:
v = fλ = 50 × 4 = 200 m/s

Worked Example 2: Light has wavelength 600nm. Find frequency (c = 3×10⁸ m/s).

Solution:
f = c/λ = 3×10⁸ / 600×10⁻⁹ = 5×10¹⁴ Hz
            """,
            "Statistics": """
Worked Example 1: Find mean of 2, 4, 6, 8, 10

Solution:
Mean = (2+4+6+8+10)/5 = 30/5 = 6

Worked Example 2: Find standard deviation of 1, 3, 5, 7

Solution:
Mean = 4
Variance = [(1-4)² + (3-4)² + (5-4)² + (7-4)²]/4 = 5
SD = √5 ≈ 2.24
            """
        }
        
        topic_key = str(self.current_topic) if self.current_topic else ""
        return examples.get(topic_key, f"Worked examples for {topic_key} will be available soon.")
    
    def get_topic_practice(self):
        """Get practice problems for the current topic"""
        practice = {
            "Differentiation": """
Practice Problems (Exam Style):

1. Differentiate f(x) = 3x^4 - 5x^2 + 7x - 2.
2. Find the equation of the tangent to the curve y = x^3 - 2x^2 + x at x = 2.
3. A particle moves so that its displacement s at time t is s = t^3 - 6t^2 + 9t. Find the time(s) when the particle is at rest.
4. The function y = e^{2x} sin(x). Find dy/dx.
5. The curve y = ln(x^2 + 1) passes through the point (1, ln2). Find the gradient at this point.

(Answers and full solutions available in the calculator section.)
            """,
            
            "Integration": """
Practice Problems:

1. Find ∫(4x³ - 2x + 1)dx

2. Evaluate ∫[1,3](x² + 2x)dx

3. Find ∫sin(x)cos(x)dx

4. Evaluate ∫e^(2x)dx

5. Find ∫(1/(x² + 1))dx

Answers will be provided in the calculator section.
            """,
            
            "Trigonometry": """
Practice Problems:

1. In triangle ABC, angle A = 40°, angle B = 60°, and side a = 8. Find side b.

2. In triangle ABC, sides a = 6, b = 8, and angle C = 45°. Find side c.

3. Find the area of a triangle with sides 5, 7, and angle between them 30°.

4. Solve the equation: 2sin(x) = 1 for 0 ≤ x ≤ 2π

5. Prove that sin²(x) + cos²(x) = 1

Answers will be provided in the calculator section.
            """,
            
            "Motion and Forces": """
Practice Problems (Exam Style):

1. A car accelerates uniformly from rest to 25 m/s in 8 seconds. Calculate the acceleration and the distance travelled.
2. A 4 kg mass is acted on by a resultant force of 18 N. Find its acceleration.
3. A box is pulled along a rough surface by a force of 20 N at an angle of 30° to the horizontal. The mass of the box is 5 kg and the coefficient of friction is 0.2. Calculate the acceleration of the box.
4. A ball is thrown vertically upwards with a speed of 12 m/s. How long does it take to return to the thrower?
5. Draw a free-body diagram for a block sliding down an inclined plane and label all forces.

(Answers and full solutions available in the calculator section.)
            """,
            
            "Electricity": """
Practice Problems:

1. A circuit has a voltage of 24V and a resistance of 8Ω. Find the current.

2. A device draws 3A at 120V. Find the power consumed.

3. Three resistors of 2Ω, 4Ω, and 6Ω are connected in series. Find the total resistance.

4. Two resistors of 10Ω and 15Ω are connected in parallel. Find the total resistance.

5. A capacitor stores 0.001C of charge at 12V. Find its capacitance.

Answers will be provided in the calculator section.
            """,
            
            "Waves": """
Practice Problems:

1. A wave has a frequency of 100Hz and a wavelength of 3m. Find its speed.

2. A wave has a period of 0.01s. Find its frequency.

3. A sound wave travels at 340 m/s with a frequency of 500Hz. Find its wavelength.

4. Light has a wavelength of 500nm. Find its frequency (speed of light = 3×10⁸ m/s).

5. A wave has an amplitude of 2m and a frequency of 10Hz. Find its maximum velocity.

Answers will be provided in the calculator section.
            """,
            
            "Statistics": """
Practice Problems:

1. Find the mean of: 3, 7, 11, 15, 19

2. Find the standard deviation of: 2, 4, 6, 8, 10

3. In a binomial experiment with n=10 and p=0.3, find P(X=3).

4. For a normal distribution with μ=50 and σ=10, find P(X>60).

5. Find the correlation coefficient for the data:
   x: 1, 2, 3, 4, 5
   y: 2, 4, 5, 4, 5

Answers will be provided in the calculator section.
            """
        }
        topic_key = str(self.current_topic) if self.current_topic else ""
        return practice.get(topic_key, f"Practice problems for {topic_key} will be available soon.") 

# Helper function to call OpenAI API for question generation
def generate_ai_question(topic):
    api_key = os.environ.get('OPENAI_API_KEY', None)
    if not openai_available or not api_key:
        return ("[OpenAI API key not set or openai package not installed. Please set the OPENAI_API_KEY environment variable and install openai.]", "")
    openai.api_key = api_key
    prompt = (
        f"Generate a new A-level {topic} exam question. Make it calculation-based, realistic, and provide the answer. Format as:\n"
        "Question: ...\nAnswer: ..."
    )
    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.7,
        )
        text = response['choices'][0]['message']['content']
        if text and "Answer:" in text:
            question, answer = text.split("Answer:", 1)
            question = question.replace("Question:", "").strip()
            answer = answer.strip()
        else:
            question, answer = text.strip() if text else "", ""
        return question, answer
    except Exception as e:
        return (f"[OpenAI API error: {e}]", "")

class InteractivePracticeWidget(QWidget):
    def __init__(self, parent, topic):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.topic = topic
        self.score = 0
        self.current_question = ""
        self.current_answer = ""

        api_key = os.environ.get('OPENAI_API_KEY', None)
        if not openai_available or not api_key:
            error_label = QLabel("AI-powered practice is unavailable. Please install the 'openai' package and set your OPENAI_API_KEY in a .env file.")
            error_label.setWordWrap(True)
            layout.addWidget(error_label)
            self.setLayout(layout)
            return

        self.question_label = QLabel()
        self.question_label.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(self.question_label)

        self.input_box = QLineEdit()
        layout.addWidget(self.input_box)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.check_answer)
        layout.addWidget(self.submit_button)

        self.next_button = QPushButton("Next Question")
        self.next_button.clicked.connect(self.next_question)
        self.next_button.setEnabled(False)
        layout.addWidget(self.next_button)

        self.feedback_label = QLabel()
        layout.addWidget(self.feedback_label)

        self.next_question()

    def next_question(self):
        self.input_box.clear()
        self.feedback_label.clear()
        self.submit_button.setEnabled(True)
        self.next_button.setEnabled(False)
        self.current_question, self.current_answer = generate_ai_question(self.topic)
        self.question_label.setText(self.current_question)

    def check_answer(self):
        user_answer = self.input_box.text().strip()
        if not user_answer:
            self.feedback_label.setText("Please enter an answer.")
            return
        # For now, check for exact match (case-insensitive, stripped)
        if self.current_answer:
            if user_answer.lower().strip() == self.current_answer.lower().strip():
                self.feedback_label.setText("Correct!")
                self.score += 1
            else:
                self.feedback_label.setText(f"Incorrect. The correct answer was: {self.current_answer}")
        else:
            self.feedback_label.setText("Answer submitted. (No answer available for auto-checking.)")
        self.submit_button.setEnabled(False)
        self.next_button.setEnabled(True) 