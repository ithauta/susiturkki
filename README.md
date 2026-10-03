# Susiturkki

Maastohiihdon kilometrimittarin backend. Selainkäyttöliittymä ei ole vielä mukana. Rajapinta vastaa osoitteessa `http://localhost:8000`.

Tarvitset kaksi ympäristömuuttujaa:

- `ADMIN_PASSWORD` on pääkäyttäjän salasana
- `SESSION_SECRET` on evästeen allekirjoitusavain

## Docker

Siirry hakemistoon `backend` ja tee salaisuudet tiedostoon `.env`. Tiedostoa ei tallenneta git-repositorioon.

```bash
cd backend
printf 'ADMIN_PASSWORD=%s\nSESSION_SECRET=%s\n' "$(openssl rand -base64 24)" "$(openssl rand -hex 32)" > .env
docker compose up --build
```

Rajapinta vastaa vain tässä koneessa, osoitteessa `http://127.0.0.1:8000`. Kontti ei pyöri pääkäyttäjänä, sen juuritiedostojärjestelmä on kirjoitussuojattu, ja tietokanta on erillisessä volumessa `susiturkki-data`.

Kontti sammutetaan komennolla `docker compose down`. Komento ei poista tietokantaa. Jos käynnistys ilmoittaa, ettei tietokantaan voi kirjoittaa, vanha volume on jäänyt pääkäyttäjän omistukseen. `docker compose down -v` poistaa sen ja samalla tallennetut kirjaukset.

## Backend ilman Dockeria

Tarvitset Python 3.12:n tai uudemman.

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
export ADMIN_PASSWORD=vaihda-tama
export SESSION_SECRET=vaihda-tama-kin
uvicorn susiturkki.api.main:app --reload --app-dir src
```

Tietokanta syntyy tiedostoon `backend/susiturkki.db`. Polun voi vaihtaa muuttujalla `DATABASE_PATH`.

## Testit

Testit ajetaan hakemistosta `backend`. Ne käyttävät muistissa olevaa tietokantaa, joten ympäristömuuttujia ei tarvita.

```bash
cd backend
source .venv/bin/activate
pytest
```
