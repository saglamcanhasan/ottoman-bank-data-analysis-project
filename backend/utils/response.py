import numpy as np
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

        return JSONResponse(content={"data": jsonable_encoder(response), "type": type}, status_code=200)
    
    # send an error response
    except Exception as exception:
        return JSONResponse(content={"error": str(exception)}, status_code=500)
