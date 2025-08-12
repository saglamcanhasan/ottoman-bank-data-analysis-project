import pandas as pd
from utils.server.data_loader import employee_df
from utils.server.filter import filter

def generate_agency_performance_df(selected_countries=None, selected_cities=None, selected_districts= None,selected_functions=None,
                                 selected_religions=None, selected_time_period: list = [1855, 1925], end_inclusive: bool=False):
    df = employee_df.copy()
    time_period_start_year, time_period_end_year = selected_time_period
    df = filter(df, True, selected_countries, selected_cities, None, selected_functions, selected_religions, None, time_period_start_year, time_period_end_year)
    return df


def generate_agency_empcountdf(selected_countries=None, selected_cities=None, selected_districts= None,selected_functions=None,
                                 selected_religions=None, selected_time_period: list = [1855, 1925], end_inclusive: bool=False):
    
    df = generate_agency_performance_df(selected_countries, selected_cities, selected_districts ,selected_functions,
                                 selected_religions, selected_time_period, end_inclusive)
    if df.empty:
        return pd.DataFrame()
    
    unique_employees_per_city = df.groupby('City')['ID'].nunique().reset_index()
    unique_employees_per_city.columns = ['City', 'Unique Employee Count']
    
    return unique_employees_per_city
    
   
def generate_top_agency_empcountdf(selected_countries=None, selected_cities=None, selected_districts= None,selected_functions=None,
                                 selected_religions=None, selected_time_period: list = [1855, 1925], end_inclusive: bool=False):
    
    df = generate_agency_empcountdf(selected_countries, selected_cities, selected_districts,selected_functions,
                                 selected_religions, selected_time_period, end_inclusive)
   
    if selected_countries is None or len(selected_countries) == 0:
        df = df[df['City'] != 'Unknown']
        
    if not df.empty:
        df = df.sort_values(by='Unique Employee Count', ascending=False).head(10)
    return df
   
def generate_emp_tenuredf(selected_countries=None, selected_cities=None, selected_districts= None,selected_functions=None,
                                 selected_religions=None, selected_time_period: list = [1855, 1925], end_inclusive: bool=False):
    
    df = generate_agency_performance_df(selected_countries, selected_cities, selected_districts,selected_functions,
                                 selected_religions, selected_time_period, end_inclusive)
   
    if df.empty:
        return pd.DataFrame()

    emp_tenure_df = df.groupby(['ID', 'City'])['Tenure'].mean().reset_index()
    emp_tenure_df = emp_tenure_df.groupby("City")[["Tenure"]].agg(list).reset_index()
    emp_tenure_df = emp_tenure_df.explode("Tenure").reset_index(drop=True)
     
    if selected_countries is None or len(selected_countries) == 0:
        emp_tenure_df = emp_tenure_df[emp_tenure_df['City'] != 'Unknown']
    
    #print(emp_tenure_df)    
    return emp_tenure_df   
   
   
def generate_avg_emp_tenuredf(selected_countries=None, selected_cities=None, selected_districts= None, selected_functions=None,
                                 selected_religions=None, selected_time_period: list = [1855, 1925], end_inclusive: bool=False):
   
    df = generate_agency_performance_df(selected_countries, selected_cities, selected_districts, selected_functions,
                                 selected_religions, selected_time_period, end_inclusive)
    if df.empty:
        return pd.DataFrame()
    
    avg_tenure_by_agency = df.groupby('City')['Tenure'].mean().reset_index()
    avg_tenure_by_agency.columns = ['City', 'Avg Tenure']
    
    return avg_tenure_by_agency


def generate_agency_vs_avgtenuredf(selected_countries=None, selected_cities=None, selected_districts=None, selected_functions=None,
                                 selected_religions=None, selected_time_period: list = [1855, 1925], end_inclusive: bool=False):
    
    agency_size_df = generate_agency_empcountdf(selected_countries, selected_cities, selected_districts, selected_functions,
                                 selected_religions, selected_time_period, end_inclusive)
    
    avg_tenure_df = generate_avg_emp_tenuredf(selected_countries, selected_cities, selected_districts, selected_functions,
                                 selected_religions, selected_time_period, end_inclusive)
    
    if avg_tenure_df.empty or agency_size_df.empty:
        return pd.DataFrame()
    
    agency_vs_tenure_df = agency_size_df.merge(avg_tenure_df, how='outer', on='City')
    agency_vs_tenure_df['Avg Tenure'] = agency_vs_tenure_df['Avg Tenure'].round(4)
    
    #print(agency_vs_tenure_df)
    return pd.DataFrame(agency_vs_tenure_df)