# Susiturkki

Susiturkki on maastohiihdon kilometrimittari. Osallistujat kirjaavat hiihtokilometrejä ryhmäänsä, ja ryhmän kertymät näkyvät muille saman ryhmän jäsenille.

## Käyttäjät ja pääsy

Osallistuja ei ole erillinen käyttäjätili. Pääkäyttäjä lisää henkilön ryhmään ja antaa nimen. Osallistuja ei voi vaihtaa nimeään. Jokaisella ryhmäjäsenyydellä on oma yksityinen linkki, jolla osallistuja kirjaa kilometrejä ja katsoo kyseisen ryhmän tietoja. Linkki avaa vain sen ryhmän.

Sama ihminen voi kuulua useaan ryhmään. Jokaisella jäsenyydellä on oma linkki ja oma nimi.

Pääkäyttäjä on yksi koko sovellukselle, ja hän kirjautuu salasanalla. Hän hallitsee kaikkia ryhmiä: lisää, muokkaa ja poistaa osallistujia sekä kirjauksia milloin tahansa, ja voi uusia yksityisen linkin. Uusiminen mitätöi vanhan linkin.

## Ryhmät

Pääkäyttäjä luo ryhmän ja lisää siihen osallistujat. Osallistuja on aina jonkin ryhmän jäsen, koska hänet luodaan ryhmään.

Osallistujan poisto hävittää hänet, hänen linkkinsä ja kaikki hänen kirjauksensa siitä ryhmästä.

Ryhmän voi poistaa vain, kun siinä ei ole osallistujia eikä kirjauksia. Jäsenet poistetaan ensin, jolloin myös heidän kirjauksensa katoavat.

## Kilometrikirjaus

Kirjauksessa on kolme kenttää:

- **Ajankohta** (pakollinen). Päivämäärä ja kellonaika. Oletus on kirjaushetki. Aikavyöhyke on Europe/Helsinki.
- **Pituus** (pakollinen). Kilometrit yhden desimaalin tarkkuudella, esimerkiksi 10,1. Luvun on oltava positiivinen.
- **Paikka** (valinnainen). Suorituspaikka, esimerkiksi "Sievin valaistulatu". Uusi paikka tallennetaan ja näytetään myöhemmin pikavalintana. Pikavalinnoissa ovat myös saman ryhmän muiden jäsenten paikat. Oletuksena on tämän osallistujan edellinen paikka samassa ryhmässä.

Osallistuja voi asettaa suoritusajankohdan enintään 14 vuorokautta menneisyyteen nykyhetkestä. Tulevaa aikaa ei sallita. Suorituspäivän on lisäksi osuttava hiihtokaudelle (1.10.–30.4.). Osallistuja ei siis käytännössä kirjaa aiemmalle kaudelle.

Osallistuja voi muokata ja poistaa omaa kirjaustaan 7 vuorokautta kirjaamishetkestä. Muokatessa suoritusajankohdan on yhä oltava enintään 14 vuorokautta nykyhetkestä menneisyyteen, ei tulevaisuudessa, ja kauden sisällä.

Kauden ulkopuolella uutta kirjausta ei voi tehdä. Seitsemän vuorokauden muokkaus- ja poistoikkuna toimii silti.

Pääkäyttäjää kumpikaan aikaraja ei koske. Hän voi kirjata ja muokata mille tahansa kauden päivälle menneisyydessä.

## Tilastot ja näkyvyys

Hiihtokausi on 1.10.–30.4. Kausi 2025–2026 on siis 1.10.2025–30.4.2026. Viikko alkaa maanantaista. Kuukausi- ja viikkorajat lasketaan aikavyöhykkeellä Europe/Helsinki.

Osallistuja näkee kaikki omat kirjauksensa. Muista ryhmän jäsenistä hän näkee kausi-, kuukausi- ja viikkokertymät rinnakkain sekä viisi tuoreinta kirjausta per jäsen. Tuoreessa listassa näkyvät päivä, kilometrit ja paikka. Tuoreus määräytyy suoritusajankohdan mukaan koko historiasta, ei siitä kaudesta, jota tilastoissa katsotaan.

Valitulta kaudelta näytetään kauden, kuukausien ja viikkojen kertymät. Aiempaan kauteen voi vaihtaa. Kauden ulkopuolella sovellus on katselutilassa: oletuksena näytetään viimeksi päättynyt kausi, vanhat tilastot ja kirjaukset näkyvät, eikä uutta kirjausta voi lisätä.

Pääkäyttäjä näkee kaikkien ryhmien kirjaukset kokonaan, ei vain viittä tuoreinta.

## Tekninen toteutus

Arkkitehtuuri noudattaa clean architecture -periaatetta. Toteutus on Python, FastAPI ja SQLite. Tietokantakerros on rajapinnan takana, jotta SQLite voidaan vaihtaa tarvittaessa.

Sovellus pyörii yhdessä Docker-kontissa. SQLite-tiedosto säilyy kontin uudelleenkäynnistyksen yli.

Selainkäyttöliittymä toimii kännykällä, käyttää modernia CSS:ää ja talviteemaa, ja on suomeksi. Käyttöliittymän tekstit ovat erillisessä kielitiedostossa, jotta kieli on helppo vaihtaa.
