import datetime

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_encounter_timespan_with_parameter():
    start = datetime.datetime.now().isoformat()
    end = datetime.datetime.now() + datetime.timedelta(hours=1)
    end = end.isoformat()
    response = client.get("/analytics/EncounterTimespan?start=" + start + "&end=" + end)
    assert response.status_code == 200
    assert response.json() == {"encounter_ids": [], "start": start, "end": end}


def test_encounter_timespan_missing_parameter():
    response = client.get("/analytics/EncounterTimespan")
    assert response.status_code == 422
    assert response.json() == {'detail': [{'input': None,
                                           'loc': ['query', 'start'],
                                           'msg': 'Field required',
                                           'type': 'missing'},
                                          {'input': None,
                                           'loc': ['query', 'end'],
                                           'msg': 'Field required',
                                           'type': 'missing'}]}


def test_encounter_timespan_wrong_parameter():
    response = client.get("/analytics/EncounterTimespan?start=a&end=b")
    assert response.status_code == 422
    assert response.json() == {'detail': [{'ctx': {'error': 'input is too short'},
                                           'input': 'a',
                                           'loc': ['query', 'start'],
                                           'msg': 'Input should be a valid datetime or date, input is too '
                                                  'short',
                                           'type': 'datetime_from_date_parsing'},
                                          {'ctx': {'error': 'input is too short'},
                                           'input': 'b',
                                           'loc': ['query', 'end'],
                                           'msg': 'Input should be a valid datetime or date, input is too '
                                                  'short',
                                           'type': 'datetime_from_date_parsing'}]}


def test_encounter_timespan_wrong_parameter_name():
    response = client.get("/analytics/EncounterTimespan?random=abc")
    assert response.status_code == 422
    assert response.json() == {'detail': [{'input': None,
                                           'loc': ['query', 'start'],
                                           'msg': 'Field required',
                                           'type': 'missing'},
                                          {'input': None,
                                           'loc': ['query', 'end'],
                                           'msg': 'Field required',
                                           'type': 'missing'}]}


def test_medication_manufacturer_with_parameter():
    response = client.get("/analytics/MedicationManufacturer?medication_code=1&manufacturer_id=2")
    assert response.status_code == 200
    assert response.json() == {"medication_code": 1, "medication_statements": []}


def test_medication_manufacturer_missing_parameter():
    response = client.get("/analytics/MedicationManufacturer")
    assert response.status_code == 422
    assert response.json() == {'detail': [{'input': None,
                                           'loc': ['query', 'medication_code'],
                                           'msg': 'Field required',
                                           'type': 'missing'},
                                          {'input': None,
                                           'loc': ['query', 'manufacturer_id'],
                                           'msg': 'Field required',
                                           'type': 'missing'}]}


def test_medication_manufacturer_wrong_parameter():
    response = client.get("/analytics/MedicationManufacturer?medication_code=a&manufacturer_id=b")
    assert response.status_code == 422
    assert response.json() == {'detail': [{'input': 'a',
                                           'loc': ['query', 'medication_code'],
                                           'msg': 'Input should be a valid integer, unable to parse string '
                                                  'as an integer',
                                           'type': 'int_parsing'},
                                          {'input': 'b',
                                           'loc': ['query', 'manufacturer_id'],
                                           'msg': 'Input should be a valid integer, unable to parse string '
                                                  'as an integer',
                                           'type': 'int_parsing'}]}


def test_medication_manufacturer_wrong_parameter_name():
    response = client.get("/analytics/MedicationManufacturer?random=abc")
    assert response.status_code == 422
    assert response.json() == {'detail': [{'input': None,
                                           'loc': ['query', 'medication_code'],
                                           'msg': 'Field required',
                                           'type': 'missing'},
                                          {'input': None,
                                           'loc': ['query', 'manufacturer_id'],
                                           'msg': 'Field required',
                                           'type': 'missing'}]}


def test_medication_patient_with_parameter():
    response = client.get("/analytics/MedicationPatient?medication_code=1")
    assert response.status_code == 200
    assert response.json() == {"medication_id": 1, "patient_ids": []}


def test_medication_patient_missing_parameter():
    response = client.get("/analytics/MedicationPatient")
    assert response.status_code == 422
    assert response.json() == {'detail': [{'input': None,
                                           'loc': ['query', 'medication_code'],
                                           'msg': 'Field required',
                                           'type': 'missing'}]}


def test_medication_patient_wrong_parameter():
    response = client.get("/analytics/MedicationPatient?medication_code=abc")
    assert response.status_code == 422
    assert response.json() == {'detail': [{'input': 'abc',
                                           'loc': ['query', 'medication_code'],
                                           'msg': 'Input should be a valid integer, unable to parse string '
                                                  'as an integer',
                                           'type': 'int_parsing'}]}


def test_medication_patient_wrong_parameter_name():
    response = client.get("/analytics/MedicationPatient?random=abc")
    assert response.status_code == 422
    assert response.json() == {'detail': [{'input': None,
                                           'loc': ['query', 'medication_code'],
                                           'msg': 'Field required',
                                           'type': 'missing'}]}


def test_organization_contact_with_parameter():
    response = client.get("/analytics/OrganizationContact?organization_id=1")
    assert response.status_code == 200
    assert response.json() == {"patient_ids": [], "encounter_ids": []}


def test_organization_contact_missing_parameter():
    response = client.get("/analytics/OrganizationContact")
    assert response.status_code == 422
    assert response.json() == {'detail': [{'input': None,
                                           'loc': ['query', 'organization_id'],
                                           'msg': 'Field required',
                                           'type': 'missing'}]}


def test_organization_contact_wrong_parameter():
    response = client.get("/analytics/OrganizationContact?organization_id=abc")
    assert response.status_code == 422
    assert response.json() == {'detail': [{'input': 'abc',
                                           'loc': ['query', 'organization_id'],
                                           'msg': 'Input should be a valid integer, unable to parse string '
                                                  'as an integer',
                                           'type': 'int_parsing'}]}


def test_organization_contact_wrong_parameter_name():
    response = client.get("/analytics/OrganizationContact?random=abc")
    assert response.status_code == 422
    assert response.json() == {'detail': [{'input': None,
                                           'loc': ['query', 'organization_id'],
                                           'msg': 'Field required',
                                           'type': 'missing'}]}
