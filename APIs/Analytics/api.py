import datetime

from fastapi import APIRouter, HTTPException
from Clickhouse.clickhouse_client import clickhouse_client
router = APIRouter()


# Abfrage 1
@router.get("/analytics/MedicationPatient", status_code=200)
async def medication_patient(medication_code: int):
    try:
        client = clickhouse_client()

        query = """
            SELECT subject 
            FROM FHIROptimization.MedicationStatement
            WHERE arrayExists(code -> code = toString(%(medication_code)s), medication_code.code)
        """

        result = client.query(query, parameters={"medication_code": medication_code})

        patient_ids = [row[0] for row in result.result_rows]

        return {"medication_id": medication_code, "patient_ids": patient_ids}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing analytics request: {str(e)}")


# Abfrage 2
@router.get("/analytics/OrganizationContact", status_code=200)
async def patient_organization_contact(organization_id: int):
    try:
        client = clickhouse_client()

        query = """
            SELECT patient_id, encounter_id
            FROM FHIROptimization.Encounter
            WHERE service_provider_id = toString(%(organization_id)s)
        """

        result = client.query(query, parameters={"organization_id": organization_id})

        patient_ids = [row[0] for row in result.result_rows]
        encounter_ids = [row[1] for row in result.result_rows]

        return {"patient_ids": patient_ids, "encounter_ids": encounter_ids}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing analytics request: {str(e)}")


# Abfrage 3
@router.get("/analytics/EncounterTimespan", status_code=200)
async def encounter_timespan(start: datetime.datetime, end: datetime.datetime):
    try:
        if type(start) is not datetime.datetime or type(end) is not datetime.datetime:
            raise HTTPException(status_code=400, detail=f"start and end must be datetime objects")
        client = clickhouse_client()

        query = """
            SELECT encounter_id
            FROM FHIROptimization.Encounter
            WHERE period_start > toString(%(start)s) AND period_end < toString(%(end)s)
            AND patient_active = true
        """

        result = client.query(query, parameters={"start": start, "end": end})

        encounter_ids = [row[0] for row in result.result_rows]

        return {"encounter_ids": encounter_ids, "start": start, "end": end}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing analytics request: {str(e)}")


# Abfrage 4
@router.get("/analytics/MedicationManufacturer", status_code=200)
async def medication_manufacturer(medication_code: int, manufacturer_id: int):
    try:
        client = clickhouse_client()

        query = """
            SELECT medication_statement_id
            FROM FHIROptimization.MedicationStatement
            WHERE arrayExists(code -> code = toString(%(medication_code)s), medication_code.code)
                AND
                medication_manufacturer_id = toString(%(manufacturer_id)s)     
        """

        result = client.query(query, parameters={"medication_code": medication_code, "manufacturer_id": manufacturer_id})

        medication_statement_ids = [row[0] for row in result.result_rows]

        return {"medication_code": medication_code, "medication_statements": medication_statement_ids}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing analytics request: {str(e)}")
