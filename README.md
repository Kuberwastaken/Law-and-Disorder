<h1 align="center">Law & Disorder</h1>

<p align="center">
  <img src="https://github.com/user-attachments/assets/c13b7fd2-e3ad-44fa-9a3b-c8053a03f34a" alt="image">
</p>

<p align="center">
   <img src="https://img.shields.io/static/v1?label=Future Layoffs&message=Law-and-Disorder&color=white&logo=github" alt="Future Layoffs - Law and Disorder">
   <img src="https://img.shields.io/badge/version-0.2.11-white" alt="Version 0.2.11">
   <img src="https://img.shields.io/badge/License-Apache_2.0-white" alt="License Apache 2.0">
   </a>
</p>

## Overview
"Law & Disorder" is a party game that allows players to input absurd situations and check their legality according to the Indian Constitution. The game provides a verdict of **YES**, **NO**, or **MAYBE**, along with cited articles and reasoning. Additionally, it offers insights into potential legal loopholes that could be exploited.

## Features
- User-friendly interface for inputting situations.
- AI-powered analysis of legality based on the Indian Constitution.
- Clear presentation of verdicts, relevant articles, and reasoning.
- Suggestions for legal loopholes related to the situation.

## Project Structure
```
legal-game
├── frontend
│   ├── src
│   │   ├── components
│   │   │   └── LegalGame.jsx
│   │   ├── styles
│   │   │   └── globals.css
│   │   └── app.jsx
│   ├── package.json
│   └── index.html
├── backend
│   ├── models.py
│   ├── constitution_analyzer.py
│   ├── main.py
│   ├── requirements.txt
│   └── data
│       └── constitution_of_india.csv
└── README.md
```

## Setup Instructions

### Frontend
1. Navigate to the `frontend` directory.
2. Install dependencies:
   ```
   npm install
   ```
3. Start the development server:
   ```
   npm start
   ```

### Backend
1. Navigate to the `backend` directory.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Start the FastAPI server:
   ```
   python app.py
   ```

## Technologies
- **Frontend**: React JS
- **Backend**: FastAPI, Python
- **AI/ML**: Modified Version of MiniLM-L6 and Google Flan-T5
- **Database**: CSV for storing the Indian Constitution data

## Usage
1. Open the frontend application in your browser.
2. Enter a situation in the input field and submit.
3. View the verdict, relevant articles, reasoning, and potential loopholes.

## How the Game Works
```mermaid
flowchart TD
    A[Start Game] --> B{Choose Mode}
    B --> |Party Mode| C[Player writes a prompt]
    C --> D[Opposite Player guesses YES/NO/MAYBE]
    D --> E{Verdict}
    E --> |Correct| F[+5 Point]
    E --> |Maybe| G[0 Points]
    E --> |Wrong| H[-1 Point]
    F --> I{First to X Points Wins}
    G --> I
    H --> I
    B --> |AI Generative Mode| J[AI generates a scenario]
    J --> D
    I --> K[End Game]
```

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the Apache 2.0 License.
