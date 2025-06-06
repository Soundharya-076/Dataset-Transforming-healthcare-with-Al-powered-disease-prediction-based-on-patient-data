# -*- coding: utf-8 -*-
"""Untitled15.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1tHeBvLcA5RJtCe0qFp-r3OBJTH5gUoj6
"""



import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
df = pd.read_csv("/healthcare_dataset.csv")
df.head()
df["Date of Admission"] = pd.to_datetime(df["Date of Admission"], errors='coerce')
df["Discharge Date"] = pd.to_datetime(df["Discharge Date"], errors='coerce')
df["Admission Month"] = df["Date of Admission"].dt.month
df["Admission Weekday"] = df["Date of Admission"].dt.weekday
df["Length of Stay"] = (df["Discharge Date"] - df["Date of Admission"]).dt.days
df.drop(columns=[
    "Name", "Doctor", "Hospital", "Room Number",
    "Date of Admission", "Discharge Date"
], inplace=True)
df.fillna(0, inplace=True)
label_encoders = {}
categorical_cols = df.select_dtypes(include=["object"]).columns.tolist()
categorical_cols.remove("Medical Condition")
for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le
target_le = LabelEncoder()
df["Medical Condition"] = target_le.fit_transform(df["Medical Condition"])
X = df.drop(columns=["Medical Condition"])
y = df["Medical Condition"]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)
model = GradientBoostingClassifier(random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred, target_names=target_le.classes_)
conf_matrix = confusion_matrix(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")
print("\nClassification Report:\n", report)
print("\nConfusion Matrix:\n", conf_matrix)
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))
sns.countplot(data=df, x="Medical Condition", order=df["Medical Condition"].value_counts().index)
plt.title("Distribution of Medical Conditions")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
plt.figure(figsize=(10, 6))
sns.countplot(data=df, x="Gender", hue="Medical Condition")
plt.title("Gender vs. Medical Condition")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()
plt.figure(figsize=(12, 6))
sns.boxplot(data=df, x="Medical Condition", y="Length of Stay")
plt.title("Length of Stay by Medical Condition")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
df_numeric = df.select_dtypes(include=["int64", "float64"])
plt.figure(figsize=(10, 8))
sns.heatmap(df_numeric.corr(), annot=True, cmap="coolwarm")
plt.title("Correlation Matrix")
plt.tight_layout()
plt.show()



