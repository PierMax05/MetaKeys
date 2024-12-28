# Configurazione di Celery per eseguire un task alle 3 di notte

Questa guida ti mostrerà come configurare Celery per eseguire un task ogni notte alle 3:00 nel tuo progetto Django.

## Prerequisiti

- Python 3.x
- Django
- Redis
- Celery

## Passaggi

### 1. Installa Redis

#### Su macOS con Homebrew

```sh
brew install redis
brew services start redis

Su Ubuntu con systemd
2. Installa Celery e le dipendenze
Aggiungi Celery e Redis come dipendenze nel tuo progetto Django:

3. Configura Celery nel progetto Django
metaKeys/settings.py
Aggiungi la configurazione di Celery:

metaKeys/celery.py
Crea il file celery.py nella directory metaKeys:

metaKeys/__init__.py
Assicurati che Celery venga caricato quando Django avvia:

4. Definisci il task Celery
users/tasks.py
Aggiungi il task condiviso per eliminare i dati di check-in scaduti:

5. Avvia Celery
Avvia il worker Celery
Apri un terminale e avvia il worker Celery:

Avvia il beat scheduler di Celery
Apri un altro terminale e avvia il beat scheduler di Celery:

6. Verifica il funzionamento del task
Controlla i log nel terminale dove hai avviato il worker Celery per vedere se il task delete_expired_checkin_data viene eseguito correttamente ogni notte alle 3:00.

Esecuzione manuale del task
Per eseguire il task manualmente e verificare la cancellazione, puoi utilizzare la shell di Django:

Nella shell di Django, esegui il task:

Controlla i log di Celery per confermare che il task sia stato eseguito correttamente e verifica il database e il filesystem per assicurarti che i dati siano stati cancellati come previsto.

Fermare Celery e Redis
Fermare il worker Celery
Premi Ctrl + C nel terminale dove il worker Celery è in esecuzione.

Fermare il beat scheduler di Celery
Premi Ctrl + C nel terminale dove il beat scheduler di Celery è in esecuzione.

Fermare Redis
Su macOS con Homebrew
Su Ubuntu con systemd
sudo systemctl stop redis
Seguendo questi passaggi, dovresti essere in grado di configurare e far funzionare il task Celery per eseguire ogni notte alle 3:00 nel tuo progetto Django.