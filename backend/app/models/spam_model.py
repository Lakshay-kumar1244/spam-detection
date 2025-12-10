# backend/app/models/spam_model.py

import os
import joblib
import re

# ---------------- PATH ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "spam_model.pkl")

# ---------------- LOAD MODEL ----------------
# spam_model.pkl MUST be saved as: joblib.dump((model, vectorizer), ...)
model, vectorizer = joblib.load(MODEL_PATH)

# ---------------- CONFIG ----------------
SPAM_PROB_THRESHOLD = 0.45  # balanced threshold

SPAM_KEYWORDS = [
    # rewards / winnings
    "congrat", "winner", "won cash", "you won", "claim prize",
    "claim reward", "unclaimed", "reward waiting", "lucky draw",

    # urgency / pressure
    "urgent", "act now", "limited time", "final notice",
    "last chance", "offer expires", "response required",

    # clicks / links
    "click now", "click here", "tap here", "open link",
    "visit link", "verify here",

    # money scams
    "free money", "cash bonus", "instant cash", "quick cash",
    "easy money", "get rich", "investment opportunity",

    # banking & credentials
    "bank account", "verify account", "update kyc",
    "suspended account", "login immediately", "confirm details",
    "password", "pin number", "atm blocked",

    # delivery & fake alerts
    "package pending", "delivery failed", "courier on hold",
    "reschedule delivery", "customs charge",

    # government / authority scams
    "income tax refund", "tax refund", "government benefit",
    "subsidy approved",

    # crypto & financial scams
    "bitcoin", "crypto reward", "wallet suspended",
    "investment guaranteed", "high returns",

    # lottery / vouchers
    "lottery", "jackpot", "voucher winner", "gift card",
    "gift voucher",

    # emotional manipulation
    "risk free", "guaranteed", "100% safe", "no cost",
    "hurry up", "exclusive deal"
]

URL_PATTERN = re.compile(r"https?://|www\.|bit\.ly|tinyurl", re.I)

# ---------------- PREDICTION ----------------
def predict_spam(text: str) -> dict:
    if not text or not text.strip():
        return {"label": "safe", "confidence": 0.0}

    text_lower = text.lower()

    # ---- 1. Heuristic detection (short scam texts) ----
    keyword_hits = sum(1 for k in SPAM_KEYWORDS if k in text_lower)
    has_url = bool(URL_PATTERN.search(text_lower))

    if keyword_hits >= 2 or (keyword_hits >= 1 and has_url):
        return {
            "label": "spam",
            "confidence": 0.95
        }

    # ---- 2. ML probability ----
    X = vectorizer.transform([text])
    proba = model.predict_proba(X)[0]

    classes = list(model.classes_)
    spam_index = classes.index(1) if 1 in classes else classes.index("spam")
    spam_prob = float(proba[spam_index])

    if spam_prob >= SPAM_PROB_THRESHOLD:
        return {
            "label": "spam",
            "confidence": round(spam_prob, 2)
        }

    return {
        "label": "safe",
        "confidence": round(1 - spam_prob, 2)
    }

# ---------------- DEBUG ----------------
if __name__ == "__main__":
    samples = [
        "Congratulations! You won cash click now",
        "Urgent! Claim your prize now http://bit.ly/win",
        "Burger King: Get 20% off this weekend",
        "Your OTP is 482913"
    ]

    for s in samples:
        print(s, "=>", predict_spam(s))
