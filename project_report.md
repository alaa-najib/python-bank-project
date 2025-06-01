# 📄 Individuell Projektrapport - Bankdataflöde och Automatiserad Datakvalitet

## 🔧 Teknisk Översikt

I detta projekt har jag implementerat ett fullständigt arbetsflöde för hantering och kvalitetssäkring av banktransaktioner med hjälp av Python, PostgreSQL, SQLAlchemy, Alembic och Prefect. Målet har varit att ta emot transaktionsdata i CSV-format, validera dessa, lagra godkända poster i databasen, avvisa ogiltiga, och logga alla steg systematiskt.

---

## 📦 Databashantering med PostgreSQL och SQLAlchemy

Vi skapade en PostgreSQL-databas kallad `bank`. Därefter designades och skapades tabellerna:

- `customers`
- `accounts`
- `transactions`
- `invalid_transactions`
- `logs`

Varje tabell skapades som SQLAlchemy-modeller i Python. Tabellerna kopplades ihop via främmande nycklar, till exempel `sender_account` och `receiver_account` i `transactions` som pekar på `accounts`.

---

## 🛠 Alembic-migreringar

För att versionshantera och applicera ändringar på databasen användes Alembic. Vi initierade Alembic, skapade revisionsfiler och autogenererade schemat från modellerna. Med kommandot `alembic upgrade head` applicerades hela databasschemat.

---

## 📥 Datainläsning och Städning

- `customers.csv` laddades och sparades till databasen via Pandas och SQLAlchemy.
- `transactions.csv` lästes in, och unika konton extraherades automatiskt till `accounts`.
- Alla transaktioner validerades radvis för format, datatyper och obligatoriska fält.

Ogiltiga rader sparades i `invalid_transactions`-tabellen med originaldata som JSON och felbeskrivning.

---

## 🧹 Datavalidering

Valideringen kontrollerade:
- Att fält som `transaction_id`, `timestamp`, `amount`, `currency`, `sender_account` och `receiver_account` inte var tomma
- Datumformat med `pd.to_datetime`
- Numeriska belopp via `float()`

Valideringslogik flyttades till en egen modul (`validate_transactions.py`) för att möjliggöra återanvändning och testning.

---

## 📁 README-dokumentation

Två README-filer togs fram:

1. **Teknisk README** som förklarar tabellstruktur, valideringsstrategier och systemdesign
2. **Sammanfattad README** som listar verktyg, flöden och hur man kör projektet

---

## 🔄 Workflow Automation med Prefect

Vi byggde ett fullständigt arbetsflöde med **Prefect** i `pipeline.py`. Det hanterar följande:

1. Laddar kunddata
2. Laddar och förbereder transaktioner
3. Extraherar unika konton
4. Validerar varje rad
5. Lagrar godkända i `transactions`
6. Lagrar felaktiga i `invalid_transactions`
7. Loggar alla steg i `logs`
8. Skriver ut en slutrapport

Prefect gjorde det enkelt att övervaka och felsöka arbetsflödet samt att modulera stegen tydligt.

---

## 🤔 Reflektion

Projektet gav mig djupare förståelse för hur automatiserade dataflöden fungerar i praktiken. Jag fick erfarenhet av att hantera verkliga datakvalitetsproblem, bygga felresistenta pipelines, och använda moderna verktyg som Prefect och Alembic. Den modulära koden, tydliga loggningen och databasens struktur gör lösningen lätt att underhålla och vidareutveckla.

---