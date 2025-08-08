import pandas as pd
from utils.server.data_loader import employee_df

def generate_employee_profile_df(selected_ids=None):
    if selected_ids:
        employee_data = employee_df[employee_df['ID'].isin(selected_ids)]
    else:
        employee_data = employee_df
    return employee_data

def get_multiple_employees_gantt_data(selected_ids=None):
    
    df = generate_employee_profile_df(selected_ids)
    
    if df.empty:
        return pd.DataFrame()

    gantt_data = []
    
    # Iterate through each row to create Gantt data (employee timeline by country)
    for _, row in df.iterrows():
        start_year = int(row['Period Start Year']) if pd.notna(row['Period Start Year']) else 0
        finish_year = int(row['Period End Year']) if pd.notna(row['Period End Year']) else 0
        
        if start_year is None and finish_year is None:
            continue

        if start_year is None:
            start_year = finish_year - 1

        if finish_year is None:
            finish_year = start_year + 1
            
        gantt_data.append({
            'Task': f"{row['Country']}",  # Country as Task
            'Start': start_year,
            'Finish': finish_year,
            'Employee ID': row['ID']
        })

    return pd.DataFrame(gantt_data)