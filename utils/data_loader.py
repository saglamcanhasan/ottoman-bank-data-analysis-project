from os.path import join
import pandas as pd

# load datasets
employee_dataset = pd.read_excel(join("datasets", "employees.xlsx"))
agency_dataset = pd.read_excel(join("datasets", "agencies.xlsx"))