from glob import glob
import pandas as pd
from pandas import DataFrame
from pathlib import Path
from typing import List
from joblib import Parallel, delayed
from time import time
from joblib import parallel_backend

def get_one_csv_data(j: int, path: Path):
    print(j, path)
    return pd.read_csv(path)


if __name__ == "__main__":

    num_jobs = 20

    paths: List[Path] = [Path(path) for path in glob("*.csv")]
    
    paths = [path for path in paths if "detail" not in str(path)]
    paths = paths[:60] # test: only paths of five csvs

    print(f"{len(paths)}, {paths[:3]}")

    ti = time()

    with parallel_backend('threading'):
        dfs: List[DataFrame] = Parallel(n_jobs=num_jobs)(delayed(get_one_csv_data)(j, path) for j, path in enumerate(paths))
        # for df in dfs:
            # print(df)
    df_all: DataFrame = pd.concat(dfs)
    print(df_all.shape, [dfs[j].shape for j in range(len(dfs))])

    print(f"INFO: total number of rows= {len(df_all)}")
    print(f"INFO: total elapsed time={(time() - ti) / 60.} (minutes)")
    print(df_all.head(3))

