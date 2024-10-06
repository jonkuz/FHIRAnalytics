from fastapi import APIRouter
from datetime import datetime

from fastapi import FastAPI, HTTPException, Request

from Clickhouse.clickhouse_client import clickhouse_client

from Requests.encounter import get_encounter
from Requests.medication import get_medication

from Requests.patient import get_patient

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

        category = payload.get('category', None)
        status = payload.get('status', None)
        systems = []
        codes = []
        if category is not None:
            for code in category['coding']:
                systems.append(code.get('system', ""))
                codes.append(code.get('code', ""))

        medication_id = payload['medicationReference'].get('reference', "").split('/')[1]
        patient_id = payload['subject'].get('reference', "").split('/')[1]
        context_type = payload['context'].get('reference', "").split('/')[0]
        context = payload['context'].get('reference', "").split('/')[1]
        row = [
            medication_statement_id,
            status,
            systems,
            codes,
            medication_id,
            patient_id,
            context,
            effective_date_time
        ]

        medication = get_medication(medication_id)
        row += medication

        patient = get_patient(patient_id)
        row += patient

        if context_type == 'Encounter':
            encounter = get_encounter(context)
            row += encounter

        data = [row]
        client = clickhouse_client()
        client.insert("FHIROptimization.MedicationStatementNew", data,
                      column_names=[
                          'medication_statement_id',
                          'status',
                          'category.system',
                          'category.code',
                          'medication_id',
                          'subject',
                          'context',
                          'effective_date_time',
                          'medication_identifier_value',
                          'medication_code.system',
                          'medication_code.code',
                          'medication_code.display',
                          'medication_status',
                          'medication_manufacturer_id',
                          'amount_numerator_code',
                          'amount_numerator_unit',
                          'amount_numerator_system',
                          'amount_numerator_value',
                          'amount_denominator_code',
                          'amount_denominator_unit',
                          'amount_denominator_system',
                          'amount_denominator_value',
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
                          'encounter_id',
                          'encounter_identifier.system',
                          'encounter_identifier.code',
                          'encounter_identifier.value',
                          'encounter_status',
                          'encounter_class',
                          'encounter_period_start',
                          'encounter_period_end',
                      ])

        # Zurückgeben der Daten damit der FHIR Server erkennt, dass die Anfrage erfolgreich war.
        return payload

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing subscription: {str(e)}")
