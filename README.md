# 🏦 Smart Banking Bot | AI Chatbot

An AI-powered banking assistant built with Python and Streamlit that classifies user intent using a **TF-IDF + Logistic Regression** NLP pipeline and responds to common banking queries in a modern chat interface.

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-red?logo=streamlit)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.4+-orange?logo=scikit-learn)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📸 Preview

> Chat UI built with `st.chat_message` — clean, responsive, and stateful.

| Feature | Demo Input |
|---------|-----------|
| Balance Check | *"What's my balance?"* |
| Account Info | *"Show my account details"* |
| Lost Card | *"I lost my card"* |
| Password Reset | *"Reset my password"* |
| Working Hours | *"When are you open?"* |
| Money Transfer | *"How do I transfer money?"* |

---

## 🚀 Features

- 💬 **Modern Chat UI** — built with Streamlit's `st.chat_message` and `st.chat_input`
- 🧠 **NLP Intent Classification** — TF-IDF vectorization + Logistic Regression (9 intents, 90 training phrases)
- 🔒 **PIN Authentication Flow** — multi-turn conversation to securely access account data
- 📋 **Mock Banking Database** — 3 demo user accounts with balance, account type, and interest rate
- 🤔 **Confidence Threshold** — returns a helpful fallback instead of a wrong answer for unknown inputs
- 💾 **Session State** — full chat history and authentication persist across interactions

---

## 🗂️ Project Structure

```
smart-banking-bot/
├── app.py                            # Main app: Streamlit UI + NLP pipeline + response logic
├── intents.py                        # Training data (90 phrases × 9 intents) + response templates
├── requirements.txt                  # Python dependencies
├── INTERVIEW_PREP.md                 # Deep-dive interview preparation guide
└── SmartBankingBot_Interview_Prep.docx  # Interview guide as Word document
```

---

## 🧠 How It Works

```
User Input
    │
    ▼
TF-IDF Vectorizer  →  Logistic Regression  →  Confidence Check (≥ 0.35)
    │
    ▼
generate_response(intent)
    ├── check_balance / account_info  →  PIN Auth  →  Mock DB lookup
    ├── faq_* / greet / goodbye       →  Static response
    └── unknown                       →  Fallback help message
```

### Intents Supported

| Intent | Example |
|--------|---------|
| `check_balance` | "What's my balance?" |
| `account_info` | "Show my account details" |
| `faq_lost_card` | "I lost my card" |
| `faq_reset_password` | "Forgot my password" |
| `faq_working_hours` | "When are you open?" |
| `faq_transfer` | "How do I transfer money?" |
| `faq_new_account` | "Open a bank account" |
| `greet` | "Hello" |
| `goodbye` | "Bye" |

---

## ⚙️ Getting Started

### Prerequisites
- Python 3.8+ installed
- Git installed

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Yashwanth26122005/smart-banking-bot.git
cd smart-banking-bot

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

Open your browser at **http://localhost:8501**

---

## 🔑 Demo PINs

| PIN | User | Account Type | Balance |
|-----|------|-------------|---------|
| `1234` | Alex Johnson | Premium Savings | $12,450.75 |
| `5678` | Maria Garcia | Checking | $3,210.00 |
| `9999` | Demo User | Basic Savings | $500.00 |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.x |
| UI Framework | Streamlit |
| ML / NLP | Scikit-learn |
| Vectorizer | TF-IDF (`TfidfVectorizer`) |
| Classifier | Logistic Regression |
| State Management | `st.session_state` |
| Data | Python Dictionaries |

---

## 📈 Possible Enhancements

- [ ] Replace TF-IDF with sentence embeddings (`sentence-transformers`)
- [ ] Integrate an LLM via Amazon Bedrock (Claude / Titan)
- [ ] Connect to a real database (PostgreSQL / DynamoDB)
- [ ] Add proper authentication (JWT + bcrypt)
- [ ] Deploy to AWS App Runner / ECS
- [ ] Add voice input support
- [ ] Multi-language support via AWS Translate

---

## 📄 License

This project is licensed under the MIT License.
