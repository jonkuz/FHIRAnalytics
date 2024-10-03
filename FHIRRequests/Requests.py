from fastapi import APIRouter, HTTPException
import httpx
from starlette.requests import Request
from typing import List

router = APIRouter()

FHIR_SERVER_URL = "http://localhost:8080/fhir/"


async def forward_request(resource_type: str, request: Request):
    async with httpx.AsyncClient() as client:
        try:
            url = f"{FHIR_SERVER_URL}{resource_type}"

            response = await client.request(
                method=request.method,
                url=url,
                headers=request.headers,
                params=request.query_params,
                content=await request.body(),
            )

            return response.json(), response.status_code, response.headers
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error proxying the request: {str(e)}")


FHIR_RESOURCES: List[str] = [
    "Patient", "Encounter", "DocumentReference", "MedicationStatement",
    "Organization", "Condition", "Procedure", "EpisodeOfCare",
    "Medication", "Subscription"
]

for resource in FHIR_RESOURCES:
    @router.api_route(f"/fhir/{resource}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
    async def proxy_resource(request: Request, resource_type=resource):
        return await forward_request(resource_type, request)
