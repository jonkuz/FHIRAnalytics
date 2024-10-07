# FHIR Analytics API
In diesem Projekt ist eine RestAPI implementiert. Diese kann die gleichen Anfragen wie ein HAPI FHIR Server verarbeiten.
Zudem kann die Schnittstelle PUT-Anfragen von der in der Bachelorarbeit definierten FHIR-Subscription empfangen. 
Diese Daten werden dann für einen Clickhouse Server aufbereitet und dort abgespeichert. 

## Voraussetzungen
- Python Version 3.11.0 installiert
- Python Package requests installiert
- Python Package fastapi installiert
- Python Package httpx installiert
- Python Package ClickHouse connect installiert

## Aufsetzen der Umgebung
- Falls noch nicht installiert: Installation von [Python 3.11](https://www.python.org/downloads/release/python-3110/)
- Klonen des Source-Codes von [github](https://github.com/jonkuz/FHIRAnalytics)
```
git clone https://github.com/jonkuz/FHIRAnalytics
```
- Einstellen des Python Interpreter (In Pycharm unten rechts)
- Installieren der Pakete requests, httpx und ClickHouse connect funktioniert in PyCharm auch über den Package Manager. 
  - [FastAPI](https://fastapi.tiangolo.com/)
  - [ClickHouse connect](https://clickhouse.com/docs/en/integrations/python)
  - [requests](https://pypi.org/project/requests/)
  - [HTTPX](https://www.python-httpx.org/)
- Installation von [Docker (Desktop)](https://www.docker.com/)  
- Installieren vom [HAPI FHIR Server](https://github.com/hapifhir/hapi-fhir-jpaserver-starter) in Docker 
  - Hierbei die Standard Ports und Einstellungen bestehen lassen, dann muss im Skript keine Anpassung vorgenommen werden.
    - Die Einstellungen für die Verbindung können unter [proxy.py](FHIRRequests/proxy.py) angepasst werden.
- Installation von [Clickhouse Server](https://hub.docker.com/r/clickhouse/clickhouse-server/)
  - Hier kann der User auf default und das Password leer gelassen werden. Dann funktioniert die im Programm bereits definierte Verbindung.
  - Anpassung der Verbindungseinstellung kann, wenn notwendig, unter [clickhouse_client.py](Clickhouse/clickhouse_client.py) vorgenommen werden.
- Ausführen der FHIR-Subscription (z.B. mit [Postman](https://www.postman.com/))
```
{
    "resourceType": "Subscription",
    "status": "active",
    "criteria": "[MedicationStatement,Encounter]",
    "contact": [{
        "system": "email",
        "value": "jonaskuzia@gmail.com"
    }],
    "reason": "Loading Data into Clickhouse for optimized analytics.",
    "channel": {
        "type": "rest-hook",
        "endpoint": "http://host.docker.internal:8000/api/data/",
        "payload": "application/fhir+json"
    }
}
```

## Ausführen der API
Zum Ausführen der API muss nur die main Methode des Python-Programmes ausgeführt werden. ([main.py](main.py))
Die Logs werden auf der Konsole ausgegeben.

## Testen der Funktionalitäten
- FHIRAnalytics API starten ([main.py](main.py))
- Clickhouse Server starten (Docker oder CLI)
- HAPI FHIR Server starten (Docker oder CLI)
- 
### Testen der Funktionalitäten
Mit dem Testdaten-Generator oder manuell eine Resource vom Typ MedicationStatement oder Encounter erzeugen. Diese kann direkt an die FHIRAnalytics API gesendet werden. Es sind keine direkten Anfragen an den FHIR Server mehr notwendig.
- Überprüfen der Logs in der API
- Prüfen, ob die Ressource von HAPI FHIR Sever angenommen wurde.
- Abrufen der Clickhouse Tabelle, ob die Daten übernommen wurden.


