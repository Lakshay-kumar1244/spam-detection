import pandas as pd
import re
import nltk
import joblib

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, precision_score

# --------------------------
# Setup
# --------------------------
ps = PorterStemmer()
stop_words = set(stopwords.words("english"))

def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    words = nltk.word_tokenize(text)
    words = [
        ps.stem(w)
        for w in words
        if w.isalnum() and w not in stop_words
    ]
    return " ".join(words)

# --------------------------
# Load SMS dataset
# --------------------------
print("Loading SMS dataset...")
sms = pd.read_csv("sms_spam.csv", encoding="latin-1")
sms = sms[["v1", "v2"]]
sms.columns = ["label", "text"]
sms["label"] = sms["label"].map({"spam": 1, "ham": 0})

# --------------------------
# Load Enron dataset
# --------------------------
print("Loading Enron dataset...")
print("Loading Enron dataset...")
enron = pd.read_csv("enron_mail_20150507.csv", encoding="latin-1")

# rename column
enron = enron.rename(columns={"message": "text"})

# label ALL Enron emails as ham (0)
enron["label"] = 0

# keep only needed columns
enron = enron[["text", "label"]]

# reduce size so training is fast (recommended)
enron = enron.sample(n=15000, random_state=42)

print("Enron rows used:", enron.shape[0])

enron.columns = ["text", "label"]

# --------------------------
# Combine datasets
# --------------------------
df = pd.concat([sms, enron], ignore_index=True)
df.dropna(inplace=True)

df["clean_text"] = df["text"].apply(clean_text)

X = df["clean_text"]
y = df["label"]

# --------------------------
# Vectorization
# --------------------------
vectorizer = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2)
)

X_vec = vectorizer.fit_transform(X)

# --------------------------
# Train model
# --------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X_vec, y, test_size=0.2, random_state=42
)

model = MultinomialNB()
model.fit(X_train, y_train)

# --------------------------
# Evaluation
# --------------------------
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred))

# --------------------------
# Save model (SINGLE FILE ✅)
# --------------------------
joblib.dump((model, vectorizer), "spam_model.pkl")


print("✅ Model trained and saved as spam_model.pkl")
