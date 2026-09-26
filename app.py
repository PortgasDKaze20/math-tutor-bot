import streamlit as st
import time
import random
from google import genai
from google.genai import types

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

SYSTEM_PROMPT = """You are a friendly, patient math tutor for Malaysian secondary school students (Form 3-5, SPM level).
Rules:
- Explain concepts step by step, never just give the final answer straight away.
- Use simple, clear language, and give a worked example when helpful.
- If the student's question is not related to math, politely redirect them back to math topics.
- Keep answers concise and focused on helping them understand, not overwhelming them."""

MODELS_TO_TRY = ["gemini-3.5-flash-lite", "gemini-3.6-flash"]

def ask_gemini(prompt_text, system=SYSTEM_PROMPT, temperature=0.7):
    for model_name in MODELS_TO_TRY:
        for attempt in range(2):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt_text,
                    config=types.GenerateContentConfig(
                        system_instruction=system,
                        temperature=temperature
                    )
                )
                return response.text
            except Exception as e:
                print("ERROR DETAILS:", repr(e))
                time.sleep(2)
    return None

def check_answer(correct_answer, student_answer):
    prompt = f"Correct answer: {correct_answer}\nStudent's answer: {student_answer}\n\nAre these mathematically equivalent (ignoring formatting, order, wording like 'and' vs comma)? Reply with EXACTLY one word: YES or NO."
    result = ask_gemini(prompt, system="You are a strict math answer checker. Reply with only YES or NO.", temperature=0.1)
    if result:
        return result.strip().upper().startswith("YES")
    return student_answer.strip().lower() == correct_answer.strip().lower()

if "score_correct" not in st.session_state:
    st.session_state["score_correct"] = 0
if "score_total" not in st.session_state:
    st.session_state["score_total"] = 0
if "seen_problems" not in st.session_state:
    st.session_state["seen_problems"] = []

st.title("Math Tutor Bot")

tab1, tab2 = st.tabs(["Ask a Question", "Practice Problems"])

with tab1:
    question = st.text_input("Ask a math question:")
    if question:
        cleaned = question.strip()
        if len(cleaned) == 0:
            st.warning("Please type a question before submitting.")
        elif len(cleaned) < 3:
            st.warning("That looks too short to be a real question. Try adding more detail.")
        else:
            with st.spinner("Thinking..."):
                result = ask_gemini(cleaned)
                if result:
                    st.write(result)
                else:
                    st.error("The AI is currently busy. Please try again in a moment.")

with tab2:
    st.write(f"**Score: {st.session_state['score_correct']} / {st.session_state['score_total']}**")

    topic = st.selectbox("Choose a topic:", ["Algebra", "Quadratic Equations", "Statistics", "Matrices"])

    if st.button("Generate a practice problem"):
        with st.spinner("Generating..."):
            difficulty = random.choice(["easy", "medium", "slightly challenging"])
            seed_hint = random.randint(1000, 9999)
            avoid_text = ""
            if st.session_state["seen_problems"]:
                recent = st.session_state["seen_problems"][-3:]
                avoid_text = "Do NOT repeat these previous problems:\n" + "\n".join(recent)

            prompt = f"Give me ONE {difficulty} {topic} practice problem suitable for SPM level (variation seed: {seed_hint}). Use different numbers/context than typical textbook examples. {avoid_text}\nFormat your reply EXACTLY like this, nothing else:\nPROBLEM: <the problem>\nANSWER: <the final numeric or short answer>"
            result = ask_gemini(prompt, system="You are a math problem generator. Follow the format exactly. Always vary the numbers and context.", temperature=1.0)
            if result and "PROBLEM:" in result and "ANSWER:" in result:
                problem_part = result.split("ANSWER:")[0].replace("PROBLEM:", "").strip()
                answer_part = result.split("ANSWER:")[1].strip()
                st.session_state["current_problem"] = problem_part
                st.session_state["current_answer"] = answer_part
                st.session_state["answered"] = False
                st.session_state["seen_problems"].append(problem_part)
            else:
                st.error("Couldn't generate a problem right now. Try again.")

    if "current_problem" in st.session_state:
        st.write("**Problem:**", st.session_state["current_problem"])
        student_answer = st.text_input("Your answer:", key="student_answer")

        if st.button("Submit Answer"):
            if student_answer.strip() == "":
                st.warning("Type an answer first.")
            elif not st.session_state.get("answered", False):
                correct_answer = st.session_state["current_answer"]
                with st.spinner("Checking..."):
                    is_correct = check_answer(correct_answer, student_answer)
                st.session_state["score_total"] += 1
                if is_correct:
                    st.session_state["score_correct"] += 1
                    st.success(f"Correct! The answer is {correct_answer}.")
                else:
                    st.error(f"Not quite. The correct answer is {correct_answer}.")
                st.session_state["answered"] = True
