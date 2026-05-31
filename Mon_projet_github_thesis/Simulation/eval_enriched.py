import joblib, pandas as pd, numpy as np, time
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, classification_report
from sklearn.preprocessing import LabelEncoder

model = joblib.load('xgboost_edgeiiot.pkl')
df = pd.read_csv('simulation_enriched.csv')
X = df.drop(columns=['label']).values
y_true_str = df['label'].values

le = LabelEncoder()
le.classes_ = np.array(['Backdoor', 'DDoS', 'Intrusion', 'MITM', 'Normal', 'Reconnaissance'])
y_true_enc = le.transform(y_true_str)

start = time.time()
y_pred = model.predict(X)
inference_time_ms = (time.time() - start) / len(y_pred) * 1000
y_proba_full = model.predict_proba(X)

present_labels = np.unique(y_true_enc)
mask = np.isin(le.transform(le.classes_), present_labels)
y_proba_present = y_proba_full[:, mask]
y_proba_present = y_proba_present / y_proba_present.sum(axis=1, keepdims=True)

acc = accuracy_score(y_true_enc, y_pred)
f1 = f1_score(y_true_enc, y_pred, average='weighted')
auc = roc_auc_score(y_true_enc, y_proba_present, multi_class='ovr', average='weighted')

print(" Enriched Simulation Results")
print(f"Accuracy  : {acc:.4f}")
print(f"F1-score  : {f1:.4f}")
print(f"AUC       : {auc:.4f}")
print(f"Inference : {inference_time_ms:.4f} ms/sample")
print(classification_report(y_true_enc, y_pred, labels=present_labels, target_names=le.classes_[present_labels]))