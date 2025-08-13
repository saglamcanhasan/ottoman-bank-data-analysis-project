import traceback
import pandas as pd
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

async def respond(request, controller):
    # send the requested graph data
    try:
        response = await controller(**request.dict(exclude_unset=True))
        
        type = "builtin"
        if isinstance(response, pd.DataFrame):
            response = response.to_dict(orient="records")
            type = "dataframe"
        if isinstance(response, tuple):
            types = list("dataframe" if isinstance(item, pd.DataFrame) else "builtin" for item in response)
            if any(type == "dataframe" for type in types):
                response = [item.to_dict(orient="records") if isinstance(item, pd.DataFrame) else item for item in response]
                type = types

        return JSONResponse(content={"data": jsonable_encoder(response), "type": type}, status_code=200)
    
    # send an error response
    except Exception as exception:
        print(f"ERROR <= {str(exception)}")
        traceback.print_exception(exception)
        return JSONResponse(content={"error": str(exception)}, status_code=500)
