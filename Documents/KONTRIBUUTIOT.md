# Kontribuutiot

Tämä osio dokumentoi projektin hakemistorakenteen ja siihen osallistuneiden henkilöiden vastuualueet. Jos joku osa-alue on kokonaan yhden henkilön tekemä, sen kansioita/tiedostoja ei tässä erikseen listata. `Eprice/Documents/` kansiosta löytyy yksityiskohtainen dokumentaatio koko projektista.

```code
|– projektinhallinta "juuren" tasolla, "full stack plus", (Paavo)
|
├── LICENSE
├── README.md
├── App
│   ├── README.md
│   ├── compose.yaml – konttien hallinta (Paavo)
│   ├── pgdata.tar.gz – tietokannan snapshot (Paavo)
│   ├── project.env – projektin ja konttien konfiguraatiot (Paavo)
│   │
│   ├── backend-tests – testauksen alustus (Paavo)
│   │   ├── Dockerfile
│   │   ├── README.md
│   │   └── tests
│   │       ├── test_auth_controller.py – (Juho & Paavo)
│   │       └── test_data_controller.py – (Juho)
│   │
│   ├── chat-engine – developer chat (Paavo)
│   │   ├── Dockerfile
│   │   ├── README.md
│   │   ├── agent_app.py
│   │   ├── agent_manager.py
│   │   ├── app.py
│   │   ├── autoloading_uml.py
│   │   ├── chat_app.py
│   │   ├── chat_manager_with_tools.py
│   │   ├── file_app.py
│   │   ├── diagrams
│   │   └── utils
│   │       ├── __init__.py
│   │       ├── db_calls.py
│   │       ├── helpers.py
│   │       └── tools.py
│   │
│   ├── client – käyttöliittymä (Paavo)
│   │   ├── Dockerfile
│   │   ├── README.md
│   │   ├── src
│   │   │   ├── app.css
│   │   │   ├── app.html
│   │   │   ├── hooks.server.js
│   │   │   ├── lib
│   │   │   │   ├── apis
│   │   │   │   │   └── data-api.js
│   │   │   │   ├── assets
│   │   │   │   │   ├── image12.jpg
│   │   │   │   │   └── image3.png
│   │   │   │   ├── components
│   │   │   │   │   ├── ChatBot.svelte
│   │   │   │   │   ├── ChatView1.svelte
│   │   │   │   │   ├── ChatView2.svelte
│   │   │   │   │   ├── ChatView3.svelte
│   │   │   │   │   ├── ChatView4.svelte
│   │   │   │   │   ├── PriceCards.svelte
│   │   │   │   │   ├── Tabs.svelte
│   │   │   │   │   └── layout
│   │   │   │   │       ├── Clock.svelte
│   │   │   │   │       ├── Footer.svelte
│   │   │   │   │       ├── Header.svelte
│   │   │   │   │       └── User.svelte
│   │   │   │   ├── states
│   │   │   │   │   ├── usePricesState.svelte.js
│   │   │   │   │   └── userState.svelte.js
│   │   │   │   └── utils
│   │   │   │       ├── clock.js
│   │   │   │       ├── date-helpers.js
│   │   │   │       └── stats-helpers.js
│   │   │   └── routes
│   │   │       ├── +layout.js
│   │   │       ├── +layout.server.js
│   │   │       ├── +layout.svelte
│   │   │       ├── +page.server.js
│   │   │       ├── +page.svelte
│   │   │       ├── api
│   │   │       │   └── devchat
│   │   │       │       └── +server.js
│   │   │       ├── auth
│   │   │       │   └── [action]
│   │   │       │       ├── +page.js
│   │   │       │       ├── +page.server.js
│   │   │       │       └── +page.svelte
│   │   │       ├── chat
│   │   │       │   ├── +page.server.js
│   │   │       │   └── +page.svelte
│   │   │       ├── epc
│   │   │       │   ├── +page.server.js
│   │   │       │   └── +page.svelte
│   │   │       ├── logout
│   │   │       │   ├── +page.js
│   │   │       │   ├── +page.server.js
│   │   │       │   └── +page.svelte
│   │   │       ├── price
│   │   │       │   ├── +page.server.js
│   │   │       │   └── +page.svelte
│   │   │       └── send
│   │   │           ├── +page.server.js
│   │   │           └── +page.svelte
│   │   └── static
│   │       └── favicon.png
│   │
│   ├── data-preparation – datan esikäsittely ja lataus (Paavo)
│   │   ├── README.md
│   │   └── scripts
│   │       ├── Dockerfile
│   │       ├── README.md
│   │       ├── clean_porssisahko.py
│   │       ├── populate_porssisahko.py
│   │       └── retrieve_porssisahko_update.sh
│   │
│   ├── database-migrations – tietokantamuutokset (Paavo & Juho)
│   │   ├── V1__users.sql
│   │   ├── V2__porssisahko.sql
│   │   ├── V3__timezone.sql
│   │   ├── V4__users_add_role.sql
│   │   ├── V5__porssisahko_load_entries.sql
│   │   ├── V6__users_add_isverified.sql
│   │   ├── V8__extension_vector.sql
│   │   ├── V9__code.sql
│   │   ├── V10__code_constraint.sql
│   │   ├── V11__documents.sql
│   │   ├── V12__files.sql
│   │   ├── V13__fingrid.sql
│   │   ├── V14__fingrid_load_entries.sql
│   │
│   ├── e2e-tests – end-to-end testit (Paavo)
│   │   ├── Dockerfile
│   │   └── tests
│   │       ├── home.spec.js
│   │       └── auth.spec.js
|   |
│   └── python-server (Juho & Paavo)
│       ├── Dockerfile
│       ├── README.md
│       ├── main.py (Juho & Paavo)
│       ├── requirements.txt
│       ├── config
│       │   ├── __init__.py
│       │   └── secrets.py
│       ├── controllers
│       │   ├── auth_controller.py (Juho & Paavo)
│       │   └── data_controller.py (Juho)
│       ├── ext_apis
│       │   └── ext_apis.py (Juho)
│       ├── models
│       │   ├── custom_exception.py (Juho)
│       │   ├── data_model.py (Juho)
│       │   └── user_model.py (Paavo)
│       ├── repositories
│       │   ├── fingrid_repository.py (Juho)
│       │   ├── porssisahko_repository.py (Paavo)
│       │   └── user_repository.py (Paavo)
│       ├── scheduled_tasks
│       │   └── porssisahko_scheduler.py (Paavo)
│       ├── services
│       │   ├── auth_service.py (Paavo)
│       │   └── data_service.py (Juho)
│       └── utils
│           ├── email_tools.py (Paavo)
│           ├── fingrid_service_tools.py (Juho)
│           ├── porssisahko_service_tools.py (Juho)
│           └── porssisahko_tools.py (Paavo)
│
└── Documents – projektin dokumentaatio
    ├── CONTRIBUTIONS.md
    ├── CONTRIBUTIONS.pdf
    ├── KONTRIBUUTIOT.md
    ├── KONTRIBUUTIOT.pdf
    ├── README.md
    ├── backend_design.md
    ├── frontend_description.md
    ├── openapi_endpoint_descriptions.md
    ├── project_description.md
    ├── project_description.pdf
    ├── project_directory_structure.txt
    ├── projektin_kuvaus.md
    ├── projektin_kuvaus.pdf
    └── diagrams
        └── sources – PlantUML-muotoiset kaaviot
            ├── authentication_call_sequence_diagram.wsd
            ├── authentication_class_diagram.wsd
            ├── authentication_use_case.wsd
            ├── data_access_call_sequence_diagram.wsd
            ├── frontend_structure.wsd
            ├── llm_retrieval.wsd
            ├── services_diagram.wsd
            ├── tool_calling.wsd
            └── use_case.wsd
```

## Notebooks hakemisto (tavallaan extraa)

Developer chatin retrieval toiminto vaatii tietyn määrän esikäsittelyä (parserointi / siivous / lataus), joka tehdään offline-tilassa skripteillä ja tiedostolla `Eprice/Notebooks/document_loading.ipynb`. Nämä perustuvat osittain Paavon (heh, siis minun) aiempiin ja rinnakkaisiin projekteihin. Kaikki ei ole vielä mukana tässä repossa, mutta tullaan julkaisemaan myöhemmin osoitteessa https://github.com/PaavoReinikka.

Projektin dokumentoinnin avuksi on koodattu myös UML-kaavioiden generointityökalu, joka käyttää PlantUML-syntaksia ja on toteutettu Pythonilla (lisätietoja Notebooks README:ssä).

## Kehittäjächat / Developer-Chat

`Eprice/App/chat-engine` kontissa ajettava developer chat käyttää OpenAI:n gpt-4o-mini -mallia, joka on käytännössä ilmainen tutkimus- ja kehityskäyttöön. Projektiin liittyy myös kokeiluja useiden avoimen lähdekoodin generatiivisten mallien kanssa (sekä chatti- että completionmalleilla), jotka julkaistaan myöhemmin osoitteessa https://github.com/PaavoReinikka.

Embeddaukseen käytetty malli on avoin malli HuggingFacesta. Sieltä löytyy useita laadukkaita vaihtoehtoja, ja hyvä aloituspiste on MTEB Leaderboard: https://huggingface.co/spaces/mteb/leaderboard.

## Dokumentaatio

Dokumentaatio on pääosin Paavo Reinikan tekemää. Juho Ahopelto dokumentoi serverin endpointit (openapi endpoints). Dokumentaation teossa on käytetty myös kielimalleja.