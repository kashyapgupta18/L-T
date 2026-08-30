"""Model performance evaluation metrics calculation."""
from typing import Dict
from sklearn.metrics import roc_auc_score, f1_score, precision_score, recall_score, brier_score_loss

def evaluate_classification_metrics(y_true, y_prob, threshold: float = 0.35) -> Dict[str, float]:
    y_pred = (y_prob >= threshold).astype(int)
    return {
        "roc_auc": round(float(roc_auc_score(y_true, y_prob)), 4),
        "f1": round(float(f1_score(y_true, y_pred, zero_division=0)), 4),
        "precision": round(float(precision_score(y_true, y_pred, zero_division=0)), 4),
        "recall": round(float(recall_score(y_true, y_pred, zero_division=0)), 4),
        "brier_score": round(float(brier_score_loss(y_true, y_prob)), 4)
    }
