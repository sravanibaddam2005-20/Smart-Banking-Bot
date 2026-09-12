# Smart Banking Bot — Interview Preparation Guide

---

## 1. PROJECT OVERVIEW

**Project Name:** Smart Banking Bot | AI Chatbot
**Type:** Conversational AI / NLP Web Application
**Domain:** FinTech / Banking

### One-Line Summary (for interviews)
> "I built an AI-powered banking chatbot using Python and Streamlit that classifies user intent using a TF-IDF + Logistic Regression NLP pipeline and responds to banking queries like balance checks, account info, and FAQs — with a PIN-based authentication flow."

### Project Purpose
To simulate a real-world virtual banking assistant that can handle common customer queries 24/7 without human intervention, reducing support costs and improving customer experience.

---

## 2. TECH STACK

| Layer | Technology | Why It Was Chosen |
|-------|-----------|-------------------|
| Language | Python 3.x | Industry standard for ML/AI projects |
| UI Framework | Streamlit | Rapid prototyping of data/AI web apps, no HTML/CSS needed |
| NLP / ML | Scikit-learn | Lightweight, production-ready ML library |
| Vectorizer | TF-IDF (TfidfVectorizer) | Converts text to numerical features efficiently |
| Classifier | Logistic Regression | Fast, interpretable, works well on small NLP datasets |
| Data | Python Dictionaries | Simple mock database for demo purposes |
| State Management | st.session_state | Maintains chat history and user session across reruns |

---

## 3. PROJECT ARCHITECTURE

```
User Input (Streamlit Chat UI)
        │
        ▼
Intent Detection
  ├── Is there a pending_intent + PIN in input?
  │       └── YES → Resume pending intent with PIN
  └── NO → predict_intent(model, user_input)
              │
              ▼
        TF-IDF Vectorizer
        (text → feature vector)
              │
              ▼
        Logistic Regression
        (feature vector → intent label)
              │
              ▼
        Confidence Threshold Check (≥ 0.35)
        ├── BELOW → return "unknown"
        └── ABOVE → return predicted intent
              │
              ▼
        generate_response(intent, user_input, session)
        ├── check_balance / account_info → PIN Auth → Mock DB lookup
        ├── faq_* / greet / goodbye → Static response from RESPONSES dict
        └── unknown → Fallback help message
              │
              ▼
        Streamlit Chat UI (st.chat_message)
```

---

## 4. FILE STRUCTURE

```
project/
├── app.py          — Main app: UI, NLP pipeline, response logic
├── intents.py      — Training data (90 phrases × 9 intents) + response templates
└── requirements.txt — streamlit, scikit-learn, pandas
```

### Why Two Files?
Separating training data (intents.py) from application logic (app.py) follows the **Separation of Concerns** principle. Adding new intents or responses only requires editing intents.py — the ML pipeline and UI remain untouched.

---

## 5. NLP PIPELINE — DEEP DIVE

### What is Intent Classification?
Intent classification is the task of mapping a user's free-text input to a predefined category (intent). For example:
- "What's my balance?" → `check_balance`
- "I lost my card" → `faq_lost_card`

### Step 1 — TF-IDF Vectorization

**TF-IDF = Term Frequency × Inverse Document Frequency**

- **Term Frequency (TF):** How often a word appears in a single training phrase.
- **Inverse Document Frequency (IDF):** How rare that word is across ALL training phrases.
- Words that are unique to specific intents (e.g., "balance", "stolen", "transfer") get HIGH scores.
- Common words like "my", "is", "the" get LOW scores (also removed by stop_words="english").

**Configuration used:**
```python
TfidfVectorizer(
    ngram_range=(1, 2),    # captures single words AND two-word phrases
    lowercase=True,         # normalizes case
    stop_words="english"    # removes filler words
)
```

**ngram_range=(1,2) example:**
- Input: "lost card"
- Unigrams: ["lost", "card"]
- Bigrams: ["lost card"]
- "lost card" as a bigram is a much stronger signal than either word alone.

### Step 2 — Logistic Regression Classifier

- A **multi-class linear classifier** that learns a weight for each TF-IDF feature per intent.
- Uses the **lbfgs solver** (Limited-memory Broyden–Fletcher–Goldfarb–Shanno) — efficient for small-to-medium datasets.
- **C=5.0** is the inverse regularization strength — higher C = less regularization = model fits training data more closely.
- Outputs a **probability distribution** across all 9 intents for every input.

### Step 3 — Confidence Threshold

```python
def predict_intent(model, text, threshold=0.35):
    proba = model.predict_proba([text])[0]
    if proba.max() < threshold:
        return "unknown"
    return model.classes_[proba.argmax()]
```

- Without a threshold, the model always picks the "most likely" intent even for completely unrelated input.
- If max probability < 35%, the bot returns a helpful fallback instead of a wrong answer.
- This is called **rejection/abstention** — important for production chatbots.

### Why Not Deep Learning (BERT, GPT)?
| Aspect | TF-IDF + LR | BERT/GPT |
|--------|------------|----------|
| Training data needed | ~10 phrases/intent | Thousands |
| Training time | Milliseconds | Hours/GPUs |
| Inference speed | Instant | Slower |
| Interpretability | High | Low (black box) |
| Best for | Prototype / small domain | Large-scale production |

For a banking FAQ bot with well-defined intents, TF-IDF + LR is the right tool.

---

## 6. INTENTS DEFINED

| Intent | Example Phrases | Response Type |
|--------|----------------|---------------|
| `check_balance` | "What's my balance?", "How much do I have?" | Dynamic (Mock DB) |
| `account_info` | "Show my account details", "Account type?" | Dynamic (Mock DB) |
| `faq_lost_card` | "I lost my card", "Block my card" | Static |
| `faq_reset_password` | "Forgot my password", "Reset PIN" | Static |
| `faq_working_hours` | "When are you open?", "Branch hours" | Static |
| `faq_transfer` | "How do I transfer money?", "Wire transfer" | Static |
| `faq_new_account` | "Open a bank account", "Account requirements" | Static |
| `greet` | "Hello", "Hi", "Good morning" | Static |
| `goodbye` | "Bye", "Exit", "I'm done" | Static |

**Total training phrases:** 90 (10 per intent)

---

## 7. AUTHENTICATION FLOW

The bot implements a simple **multi-turn conversation flow** for secure intents:

```
User: "What's my balance?"
  → Intent: check_balance
  → No PIN in session → Store pending_intent = "check_balance"
  → Bot: "Please enter your 4-digit PIN"

User: "1234"
  → extract_pin("1234") → "1234"
  → pending_intent exists → intent = "check_balance"
  → PIN "1234" found in MOCK_ACCOUNTS
  → Store pin in session_state
  → Return balance for Alex Johnson

User: "Show my account info"  (same session)
  → Intent: account_info
  → PIN already in session → Skip PIN prompt
  → Return account info directly
```

**Key functions:**
- `extract_pin(text)` — uses regex `\b(\d{4})\b` to find a 4-digit number
- `session.get("pin")` — checks if user is already authenticated
- `session["pending_intent"]` — stores what the user wanted before PIN entry

---

## 8. STREAMLIT SESSION STATE

Streamlit reruns the entire script on every user interaction. `st.session_state` is a persistent dictionary that survives reruns.

**Keys used:**
| Key | Type | Purpose |
|-----|------|---------|
| `messages` | List of dicts | Full chat history [{role, content}] |
| `model` | sklearn Pipeline | Trained ML model (trained once, reused) |
| `pin` | String | Authenticated user's PIN |
| `pending_intent` | String | Intent waiting for PIN confirmation |

**Why store the model in session_state?**
Without it, the model would retrain on every message sent — wasting CPU. Storing it means it trains once per browser session.

---

## 9. MOCK DATABASE

```python
MOCK_ACCOUNTS = {
    "1234": {
        "name": "Alex Johnson",
        "account_number": "****-****-****-4521",
        "account_type": "Premium Savings",
        "balance": 12_450.75,
        "interest_rate": "3.5% p.a.",
        "status": "Active",
    },
    ...
}
```

- Keyed by PIN for O(1) lookup.
- Account numbers are masked (only last 4 digits shown) — simulating real PII handling.
- In a real system, this would be replaced by a database query (PostgreSQL, DynamoDB, etc.) after proper authentication (JWT, OAuth2).

---

## 10. POTENTIAL INTERVIEW QUESTIONS & ANSWERS

### Q1: What is TF-IDF and why did you use it?
**A:** TF-IDF stands for Term Frequency–Inverse Document Frequency. It converts text into numerical vectors by weighting words based on how important they are to a specific document relative to the entire corpus. I used it because it's fast, requires no pre-training, and works well for small, domain-specific datasets like banking FAQs. Words like "balance" or "transfer" that are unique to specific intents get high weights, making classification accurate.

### Q2: Why Logistic Regression over Naive Bayes or SVM?
**A:** Logistic Regression outputs calibrated probabilities, which I needed for the confidence threshold check. Naive Bayes assumes feature independence (not always true for text), and SVM doesn't natively output probabilities without Platt scaling. LR is also fast to train, easy to interpret, and performs well on linearly separable text classification tasks.

### Q3: How does the confidence threshold work?
**A:** After prediction, I call `predict_proba()` which returns a probability for each intent. If the highest probability is below 0.35 (35%), I return "unknown" instead of the predicted intent. This prevents the bot from confidently giving a wrong answer when the user asks something outside its training domain.

### Q4: How would you scale this to production?
**A:** Several improvements for production:
1. Replace mock DB with a real database (PostgreSQL/DynamoDB) with proper ORM
2. Replace PIN auth with JWT tokens / OAuth2
3. Replace TF-IDF+LR with a fine-tuned BERT model or use an LLM API (like Amazon Bedrock) for better generalization
4. Add logging and monitoring (AWS CloudWatch)
5. Deploy on AWS (ECS/EKS for containers, or AWS App Runner for simplicity)
6. Add rate limiting and input sanitization for security
7. Use Redis for session management instead of in-memory state

### Q5: What are the limitations of your current approach?
**A:**
- **Small training set:** Only 10 phrases per intent — real bots need hundreds.
- **No context memory:** The bot doesn't remember previous turns (except PIN state).
- **No entity extraction:** Can't extract amounts, dates, or account numbers from natural language.
- **No spelling correction:** Typos can reduce classification accuracy.
- **Static responses:** FAQ answers are hardcoded, not fetched from a live knowledge base.

### Q6: How does Streamlit handle state between messages?
**A:** Streamlit reruns the entire Python script on every user interaction. `st.session_state` is a special dictionary that persists across these reruns within a browser session. I store the chat history, trained model, and authentication state there so they survive each rerun without being reset.

### Q7: What is a scikit-learn Pipeline and why use it?
**A:** A Pipeline chains multiple processing steps (vectorizer → classifier) into a single object. Benefits: (1) prevents data leakage during cross-validation, (2) makes the code cleaner, (3) allows saving/loading the entire pipeline as one object with joblib, and (4) ensures the same preprocessing is applied consistently during training and inference.

### Q8: How would you add a new intent?
**A:** Three steps:
1. Add training phrases to `TRAINING_DATA` in intents.py: `("phrase", "new_intent")`
2. Add a response to `RESPONSES` dict in intents.py
3. If it needs dynamic data, add a handler block in `generate_response()` in app.py
No changes to the ML pipeline code needed — it automatically picks up new intents.

### Q9: How did you handle the multi-turn PIN authentication?
**A:** When a user asks for balance/account info without a PIN, I store the original intent in `session_state["pending_intent"]`. On the next message, I check if there's a pending intent AND a 4-digit number in the input. If both are true, I skip the NLP classifier and directly use the pending intent with the extracted PIN. This creates a natural two-turn conversation flow.

### Q10: What security concerns exist in this prototype?
**A:**
- PINs are stored in plain text in session state (should be hashed in production)
- No rate limiting — vulnerable to brute force PIN attacks
- No HTTPS enforcement
- Mock data is hardcoded (no real encryption)
- No input sanitization against injection attacks
In production, I'd use bcrypt for PIN hashing, implement account lockout after failed attempts, and use HTTPS with proper session tokens.

---

## 11. KEY METRICS TO MENTION

- **9 intents** supported
- **90 training phrases** (10 per intent)
- **3 files**, ~250 lines of code total
- **Sub-second** model training time
- **0.35** confidence threshold for fallback
- **3 demo users** in mock database
- **2-turn** authentication flow for secure intents

---

## 12. HOW TO DEMO THE PROJECT

**Start the app:**
```bash
cd project
venv\Scripts\activate
streamlit run app.py
```

**Demo script for interviewers:**
1. Open `http://localhost:8501`
2. Type: `"Hello"` → Shows welcome message with capabilities
3. Type: `"What's my balance?"` → Bot asks for PIN
4. Type: `"1234"` → Shows Alex Johnson's balance ($12,450.75)
5. Type: `"Show my account info"` → Shows full account details (no PIN re-prompt)
6. Type: `"I lost my card"` → Shows card blocking instructions
7. Type: `"What are your working hours?"` → Shows branch hours table
8. Type: `"How do I transfer money?"` → Shows transfer guide
9. Type: `"xyz random gibberish"` → Shows fallback message (threshold working)
10. Click `"Clear Chat"` in sidebar → Resets session

---

## 13. POSSIBLE ENHANCEMENTS (Show Initiative)

| Enhancement | Technology |
|-------------|-----------|
| Replace TF-IDF with sentence embeddings | sentence-transformers |
| Add LLM for open-ended questions | Amazon Bedrock (Claude/Titan) |
| Real database integration | SQLAlchemy + PostgreSQL |
| Proper authentication | JWT + bcrypt |
| Voice input support | SpeechRecognition library |
| Multi-language support | googletrans / AWS Translate |
| Deploy to cloud | AWS App Runner / ECS |
| Analytics dashboard | Streamlit + Plotly |
| Spelling correction | pyspellchecker |
| Conversation memory | LangChain ConversationBufferMemory |
