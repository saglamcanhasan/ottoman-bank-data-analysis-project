from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List
from utils.response import respond
from controllers.filter_parameters import filter_parameters
from controllers.coworker_network_analysis import coworker_network
from controllers.geographic_footprint_analysis import geo_footprint
from controllers.employee_profiles_analysis import employee_profiles, career_timeline
from controllers.employee_transfers_analysis import employee_transfers, employee_flow
from controllers.workforce_demographics_analysis import religion_count, religion_distribution
from controllers.agency_performance_analysis import top_agencies, employee_tenure, size_vs_tenure
from controllers.historical_overview_analysis import employee_count, agency_count, employee_turnover

# create router
router = APIRouter()

# request model
class Request(BaseModel):
    selected_districts: Optional[List[str]] = None
    selected_cities: Optional[List[str]] = None
    selected_countries: Optional[List[str]] = None
    selected_functions: Optional[List[str]] = None
    selected_religions: Optional[List[str]] = None
    selected_ids: Optional[List[str]] = None
    selected_time_period: Optional[List[int]] = None

# route get requests
@router.get("/{api_name}")
async def route_get_requests(api_name: str):
    if api_name == "filter-parameters":
        return await respond(Request(), filter_parameters)
    
@router.post("/{api_name}")
async def route_post_requests(api_name: str, request: Request):    
    if api_name == "employee-count":
        return await respond(request, employee_count)
    elif api_name == "agency-count":
        return await respond(request, agency_count)
    elif api_name == "employee-turnover":
        return await respond(request, employee_turnover)
    
    elif api_name == "geographic-footprint":
        return await respond(request, geo_footprint)
    
    elif api_name == "religion-count":
        return await respond(request, religion_count)
    elif api_name == "religion-distribution":
        return await respond(request, religion_distribution)
    
    elif api_name == "top-agencies":
        return await respond(request, top_agencies)
    elif api_name == "employee-tenure":
        return await respond(request, employee_tenure)
    elif api_name == "size-vs-tenure":
        return await respond(request, size_vs_tenure)
    
    elif api_name == "employee-transfers":
        return await respond(request, employee_transfers)
    elif api_name == "employee-flow":
        return await respond(request, employee_flow)
    
    elif api_name == "employee-profiles":
        return await respond(request, employee_profiles)
    elif api_name == "career-timeline":
        return await respond(request, career_timeline)  
    
    elif api_name == "coworker-network":
        return await respond(request, coworker_network)