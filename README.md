# A-Level Mathematics & Physics Educational App

A modern, AI-powered educational platform for A-Level Mathematics and Physics, built with PyQt5. This application combines interactive calculators, simulations, AI-generated practice, and comprehensive topic theory to help students master advanced STEM concepts.

## Features

- **Subject & Topic Selection**: Intuitive navigation for A-Level Maths and Physics topics.
- **Smart Calculators**: Topic-specific calculators (e.g., Quadratic Formula, Trigonometry, Kinematics, Statistics) with step-by-step solutions.
- **Graphical Calculator**: Advanced graph generator with automatic analysis of roots, turning points, intercepts, and asymptotes. Trigonometric functions are interpreted in degrees for user convenience.
- **Interactive Simulations**: Physics and mathematics simulations for hands-on learning (e.g., projectile motion, pendulum, circuits).
- **AI-Powered Practice**: Integrates OpenAI API to generate custom practice questions and explanations.
- **User Accounts & History**: Secure login, personalized calculation history, and high score tracking.
- **Accessibility & Preferences**: Dark mode, font scaling, colorblind options, and more.

## Technologies Used

- **Python 3**
- **PyQt5** (GUI framework)
- **SymPy** (symbolic mathematics)
- **NumPy** (numerical computations)
- **Matplotlib** (graph plotting)
- **SQLite** (local database)
- **OpenAI API** (AI question generation)

## Screenshots

![Main Menu](docs/screenshots/main_menu.png)
![Calculator](docs/screenshots/calculator.png)
![Graphical Calculator](docs/screenshots/graphical_calculator.png)
![Simulations](docs/screenshots/simulations.png)

## Getting Started

### Prerequisites
- Python 3.8+
- [pip](https://pip.pypa.io/en/stable/)

### Installation
```bash
# Clone the repository
https://github.com/yourusername/alevel-maths-physics-app.git
cd alevel-maths-physics-app

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### OpenAI API Key (for AI-powered features)
1. [Get your OpenAI API key](https://platform.openai.com/account/api-keys)
2. Create a `.env` file in the project root:
   ```
   OPENAI_API_KEY=sk-...
   ```

### Running the App
```bash
python main.py
```

## Project Structure
```
Aidens Workspace/
├── main.py                # Main application entry point
├── calculator.py          # All calculators and graphical calculator
├── simulations.py         # Interactive simulations
├── subject_selection.py   # Subject/topic selection and theory
├── educational_app.db     # SQLite database
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
├── public/                # Static assets (screenshots, docs)
└── ...
```

## Why This Project Stands Out
- **Comprehensive**: Covers the full A-Level Maths & Physics curriculum with theory, examples, calculators, and practice.
- **Modern UI/UX**: Built with PyQt5 for a professional, desktop-grade user experience.
- **AI Integration**: Uses OpenAI to generate custom questions and explanations, simulating a personal tutor.
- **Robust Engineering**: Modular codebase, error handling, and extensible architecture.
- **Educational Impact**: Designed to help students truly understand and apply advanced concepts, not just memorize formulas.

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT License](LICENSE)

---

**Created by [Your Name]**

*Empowering the next generation of scientists and engineers.* 