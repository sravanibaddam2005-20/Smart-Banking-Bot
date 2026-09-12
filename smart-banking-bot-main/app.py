# app.py — Smart Banking Bot | AI Chatbot
# Stack: Streamlit + Scikit-learn (TF-IDF + Logistic Regression) + Pandas

import re
import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from intents import TRAINING_DATA, RESPONSES

# ─────────────────────────────────────────────
# 1. MOCK DATABASE
# ─────────────────────────────────────────────

# Simulated user accounts — keyed by a 4-digit PIN for demo authentication
MOCK_ACCOUNTS = {
    "1234": {
        "name": "Alex Johnson",
        "account_number": "****-****-****-4521",
        "account_type": "Premium Savings",
        "balance": 12_450.75,
        "interest_rate": "3.5% p.a.",
        "status": "Active",
    },
    "5678": {
        "name": "Maria Garcia",
        "account_number": "****-****-****-8832",
        "account_type": "Checking",
        "balance": 3_210.00,
        "interest_rate": "1.2% p.a.",
        "status": "Active",
    },
    "9999": {
        "name": "Demo User",
        "account_number": "****-****-****-0001",
        "account_type": "Basic Savings",
        "balance": 500.00,
        "interest_rate": "2.0% p.a.",
        "status": "Active",
    },
}

# ─────────────────────────────────────────────
# 2. NLP PIPELINE — TF-IDF + Logistic Regression
# ─────────────────────────────────────────────

def build_and_train_model():
    """
    Builds a scikit-learn Pipeline:
      - TfidfVectorizer: converts raw text into TF-IDF feature vectors.
        TF-IDF (Term Frequency–Inverse Document Frequency) weights words
        by how often they appear in a phrase vs. how common they are across
        all training phrases — making distinctive words more influential.
      - LogisticRegression: a fast, interpretable multi-class classifier
        that learns decision boundaries between intent categories.
    The pipeline is trained on (phrase, intent) pairs from intents.py.
    """
    phrases, labels = zip(*TRAINING_DATA)

    model = Pipeline([
        ("tfidf", TfidfVectorizer(
            ngram_range=(1, 2),   # unigrams + bigrams capture short phrases
            lowercase=True,
            stop_words="english", # remove filler words like "the", "is", "do"
        )),
        ("clf", LogisticRegression(
            max_iter=1000,
            C=5.0,                # regularization strength
            solver="lbfgs",
        )),
    ])

    model.fit(phrases, labels)
    return model


def predict_intent(model, text: str, threshold: float = 0.35) -> str:
    """
    Predicts the intent of a user message.
    Returns 'unknown' if the top class probability is below the threshold,
    preventing overconfident predictions on out-of-scope inputs.
    """
    proba = model.predict_proba([text])[0]
    max_proba = proba.max()
    if max_proba < threshold:
        return "unknown"
    return model.classes_[proba.argmax()]


# ─────────────────────────────────────────────
# 3. RESPONSE LOGIC
# ─────────────────────────────────────────────

def extract_pin(text: str):
    """Extracts a 4-digit PIN from user input using regex."""
    match = re.search(r"\b(\d{4})\b", text)
    return match.group(1) if match else None


def generate_response(intent: str, user_input: str, session: dict) -> str:
    """
    Routes the predicted intent to the correct response.
    For account-specific intents (balance, account_info), it checks
    whether the user is authenticated via their PIN in session state.
    """

    # ── Account-specific intents require PIN authentication ──
    if intent in ("check_balance", "account_info"):
        pin = session.get("pin") or extract_pin(user_input)

        if not pin:
            session["pending_intent"] = intent
            return (
                "🔒 To access your account details, please enter your **4-digit PIN**.\n\n"
                "*(Demo PINs: `1234`, `5678`, `9999`)*"
            )

        if pin not in MOCK_ACCOUNTS:
            session.pop("pin", None)
            session.pop("pending_intent", None)
            return "❌ **Invalid PIN.** Please try again with a valid 4-digit PIN."

        # PIN is valid — store in session and serve the request
        session["pin"] = pin
        session.pop("pending_intent", None)
        account = MOCK_ACCOUNTS[pin]

        if intent == "check_balance":
            return (
                f"💰 **Account Balance for {account['name']}**\n\n"
                f"| Field | Details |\n"
                f"|-------|---------|\n"
                f"| Account | `{account['account_number']}` |\n"
                f"| Available Balance | **${account['balance']:,.2f}** |\n"
                f"| Account Type | {account['account_type']} |\n"
                f"| Status | ✅ {account['status']} |"
            )

        if intent == "account_info":
            return (
                f"📋 **Account Information for {account['name']}**\n\n"
                f"| Field | Details |\n"
                f"|-------|---------|\n"
                f"| Account Number | `{account['account_number']}` |\n"
                f"| Account Type | {account['account_type']} |\n"
                f"| Interest Rate | {account['interest_rate']} |\n"
                f"| Balance | **${account['balance']:,.2f}** |\n"
                f"| Status | ✅ {account['status']} |"
            )

    # ── Static FAQ / greeting / goodbye responses ──
    if intent in RESPONSES and RESPONSES[intent]:
        return RESPONSES[intent]

    # ── Fallback for unrecognized input ──
    return (
        "🤔 I'm not sure I understood that. I can help you with:\n\n"
        "- 💰 **Balance** — *'What's my balance?'*\n"
        "- 📋 **Account Info** — *'Show my account details'*\n"
        "- 🚨 **Lost Card** — *'I lost my card'*\n"
        "- 🔐 **Password Reset** — *'Reset my password'*\n"
        "- 🕐 **Working Hours** — *'When are you open?'*\n"
        "- 💸 **Transfers** — *'How do I transfer money?'*"
    )


# ─────────────────────────────────────────────
# 4. STREAMLIT UI
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="SmartBank AI Chatbot",
    page_icon="🏦",
    layout="centered",
)

# ── Sidebar ──
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/bank-building.png", width=80)
    st.title("SmartBank")
    st.caption("AI-Powered Banking Assistant")
    st.divider()
    st.markdown("**🔧 Demo PINs**")
    st.code("1234 — Alex Johnson\n5678 — Maria Garcia\n9999 — Demo User")
    st.divider()
    st.markdown("**💡 Try asking:**")
    st.markdown(
        "- *What's my balance?*\n"
        "- *Show my account info*\n"
        "- *I lost my card*\n"
        "- *Reset my password*\n"
        "- *What are your hours?*\n"
        "- *How do I transfer money?*"
    )
    st.divider()
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pop("pin", None)
        st.session_state.pop("pending_intent", None)
        st.rerun()

# ── Page Header ──
st.title("🏦 SmartBank AI Chatbot")
st.caption("Your intelligent banking assistant — available 24/7")
st.divider()

# ── Session State Initialization ──
if "messages" not in st.session_state:
    st.session_state.messages = []

# Train the model once and cache it in session state
if "model" not in st.session_state:
    st.session_state.model = build_and_train_model()

# Show welcome message on first load
if not st.session_state.messages:
    welcome = RESPONSES["greet"]
    st.session_state.messages.append({"role": "assistant", "content": welcome})

# ── Render Chat History ──
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🏦" if msg["role"] == "assistant" else "👤"):
        st.markdown(msg["content"])

# ── Chat Input ──
if user_input := st.chat_input("Type your message here..."):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)

    # Determine intent — check if we're waiting for a PIN first
    pending = st.session_state.get("pending_intent")
    pin_in_input = extract_pin(user_input)

    if pending and pin_in_input:
        # User replied with a PIN to satisfy a pending intent
        intent = pending
    else:
        intent = predict_intent(st.session_state.model, user_input)

    # Generate and display bot response
    response = generate_response(intent, user_input, st.session_state)

    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant", avatar="🏦"):
        st.markdown(response)
