from fastapi import APIRouter, HTTPException
from Clickhouse.clickhouse_client import clickhouse_client
router = APIRouter()


# Abfrage 1
@router.get("/analytics/MedicationPatient", status_code=200)
async def medication_patient(medication_id: int):
    try:
        client = clickhouse_client()

        query = """
            SELECT patient.id 
            FROM FHIROptimization.MedicationStatement 
            WHERE arrayExists(
                innerArray -> arrayExists(medication_id -> medication_id = toString(%(medication_id)s), innerArray),
                medication.code_code
            )
        """

        result = client.query(query, parameters={"medication_id": medication_id})

        patient_ids = [row[0] for row in result.result_rows]

        return {"medication_id": medication_id, "patient_ids": patient_ids}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing analytics request: {str(e)}")


# Abfrage 2
@router.get("/analytics/PatientOrganizationContact", status_code=200)
async def patient_organization_contact(patient_id: int, organization_id: int):
    try:
        client = clickhouse_client()

        query = """
            SELECT patient.id, encounter_id
            FROM FHIROptimization.Encounter
            WHERE arrayExists(patient -> patient = toString(%(patient_id)s), patient.id)
            AND arrayExists(service_provider -> service_provider = toString(%(organization_id)s), service_provider.id)
        """

        result = client.query(query, parameters={"patient_id": patient_id, "organization_id": organization_id})

        patient_ids = [row[0] for row in result.result_rows]
        encounter_ids = [row[1] for row in result.result_rows]

        return {"patient_ids": patient_ids, "encounter_ids": encounter_ids}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing analytics request: {str(e)}")


# Abfrage 3
@router.get("/analytics/EncounterTimespan", status_code=200)
async def encounter_timespan(start: str, end: str):
    try:
        client = clickhouse_client()

        query = """
            SELECT encounter_id
            FROM FHIROptimization.Encounter
            WHERE period_start > toString(%(start)s) AND period_end < toString(%(end)s)
        """

        result = client.query(query, parameters={"start": start, "end": end})

        encounter_ids = [row[0] for row in result.result_rows]

        return {"encounter_ids": encounter_ids, "start": start, "end": end}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing analytics request: {str(e)}")


# Abfrage 4
@router.get("/analytics/MedicationManufacturer", status_code=200)
async def medication_manufacturer(medication_id: int, manufacturer_id: int):
    try:
        client = clickhouse_client()

        query = """
            SELECT medication_statement_id
            FROM FHIROptimization.MedicationStatement
            WHERE arrayExists(innerArray -> 
                arrayExists(medication_id -> medication_id = toString(%(medication_id)s), innerArray), medication.code_code)
                AND
                arrayExists(manufacturer -> manufacturer = toString(%(manufacturer_id)s), `medication.manufacturer_id`)     
        """

        result = client.query(query, parameters={"medication_id": medication_id, "manufacturer_id": manufacturer_id})

        medication_statement_ids = [row[0] for row in result.result_rows]

        return {"medication_id": medication_id, "medication_statements": medication_statement_ids}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing analytics request: {str(e)}")


