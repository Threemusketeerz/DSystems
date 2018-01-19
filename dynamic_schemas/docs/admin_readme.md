### Hvordan bruger man sitet som admin?

Når du logger ind på sitet vil alt være som alle andres. Men med en forskel. Du kommer til at have adgang til admin-sitet.

- For at få adgang til admin-sitet, er der tilføjet et link på selve dit brugernavn i top-baren (nav-baren).**Hvis du trykker på admin, vil du blive ledt videre til sitet.**

- Når du er inde på sitet skulle du gerne blive mødt af en skærm der beskriver Brugere og længere nede **rengøring**

- For at ændre noget med instruktioner, gå ind i **Schema help urls** herinde skaber du en url (bdkls links, giver den et navn, og en kort beskrivelse. Hvis du laver en ny vil den ikke være tilknyttet noget som helt endnu.

- Under **Schemas** vil du sjovt nok finde skemaerne. De er de entiteter hele systemet er bygget op omkring, vær forsigtig når du håndterer disse, da bare en lille fejl kan slette et helt sæt data.

- Hvis du går ind på et skema, eller laver en ny skema, vil du blive mødt af mindre smøre af felter. FRYGT EJ. Felter vil være beskrevet herunder i en rækkefølge top til bund.


### Skema/Tabel
  - **Navn:** Navnet på skemaet.
  - Instruktions felt: Herinde vælger du alle de links skemaet ønsker sig. **Vær opmærksom på at tabellen ikke kan blive indtastet på hvis ikke der er en instruktion til indtastningen.**
  - Aktiv: Hvis skemaet skal være tilgængelig igennem front-end skal den også være aktiv.  Foreløbigt er der ikke nogen direkte måde at 'preview' en tabel der ikke er aktiv, men er en planlagt funktionalitet. 
  - **Udgået:** Når tabellerne udgår bliver dette felt slået til. Det eneste den gør er at tilføje en dato til tabellen, hvis man fravælger feltet vil det blive fjernet. 
  - **Lås:** For at sikre at en tabel forbliver det man originalt satte den som er der blevet lavet en låse funktionalitet.  
For ikke at ødelægge den måde dataen bliver vist på front-endpointed.  
Hvis man ønsker sig en ny kolonne, eller ændringer til en kolonne bliver man nød til at lave en ny tabel, og sætte denne som udgået.  
Det eneste der sker er at hvis tabellen er låst, kan ændringer hos kolonner ikke gemmes. Dette betyder at du kan ændre de øverste indstillinger lige så tosset som du vil.


### Skema/tabel kolonner/columns:
  - **Text:** Kolonne navn.
  - **Ja/Nej Spørgsmål**: Hvis den bliver tikket af, vil kolonnen give et **dropdown** felt til brugeren når en ny indtastning skal finde sted.
  - Felt kan ændres: En bedre formulering havde nok været 'Kan opdateres'. Hvis den er givet, kan brugeren efterlade feltet tomt, og på et senere tidspunkt opdatere rækken.


### SchemaHistoryLogs
Her kræver det sådan set at det gamle skema er sat som udgået, og det nye skema er lavet.

  - **Gammelt shema**: Den her viser kun udgåede skemaer,  så for at kunne lave en historik skal de skemaer der ønskes logget, være Udgåede først. 
  - **Nyt skema**: Det er det nye skema der erstatter det gamle skema. 
