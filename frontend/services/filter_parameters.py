from services.request import request

filter_parameters = request("filter-parameters")

if filter_parameters is None:
    raise Exception("Back-end server does not respond. Needed at initialization for filter parameters.")
    
else:
    countries = filter_parameters["countries"]
    cities = filter_parameters["cities"]
    districts = filter_parameters["districts"]
    functions = filter_parameters["functions"]
    religions = filter_parameters["religions"]
    ids = filter_parameters["ids"]
    start = filter_parameters["start"]
    end = filter_parameters["end"]