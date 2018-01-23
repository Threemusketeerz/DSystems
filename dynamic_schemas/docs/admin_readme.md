### Hvordan bruger man sitet som admin?

Når du logger ind på sitet vil alt være som alle andres. Men med en forskel. Du kommer til at have adgang til admin-sitet.

- For at få adgang til admin-sitet, er der tilføjet et link på selve dit brugernavn i top-baren (nav-baren). **Hvis du trykker på admin, vil du blive ledt videre til sitet.**

- Når du er inde på sitet skulle du gerne blive mødt af en skærm der beskriver Brugere og længere nede **rengøring**

- For at ændre noget med instruktioner, gå ind i **Instruktioner** herinde skaber du en url (bdkls links, giver den et navn, og en kort beskrivelse). Hvis du laver en ny vil den ikke være tilknyttet noget som helt endnu.

- Under **Skemaer** vil du sjovt nok finde skemaerne. De er de entiteter hele systemet er bygget op omkring, vær forsigtig når du håndterer disse, da bare en lille fejl kan slette et helt sæt data.

- Hvis du går ind på et skema, eller laver en ny skema, vil du blive mødt af mindre smøre af felter. FRYGT EJ. Felter vil være beskrevet herunder i en rækkefølge top til bund.


### Skema
  - **Navn:** Navnet på skemaet.
  - **Instruktions felt**: Herinde vælger du alle de links skemaet ønsker sig. **Vær opmærksom på at tabellen ikke kan blive indtastet på hvis ikke der er en instruktion til indtastningen.**
  - **Aktiv**: Hvis skemaet skal være tilgængelig igennem front-end skal den også være aktiv.  Foreløbigt er der ikke nogen direkte måde at 'preview' en tabel der ikke er aktiv, men er en planlagt funktionalitet. 
  - **Udgået:** Når tabellerne udgår bliver dette felt slået til. Det eneste den gør er at tilføje en dato til tabellen, hvis man fravælger feltet vil det blive fjernet. 
  - **Lås:** For at sikre at en tabel forbliver det man originalt satte den som er der blevet lavet en låse funktionalitet.  
For ikke at ødelægge den måde dataen bliver vist på front-endpointed.  
Hvis man ønsker sig en ny kolonne, eller ændringer til en kolonne bliver man nød til at lave en ny tabel, og sætte denne som udgået.  
Det eneste der sker er at hvis tabellen er låst, kan ændringer hos kolonner ikke gemmes. Dette betyder at du kan ændre de øverste indstillinger lige så tosset som du vil.


### Skema kolonner/columns:
  - **Text:** Kolonne navn.
  - **Ja/Nej Spørgsmål**: Hvis den bliver tikket af, vil kolonnen give et **dropdown** felt til brugeren når en ny indtastning skal finde sted.
  - Felt kan ændres: En bedre formulering havde nok været 'Kan opdateres'. Hvis den er givet, kan brugeren efterlade feltet tomt, og på et senere tidspunkt opdatere rækken.


### Skema historik
Her kræver det sådan set at det gamle skema er sat som udgået, og det nye skema er lavet.

  - **Gammelt shema**: Den her viser kun udgåede skemaer,  så for at kunne lave en historik skal de skemaer der ønskes logget, være Udgåede først. 
  - **Nyt skema**: Det er det nye skema der erstatter det gamle skema. 


### Hvad ville et normalt workflow være?
Her vil jeg prøve at forklare så godt som muligt hvordan man ville bruge de funktionaliteter der i skemasystemet. 
Jeg starter fra start til slut af et skemas levetid.

**Skema kreation**:
    1. Udfyld Skema felter (du kan lave instruktioner fra denne side) 
    2. Lav kolonner 
    3. Sæt skema som aktivt 
    4. Lav evt. en test indtastning, for at se om tabellen viser det den skal 
    5. Vent evt. på at tabellen bliver brugt. Hvis kravene er opfyld, lås tabellen. Sæt dig tilbage og drik en kop kaffe.

**Skema skal skiftes ud med nyt skema**:
    1. Find det skema i admin panelet der skal skiftes ud. 
    2. Markér udgået -> tryk på gem
    3. Sørg for at 'aktiv' boksen er trykket af (vi vil ikke længere have den vist i menuen).
    4. Gå nu ind i Skema Historik modulet, og lav en ny indtastning.
    5. Du bliver mødt af to dropdown menuer, den ene indeholder udgåede skemaer og den anden indeholder skemaer der ikke er udgåede. -> Vælg det udgåede skema i den første dropdown, herefter vælg det skema den bliver erstattet med i den anden dropdown. -> tryk på Save.
    6. Hvis du har lavet den nye skema ifølge Skema Kreation instruktionerne, vil det nye skema blive vist i menuen på front-end og referere tilbage til det gamle skema.

