import os
import time
import sqlite3
import utils as u
import numpy as np
import pandas as pd
import multiprocessing
import xgboost as xgb
import seaborn as sns
import matplotlib.pyplot as plt

from tqdm import tqdm
from itertools import product

from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.utils.class_weight import compute_sample_weight
from sklearn.metrics import (
    balanced_accuracy_score,
    accuracy_score,
    precision_score,
    recall_score, 
    f1_score,
    precision_recall_curve,
)


n_jobs = multiprocessing.cpu_count() - 1
print(f"Using {n_jobs} CPU cores")

# %%
if not os.path.exists("./data/data.db"):
    os.system("python3.11 build_db.py")

conn = sqlite3.connect("./data/data.db")
c = conn.cursor()


COLS_EXCLUDE = set([
    "StateAbbr",
    "StateDesc",
    "CountyName",
    "CountyFIPS",
    "TractFIPS",
    "fips",
    "stateabb",
    "sedaadmin",
    "sedaadminname",
    "TRACT",
    "COUNT"
])

if not os.path.exists("./data/full_joined_table.csv"):
    c.execute(f"""
    WITH seda_tracts AS (
        SELECT *
        FROM seda s
        JOIN nces n
        ON s.sedaadmin = n.LEAID
        WHERE s.year = 2019
    )

    , food_atlas_tracts AS (
        SELECT *
        FROM food f
        JOIN seda_tracts st
        ON st.TRACT = f.CensusTract
    )

    , cdc_tracts AS (
        SELECT *
        FROM cdc c
        JOIN food_atlas_tracts ft
        ON ft.TRACT = c.TractFIPS
    )

    SELECT *
    FROM cdc_tracts;
    """)

    rows = c.fetchall()
    print(len(rows))
    columns = [col[0] for col in c.description]

    ## Write the rows manually into a CSV file without pandas
    to_remove = [
        "StateAbbr",
        "CountyName",
        "TractFIPS",
        "stateabb",
        "MHLTH_CrudePrev:1",
        "SLEEP_CrudePrev:1",
        "fips",
        "LEAID",
        "NAME_LEA19",
        "TRACT",
        "COUNT"
    ]
    to_remove_idx = set([i for i, col in enumerate(columns) if col in to_remove])
    with open("data/full_joined_table.csv", "w") as f:
        race_cols = []
        f.write(",".join([col for i, col in enumerate(columns) if i not in to_remove_idx]) + "\n")
        for row in tqdm(rows):
            # if row[0] == "CA":
            f.write(",".join([str(x) for i, x in enumerate(row) if i not in to_remove_idx]) + "\n")


df = pd.read_csv("data/full_joined_table.csv")
print(df.shape)
df.head()

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
print(f"Original length: {len(race_df)}")
race_df = race_df.dropna().reset_index(drop=True)
race_df["y"] = race_df.apply(lambda row: str(row["Urban"]) + str(row["LATracts_half"]), axis=1)
print(f"Length after dropping NaNs: {len(race_df)}")
race_df.head()

uncorrelated_features, correlated_features = u.de_correlate(race_df[feature_cols])
race_df_no_corr_mth = race_df[race_df.subject == "mth"].drop(correlated_features, axis=1)
race_df_no_corr_rla = race_df[race_df.subject == "rla"].drop(correlated_features, axis=1)
print(f"Math df length: {len(race_df_no_corr_mth)}")
print(f"Reading/Language Arts df length: {len(race_df_no_corr_rla)}")

param_grid = {
    "learning_rate": [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1],
    "n_estimators": [100_000],
    "max_depth": [32, 64, 128],
    "subsample": [1.0],
    "colsample_bytree": [1.0],
    "gamma": [0.0],
}

param_combinations = list(product(
    param_grid["learning_rate"],
    param_grid["n_estimators"],
    param_grid["max_depth"],
    param_grid["subsample"],
    param_grid["colsample_bytree"],
    param_grid["gamma"],
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
    num_classes = one_hot.categories_[0].shape[0]

    X_train, X_val_test, y_train, y_val_test = train_test_split(X, df.y, test_size=0.4, stratify=df.y, random_state=42)
    X_val, X_test, y_val, y_test = train_test_split(X_val_test, y_val_test, test_size=0.5, stratify=y_val_test, random_state=42)

    # print(f"Train: {y_train.value_counts(normalize=True)}")
    # print(f"Val: {y_val.value_counts(normalize=True)}")
    # print(f"Test: {y_test.value_counts(normalize=True)}")
    label_counts = y_train.value_counts()
    print(f"Baseline accuracy: {label_counts.max() / label_counts.sum():.4f}")

    param_results = {}
    for lr, n_estimators, max_depth, subsample, colsample, gamma in param_combinations:
        start = time.time()
        skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        cv_scores = []
        for train_idx, val_idx in skf.split(X_train, y_train, groups=y_train):
            X_cv_train, X_cv_val = X_train.iloc[train_idx].copy(), X_train.iloc[val_idx].copy()
            y_cv_train, y_cv_val = y_train.iloc[train_idx].copy(), y_train.iloc[val_idx].copy()

            y_cv_train = one_hot.transform(y_cv_train.values.reshape(-1, 1))
            y_cv_val = one_hot.transform(y_cv_val.values.reshape(-1, 1))
            train_weights = compute_sample_weight(class_weight="balanced", y=y_cv_train)
            val_weights = compute_sample_weight(class_weight="balanced", y=y_cv_val)
            y_cv_train = y_cv_train.argmax(axis=1)
            y_cv_val = y_cv_val.argmax(axis=1)

            scaler = StandardScaler()
            X_cv_train = scaler.fit_transform(X_cv_train)
            X_cv_val = scaler.transform(X_cv_val)

            dtrain = xgb.DMatrix(X_cv_train, label=y_cv_train, weight=train_weights)
            dval = xgb.DMatrix(X_cv_val, label=y_cv_val, weight=val_weights)

            params = {
                "objective": "multi:softmax",
                "num_class": num_classes,
                "learning_rate": lr,
                "max_depth": max_depth,
                "subsample": subsample,
                "colsample_bytree": colsample,
                "gamma": gamma,
                "use_rmm": True,
                "verbosity": 0,
                "seed": 42,
                "n_jobs": n_jobs,
            }

            booster = xgb.train(
                params,
                dtrain,
                num_boost_round=n_estimators,
                evals=[(dval, "val")],
                early_stopping_rounds=10_000,
                verbose_eval=False,
            )

            preds = booster.predict(dval)
            cv_scores.append(accuracy_score(y_cv_val, preds))

        print(
            f"[{lr}|{n_estimators}|{max_depth}|{subsample}|{colsample}|{gamma}]\tVal accuracy: "
            f"{np.mean(cv_scores):.4f} +/- {np.std(cv_scores):.4f}\t({(time.time()-start):.4f} seconds)"
        )
        param_results[(lr, n_estimators, max_depth)] = np.mean(cv_scores)

    best_param = max(param_results, key=param_results.get)
    print(f"Best params: {best_param}")
    best_params[name] = best_param

    y_train = one_hot.transform(y_train.values.reshape(-1, 1))
    y_val = one_hot.transform(y_val.values.reshape(-1, 1))
    y_test = one_hot.transform(y_test.values.reshape(-1, 1))
    train_weights = compute_sample_weight(class_weight="balanced", y=y_train)
    val_weights = compute_sample_weight(class_weight="balanced", y=y_val)
    test_weights = compute_sample_weight(class_weight="balanced", y=y_test)
    y_train = y_train.argmax(axis=1)
    y_val = y_val.argmax(axis=1)
    y_test = y_test.argmax(axis=1)

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_val = scaler.transform(X_val)
    X_test = scaler.transform(X_test)

    dtrain = xgb.DMatrix(X_train, label=y_train, weight=train_weights)
    dval = xgb.DMatrix(X_val, label=y_val, weight=val_weights)
    dtest = xgb.DMatrix(X_test, label=y_test, weight=test_weights)

    params = {
        "objective": "multi:softmax",
        "num_class": num_classes,
        "use_rmm": True,
        "learning_rate": best_params[0],
        "max_depth": best_params[2],
        "subsample": best_params[3],
        "colsample_bytree": best_params[4],
        "gamma": best_params[5],
        "seed": 42,
        "verbosity": 0,
        "n_jobs": n_jobs,
    }

    booster = xgb.train(
        params,
        dtrain,
        num_boost_round=best_param[1],
        evals=[(dval, "val")],
        early_stopping_rounds=10_000,
        verbose_eval=False,
    )

    train_preds = booster.predict(dtrain)
    val_preds = booster.predict(dval)
    test_preds = booster.predict(dtest)
    print(f"Train accuracy: {accuracy_score(y_train, train_preds):.4f}")
    print(f"Val accuracy: {accuracy_score(y_val, val_preds):.4f}")
    print(f"Test accuracy: {accuracy_score(y_test, test_preds):.4f}")

    print(f"Train balanced accuracy: {balanced_accuracy_score(y_train, train_preds):.4f}")
    print(f"Val balanced accuracy: {balanced_accuracy_score(y_val, val_preds):.4f}")
    print(f"Test balanced accuracy: {balanced_accuracy_score(y_test, test_preds):.4f}")

    print(f"Train precision: {precision_score(y_train, train_preds, average='weighted'):.4f}")
    print(f"Val precision: {precision_score(y_val, val_preds, average='weighted'):.4f}")
    print(f"Test precision: {precision_score(y_test, test_preds, average='weighted'):.4f}")

    print(f"Train recall: {recall_score(y_train, train_preds, average='weighted'):.4f}")
    print(f"Val recall: {recall_score(y_val, val_preds, average='weighted'):.4f}")
    print(f"Test recall: {recall_score(y_test, test_preds, average='weighted'):.4f}")

    print(f"Train f1: {f1_score(y_train, train_preds, average='weighted'):.4f}")
    print(f"Val f1: {f1_score(y_val, val_preds, average='weighted'):.4f}")
    print(f"Test f1: {f1_score(y_test, test_preds, average='weighted'):.4f}")

    importance = booster.get_score(importance_type="weight")
    importance_df = pd.DataFrame(importance.items(), columns=["feature", "importance"])
    importance_df["feature"] = importance_df["feature"].apply(lambda x: uncorrelated_features[int(x[1:])])
    importance_df = importance_df.sort_values(by="importance", ascending=False)
    plt.figure(figsize=(10, 6))
    sns.barplot(x="importance", y="feature", data=importance_df.head(20))
    plt.title(f"Feature Importance - {name}")
    plt.tight_layout()
    plt.show()


print(best_params)



# %%



