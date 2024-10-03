from fastapi import APIRouter, HTTPException
import httpx
from starlette.requests import Request

router = APIRouter()


# URL des echten FHIR Servers
FHIR_SERVER_URL = "http://localhost:8080/fhir/"


@router.api_route("/fhir/Patient", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_patient(request: Request):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method=request.method,
                url=FHIR_SERVER_URL + "Patient",
                headers=request.headers,
                params=request.query_params,
                content=await request.body()
            )
            return response.json(), response.status_code, response.headers
        except Exception as e:
            raise HTTPException(status_code=400, detail="Error proxying the request")


@router.api_route("/fhir/Encounter", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_encounter(request: Request):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method=request.method,
                url=FHIR_SERVER_URL + "Encounter",
                headers=request.headers,
                params=request.query_params,
                content=await request.body()
            )
            return response.json(), response.status_code, response.headers
        except Exception as e:
            raise HTTPException(status_code=400, detail="Error proxying the request")


@router.api_route("/fhir/DocumentReference", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_encounter(request: Request):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method=request.method,
                url=FHIR_SERVER_URL + "DocumentReference",
                headers=request.headers,
                params=request.query_params,
                content=await request.body()
            )
            return response.json(), response.status_code, response.headers
        except Exception as e:
            raise HTTPException(status_code=400, detail="Error proxying the request")


@router.api_route("/fhir/MedicationStatement", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_encounter(request: Request):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method=request.method,
                url=FHIR_SERVER_URL + "MedicationStatement",
                headers=request.headers,
                params=request.query_params,
                content=await request.body()
            )
            return response.json(), response.status_code, response.headers
        except Exception as e:
            raise HTTPException(status_code=400, detail="Error proxying the request")


@router.api_route("/fhir/Organization", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_encounter(request: Request):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method=request.method,
                url=FHIR_SERVER_URL + "Organization",
                headers=request.headers,
                params=request.query_params,
                content=await request.body()
            )
            return response.json(), response.status_code, response.headers
        except Exception as e:
            raise HTTPException(status_code=400, detail="Error proxying the request")


@router.api_route("/fhir/Condition", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_encounter(request: Request):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method=request.method,
                url=FHIR_SERVER_URL + "Condition",
                headers=request.headers,
                params=request.query_params,
                content=await request.body()
            )
            return response.json(), response.status_code, response.headers
        except Exception as e:
            raise HTTPException(status_code=400, detail="Error proxying the request")


@router.api_route("/fhir/Procedure", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_encounter(request: Request):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method=request.method,
                url=FHIR_SERVER_URL + "Procedure",
                headers=request.headers,
                params=request.query_params,
                content=await request.body()
            )
            return response.json(), response.status_code, response.headers
        except Exception as e:
            raise HTTPException(status_code=400, detail="Error proxying the request")


@router.api_route("/fhir/EpisodeOfCare", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_encounter(request: Request):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method=request.method,
                url=FHIR_SERVER_URL + "EpisodeOfCare",
                headers=request.headers,
                params=request.query_params,
                content=await request.body()
            )
            return response.json(), response.status_code, response.headers
        except Exception as e:
            raise HTTPException(status_code=400, detail="Error proxying the request")


@router.api_route("/fhir/Medication", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_encounter(request: Request):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method=request.method,
                url=FHIR_SERVER_URL + "Medication",
                headers=request.headers,
                params=request.query_params,
                content=await request.body()
            )
            return response.json(), response.status_code, response.headers
        except Exception as e:
            raise HTTPException(status_code=400, detail="Error proxying the request")


@router.api_route("/fhir/Subscription", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_encounter(request: Request):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method=request.method,
                url=FHIR_SERVER_URL + "Subscription",
                headers=request.headers,
                params=request.query_params,
                content=await request.body()
            )
            return response.json(), response.status_code, response.headers
        except Exception as e:
            raise HTTPException(status_code=400, detail="Error proxying the request")
