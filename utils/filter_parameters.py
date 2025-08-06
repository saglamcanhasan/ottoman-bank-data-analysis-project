import pandas as pd
import numpy as np
from utils.data_loader import employee_dataset, agency_dataset

# time period bounds
start = 1855
end = 1926

# dropdown values
agencies = np.unique(agency_dataset["City"].dropna())
grouped_functions = np.unique(employee_dataset["Grouped_Functions"].dropna())
religions = np.unique(employee_dataset["merged_religion"].dropna())
ids = np.unique(employee_dataset["employee_code"].dropna())