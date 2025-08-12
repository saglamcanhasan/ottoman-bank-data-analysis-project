import numpy as np
import pandas as pd
from os.path import join

# load datasets
employee_df = pd.read_excel(join("datasets", "employees_preprocessed.xlsx"))
agency_df = pd.read_excel(join("datasets", "agencies_preprocessed.xlsx"))
agency_geo_df = pd.read_excel(join("datasets", "agencies_geo_preprocessed.xlsx"))