from fastapi import APIRouter, HTTPException

from Clickhouse.clickhouse_client import clickhouse_client

router = APIRouter()


@router.get("/MedicationPatient", status_code=200)
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
        raise HTTPException(status_code=500, detail=f"Error processing subscription: {str(e)}")
