from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QLineEdit, QTextEdit, QMessageBox, 
                             QGridLayout, QComboBox, QScrollArea, QSlider,
                             QSpinBox, QDoubleSpinBox, QTabWidget, QFrame)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import sympy as sp
from sympy import symbols, solve, diff, integrate
import json
import traceback
import re

class Calculator:
    def __init__(self, parent_app):
        self.parent_app = parent_app
        self.calculation_history = []
        self.user_variables = {}
        self.current_topic = None
        
        # Comprehensive topic formulas for all topics
        self.topic_formulas = {
            "Algebra and Functions": {
                "Quadratic Formula": {
                    "formula": "x = [-b ± sqrt(b^2 - 4ac)] / (2a)",
                    "inputs": ["a", "b", "c"],
                    "description": "Solves ax^2 + bx + c = 0"
                }
            },
            "Coordinate Geometry": {
                "Distance Between Points": {
                    "formula": "d = sqrt((x2 - x1)^2 + (y2 - y1)^2)",
                    "inputs": ["x1", "y1", "x2", "y2"],
                    "description": "Distance between (x1, y1) and (x2, y2)"
                }
            },
            "Sequences and Series": {
                "Arithmetic nth Term": {
                    "formula": "a_n = a_1 + (n-1)d",
                    "inputs": ["a_1", "d", "n"],
                    "description": "nth term of an arithmetic sequence"
                }
            },
            "Differentiation": {
                "Power Rule": {
                    "formula": "d/dx[x^n] = n*x^(n-1)",
                    "inputs": ["n"],
                    "description": "Differentiate x^n with respect to x"
                }
            },
            "Integration": {
                "Power Rule": {
                    "formula": "∫x^n dx = x^(n+1)/(n+1) + C, n ≠ -1",
                    "inputs": ["n"],
                    "description": "Integrate x^n with respect to x"
                }
            },
            "Trigonometry": {
                "Sine Rule": {
                    "formula": "a/sin(A) = b/sin(B) = c/sin(C)",
                    "inputs": ["a", "A", "b", "B", "c", "C"],
                    "description": "Relates sides and angles in any triangle"
                }
            },
            "Exponentials and Logarithms": {
                "Laws of Logs": {
                    "formula": "log_a(xy) = log_a(x) + log_a(y)",
                    "inputs": ["x", "y", "a"],
                    "description": "Product law for logarithms"
                }
            },
            "Vectors": {
                "Magnitude": {
                    "formula": "|a| = sqrt(a1^2 + a2^2 + a3^2)",
                    "inputs": ["a1", "a2", "a3"],
                    "description": "Magnitude of vector a"
                }
            },
            "Proof": {
                "Proof by Contradiction": {
                    "formula": "Assume the opposite, show contradiction",
                    "inputs": [],
                    "description": "General proof method"
                }
            },
            "Numerical Methods": {
                "Newton-Raphson": {
                    "formula": "x_{n+1} = x_n - f(x_n)/f'(x_n)",
                    "inputs": ["x_n", "f(x_n)", "f'(x_n)"],
                    "description": "Root-finding iterative method"
                }
            },

            # --- Mechanics ---
            "Kinematics": {
                "SUVAT (v = u + at)": {
                    "formula": "v = u + at",
                    "inputs": ["u", "a", "t"],
                    "description": "Final velocity from initial velocity, acceleration, and time"
                }
            },
            "Forces and Newton's Laws": {
                "Newton's Second Law": {
                    "formula": "F = ma",
                    "inputs": ["m", "a"],
                    "description": "Force equals mass times acceleration"
                }
            },
            "Moments": {
                "Moment": {
                    "formula": "Moment = F × d",
                    "inputs": ["F", "d"],
                    "description": "Moment of a force about a point"
                }
            },
            "Energy and Work": {
                "Kinetic Energy": {
                    "formula": "KE = 0.5 * m * v^2",
                    "inputs": ["m", "v"],
                    "description": "Kinetic energy of a moving object"
                }
            },
            "Collisions": {
                "Conservation of Momentum": {
                    "formula": "m1*u1 + m2*u2 = m1*v1 + m2*v2",
                    "inputs": ["m1", "u1", "m2", "u2", "v1", "v2"],
                    "description": "Total momentum before = after collision"
                }
            },
            "Circular Motion": {
                "Centripetal Force": {
                    "formula": "F = m*v^2/r",
                    "inputs": ["m", "v", "r"],
                    "description": "Force required for circular motion"
                }
            },
            "Simple Harmonic Motion": {
                "SHM Equation": {
                    "formula": "a = -ω^2 x",
                    "inputs": ["ω", "x"],
                    "description": "Acceleration in simple harmonic motion"
                }
            },

            # --- Statistics ---
            "Data Presentation": {
                "Mean": {
                    "formula": "mean = (Σx) / n",
                    "inputs": ["Σx", "n"],
                    "description": "Arithmetic mean of data"
                }
            },
            "Probability": {
                "Probability": {
                    "formula": "P(A) = number of favourable outcomes / total outcomes",
                    "inputs": ["favourable", "total"],
                    "description": "Basic probability"
                }
            },
            "Discrete Random Variables": {
                "Expected Value": {
                    "formula": "E(X) = Σ[x * P(x)]",
                    "inputs": ["x", "P(x)"],
                    "description": "Expected value of a discrete random variable"
                }
            },
            "Binomial Distribution": {
                "Binomial Probability": {
                    "formula": "P(X = r) = nCr * p^r * (1-p)^(n-r)",
                    "inputs": ["n", "r", "p"],
                    "description": "Probability of r successes in n trials"
                }
            },
            "Normal Distribution": {
                "Standardization": {
                    "formula": "z = (x - μ) / σ",
                    "inputs": ["x", "μ", "σ"],
                    "description": "Standardizing a normal variable"
                }
            },
            "Hypothesis Testing": {
                "Test Statistic": {
                    "formula": "z = (x̄ - μ) / (σ/√n)",
                    "inputs": ["x̄", "μ", "σ", "n"],
                    "description": "Test statistic for hypothesis testing"
                }
            },
            "Correlation and Regression": {
                "Pearson's r": {
                    "formula": "r = Σ[(x - x̄)(y - ȳ)] / sqrt(Σ(x - x̄)^2 * Σ(y - ȳ)^2)",
                    "inputs": ["x", "x̄", "y", "ȳ"],
                    "description": "Pearson correlation coefficient"
                }
            },

            # --- Physics: Mechanics ---
            "Motion and Forces": {
                "Newton's Second Law": {
                    "formula": "F = ma",
                    "inputs": ["m", "a"],
                    "description": "Force equals mass times acceleration"
                }
            },
            "Work, Energy and Power": {
                "Work Done": {
                    "formula": "W = Fd",
                    "inputs": ["F", "d"],
                    "description": "Work done by a force"
                }
            },
            "Momentum and Impulse": {
                "Impulse": {
                    "formula": "Impulse = FΔt = Δp",
                    "inputs": ["F", "Δt"],
                    "description": "Impulse equals change in momentum"
                }
            },
            "Gravitational Fields": {
                "Gravitational Force": {
                    "formula": "F = G * m1 * m2 / r^2",
                    "inputs": ["m1", "m2", "r"],
                    "description": "Newton's law of gravitation"
                }
            },

            # --- Physics: Electricity ---
            "Electric Current": {
                "Current": {
                    "formula": "I = Q / t",
                    "inputs": ["Q", "t"],
                    "description": "Current is charge per unit time"
                }
            },
            "Resistance and Resistivity": {
                "Ohm's Law": {
                    "formula": "V = IR",
                    "inputs": ["I", "R"],
                    "description": "Voltage equals current times resistance"
                }
            },
            "Kirchhoff's Laws": {
                "Kirchhoff's First Law": {
                    "formula": "ΣI_in = ΣI_out",
                    "inputs": [],
                    "description": "Sum of currents into a junction equals sum out"
                }
            },
            "Capacitors": {
                "Capacitance": {
                    "formula": "C = Q / V",
                    "inputs": ["Q", "V"],
                    "description": "Capacitance is charge per unit voltage"
                }
            },
            "Magnetic Fields": {
                "Force on a Wire": {
                    "formula": "F = BIL sinθ",
                    "inputs": ["B", "I", "L", "θ"],
                    "description": "Force on a current-carrying wire in a magnetic field"
                }
            },
            "Electromagnetic Induction": {
                "Faraday's Law": {
                    "formula": "E = -dΦ/dt",
                    "inputs": ["dΦ", "dt"],
                    "description": "Induced EMF equals rate of change of flux"
                }
            },

            # --- Physics: Waves ---
            "Wave Properties": {
                "Wave Speed": {
                    "formula": "v = fλ",
                    "inputs": ["f", "λ"],
                    "description": "Wave speed equals frequency times wavelength"
                }
            },
            "Interference and Diffraction": {
                "Double Slit": {
                    "formula": "w = λD / s",
                    "inputs": ["λ", "D", "s"],
                    "description": "Fringe spacing in double-slit experiment"
                }
            },
            "Standing Waves": {
                "Fundamental Frequency": {
                    "formula": "f = v / 2L",
                    "inputs": ["v", "L"],
                    "description": "Fundamental frequency of a string"
                }
            },
            "Sound Waves": {
                "Speed of Sound": {
                    "formula": "v = sqrt(γRT / M)",
                    "inputs": ["γ", "R", "T", "M"],
                    "description": "Speed of sound in a gas"
                }
            },
            "Light and Optics": {
                "Snell's Law": {
                    "formula": "n1 sinθ1 = n2 sinθ2",
                    "inputs": ["n1", "θ1", "n2", "θ2"],
                    "description": "Law of refraction"
                }
            },
            "Polarisation": {
                "Malus' Law": {
                    "formula": "I = I0 cos^2θ",
                    "inputs": ["I0", "θ"],
                    "description": "Intensity after polariser"
                }
            },

            # --- Physics: Thermal Physics ---
            "Temperature and Heat": {
                "Specific Heat Capacity": {
                    "formula": "Q = mcΔT",
                    "inputs": ["m", "c", "ΔT"],
                    "description": "Heat energy to change temperature"
                }
            },
            "Ideal Gases": {
                "Ideal Gas Law": {
                    "formula": "pV = nRT",
                    "inputs": ["p", "V", "n", "R", "T"],
                    "description": "Equation of state for an ideal gas"
                }
            },
            "Thermodynamics": {
                "First Law": {
                    "formula": "ΔU = Q - W",
                    "inputs": ["Q", "W"],
                    "description": "Change in internal energy"
                }
            },
            "Heat Engines": {
                "Efficiency": {
                    "formula": "η = W_out / Q_in",
                    "inputs": ["W_out", "Q_in"],
                    "description": "Efficiency of a heat engine"
                }
            },
            "Entropy": {
                "Change in Entropy": {
                    "formula": "ΔS = Q / T",
                    "inputs": ["Q", "T"],
                    "description": "Change in entropy"
                }
            },

            # --- Physics: Modern Physics ---
            "Quantum Physics": {
                "Photon Energy": {
                    "formula": "E = hf",
                    "inputs": ["h", "f"],
                    "description": "Energy of a photon"
                }
            },
            "Photoelectric Effect": {
                "Photoelectric Equation": {
                    "formula": "hf = φ + KE_max",
                    "inputs": ["h", "f", "φ"],
                    "description": "Energy balance in photoelectric effect"
                }
            },
            "Wave-Particle Duality": {
                "de Broglie Wavelength": {
                    "formula": "λ = h / p",
                    "inputs": ["h", "p"],
                    "description": "Wavelength of a particle"
                }
            },
            "Nuclear Physics": {
                "Radioactive Decay": {
                    "formula": "N = N0 e^{-λt}",
                    "inputs": ["N0", "λ", "t"],
                    "description": "Number of nuclei remaining after time t"
                }
            },
            "Radioactivity": {
                "Half-life": {
                    "formula": "N = N0 * (1/2)^{t/T_{1/2}}",
                    "inputs": ["N0", "t", "T_{1/2}"],
                    "description": "Radioactive decay by half-life"
                }
            },
            "Particle Physics": {
                "Energy-Mass Equivalence": {
                    "formula": "E = mc^2",
                    "inputs": ["m", "c"],
                    "description": "Mass-energy equivalence"
                }
            }
        }
        
        self.topic_formulas.update({
            # --- Statistics ---
            "Data Presentation": {
                "Mean": {
                    "formula": "mean = (Σx) / n",
                    "inputs": ["Σx", "n"],
                    "description": "Arithmetic mean of data"
                }
            },
            "Probability": {
                "Probability": {
                    "formula": "P(A) = number of favourable outcomes / total outcomes",
                    "inputs": ["favourable", "total"],
                    "description": "Basic probability"
                }
            },
            "Discrete Random Variables": {
                "Expected Value": {
                    "formula": "E(X) = Σ[x * P(x)]",
                    "inputs": ["x", "P(x)"],
                    "description": "Expected value of a discrete random variable"
                }
            },
            "Binomial Distribution": {
                "Binomial Probability": {
                    "formula": "P(X = r) = nCr * p^r * (1-p)^(n-r)",
                    "inputs": ["n", "r", "p"],
                    "description": "Probability of r successes in n trials"
                }
            },
            "Normal Distribution": {
                "Standardization": {
                    "formula": "z = (x - μ) / σ",
                    "inputs": ["x", "μ", "σ"],
                    "description": "Standardizing a normal variable"
                }
            },
            "Hypothesis Testing": {
                "Test Statistic": {
                    "formula": "z = (x̄ - μ) / (σ/√n)",
                    "inputs": ["x̄", "μ", "σ", "n"],
                    "description": "Test statistic for hypothesis testing"
                }
            },
            "Correlation and Regression": {
                "Pearson's r": {
                    "formula": "r = Σ[(x - x̄)(y - ȳ)] / sqrt(Σ(x - x̄)^2 * Σ(y - ȳ)^2)",
                    "inputs": ["x", "x̄", "y", "ȳ"],
                    "description": "Pearson correlation coefficient"
                }
            },

            # --- Physics: Mechanics ---
            "Motion and Forces": {
                "Newton's Second Law": {
                    "formula": "F = ma",
                    "inputs": ["m", "a"],
                    "description": "Force equals mass times acceleration"
                }
            },
            "Work, Energy and Power": {
                "Work Done": {
                    "formula": "W = Fd",
                    "inputs": ["F", "d"],
                    "description": "Work done by a force"
                }
            },
            "Momentum and Impulse": {
                "Impulse": {
                    "formula": "Impulse = FΔt = Δp",
                    "inputs": ["F", "Δt"],
                    "description": "Impulse equals change in momentum"
                }
            },
            "Gravitational Fields": {
                "Gravitational Force": {
                    "formula": "F = G * m1 * m2 / r^2",
                    "inputs": ["m1", "m2", "r"],
                    "description": "Newton's law of gravitation"
                }
            },

            # --- Physics: Electricity ---
            "Electric Current": {
                "Current": {
                    "formula": "I = Q / t",
                    "inputs": ["Q", "t"],
                    "description": "Current is charge per unit time"
                }
            },
            "Resistance and Resistivity": {
                "Ohm's Law": {
                    "formula": "V = IR",
                    "inputs": ["I", "R"],
                    "description": "Voltage equals current times resistance"
                }
            },
            "Kirchhoff's Laws": {
                "Kirchhoff's First Law": {
                    "formula": "ΣI_in = ΣI_out",
                    "inputs": [],
                    "description": "Sum of currents into a junction equals sum out"
                }
            },
            "Capacitors": {
                "Capacitance": {
                    "formula": "C = Q / V",
                    "inputs": ["Q", "V"],
                    "description": "Capacitance is charge per unit voltage"
                }
            },
            "Magnetic Fields": {
                "Force on a Wire": {
                    "formula": "F = BIL sinθ",
                    "inputs": ["B", "I", "L", "θ"],
                    "description": "Force on a current-carrying wire in a magnetic field"
                }
            },
            "Electromagnetic Induction": {
                "Faraday's Law": {
                    "formula": "E = -dΦ/dt",
                    "inputs": ["dΦ", "dt"],
                    "description": "Induced EMF equals rate of change of flux"
                }
            },

            # --- Physics: Waves ---
            "Wave Properties": {
                "Wave Speed": {
                    "formula": "v = fλ",
                    "inputs": ["f", "λ"],
                    "description": "Wave speed equals frequency times wavelength"
                }
            },
            "Interference and Diffraction": {
                "Double Slit": {
                    "formula": "w = λD / s",
                    "inputs": ["λ", "D", "s"],
                    "description": "Fringe spacing in double-slit experiment"
                }
            },
            "Standing Waves": {
                "Fundamental Frequency": {
                    "formula": "f = v / 2L",
                    "inputs": ["v", "L"],
                    "description": "Fundamental frequency of a string"
                }
            },
            "Sound Waves": {
                "Speed of Sound": {
                    "formula": "v = sqrt(γRT / M)",
                    "inputs": ["γ", "R", "T", "M"],
                    "description": "Speed of sound in a gas"
                }
            },
            "Light and Optics": {
                "Snell's Law": {
                    "formula": "n1 sinθ1 = n2 sinθ2",
                    "inputs": ["n1", "θ1", "n2", "θ2"],
                    "description": "Law of refraction"
                }
            },
            "Polarisation": {
                "Malus' Law": {
                    "formula": "I = I0 cos^2θ",
                    "inputs": ["I0", "θ"],
                    "description": "Intensity after polariser"
                }
            },

            # --- Physics: Thermal Physics ---
            "Temperature and Heat": {
                "Specific Heat Capacity": {
                    "formula": "Q = mcΔT",
                    "inputs": ["m", "c", "ΔT"],
                    "description": "Heat energy to change temperature"
                }
            },
            "Ideal Gases": {
                "Ideal Gas Law": {
                    "formula": "pV = nRT",
                    "inputs": ["p", "V", "n", "R", "T"],
                    "description": "Equation of state for an ideal gas"
                }
            },
            "Thermodynamics": {
                "First Law": {
                    "formula": "ΔU = Q - W",
                    "inputs": ["Q", "W"],
                    "description": "Change in internal energy"
                }
            },
            "Heat Engines": {
                "Efficiency": {
                    "formula": "η = W_out / Q_in",
                    "inputs": ["W_out", "Q_in"],
                    "description": "Efficiency of a heat engine"
                }
            },
            "Entropy": {
                "Change in Entropy": {
                    "formula": "ΔS = Q / T",
                    "inputs": ["Q", "T"],
                    "description": "Change in entropy"
                }
            },

            # --- Physics: Modern Physics ---
            "Quantum Physics": {
                "Photon Energy": {
                    "formula": "E = hf",
                    "inputs": ["h", "f"],
                    "description": "Energy of a photon"
                }
            },
            "Photoelectric Effect": {
                "Photoelectric Equation": {
                    "formula": "hf = φ + KE_max",
                    "inputs": ["h", "f", "φ"],
                    "description": "Energy balance in photoelectric effect"
                }
            },
            "Wave-Particle Duality": {
                "de Broglie Wavelength": {
                    "formula": "λ = h / p",
                    "inputs": ["h", "p"],
                    "description": "Wavelength of a particle"
                }
            },
            "Nuclear Physics": {
                "Radioactive Decay": {
                    "formula": "N = N0 e^{-λt}",
                    "inputs": ["N0", "λ", "t"],
                    "description": "Number of nuclei remaining after time t"
                }
            },
            "Radioactivity": {
                "Half-life": {
                    "formula": "N = N0 * (1/2)^{t/T_{1/2}}",
                    "inputs": ["N0", "t", "T_{1/2}"],
                    "description": "Radioactive decay by half-life"
                }
            },
            "Particle Physics": {
                "Energy-Mass Equivalence": {
                    "formula": "E = mc^2",
                    "inputs": ["m", "c"],
                    "description": "Mass-energy equivalence"
                }
            }
        })
        
        self.topic_formulas.update({
            # --- Physics: Mechanics ---
            "Motion and Forces": {
                "Newton's Second Law": {
                    "formula": "F = ma",
                    "inputs": ["m", "a"],
                    "description": "Force equals mass times acceleration"
                }
            },
            "Work, Energy and Power": {
                "Work Done": {
                    "formula": "W = Fd",
                    "inputs": ["F", "d"],
                    "description": "Work done by a force"
                }
            },
            "Momentum and Impulse": {
                "Impulse": {
                    "formula": "Impulse = FΔt = Δp",
                    "inputs": ["F", "Δt"],
                    "description": "Impulse equals change in momentum"
                }
            },
            "Gravitational Fields": {
                "Gravitational Force": {
                    "formula": "F = G * m1 * m2 / r^2",
                    "inputs": ["m1", "m2", "r"],
                    "description": "Newton's law of gravitation"
                }
            },

            # --- Physics: Electricity ---
            "Electric Current": {
                "Current": {
                    "formula": "I = Q / t",
                    "inputs": ["Q", "t"],
                    "description": "Current is charge per unit time"
                }
            },
            "Resistance and Resistivity": {
                "Ohm's Law": {
                    "formula": "V = IR",
                    "inputs": ["I", "R"],
                    "description": "Voltage equals current times resistance"
                }
            },
            "Kirchhoff's Laws": {
                "Kirchhoff's First Law": {
                    "formula": "ΣI_in = ΣI_out",
                    "inputs": [],
                    "description": "Sum of currents into a junction equals sum out"
                }
            },
            "Capacitors": {
                "Capacitance": {
                    "formula": "C = Q / V",
                    "inputs": ["Q", "V"],
                    "description": "Capacitance is charge per unit voltage"
                }
            },
            "Magnetic Fields": {
                "Force on a Wire": {
                    "formula": "F = BIL sinθ",
                    "inputs": ["B", "I", "L", "θ"],
                    "description": "Force on a current-carrying wire in a magnetic field"
                }
            },
            "Electromagnetic Induction": {
                "Faraday's Law": {
                    "formula": "E = -dΦ/dt",
                    "inputs": ["dΦ", "dt"],
                    "description": "Induced EMF equals rate of change of flux"
                }
            },

            # --- Physics: Waves ---
            "Wave Properties": {
                "Wave Speed": {
                    "formula": "v = fλ",
                    "inputs": ["f", "λ"],
                    "description": "Wave speed equals frequency times wavelength"
                }
            },
            "Interference and Diffraction": {
                "Double Slit": {
                    "formula": "w = λD / s",
                    "inputs": ["λ", "D", "s"],
                    "description": "Fringe spacing in double-slit experiment"
                }
            },
            "Standing Waves": {
                "Fundamental Frequency": {
                    "formula": "f = v / 2L",
                    "inputs": ["v", "L"],
                    "description": "Fundamental frequency of a string"
                }
            },
            "Sound Waves": {
                "Speed of Sound": {
                    "formula": "v = sqrt(γRT / M)",
                    "inputs": ["γ", "R", "T", "M"],
                    "description": "Speed of sound in a gas"
                }
            },
            "Light and Optics": {
                "Snell's Law": {
                    "formula": "n1 sinθ1 = n2 sinθ2",
                    "inputs": ["n1", "θ1", "n2", "θ2"],
                    "description": "Law of refraction"
                }
            },
            "Polarisation": {
                "Malus' Law": {
                    "formula": "I = I0 cos^2θ",
                    "inputs": ["I0", "θ"],
                    "description": "Intensity after polariser"
                }
            },

            # --- Physics: Thermal Physics ---
            "Temperature and Heat": {
                "Specific Heat Capacity": {
                    "formula": "Q = mcΔT",
                    "inputs": ["m", "c", "ΔT"],
                    "description": "Heat energy to change temperature"
                }
            },
            "Ideal Gases": {
                "Ideal Gas Law": {
                    "formula": "pV = nRT",
                    "inputs": ["p", "V", "n", "R", "T"],
                    "description": "Equation of state for an ideal gas"
                }
            },
            "Thermodynamics": {
                "First Law": {
                    "formula": "ΔU = Q - W",
                    "inputs": ["Q", "W"],
                    "description": "Change in internal energy"
                }
            },
            "Heat Engines": {
                "Efficiency": {
                    "formula": "η = W_out / Q_in",
                    "inputs": ["W_out", "Q_in"],
                    "description": "Efficiency of a heat engine"
                }
            },
            "Entropy": {
                "Change in Entropy": {
                    "formula": "ΔS = Q / T",
                    "inputs": ["Q", "T"],
                    "description": "Change in entropy"
                }
            },

            # --- Physics: Modern Physics ---
            "Quantum Physics": {
                "Photon Energy": {
                    "formula": "E = hf",
                    "inputs": ["h", "f"],
                    "description": "Energy of a photon"
                }
            },
            "Photoelectric Effect": {
                "Photoelectric Equation": {
                    "formula": "hf = φ + KE_max",
                    "inputs": ["h", "f", "φ"],
                    "description": "Energy balance in photoelectric effect"
                }
            },
            "Wave-Particle Duality": {
                "de Broglie Wavelength": {
                    "formula": "λ = h / p",
                    "inputs": ["h", "p"],
                    "description": "Wavelength of a particle"
                }
            },
            "Nuclear Physics": {
                "Radioactive Decay": {
                    "formula": "N = N0 e^{-λt}",
                    "inputs": ["N0", "λ", "t"],
                    "description": "Number of nuclei remaining after time t"
                }
            },
            "Radioactivity": {
                "Half-life": {
                    "formula": "N = N0 * (1/2)^{t/T_{1/2}}",
                    "inputs": ["N0", "t", "T_{1/2}"],
                    "description": "Radioactive decay by half-life"
                }
            },
            "Particle Physics": {
                "Energy-Mass Equivalence": {
                    "formula": "E = mc^2",
                    "inputs": ["m", "c"],
                    "description": "Mass-energy equivalence"
                }
            }
        })
        
        self.topic_formulas["Algebra and Functions"]["Quadratic Formula"]["symbols"] = {
            "a": "Quadratic coefficient (a)",
            "b": "Linear coefficient (b)",
            "c": "Constant term (c)"
        }
        self.topic_formulas["Coordinate Geometry"]["Distance Between Points"]["symbols"] = {
            "x1": "x-coordinate of first point",
            "y1": "y-coordinate of first point",
            "x2": "x-coordinate of second point",
            "y2": "y-coordinate of second point"
        }
        self.topic_formulas["Sequences and Series"]["Arithmetic nth Term"]["symbols"] = {
            "a_1": "First term of sequence",
            "d": "Common difference",
            "n": "Term number (n)"
        }
        self.topic_formulas["Differentiation"]["Power Rule"]["symbols"] = {
            "n": "Exponent in x^n"
        }
        self.topic_formulas["Integration"]["Power Rule"]["symbols"] = {
            "n": "Exponent in x^n"
        }
        self.topic_formulas["Trigonometry"]["Sine Rule"]["symbols"] = {
            "a": "Side a",
            "A": "Angle A (opposite side a)",
            "b": "Side b",
            "B": "Angle B (opposite side b)",
            "c": "Side c",
            "C": "Angle C (opposite side c)"
        }
        self.topic_formulas["Exponentials and Logarithms"]["Laws of Logs"]["symbols"] = {
            "x": "First argument",
            "y": "Second argument",
            "a": "Base of logarithm"
        }
        self.topic_formulas["Vectors"]["Magnitude"]["symbols"] = {
            "a1": "First component",
            "a2": "Second component",
            "a3": "Third component"
        }
        self.topic_formulas["Proof"]["Proof by Contradiction"]["symbols"] = {}
        self.topic_formulas["Numerical Methods"]["Newton-Raphson"]["symbols"] = {
            "x_n": "Current guess",
            "f(x_n)": "Function value at x_n",
            "f'(x_n)": "Derivative at x_n"
        }
        self.topic_formulas["Kinematics"]["SUVAT (v = u + at)"]["symbols"] = {
            "u": "Initial velocity (m/s)",
            "a": "Acceleration (m/s²)",
            "t": "Time (s)"
        }
        self.topic_formulas["Forces and Newton's Laws"]["Newton's Second Law"]["symbols"] = {
            "m": "Mass (kg)",
            "a": "Acceleration (m/s²)"
        }
        self.topic_formulas["Moments"]["Moment"]["symbols"] = {
            "F": "Force (N)",
            "d": "Perpendicular distance (m)"
        }
        self.topic_formulas["Energy and Work"]["Kinetic Energy"]["symbols"] = {
            "m": "Mass (kg)",
            "v": "Velocity (m/s)"
        }
        self.topic_formulas["Collisions"]["Conservation of Momentum"]["symbols"] = {
            "m1": "Mass 1 (kg)",
            "u1": "Initial velocity 1 (m/s)",
            "m2": "Mass 2 (kg)",
            "u2": "Initial velocity 2 (m/s)",
            "v1": "Final velocity 1 (m/s)",
            "v2": "Final velocity 2 (m/s)"
        }
        self.topic_formulas["Circular Motion"]["Centripetal Force"]["symbols"] = {
            "m": "Mass (kg)",
            "v": "Velocity (m/s)",
            "r": "Radius (m)"
        }
        self.topic_formulas["Simple Harmonic Motion"]["SHM Equation"]["symbols"] = {
            "ω": "Angular frequency (rad/s)",
            "x": "Displacement (m)"
        }
        self.topic_formulas["Data Presentation"]["Mean"]["symbols"] = {
            "Σx": "Sum of all values",
            "n": "Number of values"
        }
        self.topic_formulas["Probability"]["Probability"]["symbols"] = {
            "favourable": "Number of favourable outcomes",
            "total": "Total number of outcomes"
        }
        self.topic_formulas["Discrete Random Variables"]["Expected Value"]["symbols"] = {
            "x": "Value of random variable",
            "P(x)": "Probability of x"
        }
        self.topic_formulas["Binomial Distribution"]["Binomial Probability"]["symbols"] = {
            "n": "Number of trials",
            "r": "Number of successes",
            "p": "Probability of success"
        }
        self.topic_formulas["Normal Distribution"]["Standardization"]["symbols"] = {
            "x": "Value",
            "μ": "Mean",
            "σ": "Standard deviation"
        }
        self.topic_formulas["Hypothesis Testing"]["Test Statistic"]["symbols"] = {
            "x̄": "Sample mean",
            "μ": "Population mean",
            "σ": "Standard deviation",
            "n": "Sample size"
        }
        self.topic_formulas["Correlation and Regression"]["Pearson's r"]["symbols"] = {
            "x": "x value",
            "x̄": "Mean of x",
            "y": "y value",
            "ȳ": "Mean of y"
        }
        self.topic_formulas["Motion and Forces"]["Newton's Second Law"]["symbols"] = {
            "m": "Mass (kg)",
            "a": "Acceleration (m/s²)"
        }
        self.topic_formulas["Work, Energy and Power"]["Work Done"]["symbols"] = {
            "F": "Force (N)",
            "d": "Distance (m)"
        }
        self.topic_formulas["Momentum and Impulse"]["Impulse"]["symbols"] = {
            "F": "Force (N)",
            "Δt": "Time interval (s)"
        }
        self.topic_formulas["Gravitational Fields"]["Gravitational Force"]["symbols"] = {
            "m1": "Mass 1 (kg)",
            "m2": "Mass 2 (kg)",
            "r": "Distance between masses (m)"
        }
        self.topic_formulas["Electric Current"]["Current"]["symbols"] = {
            "Q": "Charge (C)",
            "t": "Time (s)"
        }
        self.topic_formulas["Resistance and Resistivity"]["Ohm's Law"]["symbols"] = {
            "I": "Current (A)",
            "R": "Resistance (Ω)"
        }
        self.topic_formulas["Kirchhoff's Laws"]["Kirchhoff's First Law"]["symbols"] = {}
        self.topic_formulas["Capacitors"]["Capacitance"]["symbols"] = {
            "Q": "Charge (C)",
            "V": "Voltage (V)"
        }
        self.topic_formulas["Magnetic Fields"]["Force on a Wire"]["symbols"] = {
            "B": "Magnetic flux density (T)",
            "I": "Current (A)",
            "L": "Length of wire (m)",
            "θ": "Angle (degrees)"
        }
        self.topic_formulas["Electromagnetic Induction"]["Faraday's Law"]["symbols"] = {
            "dΦ": "Change in magnetic flux (Wb)",
            "dt": "Change in time (s)"
        }
        self.topic_formulas["Wave Properties"]["Wave Speed"]["symbols"] = {
            "f": "Frequency (Hz)",
            "λ": "Wavelength (m)"
        }
        self.topic_formulas["Interference and Diffraction"]["Double Slit"]["symbols"] = {
            "λ": "Wavelength (m)",
            "D": "Distance to screen (m)",
            "s": "Slit separation (m)"
        }
        self.topic_formulas["Standing Waves"]["Fundamental Frequency"]["symbols"] = {
            "v": "Wave speed (m/s)",
            "L": "Length (m)"
        }
        self.topic_formulas["Sound Waves"]["Speed of Sound"]["symbols"] = {
            "γ": "Adiabatic index",
            "R": "Gas constant (J/(kg·K))",
            "T": "Temperature (K)",
            "M": "Molar mass (kg/mol)"
        }
        self.topic_formulas["Light and Optics"]["Snell's Law"]["symbols"] = {
            "n1": "Refractive index 1",
            "θ1": "Angle of incidence (degrees)",
            "n2": "Refractive index 2",
            "θ2": "Angle of refraction (degrees)"
        }
        self.topic_formulas["Polarisation"]["Malus' Law"]["symbols"] = {
            "I0": "Initial intensity",
            "θ": "Angle (degrees)"
        }
        self.topic_formulas["Temperature and Heat"]["Specific Heat Capacity"]["symbols"] = {
            "m": "Mass (kg)",
            "c": "Specific heat capacity (J/kg·K)",
            "ΔT": "Temperature change (K)"
        }
        self.topic_formulas["Ideal Gases"]["Ideal Gas Law"]["symbols"] = {
            "p": "Pressure (Pa)",
            "V": "Volume (m³)",
            "n": "Amount of substance (mol)",
            "R": "Gas constant (J/(mol·K))",
            "T": "Temperature (K)"
        }
        self.topic_formulas["Thermodynamics"]["First Law"]["symbols"] = {
            "Q": "Heat added (J)",
            "W": "Work done by system (J)"
        }
        self.topic_formulas["Heat Engines"]["Efficiency"]["symbols"] = {
            "W_out": "Work output (J)",
            "Q_in": "Heat input (J)"
        }
        self.topic_formulas["Entropy"]["Change in Entropy"]["symbols"] = {
            "Q": "Heat transferred (J)",
            "T": "Temperature (K)"
        }
        self.topic_formulas["Quantum Physics"]["Photon Energy"]["symbols"] = {
            "h": "Planck's constant (J·s)",
            "f": "Frequency (Hz)"
        }
        self.topic_formulas["Photoelectric Effect"]["Photoelectric Equation"]["symbols"] = {
            "h": "Planck's constant (J·s)",
            "f": "Frequency (Hz)",
            "φ": "Work function (J)"
        }
        self.topic_formulas["Wave-Particle Duality"]["de Broglie Wavelength"]["symbols"] = {
            "h": "Planck's constant (J·s)",
            "p": "Momentum (kg·m/s)"
        }
        self.topic_formulas["Nuclear Physics"]["Radioactive Decay"]["symbols"] = {
            "N0": "Initial number of nuclei",
            "λ": "Decay constant (1/s)",
            "t": "Time (s)"
        }
        self.topic_formulas["Radioactivity"]["Half-life"]["symbols"] = {
            "N0": "Initial number of nuclei",
            "t": "Time (s)",
            "T_{1/2}": "Half-life (s)"
        }
        self.topic_formulas["Particle Physics"]["Energy-Mass Equivalence"]["symbols"] = {
            "m": "Mass (kg)",
            "c": "Speed of light (m/s)"
        }
        
    def show_calculator_menu(self):
        """Show calculator selection menu"""
        self.parent_app.clear_layout()
        
        # Title
        title_label = QLabel("Calculator")
        title_label.setFont(QFont("Arial", 36, QFont.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.parent_app.main_layout.addWidget(title_label)
        
        # Subtitle
        subtitle_label = QLabel("Select a calculator or tool:")
        subtitle_label.setFont(QFont("Arial", 18))
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.parent_app.main_layout.addWidget(subtitle_label)
        
        # Buttons
        button_widget = QWidget()
        button_layout = QVBoxLayout(button_widget)
        
        all_purpose_button = QPushButton("All-Purpose Calculator")
        all_purpose_button.clicked.connect(self.show_all_purpose_calculator)
        button_layout.addWidget(all_purpose_button)
        
        maths_topic_button = QPushButton("Maths Topic Calculator")
        maths_topic_button.clicked.connect(self.show_maths_topic_calculator)
        button_layout.addWidget(maths_topic_button)
        
        physics_topic_button = QPushButton("Physics Topic Calculator")
        physics_topic_button.clicked.connect(self.show_physics_topic_calculator)
        button_layout.addWidget(physics_topic_button)
        
        graphical_button = QPushButton("Graphical Calculator")
        graphical_button.clicked.connect(self.show_graphical_calculator)
        button_layout.addWidget(graphical_button)
        
        self.parent_app.main_layout.addWidget(button_widget)
        
        # Back button
        back_button = QPushButton("Back to Main Menu")
        back_button.clicked.connect(self.parent_app.show_main_menu)
        self.parent_app.main_layout.addWidget(back_button)

    def show_maths_topic_calculator(self):
        """Show topic calculator for maths topics only"""
        self._show_filtered_topic_calculator(self._get_maths_topics(), "Maths Topic Calculator")

    def show_physics_topic_calculator(self):
        """Show topic calculator for physics topics only"""
        self._show_filtered_topic_calculator(self._get_physics_topics(), "Physics Topic Calculator")

    def _show_filtered_topic_calculator(self, topics, title):
        self.parent_app.clear_layout()
        
        # Title
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 32, QFont.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.parent_app.main_layout.addWidget(title_label)
        
        # Topic selection
        topic_widget = QWidget()
        topic_layout = QVBoxLayout(topic_widget)
        
        topic_label = QLabel("Select Topic:")
        topic_layout.addWidget(topic_label)
        
        self.topic_var = QComboBox()
        self.topic_var.addItems(topics)
        self.topic_var.currentTextChanged.connect(self.on_topic_change)
        topic_layout.addWidget(self.topic_var)
        self.parent_app.main_layout.addWidget(topic_widget)
        
        # Formula selection
        formula_widget = QWidget()
        formula_layout = QVBoxLayout(formula_widget)
        
        formula_label = QLabel("Select Formula:")
        formula_layout.addWidget(formula_label)
        
        self.formula_var = QComboBox()
        self.formula_var.currentTextChanged.connect(self.on_formula_change)
        formula_layout.addWidget(self.formula_var)
        self.parent_app.main_layout.addWidget(formula_widget)
        
        # Input frame
        self.input_widget = QWidget()
        self.input_layout = QVBoxLayout(self.input_widget)
        self.parent_app.main_layout.addWidget(self.input_widget)
        
        # Result frame
        result_widget = QWidget()
        result_layout = QVBoxLayout(result_widget)
        
        result_label = QLabel("Result:")
        result_layout.addWidget(result_label)
        
        self.result_var = QLineEdit()
        self.result_var.setReadOnly(True)
        self.result_var.setFont(QFont("Arial", 18))
        result_layout.addWidget(self.result_var)
        self.parent_app.main_layout.addWidget(result_widget)
        
        # Calculate button
        calculate_button = QPushButton("Calculate")
        calculate_button.clicked.connect(self.calculate_topic_formula)
        self.parent_app.main_layout.addWidget(calculate_button)
        
        # History widget (added for topic calculators)
        history_widget = QWidget()
        history_layout = QVBoxLayout(history_widget)
        history_label = QLabel("Calculation History:")
        history_label.setFont(QFont("Arial", 16, QFont.Bold))
        history_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        history_layout.addWidget(history_label)
        self.history_text = QTextEdit()
        self.history_text.setMaximumHeight(100)
        history_layout.addWidget(self.history_text)
        self.parent_app.main_layout.addWidget(history_widget)
        
        # Back button
        back_button = QPushButton("Back to Calculator Menu")
        back_button.clicked.connect(self.show_calculator_menu)
        self.parent_app.main_layout.addWidget(back_button)
        
        # Initialize topic dropdown
        if topics:
            self.on_topic_change(topics[0])

    def _get_maths_topics(self):
        return [
            "Algebra and Functions", "Coordinate Geometry", "Sequences and Series", "Differentiation", "Integration", "Trigonometry", "Exponentials and Logarithms", "Vectors", "Proof", "Numerical Methods",
            "Kinematics", "Forces and Newton's Laws", "Moments", "Energy and Work", "Collisions", "Circular Motion", "Simple Harmonic Motion",
            "Data Presentation", "Probability", "Discrete Random Variables", "Binomial Distribution", "Normal Distribution", "Hypothesis Testing", "Correlation and Regression"
        ]

    def _get_physics_topics(self):
        return [
            "Motion and Forces", "Work, Energy and Power", "Momentum and Impulse", "Gravitational Fields",
            "Electric Current", "Resistance and Resistivity", "Kirchhoff's Laws", "Capacitors", "Magnetic Fields", "Electromagnetic Induction",
            "Wave Properties", "Interference and Diffraction", "Standing Waves", "Sound Waves", "Light and Optics", "Polarisation",
            "Temperature and Heat", "Ideal Gases", "Thermodynamics", "Heat Engines", "Entropy",
            "Quantum Physics", "Photoelectric Effect", "Wave-Particle Duality", "Nuclear Physics", "Radioactivity", "Particle Physics"
        ]

    def show_all_purpose_calculator(self):
        """Show all-purpose calculator"""
        self.parent_app.clear_layout()
        
        # Title
        title_label = QLabel("All-Purpose Calculator")
        title_label.setFont(QFont("Arial", 32, QFont.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.parent_app.main_layout.addWidget(title_label)
        
        # Display
        display_widget = QWidget()
        display_layout = QVBoxLayout(display_widget)
        
        self.display_var = QLineEdit()
        self.display_var.setText("0")
        self.display_var.setFont(QFont("Arial", 24))
        self.display_var.setAlignment(Qt.AlignmentFlag.AlignRight)
        display_layout.addWidget(self.display_var)
        
        self.parent_app.main_layout.addWidget(display_widget)
        
        # Buttons grid
        buttons_widget = QWidget()
        buttons_layout = QGridLayout(buttons_widget)
        
        # Calculator buttons
        button_layout = [
            ['C', 'CE', '⌫', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['±', '0', '.', '='],
            ['(', ')', '^', '√']
        ]
        
        for i, row in enumerate(button_layout):
            for j, button_text in enumerate(row):
                button = QPushButton(button_text)
                button.setFont(QFont("Arial", 18))
                button.clicked.connect(lambda checked, text=button_text: self.calculator_button_click(text))
                buttons_layout.addWidget(button, i, j)
                
        self.parent_app.main_layout.addWidget(buttons_widget)
        
        # History
        history_widget = QWidget()
        history_layout = QVBoxLayout(history_widget)
        
        history_label = QLabel("Calculation History:")
        history_label.setFont(QFont("Arial", 16, QFont.Bold))
        history_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        history_layout.addWidget(history_label)
        
        self.history_text = QTextEdit()
        self.history_text.setMaximumHeight(100)
        history_layout.addWidget(self.history_text)
        
        self.parent_app.main_layout.addWidget(history_widget)
        
        # Back button
        back_button = QPushButton("Back to Calculator Menu")
        back_button.clicked.connect(self.show_calculator_menu)
        self.parent_app.main_layout.addWidget(back_button)
        
    def calculator_button_click(self, button_text):
        """Handle calculator button clicks"""
        current = self.display_var.text()
        
        if button_text == 'C':
            self.display_var.setText("0")
        elif button_text == 'CE':
            self.display_var.setText("0")
        elif button_text == '⌫':
            if len(current) > 1:
                self.display_var.setText(current[:-1])
            else:
                self.display_var.setText("0")
        elif button_text == '=':
            try:
                # Replace symbols with operators
                expression = current.replace('×', '*').replace('÷', '/').replace('^', '**')
                result = eval(expression)
                self.display_var.setText(str(result))
                
                # Add to history
                self.add_to_history(f"{current} = {result}")
                
            except Exception as e:
                QMessageBox.critical(self.parent_app, "Error", f"Invalid expression: {e}")
        elif button_text == '±':
            if current.startswith('-'):
                self.display_var.setText(current[1:])
            else:
                self.display_var.setText('-' + current)
        elif button_text == '√':
            try:
                result = math.sqrt(float(current))
                self.display_var.setText(str(result))
                self.add_to_history(f"√{current} = {result}")
            except:
                QMessageBox.critical(self.parent_app, "Error", "Invalid input for square root")
        else:
            if current == "0" and button_text not in ['.', '(', ')']:
                self.display_var.setText(button_text)
            else:
                self.display_var.setText(current + button_text)
                
    def add_to_history(self, calculation):
        """Add calculation to history"""
        self.calculation_history.append(calculation)
        if hasattr(self, 'history_text') and self.history_text is not None:
            self.history_text.append(calculation)
            
        # Save to database if user is logged in
        if self.parent_app.current_user:
            self.parent_app.db_cursor.execute(
                "INSERT INTO calculation_history (user_id, calculation, result) VALUES (?, ?, ?)",
                (self.parent_app.current_user['id'], calculation, calculation.split(" = ")[-1])
            )
            self.parent_app.conn.commit()
            
    def on_topic_change(self, topic):
        """Handle topic change"""
        self.current_topic = topic
        # Guard: check if topic is valid
        if not topic or topic not in self.topic_formulas:
            QMessageBox.critical(self.parent_app, "Error", "No valid topic selected.")
            self.formula_var.clear()
            return
        
        formulas = list(self.topic_formulas[topic].keys())
        self.formula_var.clear()
        self.formula_var.addItems(formulas)
        
        # Set the first formula as selected and trigger the change
        if formulas:
            self.formula_var.setCurrentText(formulas[0])
            # Call on_formula_change with the selected formula
            self.on_formula_change(formulas[0])
            
    def on_formula_change(self, formula):
        """Handle formula change"""
        # Clear previous inputs
        while self.input_layout.count():
            child = self.input_layout.takeAt(0)
            if child is not None and child.widget() is not None:
                child.widget().deleteLater()
        
        # Guard: check if current_topic is valid
        if not self.current_topic or self.current_topic == '':
            return  # Don't show error, just return silently
        # Guard: check if formula is valid
        if not formula or formula not in self.topic_formulas[self.current_topic]:
            return  # Don't show error, just return silently
        
        # Get formula info
        formula_info = self.topic_formulas[self.current_topic][formula]
        inputs = formula_info["inputs"]
        formula_str = formula_info.get("formula", "")
        description = formula_info.get("description", "")
        symbols_dict = formula_info.get("symbols", {})
        
        # Display formula as symbols
        formula_label = QLabel(f"<b>Formula:</b> {formula_str}")
        formula_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.input_layout.addWidget(formula_label)
        
        # Display symbol list with descriptions
        if symbols_dict:
            symbol_lines = [f"<b>{k}</b>: {v}" for k, v in symbols_dict.items()]
        else:
            # Fallback: just list the input names
            symbol_lines = [f"<b>{inp}</b>: (see topic notes)" for inp in inputs]
        symbols_html = "<ul>" + "".join([f"<li>{line}</li>" for line in symbol_lines]) + "</ul>"
        symbols_label = QLabel(f"<b>Symbols:</b> {symbols_html}")
        symbols_label.setFont(QFont("Arial", 12))
        symbols_label.setTextFormat(Qt.TextFormat.RichText)
        self.input_layout.addWidget(symbols_label)
        
        # Create input fields
        self.input_vars = {}
        for i, input_name in enumerate(inputs):
            label = QLabel(f"{input_name}:")
            self.input_layout.addWidget(label)
            
            var = QLineEdit()
            self.input_layout.addWidget(var)
            
            self.input_vars[input_name] = var
            
    def calculate_topic_formula(self):
        """Calculate result for topic formula"""
        try:
            formula = self.formula_var.currentText()
            # Guard: check if current_topic and formula are valid
            if not self.current_topic or self.current_topic not in self.topic_formulas:
                QMessageBox.critical(self.parent_app, "Error", "No valid topic selected for calculation.")
                return
            if not formula or formula not in self.topic_formulas[self.current_topic]:
                QMessageBox.critical(self.parent_app, "Error", "No valid formula selected for calculation.")
                return
            formula_info = self.topic_formulas[self.current_topic][formula]
            
            # Get input values
            values = {}
            for input_name, var in self.input_vars.items():
                value = var.text()
                if not value:
                    QMessageBox.critical(self.parent_app, "Error", f"Please enter value for {input_name}")
                    return
                try:
                    values[input_name] = float(value)
                except ValueError:
                    QMessageBox.critical(self.parent_app, "Error", f"Invalid value for {input_name}")
                    return
                    
            # Calculate based on formula
            result = self.evaluate_formula(formula, values)
            self.result_var.setText(str(result))
            
            # Add to history
            calculation = f"{formula}: {values} = {result}"
            self.add_to_history(calculation)
            
        except Exception as e:
            QMessageBox.critical(self.parent_app, "Error", f"Calculation error: {e}")
            
    def evaluate_formula(self, formula, values):
        """Evaluate formula with given values"""
        # Algebra and Functions
        if formula == "Quadratic Formula":
            a = values.get('a', 0)
            b = values.get('b', 0)
            c = values.get('c', 0)
            if a == 0:
                return "a cannot be zero"
            discriminant = b**2 - 4*a*c
            if discriminant < 0:
                return "No real roots"
            sqrt_disc = math.sqrt(discriminant)
            x1 = (-b + sqrt_disc) / (2*a)
            x2 = (-b - sqrt_disc) / (2*a)
            return f"x1 = {x1}, x2 = {x2}"
        # Coordinate Geometry
        elif formula == "Distance Between Points":
            x1 = values.get('x1', 0)
            y1 = values.get('y1', 0)
            x2 = values.get('x2', 0)
            y2 = values.get('y2', 0)
            d = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            return d
        # Sequences and Series
        elif formula == "Arithmetic nth Term":
            a_1 = values.get('a_1', 0)
            d = values.get('d', 0)
            n = values.get('n', 1)
            return a_1 + (n-1)*d
        # Differentiation/Integration (already implemented)
        elif formula == "Power Rule" and self.current_topic == "Differentiation":
            n = values.get('n', 0)
            return f"{n}x^({n-1})"
        elif formula == "Power Rule" and self.current_topic == "Integration":
            n = values.get('n', 0)
            return f"x^({n+1})/({n+1}) + C"
        # Trigonometry
        elif formula == "Sine Rule":
            # a/sin(A) = b/sin(B) = c/sin(C)
            # If 3 knowns, solve for the 4th
            a = values.get('a', None)
            A = values.get('A', None)
            b = values.get('b', None)
            B = values.get('B', None)
            c = values.get('c', None)
            C = values.get('C', None)
            # Try to solve for the missing value
            try:
                if a is None and b and B and c and C:
                    a = b * math.sin(math.radians(A)) / math.sin(math.radians(B))
                    return a
                elif b is None and a and A and c and C:
                    b = a * math.sin(math.radians(B)) / math.sin(math.radians(A))
                    return b
                elif c is None and a and A and b and B:
                    c = a * math.sin(math.radians(C)) / math.sin(math.radians(A))
                    return c
                else:
                    return "Provide all but one value. Angles in degrees."
            except Exception as e:
                return f"Error: {e}"
        # Exponentials and Logarithms
        elif formula == "Laws of Logs":
            x = values.get('x', 0)
            y = values.get('y', 0)
            a = values.get('a', math.e)
            try:
                return math.log(x*y, a)
            except Exception as e:
                return f"Error: {e}"
        # Vectors
        elif formula == "Magnitude":
            a1 = values.get('a1', 0)
            a2 = values.get('a2', 0)
            a3 = values.get('a3', 0)
            return math.sqrt(a1**2 + a2**2 + a3**2)
        # Numerical Methods
        elif formula == "Newton-Raphson":
            x_n = values.get('x_n', 0)
            fxn = values.get('f(x_n)', 0)
            fpxn = values.get("f'(x_n)", 1)
            if fpxn == 0:
                return "f'(x_n) cannot be zero"
            return x_n - fxn / fpxn
        # Kinematics
        elif formula == "SUVAT (v = u + at)":
            u = values.get('u', 0)
            a = values.get('a', 0)
            t = values.get('t', 0)
            return u + a*t
        # Forces and Newton's Laws
        elif formula == "Newton's Second Law":
            return values.get('m', 0) * values.get('a', 0)
        # Moments
        elif formula == "Moment":
            return values.get('F', 0) * values.get('d', 0)
        # Energy and Work
        elif formula == "Kinetic Energy":
            return 0.5 * values.get('m', 0) * (values.get('v', 0) ** 2)
        # Collisions
        elif formula == "Conservation of Momentum":
            m1 = values.get('m1', 0)
            u1 = values.get('u1', 0)
            m2 = values.get('m2', 0)
            u2 = values.get('u2', 0)
            v1 = values.get('v1', 0)
            v2 = values.get('v2', 0)
            return m1*u1 + m2*u2 == m1*v1 + m2*v2
        # Circular Motion
        elif formula == "Centripetal Force":
            m = values.get('m', 0)
            v = values.get('v', 0)
            r = values.get('r', 1)
            return m * v**2 / r
        # Simple Harmonic Motion
        elif formula == "SHM Equation":
            omega = values.get('ω', 0)
            x = values.get('x', 0)
            return -omega**2 * x
        # Statistics
        elif formula == "Mean":
            sum_x = values.get('Σx', 0)
            n = values.get('n', 1)
            return sum_x / n
        elif formula == "Probability":
            favourable = values.get('favourable', 0)
            total = values.get('total', 1)
            return favourable / total
        elif formula == "Expected Value":
            x = values.get('x', 0)
            px = values.get('P(x)', 0)
            return x * px
        elif formula == "Binomial Probability":
            n = int(values.get('n', 0))
            r = int(values.get('r', 0))
            p = values.get('p', 0)
            from math import comb
            return comb(n, r) * (p**r) * ((1-p)**(n-r))
        elif formula == "Standardization":
            x = values.get('x', 0)
            mu = values.get('μ', 0)
            sigma = values.get('σ', 1)
            return (x - mu) / sigma
        elif formula == "Test Statistic":
            xbar = values.get('x̄', 0)
            mu = values.get('μ', 0)
            sigma = values.get('σ', 1)
            n = values.get('n', 1)
            return (xbar - mu) / (sigma / math.sqrt(n))
        elif formula == "Pearson's r":
            x = values.get('x', 0)
            xbar = values.get('x̄', 0)
            y = values.get('y', 0)
            ybar = values.get('ȳ', 0)
            try:
                numerator = (x - xbar) * (y - ybar)
                denominator = math.sqrt((x - xbar)**2 * (y - ybar)**2)
                return numerator / denominator
            except Exception as e:
                return f"Error: {e}"
        # Physics: Electricity
        elif formula == "Current":
            Q = values.get('Q', 0)
            t = values.get('t', 1)
            return Q / t
        elif formula == "Ohm's Law":
            I = values.get('I', 0)
            R = values.get('R', 1)
            return I * R
        elif formula == "Capacitance":
            Q = values.get('Q', 0)
            V = values.get('V', 1)
            return Q / V
        elif formula == "Force on a Wire":
            B = values.get('B', 0)
            I = values.get('I', 0)
            L = values.get('L', 0)
            theta = values.get('θ', 0)
            return B * I * L * math.sin(math.radians(theta))
        elif formula == "Faraday's Law":
            dPhi = values.get('dΦ', 0)
            dt = values.get('dt', 1)
            return -dPhi / dt
        # Physics: Waves
        elif formula == "Wave Speed":
            f = values.get('f', 0)
            lam = values.get('λ', 0)
            return f * lam
        elif formula == "Double Slit":
            lam = values.get('λ', 0)
            D = values.get('D', 0)
            s = values.get('s', 1)
            return lam * D / s
        elif formula == "Fundamental Frequency":
            v = values.get('v', 0)
            L = values.get('L', 1)
            return v / (2 * L)
        elif formula == "Speed of Sound":
            gamma = values.get('γ', 0)
            R = values.get('R', 0)
            T = values.get('T', 0)
            M = values.get('M', 1)
            return math.sqrt(gamma * R * T / M)
        elif formula == "Snell's Law":
            n1 = values.get('n1', 1)
            theta1 = values.get('θ1', 0)
            n2 = values.get('n2', 1)
            theta2 = values.get('θ2', 0)
            # n1*sin(theta1) = n2*sin(theta2)
            # Solve for missing value if possible
            try:
                if theta2 == 0:
                    theta2 = math.degrees(math.asin(n1 * math.sin(math.radians(theta1)) / n2))
                    return theta2
                elif theta1 == 0:
                    theta1 = math.degrees(math.asin(n2 * math.sin(math.radians(theta2)) / n1))
                    return theta1
                elif n2 == 1:
                    n2 = n1 * math.sin(math.radians(theta1)) / math.sin(math.radians(theta2))
                    return n2
                elif n1 == 1:
                    n1 = n2 * math.sin(math.radians(theta2)) / math.sin(math.radians(theta1))
                    return n1
                else:
                    return "Provide all but one value. Angles in degrees."
            except Exception as e:
                return f"Error: {e}"
        elif formula == "Malus' Law":
            I0 = values.get('I0', 0)
            theta = values.get('θ', 0)
            return I0 * (math.cos(math.radians(theta)) ** 2)
        # Physics: Thermal Physics
        elif formula == "Specific Heat Capacity":
            m = values.get('m', 0)
            c = values.get('c', 0)
            dT = values.get('ΔT', 0)
            return m * c * dT
        elif formula == "Ideal Gas Law":
            p = values.get('p', 0)
            V = values.get('V', 0)
            n = values.get('n', 0)
            R = values.get('R', 8.314)
            T = values.get('T', 1)
            return p * V == n * R * T
        elif formula == "First Law":
            Q = values.get('Q', 0)
            W = values.get('W', 0)
            return Q - W
        elif formula == "Efficiency":
            W_out = values.get('W_out', 0)
            Q_in = values.get('Q_in', 1)
            return W_out / Q_in
        elif formula == "Change in Entropy":
            Q = values.get('Q', 0)
            T = values.get('T', 1)
            return Q / T
        # Physics: Modern Physics
        elif formula == "Photon Energy":
            h = values.get('h', 6.626e-34)
            f = values.get('f', 0)
            return h * f
        elif formula == "Photoelectric Equation":
            h = values.get('h', 6.626e-34)
            f = values.get('f', 0)
            phi = values.get('φ', 0)
            return h * f - phi
        elif formula == "de Broglie Wavelength":
            h = values.get('h', 6.626e-34)
            p = values.get('p', 1)
            return h / p
        elif formula == "Radioactive Decay":
            N0 = values.get('N0', 0)
            lam = values.get('λ', 0)
            t = values.get('t', 0)
            return N0 * math.exp(-lam * t)
        elif formula == "Half-life":
            N0 = values.get('N0', 0)
            t = values.get('t', 0)
            T_half = values.get('T_{1/2}', 1)
            return N0 * (0.5) ** (t / T_half)
        elif formula == "Energy-Mass Equivalence":
            m = values.get('m', 0)
            c = values.get('c', 3e8)
            return m * c ** 2
        else:
            return "Formula not implemented"
            
    def show_graphical_calculator(self):
        """Show enhanced graphical calculator with function analysis"""
        self.parent_app.clear_layout()
        
        # Title
        title_label = QLabel("Function Graph Generator & Analyzer")
        title_label.setFont(QFont("Arial", 32, QFont.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.parent_app.main_layout.addWidget(title_label)
        
        # Input frame
        input_widget = QWidget()
        input_layout = QVBoxLayout(input_widget)
        
        # Function input
        function_label = QLabel("Enter function (e.g., x**2, sin(x), x**3 - 2*x):")
        function_label.setFont(QFont("Arial", 12, QFont.Bold))
        input_layout.addWidget(function_label)
        
        # Example functions
        examples_widget = QWidget()
        examples_layout = QHBoxLayout(examples_widget)
        examples_layout.addWidget(QLabel("Examples:"))
        
        example_functions = ["x**2 - 4", "x**3 - 3*x", "sin(x)", "1/x", "exp(x)"]
        for example in example_functions:
            example_btn = QPushButton(example)
            example_btn.setMaximumWidth(80)
            example_btn.clicked.connect(lambda checked, ex=example: self.function_var.setText(ex))
            examples_layout.addWidget(example_btn)
        
        input_layout.addWidget(examples_widget)
        
        self.function_var = QLineEdit()
        self.function_var.setText("x**2 - 4")
        self.function_var.setFont(QFont("Arial", 14))
        input_layout.addWidget(self.function_var)
        
        # Range inputs
        range_widget = QWidget()
        range_layout = QHBoxLayout(range_widget)
        
        # X range
        x_range_label = QLabel("X range:")
        x_range_label.setFont(QFont("Arial", 12, QFont.Bold))
        range_layout.addWidget(x_range_label)
        
        self.x_min_var = QLineEdit()
        self.x_min_var.setText("-10")
        self.x_min_var.setMaximumWidth(80)
        range_layout.addWidget(self.x_min_var)
        
        x_max_label = QLabel("to")
        range_layout.addWidget(x_max_label)
        
        self.x_max_var = QLineEdit()
        self.x_max_var.setText("10")
        self.x_max_var.setMaximumWidth(80)
        range_layout.addWidget(self.x_max_var)
        
        input_layout.addWidget(range_widget)
        
        # Analysis options
        options_widget = QWidget()
        options_layout = QHBoxLayout(options_widget)
        
        self.show_roots_var = QComboBox()
        self.show_roots_var.addItems(["Find Roots", "Don't Find Roots"])
        self.show_roots_var.setCurrentText("Find Roots")
        options_layout.addWidget(QLabel("Roots:"))
        options_layout.addWidget(self.show_roots_var)
        
        self.show_turning_points_var = QComboBox()
        self.show_turning_points_var.addItems(["Find Turning Points", "Don't Find Turning Points"])
        self.show_turning_points_var.setCurrentText("Find Turning Points")
        options_layout.addWidget(QLabel("Turning Points:"))
        options_layout.addWidget(self.show_turning_points_var)
        
        self.show_asymptotes_var = QComboBox()
        self.show_asymptotes_var.addItems(["Find Asymptotes", "Don't Find Asymptotes"])
        self.show_asymptotes_var.setCurrentText("Find Asymptotes")
        options_layout.addWidget(QLabel("Asymptotes:"))
        options_layout.addWidget(self.show_asymptotes_var)
        
        input_layout.addWidget(options_widget)
        
        # Plot button
        plot_button = QPushButton("Analyze & Plot Function")
        plot_button.setFont(QFont("Arial", 14, QFont.Bold))
        plot_button.clicked.connect(self.plot_function)
        input_layout.addWidget(plot_button)
        
        self.parent_app.main_layout.addWidget(input_widget)
        
        # Results frame
        self.results_frame = QWidget()
        self.results_layout = QVBoxLayout(self.results_frame)
        self.parent_app.main_layout.addWidget(self.results_frame)
        
        # Graph frame
        self.graph_frame = QWidget()
        self.graph_layout = QVBoxLayout(self.graph_frame)
        self.parent_app.main_layout.addWidget(self.graph_frame)
        
        # Back button
        back_button = QPushButton("Back to Calculator Menu")
        back_button.clicked.connect(self.show_calculator_menu)
        self.parent_app.main_layout.addWidget(back_button)
        
    def plot_function(self):
        """Plot the function with comprehensive analysis"""
        try:
            # Clear previous results and plot
            for widget in self.results_frame.findChildren(QWidget):
                widget.deleteLater()
            for widget in self.graph_frame.findChildren(QWidget):
                widget.deleteLater()
                
            # Get function and range
            function_str = self.function_var.text().strip()
            if not function_str:
                QMessageBox.warning(self.parent_app, "Warning", "Please enter a function")
                return
                
            try:
                x_min = float(self.x_min_var.text())
                x_max = float(self.x_max_var.text())
            except ValueError:
                QMessageBox.critical(self.parent_app, "Error", "Invalid range values. Please enter valid numbers.")
                return
            
            if x_min >= x_max:
                QMessageBox.critical(self.parent_app, "Error", "X minimum must be less than X maximum")
                return
            
            # Preprocess function string for degrees in trig functions
            # Replace sin(x) -> sin(radians(x)), etc.
            def deg_replace(match):
                func = match.group(1)
                arg = match.group(2)
                return f"{func}(math.radians({arg}))"
            function_str_processed = re.sub(r"(sin|cos|tan)\(([^)]+)\)", deg_replace, function_str)
            
            # Create sympy symbols and function
            try:
                x_sym = symbols('x')
                # Use math for trig in degrees
                local_dict = {'sin': lambda x: math.sin(x),
                              'cos': lambda x: math.cos(x),
                              'tan': lambda x: math.tan(x),
                              'exp': math.exp,
                              'log': math.log,
                              'sqrt': math.sqrt,
                              'radians': math.radians,
                              'pi': math.pi,
                              'e': math.e}
                f = sp.sympify(function_str_processed, locals=local_dict)
            except Exception as e:
                QMessageBox.critical(self.parent_app, "Error", f"Invalid function: {e}\n\nPlease use standard mathematical notation:\n- Use ** for powers (e.g., x**2)\n- Use * for multiplication (e.g., 2*x)\n- Use standard functions (sin, cos, exp, log)")
                return
            
            # Create plot
            fig, ax = plt.subplots(figsize=(12, 8))
            x_plot = np.linspace(x_min, x_max, 2000)
            x_plot_list = x_plot.tolist()  # Convert to Python list
            
            # Evaluate function for plotting (no finite/NaN checks)
            y_plot = []
            for xi in x_plot_list:
                try:
                    y_val = f.subs(x_sym, xi)
                    y_val_float = float(y_val)
                    y_plot.append(y_val_float)
                except Exception:
                    y_plot.append(float('nan'))
            
            # Plot the function for the full range, including NaN/infinite values
            ax.plot(x_plot_list, y_plot, 'b-', linewidth=2, label=f'f(x) = {function_str}')
            ax.grid(True, alpha=0.3)
            ax.set_xlabel('x', fontsize=12)
            ax.set_ylabel('y', fontsize=12)
            ax.set_title(f'Function Analysis: f(x) = {function_str}', fontsize=14, fontweight='bold')
            ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
            ax.axvline(x=0, color='k', linestyle='-', alpha=0.3)
            
            # Analysis results
            analysis_results = []
            
            # Find y-intercept
            try:
                y_intercept_expr = f.subs(x_sym, 0)
                if hasattr(y_intercept_expr, 'is_real') and y_intercept_expr.is_real:
                    y_intercept = float(y_intercept_expr)
                    if self.is_valid_number(y_intercept):
                        analysis_results.append(f"Y-intercept: (0, {y_intercept:.4f})")
                        ax.plot([0], [y_intercept], 'go', markersize=8, label=f'Y-intercept: (0, {y_intercept:.4f})')
                    else:
                        analysis_results.append("Y-intercept: Not defined or infinite")
                else:
                    analysis_results.append("Y-intercept: Not defined or complex")
            except (TypeError, ValueError, OverflowError):
                analysis_results.append("Y-intercept: Not defined or complex")
            
            # Find roots if requested
            if self.show_roots_var.currentText() == "Find Roots":
                try:
                    roots = self.find_roots(f, x_sym, x_min, x_max)
                    if roots:
                        analysis_results.append(f"Roots: {', '.join([f'({r:.4f}, 0)' for r in roots])}")
                        for root in roots:
                            if self.is_valid_number(root):
                                ax.plot([root], [0], 'ro', markersize=8, label=f'Root: ({root:.4f}, 0)')
                    else:
                        analysis_results.append("Roots: No real roots found in range")
                except Exception as e:
                    analysis_results.append("Roots: Error in calculation")
            
            # Find turning points if requested
            if self.show_turning_points_var.currentText() == "Find Turning Points":
                try:
                    turning_points = self.find_turning_points(f, x_sym, x_min, x_max)
                    if turning_points:
                        tp_text = []
                        for tp in turning_points:
                            x_val, y_val, tp_type = tp
                            if self.is_valid_number(x_val) and self.is_valid_number(y_val):
                                tp_text.append(f'({x_val:.4f}, {y_val:.4f}) [{tp_type}]')
                                color = 'orange' if tp_type == 'Maximum' else 'purple'
                                ax.plot([x_val], [y_val], 'o', color=color, markersize=8, 
                                       label=f'{tp_type}: ({x_val:.4f}, {y_val:.4f})')
                        if tp_text:
                            analysis_results.append(f"Turning Points: {', '.join(tp_text)}")
                    else:
                        analysis_results.append("Turning Points: No turning points found in range")
                except Exception as e:
                    analysis_results.append("Turning Points: Error in calculation")
            
            # Find asymptotes if requested
            if self.show_asymptotes_var.currentText() == "Find Asymptotes":
                asymptotes = self.find_asymptotes(f, x_sym, x_min, x_max)
                if asymptotes:
                    for asym in asymptotes:
                        if asym['type'] == 'vertical':
                            ax.axvline(x=asym['value'], color='r', linestyle='--', alpha=0.7, 
                                     label=f"Vertical asymptote: x = {asym['value']:.4f}")
                            analysis_results.append(f"Vertical asymptote: x = {asym['value']:.4f}")
                        elif asym['type'] == 'horizontal':
                            ax.axhline(y=asym['value'], color='g', linestyle='--', alpha=0.7,
                                     label=f"Horizontal asymptote: y = {asym['value']:.4f}")
                            analysis_results.append(f"Horizontal asymptote: y = {asym['value']:.4f}")
                else:
                    analysis_results.append("Asymptotes: No asymptotes found")
            
            # Domain and range analysis
            domain_range = self.analyze_domain_range(f, x_sym, x_min, x_max)
            analysis_results.extend(domain_range)
            
            # Additional analysis
            behavior_analysis = self.analyze_function_behavior(f, x_sym, x_min, x_max)
            analysis_results.extend(behavior_analysis)
            
            # Add legend
            ax.legend(loc='best', fontsize=10)
            
            # Create canvas
            canvas = FigureCanvas(Figure(fig))
            self.graph_layout.addWidget(canvas)
            
            # Display analysis results
            self.display_analysis_results(analysis_results)
                
        except Exception as e:
            print(f"Detailed error: {traceback.format_exc()}")
            QMessageBox.critical(self.parent_app, "Error", f"Analysis error: {e}\n\nPlease check your function syntax and try again.")
    
    def find_roots(self, f, x_sym, x_min, x_max):
        """Find roots of the function in the given range"""
        try:
            # Try to solve f(x) = 0
            roots = sp.solve(f, x_sym)
            real_roots = []
            
            for root in roots:
                try:
                    if hasattr(root, 'is_real') and root.is_real:
                        root_val = float(root)
                        if x_min <= root_val <= x_max:
                            real_roots.append(root_val)
                except (TypeError, ValueError, OverflowError):
                    # Complex root or conversion error, skip
                    continue
            
            # Also try numerical methods for more roots
            x_test = np.linspace(x_min, x_max, 1000)
            y_test = []
            
            for xi in x_test:
                try:
                    y_val = f.subs(x_sym, xi)
                    if hasattr(y_val, 'is_real') and y_val.is_real:
                        y_test.append(float(y_val))
                    else:
                        y_test.append(np.nan)
                except (TypeError, ValueError, OverflowError):
                    y_test.append(np.nan)
            
            # Find sign changes
            for i in range(len(y_test) - 1):
                if (self.is_valid_number(y_test[i]) and self.is_valid_number(y_test[i+1]) and 
                    y_test[i] * y_test[i+1] < 0):
                    # Root between x_test[i] and x_test[i+1]
                    root_approx = (x_test[i] + x_test[i+1]) / 2
                    if not any(abs(root_approx - r) < 0.01 for r in real_roots):
                        real_roots.append(root_approx)
            
            return sorted(list(set([round(r, 4) for r in real_roots])))
        except Exception as e:
            print(f"Error in find_roots: {e}")
            return []
    
    def find_turning_points(self, f, x_sym, x_min, x_max):
        """Find turning points (critical points) of the function"""
        try:
            # Find derivative
            f_prime = sp.diff(f, x_sym)
            
            # Solve f'(x) = 0
            critical_points = sp.solve(f_prime, x_sym)
            turning_points = []
            
            for cp in critical_points:
                try:
                    if hasattr(cp, 'is_real') and cp.is_real:
                        x_val = float(cp)
                        if x_min <= x_val <= x_max:
                            y_val_expr = f.subs(x_sym, x_val)
                            if hasattr(y_val_expr, 'is_real') and y_val_expr.is_real:
                                y_val = float(y_val_expr)
                                
                                # Determine if it's a maximum or minimum
                                f_double_prime = sp.diff(f_prime, x_sym)
                                second_derivative_expr = f_double_prime.subs(x_sym, x_val)
                                
                                if hasattr(second_derivative_expr, 'is_real') and second_derivative_expr.is_real:
                                    second_derivative = float(second_derivative_expr)
                                    
                                    if second_derivative > 0:
                                        tp_type = "Minimum"
                                    elif second_derivative < 0:
                                        tp_type = "Maximum"
                                    else:
                                        tp_type = "Saddle Point"
                                    
                                    turning_points.append((x_val, y_val, tp_type))
                except (TypeError, ValueError, OverflowError):
                    continue
            
            return turning_points
        except Exception as e:
            print(f"Error in find_turning_points: {e}")
            return []
    
    def find_asymptotes(self, f, x_sym, x_min, x_max):
        """Find vertical and horizontal asymptotes"""
        asymptotes = []
        
        try:
            # Check for vertical asymptotes (where denominator = 0)
            if '/' in str(f):
                # Try to find where denominator equals zero
                try:
                    # This is a simplified approach - extract denominator
                    f_str = str(f)
                    if '/' in f_str:
                        # For rational functions, find where denominator = 0
                        # This is a basic implementation
                        pass
                except:
                    pass
            
            # Check for horizontal asymptotes using limits
            try:
                limit_pos = sp.limit(f, x_sym, sp.oo)
                limit_neg = sp.limit(f, x_sym, -sp.oo)
                
                # Check if limits are finite and equal
                if (limit_pos == limit_neg and 
                    limit_pos != sp.oo and limit_pos != -sp.oo and
                    limit_pos != sp.zoo and limit_pos != -sp.zoo):
                    asymptotes.append({'type': 'horizontal', 'value': float(limit_pos)})
                elif (limit_pos != sp.oo and limit_pos != -sp.oo and 
                      limit_pos != sp.zoo and limit_pos != -sp.zoo):
                    asymptotes.append({'type': 'horizontal', 'value': float(limit_pos)})
            except:
                pass
                
        except:
            pass
        
        return asymptotes
    
    def analyze_domain_range(self, f, x_sym, x_min, x_max):
        """Analyze domain and range of the function"""
        results = []
        
        try:
            # Sample more points to get better range estimate
            x_sample = np.linspace(x_min, x_max, 100)
            y_sample = []
            
            for xi in x_sample:
                try:
                    y_val = f.subs(x_sym, xi)
                    if hasattr(y_val, 'is_real') and y_val.is_real:
                        y_sample.append(float(y_val))
                except (TypeError, ValueError, OverflowError):
                    continue
            
            if y_sample:
                y_min_sample = min(y_sample)
                y_max_sample = max(y_sample)
                
                results.append(f"Domain: [{x_min}, {x_max}]")
                results.append(f"Range (approximate): [{y_min_sample:.4f}, {y_max_sample:.4f}]")
            else:
                results.append("Domain/Range: Could not determine")
            
        except Exception as e:
            results.append("Domain/Range: Could not determine")
        
        return results
    
    def display_analysis_results(self, results):
        """Display analysis results in a text widget"""
        results_widget = QWidget()
        results_layout = QVBoxLayout(results_widget)
        
        results_label = QLabel("Function Analysis Results:")
        results_label.setFont(QFont("Arial", 14, QFont.Bold))
        results_layout.addWidget(results_label)
        
        results_text = QTextEdit()
        results_text.setMaximumHeight(150)
        results_text.setFont(QFont("Arial", 11))
        
        for result in results:
            results_text.append(result)
        
        results_layout.addWidget(results_text)
        self.results_layout.addWidget(results_widget)
    
    def show_simulations_menu(self):
        """Show interactive simulations menu"""
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
        
        wave_button = QPushButton("Wave Interference")
        wave_button.setFont(QFont("Arial", 16))
        wave_button.clicked.connect(self.show_wave_simulation)
        sim_layout.addWidget(wave_button)
        
        # Mathematics simulations
        math_label = QLabel("Mathematics Simulations")
        math_label.setFont(QFont("Arial", 20, QFont.Bold))
        sim_layout.addWidget(math_label)
        
        function_button = QPushButton("Function Explorer")
        function_button.setFont(QFont("Arial", 16))
        function_button.clicked.connect(self.show_function_explorer)
        sim_layout.addWidget(function_button)
        
        derivative_button = QPushButton("Derivative Visualizer")
        derivative_button.setFont(QFont("Arial", 16))
        derivative_button.clicked.connect(self.show_derivative_visualizer)
        sim_layout.addWidget(derivative_button)
        
        integral_button = QPushButton("Integral Visualizer")
        integral_button.setFont(QFont("Arial", 16))
        integral_button.clicked.connect(self.show_integral_visualizer)
        sim_layout.addWidget(integral_button)
        
        self.parent_app.main_layout.addWidget(sim_widget)
        
        # Back button
        back_button = QPushButton("Back to Calculator Menu")
        back_button.clicked.connect(self.show_calculator_menu)
        self.parent_app.main_layout.addWidget(back_button)
    
    def show_projectile_simulation(self):
        """Show projectile motion simulation"""
        self.parent_app.clear_layout()
        
        # Title
        title_label = QLabel("Projectile Motion Simulation")
        title_label.setFont(QFont("Arial", 32, QFont.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.parent_app.main_layout.addWidget(title_label)
        
        # Control panel
        control_widget = QWidget()
        control_layout = QGridLayout(control_widget)
        
        # Initial velocity
        control_layout.addWidget(QLabel("Initial Velocity (m/s):"), 0, 0)
        self.velocity_input = QDoubleSpinBox()
        self.velocity_input.setRange(0, 100)
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
        
        # Fire button
        fire_button = QPushButton("Fire!")
        fire_button.clicked.connect(self.run_projectile_simulation)
        control_layout.addWidget(fire_button, 3, 0, 1, 2)
        
        self.parent_app.main_layout.addWidget(control_widget)
        
        # Results display
        self.results_text = QTextEdit()
        self.results_text.setMaximumHeight(100)
        self.parent_app.main_layout.addWidget(self.results_text)
        
        # Back button
        back_button = QPushButton("Back to Simulations")
        back_button.clicked.connect(self.show_simulations_menu)
        self.parent_app.main_layout.addWidget(back_button)
    
    def run_projectile_simulation(self):
        """Run projectile motion simulation"""
        v0 = self.velocity_input.value()
        angle = math.radians(self.angle_input.value())
        g = self.gravity_input.value()
        
        # Calculate components
        v0x = v0 * math.cos(angle)
        v0y = v0 * math.sin(angle)
        
        # Time of flight
        t_flight = 2 * v0y / g
        
        # Range
        range_distance = v0x * t_flight
        
        # Maximum height
        max_height = (v0y ** 2) / (2 * g)
        
        # Display results
        results = f"""
Projectile Motion Results:
Initial Velocity: {v0:.2f} m/s
Angle: {self.angle_input.value():.1f}°
Time of Flight: {t_flight:.2f} s
Range: {range_distance:.2f} m
Maximum Height: {max_height:.2f} m
        """
        
        self.results_text.setText(results)
    
    def show_pendulum_simulation(self):
        """Show simple pendulum simulation"""
        self.parent_app.clear_layout()
        
        # Title
        title_label = QLabel("Simple Pendulum Simulation")
        title_label.setFont(QFont("Arial", 32, QFont.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.parent_app.main_layout.addWidget(title_label)
        
        # Control panel
        control_widget = QWidget()
        control_layout = QGridLayout(control_widget)
        
        # Length
        control_layout.addWidget(QLabel("Length (m):"), 0, 0)
        self.length_input = QDoubleSpinBox()
        self.length_input.setRange(0.1, 10)
        self.length_input.setValue(1.0)
        control_layout.addWidget(self.length_input, 0, 1)
        
        # Initial angle
        control_layout.addWidget(QLabel("Initial Angle (degrees):"), 1, 0)
        self.pendulum_angle_input = QDoubleSpinBox()
        self.pendulum_angle_input.setRange(0, 90)
        self.pendulum_angle_input.setValue(30)
        control_layout.addWidget(self.pendulum_angle_input, 1, 1)
        
        # Calculate button
        calc_button = QPushButton("Calculate Period")
        calc_button.clicked.connect(self.calculate_pendulum_period)
        control_layout.addWidget(calc_button, 2, 0, 1, 2)
        
        self.parent_app.main_layout.addWidget(control_widget)
        
        # Results display
        self.pendulum_results = QTextEdit()
        self.pendulum_results.setMaximumHeight(100)
        self.parent_app.main_layout.addWidget(self.pendulum_results)
        
        # Back button
        back_button = QPushButton("Back to Simulations")
        back_button.clicked.connect(self.show_simulations_menu)
        self.parent_app.main_layout.addWidget(back_button)
    
    def calculate_pendulum_period(self):
        """Calculate pendulum period"""
        length = self.length_input.value()
        g = 9.81
        
        # Period = 2π√(L/g)
        period = 2 * math.pi * math.sqrt(length / g)
        frequency = 1 / period
        
        results = f"""
Pendulum Results:
Length: {length:.2f} m
Period: {period:.3f} s
Frequency: {frequency:.3f} Hz
        """
        
        self.pendulum_results.setText(results)
    
    def show_circuit_simulation(self):
        """Show electric circuit simulation"""
        self.parent_app.clear_layout()
        
        # Title
        title_label = QLabel("Electric Circuit Simulation")
        title_label.setFont(QFont("Arial", 32, QFont.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.parent_app.main_layout.addWidget(title_label)
        
        # Control panel
        control_widget = QWidget()
        control_layout = QGridLayout(control_widget)
        
        # Voltage
        control_layout.addWidget(QLabel("Voltage (V):"), 0, 0)
        self.voltage_input = QDoubleSpinBox()
        self.voltage_input.setRange(1, 100)
        self.voltage_input.setValue(12)
        control_layout.addWidget(self.voltage_input, 0, 1)
        
        # Resistance
        control_layout.addWidget(QLabel("Resistance (Ω):"), 1, 0)
        self.resistance_input = QDoubleSpinBox()
        self.resistance_input.setRange(0.1, 1000)
        self.resistance_input.setValue(10)
        control_layout.addWidget(self.resistance_input, 1, 1)
        
        # Calculate button
        calc_button = QPushButton("Calculate Current & Power")
        calc_button.clicked.connect(self.calculate_circuit)
        control_layout.addWidget(calc_button, 2, 0, 1, 2)
        
        self.parent_app.main_layout.addWidget(control_widget)
        
        # Results display
        self.circuit_results = QTextEdit()
        self.circuit_results.setMaximumHeight(100)
        self.parent_app.main_layout.addWidget(self.circuit_results)
        
        # Back button
        back_button = QPushButton("Back to Simulations")
        back_button.clicked.connect(self.show_simulations_menu)
        self.parent_app.main_layout.addWidget(back_button)
    
    def calculate_circuit(self):
        """Calculate circuit parameters"""
        voltage = self.voltage_input.value()
        resistance = self.resistance_input.value()
        
        # Ohm's Law: I = V/R
        current = voltage / resistance
        
        # Power: P = VI
        power = voltage * current
        
        results = f"""
Circuit Results:
Voltage: {voltage:.2f} V
Resistance: {resistance:.2f} Ω
Current: {current:.3f} A
Power: {power:.3f} W
        """
        
        self.circuit_results.setText(results)
    
    def show_wave_simulation(self):
        """Show wave interference simulation"""
        self.parent_app.clear_layout()
        
        # Title
        title_label = QLabel("Wave Interference Simulation")
        title_label.setFont(QFont("Arial", 32, QFont.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.parent_app.main_layout.addWidget(title_label)
        
        # Control panel
        control_widget = QWidget()
        control_layout = QGridLayout(control_widget)
        
        # Wavelength
        control_layout.addWidget(QLabel("Wavelength (m):"), 0, 0)
        self.wavelength_input = QDoubleSpinBox()
        self.wavelength_input.setRange(0.1, 10)
        self.wavelength_input.setValue(1.0)
        control_layout.addWidget(self.wavelength_input, 0, 1)
        
        # Frequency
        control_layout.addWidget(QLabel("Frequency (Hz):"), 1, 0)
        self.frequency_input = QDoubleSpinBox()
        self.frequency_input.setRange(1, 1000)
        self.frequency_input.setValue(340)
        control_layout.addWidget(self.frequency_input, 1, 1)
        
        # Calculate button
        calc_button = QPushButton("Calculate Wave Speed")
        calc_button.clicked.connect(self.calculate_wave_speed)
        control_layout.addWidget(calc_button, 2, 0, 1, 2)
        
        self.parent_app.main_layout.addWidget(control_widget)
        
        # Results display
        self.wave_results = QTextEdit()
        self.wave_results.setMaximumHeight(100)
        self.parent_app.main_layout.addWidget(self.wave_results)
        
        # Back button
        back_button = QPushButton("Back to Simulations")
        back_button.clicked.connect(self.show_simulations_menu)
        self.parent_app.main_layout.addWidget(back_button)
    
    def calculate_wave_speed(self):
        """Calculate wave speed"""
        wavelength = self.wavelength_input.value()
        frequency = self.frequency_input.value()
        
        # Wave speed: v = fλ
        wave_speed = frequency * wavelength
        
        results = f"""
Wave Results:
Wavelength: {wavelength:.2f} m
Frequency: {frequency:.1f} Hz
Wave Speed: {wave_speed:.1f} m/s
        """
        
        self.wave_results.setText(results)
    
    def show_function_explorer(self):
        """Show function explorer simulation"""
        self.parent_app.clear_layout()
        
        # Title
        title_label = QLabel("Function Explorer")
        title_label.setFont(QFont("Arial", 32, QFont.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.parent_app.main_layout.addWidget(title_label)
        
        # Function input
        function_widget = QWidget()
        function_layout = QHBoxLayout(function_widget)
        
        function_layout.addWidget(QLabel("f(x) = "))
        self.function_input = QLineEdit()
        self.function_input.setText("x**2")
        function_layout.addWidget(self.function_input)
        
        # Evaluate button
        eval_button = QPushButton("Evaluate")
        eval_button.clicked.connect(self.evaluate_function)
        function_layout.addWidget(eval_button)
        
        self.parent_app.main_layout.addWidget(function_widget)
        
        # X value input
        x_widget = QWidget()
        x_layout = QHBoxLayout(x_widget)
        
        x_layout.addWidget(QLabel("x = "))
        self.x_value_input = QDoubleSpinBox()
        self.x_value_input.setRange(-100, 100)
        self.x_value_input.setValue(2)
        x_layout.addWidget(self.x_value_input)
        
        self.parent_app.main_layout.addWidget(x_widget)
        
        # Results display
        self.function_results = QTextEdit()
        self.function_results.setMaximumHeight(100)
        self.parent_app.main_layout.addWidget(self.function_results)
        
        # Back button
        back_button = QPushButton("Back to Simulations")
        back_button.clicked.connect(self.show_simulations_menu)
        self.parent_app.main_layout.addWidget(back_button)
    
    def evaluate_function(self):
        """Evaluate function at given x value"""
        try:
            function_str = self.function_input.text()
            x_value = self.x_value_input.value()
            
            # Create a safe evaluation environment
            safe_dict = {
                'x': x_value,
                'sin': math.sin,
                'cos': math.cos,
                'tan': math.tan,
                'exp': math.exp,
                'log': math.log,
                'sqrt': math.sqrt,
                'pi': math.pi,
                'e': math.e
            }
            
            # Evaluate the function
            result = eval(function_str, {"__builtins__": {}}, safe_dict)
            
            results = f"""
Function Evaluation:
f(x) = {function_str}
x = {x_value}
f({x_value}) = {result:.6f}
            """
            
            self.function_results.setText(results)
            
        except Exception as e:
            self.function_results.setText(f"Error: {str(e)}")
    
    def show_derivative_visualizer(self):
        """Show derivative visualizer"""
        self.parent_app.clear_layout()
        
        # Title
        title_label = QLabel("Derivative Visualizer")
        title_label.setFont(QFont("Arial", 32, QFont.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.parent_app.main_layout.addWidget(title_label)
        
        # Function input
        function_widget = QWidget()
        function_layout = QHBoxLayout(function_widget)
        
        function_layout.addWidget(QLabel("f(x) = "))
        self.derivative_function_input = QLineEdit()
        self.derivative_function_input.setText("x**2")
        function_layout.addWidget(self.derivative_function_input)
        
        # Calculate derivative button
        calc_button = QPushButton("Calculate Derivative")
        calc_button.clicked.connect(self.calculate_derivative)
        function_layout.addWidget(calc_button)
        
        self.parent_app.main_layout.addWidget(function_widget)
        
        # Results display
        self.derivative_results = QTextEdit()
        self.derivative_results.setMaximumHeight(150)
        self.parent_app.main_layout.addWidget(self.derivative_results)
        
        # Back button
        back_button = QPushButton("Back to Simulations")
        back_button.clicked.connect(self.show_simulations_menu)
        self.parent_app.main_layout.addWidget(back_button)
    
    def calculate_derivative(self):
        """Calculate derivative of function"""
        try:
            function_str = self.derivative_function_input.text()
            
            # Use sympy to calculate derivative
            x = sp.Symbol('x')
            f = sp.sympify(function_str)
            derivative = sp.diff(f, x)
            
            results = f"""
Derivative Calculation:
f(x) = {function_str}
f'(x) = {derivative}
            """
            
            self.derivative_results.setText(results)
            
        except Exception as e:
            self.derivative_results.setText(f"Error: {str(e)}")
    
    def show_integral_visualizer(self):
        """Show integral visualizer"""
        self.parent_app.clear_layout()
        
        # Title
        title_label = QLabel("Integral Visualizer")
        title_label.setFont(QFont("Arial", 32, QFont.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.parent_app.main_layout.addWidget(title_label)
        
        # Function input
        function_widget = QWidget()
        function_layout = QHBoxLayout(function_widget)
        
        function_layout.addWidget(QLabel("f(x) = "))
        self.integral_function_input = QLineEdit()
        self.integral_function_input.setText("x**2")
        function_layout.addWidget(self.integral_function_input)
        
        # Calculate integral button
        calc_button = QPushButton("Calculate Integral")
        calc_button.clicked.connect(self.calculate_integral)
        function_layout.addWidget(calc_button)
        
        self.parent_app.main_layout.addWidget(function_widget)
        
        # Results display
        self.integral_results = QTextEdit()
        self.integral_results.setMaximumHeight(150)
        self.parent_app.main_layout.addWidget(self.integral_results)
        
        # Back button
        back_button = QPushButton("Back to Simulations")
        back_button.clicked.connect(self.show_simulations_menu)
        self.parent_app.main_layout.addWidget(back_button)
    
    def calculate_integral(self):
        """Calculate integral of function"""
        try:
            function_str = self.integral_function_input.text()
            
            # Use sympy to calculate integral
            x = sp.Symbol('x')
            f = sp.sympify(function_str)
            integral = sp.integrate(f, x)
            
            results = f"""
Integral Calculation:
f(x) = {function_str}
∫f(x)dx = {integral} + C
            """
            
            self.integral_results.setText(results)
            
        except Exception as e:
            self.integral_results.setText(f"Error: {str(e)}")

    def open_topic_calculator_with_formula(self, topic, formula):
        """Open topic calculator with specific topic and formula pre-selected"""
        # Set the current topic
        self.current_topic = topic
        
        # Determine which topic calculator to show based on the topic
        maths_topics = self._get_maths_topics()
        physics_topics = self._get_physics_topics()
        
        if topic in maths_topics:
            self._show_filtered_topic_calculator(maths_topics, "Maths Topic Calculator")
        elif topic in physics_topics:
            self._show_filtered_topic_calculator(physics_topics, "Physics Topic Calculator")
        else:
            # Fallback to maths calculator
            self._show_filtered_topic_calculator(maths_topics, "Maths Topic Calculator")
        
        # Set the topic dropdown to the correct topic
        if hasattr(self, 'topic_var'):
            index = self.topic_var.findText(topic)
            if index >= 0:
                self.topic_var.setCurrentIndex(index)
        
        # Set the formula dropdown to the correct formula
        if hasattr(self, 'formula_var') and formula:
            # Wait a moment for the formula dropdown to be populated
            QTimer.singleShot(100, lambda: self._set_formula_selection(formula))
    
    def _set_formula_selection(self, formula):
        """Set the formula dropdown to the specified formula"""
        if hasattr(self, 'formula_var'):
            index = self.formula_var.findText(formula)
            if index >= 0:
                self.formula_var.setCurrentIndex(index)
            else:
                # If exact match not found, try partial match
                for i in range(self.formula_var.count()):
                    if formula.lower() in self.formula_var.itemText(i).lower():
                        self.formula_var.setCurrentIndex(i)
                        break
    
    def analyze_function_behavior(self, f, x_sym, x_min, x_max):
        """Analyze additional function behavior"""
        results = []
        
        try:
            # Check for symmetry
            f_neg_x = f.subs(x_sym, -x_sym)
            
            if f == f_neg_x:
                results.append("Symmetry: Even function (symmetric about y-axis)")
            elif f == -f_neg_x:
                results.append("Symmetry: Odd function (symmetric about origin)")
            else:
                results.append("Symmetry: Neither even nor odd")
            
            # Check for periodicity (basic check for trigonometric functions)
            trig_functions = ['sin', 'cos', 'tan', 'csc', 'sec', 'cot']
            f_str = str(f).lower()
            
            is_periodic = any(trig in f_str for trig in trig_functions)
            if is_periodic:
                results.append("Periodicity: Function appears to be periodic")
            else:
                results.append("Periodicity: Function appears to be non-periodic")
            
            # Check for monotonicity in different intervals
            f_prime = sp.diff(f, x_sym)
            
            # Sample points to check if derivative is always positive/negative
            x_sample = np.linspace(x_min, x_max, 50)
            derivative_signs = []
            
            for xi in x_sample:
                try:
                    deriv_val = f_prime.subs(x_sym, xi)
                    if hasattr(deriv_val, 'is_real') and deriv_val.is_real:
                        deriv_float = float(deriv_val)
                        if deriv_float > 0:
                            derivative_signs.append(1)
                        elif deriv_float < 0:
                            derivative_signs.append(-1)
                        else:
                            derivative_signs.append(0)
                    else:
                        derivative_signs.append(0)
                except (TypeError, ValueError, OverflowError):
                    derivative_signs.append(0)
            
            if all(sign >= 0 for sign in derivative_signs):
                results.append("Monotonicity: Function is increasing in the given range")
            elif all(sign <= 0 for sign in derivative_signs):
                results.append("Monotonicity: Function is decreasing in the given range")
            else:
                results.append("Monotonicity: Function is neither strictly increasing nor decreasing")
            
            # Check for boundedness
            y_sample = []
            for xi in x_sample:
                try:
                    y_val = f.subs(x_sym, xi)
                    if hasattr(y_val, 'is_real') and y_val.is_real:
                        y_sample.append(float(y_val))
                except (TypeError, ValueError, OverflowError):
                    continue
            
            if y_sample:
                y_min_sample = min(y_sample)
                y_max_sample = max(y_sample)
                
                if abs(y_min_sample) < 1e6 and abs(y_max_sample) < 1e6:
                    results.append("Boundedness: Function appears to be bounded in the given range")
                else:
                    results.append("Boundedness: Function appears to be unbounded in the given range")
            else:
                results.append("Boundedness: Could not determine")
                
        except Exception as e:
            results.append("Behavior Analysis: Could not determine function behavior")
        
        return results

    def is_valid_number(self, value):
        """Check if a value is a valid finite number"""
        try:
            if isinstance(value, (int, float)):
                return not (math.isnan(value) or math.isinf(value))
            elif hasattr(value, 'is_real') and value.is_real:
                float_val = float(value)
                return not (math.isnan(float_val) or math.isinf(float_val))
            else:
                return False
        except (TypeError, ValueError, OverflowError):
            return False