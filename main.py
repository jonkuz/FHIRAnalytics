from datetime import datetime

from fastapi import FastAPI, HTTPException, Request

from Clickhouse.clickhouse_client import clickhouse_client
from Requests.EpisodeOfCare import get_episode_of_care
from Requests.Organization import get_organization
from Requests.Patient import get_patient
from APIs.Analytics.AnalyticsAPI import router as analytics_api_router
from APIs.MedicationStatement import router as medication_statement_router
from APIs.DocumentRefernce import router as document_reference_router
from FHIRRequests.Requests import router as FHIR_requests_router
app = FastAPI()
app.include_router(analytics_api_router)
app.include_router(medication_statement_router)
app.include_router(document_reference_router)
app.include_router(FHIR_requests_router)


@app.get("/")
async def root():
    return {"message": "Welcome to the FHIR Analytics API! See the documentation at /docs"}


@app.put("/api/data/Encounter/{encounter_id}", status_code=200)
async def handle_encounter(encounter_id: str, request: Request):
    try:
        payload = await request.json()
        # Überprüfe, ob das payload die benötigten Felder enthält
        if 'resourceType' not in payload:
            raise HTTPException(status_code=400, detail="Missing 'resourceType' in JSON payload")

        # Verarbeiten der Daten
        print(f"Received encounter {encounter_id}: {payload}")
        if len(payload['identifier']) > 1:
            # TODO implement logic
            raise HTTPException(status_code=400, detail="Multiple 'identifier' in JSON payload")

        # Convert to Datetime object
        period_start = datetime.fromisoformat(payload.get('period').get('start').replace("Z", "+00:00"))
        period_end = datetime.fromisoformat(payload.get('period').get('end').replace("Z", "+00:00"))

        row = [
            encounter_id,  # 1. encounter_id
            payload['identifier'][0].get('value'),  # 3. identifier
            payload.get('status'),  # 10. status
            payload.get('class').get('system'),  # 11. class
            period_start,  # 12. period_start
            period_end  # 13. period_end
        ]

        # Abfragen des referenzierten Patienten
        patient_id = payload['subject']['reference'].split('/')[1]
        patient = get_patient(patient_id)
        row += patient

        # Abfragen der referenzierten Episode of care
        episode_of_care_id = payload['episodeOfCare'][0]['reference'].split('/')[1]
        episode_of_care = get_episode_of_care(episode_of_care_id)
        row += episode_of_care

        # Abfragen der referenzierten Organisation
        organization_id = payload['serviceProvider']['reference'].split('/')[1]
        organization = get_organization(organization_id)
        row += organization

        # Abfragen der referenzierten Diagnose - ist optional deswegen mit get

        data = [row]
        client = clickhouse_client()
        client.insert("FHIROptimization.Encounter", data,
                      column_names=[
                          'encounter_id',  # 1
                          'identifier',
                          'status',
                          'class',  # 10
                          'period_start',
                          'period_end',
                          'patient.id',
                          'patient.identifier_use',
                          'patient.identifier_system',
                          'patient.identifier_value',
                          'patient.active',  # 20
                          'patient.name_use',
                          'patient.name_family',
                          'patient.name_given',
                          'patient.gender',
                          'patient.birth_date',
                          'patient.address_type',
                          'patient.address_line',
                          'patient.address_city',
                          'patient.address_postal_code',
                          'patient.address_country',  # 30
                          'patient.marital_status_system',
                          'patient.marital_status_code',  # 32
                          'episode_of_care.id',
                          'episode_of_care.identifier_type_coding_system',
                          'episode_of_care.identifier_type_coding_code',
                          'episode_of_care.identifier_value',
                          'episode_of_care.status',
                          'episode_of_care.patient_id',
                          'episode_of_care.managing_organization',
                          'episode_of_care.period_start',
                          'episode_of_care.period_end',
                          'service_provider.id',
                          'service_provider.name',
                          'service_provider.active',
                          'service_provider.identifier_system',
                          'service_provider.identifier_value',
                          'service_provider.type_system',
                          'service_provider.type_code',
                          'service_provider.address_type',
                          'service_provider.address_line',
                          'service_provider.address_city',
                          'service_provider.address_postal_code',
                          'service_provider.address_country',
                      ])

        # Zurückgeben der Daten damit der FHIR Server erkennt, dass die Anfrage erfolgreich war
        client.close()
        return payload
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing encounter subscription: {str(e)}")
