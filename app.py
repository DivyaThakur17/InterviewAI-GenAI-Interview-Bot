"""
=============================================================================
InterviewAI - AI-Powered Interview Practice Bot
=============================================================================
Problem Statement #18 | Roll Number #18
Students lack mock interview practice. Build a bot that asks role-based
questions one by one and gives feedback on each answer.

Built with:
- Streamlit
- Google Gemini API (official google-genai SDK)
- python-dotenv
- Streamlit Session State
=============================================================================
"""

import streamlit as st
import pandas as pd
import datetime
import os
from dotenv import load_dotenv

# Import our LLM service functions
import llm_service

# Load environment variables
load_dotenv()

# =============================================================================
# Streamlit Page Configuration
# =============================================================================
st.set_page_config(
    page_title="InterviewAI – AI Practice Bot",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================================
# Custom CSS: Modern Dark Navy & Purple Theme
# =============================================================================
CUSTOM_CSS = """
<style>
    /* Google Fonts Import */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Main Container background subtle glow */
    .stApp {
        background: radial-gradient(circle at 15% 20%, rgba(139, 92, 246, 0.08) 0%, transparent 40%),
                    radial-gradient(circle at 85% 80%, rgba(99, 102, 241, 0.08) 0%, transparent 40%),
                    #0A0E1A;
    }

    /* Card styling */
    .custom-card {
        background: #13192B;
        border: 1px solid #1E293B;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.35);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .custom-card:hover {
        border-color: #384566;
    }

    .hero-card {
        background: linear-gradient(135deg, rgba(30, 27, 75, 0.6) 0%, rgba(19, 25, 43, 0.9) 100%);
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-radius: 20px;
        padding: 32px;
        text-align: center;
        margin-bottom: 28px;
        box-shadow: 0 10px 30px -5px rgba(139, 92, 246, 0.15);
    }

    /* Gradient Header Text */
    .gradient-title {
        background: linear-gradient(135deg, #A78BFA 0%, #C084FC 50%, #818CF8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.5rem;
        margin-bottom: 8px;
    }

    .sub-title {
        color: #94A3B8;
        font-size: 1.1rem;
        margin-bottom: 16px;
    }

    /* Project badge pill */
    .badge-pill {
        display: inline-block;
        padding: 4px 14px;
        background: rgba(139, 92, 246, 0.15);
        border: 1px solid rgba(139, 92, 246, 0.4);
        border-radius: 20px;
        color: #C084FC;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 12px;
    }

    /* Question Box */
    .question-box {
        background: #161F36;
        border-left: 5px solid #8B5CF6;
        border-radius: 12px;
        padding: 20px 24px;
        margin: 15px 0 24px 0;
        font-size: 1.25rem;
        font-weight: 600;
        color: #F8FAFC;
        line-height: 1.6;
    }

    /* Feedback Cards */
    .feedback-section {
        background: #111827;
        border: 1px solid #1F2937;
        border-radius: 12px;
        padding: 20px;
        margin-top: 16px;
    }

    .strength-card {
        background: rgba(16, 185, 129, 0.08);
        border-left: 4px solid #10B981;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 10px;
        color: #D1FAE5;
    }

    .improve-card {
        background: rgba(245, 158, 11, 0.08);
        border-left: 4px solid #F59E0B;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 10px;
        color: #FEF3C7;
    }

    .ideal-card {
        background: rgba(99, 102, 241, 0.08);
        border-left: 4px solid #6366F1;
        border-radius: 8px;
        padding: 16px 20px;
        margin-top: 12px;
        color: #E0E7FF;
        line-height: 1.6;
    }

    /* Metric Card */
    .metric-box {
        background: #161F36;
        border: 1px solid #2A3654;
        border-radius: 14px;
        padding: 20px;
        text-align: center;
    }
    .metric-val {
        font-size: 2.2rem;
        font-weight: 800;
        color: #A78BFA;
    }
    .metric-label {
        color: #94A3B8;
        font-size: 0.9rem;
        font-weight: 500;
        margin-top: 4px;
    }

    /* Button enhancements */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #7C3AED 0%, #6366F1 100%);
        color: #FFFFFF;
        font-weight: 600;
        border: none;
        border-radius: 10px;
        padding: 12px 24px;
        transition: all 0.25s ease;
        box-shadow: 0 4px 14px 0 rgba(124, 58, 237, 0.35);
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px 0 rgba(124, 58, 237, 0.5);
        color: #FFFFFF;
    }

    /* Score badges */
    .score-badge-high {
        background: rgba(16, 185, 129, 0.2);
        color: #34D399;
        border: 1px solid #059669;
        border-radius: 30px;
        padding: 4px 16px;
        font-weight: 700;
        font-size: 1.1rem;
        display: inline-block;
    }
    .score-badge-mid {
        background: rgba(245, 158, 11, 0.2);
        color: #FBBF24;
        border: 1px solid #D97706;
        border-radius: 30px;
        padding: 4px 16px;
        font-weight: 700;
        font-size: 1.1rem;
        display: inline-block;
    }
    .score-badge-low {
        background: rgba(239, 68, 68, 0.2);
        color: #F87171;
        border: 1px solid #DC2626;
        border-radius: 30px;
        padding: 4px 16px;
        font-weight: 700;
        font-size: 1.1rem;
        display: inline-block;
    }

    /* Progress bar tint */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #7C3AED, #A855F7);
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# =============================================================================
# Session State Initialization
# =============================================================================
if "page" not in st.session_state:
    st.session_state.page = "welcome"  # Options: 'welcome', 'interview', 'final'

if "candidate_name" not in st.session_state:
    st.session_state.candidate_name = ""

if "role" not in st.session_state:
    st.session_state.role = "Python Developer"

if "difficulty" not in st.session_state:
    st.session_state.difficulty = "Intermediate"

if "questions" not in st.session_state:
    st.session_state.questions = []

if "current_index" not in st.session_state:
    st.session_state.current_index = 0

if "current_evaluation" not in st.session_state:
    st.session_state.current_evaluation = None

if "history" not in st.session_state:
    st.session_state.history = []

if "final_summary" not in st.session_state:
    st.session_state.final_summary = None

if "interview_date" not in st.session_state:
    st.session_state.interview_date = ""

# Available options per specification
ROLE_OPTIONS = [
    "Java Developer",
    "Python Developer",
    "Software Engineer",
    "Frontend Developer",
    "Data Analyst",
    "AI/ML Engineer",
    "HR Interview",
]

DIFFICULTY_OPTIONS = ["Beginner", "Intermediate", "Advanced"]


# =============================================================================
# Helper Functions
# =============================================================================
def reset_interview():
    """Reset all interview variables and return to welcome page."""
    st.session_state.page = "welcome"
    st.session_state.questions = []
    st.session_state.current_index = 0
    st.session_state.current_evaluation = None
    st.session_state.history = []
    st.session_state.final_summary = None
    st.session_state.interview_date = ""
    st.rerun()


def render_score_badge(score: int) -> str:
    """Return styled HTML badge according to score range."""
    if score >= 8:
        return f'<span class="score-badge-high">⭐ {score} / 10 &nbsp;•&nbsp; Strong</span>'
    elif score >= 5:
        return f'<span class="score-badge-mid">⚡ {score} / 10 &nbsp;•&nbsp; Moderate</span>'
    else:
        return f'<span class="score-badge-low">⚠️ {score} / 10 &nbsp;•&nbsp; Needs Work</span>'


def build_text_report() -> str:
    """Generate a clean, structured text report for candidate download."""
    history = st.session_state.history
    total_score = sum(item["score"] for item in history)
    max_score = len(history) * 10
    percentage = (total_score / max_score * 100) if max_score > 0 else 0
    avg_score = (total_score / len(history)) if len(history) > 0 else 0

    verdict = (
        st.session_state.final_summary.get("verdict", "Completed")
        if st.session_state.final_summary
        else "Completed"
    )
    overall_summary = (
        st.session_state.final_summary.get("overall_summary", "N/A")
        if st.session_state.final_summary
        else "N/A"
    )

    lines = [
        "=" * 70,
        "INTERVIEWAI – MOCK INTERVIEW EVALUATION REPORT",
        "Problem Statement #18 | Roll Number #18",
        "=" * 70,
        f"Candidate Name    : {st.session_state.candidate_name}",
        f"Target Role       : {st.session_state.role}",
        f"Difficulty Level  : {st.session_state.difficulty}",
        f"Interview Date    : {st.session_state.interview_date}",
        "-" * 70,
        f"OVERALL PERFORMANCE",
        f"Total Score       : {total_score} / {max_score}",
        f"Percentage        : {percentage:.1f}%",
        f"Average Score     : {avg_score:.1f} / 10",
        f"Hiring Verdict    : {verdict}",
        "-" * 70,
        f"OVERALL EVALUATION SUMMARY:",
        overall_summary,
        "=" * 70,
        "",
        "QUESTION-BY-QUESTION BREAKDOWN:",
        "",
    ]

    for item in history:
        lines.append(f"Question {item['question_num']}: {item['question']}")
        lines.append(f"Candidate's Answer:\n{item['answer']}")
        lines.append(f"Score: {item['score']} / 10")
        lines.append(f"Feedback: {item['feedback']}")
        lines.append("Key Strengths:")
        for s in item.get("strengths", []):
            lines.append(f"  • {s}")
        lines.append("Areas for Improvement:")
        for imp in item.get("improvements", []):
            lines.append(f"  • {imp}")
        lines.append(f"Ideal Model Answer:\n{item.get('ideal_answer', 'N/A')}")
        lines.append("-" * 70)
        lines.append("")

    lines.append("Generated by InterviewAI – AI-Powered Interview Practice Bot")
    lines.append("=" * 70)
    return "\n".join(lines)


# =============================================================================
# Sidebar
# =============================================================================
with st.sidebar:
    st.markdown("### 🎯 **InterviewAI**")
    st.caption("AI-Powered Technical & HR Practice")
    st.markdown("<hr style='margin: 10px 0; border-color: #1E293B;'>", unsafe_allow_html=True)

    # API Key Configuration Indicator
    configured_key = llm_service.get_api_key()
    configured_model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

    if configured_key and configured_key != "your_gemini_api_key_here":
        st.markdown(
            """
            <div style="background: rgba(16, 185, 129, 0.15); border: 1px solid #059669; border-radius: 8px; padding: 10px 14px; margin-bottom: 15px;">
                <span style="color: #34D399; font-weight: 600; font-size: 0.85rem;">🟢 Gemini API Connected</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div style="background: rgba(239, 68, 68, 0.15); border: 1px solid #DC2626; border-radius: 8px; padding: 10px 14px; margin-bottom: 15px;">
                <span style="color: #F87171; font-weight: 600; font-size: 0.85rem;">🔴 Gemini API Key Missing</span><br>
                <small style="color: #CBD5E1;">Add key in <code>.env</code> file</small>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(f"**🤖 Model:** `{configured_model}`")

    # Session Status in Sidebar
    if st.session_state.page in ["interview", "final"]:
        st.markdown("<hr style='margin: 12px 0; border-color: #1E293B;'>", unsafe_allow_html=True)
        st.markdown("#### 👤 **Candidate Info**")
        st.write(f"**Name:** {st.session_state.candidate_name}")
        st.write(f"**Role:** {st.session_state.role}")
        st.write(f"**Difficulty:** {st.session_state.difficulty}")

        if st.session_state.page == "interview":
            q_num = st.session_state.current_index + 1
            st.markdown(f"**Progress:** Question {q_num} of 5")
            st.progress(q_num / 5)

            # Live Score Tally
            if st.session_state.history:
                live_score = sum(item["score"] for item in st.session_state.history)
                st.markdown(f"**Current Score:** `{live_score} / {len(st.session_state.history) * 10}`")

        st.markdown("<hr style='margin: 16px 0; border-color: #1E293B;'>", unsafe_allow_html=True)
        if st.button("🔄 Restart Interview", use_container_width=True):
            reset_interview()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="color: #64748B; font-size: 0.75rem; text-align: center;">
            Problem Statement #18 • Roll #18<br>
            GenAI Final-Year Mini Project
        </div>
        """,
        unsafe_allow_html=True,
    )


# =============================================================================
# View 1: Welcome / Setup Page
# =============================================================================
if st.session_state.page == "welcome":
    st.markdown(
        """
        <div class="hero-card">
            <span class="badge-pill">🎓 Final Year GenAI Mini Project • PS #18 • Roll #18</span>
            <div class="gradient-title">InterviewAI</div>
            <div class="sub-title">Master your technical and HR interviews with real-time AI role-based evaluation</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([1.2, 0.8], gap="large")

    with col1:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.subheader("📋 Candidate Profile & Interview Setup")
        st.markdown("Configure your mock interview session below:")

        candidate_name = st.text_input(
            "Candidate Full Name *",
            placeholder="e.g. Divya Sharma",
            value=st.session_state.candidate_name,
        )

        role_selected = st.selectbox(
            "Select Target Job Role *",
            options=ROLE_OPTIONS,
            index=ROLE_OPTIONS.index(st.session_state.role)
            if st.session_state.role in ROLE_OPTIONS
            else 1,
            help="Choose the specific technical or managerial track you want to practice for.",
        )

        diff_selected = st.select_slider(
            "Select Difficulty Level *",
            options=DIFFICULTY_OPTIONS,
            value=st.session_state.difficulty,
            help="Beginner (fundamentals), Intermediate (practical application), Advanced (system design & optimization)",
        )

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("🚀 Start Interview", use_container_width=True):
            # Validation Checks
            if not candidate_name.strip():
                st.error("⚠️ Please enter your name before starting the interview.")
            elif not configured_key or configured_key == "your_gemini_api_key_here":
                st.error(
                    "⚠️ Gemini API Key not detected! Please configure `GEMINI_API_KEY` in your `.env` file first."
                )
            else:
                with st.spinner("🤖 InterviewAI is generating 5 unique, role-specific questions with Gemini..."):
                    try:
                        questions = llm_service.generate_interview_questions(
                            role=role_selected,
                            difficulty=diff_selected,
                            num_questions=5,
                        )

                        # Update Session State
                        st.session_state.candidate_name = candidate_name.strip()
                        st.session_state.role = role_selected
                        st.session_state.difficulty = diff_selected
                        st.session_state.questions = questions
                        st.session_state.current_index = 0
                        st.session_state.current_evaluation = None
                        st.session_state.history = []
                        st.session_state.interview_date = datetime.datetime.now().strftime(
                            "%B %d, %Y, %I:%M %p"
                        )
                        st.session_state.page = "interview"
                        st.rerun()

                    except Exception as e:
                        st.error(f"❌ Error generating questions: {str(e)}")
                        st.info("Tip: Check your internet connection and verify that your Gemini API key has quota.")

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.subheader("💡 How It Works")
        st.markdown(
            """
            1. **Select Role & Difficulty**: 7 distinct tracks with custom difficulty calibration.
            2. **5 Real AI Questions**: Generated dynamically using Google Gemini Flash model.
            3. **Submit One by One**: Type your candid response in the answer console.
            4. **Instant Objective Grading**: Receive:
               - Detailed Score out of 10
               - Constructive Feedback
               - Key Strengths Identified
               - Specific Improvement Areas
               - Benchmark Ideal Answer
            5. **Final Comprehensive Dashboard**: View total score out of 50, visual bar chart, and download your full PDF/Text report!
            """
        )
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            """
            <div class="custom-card" style="border-left: 4px solid #8B5CF6;">
                <h4 style="margin: 0 0 8px 0; color: #C084FC;">🔒 Untrusted Input Protection</h4>
                <p style="color: #94A3B8; font-size: 0.85rem; margin: 0;">
                    All submitted answers are safely treated as strictly untrusted candidate data to protect against prompt injection and jailbreak attempts.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )


# =============================================================================
# View 2: Interview Execution Screen (Question by Question)
# =============================================================================
elif st.session_state.page == "interview":
    q_index = st.session_state.current_index
    total_q = len(st.session_state.questions)
    current_question = st.session_state.questions[q_index]

    # Top Navigation / Progress Header
    col_hdr1, col_hdr2 = st.columns([3, 1])
    with col_hdr1:
        st.markdown(
            f"""
            <span class="badge-pill">📌 {st.session_state.role} &nbsp;•&nbsp; {st.session_state.difficulty}</span>
            <h2 style="margin: 4px 0 8px 0; color: #F8FAFC;">Question {q_index + 1} of {total_q}</h2>
            """,
            unsafe_allow_html=True,
        )
    with col_hdr2:
        progress_val = (q_index + 1) / total_q
        st.progress(progress_val)
        st.caption(f"Completed: {q_index}/{total_q} questions")

    # Question Display Box
    st.markdown(
        f"""
        <div class="question-box">
            {current_question}
        </div>
        """,
        unsafe_allow_html=True,
    )

    # If this question has NOT been evaluated yet, show input form
    if st.session_state.current_evaluation is None:
        st.markdown("#### ✍️ **Your Answer:**")
        answer_key = f"answer_input_{q_index}"
        candidate_ans = st.text_area(
            "Type your response below (explain concepts clearly, give examples where helpful):",
            key=answer_key,
            height=200,
            placeholder="Type your detailed answer here...",
        )

        col_b1, col_b2 = st.columns([1, 4])
        with col_b1:
            submit_btn = st.button("📤 Submit Answer", use_container_width=True)

        if submit_btn:
            if not candidate_ans or not candidate_ans.strip():
                st.warning("⚠️ Please provide an answer before submitting. Empty submissions cannot be evaluated.")
            elif len(candidate_ans.strip()) < 10:
                st.warning("⚠️ Your answer is very short. Please elaborate to receive an accurate evaluation.")
            else:
                with st.spinner("🔍 Evaluating your answer with Gemini AI..."):
                    try:
                        evaluation = llm_service.evaluate_answer(
                            role=st.session_state.role,
                            difficulty=st.session_state.difficulty,
                            question=current_question,
                            candidate_answer=candidate_ans.strip(),
                        )

                        # Save evaluation into session state
                        st.session_state.current_evaluation = evaluation
                        # Record in history
                        st.session_state.history.append({
                            "question_num": q_index + 1,
                            "question": current_question,
                            "answer": candidate_ans.strip(),
                            "score": evaluation["score"],
                            "feedback": evaluation["feedback"],
                            "strengths": evaluation["strengths"],
                            "improvements": evaluation["improvements"],
                            "ideal_answer": evaluation["ideal_answer"],
                        })
                        st.rerun()

                    except Exception as e:
                        st.error(f"❌ Evaluation Error: {str(e)}")
                        st.info("Please retry submitting your answer.")

    # If this question HAS been evaluated, display feedback and 'Next' button
    else:
        eval_data = st.session_state.current_evaluation
        score = eval_data["score"]

        # Evaluation Result Card
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        col_res1, col_res2 = st.columns([3, 1])

        with col_res1:
            st.markdown("### 📊 AI Evaluation Feedback")
        with col_res2:
            st.markdown(render_score_badge(score), unsafe_allow_html=True)

        st.markdown(f"**Constructive Feedback:** {eval_data['feedback']}")

        col_f1, col_f2 = st.columns(2, gap="medium")
        with col_f1:
            st.markdown("#### ✅ **Key Strengths**")
            for strength in eval_data["strengths"]:
                st.markdown(
                    f'<div class="strength-card">✔ {strength}</div>',
                    unsafe_allow_html=True,
                )

        with col_f2:
            st.markdown("#### 💡 **Improvement Suggestions**")
            for imp in eval_data["improvements"]:
                st.markdown(
                    f'<div class="improve-card">📌 {imp}</div>',
                    unsafe_allow_html=True,
                )

        # Ideal Model Answer Collapsible
        with st.expander("📖 View Benchmark Ideal Answer", expanded=True):
            st.markdown(
                f'<div class="ideal-card">{eval_data["ideal_answer"]}</div>',
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)

        # Navigation to Next Question or Final Summary
        col_n1, col_n2 = st.columns([1.5, 3.5])
        with col_n1:
            if q_index + 1 < total_q:
                if st.button("➡️ Next Question", use_container_width=True):
                    st.session_state.current_index += 1
                    st.session_state.current_evaluation = None
                    st.rerun()
            else:
                if st.button("🏁 View Final Performance Dashboard", use_container_width=True):
                    with st.spinner("📊 Compiling your final interview performance dashboard..."):
                        summary = llm_service.generate_final_summary(
                            candidate_name=st.session_state.candidate_name,
                            role=st.session_state.role,
                            difficulty=st.session_state.difficulty,
                            history=st.session_state.history,
                        )
                        st.session_state.final_summary = summary
                        st.session_state.page = "final"
                        st.rerun()


# =============================================================================
# View 3: Final Performance Dashboard
# =============================================================================
elif st.session_state.page == "final":
    history = st.session_state.history
    total_score = sum(item["score"] for item in history)
    max_score = len(history) * 10
    percentage = (total_score / max_score * 100) if max_score > 0 else 0
    avg_score = (total_score / len(history)) if len(history) > 0 else 0
    final_summary = st.session_state.final_summary or {}

    # Header
    st.markdown(
        f"""
        <div class="hero-card">
            <span class="badge-pill">🎉 Interview Completed • Final Evaluation</span>
            <div class="gradient-title">Performance Summary</div>
            <div class="sub-title">Candidate: <strong>{st.session_state.candidate_name}</strong> &nbsp;|&nbsp; Role: <strong>{st.session_state.role}</strong> &nbsp;|&nbsp; Level: <strong>{st.session_state.difficulty}</strong></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Top Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(
            f"""
            <div class="metric-box">
                <div class="metric-val">{total_score} <span style="font-size: 1.2rem; color: #94A3B8;">/ {max_score}</span></div>
                <div class="metric-label">TOTAL SCORE</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m2:
        st.markdown(
            f"""
            <div class="metric-box">
                <div class="metric-val">{percentage:.1f}%</div>
                <div class="metric-label">PERCENTAGE</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m3:
        st.markdown(
            f"""
            <div class="metric-box">
                <div class="metric-val">{avg_score:.1f} <span style="font-size: 1.2rem; color: #94A3B8;">/ 10</span></div>
                <div class="metric-label">AVERAGE SCORE</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m4:
        verdict = final_summary.get("verdict", "Candidate Evaluated")
        st.markdown(
            f"""
            <div class="metric-box">
                <div class="metric-val" style="font-size: 1.3rem; color: #34D399; margin-top: 8px;">{verdict}</div>
                <div class="metric-label">OVERALL VERDICT</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Chart & Overall Remarks
    col_chart, col_eval = st.columns([1.2, 1], gap="large")

    with col_chart:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown("### 📈 Question-wise Score Breakdown")

        chart_data = pd.DataFrame({
            "Question": [f"Q{item['question_num']}" for item in history],
            "Score (out of 10)": [item["score"] for item in history],
        })
        chart_data = chart_data.set_index("Question")
        st.bar_chart(chart_data, color="#8B5CF6")
        st.caption("Visual breakdown of your performance across each individual question.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_eval:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown("### 🎯 Evaluator Final Remarks")
        st.write(final_summary.get("overall_summary", "Great performance overall!"))

        st.markdown("#### 🌟 Key Takeaways")
        for t in final_summary.get("key_takeaways", []):
            st.markdown(f"• {t}")

        st.markdown("#### 🚀 Preparation Tips")
        for tip in final_summary.get("preparation_tips", []):
            st.markdown(f"• {tip}")
        st.markdown("</div>", unsafe_allow_html=True)

    # Detailed Accordion Breakdown of All Questions
    st.markdown("### 📑 Detailed Question Review")
    for item in history:
        with st.expander(
            f"Question {item['question_num']}: {item['question']} — Score: {item['score']}/10",
            expanded=False,
        ):
            st.markdown(f"**Your Submitted Answer:**")
            st.info(item["answer"])

            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("**Strengths:**")
                for s in item.get("strengths", []):
                    st.markdown(f"• {s}")
            with col_b:
                st.markdown("**Improvement Points:**")
                for imp in item.get("improvements", []):
                    st.markdown(f"• {imp}")

            st.markdown("**Ideal Benchmark Answer:**")
            st.success(item.get("ideal_answer", "N/A"))

    st.markdown("<br>", unsafe_allow_html=True)

    # Action Buttons: Download Report & Restart
    col_act1, col_act2, col_act3 = st.columns([1.5, 1.5, 2])

    with col_act1:
        report_text = build_text_report()
        st.download_button(
            label="📥 Download Performance Report",
            data=report_text,
            file_name=f"InterviewAI_Report_{st.session_state.candidate_name.replace(' ', '_')}.txt",
            mime="text/plain",
            use_container_width=True,
        )

    with col_act2:
        if st.button("🔄 Practice Again", use_container_width=True):
            reset_interview()

    st.markdown("<br><br>", unsafe_allow_html=True)
