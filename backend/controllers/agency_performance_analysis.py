import pandas as pd
from utils.filter import filter
from services.data_loader import employee_df
import numpy as np

def generate_agency_performance_df(selected_countries=None, selected_cities=None, selected_districts= None,selected_functions=None,
                                 selected_religions=None, selected_time_period: list = [1855, 1925], end_inclusive: bool=False):
    df = employee_df.copy()
    time_period_start_year, time_period_end_year = selected_time_period
    df = filter(df, True, selected_countries, selected_cities, selected_districts, selected_functions, selected_religions, None, time_period_start_year, time_period_end_year)
    
    employee_records = list()
    for _, record in df.iterrows():
        start = max(record["Career Start Year"], time_period_start_year)
        end = min(record["Career End Year"], time_period_end_year)

        for year in range(int(start), int(end)+1):
            employee_records.append({"Agency": record["Agency"], "Year": year, "ID": record["ID"], "Tenure": record["Tenure"],
                "District": record.get("District"),"City": record.get("City"),"Country": record.get("Country")})
    df = pd.DataFrame(employee_records, columns=["Agency", "Year", "Tenure", "ID", "District", "City", "Country"]).drop_duplicates(subset=["Agency", "Year", "ID"])
    
    def choose_agency(row):
        for v in (row.get("District"), row.get("City"), row.get("Country")):
            if isinstance(v, str):
                if v.strip().lower() != "unknown":
                    return v
            elif v is not None and not pd.isna(v):
                return v
        return "Unknown"


    df["Agency"] = df.apply(choose_agency, axis=1)
    
    return df


def generate_agency_empcountdf(selected_countries=None, selected_cities=None, selected_districts= None,selected_functions=None,
                                 selected_religions=None, selected_time_period: list = [1855, 1925], end_inclusive: bool=False):
    
    df = generate_agency_performance_df(selected_countries, selected_cities, selected_districts ,selected_functions,
                                 selected_religions, selected_time_period, end_inclusive)
    if df.empty:
        return pd.DataFrame()
    
    employee_counts_df = df.groupby(["Agency", "Year"])["ID"].count().reset_index(name="Employee Count")
    stats_df = employee_counts_df.groupby("Agency")["Employee Count"].agg(["mean", "min", "max"]).reset_index()
    stats_df.rename(columns={"mean": "Average Employee Count", "min": "Min Employee Count", "max": "Max Employee Count"}, inplace=True)
    
    unique_df = df.groupby("Agency")["ID"].nunique().reset_index(name="Unique Employee Count")
    out = stats_df.merge(unique_df, on="Agency", how="left")
    out = out[out["Agency"] != "Unknown"]
    return out
    
   
async def top_agencies(selected_countries=None, selected_cities=None, selected_districts= None,selected_functions=None,
                                 selected_religions=None, selected_time_period: list = [1855, 1925], end_inclusive: bool=False):
    df = generate_agency_empcountdf(selected_countries, selected_cities, selected_districts,selected_functions,
                                 selected_religions, selected_time_period, end_inclusive)
    
    if not df.empty:
        df = df.sort_values(by='Unique Employee Count', ascending=False).head(10)
    return df
   
   
async def employee_tenure(selected_countries=None, selected_cities=None, selected_districts= None,selected_functions=None,
                                 selected_religions=None, selected_time_period: list = [1855, 1925], end_inclusive: bool=False):
    
    df = generate_agency_performance_df(selected_countries, selected_cities, selected_districts,selected_functions,
                                 selected_religions, selected_time_period, end_inclusive)
   
    if df.empty:
        return pd.DataFrame()

    emp_tenure_df = df.groupby(['ID', 'Agency'])['Tenure'].mean().reset_index()
    emp_tenure_df = emp_tenure_df.groupby("Agency")[["Tenure"]].agg(list).reset_index()
    emp_tenure_df = emp_tenure_df.explode("Tenure").reset_index(drop=True)
     
    if selected_countries is None or len(selected_countries) == 0:
        emp_tenure_df = emp_tenure_df[emp_tenure_df['Agency'] != 'Unknown']
  
    emp_tenure_df = emp_tenure_df.sort_values(by='Tenure', ascending=False)
    return emp_tenure_df   
   
   
def generate_avg_emp_tenuredf(selected_countries=None, selected_cities=None, selected_districts= None, selected_functions=None,
                                 selected_religions=None, selected_time_period: list = [1855, 1925], end_inclusive: bool=False):
   
    df = generate_agency_performance_df(selected_countries, selected_cities, selected_districts, selected_functions,
                                 selected_religions, selected_time_period, end_inclusive)
    if df.empty:
        return pd.DataFrame()
    
    employee_counts_df = df.groupby(["Agency", "Year"])["Tenure"].mean().reset_index(name="Avg Tenure")
    stats_df = employee_counts_df.groupby("Agency")["Avg Tenure"].agg(["mean", "min", "max"]).reset_index()
    stats_df.rename(columns={"mean": "Average Tenure", "min": "Min Tenure", "max": "Max Tenure"}, inplace=True)
    
    return stats_df


async def size_vs_tenure(selected_countries=None, selected_cities=None, selected_districts=None, selected_functions=None,
                                 selected_religions=None, selected_time_period: list = [1855, 1925], end_inclusive: bool=False):
    
    agency_size_df = generate_agency_empcountdf(selected_countries, selected_cities, selected_districts, selected_functions,
                                 selected_religions, selected_time_period, end_inclusive)
    
    avg_tenure_df = generate_avg_emp_tenuredf(selected_countries, selected_cities, selected_districts, selected_functions,
                                 selected_religions, selected_time_period, end_inclusive)
    
    if avg_tenure_df.empty or agency_size_df.empty:
        return pd.DataFrame()
    
    agency_vs_tenure_df = agency_size_df.merge(avg_tenure_df, how='outer', on='Agency')
    agency_vs_tenure_df['Average Tenure'] = agency_vs_tenure_df['Average Tenure'].round(4)
   
    agency_vs_tenure_df = agency_vs_tenure_df.replace([np.inf, -np.inf], np.nan).dropna(how="any")

    return agency_vs_tenure_df