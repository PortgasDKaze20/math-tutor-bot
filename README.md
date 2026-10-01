markdown
# Math Tutor Bot 🧮

An AI-powered math tutoring chatbot built for **DDS1343 (Generative AI with LLMs)**. Helps SPM-level (Form 3–5) students practice math through step-by-step explanations and auto-generated practice problems.

**Live demo:** https://math-tutor-bot-ub2nyjplxniv4jgverkewv.streamlit.app

## Features

- **Ask a Question** — students can ask any math question and get a step-by-step explanation instead of just the final answer
- **Non-math redirect** — politely steers off-topic questions back to math
- **Practice Problems** — generates varied SPM-level problems by topic (Algebra, Quadratic Equations, Statistics, Matrices)
- **AI-based answer checking** — accepts mathematically equivalent answers regardless of formatting/wording
- **Score tracking** — tracks correct/total answers across a session
- **Input validation** — rejects empty or too-short submissions before calling the API
- **Error handling** — automatically retries and falls back to a backup model if the AI service is temporarily busy

## Tech Stack

- **Frontend/App:** [Streamlit](https://streamlit.io)
- **AI Model:** Google Gemini (`gemini-3.5-flash-lite` primary, `gemini-3.6-flash` fallback) via the `google-genai` SDK
- **Deployment:** Streamlit Community Cloud
- **Language:** Python

## Running Locally

1. Clone this repo:

git clone https://github.com/PortgasDKaze20/math-tutor-bot.git
cd math-tutor-bot


2. Install dependencies:

pip install -r requirements.txt


3. Create a `.streamlit/secrets.toml` file with your own Gemini API key:

GEMINI_API_KEY = "your_key_here"


4. Run the app:

streamlit run app.py


## Known Limitations

- **No document-retrieval pipeline yet** — the tutor's domain knowledge currently comes from the system prompt and the Gemini model's own training, not from a dedicated SPM syllabus knowledge base. A chunked retrieval layer is a planned next step.
- **Depends on a live internet connection and the Gemini API** — there is no offline mode. If Google's API is down or unreachable, the app falls back between two models and retries, but cannot function with no connection at all.
- **Score tracking is session-only** — practice scores reset if the browser tab is closed or the app is reloaded; there is no persistent login or database storing long-term student progress yet.
- **No fixed question bank or sample dataset** — practice problems are generated live by the Gemini model on each request rather than pulled from a static set of sample questions. This was a deliberate design choice to avoid repetitive, limited practice material, but it also means problem difficulty/correctness depends on the model's output each time rather than pre-verified content.
- **Single-language support** — the tutor currently responds in English only; it does not yet support Bahasa Malaysia, which many of the intended SPM students may prefer.

## Project Context

Built as part of the **AI-Powered Math Exam Practice Assistant** group assignment for DDS1343.