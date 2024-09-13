from fastapi import FastAPI, HTTPException, Request
from Entities.Encounter import Encounter

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.put("/api/data/encounter/Encounter/{encounter_id}")
async def handle_encounter(encounter_id: str, request: Request):
    try:
        payload = await request.json()
        # Überprüfe, ob das payload die benötigten Felder enthält
        if 'resourceType' not in payload:
            raise HTTPException(status_code=400, detail="Missing 'resourceType' in JSON payload")

        # Optional: Validierung und Verarbeitung des Encounters hier
        print(f"Received encounter {encounter_id}: {payload}")

        # Beispielhafte Rückgabe eines Encounter-Objekts im FHIR-Format
        response_payload = {
            "resourceType": "Encounter",
            "id": encounter_id,
            "status": "completed"  # Beispielstatus, passe dies nach Bedarf an
        }

        return response_payload
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing subscription: {str(e)}")
