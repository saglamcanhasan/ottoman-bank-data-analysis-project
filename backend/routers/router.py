from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List
from utils.response import respond
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
@router.post("/{api_name}")
async def route(api_name: str, request: Request):
    if api_name == "employee-count":
        return await respond(request, employee_count)
    elif api_name == "agency-count":
        return await respond(request, agency_count)
    elif api_name == "employee-turnover":
        return await respond(request, employee_turnover)