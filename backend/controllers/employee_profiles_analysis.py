import pandas as pd
from services.data_loader import employee_df

def generate_employee_profile_df(selected_ids=None):
    if selected_ids:
        employee_data = employee_df[employee_df['ID'].isin(selected_ids)]
    else:
        employee_data = employee_df
    return employee_data

async def career_timeline(selected_ids=None):
    
    df = generate_employee_profile_df(selected_ids)
    
    if df.empty:
        return pd.DataFrame()

    gantt_data = []
    
    # Iterate through each row to create Gantt data (employee timeline by country)
    for _, row in df.iterrows():
        start_year = int(row['Period Start Year']) if pd.notna(row['Period Start Year']) else 0
        finish_year = int(row['Period End Year']) if pd.notna(row['Period End Year']) else 0
        
        if start_year == 0 and finish_year == 0:
            continue

        if start_year == 0:
            start_year = finish_year - 1

        if finish_year == 0 or finish_year == start_year:
            finish_year = start_year + 1
            
        gantt_data.append({
            'Task': f"{row['Country']}",  # Country as Task
            'Start': start_year,
            'Finish': finish_year,
            'Employee ID': row['ID']
        })

    df_g = pd.DataFrame(gantt_data)
    df_g['Start'] = pd.to_datetime(df_g['Start'], format='%Y')  # Convert to datetime 
    df_g['Finish'] = pd.to_datetime(df_g['Finish'], format='%Y') 

    return df_g




async def employee_profiles(selected_ids=None):
    
    df = generate_employee_profile_df(selected_ids)
    
    if df.empty:
        return pd.DataFrame()
    
    profiles = []

    for employee_id in df['ID'].unique():
        employee_data = df[df['ID'] == employee_id]
        
        countries_worked_in = set()
        functions_worked_in = set() 
        unique_agencies = set() 

        for _, row in employee_data.iterrows():
            countries_worked_in.add(row['Country'])
            functions_worked_in.add(row['Function'])
            unique_agencies.add(row['Agency'])
        
        # Prepare the profile data
        profile = {
            'Employee ID': employee_id,
            'Total Career Length': row['Career End Year'] - row['Career Start Year'] + 1, 
            'Countries Worked In': ', '.join(countries_worked_in), 
            'Functions Worked In': ', '.join(functions_worked_in),  
            'Unique Agencies': ' / '.join(unique_agencies)  
        }

        profiles.append(profile)
    
    profile_df = pd.DataFrame(profiles)
    
    return profile_df