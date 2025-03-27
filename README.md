
# Quiz Application 🎮

A interactive quiz game built with Python and Tkinter. Test your knowledge, race against the clock, and compete for high scores!

## Features ✨

- **Multiple-Choice Questions**: Load questions from a JSON file (easy to customize).
- **Timer Pressure**: 15 seconds per question to keep you on your toes! ⏳
- **Score Tracking**: Earn points for correct answers and bonus points for streaks (3+ in a row).
- **Highscore System**: Local storage of top 10 scores with timestamps 🏆.
- **Review Mode**: Analyze incorrect answers after the game ends.
- **Modern GUI**: Dark theme, hover effects, and responsive design.
- **Error Handling**: Graceful handling of missing files and invalid inputs.

## Installation 🛠️

1. **Clone the repository**:
   ```bash
   git clone https://github.com/deltaseconds/quiz-app-python.git
   cd quiz-app-python
   ```

2. **Install Python** (3.6 or higher required).

3. **Run the app**:
   ```bash
   python quiz.py
   ```

## Usage 🚀

1. **Start the Quiz**: Click "Quiz starten" on the splash screen.
2. **Enter Username**: Provide a name to track your score.
3. **Answer Questions**: Click the correct answer before time runs out.
4. **Avoid Mistakes**: 3 wrong answers end the game!
5. **Review Performance**: After the game, see where you went wrong.

## Configuration ⚙️

### Customize Questions
Edit `questions.json` to add/remove questions:
```json
{
  "questions": [
    {
      "question": "Your question here?",
      "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
      "answer": 0 // Index of correct option (0-3)
    }
  ]
}
```

### Highscores
- Scores are saved in `highscores.json`.
- Clear the file to reset all highscores.


## Contributing 🤝

Contributions are welcome! 
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit changes (`git commit -m 'Add AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

## License 📄

This project is open-source under the MIT License.

---
```
