"""
BeeStudy - terminal study assistant
Run with: python main.py

Functions:
- load_session(): reads simulated study-session data
- make_questions(): creates a quiz from the study topic
- check_answer(): checks a student's answer using simple keywords
- save_result(): stores quiz results in a JSON history file
- main(): runs the study session
"""

import json
from pathlib import Path
from datetime import datetime

SESSION_FILE = Path("data/simulated/study_session_01.json")
RESULTS_FILE = Path("data/results/study_results.json")


def load_session():
    """Load the current study session, or use safe demo content."""
    try:
        with SESSION_FILE.open("r", encoding="utf-8") as file:
            session = json.load(file)
        if not isinstance(session, dict):
            raise ValueError("Study session must be a JSON object.")
        return session
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as error:
        print(f"\nCould not load session file ({error}). Using demo content.")
        return {
            "student": "Student",
            "subject": "Analog Electronics",
            "duration_minutes": 25,
            "activity": "Revision",
            "content": (
                "A differential amplifier amplifies the difference between two input signals. "
                "Differential gain is the gain for the difference between inputs. "
                "Common-mode gain is the gain for a signal common to both inputs. "
                "CMRR is the ratio of differential gain to common-mode gain."
            ),
            "data_source": "simulated"
        }


def make_questions(session):
    """Return beginner-friendly questions related to the session content."""
    content = session.get("content", "").lower()
    questions = []

    if "differential amplifier" in content:
        questions.append({
            "topic": "Differential Amplifier",
            "question": "What does a differential amplifier amplify?",
            "accepted_keywords": ["difference", "input"],
            "answer": "It amplifies the difference between two input signals."
        })
    if "differential gain" in content:
        questions.append({
            "topic": "Differential Gain",
            "question": "What is differential gain?",
            "accepted_keywords": ["gain", "difference"],
            "answer": "Differential gain is the gain for the difference between the two inputs."
        })
    if "common-mode gain" in content:
        questions.append({
            "topic": "Common-Mode Gain",
            "question": "What is common-mode gain?",
            "accepted_keywords": ["gain", "common"],
            "answer": "It is the gain for a signal common to both inputs."
        })
    if "cmrr" in content:
        questions.append({
            "topic": "CMRR",
            "question": "What does CMRR measure?",
            "accepted_keywords": ["ratio", "differential", "common"],
            "answer": "CMRR is the ratio of differential gain to common-mode gain."
        })

    if not questions:
        questions = [{
            "topic": session.get("subject", "General Study"),
            "question": "Write one important idea you learned in this session.",
            "accepted_keywords": [],
            "answer": "Review the session notes and identify its main idea."
        }]
    return questions


def check_answer(user_answer, accepted_keywords):
    """Simple keyword-based checking; this is not an AI model."""
    answer = user_answer.lower().strip()
    if not answer:
        return False
    if not accepted_keywords:
        return len(answer.split()) >= 3
    matches = sum(1 for word in accepted_keywords if word in answer)
    required = max(1, (len(accepted_keywords) + 1) // 2)
    return matches >= required


def save_result(result):
    """Append one result to the history file without deleting earlier results."""
    RESULTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    try:
        with RESULTS_FILE.open("r", encoding="utf-8") as file:
            history = json.load(file)
        if not isinstance(history, list):
            history = []
    except (FileNotFoundError, json.JSONDecodeError):
        history = []

    result["timestamp"] = datetime.now().isoformat(timespec="seconds")
    result["data_source"] = "simulated"
    history.append(result)

    with RESULTS_FILE.open("w", encoding="utf-8") as file:
        json.dump(history, file, indent=4, ensure_ascii=False)


def main():
    """Start the terminal study session and quiz."""
    print("\n" + "=" * 48)
    print("🐝  BEESTUDY — YOUR LEARNING COMPANION")
    print("=" * 48)

    session = load_session()
    student = session.get("student", "Student")
    subject = session.get("subject", "General Study")
    duration = session.get("duration_minutes", 0)
    activity = session.get("activity", "Study Session")
    content = session.get("content", "")

    print(f"\nHello, {student}!")
    print(f"Subject : {subject}")
    print(f"Activity: {activity}")
    print(f"Duration: {duration} minutes")
    print("\nSESSION NOTES")
    print("-" * 48)
    print(content or "No study notes were provided.")

    questions = make_questions(session)
    score = 0
    topic_results = []

    print("\nQUIZ TIME")
    print("-" * 48)
    for number, question in enumerate(questions, start=1):
        print(f"\nQ{number}. {question['question']}")
        user_answer = input("Your answer: ")
        correct = check_answer(user_answer, question["accepted_keywords"])

        if correct:
            score += 1
            print("✅ Good job, macha!")
        else:
            print("📘 Keep practising, macha!")
            print(f"Suggested answer: {question['answer']}")

        topic_results.append({
            "topic": question["topic"],
            "correct": correct
        })

    total = len(questions)
    percentage = round((score / total) * 100) if total else 0
    result = {
        "student": student,
        "subject": subject,
        "activity": activity,
        "duration_minutes": duration,
        "score": score,
        "total_questions": total,
        "percentage": percentage,
        "topic_results": topic_results
    }
    save_result(result)

    print("\n" + "=" * 48)
    print(f"FINAL SCORE: {score}/{total} ({percentage}%)")
    print("Your result has been saved for the dashboard.")
    print("Data mode: SIMULATED DEMO")
    print("Run the dashboard with: python -m streamlit run dashboard.py")
    print("=" * 48)


if __name__ == "__main__":
    main()
