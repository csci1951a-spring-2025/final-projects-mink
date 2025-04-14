import time
import cupy as cp
import utils as u
import numpy as np
import pandas as pd
import xgboost as xgb

from itertools import product

from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.utils.class_weight import compute_sample_weight
from sklearn.metrics import precision_recall_curve, roc_auc_score, average_precision_score
from sklearn.metrics import balanced_accuracy_score, accuracy_score, precision_score, recall_score, f1_score


df = pd.read_csv("data/full_joined_table.csv")
meta_data_cols = [
    "CensusTract",
    "State",
    "County",
    "sedaadmin",
    "sedaadminname",
    "subject",
    "grade"
]

health_feature_cols = [
    "MHLTH_CrudePrev", # cont
    "SLEEP_CrudePrev", # cont
]

food_desert_cols = [
    "Urban",            # bool
    "LATracts_half",    # bool
    "LATracts10",       # bool
    "PovertyRate",      # cont
    "LowIncomeTracts",  # bool
    "lahunvhalfshare",  # bool
    "lahunv10share",    # bool
]

academics_all_cols = [
    "gcs_mn_all", "gcs_mn_se_all", "tot_asmt_all",
    "gcs_mn_asn", "gcs_mn_se_asn", "tot_asmt_asn",
    "gcs_mn_blk", "gcs_mn_se_blk", "tot_asmt_blk",
    "gcs_mn_ecd", "gcs_mn_se_ecd", "tot_asmt_ecd",
    "gcs_mn_fem", "gcs_mn_se_fem", "tot_asmt_fem",
    "gcs_mn_hsp", "gcs_mn_se_hsp", "tot_asmt_hsp",
    "gcs_mn_mal", "gcs_mn_se_mal", "tot_asmt_mal",
    "gcs_mn_mfg", "gcs_mn_se_mfg", "tot_asmt_mfg",
    "gcs_mn_nam", "gcs_mn_se_nam", "tot_asmt_nam",
    "gcs_mn_nec", "gcs_mn_se_nec", "tot_asmt_nec",
    "gcs_mn_neg", "gcs_mn_se_neg", "tot_asmt_neg",
    "gcs_mn_wag", "gcs_mn_se_wag", "tot_asmt_wag",
    "gcs_mn_wbg", "gcs_mn_se_wbg", "tot_asmt_wbg",
    "gcs_mn_whg", "gcs_mn_se_whg", "tot_asmt_whg",
    "gcs_mn_wht", "gcs_mn_se_wht", "tot_asmt_wht",
    "gcs_mn_wng", "gcs_mn_se_wng", "tot_asmt_wng",
]

academics_race_cols = [
    "gcs_mn_all", "gcs_mn_se_all", "tot_asmt_all",
    "gcs_mn_wht", "gcs_mn_se_wht", "tot_asmt_wht",
    "gcs_mn_asn", "gcs_mn_se_asn", "tot_asmt_asn",
    "gcs_mn_blk", "gcs_mn_se_blk", "tot_asmt_blk",
    "gcs_mn_hsp", "gcs_mn_se_hsp", "tot_asmt_hsp",
    "gcs_mn_nam", "gcs_mn_se_nam", "tot_asmt_nam",
]

academics_gender_cols = [
    # "gcs_mn_all", "gcs_mn_se_all", "tot_asmt_all",
    "gcs_mn_fem", "gcs_mn_se_fem", "tot_asmt_fem",
    "gcs_mn_mal", "gcs_mn_se_mal", "tot_asmt_mal",
]

feature_cols = academics_all_cols + health_feature_cols
race_df = df[academics_all_cols + health_feature_cols + food_desert_cols[:-1] + meta_data_cols].copy()

race_df = race_df.dropna().reset_index(drop=True)
race_df["y"] = race_df.apply(lambda row: str(row["Urban"]) + str(row["LATracts_half"]), axis=1)
uncorrelated_features, correlated_features = u.de_correlate(race_df[feature_cols])

race_df_no_corr_mth = race_df[race_df.subject == "mth"].drop(correlated_features, axis=1)
race_df_no_corr_rla = race_df[race_df.subject == "rla"].drop(correlated_features, axis=1)
print(f"Math df length: {len(race_df_no_corr_mth)}")
print(f"Reading/Language Arts df length: {len(race_df_no_corr_rla)}")
param_grid = {
    "learning_rate": [0.5, 0.01],
    "n_estimators": [100, 250, 500],
    "max_depth": [16, 32, 64],
}

param_combinations = list(product(
    param_grid["learning_rate"],
    param_grid["n_estimators"],
    param_grid["max_depth"]
))

datasets = [("Math", race_df_no_corr_mth), ("RLA", race_df_no_corr_rla)]
best_params = {
    "Math": {},
    "RLA": {}
}
for dataset in datasets:
    name, df = dataset
    print(f"Dataset: {name}")

    X = df[uncorrelated_features]

    one_hot = OneHotEncoder(sparse_output=False)
    one_hot.fit(df.y.values.reshape(-1, 1))

    X_train, X_test, y_train, y_test = train_test_split(X, df.y, test_size=0.2, random_state=42)
    label_counts = y_test.value_counts()
    print(f"Baseline accuracy: {label_counts.max() / label_counts.sum():.4f}")

    param_results = {}
    for lr, n_estimators, max_depth in param_combinations:
        start = time.time()
        skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        cv_scores = []
        for train_idx, val_idx in skf.split(X_train, y_train):
            X_cv_train, X_cv_val = X_train.iloc[train_idx], X_train.iloc[val_idx]
            y_cv_train, y_cv_val = y_train.iloc[train_idx], y_train.iloc[val_idx]

            y_cv_train = one_hot.transform(y_cv_train.values.reshape(-1, 1))
            y_cv_val = one_hot.transform(y_cv_val.values.reshape(-1, 1))
            weights = compute_sample_weight(class_weight="balanced", y=y_cv_train)
            y_cv_train = y_cv_train.argmax(axis=1)
            y_cv_val = y_cv_val.argmax(axis=1)

            scaler = StandardScaler()
            X_cv_train = scaler.fit_transform(X_cv_train)
            X_cv_val = scaler.transform(X_cv_val)
            model = xgb.XGBClassifier(
                objective="multi:softmax",
                num_class=3,
                learning_rate=lr,
                n_estimators=n_estimators,
                max_depth=max_depth,
                random_state=42,
                device="cuda"
            )

            model.fit(cp.array(X_cv_train), cp.array(y_cv_train), sample_weight=cp.array(weights))
            model.set_params(device="cpu")
            cv_scores.append(model.score(X_cv_val, y_cv_val))

        print(
            f"[{lr}|{n_estimators}|{max_depth}] Val accuracy: "
            f"{np.mean(cv_scores):.4f} +/- {np.std(cv_scores):.4f}\t({(time.time()-start):.4f} seconds)"
        )
        param_results[(lr, n_estimators, max_depth)] = np.mean(cv_scores)

    best_params[name] = max(param_results, key=param_results.get)

print(best_params)




