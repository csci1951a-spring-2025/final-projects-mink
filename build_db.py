import os
import sqlite3
import pandas as pd


if __name__ == "__main__":
    conn = sqlite3.connect("./data/data.db")
    c = conn.cursor()

    if not os.path.exists("./data/seda_admindist_long_gcs_5.0_updated_20240319.csv"):
        print("Downloading SEDA data...")
        os.system('curl --output ./data/seda_codebook_admindist_5.0.xlsx "https://stacks.stanford.edu/file/druid:cs829jn7849/seda_codebook_admindist_5.0.xlsx"')
        os.system('curl --output ./data/seda_admindist_long_cs_5.0_updated_20240319.csv   "https://stacks.stanford.edu/file/druid:cs829jn7849/seda_admindist_long_cs_5.0_updated_20240319.csv"')
        os.system('curl --output ./data/seda_admindist_long_gcs_5.0_updated_20240319.csv  "https://stacks.stanford.edu/file/druid:cs829jn7849/seda_admindist_long_gcs_5.0_updated_20240319.csv"')
    if not os.path.exists("./data/grf19_lea_tract.xlsx"):
        print("Downloading NCES geographic mapping data...")
        os.system('curl --output ./data/GRF19.zip "https://nces.ed.gov/programs/edge/data/GRF19.zip"')
        os.system('unzip ./data/GRF19.zip -d ./data')
    if not os.path.exists("./data/health_food_access_all.csv"):
        print("Downloading food access data...")
        os.system('curl -L -o ./data/health_food_access_all.csv "https://drive.google.com/uc?export=download&id=1L0HB_qGJrIUnZ_In7iB1jGNuhlX5rNNZ"')
    if not os.path.exists("./data/cdc_health_data.csv"):
        print("Downloading CDC health data...")
        os.system('curl --output ./data/cdc_health_data.csv "https://data.cdc.gov/api/views/mb5y-ytti/rows.csv?accessType=DOWNLOAD"')

    df = pd.read_csv("./data/health_food_access_all.csv")
    df.to_sql("food", conn, if_exists="replace", index=False)

    df = pd.read_csv("./data/cdc_health_data.csv")
    df = df[["StateAbbr", "CountyName", "TractFIPS", "MHLTH_CrudePrev", "SLEEP_CrudePrev"]]
    df.to_sql("cdc", conn, if_exists="replace", index=False)

    df = pd.read_csv("./data/seda_admindist_long_gcs_5.0_updated_20240319.csv")
    df = df[df.year == 2019]
    df.to_sql("seda", conn, if_exists="replace", index=False)

    df = pd.read_excel("./data/grf19_lea_tract.xlsx")
    df.to_sql("nces", conn, if_exists="replace", index=False)

    conn.commit()
    conn.close()