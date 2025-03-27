# Import notwendiger libraries
import json  # Für JSON (Fragen und Highscores)
import random  # Zum randomisen der Fragen
import tkinter as tk  # gui erstellung
from tkinter import simpledialog, ttk, messagebox  # Dialoge und Widgets
from datetime import datetime  # timestamp für highscores

# Konstantendefinition für Dateinamen
HIGHSCORES_FILE = "highscores.json"  # Datei zur Speicherung der highscores
QUESTIONS_FILE = "questions.json"  # Datei mit den Quizfragen

# main class für die Quiz app
class QuizApp:
    def __init__(self, window):
        # Initialisierung des Hauptfensters
        self.window = window
        self.window.title("Quiz")  # Fenstertitel
        self.window.geometry("1000x800")  # Fenstergröße
        self.window.configure(bg="#1a1a1a")  # Hintergrundfarbe (dunkelgrau)
        self.window.resizable(False, False)  # Fixierte Fenstergröße

        # Spielvariablen Initialisierung
        self.username = None  # Speichert den Spielernamen
        self.score = 0  # Aktueller Punktestand
        self.wrong_answers = 0  # Zähler für falsche Antworten
        self.questions = []  # Liste aller Fragen
        self.remaining_questions = []  # Noch nicht gestellte Fragen
        self.highscores = []  # highscores
        self.current_question = None  # Aktuelle Frage
        self.time_left = 15  # Verbleibende Zeit pro Frage
        self.streak = 0  # Richtige Antworten in Folge
        self.timer_job = None  # ID für Timer-Event

        # GUI-Elemente erstellen
        self.create_widgets()
        # Fragen und Highscores laden
        self.load_questions()
        self.load_highscores()
        # Startbildschirm anzeigen
        self.show_splash_screen()

    def create_widgets(self):
        #Erstellt alle GUI-Elemente des Hauptfensters
        # Frage-Label
        self.question_label = tk.Label(
            self.window,
            bg="#1a1a1a",  # Hintergrundfarbe
            fg="white",  # Schriftfarbe
            wraplength=900,  # Zeilenumbruch bei 900px
            font=("Arial", 24, "bold"),  # Schriftart
            justify=tk.CENTER  # Zentrierte Ausrichtung
        )
        self.question_label.pack(pady=40)  # Abstand nach oben/unten

        # Feedback-Label
        self.feedback_label = tk.Label(
            self.window,
            bg="#1a1a1a",
            fg="#FFD700",  # Goldene Schriftfarbe
            font=("Arial", 18, "italic"),
            justify=tk.CENTER
        )
        self.feedback_label.pack(pady=10)

        # Antwort-Buttons
        self.buttons = []
        for i in range(4):  # 4 Antwortmöglichkeiten
            btn = tk.Button(
                self.window,
                width=30,
                height=2,
                bg="#4CAF50",  # grüne Hintergrundfarbe
                fg="white",
                font=("Arial", 16, "bold"),
                relief="flat",  # Keine 3D-Effekte
                command=lambda idx=i: self.check_answer(idx)  # Klick-Event
            )
            btn.pack(pady=15)
            self.buttons.append(btn)
            # Hover-Effekte
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#45a049"))  # Dunkleres Grün
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#4CAF50"))

        # fortschrittsbalken
        self.progress = ttk.Progressbar(
            self.window,
            orient=tk.HORIZONTAL,
            length=800,
            mode='determinate'  # prozentbasierte Anzeige
        )
        self.progress.pack(pady=20)

        # score anzeige rahmen
        self.score_frame = tk.Frame(self.window, bg="#1a1a1a")
        self.score_frame.pack(pady=20, fill=tk.X)  # Volle Breite

        # aktueller Score
        self.current_score_label = tk.Label(
            self.score_frame,
            bg="#1a1a1a",
            fg="#00BCD4",  # Farbe
            font=("Arial", 14),
            anchor="w"  # linksbündig
        )
        self.current_score_label.pack(side=tk.LEFT, padx=50)

        # Timer Anzeige
        self.timer_label = tk.Label(
            self.score_frame,
            bg="#1a1a1a",
            fg="white",
            font=("Arial", 14),
            anchor="center"  # zentriert
        )
        self.timer_label.pack(side=tk.LEFT, expand=True)

        # highscores-display
        self.highscores_label = tk.Label(
            self.score_frame,
            bg="#1a1a1a",
            fg="#8BC34A",  # Hellgrün
            font=("Arial", 14),
            anchor="e"  # Rechtsbündig
        )
        self.highscores_label.pack(side=tk.RIGHT, padx=50)

    def show_splash_screen(self):
        # Zeigt den Startbildschirm mit Spielregeln und Button
        # Splashscreen erstellen
        splash = tk.Toplevel(self.window)
        splash.geometry("600x400")
        splash.configure(bg="#1a1a1a")
        
        # Titelname und "Regeln"
        tk.Label(splash, text="Quiz", font=("Arial", 32, "bold"), 
                bg="#1a1a1a", fg="white").pack(pady=50)
        tk.Label(splash, text="Regeln:\n1. 15 Sekunden pro Frage\n2. 3 Fehler beenden das Spiel\n3. Serien geben Bonuspunkte!", 
                font=("Arial", 14), bg="#1a1a1a", fg="white").pack()
        # start button
        tk.Button(splash, text="Quiz starten", command=lambda: self.start_quiz(splash), 
                font=("Arial", 16), bg="#4CAF50", fg="white").pack(pady=30)
        
        # window konfiguration 
        splash.protocol("WM_DELETE_WINDOW", self.window.destroy)
        splash.grab_set()  # Fokus erzwingen
        splash.focus_force()

    def start_quiz(self, splash):
        # startet quiz nach splash screen
        splash.destroy()
        self.get_username()

    def load_questions(self):
        # Lädt Fragen aus json
        try:
            with open(QUESTIONS_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
                self.questions = data["questions"]
                random.shuffle(self.questions)  # Zufällige Reihenfolge der fragen
                self.remaining_questions = self.questions.copy()
        except Exception as e:
            messagebox.showerror("Fehler", f"Fragen konnten nicht geladen werden: {str(e)}")
            self.window.destroy()

    def get_username(self):
        # Öffnet Namenseingabe-Dialog
        self.window.withdraw()  # main window verstecken
        
        dialog = tk.Toplevel(self.window)
        dialog.title("Username eingeben")
        dialog.geometry("500x300")
        dialog.configure(bg="#1a1a1a")
        
        # grafik Elemente
        canvas = tk.Canvas(dialog, bg="#1a1a1a", highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)
        canvas.create_rectangle(0, 150, 500, 300, fill="#4CAF50", outline="")
        
        # Texte und username eingabefeld
        tk.Label(dialog, text="Dein Name?", font=("Arial", 24, "bold"), 
                bg="#1a1a1a", fg="white").place(relx=0.5, rely=0.3, anchor=tk.CENTER)
        self.username_entry = tk.Entry(dialog, font=("Arial", 18), 
                                     bg="#333333", fg="white")
        self.username_entry.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # startbutton
        tk.Button(dialog, text="START →", font=("Arial", 14, "bold"), 
                command=lambda: self.validate_username(dialog)).place(relx=0.5, rely=0.7, anchor=tk.CENTER)
        
        dialog.grab_set()
        dialog.protocol("WM_DELETE_WINDOW", lambda: self.on_dialog_close(dialog))

    def validate_username(self, dialog):
        # Überprüft username
        username = self.username_entry.get().strip()
        if username:
            self.username = username
            dialog.destroy()
            self.window.deiconify()  # Hauptfenster wieder anzeigen
            self.show_question()
            self.start_timer()
            self.update_score_display()
        else:
            # Fehleranzeige bei leerem Namen
            self.username_entry.config(highlightbackground="red", highlightthickness=1)
            self.username_entry.focus_set()

    def show_question(self):
        #Zeigt die nächste Frage an#
        if self.remaining_questions and self.wrong_answers < 3:
            # Aktiviere Buttons für neue Frage
            for btn in self.buttons:
                btn.config(state=tk.NORMAL)

            self.current_question = self.remaining_questions.pop(0)
            self.question_label.config(text=self.current_question["question"])
            # Setze Antwortoptionen
            for i, option in enumerate(self.current_question["options"]):
                self.buttons[i].config(text=option)
            self.update_progress()
            self.start_timer()
        else:
            self.end_quiz()

    def check_answer(self, selected_index):
        # Überprüft die ausgewählte Antwort
        if self.timer_job:
            self.window.after_cancel(self.timer_job)
            self.timer_job = None

        correct_index = self.current_question["answer"]

        # Deaktiviere buttons nach Antwort
        for btn in self.buttons:
            btn.config(state=tk.DISABLED)
        self.buttons[correct_index].config(bg="#2E7D32")  # Korrekte Antwort grün markieren

        if selected_index == correct_index:
            self.handle_correct_answer()
        else:
            self.handle_wrong_answer(correct_index)

        self.update_score_display()
        self.window.after(1500, self.reset_buttons)
        self.window.after(1500, self.show_question)

    def handle_correct_answer(self):
        # Verarbeitet true Antwort
        self.score += 1
        self.streak += 1
        if self.streak >= 3:
            self.score += 1  # Bonuspunkte für Serie
            self.show_feedback(f"Richtig! {self.streak} Serie! +1 Bonus", "#2E7D32")
        else:
            self.show_feedback("Richtig!", "#2E7D32")

    def handle_wrong_answer(self, correct_index):
        # Verarbeitet false Antwort
        self.wrong_answers += 1
        self.streak = 0
        correct_answer = self.current_question["options"][correct_index]
        self.show_feedback(f"Falsch! Richtig: {correct_answer}", "#D32F2F")
        self.update_score_display()
        if self.wrong_answers >= 3:
            self.end_quiz()

    def reset_buttons(self):
        # Setzt button farben zurück
        for btn in self.buttons:
            btn.config(bg="#4CAF50", state=tk.NORMAL)

    def start_timer(self):
        # Startet Countdown
        if self.timer_job:
            self.window.after_cancel(self.timer_job)
        self.time_left = 15
        self.update_timer()

    def update_timer(self):
        # aktualisiert timer
        self.timer_label.config(text=f"⏳ Verbleibend: {self.time_left}s")
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_job = self.window.after(1000, self.update_timer)
        else:
            self.show_feedback("Zeit abgelaufen!", "#D32F2F")
            self.wrong_answers += 1
            self.check_answer(None)

    def update_progress(self):
        # Aktualisiert progress bar
        total = len(self.questions)
        answered = total - len(self.remaining_questions)
        self.progress['value'] = (answered / total) * 100

    def show_feedback(self, message, color):
        #Zeigt temporäres Feedback
        self.feedback_label.config(text=message, fg=color)
        self.window.after(1500, lambda: self.feedback_label.config(text=""))

    def update_score_display(self):
        # Aktualisiert die score display
        self.current_score_label.config(
            text=f"Spieler: {self.username}\n"
                 f"Punkte: {self.score} | Fehler: {self.wrong_answers}/3\n"
                 f"Serie: {self.streak}🔥"
        )
        self.update_highscores_display()

    def load_highscores(self):
        # Lädt die highscores aus der Datei
        try:
            with open(HIGHSCORES_FILE, "r", encoding="utf-8") as file:
                self.highscores = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.highscores = []

    def save_highscores(self):
        # Speichert den aktuellen Score in highscore.json
        self.highscores.append({
            "username": self.username,
            "score": self.score,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        # Sortiere und beschränke auf Top 10
        self.highscores.sort(key=lambda x: x["score"], reverse=True)
        self.highscores = self.highscores[:10]
        
        with open(HIGHSCORES_FILE, "w", encoding="utf-8") as file:
            json.dump(self.highscores, file, indent=2)

    def update_highscores_display(self):
        #   Aktualisiert die highscore-Anzeige#
        scores_text = "🏆 Highscores:\n"
        for i, score in enumerate(self.highscores[:5], 1):
            scores_text += f"{i}. {score['username']}: {score['score']}\n"
        self.highscores_label.config(text=scores_text)

    def end_quiz(self):
        # Beendet das Quiz und zeigt Ergebnisse#
        self.save_highscores()
        self.question_label.config(
            text=f"Spielende!\nPunkte: {self.score}\n"
                 f"Richtig: {self.score}/{len(self.questions)}"
        )
        for btn in self.buttons:
            btn.config(state=tk.DISABLED)
        self.timer_label.config(text="⏳ Zeit abgelaufen!")
        self.show_review_button()

    def show_review_button(self):
        # Zeigt Button zur Fehlerüberprüfung
        review_btn = tk.Button(
            self.window,
            text="Fehler anzeigen",
            command=self.show_review,
            bg="#2196F3",  # Blaue Hintergrundfarbe
            fg="white",
            font=("Arial", 14)
        )
        review_btn.pack(pady=20)

    def show_review(self):
        # Zeigt Fenster mit falschen Antworten
        review_window = tk.Toplevel(self.window)
        review_window.title("Fehleranalyse")
        review_window.geometry("800x600")
        
        tk.Label(review_window, text="Falsch beantwortete Fragen", 
                font=("Arial", 20)).pack(pady=20)
        
        # Zeige alle Fragen mit korrekten Antworten
        for q in self.questions:
            frame = tk.Frame(review_window)
            tk.Label(frame, text=q["question"], wraplength=700).pack()
            tk.Label(frame, text=f"Korrekte Antwort: {q['options'][q['answer']]}").pack()
            frame.pack(pady=10)

# Hauptprogramm
if __name__ == "__main__":
    window = tk.Tk()  # Tkinter Hauptfenster erstellen
    app = QuizApp(window)  # QuizApp-Instanz erzeugen
    window.mainloop()  # GUI-Hauptloop starten
