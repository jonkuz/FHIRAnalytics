from fastapi import APIRouter
from datetime import datetime

from fastapi import FastAPI, HTTPException, Request

from Clickhouse.clickhouse_client import clickhouse_client

router = APIRouter()


@router.put("/api/data/DocumentReference/{document_reference_id}", status_code=200)
async def handle_encounter(document_reference_id: str, request: Request):
    try:
        payload = await request.json()
        if 'resourceType' not in payload:
            raise HTTPException(status_code=400, detail="Missing 'resourceType' in JSON payload")

        print(f"Received document_reference {document_reference_id}: {payload}")

        status = payload.get('status')
        type_system = []
        type_code = []
        type_display = []
        for coding in payload['type']['coding']:
            type_system.append(coding['system'])
            type_code.append(coding['code'])
            type_display.append(coding['display'])

        category_system = []
        category_code = []
        category_display = []
        for category in payload['category']:
            for code in category['coding']:
                category_system.append(code['system'])
                category_code.append(code['code'])
                category_display.append(code['display'])

        patient_id = payload['subject']['reference'].split('/')[1]
        context_ids = []
        for context in payload['context'].get('encounter', []):
            context_ids.append(context['reference'].split('/')[1])

        for context in payload['context'].get('episodeOfCare', []):
            context_ids.append(context['reference'].split('/')[1])

        content_type = []
        content_url = []
        content_title = []
        content_format = []
        for a in payload['content']:
            content_type.append(a.get('attachment', "").get('contentType', ""))
            content_url.append(a.get('attachment', "").get('url', ""))
            content_title.append(a.get('attachment', "").get('title', ""))
            temp = a.get('format', "")
            if temp != "":
                content_format.append(a.get('format', "").get('display', ""))
            else:
                content_format.append("")

        row = [
            document_reference_id,
            status,
            type_system,
            type_code,
            type_display,
            category_system,
            category_code,
            category_display,
            patient_id,
            context_ids,
            content_type,
            content_url,
            content_title,
            content_format
        ]
        data = [row]
        client = clickhouse_client()
        client.insert("FHIROptimization.DocumentReference", data,
                      column_names=[
                          'document_reference_id',
                          'status',
                          'type.system',
                          'type.code',
                          'type.display',
                          'category.system',
                          'category.code',
                          'category.display',
                          'patient_id',
                          'context_ids',
                          'content.type',
                          'content.url',
                          'content.title',
                          'content.content_format'
                      ])

        # Zurückgeben der Daten damit der FHIR Server erkennt, dass die Anfrage erfolgreich war.
        return payload

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing subscription: {str(e)}")
