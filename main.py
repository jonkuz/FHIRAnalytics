from datetime import datetime

from fastapi import FastAPI, HTTPException, Request

from Clickhouse.clickhouse_client import clickhouse_client
import requests

from Requests.Diagnosis import get_condition
from Requests.Encounter import get_encounter
from Requests.EpisodeOfCare import get_episode_of_care
from Requests.Medication import get_medication
from Requests.Organization import get_organization
from Requests.Patient import get_patient

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


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


@app.put("/api/data/DocumentReference/{encounter_id}", status_code=200)
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


@app.put("/api/data/MedicationStatement/{medication_statement_id}", status_code=200)
async def handle_encounter(medication_statement_id: str, request: Request):
    try:
        payload = await request.json()
        if 'resourceType' not in payload:
            raise HTTPException(status_code=400, detail="Missing 'resourceType' in JSON payload")

        print(f"Received medication_statement {medication_statement_id}: {payload}")

        # Convert to Datetime object
        effective_date_time = payload.get('effectiveDateTime')
        if effective_date_time is not None:
                effective_date_time = datetime.fromisoformat(payload.get('effectiveDateTime').replace("Z", "+00:00"))


        category = payload.get('category')
        systems = ""
        codes = ""
        if category is not None:
            for code in category['coding']:
                systems += code.get('system')
                codes += code.get('code')

        medication_id = payload['medicationReference']['reference'].split('/')[1]
        patient_id = payload['subject']['reference'].split('/')[1]
        context_type = payload['context']['reference'].split('/')[0]
        context = payload['context']['reference'].split('/')[1]
        row = [
            medication_statement_id,
            payload['status'],
            [systems],
            [codes],
            medication_id,
            patient_id,
            context,
            effective_date_time
        ]

        medication = get_medication(medication_id)
        row += medication

        patient = get_patient(patient_id)
        row += patient

        if context_type == 'EpisodeOfCare':
            get_episode_of_care(context)

        if context_type == 'Encounter':
            encounter = get_encounter(context)
            row += encounter

        data = [row]
        client = clickhouse_client()
        client.insert("FHIROptimization.MedicationStatement", data,
                      column_names=[
                          'medication_statement_id',
                          'status',
                          'category.system',
                          'category.code',
                          'medication_id',
                          'subject',
                          'context',
                          'effective_date_time',
                          'medication.id',
                          'medication.identifier_value',
                          'medication.code_system',
                          'medication.code_code',
                          'medication.code_display',
                          'medication.status',
                          'medication.manufacturer_id',
                          'medication.amount_numerator_code',
                          'medication.amount_numerator_unit',
                          'medication.amount_numerator_system',
                          'medication.amount_numerator_value',
                          'medication.amount_denominator_code',
                          'medication.amount_denominator_unit',
                          'medication.amount_denominator_system',
                          'medication.amount_denominator_value',
                          'patient.id',
                          'patient.identifier_use',
                          'patient.identifier_system',
                          'patient.identifier_value',
                          'patient.active',
                          'patient.name_use',
                          'patient.name_family',
                          'patient.name_given',
                          'patient.gender',
                          'patient.birth_date',
                          'patient.address_type',
                          'patient.address_line',
                          'patient.address_city',
                          'patient.address_postal_code',
                          'patient.address_country',
                          'patient.marital_status_system',
                          'patient.marital_status_code',
                          'encounter.id',
                          'encounter.identifier',
                          'encounter.status',
                          'encounter.class',
                          'encounter.period_start',
                          'encounter.period_end',
                      ])

        # Zurückgeben der Daten damit der FHIR Server erkennt, dass die Anfrage erfolgreich war.
        return payload

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing subscription: {str(e)}")
