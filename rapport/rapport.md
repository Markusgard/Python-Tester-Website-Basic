<<< Rapport/Planlegging >>>

Vår applikasjon skal være et spill som handler om å skrive en Python kode for å løse en gitt "case" med tilsvarende datasett.

Nettsiden består av flere routes.
- Forsiden består av et sorterbar leaderboard av flere brukere.
- Forsiden omdirigerer brukeren til en login/registrering-side.
- Forsiden omdirigerer brukeren også til et "nytt spill"-side som inneholder selve spillet.

<< Spillsiden >>

Siden består av en <textfield> element hvor brukeren har mulighet til å skrive inn sin kode, med en tilsvarende "kjør kode" knapp.
Poengsummen avhenger av hvor mange linjer brukeren skriver, og hvor mange forsøk har blitt brukt.
Når brukeren kjører sin kode vil kodestrengen bli overført til en route i Flask-applikasjonen med AJAX. Denne routen vil da opprette en separat python fil som inneholder brukerens kode, og kjører den som en importert funksjon. I virkeligheten ville flere brukere kjøre koden sin samtidig, så vi velger å navnsette python-filen til brukernavnet, slik at det ikke oppstår konflikter.
Dette betyr at brukerens kode kjører fullstendig back-end, som gir enorme sikkerhetssvakheter på serverens side:
- Brukeren har full tilgang til pythons moduler, som inneholder mange sårbare funksjoner. Vi løser denne svakheten ved å "whiteliste" enkelte moduler gjennom inspeksjon av brukerens kodestreng før den blir opplastet til python filen.
- Brukeren har også tilgang til å endre på systemfiler gjennom pythons "open" funksjon. Vi kan løse det ved å bannlyse bruken av "open" ved inspeksjon av kodestrengen.
- Dersom brukerens kode resulterer i en uendelig while-funksjon vil dette svekke applikasjonens funksjonalitet og serverens ytelse, på samme måte er serveren sårbar mot DoS angrep. Vi har ikke funnet en løsning for dette enda.
- Ytelsen på servermaskinen vil også svekkes ved vanlig bruk. Python er et tungt program, og hvis denne applikasjonen var ekte hadde sannsynlig vis flere tusen brukere brukt den samtidig, som servermaskinen kanskje ikke ville takle.

Sikkerhetsmessig er dette en svært tvilsom løsning for python-delen av applikasjonen, men vi velger å gå for denne løsningen siden dette ikke er et sikkerhetsorientert fag. I tilfelle vi må forlate denne ideen har vi en backup-løsning for spillsiden.

<< Spillsiden (Backup) >>

I stedet for å ha en innebygd python-interpreter velger vi å gå for en slags "quiz" løsning som består av en serie med flervalg-spørsmål.
