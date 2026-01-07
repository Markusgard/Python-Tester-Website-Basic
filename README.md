This is an old project from 2 years ago. but its a fun one.

# Applikasjonbeskrivelse


### Funksjoner av applikasjonen opplistet
* Logg inn
* Passord krav
* Lage bruker
* slette bruker
* legge til poeng
* admin roller
* søk og sortering
* lagring med cookies
* ajax søking
* dynamisk jnja loop i html
* flex box og absolut
* fluid mellom pc modus og mobil modus
* Access control: Kun Admin kan slette andre brukere.
* spill


### Instruksjoner for testing

login:

* brukernavn:Admin
* passord:123

* brukernavn:Bruker
* passord:123

(Vanligvis ville ikke 123 være godkjent som passord. men for testing gjør dette det enklere for dere.)

Logg inn på Admin for å teste hvordan man kan slette brukere. Både Bruker og Admin kan spille og få poeng. Hvis en ikke er intressert i de to første oppgavene kan man bare ta Sample spillet hvor svaret er bare `return ""`. Brukere kan slette sin egen bruker hvis de vil. Brukere kan ikke slette andre brukere.

### Hvordan man kjører nettsiden

Vår nettside er et spill hvor brukere kan konkurrere sine kode-ferdigheter i Python. Spillet består av en "case" hver bruker får, som de skal løse med koding. Hver case har en tilsvarende datasett som brukeren skal ta utgangspunkt fra.
I tillegg til spillet har vi lagt inn et leaderboard av brukerene på applikasjonen. Leaderboardet endrer seg automatisk når en bruker fullfører et spill eller når en ny bruker blir opprettet.
Fremsiden består av en liste med utvalgte cases brukere kan velge mellom, i tillegg til topp-3 spillere.
Hver side har felles navigasjons-ramme.

## main og login

Vi brukte jinja for å vise fram login page eller game page bassert på om brukeren er logget inn. Vi brukte jinja og for å loope igjennom json filene for å finne alle caser, case description, og topp 3 på leaderboard. Vi har brukt bootstrap for å få til looken av nettsiden. Hvis man klikker på logut eller slett bruker vil det dukke opp en modal som spør om man er sikker. 

på login page brukte vi en form submit for å sende inn passord  og brukernavn til flask for en sjekk om det er riktig. etterpå brukte vi session for å gi brukeren rollen og logge de inn på nettsiden. Hvis man klikker på create account blir man sendt til en ny side.

## Create account

Her kan man lage en bruker. det er plassert restriksjoner på passord og vi bruker ajax for å sjekke om brukernavnet er i bruk. Etter man har registert seg får man utdelt rolle og leaderboard plass. 

## leaderboard

Vi brukte ajax for å få en søke funksjon og filteringsfunksjon. Her kan man se poeng summen av alle spillere, hva datoen var sist de spilte, og hvilken rank de har. Den med flest poeng er på toppen. Hvis man har rollen Admin vil det dukke opp en slette knapp bak hver bruker og man kan endre poengsummen til alle brukere. etter man har gjort en av delene vil siden laste inn på nytt og sortere alle spillere på nytt. Det er satt inn en role validation for å sjekke at personen som sletter brukerene er en Admin. Cookies vil lagre hva man har søkt på og hvilken av filterene man brukte sist.

## error_handling

dette er en exception redirect handler. altså her kommer server request errors eller validation errors. 

## SPILLSIDEN

Spillsiden har url-en `localhost/gamepage`. Nye brukere får opp et vindu som viser hvordan spillet fungerer og hva regler de må følge, brukeren har mulighet til å klikke på `do no show again` som lagrer en boolsk verdi i en cookie. Cookien passer på at vinduet ikke vises igjen, men brukeren har fortsatt mulighet til å få opp vinduet igjen.

Hver gang et nytt spill starter får brukeren se og lese sin case. Spillet starter ikke før brukeren klikker `start`.

Når spillet har startet starter en tidtaker, og spillet teller opp hvor mange feilmedlinger og feilsvar brukeren får, som vil påvirke poengsummen.

### Kjøring av brukerens kode

Spillsiden har en innebygd Python-ramme som brukeren skriver koden sin i, med en tilsvarende konsoll som viser hva verdier brukerens kode returnerer.

For at Python-koden skal kjøre vil brukerens kode bli sendt til en `localhost/runcode` rute med AJAX i POST modus. Funksjonen i ruten skal undersøke om brukeren har forsøkt å hente inn nye moduler, eller bruk av `open()` kommandoen, som ikke er tillatt. Når de restriksjonene er godkjente vil funksjonen opprette en ny `.py` fil med brukerens navn som inneholder koden. Denne filen inneholder en import av `math` modulen (den eneste modulen vi tillater), og en erklæring av funksjonen `usercode()` som inneholder coden til brukeren. Rute-funksjonen vil først undersøke om koden foråsaker en uendelig løkke ved å sjekke om koden fullføres innen 5 sekund, tar koden mer enn 5 sekund vil funksjonen stoppe og `bruker.py` filen slettes. Dersom funksjonen bruker mindre enn 5 sekund, vil resultatet til funksjonen sammenlignes med det tilsvarende svaret. Dersom svaret stemmer, vil rute-funksjonen returnere en streng med format `XX> melding`. Det første tallet `X` bestemmer hva type melding det er (kodesvar, advarsel, feilmelding). Det andre tallet `X` bestemmer om brukeren har fått rett svar eller ikke. Meldingen vises i konsollen. Pythonfilen `bruker.py` blir slettet med en gang det er ferdig å kjøre.

### Poengsystemet

Poengsystemet bestemmes av hvor lang tid brukeren har tatt. Denne verdien starter på 100, og har en logaritmisk nedgang dess mer tid brukeren tar. Hvert minutt teller som poeng, og hvis brukeren tar mer enn 60 minutt vil tid-poengsummen bli låst på 1 poeng. Brukeren får poeng for hvor mange forsøk han/hun har brukt, som starter på 50 poeng, og har en lineær nedgang for hvert forsøk. forsøk-poengsummen blir låst på 1 poeng. Den totale poengsummen trekkes fra hvor mange feilmeldinger brukeren får, -1 poeng for hver feilmelding. feilmelding-poengsummen blir låst på det negative av den totale poengsummen, som vil si at brukeren ikke kan få mindre enn 0 poeng.

## DATABASE

`cases.json`

Denne databasen inneholder alle oppgavene. Det består av et objekt med en "case-ID" som nøkkel. Hver "case-ID" er et nytt objekt med nøkler "title": Tittel for oppgaven, "description": Beskrivelse av oppgaven, "tiny_desc": Kort beskrivelse for fremsiden, "dataset": Tilsvarende datasett, "result": Tilsvarende resultat som sammenlignes med brukerens resultat.

`leaderboard.json`

Denne databasen innerholder brukere. Vi burde hatt kalt den for bruker.json, beklager for det. Inni finner vi at vær bruker har en user_ID. det er og lagret brukernavn, dato (sist de spillet), role, placement, points og passord som er hashet. 
