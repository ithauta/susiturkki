# Susiturkki

Susiturkki on maastohiihdon kilometrimittari. Osallistujat kirjaavat hiihtokilometrejä ryhmäänsä, ja ryhmän kertymät näkyvät muille saman ryhmän jäsenille.

## Käyttäjät ja pääsy

Osallistuja ei ole erillinen käyttäjätili. Pääkäyttäjä lisää henkilön ryhmään ja antaa etunimen ja sukunimen. Sukunimi saa olla tyhjä. Osallistuja ei voi vaihtaa nimeään. Henkilöllä on yksi yksityinen linkki. Hän kirjaa kilometrit kerran, ja sama kirjaus kertyy jokaiseen ryhmään, johon hän kuuluu. Linkki näyttää kaikkien hänen ryhmiensä kertymät.

Sama ihminen voi kuulua useaan ryhmään. Nimi ja linkki ovat yhteiset. Pääkäyttäjä voi liittää olemassa olevan henkilön toiseen ryhmään.

Pääkäyttäjä on yksi koko sovellukselle, ja hän kirjautuu salasanalla. Hän hallitsee kaikkia ryhmiä: lisää, muokkaa ja poistaa osallistujia sekä kirjauksia milloin tahansa, ja voi uusia yksityisen linkin. Uusiminen mitätöi vanhan linkin kaikissa ryhmissä.

## Ryhmät

Pääkäyttäjä luo ryhmän ja lisää siihen osallistujat. Osallistuja on aina jonkin ryhmän jäsen, koska hänet luodaan ryhmään.

Osallistujan poistaminen ryhmästä poistaa vain sen jäsenyyden. Jos hän kuuluu vielä toiseen ryhmään, kirjaukset säilyvät ja näkyvät siellä. Viimeisen ryhmän poistaminen hävittää henkilön, linkin ja kirjaukset.

Ryhmän voi poistaa vain, kun siinä ei ole osallistujia. Jäsenet poistetaan ensin.

## Omat tiedot

Osallistuja ylläpitää omia tietojaan Tiedot-välilehdellä. Ne ovat henkilökohtaisia ja yhteisiä kaikkiin hänen ryhmiinsä. Ne eivät näy ryhmän tilanteessa eivätkä pääkäyttäjälle.

Syntymävuosi on valinnainen. Sallittu väli on 1900–kuluva vuosi.

Kauden tavoitekilometrit ovat valinnaiset. Jos ne on asetettu, tavoitepäivä on pakollinen ja sen on osuttava saman kauden sisään. Kilometrejä voi asettaa, muuttaa tai tyhjentää 1.10.–31.12. Sen jälkeen kilometrikenttä on lukittu, mutta päivää voi yhä muuttaa. Touko–syyskuussa lomake käsittelee seuraavaa kautta.

Kun kausi päättyy, edellisen kauden tavoite siirtyy seuraavalle: kilometrit säilyvät ja päivä siirtyy vuodella eteenpäin. Karkauspäivä siirtyy helmikuun 28. päivälle. Tyhjäksi tallennettu kausi ei siirry.

Jos osallistuja kirjaa tai muokkaa kirjausta käynnissä olevalla kaudella tavoitepäivän jälkeiseen ajankohtaan, tavoitepäiväksi tulee sen kauden viimeisimmän kirjauksen päivä. Pääkäyttäjän kirjaus ei siirrä päivää, eikä poisto palauta vanhaa päivää.

## Kilometrikirjaus

Kirjauksessa on viisi kenttää:

- **Ajankohta** (pakollinen). Päivämäärä ja kellonaika. Oletus on kirjaushetki. Aikavyöhyke on Europe/Helsinki.
- **Pituus** (pakollinen). Kilometrit yhden desimaalin tarkkuudella, esimerkiksi 10,1. Luvun on oltava positiivinen.
- **Paikka** (valinnainen). Suorituspaikka, esimerkiksi "Sievin valaistulatu". Uusi paikka tallennetaan ja näytetään myöhemmin pikavalintana. Pikavalinnoissa ovat paikat kaikista ryhmistä, joihin henkilö kuuluu, myös muiden jäsenten paikat niissä. Oletuksena on tämän henkilön edellinen paikka.
- **Tyyli** (valinnainen valinta, aina tallessa). Vapaa, perinteinen tai umpihanki. Oletus on vapaa.
- **Keli** (valinnainen valinta, aina tallessa). Luikas, normaali tai raskas. Oletus on normaali.

Osallistuja voi asettaa suoritusajankohdan enintään 14 vuorokautta menneisyyteen nykyhetkestä. Tulevaa aikaa ei sallita. Suorituspäivän on lisäksi osuttava hiihtokaudelle (1.10.–30.4.). Osallistuja ei siis käytännössä kirjaa aiemmalle kaudelle.

Osallistuja voi muokata ja poistaa omaa kirjaustaan 7 vuorokautta kirjaamishetkestä. Muokatessa suoritusajankohdan on yhä oltava enintään 14 vuorokautta nykyhetkestä menneisyyteen, ei tulevaisuudessa, ja kauden sisällä.

Kauden ulkopuolella uutta kirjausta ei voi tehdä. Seitsemän vuorokauden muokkaus- ja poistoikkuna toimii silti.

Pääkäyttäjää kumpikaan aikaraja ei koske. Hän voi kirjata ja muokata mille tahansa kauden päivälle menneisyydessä.

## Tilastot ja näkyvyys

Hiihtokausi on 1.10.–30.4. Kausi 2025–2026 on siis 1.10.2025–30.4.2026. Viikko alkaa maanantaista. Kuukausi- ja viikkorajat lasketaan aikavyöhykkeellä Europe/Helsinki.

Osallistuja näkee kaikki omat kirjauksensa. Muista ryhmän jäsenistä hän näkee kausi-, kuukausi- ja viikkokertymät rinnakkain sekä viisi tuoreinta kirjausta per jäsen. Tuoreessa listassa näkyvät päivä, kilometrit, paikka, tyyli ja keli. Tuoreus määräytyy suoritusajankohdan mukaan koko historiasta, ei siitä kaudesta, jota tilastoissa katsotaan.

Valitulta kaudelta näytetään kauden, kuukausien ja viikkojen kertymät. Aiempaan kauteen voi vaihtaa. Kauden ulkopuolella sovellus on katselutilassa: oletuksena näytetään viimeksi päättynyt kausi, vanhat tilastot ja kirjaukset näkyvät, eikä uutta kirjausta voi lisätä.

Pääkäyttäjä näkee kaikkien ryhmien kirjaukset kokonaan, ei vain viittä tuoreinta.

## Tekninen toteutus

Arkkitehtuuri noudattaa clean architecture -periaatetta. Toteutus on Python, FastAPI ja SQLite. Tietokantakerros on rajapinnan takana, jotta SQLite voidaan vaihtaa tarvittaessa.

Sovellus pyörii yhdessä Docker-kontissa. SQLite-tiedosto säilyy kontin uudelleenkäynnistyksen yli.

Selainkäyttöliittymä toimii kännykällä, käyttää modernia CSS:ää ja talviteemaa, ja on suomeksi. Käyttöliittymän tekstit ovat erillisessä kielitiedostossa, jotta kieli on helppo vaihtaa.
