from datetime import datetime

from fastapi import FastAPI, HTTPException, Request

from Clickhouse.clickhouse_client import clickhouse_client
import requests

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

        # Konvertiere den String zu einem datetime-Objekt, das ISO 8601 unterstützt
        meta_last_updated = datetime.fromisoformat(payload['meta']['lastUpdated'].replace("Z", "+00:00"))

        period_start = datetime.fromisoformat(payload['period']['start'].replace("Z", "+00:00"))

        period_end = datetime.fromisoformat(payload["period"]['end'].replace("Z", "+00:00"))
        row = [
            encounter_id,  # 1. encounter_id
            payload['identifier'][0]['value'],  # 3. identifier
            [payload['meta']['versionId']],  # 4. meta.version_id
            [meta_last_updated],  # 5. meta.last_updated
            [payload['meta']['source']],  # 6. meta.source
            [payload['meta']['tag'][0]['system']],  # 7. meta.tag_system
            [payload['meta']['tag'][0]['code']],  # 8. meta.tag_code
            [payload['meta']['tag'][0]['display']],  # 9. meta.display
            payload['status'],  # 10. status
            payload['class']['system'],  # 11. class
            period_start,  # 12. period_start
            period_end  # 13. period_end
        ]
        data = [row]
        print(row)
        client = clickhouse_client()
        client.insert("FHIROptimization.Test", data, column_names=[
            'encounter_id',  # 1
            'identifier',  # 3
            'meta.version_id',  # 4
            'meta.last_updated',  # 5
            'meta.source',  # 6
            'meta.tag_system',  # 7
            'meta.tag_code',  # 8
            'meta.display',  # 9
            'status',  # 10
            'class',  # 11
            'period_start',  # 12
            'period_end'  # 13
        ])
        x = '''
        # Abfragen des referenzierten Patienten
        patient_id = payload['subject']['reference'].split('/')[1]
        res = requests.get("http://localhost:8080/fhir/Patient", params={"_id": patient_id})
        patient_response = res.json()
        # Anhängen des Patienten in die row
        patient_id = patient_response['entry'][0]['resource']['id']
        patient_version_id = patient_response['entry'][0]['resource']['meta']['versionId']
        patient_last_updated = patient_response['entry'][0]['resource']['meta']['lastUpdated']
        patient_source = patient_response['entry'][0]['resource']['meta']['source']
        identifier_use = ""
        identifier_system = ""
        identifier_value = ""
        for identifier in patient_response['entry'][0]['resource']['identifier']:
            identifier_use += identifier['use']
            identifier_system += identifier['system']
            identifier_value += identifier['value']

        patient_active = patient_response['entry'][0]['resource']['active']

        patient_name_use = ""
        patient_family = ""
        patient_given = ""
        for name in patient_response['entry'][0]['resource']['name']:
            patient_name_use += name['use']
            patient_family += name['family']
            for given in name['given']:
                patient_given += given

        patient_gender = patient_response['entry'][0]['resource']['gender']
        patient_birth_date = patient_response['entry'][0]['resource']['birthDate']

        address_type = ""
        address_line = ""
        address_city = ""
        address_postal_code = ""
        address_country = ""
        for address in patient_response['entry'][0]['resource']['address']:
            address_type += address['type']
            for line in address['line']:
                address_line += line
            address_city += address['city']
            address_postal_code += address['postalCode']
            address_country += address['country']

        marital_status_system = ""
        marital_status_code = ""
        for marital_status in patient_response['entry'][0]['resource']['maritalStatus']['coding']:
            marital_status_system += marital_status['system']
            marital_status_code += marital_status['code']

        row += [patient_id, patient_version_id, patient_last_updated, patient_source, identifier_use, identifier_system,
                identifier_value, patient_active, patient_name_use, patient_family, patient_given, patient_gender,
                patient_birth_date, address_type, address_line, address_city, address_postal_code, address_country,
                marital_status_system, marital_status_code]
        print(row)

        client.insert("FHIROptimization.EncounterTest", row, column_names=['encounter_id', 'timestamp', 'identifier',
                                                                           'meta.version_id', 'meta.last_updated',
                                                                           'meta.source', 'meta.tag_system',
                                                                           'meta.tag_code', 'meta.display', 'status',
                                                                           'class', 'period_start', 'period_end',
                                                                           'patient.id', 'patient.meta_version_id',
                                                                           'patient.meta_last_updated',
                                                                           'patient.meta_source',
                                                                           'patient.identifier_use',
                                                                           'patient.identifier_system',
                                                                           'patient.identifier_value',
                                                                           'patient.active', 'patient.name_use',
                                                                           'patient.name_family',
                                                                           'patient.name_given', 'patient.gender',
                                                                           'patient.birth_date',
                                                                           'patient.address_type',
                                                                           'patient.address_line',
                                                                           'patient.address_city',
                                                                           'patient.address_postal_code',
                                                                           'patient.address_country',
                                                                           'patient.marital_status_system',
                                                                           'patient.marital_status_code'
                                                                           ])
        # Abfragen des referenzierten Encounters

        episode_of_care_id = payload['episodeOfCare'][0]['reference'].split('/')[1]
        res = requests.get("http://localhost:8080/fhir/EpisodeOfCare", params={"_id": episode_of_care_id})
        eoc_response = res.json()
        '''
        # Zurückgeben der Daten damit der FHIR Server erkennt, dass die Anfrage erfolgreich war.
        response_payload = {
            "resourceType": payload['resourceType'],
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


@app.put("/api/data/MedicationStatement/{encounter_id}", status_code=200)
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
