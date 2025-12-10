import pandas as pd

df = pd.read_csv("enron_mail_20150507.csv", encoding="latin-1")
 
print("Loading Enron dataset...")
enron = pd.read_csv("enron_mail_20150507.csv", encoding="latin-1")

# Rename column
enron = enron.rename(columns={"message": "text"})

# Assign ALL as ham (label = 0)
enron["label"] = 0

# Keep only required columns
enron = enron[["text", "label"]]

# Optional: reduce size for speed (recommended)
enron = enron.sample(15000, random_state=42)

print("Enron rows used:", enron.shape[0])
