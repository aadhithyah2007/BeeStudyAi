"""
BeeStudy - futuristic interactive Streamlit dashboard
Run with: python -m streamlit run dashboard.py

Features:
- Neon/glass-style theme
- Dashboard, quiz, progress, and recommendations pages
- Reads saved quiz history from data/results/study_results.json
- Quiz answers and scores are saved to the same history file
- Clearly labels the current demo data as simulated
"""

import json
from pathlib import Path
from datetime import datetime

import streamlit as st

RESULTS_FILE = Path("data/results/study_results.json")

st.set_page_config(
    page_title="BeeStudy | AI Learning Hub",
    page_icon="🐝",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.stApp {
    background:
      radial-gradient(ellipse at 10% 0%, rgba(0,130,255,.18), transparent 38%),
      radial-gradient(ellipse at 90% 100%, rgba(135,45,255,.16), transparent 40%),
      #050817;
    color: #EAF3FF;
}
[data-testid="stHeader"] { background: transparent; }
[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#09152E,#08091B);
    border-right: 1px solid #174C91;
}
h1,h2,h3 { color:#EAF5FF !important; }
.bs-banner {
    background: linear-gradient(110deg,#102A62,#30105B,#082C48);
    border:1px solid #376DFF; border-radius:22px;
    padding:26px; margin:8px 0 22px;
    box-shadow:0 0 28px rgba(66,80,255,.2);
}
.bs-card {
    background:linear-gradient(135deg,rgba(15,35,75,.95),rgba(14,12,42,.95));
    border:1px solid rgba(0,190,255,.5); border-radius:17px;
    padding:20px; min-height:120px;
    box-shadow:0 0 18px rgba(0,140,255,.09);
    transition:all .22s ease;
}
.bs-card:hover {
    border-color:#42E8FF;
    box-shadow:0 0 24px rgba(0,190,255,.26);
    transform:translateY(-3px);
}
.bs-label { color:#9BB8E8; font-size:14px; }
.bs-value { color:#47E8FF; font-size:30px; font-weight:750; margin-top:8px; }
.bs-muted { color:#A9BCE0; font-size:14px; }
.stButton>button {
    background:linear-gradient(100deg,#0759D9,#692DE0);
    color:white; border:1px solid #5AABFF; border-radius:11px;
    transition:all .2s ease;
}
.stButton>button:hover {
    border-color:#54F0FF; box-shadow:0 0 18px rgba(0,190,255,.35); color:white;
}
.stTextInput input,.stTextArea textarea {
    background:#0B1530; color:white; border:1px solid #31568F; border-radius:10px;
}
[data-testid="stMetric"] {
    background:rgba(13,29,61,.8); border:1px solid #234B85;
    border-radius:14px; padding:14px;
}
[data-testid="stMetricValue"] { color:#4AEAFF; }
.stProgress>div>div>div { background:linear-gradient(90deg,#087BFF,#9D4DFF,#42E8FF); }
#MainMenu,footer { visibility:hidden; }
</style>
""", unsafe_allow_html=True)


def load_results():
    """Read saved results; return an empty list if no history exists."""
    try:
        with RESULTS_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
        return data if isinstance(data, list) else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_result(result):
    """Append a result to the history JSON file."""
    RESULTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    history = load_results()
    result["timestamp"] = datetime.now().isoformat(timespec="seconds")
    result["data_source"] = "simulated"
    history.append(result)
    with RESULTS_FILE.open("w", encoding="utf-8") as file:
        json.dump(history, file, indent=4, ensure_ascii=False)


def render_card(label, value, emoji):
    """Display a reusable neon metric card."""
    st.markdown(
        f'<div class="bs-card"><div class="bs-label">{emoji} {label}</div>'
        f'<div class="bs-value">{value}</div></div>',
        unsafe_allow_html=True
    )


def make_dashboard(history):
    """Show summary metrics and the most recent study history."""
    st.markdown("## ⚡ Your Learning Hub")
    total_sessions = len(history)
    total_minutes = sum(int(item.get("duration_minutes", 0) or 0) for item in history)
    total_questions = sum(int(item.get("total_questions", 0) or 0) for item in history)
    total_correct = sum(int(item.get("score", 0) or 0) for item in history)
    avg_score = round(total_correct / total_questions * 100) if total_questions else 0

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_card("Study Sessions", total_sessions, "📚")
    with c2:
        render_card("Study Time", f"{total_minutes} min", "⏱️")
    with c3:
        render_card("Average Quiz Score", f"{avg_score}%", "🎯")
    with c4:
        render_card("Questions Answered", total_questions, "🧠")

    st.markdown("### 📡 Recent Activity")
    if not history:
        st.info("No saved results yet. Go to Study Quiz or run `python main.py` to create your first result.")
        return

    rows = []
    for item in reversed(history[-10:]):
        rows.append({
            "Date": item.get("timestamp", "Unknown"),
            "Subject": item.get("subject", "General Study"),
            "Activity": item.get("activity", "Study Session"),
            "Score": f"{item.get('score', 0)}/{item.get('total_questions', 0)}",
            "Percentage": f"{item.get('percentage', 0)}%",
            "Source": item.get("data_source", "simulated")
        })
    st.dataframe(rows, use_container_width=True, hide_index=True)


def make_quiz():
    """Interactive browser quiz; saves the score when submitted."""
    st.markdown("## 🧠 Knowledge Check")
    st.write("Test your Analog Electronics basics. Choose one answer for each question.")

    questions = [
        {
            "topic": "Differential Amplifier",
            "question": "What does a differential amplifier amplify?",
            "options": [
                "The difference between two input signals",
                "Only the supply voltage",
                "Only the common signal",
                "The temperature of the circuit"
            ],
            "answer": "The difference between two input signals"
        },
        {
            "topic": "CMRR",
            "question": "What does CMRR describe?",
            "options": [
                "Power supply voltage",
                "Ability to reject common-mode signals",
                "Transistor size",
                "Output resistance only"
            ],
            "answer": "Ability to reject common-mode signals"
        },
        {
            "topic": "Common-Mode Gain",
            "question": "An ideal differential amplifier has what common-mode gain?",
            "options": ["Very high", "Infinite", "Zero", "Always equal to 1"],
            "answer": "Zero"
        },
        {
            "topic": "Differential Gain",
            "question": "Differential gain is the gain for which input?",
            "options": [
                "Difference between the inputs",
                "Common signal at both inputs",
                "Supply ripple only",
                "No input signal"
            ],
            "answer": "Difference between the inputs"
        }
    ]

    with st.form("beestudy_quiz_form"):
        student = st.text_input("Your name (optional)", placeholder="Student")
        answers = []
        for i, question in enumerate(questions):
            choice = st.radio(
                f"Q{i + 1}. {question['question']}",
                question["options"],
                key=f"quiz_answer_{i}"
            )
            answers.append(choice)
        submitted = st.form_submit_button("⚡ Submit Quiz", use_container_width=True)

    if submitted:
        score = sum(
            1 for question, answer in zip(questions, answers)
            if answer == question["answer"]
        )
        percentage = round(score / len(questions) * 100)
        topic_results = [
            {"topic": q["topic"], "correct": answer == q["answer"]}
            for q, answer in zip(questions, answers)
        ]
        save_result({
            "student": student.strip() or "Student",
            "subject": "Analog Electronics",
            "activity": "Browser Quiz",
            "duration_minutes": 0,
            "score": score,
            "total_questions": len(questions),
            "percentage": percentage,
            "topic_results": topic_results
        })
        st.session_state["last_quiz_score"] = score
        st.session_state["last_quiz_total"] = len(questions)
        st.session_state["last_quiz_percentage"] = percentage

    if "last_quiz_score" in st.session_state:
        score = st.session_state["last_quiz_score"]
        total = st.session_state["last_quiz_total"]
        percentage = st.session_state["last_quiz_percentage"]
        st.markdown("### 🏆 Your Result")
        st.progress(percentage / 100)
        st.metric("Quiz Score", f"{score}/{total}", f"{percentage}%")
        if percentage >= 75:
            st.success("Excellent work, macha! Keep building on this.")
        elif percentage >= 50:
            st.info("Good effort! Revise the missed concepts and try again.")
        else:
            st.warning("Keep practising. Review your notes and retry the quiz.")
        st.caption("This quiz is a built-in demo quiz; results are saved as simulated demo data.")


def make_progress(history):
    """Show a progress chart based on saved quiz results."""
    st.markdown("## 📈 Your Progress")
    quiz_history = [x for x in history if int(x.get("total_questions", 0) or 0) > 0]
    if not quiz_history:
        st.info("Complete a quiz to see your progress chart.")
        return

    chart_rows = []
    for index, item in enumerate(quiz_history, start=1):
        chart_rows.append({
            "Attempt": f"Attempt {index}",
            "Score (%)": int(item.get("percentage", 0) or 0)
        })
    st.line_chart(chart_rows, x="Attempt", y="Score (%)")
    st.markdown("### 🧩 Topic accuracy")
    topic_stats = {}
    for item in quiz_history:
        for topic in item.get("topic_results", []):
            name = topic.get("topic", "Other")
            stats = topic_stats.setdefault(name, {"correct": 0, "total": 0})
            stats["total"] += 1
            stats["correct"] += int(bool(topic.get("correct")))
    if topic_stats:
        for name, stats in topic_stats.items():
            accuracy = round(stats["correct"] / stats["total"] * 100)
            st.write(f"**{name}** — {accuracy}%")
            st.progress(accuracy / 100)


def make_recommendations(history):
    """Suggest next steps from topic results without pretending to be AI."""
    st.markdown("## 💡 Study Recommendations")
    topic_stats = {}
    for item in history:
        for topic in item.get("topic_results", []):
            name = topic.get("topic", "Other")
            stats = topic_stats.setdefault(name, {"correct": 0, "total": 0})
            stats["total"] += 1
            stats["correct"] += int(bool(topic.get("correct")))

    if not topic_stats:
        st.info("Complete a quiz first. BeeStudy will use the saved answers to suggest what to revise.")
        st.write("- Start with Differential Amplifier basics.")
        st.write("- Learn differential gain and common-mode gain.")
        st.write("- Practise CMRR definitions and numericals.")
        return

    sorted_topics = sorted(
        topic_stats.items(),
        key=lambda item: item[1]["correct"] / item[1]["total"]
    )
    weakest_topic, stats = sorted_topics[0]
    accuracy = round(stats["correct"] / stats["total"] * 100)
    st.markdown(
        f'<div class="bs-card"><div class="bs-label">NEXT TOPIC TO REVIEW</div>'
        f'<div class="bs-value">{weakest_topic}</div>'
        f'<p class="bs-muted">Current recorded accuracy: {accuracy}%</p></div>',
        unsafe_allow_html=True
    )
    st.write("Suggested plan:")
    st.write("1. Review the definition and key formula.")
    st.write("2. Solve two short questions without looking at notes.")
    st.write("3. Retake the quiz and compare your result.")


def main():
    """Build the app layout and route between pages."""
    st.sidebar.markdown("# 🐝 BeeStudy")
    st.sidebar.caption("LEARN  •  TRACK  •  GROW")
    page = st.sidebar.radio(
        "Navigation",
        ["Dashboard", "Study Quiz", "Progress", "Recommendations"],
        index=0
    )
    st.sidebar.divider()
    st.sidebar.info("Demo mode: data is simulated. No wearable is connected.")

    st.markdown("""
    <div class="bs-banner">
      <div style="color:#55E9FF;font-size:13px;letter-spacing:2px;">
        B E E S T U D Y  •  PERSONAL LEARNING SYSTEM
      </div>
      <h1 style="margin:12px 0 8px 0;">Your futuristic study cockpit 🐝</h1>
      <p style="font-size:17px;color:#D3E4FF;">
        Study smarter. Track your progress. Grow every day.
      </p>
      <p style="color:#AABEFF;">✦ Small steps today. Stronger concepts tomorrow.</p>
    </div>
    """, unsafe_allow_html=True)

    history = load_results()
    if page == "Dashboard":
        make_dashboard(history)
    elif page == "Study Quiz":
        make_quiz()
    elif page == "Progress":
        make_progress(load_results())
    elif page == "Recommendations":
        make_recommendations(load_results())

    st.divider()
    st.caption("🐝 BeeStudy v1.0 • Demo mode • Study results are stored locally on this computer.")


if __name__ == "__main__":
    main()
