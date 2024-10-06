from datetime import datetime

import requests


def get_medication_statement_new(medication_statement_id: int) -> list:
    try:
        res = requests.get("http://localhost:8080/fhir/MedicationStatement", params={"_id": medication_statement_id})
        res = res.json()
        response = res['entry'][0]['resource']
        print(f"Received medication_statement {medication_statement_id}: {response}")

        # Convert to Datetime object
        effective_date_time = response.get('effectiveDateTime', None)
        if effective_date_time is not None:
            effective_date_time = datetime.fromisoformat(response.get('effectiveDateTime').replace("Z", "+00:00"))

        category = response.get('category')
        systems = ""
        codes = ""
        if category is not None:
            for code in category['coding']:
                systems += code.get('system')
                codes += code.get('code')

        medication_id = response['medicationReference']['reference'].split('/')[1]
        patient_id = response['subject']['reference'].split('/')[1]
        context_type = response['context']['reference'].split('/')[0]
        context = response['context']['reference'].split('/')[1]

        return [
            medication_statement_id,
            response['status'],
            [systems],
            [codes],
            medication_id,
            patient_id,
            context,
            effective_date_time
        ]
    except Exception as e:
        print(e)