from dash import Input, Output, callback
from utils.server.filter_parameters import cities, districts

def create_agency_dropdown_callback(figure_id):
    @callback(
        Output(f"{figure_id}-agency-city-dropdown", "options"),
        Output(f"{figure_id}-agency-city-dropdown", "disabled"),
        Output(f"{figure_id}-agency-district-dropdown", "options"),
        Output(f"{figure_id}-agency-district-dropdown", "disabled"),
        Input(f"{figure_id}-agency-country-dropdown", "value"),
        Input(f"{figure_id}-agency-city-dropdown", "value"),
    )
    def dropdown_callback(selected_countries, selected_cities):
        # no country selected
        if selected_countries is None or len(selected_countries) == 0:
            return [], True, [], True

        # generate city options
        city_set = set()
        for country in selected_countries:
            if country != "Unknown":
                city_set.update(cities[country])
        city_options = [{"label": "Unknown", "value": "Unknown"}] + ([{"label": "", "value": "", "disabled": True}] if len(city_set) != 0 else []) + [{"label": city, "value": city} for city in sorted(city_set)]

        # generate district options
        district_set = set()
        if selected_cities is not None and len(selected_cities) != 0:
            for country in selected_countries:
                for city in selected_cities:
                    if city != "Unknown":
                        district_set.update(districts[city])
            district_options = [{"label": "Unknown", "value": "Unknown"}] + ([{"label": "", "value": "", "disabled": True}] if len(district_set) != 0 else []) + [{"label": district, "value": district} for district in sorted(district_set)]
            return city_options, False, district_options, False

        return city_options, False, [], True