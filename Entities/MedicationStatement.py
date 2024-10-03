from pydantic import BaseModel


class MedicationStatement(BaseModel):
    medication_statement_id: int
    status: str
    system: dict
    code: dict
    medication: str
    patient: str
    context: str
    effective_date_time: str
