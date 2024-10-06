from fastapi import FastAPI

from APIs.Analytics.api import router as analytics_api_router
from APIs.medication_statement import router as medication_statement_router
from FHIRRequests.proxy import router as FHIR_requests_router
from APIs.encounter import router as encounter_router

app = FastAPI()
app.include_router(analytics_api_router)
app.include_router(medication_statement_router)
app.include_router(encounter_router)


app.include_router(FHIR_requests_router)


@app.get("/")
async def root():
    return {"message": "Welcome to the FHIR Analytics API! See the documentation at /docs"}
