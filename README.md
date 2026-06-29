secondo parziale PPM - Micol Serri, 7111594 - Polling Application API

specifiche progetto: REST API, DJANGO & DJANGO REST FRAMEWORK (DRF)

descrizione: una REST API per la creazione, gestione e votazione di sondaggi. Permette ai client di consumare endpoint per elencare i sondaggi attivi, votare le singole opzioni e visualizzare i risultati aggregati in tempo reale. Include un sistema di autenticazione basato su Token e una logica di permessi personalizzata per proteggere le operazioni di modifica e cancellazione.

funzionalità per user role:
Anonymous:
Lettura(GET) di lista polls ordinati per id e relative choices anch'esse ordinate per id
Visualizzazione(GET) risultati voti in tempo reale per ogni poll tramite Results

Authenticated User:
Creazione (POST) nuovi polls (diventanto owner, quindi con unica key per modificarli(PATCH) o cancellarli(DELETE))
votare (POST) tramite Vote su una specifica opzione di un poll

ADMIN/owner di singolo poll:
Modifica totale o parziale (PUT/PATCH) del testo del sondaggio da lui creato
Eliminazione (DELETE) del sondaggio da lui creato
Apertura/Chiusura (POST) del sondaggio per bloccare o sbloccare le votazioni

endpoint table:
| Metodo | URL | Autenticazione | Ruolo | Body Richiesta (JSON) | Descrizione |

| POST | `/api/login/` | No | Qualsiasi | `{"username"= "...", "password"= "..."}` | login, scambia credenziali con il token |
| POST | `/api/register/` | No | Qualsiasi | `{"username"= "...", "password"= "..."}` | registra utente e genera token |
| GET | `/api/polls/` | No | Qualsiasi | Vuoto | Elenca tutti i sondaggi disponibili |
| POST | `/api/polls/` | Sì (Token) | Autenticato | `{"question"= "..."}` | Crea un nuovo sondaggio (imposta l'owner) |
| GET | `/api/polls/<id>/` | No | Qualsiasi | Vuoto | Mostra i dettagli di un singolo sondaggio |
| POST | `/api/choices/` | Sì (Token) | Autenticato | `{"poll"= <id_sondaggio>, "choice_text"= "..."}` | Crea una nuova opzione di voto e la associa al sondaggio specificato tramite ID |
| PUT/PATCH | `/api/polls/<id>/` | Sì (Token) | Owner | `{"question"= "..."}` | Modifica un sondaggio (solo se owner) |
| DELETE | `/api/polls/<id>/` | Sì (Token) | Owner | Vuoto | Elimina un sondaggio (solo se owner) |
| GET | `/api/polls/<id>/results/` | No | Qualsiasi | Vuoto | Restituisce i risultati dei voti aggregati |
| POST | `/api/polls/<id>/vote/` | Sì (Token) | Autenticato | `{"choice_id"= id}` | Invia un voto per una opzione del sondaggio |
| POST | `/api/polls/<id>/toggle_status/` | Sì (Token) | Owner | Vuoto | Attiva/Disattiva il sondaggio (solo owner) |


esempi:
login: http POST https://serri-secondo-parziale-ppm.onrender.com/api/login/ username="admin" password="admin123"
restituisce "token": "token number"

register: http POST https://serri-secondo-parziale-ppm.onrender.com/api/register/ username="studente_test1" password="stud1123"
restituisce "message": "utente registrato!", "token": "token number"

creazione poll: http POST https://serri-secondo-parziale-ppm.onrender.com/api/polls/ question="Qual è il miglior framework per il backend?" Authorization:"Token token number"
restituisce "choices": [],
    "created_at": "tempo",
    "created_by": "profilo del token",
    "id": id dato,
    "is_active": true,
    "question": "Qual è il miglior framework per il backend?"

creazione choice: http POST https://serri-secondo-parziale-ppm.onrender.com/api/choices/ poll=id poll  choice_text="Opzione di Test" Authorization:"Token token number"  
restituisce "choice_text": "Opzione di Test",
    "id": id choice dato,
    "poll": id poll,
    "votes": 0

voto: http POST https://serri-secondo-parziale-ppm.onrender.com/api/polls/id poll/vote/ choice_id=id choice Authorization:"Token token number"
restituisce "message": "Voto registrato con successo per: 'Opzione di Test'!"

delete: http DELETE https://serri-secondo-parziale-ppm.onrender.com/api/polls/id poll/ Authorization:"Token token number"
restituisce 204 No Content
(se non è admin, e il poll non è suo, restituisce "detail": "You do not have permission to perform this action.")


URL: `https://serri-secondo-parziale-ppm.onrender.com`

guida a HTTPie (testing workflow):
assicurarsi che sia installato httpie (eventualmente: pip install httpie)

una volta che il sito è attivo su Render, su /api/ si può direttamente effettuare login fornito da DRF,
con credenziali utente_demo1 o 2 fornite in seed.json; o su /admin/ con credenziali admin.
Il browser riconosce credenziali e sblocca permessi riconosciuti, dopodichè è possibile testare comandi
incollando direttamente l'URL nella barra degli indirizzi del browser, sfruttando l'interfaccia grafica
di Django REST Framework.

Per le operazioni di scrittura che richiedono il Token (come la registrazione o login nuovi),
è necessario usare i comandi HTTPie documentati dal terminale.

CREDENZIALI GIÀ CREATE NEL SEED.JSON:
/admin/
utente: admin
password: admin123

login da /api/
utente: utente_demo1
password: utente1123

utente: utente_demo2
password: utente2123


