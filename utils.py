import pandas as pd

def de_correlate(df):
    corr_to_remove = set()
    columns = set(df.columns)
    corr = True
    while corr:
        highly_corr_counts = {}
        corr_map = df[list(columns)].corr()
        for col1 in corr_map.columns:
            for col2 in corr_map.index:
                if col1 != col2 and corr_map[col1][col2] > 0.95:
                    if col1 not in highly_corr_counts:
                        highly_corr_counts[col1] = 1
                    else:
                        highly_corr_counts[col1] += 1
                    if col2 not in highly_corr_counts:
                        highly_corr_counts[col2] = 1
                    else:
                        highly_corr_counts[col2] += 1
        if len(highly_corr_counts) > 1:
            highly_corr_counts = {k: v for k, v in sorted(highly_corr_counts.items(), key=lambda item: item[1], reverse=True)}
            col_to_remove = list(highly_corr_counts.keys())[0]
            corr_to_remove.add(col_to_remove)
            columns.remove(col_to_remove)
        else:
            corr = False
    return (list(columns), list(corr_to_remove))
