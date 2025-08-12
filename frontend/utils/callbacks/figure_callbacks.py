from dash import Input, Output, callback

def create_figure_callback(generate_df, generate_figure, figure_id: str, agency: bool, grouped_function: bool, religion: bool, id: bool, time_period: bool, is_cyto=False, filter_id: str=""):
    # get figure id
    if len(filter_id) == 0:
        filter_id = figure_id
    
    # determine inputs
    inputs = list()
    arg_names = []

    if agency:
        inputs.extend([
                Input(f"{filter_id}-agency-country-dropdown", "value"),
                Input(f"{filter_id}-agency-city-dropdown", "value"),
                Input(f"{filter_id}-agency-district-dropdown", "value")
            ]
        )
        arg_names.extend(["selected_countries", "selected_cities", "selected_districts"])

    if grouped_function:
        inputs.append(Input(f"{filter_id}-function-dropdown", "value"))
        arg_names.append("selected_functions")

    if religion:
        inputs.append(Input(f"{filter_id}-religion-dropdown", "value"))
        arg_names.append("selected_religions")

    if id:
        inputs.append(Input(f"{filter_id}-id-dropdown", "value"))
        arg_names.append("selected_ids")

    if time_period:
        inputs.append(Input(f"{filter_id}-time-period-slider", "value"))
        arg_names.append("selected_time_period")
        
    @callback(
        Output(figure_id, "figure" if not is_cyto else "elements"),
        *inputs
    )
    def figure_callback(*args):
        # name arguments
        kwargs = dict(zip(arg_names, args))

        df = generate_df(**kwargs)
        return generate_figure(df)