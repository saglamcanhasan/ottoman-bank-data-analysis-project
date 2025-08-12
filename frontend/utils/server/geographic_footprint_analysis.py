from utils.server.data_loader import agency_geo_df, employee_df
from utils.server.filter import filter

def generate_geo_df(selected_countries=None, selected_cities=None, selected_districts= None,selected_functions=None,
                                 selected_religions=None, selected_time_period: list = [1855, 1925]):
    df = agency_geo_df.copy()
    emp_df = employee_df.copy()
    time_period_start_year, time_period_end_year = selected_time_period
    
    emp_df = filter(emp_df, True, selected_countries, selected_cities, selected_districts, selected_functions, selected_religions, None, time_period_start_year, time_period_end_year)
    df = filter(df, False, selected_countries, selected_cities, selected_districts, None, None, None, time_period_start_year, time_period_end_year)

    unique_employees_per_city = emp_df.groupby('City')['ID'].nunique().reset_index()
    unique_employees_per_city.columns = ['City', 'Employee Count']

    df = df.merge(unique_employees_per_city, on='City', how='left')
    df['Employee Count'] = df['Employee Count'].fillna(0)
    
    return df

