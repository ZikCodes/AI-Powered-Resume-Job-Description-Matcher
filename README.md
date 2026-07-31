# 📄 AI Resume & Job Description Matcher

An AI-driven resume optimization dashboard built with **Streamlit** and Python. The application evaluates candidate resumes against target job descriptions in real time, calculating match scores, identifying missing keywords, and providing actionable feedback to help beat ATS (Applicant Tracking Systems).


---

## ✨ Features

- **📊 Instant Compatibility Metrics:** Calculates overall match percentage, Matched skills count, and Missing skills count.
- **🎯 Keyword Gap Analysis:** Automatically pinpoints matched keywords and highlights critical missing terms.
- **💡 Tailored Recommendations:** Generates clear, actionable bullet points to optimize resume content for specific roles.

---

## 🛠️ Tech Stack

- **Frontend & App Framework:** [Streamlit](https://streamlit.io/)
- **Language:** Python 3.9+
- **AI Integration:** Open Router Free Models
- **Text Processing:** `PyMuPDF` (for PDF parsing)

---

## 🚀 Quick Start

### 1. Create virtual environment
- **python -m venv venv**
- **source venv/bin/activate** # On Mac
- **venv\Scripts\activate**  # On Windows
- **pip install -r requirements.txt**


### 2. Clone the repository


git clone [https://github.com/ZikCodes/AI-Powered-Resume-Job-Description-Matcher.git](https://github.com/ZikCodes/AI-Powered-Resume-Job-Description-Matcher.git)
cd resume analyzer


### 3. Create virtual environment
- Create a .env file in the root directory (or use Streamlit Secrets .streamlit/secrets.toml):

- API_KEY="your_api_key_here"

### 4. Run the App
- Run the Streamlit App
streamlit run main.py