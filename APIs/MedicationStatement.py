from fastapi import APIRouter
from datetime import datetime

from fastapi import FastAPI, HTTPException, Request

from Clickhouse.clickhouse_client import clickhouse_client

from Requests.Encounter import get_encounter
from Requests.EpisodeOfCare import get_episode_of_care
from Requests.Medication import get_medication

from Requests.Patient import get_patient

router = APIRouter()


@router.put("/api/data/MedicationStatement/{medication_statement_id}", status_code=200)
async def handle_medication_statement(medication_statement_id: str, request: Request):
    try:
        payload = await request.json()
        if 'resourceType' not in payload:
            raise HTTPException(status_code=400, detail="Missing 'resourceType' in JSON payload")

        print(f"Received medication_statement {medication_statement_id}: {payload}")

        # Convert to Datetime object
        effective_date_time = payload.get('effectiveDateTime', None)
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
