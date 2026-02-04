import pandas as pd
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "diet-data.csv")

df = pd.read_csv(DATA_PATH)

print("Dataset loaded successfully")
print("Columns:", list(df.columns))

# -------------------------------------------------
# SELECT REQUIRED COLUMNS
# -------------------------------------------------
required_columns = [
    "Age",
    "Gender",
    "Height_cm",
    "Weight_kg",
    "BMI",
    "Exercise_Frequency",
    "Sleep_Hours",
    "Recommended_Meal_Plan"
]

missing = [col for col in required_columns if col not in df.columns]
if missing:
    raise ValueError(f"Missing columns in dataset: {missing}")

# Keep only required columns
df = df[required_columns]

# -------------------------------------------------
# HANDLE MISSING VALUES
# -------------------------------------------------
df = df.dropna()

# -------------------------------------------------
# ENCODE GENDER
# -------------------------------------------------
gender_encoder = LabelEncoder()
df["Gender"] = gender_encoder.fit_transform(df["Gender"])

# -------------------------------------------------
# FEATURES & TARGET
# -------------------------------------------------
X = df[
    [
        "Age",
        "Gender",
        "Height_cm",
        "Weight_kg",
        "BMI",
        "Exercise_Frequency",
        "Sleep_Hours",
    ]
]

y = df["Recommended_Meal_Plan"]

# -------------------------------------------------
# TRAIN-TEST SPLIT
# -------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -------------------------------------------------
# TRAIN MODEL
# -------------------------------------------------
model = RandomForestClassifier(
    n_estimators=150,
    random_state=42
)

model.fit(X_train, y_train)

# -------------------------------------------------
# MODEL ACCURACY
# -------------------------------------------------
accuracy = model.score(X_test, y_test)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# -------------------------------------------------
# SAVE MODEL & ENCODER
# -------------------------------------------------
MODEL_DIR = os.path.dirname(__file__)

with open(os.path.join(MODEL_DIR, "diet_model.pkl"), "wb") as f:
    pickle.dump(model, f)

with open(os.path.join(MODEL_DIR, "gender_encoder.pkl"), "wb") as f:
    pickle.dump(gender_encoder, f)

print("Model and encoder saved successfully")
