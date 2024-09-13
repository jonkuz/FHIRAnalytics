from pydantic import BaseModel


class Encounter(BaseModel):
    resourceType: str
    id: str
    status: str
    class_fhir: dict
    type: list