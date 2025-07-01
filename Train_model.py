     import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from feature_extractor import extract_features_from_url

# Load your labeled data
df =pd.read_csv('C:/Users/hp/OneDrive/Desktop/project1/dataset.csv')

df.columns = ['url', 'label']
df = df.dropna(subset=['url'])
df['url'] = df['url'].astype(str)
df['label'] = df['label'].apply(lambda x: 1 if str(x).lower() in ['phishing', '1'] else 0)

# Extract features
features = df['url'].apply(extract_features_from_url)
X = pd.DataFrame(features.tolist())
y = df['label']

# Save feature columns for later consistency
with open('features_order.pkl', 'wb') as f:
    pickle.dump(X.columns.tolist(), f)

# Train the model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save the model
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("✅ Model trained and saved.")

