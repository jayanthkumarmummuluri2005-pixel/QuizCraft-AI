import os
import json
import html
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# ==================================================
# PAGE CONFIGURATION
# ==================================================
st.set_page_config(
    page_title="QuizCraft AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==================================================
# GROQ CONFIGURATION
# ==================================================
load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    st.error("Groq API key not found. Check your .env file.")
    st.stop()

client = Groq(api_key=API_KEY)

# ==================================================
# SIMPLE, ATTRACTIVE CSS
# ==================================================
st.markdown("""
<style>
/* Main background */
.stApp {
    background: #0B1020;
    color: #F1F5F9;
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stMainBlockContainer"] {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #10172A;
    border-right: 1px solid #26324B;
}

.brand {
    font-size: 27px;
    font-weight: 800;
    color: #FFFFFF;
    letter-spacing: -1px;
}

.brand span {
    color: #A78BFA;
}

.brand-sub {
    color: #94A3B8;
    font-size: 12px;
    margin-top: 4px;
}

h1, h2, h3 {
    color: #F8FAFC !important;
    letter-spacing: -0.5px;
}

p {
    color: #CBD5E1;
}

label {
    color: #E2E8F0 !important;
}

/* Hero */
.hero {
    background: linear-gradient(120deg, #171F3B, #241B43);
    border: 1px solid #39345F;
    border-radius: 18px;
    padding: 28px;
    margin-bottom: 24px;
}

.hero-title {
    font-size: clamp(30px, 4vw, 43px);
    font-weight: 850;
    color: #FFFFFF;
    letter-spacing: -1.3px;
}

.hero-title span {
    color: #A78BFA;
}

.hero-subtitle {
    color: #B8C4D9;
    font-size: 16px;
    margin-top: 8px;
}

.hero-badge {
    display: inline-block;
    margin-top: 18px;
    padding: 7px 12px;
    border-radius: 8px;
    background: #302653;
    color: #DDD6FE;
    font-size: 12px;
}

/* Cards */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #111A2E;
    border: 1px solid #283550 !important;
    border-radius: 15px !important;
}

/* Question card */
.question-card {
    background: #131D33;
    border: 1px solid #303D5C;
    border-left: 4px solid #8B5CF6;
    border-radius: 14px;
    padding: 23px;
    margin: 20px 0 14px;
}

.question-label {
    color: #A78BFA;
    font-size: 12px;
    font-weight: 750;
    letter-spacing: 1.3px;
    margin-bottom: 12px;
}

.question-text {
    color: #F8FAFC;
    font-size: 19px;
    line-height: 1.6;
    font-weight: 650;
}

/* Input fields */
div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div {
    background: #0D1425 !important;
    border: 1px solid #34415D !important;
    border-radius: 9px !important;
}

div[data-baseweb="input"] input {
    color: #FFFFFF !important;
}

div[data-baseweb="select"] * {
    color: #F8FAFC !important;
}

/* Answer options */
div[role="radiogroup"] {
    gap: 9px;
}

div[role="radiogroup"] > label {
    background: #111A2E;
    border: 1px solid #2B3955;
    border-radius: 10px;
    padding: 11px 14px;
    transition: border-color 0.2s ease;
}

div[role="radiogroup"] > label:hover {
    border-color: #8B5CF6;
    background: #19213B;
}

div[role="radiogroup"] > label:has(input:checked) {
    background: #252044;
    border-color: #A78BFA;
}

div[role="radiogroup"] > label p {
    color: #E2E8F0 !important;
}

/* Buttons */
.stButton > button,
.stFormSubmitButton > button {
    min-height: 43px;
    width: 100%;
    background: #7C3AED;
    color: #FFFFFF !important;
    border: 1px solid #8B5CF6;
    border-radius: 10px;
    font-weight: 650;
    transition: background 0.2s ease;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background: #6D28D9;
    border-color: #A78BFA;
}

/* Metrics */
div[data-testid="stMetric"] {
    background: #131D33;
    border: 1px solid #2B3955;
    border-radius: 12px;
    padding: 15px;
}

div[data-testid="stMetricLabel"] {
    color: #A5B4CF !important;
}

div[data-testid="stMetricValue"] {
    color: #FFFFFF !important;
}

/* Progress */
div[data-testid="stProgressBar"] > div > div {
    background: #8B5CF6;
}

/* Alerts */
div[data-testid="stAlert"] {
    border-radius: 10px;
}

/* Dividers */
hr {
    border-color: #26324B !important;
}

/* Footer */
.footer {
    text-align: center;
    color: #64748B;
    font-size: 12px;
    padding-top: 25px;
}

@media (max-width: 768px) {
    [data-testid="stMainBlockContainer"] {
        padding: 1rem;
    }

    .hero {
        padding: 20px;
    }

    .question-text {
        font-size: 17px;
    }
}
</style>
""", unsafe_allow_html=True)


# ==================================================
# AI QUESTION GENERATOR
# ==================================================
def generate_mcqs(topic, difficulty, number):

    prompt = f"""
Create exactly {number} multiple-choice questions
about "{topic}".

Difficulty: {difficulty}

Return a valid JSON object in this format:
{{
  "questions": [
    {{
      "question": "Question text",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "answer": 0
    }}
  ]
}}

Rules:
- Generate exactly {number} questions.
- Every question must have exactly four non-empty options.
- Options should be distinct.
- The answer must be an integer from 0 to 3.
- The answer index must identify the correct option.
- Return JSON only, without markdown.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You generate accurate educational quizzes. "
                    "Return only valid JSON."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.3,
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content

    if not content:
        raise ValueError("The AI returned an empty response.")

    data = json.loads(content)
    questions = data.get("questions")

    if not isinstance(questions, list) or len(questions) != number:
        raise ValueError(
            f"Expected {number} questions. Please generate the quiz again."
        )

    for q in questions:

        if not isinstance(q, dict):
            raise ValueError("Invalid question format.")

        if not isinstance(q.get("question"), str):
            raise ValueError("A question is missing its text.")

        options = q.get("options")
        answer = q.get("answer")

        if (
            not isinstance(options, list)
            or len(options) != 4
            or not all(
                isinstance(option, str) and option.strip()
                for option in options
            )
        ):
            raise ValueError(
                "Each question must have four non-empty options."
            )

        if (
            isinstance(answer, bool)
            or not isinstance(answer, int)
            or answer not in range(4)
        ):
            raise ValueError("The correct answer index must be 0, 1, 2, or 3.")

    return questions


# ==================================================
# SESSION STATE
# ==================================================
defaults = {
    "mcqs": [],
    "topic": "",
    "difficulty": "Medium",
    "current_q": 0,
    "answers": {},
    "submitted": False,
    "result": None,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ==================================================
# SIDEBAR
# ==================================================
with st.sidebar:

    st.markdown(
        '<div class="brand">Quiz<span>Craft AI</span></div>'
        '<div class="brand-sub">AI-POWERED QUIZ GENERATOR</div>',
        unsafe_allow_html=True,
    )

    st.divider()

    st.markdown("### Quiz settings")
    st.caption("Create a quiz that suits your learning goals.")

    with st.form("settings_form"):

        topic_input = st.text_input(
            "Topic",
            placeholder="e.g. Python programming",
        )

        difficulty_input = st.selectbox(
            "Difficulty",
            ["Easy", "Medium", "Hard"],
            index=1,
        )

        number_input = st.selectbox(
            "Number of questions",
            list(range(5, 16)),
            index=5,
        )

        generate = st.form_submit_button(
            "Generate quiz",
            use_container_width=True,
        )

    st.divider()

    st.markdown("### Suggested topics")
    st.caption("Python · Artificial Intelligence · Science")
    st.caption("History · Geography · General Knowledge")

    st.divider()
    st.caption("Made with care by QuizCraft AI")


# ==================================================
# HERO SECTION
# ==================================================
st.markdown("""
<div class="hero">
    <div class="hero-title">
        Learn smarter with <span>QuizCraft AI.</span>
    </div>
    <div class="hero-subtitle">
        Turn any topic into a personalized quiz.
        Test your knowledge and track your progress.
    </div>
    <div class="hero-badge">
        AI-POWERED LEARNING
    </div>
</div>
""", unsafe_allow_html=True)


# ==================================================
# GENERATE QUIZ
# ==================================================
if generate:

    if not topic_input.strip():
        st.warning("Please enter a topic in the sidebar.")

    else:

        try:

            with st.spinner("Creating your personalized quiz..."):

                questions = generate_mcqs(
                    topic_input.strip(),
                    difficulty_input,
                    number_input,
                )

            # Clear previous radio-widget state
            for key in list(st.session_state.keys()):
                if key.startswith("answer_"):
                    del st.session_state[key]

            st.session_state.mcqs = questions
            st.session_state.topic = topic_input.strip()
            st.session_state.difficulty = difficulty_input
            st.session_state.current_q = 0
            st.session_state.answers = {}
            st.session_state.submitted = False
            st.session_state.result = None

            st.rerun()

        except Exception as error:
            st.error("Unable to generate the quiz.")
            st.caption(f"Technical details: {error}")


# ==================================================
# QUIZ INTERFACE
# ==================================================
if st.session_state.mcqs:

    questions = st.session_state.mcqs
    total = len(questions)
    index = st.session_state.current_q

    st.markdown("## Your quiz")

    info1, info2, info3 = st.columns(3)

    info1.metric("Topic", st.session_state.topic)
    info2.metric("Difficulty", st.session_state.difficulty)
    info3.metric("Total questions", total)

    st.write("")

    if not st.session_state.submitted:

        # Keep the question index within valid bounds
        index = max(0, min(index, total - 1))
        st.session_state.current_q = index

        q = questions[index]

        st.markdown(
            f"""
            <div class="question-card">
                <div class="question-label">
                    QUESTION {index + 1} OF {total}
                </div>
                <div class="question-text">
                    {html.escape(q["question"])}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Show the saved answer when returning to a question
        previous_answer = st.session_state.answers.get(index)

        selected = st.radio(
            "Choose your answer",
            options=q["options"],
            index=(
                q["options"].index(previous_answer)
                if previous_answer in q["options"]
                else None
            ),
            key=f"answer_{index}",
            label_visibility="collapsed",
        )

        if selected is not None:
            st.session_state.answers[index] = selected

        # Question progress
        answered_count = len(st.session_state.answers)

        st.caption(
            f"Progress: {answered_count} of {total} questions answered"
        )

        st.progress(answered_count / total)

        st.write("")

        left, middle, right = st.columns([1, 2, 1])

        with left:

            if index > 0:

                if st.button("Previous"):
                    st.session_state.current_q -= 1
                    st.rerun()

        with right:

            if index < total - 1:

                if st.button("Next question"):
                    st.session_state.current_q += 1
                    st.rerun()

            else:

                if st.button("Submit quiz"):

                    score = sum(
                        st.session_state.answers.get(i)
                        == questions[i]["options"][questions[i]["answer"]]
                        for i in range(total)
                    )

                    st.session_state.result = {
                        "score": score,
                        "total": total,
                        "percentage": score / total * 100,
                    }

                    st.session_state.submitted = True
                    st.rerun()


    # ==================================================
    # RESULTS
    # ==================================================
    if st.session_state.submitted:

        result = st.session_state.result

        score = result["score"]
        percentage = result["percentage"]

        st.divider()
        st.markdown("## Your results")

        col1, col2, col3 = st.columns(3)

        col1.metric("Correct answers", f"{score}/{total}")
        col2.metric("Your score", f"{percentage:.1f}%")
        col3.metric("Incorrect / skipped", total - score)

        st.progress(int(percentage))

        if percentage >= 40:
            st.success("Congratulations! You passed the quiz.")
        else:
            st.warning("Keep practising. You can improve next time.")

        st.divider()
        st.markdown("## Answer review")

        for i, q in enumerate(questions):

            correct = q["options"][q["answer"]]
            user_answer = st.session_state.answers.get(i)

            with st.container(border=True):

                st.markdown(
                    f"**Question {i + 1}: {q['question']}**"
                )

                if user_answer == correct:

                    st.success(f"Correct! Your answer: {user_answer}")

                elif user_answer is None:

                    st.warning("You did not answer this question.")
                    st.info(f"Correct answer: {correct}")

                else:

                    st.error(f"Your answer: {user_answer}")
                    st.info(f"Correct answer: {correct}")

        st.write("")

        if st.button("Create another quiz", use_container_width=True):

            for key in list(st.session_state.keys()):
                if key.startswith("answer_"):
                    del st.session_state[key]

            st.session_state.mcqs = []
            st.session_state.answers = {}
            st.session_state.current_q = 0
            st.session_state.submitted = False
            st.session_state.result = None

            st.rerun()


# ==================================================
# WELCOME SCREEN
# ==================================================
else:

    st.markdown("## Start learning")

    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.markdown("### Create")
            st.write("Generate questions on a topic you choose.")

    with col2:
        with st.container(border=True):
            st.markdown("### Practise")
            st.write("Answer questions at your preferred difficulty.")

    with col3:
        with st.container(border=True):
            st.markdown("### Improve")
            st.write("Check your score and review correct answers.")


# ==================================================
# FOOTER
# ==================================================
st.markdown("""
<div class="footer">
    QuizCraft AI · Learn something new every day
</div>
""", unsafe_allow_html=True)