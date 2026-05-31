import joblib
import pandas as pd
import numpy as np
import time


from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, classification_report
from sklearn.preprocessing import LabelEncoder


# Charger le modèle XGBoost sauvegardé

model = joblib.load('xgboost_edgeiiot.pkl')

# Charger le dataset simulé

df = pd.read_csv('simulation_dataset.csv')

# Séparer features et labels

X_sim = df.drop(columns=['label']).values
y_true = df['label'].values

# Encodage des labels 

le = LabelEncoder()
le.classes_ = np.array(['Backdoor', 'DDoS', 'Intrusion', 'MITM', 'Normal', 'Information gathering'])
y_true_enc = le.transform(y_true)

# Prédictions et mesure du temps d'inférence

start = time.time()
y_pred = model.predict(X_sim)
total_time = time.time() - start
inference_time_ms = (total_time / len(y_pred)) * 1000

y_proba = model.predict_proba(X_sim)


# Métriques

acc = accuracy_score(y_true_enc, y_pred)
f1 = f1_score(y_true_enc, y_pred, average='weighted')
auc = roc_auc_score(y_true_enc, y_proba, multi_class='ovr', average='weighted')

print(f" Resultats sur les donnees simulees ")
print(f"Accuracy  : {acc:.4f}")
print(f"F1-score  : {f1:.4f}")
print(f"AUC       : {auc:.4f}")
print(f"Inference : {inference_time_ms:.4f} ms/sample")
print("\nRapport de classification :\n", classification_report(y_true_enc, y_pred, target_names=le.classes_))