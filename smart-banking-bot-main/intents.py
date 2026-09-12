# intents.py — Training phrases and response templates for each intent

# Each entry: (training_phrase, intent_label)
TRAINING_DATA = [
    # check_balance
    ("what is my balance", "check_balance"),
    ("show me my balance", "check_balance"),
    ("how much money do i have", "check_balance"),
    ("check my account balance", "check_balance"),
    ("what's in my account", "check_balance"),
    ("show me my money", "check_balance"),
    ("current balance", "check_balance"),
    ("account balance please", "check_balance"),
    ("how much is in my account", "check_balance"),
    ("tell me my balance", "check_balance"),

    # account_info
    ("tell me about my account", "account_info"),
    ("what type of account do i have", "account_info"),
    ("account details", "account_info"),
    ("what is my account number", "account_info"),
    ("account information", "account_info"),
    ("show my account info", "account_info"),
    ("what is the interest rate on my account", "account_info"),
    ("account status", "account_info"),
    ("is my account active", "account_info"),
    ("account type", "account_info"),

    # faq_lost_card
    ("i lost my card", "faq_lost_card"),
    ("my card is lost", "faq_lost_card"),
    ("block my card", "faq_lost_card"),
    ("stolen card", "faq_lost_card"),
    ("how do i block a lost card", "faq_lost_card"),
    ("card stolen what do i do", "faq_lost_card"),
    ("freeze my card", "faq_lost_card"),
    ("deactivate my card", "faq_lost_card"),
    ("i cant find my card", "faq_lost_card"),
    ("report lost card", "faq_lost_card"),

    # faq_reset_password
    ("reset my password", "faq_reset_password"),
    ("forgot my password", "faq_reset_password"),
    ("how do i reset my password", "faq_reset_password"),
    ("change my password", "faq_reset_password"),
    ("i forgot my pin", "faq_reset_password"),
    ("password reset", "faq_reset_password"),
    ("how to change password", "faq_reset_password"),
    ("cant login forgot password", "faq_reset_password"),
    ("reset pin", "faq_reset_password"),
    ("update my password", "faq_reset_password"),

    # faq_working_hours
    ("what are your working hours", "faq_working_hours"),
    ("when are you open", "faq_working_hours"),
    ("bank opening hours", "faq_working_hours"),
    ("what time do you close", "faq_working_hours"),
    ("are you open on weekends", "faq_working_hours"),
    ("branch hours", "faq_working_hours"),
    ("when does the bank open", "faq_working_hours"),
    ("office hours", "faq_working_hours"),
    ("what time does the bank close", "faq_working_hours"),
    ("working hours please", "faq_working_hours"),

    # faq_transfer
    ("how do i transfer money", "faq_transfer"),
    ("send money to another account", "faq_transfer"),
    ("wire transfer", "faq_transfer"),
    ("how to make a transfer", "faq_transfer"),
    ("transfer funds", "faq_transfer"),
    ("move money between accounts", "faq_transfer"),
    ("how do i send money", "faq_transfer"),
    ("bank transfer steps", "faq_transfer"),
    ("online transfer", "faq_transfer"),
    ("how to transfer funds", "faq_transfer"),

    # faq_new_account
    ("how do i open a new account", "faq_new_account"),
    ("open a bank account", "faq_new_account"),
    ("create a new account", "faq_new_account"),
    ("what do i need to open an account", "faq_new_account"),
    ("account opening requirements", "faq_new_account"),
    ("how to apply for an account", "faq_new_account"),
    ("new account application", "faq_new_account"),
    ("sign up for an account", "faq_new_account"),
    ("register a new account", "faq_new_account"),
    ("open savings account", "faq_new_account"),

    # greet
    ("hello", "greet"),
    ("hi", "greet"),
    ("hey", "greet"),
    ("good morning", "greet"),
    ("good afternoon", "greet"),
    ("howdy", "greet"),
    ("hi there", "greet"),
    ("hey bot", "greet"),
    ("hello bank", "greet"),
    ("greetings", "greet"),

    # goodbye
    ("bye", "goodbye"),
    ("goodbye", "goodbye"),
    ("see you later", "goodbye"),
    ("thanks bye", "goodbye"),
    ("exit", "goodbye"),
    ("quit", "goodbye"),
    ("that's all", "goodbye"),
    ("i'm done", "goodbye"),
    ("thank you goodbye", "goodbye"),
    ("close chat", "goodbye"),
]

# Static responses for each intent
RESPONSES = {
    "check_balance": None,  # Handled dynamically from mock DB

    "account_info": None,  # Handled dynamically from mock DB

    "faq_lost_card": (
        "🚨 **Lost or Stolen Card?** Here's what to do immediately:\n\n"
        "1. **Call us** at 📞 1-800-BANK-HELP (available 24/7)\n"
        "2. **Online:** Log in → *Cards* → *Block Card*\n"
        "3. **Mobile App:** Tap *Card Controls* → *Freeze Card*\n\n"
        "Your card will be blocked instantly. A replacement card will arrive in **3–5 business days**."
    ),

    "faq_reset_password": (
        "🔐 **Reset Your Password / PIN:**\n\n"
        "1. Go to our website and click **'Forgot Password'**\n"
        "2. Enter your registered **email address**\n"
        "3. Check your email for a **reset link** (valid for 15 minutes)\n"
        "4. Follow the link to set a new password\n\n"
        "For PIN reset, visit any branch with a valid **government-issued ID**."
    ),

    "faq_working_hours": (
        "🕐 **Branch Working Hours:**\n\n"
        "| Day | Hours |\n"
        "|-----|-------|\n"
        "| Monday – Friday | 9:00 AM – 5:00 PM |\n"
        "| Saturday | 10:00 AM – 2:00 PM |\n"
        "| Sunday & Public Holidays | Closed |\n\n"
        "📱 Our **mobile app & online banking** are available **24/7**."
    ),

    "faq_transfer": (
        "💸 **How to Transfer Money:**\n\n"
        "**Online Banking:**\n"
        "1. Log in → *Payments* → *Transfer Funds*\n"
        "2. Enter recipient's account number & bank code\n"
        "3. Enter amount and confirm with your OTP\n\n"
        "**Limits:** Up to **$10,000/day** online | Up to **$50,000/day** at branch\n\n"
        "Transfers are processed within **1–2 business days**."
    ),

    "faq_new_account": (
        "🏦 **Opening a New Account:**\n\n"
        "**Requirements:**\n"
        "- Valid government-issued **photo ID** (passport, driver's license)\n"
        "- **Proof of address** (utility bill, bank statement — within 3 months)\n"
        "- **Initial deposit:** Minimum $100 for Savings | $500 for Checking\n\n"
        "**Apply online** at our website or visit any branch. "
        "Online applications take **5–10 minutes** to complete."
    ),

    "greet": (
        "👋 **Welcome to SmartBank!** I'm your AI banking assistant.\n\n"
        "I can help you with:\n"
        "- 💰 Check your account balance\n"
        "- 📋 View account information\n"
        "- 🚨 Report a lost/stolen card\n"
        "- 🔐 Reset your password\n"
        "- 💸 Transfer money guidance\n"
        "- 🏦 Open a new account\n\n"
        "How can I assist you today?"
    ),

    "goodbye": (
        "👋 **Thank you for banking with SmartBank!**\n\n"
        "Have a wonderful day. Stay safe! 😊\n\n"
        "*For urgent matters, call us 24/7 at 📞 1-800-BANK-HELP*"
    ),
}
