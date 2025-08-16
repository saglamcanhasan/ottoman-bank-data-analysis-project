import pandas as pd
from os.path import join

# load datasets
employee_df = pd.read_csv(join("datasets", "employees_preprocessed.csv"))
agency_df = pd.read_csv(join("datasets", "agencies_preprocessed.csv"))
connection_df = pd.read_csv(join("datasets", "connection_preprocessed.csv"))
transfer_df = pd.read_csv(join("datasets", "transfer_preprocessed.csv"))