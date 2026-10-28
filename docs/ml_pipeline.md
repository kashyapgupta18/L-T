# Machine Learning Pipeline Design

## Leakage Prevention Principles
To guarantee operational validity:
1. Current shift downtime and defects are excluded from training inputs.
2. Predictive features rely strictly on pre-shift indicators:
   - Cumulative machine wear index
   - Elapsed days since last maintenance overhaul
   - Historical downtime rolling statistics
3. Models evaluate using ROC-AUC and Brier calibration score.
