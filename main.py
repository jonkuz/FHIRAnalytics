from fastapi import FastAPI, HTTPException, Request
from Entities.Encounter import Encounter
import requests

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.put("/api/data/encounter/Encounter/{encounter_id}", status_code=200)
async def handle_encounter(encounter_id: str, request: Request):
    try:
        payload = await request.json()
        # Überprüfe, ob das payload die benötigten Felder enthält
        if 'resourceType' not in payload:
            raise HTTPException(status_code=400, detail="Missing 'resourceType' in JSON payload")

        # Verarbeiten der Daten

        # Abfragen des referenzierten Patienten
        print(f"Received encounter {encounter_id}: {payload}")

        patient_id = payload['subject']['reference'].split('/')[1]
        res = requests.get("http://localhost:8080/fhir/Patient", params={"_id": patient_id})
        print(res.json())
        # Zurückgeben der Daten damit der FHIR Server erkennt, dass die Anfrage erfolgreich war.
        response_payload = {
            "resourceType": payload["resourceType"],
            "id": encounter_id,
            "meta": {
                "versionId": payload['meta']['versionId'],
                "lastUpdated": payload['meta']['lastUpdated'],
                "source": payload['meta']['source']
            },
            "status": payload['status'],
            "subject": {
                "reference": payload['subject']['reference']
            }
        }

        return response_payload
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing subscription: {str(e)}")
