# Susiturkki

Maastohiihdon kilometrimittari. Selainkäyttöliittymä ja rajapinta tulevat samasta kontista. Tekstit ovat suomeksi.

Tarvitset nämä ympäristömuuttujat tiedostossa `backend/.env`:

- `ADMIN_PASSWORD` on pääkäyttäjän salasana
- `SESSION_SECRET` on evästeen allekirjoitusavain
- `SESSION_HTTPS` on `true` tai `false`. Arvo `true` merkitsee istuntoevästeen vain HTTPS-yhteydelle.
- `API_PUBLISH` on julkaisuosoite muodossa `isäntä:portti:kontinportti`
- `LISTEN_HOST` on osoite, jota prosessi kuuntelee kontin sisällä. Julkaistu portti tavoittaa prosessin, kun kuuntelu kattaa kontin verkkoliitännät (`0.0.0.0`).
- `LISTEN_PORT` on kontin kuunteluportti. Sen on oltava sama kuin `API_PUBLISH`-arvon viimeinen osa.
- `FORWARDED_ALLOW_IPS` on pilkulla erotettu lista osoitteita, joilta `X-Forwarded-Proto` uskotaan. Tyhjä arvo ei usko otsikkoa.
- `SSL_CERT_FILE` ja `SSL_KEY_FILE` ovat absoluuttisia varmennepolkuja. Molemmat yhdessä kytkevät TLS:n kontissa. Jos kumpaakaan ei ole, kontti kuuntelee salaamatonta yhteyttä.

Kehityksessä tiedosto `frontend/.env` sisältää muuttujan `API_ORIGIN`. Se on rajapinnan osoite, ja skeema saa olla `http` tai `https`.

## Docker

Siirry hakemistoon `backend` ja tee salaisuudet tiedostoon `.env`. Tiedostoa ei tallenneta git-repositorioon. Täydennä osoitteet ja `SESSION_HTTPS` samaan tiedostoon.

```bash
cd backend
printf 'ADMIN_PASSWORD=%s\nSESSION_SECRET=%s\nSESSION_HTTPS=\nAPI_PUBLISH=\nLISTEN_HOST=\nLISTEN_PORT=\nFORWARDED_ALLOW_IPS=\n' "$(openssl rand -base64 24)" "$(openssl rand -hex 32)" > .env
docker compose up --build
```

Kontti ei pyöri pääkäyttäjänä, sen juuritiedostojärjestelmä on kirjoitussuojattu, ja tietokanta on erillisessä volumessa `susiturkki-data`. Varmennetta ei kopioida kuvaan: polut mountataan vain-lukuisina, jos ne on asetettu.

Kontti sammutetaan komennolla `docker compose down`. Komento ei poista tietokantaa. Jos käynnistys ilmoittaa, ettei tietokantaan voi kirjoittaa, vanha volume on jäänyt pääkäyttäjän omistukseen. `docker compose down -v` poistaa sen ja samalla tallennetut kirjaukset.

## Kehitys ilman Dockeria

Tarvitset Python 3.12:n tai uudemman sekä Node.js:n.

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
export ADMIN_PASSWORD=vaihda-tama
export SESSION_SECRET=vaihda-tama-kin
export SESSION_HTTPS=false
export LISTEN_HOST=
export LISTEN_PORT=
python -m susiturkki.infrastructure.serve
```

Toisessa ikkunassa:

```bash
cd frontend
printf 'API_ORIGIN=\n' > .env
npm install
npm run dev
```

Täydennä `API_ORIGIN` ennen `npm run dev`. Selain kutsuu suhteellista polkua `/api`, ja Vite välittää kutsut `API_ORIGIN`-osoitteeseen.

Tietokanta syntyy tiedostoon `backend/susiturkki.db`. Polun voi vaihtaa muuttujalla `DATABASE_PATH`.

## Testit

Testit ajetaan hakemistosta `backend`. Ne käyttävät muistissa olevaa tietokantaa, joten ympäristömuuttujia ei tarvita.

```bash
cd backend
source .venv/bin/activate
pytest
```
