from fastapi import APIRouter
from datetime import datetime
from fastapi import FastAPI, HTTPException, Request
from Clickhouse.clickhouse_client import clickhouse_client
from Requests.episode_of_care import get_episode_of_care
from Requests.organization import get_organization
from Requests.patient import get_patient

router = APIRouter()


@router.put("/api/data/Encounter/{encounter_id}", status_code=200)
async def handle_encounter(encounter_id: str, request: Request):
    try:
        payload = await request.json()
        if 'resourceType' not in payload:
            raise HTTPException(status_code=400, detail="Missing 'resourceType' in JSON payload")
        print(f"Received encounter {encounter_id}: {payload}")

        identifier_system = []
        identifier_code = []
        identifier_value = []
        identifier = payload.get('identifier', [])
        for i in identifier:
            identifier_system.append(i.get('system', ""))
            identifier_code.append(i.get('code', ""))
            identifier_value.append(i.get('value', ""))

        status = payload.get('status', None)
        encounter_class = payload.get('class').get('system')

        period_start = datetime.fromisoformat(payload.get('period').get('start').replace("Z", "+00:00"))
        period_end = datetime.fromisoformat(payload.get('period').get('end').replace("Z", "+00:00"))

        row = [
            encounter_id,
            identifier_system,
            identifier_code,
            identifier_value,
            status,
            encounter_class,
            period_start,
            period_end
        ]

        # Abfragen des referenzierten Patienten
        patient_id = payload['subject']['reference'].split('/')[1]
        patient = get_patient(patient_id)
        row += patient

        # Abfragen der referenzierten EpisodeOfCare
        episode_of_care_id = payload['episodeOfCare'][0]['reference'].split('/')[1]
        episode_of_care = get_episode_of_care(episode_of_care_id)
        row += episode_of_care

        # Abfragen der referenzierten Organization
        organization_id = payload['serviceProvider']['reference'].split('/')[1]
        organization = get_organization(organization_id)
        row += organization

        data = [row]
        client = clickhouse_client()
        client.insert("FHIROptimization.Encounter", data,
                      column_names=[
                          'encounter_id',
                          'identifier.system',
                          'identifier.code',
                          'identifier.value',
                          'status',
                          'class',
                          'period_start',
                          'period_end',
                          'patient_id',
                          'patient_identifier.use',
                          'patient_identifier.system',
                          'patient_identifier.value',
                          'patient_active',
                          'patient_name.use',
                          'patient_name.text',
                          'patient_name.family',
                          'patient_name.given',
                          'patient_gender',
                          'patient_birth_date',
                          'patient_address.type',
                          'patient_address.line',
                          'patient_address.city',
                          'patient_address.postal_code',
                          'patient_address.country',
                          'patient_marital_status_system',
                          'patient_marital_status_code',
                          'episode_of_care_id',
                          'episode_of_care_identifier.value',
                          'episode_of_care_status',
                          'managing_organization_id',
                          'episode_of_care_period_start',
                          'episode_of_care_period_end',
                          'service_provider_id',
                          'service_provider_name',
                          'service_provider_active',
                          'service_provider_identifier.system',
                          'service_provider_identifier.value',
                          'service_provider_type.system',
                          'service_provider_type.code',
                          'service_provider_address.type',
                          'service_provider_address.line',
                          'service_provider_address.city',
                          'service_provider_address.postal_code',
                          'service_provider_address.country'
                      ])

        # Zurückgeben der Daten damit der FHIR Server erkennt, dass die Anfrage erfolgreich war
        client.close()
        return payload
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing encounter subscription: {str(e)}")
