"""Benchmark multiple classifier architectures on synthetic failure datasets."""
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

def get_candidate_classifiers():
    return {
        "GradientBoosting": GradientBoostingClassifier(n_estimators=100, max_depth=3, random_state=42),
        "RandomForest": RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42),
        "LogisticRegression": LogisticRegression(max_iter=1000, random_state=42)
    }
