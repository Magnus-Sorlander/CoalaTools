# Coala Solutions – underlag för ansökan

Sammanställt 2026-10-10 från QMS (SharePoint `sites/QMS`), investeringsunderlag (sept 2026), e-post, kalender, artifacts (Coala data map, Portal Renewal Decisions, Coala Bridge Close) och coalasolutions.com. Inget är gissat; osäkra punkter är markerade **[verifiera]**.

## Bolaget

- Coala Solutions AB, org.nr 556248-3700, Bangårdsgatan 13, 753 20 Uppsala. Ägs till 100 % av Magnus Sörlander (VD, utan ersättning). Riktad nyemission om 3 MSEK vid 10 MSEK pre-money pågår, stängning hösten 2026.
- Förvärvade hela produktlinjen Coala Heart Monitor ur Coala Life AB:s konkursbo i april 2024: IP, källkod, 20+ patent, produktionsprocess, cirka 6 500 CE-märkta enheter i lager. Coala Life hade investerat över 200 MSEK i produkten.
- Team: Magnus Sörlander (VD), Wilma Hoffman (Business Development and Operations Associate, projektledare i FUSMON), Anna Smedång, Yasmina Belarbi (QA/RA-dokumentation), Johan Trumstedt (teknik). Konsulter: OrderlyPeople (CEP/CER), Mikrodust (funktionstest), Intertek (60601). Tre personer i kostnadskostymen enligt investeringsunderlaget. **[verifiera anställningsform och timkostnad per person inför budgeten]**
- Historik: forskning inledd 2004 (Cometech AB), produkt lanserad 2016 av Coala Life, FDA-clearance 2019, konkurs mars 2024, förvärv april 2024, nytt QMS och omcertifiering 2024–2026, säljstart Q4 2026.

## Produkten

- Coala Heart Monitor: handhållen klass IIa-produkt som registrerar EKG och digital auskultation av hjärt- och lungljud via patenterad piezoelektrisk ljudsensor. Elektrisk och mekanisk hjärtsignal spelas in synkront, vilket få eller inga jämförbara enheter gör. 30 sekunders registrering utan plåster, av patienten själv eller personal utan specialistutbildning, via Bluetooth till mobil. Portal för vårdgivare (coalacare.com) med analys, rapporter och journalintegration.
- Indikation: tidig upptäckt och indikation som stöd för vårdens bedömning, inte diagnos. Arytmiutredning, förmaksflimmer (P-vågs- och mönsterigenkänning), andningsfrekvens under dialog med BSI.
- Regulatoriskt: CE sedan 2016, MDR klass IIa, ISO 13485 godkänt, MDR-dokumentation godkänd av BSI, EN 60601-1 el- och EMC-tester klara (Intertek, 2026), klinisk utvärdering (CER v2 godkänd 2026-07-02, DHF-06-15), FDA-clearance 2019 (förnyelse budgeterad). Design History File med över 350 styrda dokument i eQMS. Tillverkning Innokas (Tallinn).
- Klinisk evidens: validering mot 12-avlednings-EKG för förmaksflimmer, RedHeart-studien (Karolinska, cirka 1 000 kvinnor), blindad validering av ljudkvalitet likvärdig Littmann 3200, 3 625 enheter 2017–2020 med reklamationer 0,03–0,1 % och inga allvarliga tillbud, TLV och MTP-rådet rekommenderar vid misstänkt förmaksflimmer.
- Användning: cirka 1 700 kliniker i portalen, cirka 500 vårdgivare, cirka 10 000 patienter i Europa och USA. Produktionsdatabasen innehåller 1,1 miljoner mätningar och 3,2 miljoner mätdelar (Coala data map, okt 2026).
- Plattform: AngularJS-portal, .NET 6-backend, Windows-tjänster för analys (CardioLund) och rapporter, Azure SQL och Blob. Förnyelse pågår i fyra faser (ny portal mot befintligt backend, Keycloak, ny databas, "Kangaroo"), beslutat 3 oktober 2026. Relevant för SAFDIP-kravet: en ny API-kontraktsstyrd arkitektur är under uppbyggnad och kan exponeras mot en extern plattform.
- Under utveckling: långtidslogger (14–30 dygn), AI-pipeline, HL7 FHIR-, Cambio- och Epic-integration (totalbudget 6,35 MSEK varav 2,86 MSEK avses täckas av innovationsstöd).

## Tidigare Vinnova-erfarenhet (meriter i ansökan)

- **ECG AIMO, dnr 2017-04579** (Coala Life, med Cardiolund): AI-baserad EKG-uppföljning och utfallsprediktion. Slutrapport godkänd av Vinnova januari 2020. Dokument i `ArchivefromCoalaLife/.../Vinnova projekt/`.
- **Hemsjukhusvård, Region Stockholm** (Karolinska, Södersjukhuset, Danderyd, fyra sjukhus): Vinnovafinansierat projekt där Coala Solutions är teknikleverantör, steg 3 avtalat 2024, förlängt t.o.m. september 2026, vårdgivarna fortsätter på egen kostnad. Projektledare Kristina Groth (Karolinska). Avslutningsseminarium hösten 2026. Detta är den närmaste civila motsvarigheten till "utspridd vård" och bör vara ett bärande exempel.
- **FUSMON** (Mittuniversitetet, professor Jan Lundgren, och NTNU, Nils Kristian Skjærvold och Oddvar Uleberg): sensorfusion för smartare hälsomonitorering, till 2029. Coala är industripartner, Wilma Hoffman projektledare. NDA med Miun under upprättande (oktober 2026). Datadelning pågår. Kampradstiftelsen-ansökan 2024 med Miun.
- Coala var enda medtech-bolaget i SVT-serien "Folkets AI".

## Relationer som kan bli koordinator eller part

| Aktör | Typ | Relation | Kommentar |
|---|---|---|---|
| **BizMaker** (Sundsvall/Västernorrland) | Inkubator och science park, ägd av Region Västernorrland och kommunerna | Avstämningsmöte Wilma/Magnus 6 oktober 2026 | Uppfyller koordinatorkravet. Geografiskt nära Miun. Ingen känd dual use-verksamhet; det är i sig ett argument i ansökan (metod för en regional inkubator utan tidigare FM-kontakt). |
| **Uppsala Innovation Centre (UIC)** | Inkubator | Ingen dokumenterad relation i e-post | Beviljades 2024-02587 i programmet, har nätverk med FM, FMV, SOFF och 13 inkubatorer. Coala har Uppsalaadress. Stark kandidat om de tar in en extra part på tre dagar. |
| **Miun Innovation / Mittuniversitetets innovationskontor** | Innovationskontor | Via Jan Lundgren | Uppfyller formellt koordinatorkravet (innovationskontor). Miun kan också vara forskningspart (höjer Coalas stödnivå till 60 % vid faktiskt samarbete). |
| **Connect Sverige Uppsala/Norr** | Affärsnätverk | Kontakter identifierade i Bridge-arbetet (Arvid Callin Nerdal, Marie Wiklund) | Rådgivande uppdrag, kan kvalificera som innovationsaktör **[verifiera]**. |
| **Sahlgrenska Science Park** | Science park | Via Swecare-aktiviteter | Göteborg, där Försvarsmedicincentrum ligger. |
| **Swecare** | Branschförening | Medlem | Troligen inte koordinator. |
| **LEAD** (Linköping) | Nationell accelerator för civil-militära synergier | Ingen | Programmets accelerator; kontakt värd att ta oavsett. |
| **Karolinska/Region Stockholm** (Kristina Groth) | Vårdgivare | Pågående projekt | Kan vara part eller referens för hemsjukhusvårdsmodellen. |
| **Region Skåne, SUS** (Tord Juhlin, överläkare kardiologi Malmö) | Vårdgivare | Möte 9 oktober 2026 | Klinisk partner/referens. |

## Vägar in i Försvarsmakten (för behovsbeskrivningen)

Kravet: behovsägaren företräds av eller har uppdrag från stridskrafts-/försvarsgrensstab eller avdelningschef i Försvarsstaben. Ingen befintlig FM-kontakt hittades i e-post, kalender eller Teams. Kandidater att kontakta, i prioritetsordning:

1. **Försvarsmaktens överläkare / försvarsmedicinfunktionen i Försvarsstaben** (avdelningschefsnivå, uppfyller formkravet). **[verifiera aktuell befattning och namn]**
2. **Försvarsmedicincentrum (FömedC), Göteborg**: Försvarsmaktens stridsskola för försvarsmedicin med simulerings- och metodavdelning, sjukhusbataljon. Substanskontakt; signatur måste gå via stab. **[verifiera organisatorisk tillhörighet]**
3. **FMV** och **FOI** deltar i programmet och får projektsammanfattningen; FOI driver Militärt innovationsprogram (MIP) för SME. Kan inte signera behovsbilagan men kan öppna dörrar.
4. Vinnovas handläggare (Lars Resman) kan ge besked om hur andra sökande fått behovsbilagan och om FM har en samordnande ingång för utlysningen. Ring måndag 08:00 om det inte går fredag.

## Luckor och vad som saknas i tillgängliga källor

- Inget "minne" hittades i den här miljön (ingen memory-katalog). De artifacts som finns är lästa: Coala data map, Orb Platform Capability Map (annat bolag), Portal Renewal Decisions, Coala Billing Map, Ledger & Inbox, Coala Bridge Close. Claude.ai-chattminnen är inte åtkomliga från den här sessionen.
- Teams-chattsökning gav inga träffar på Vinnova/försvar; antingen finns inget eller så saknas behörighet (ChannelMessage.Read.All). **[Magnus: finns relevant material i Teams?]**
- Inga FM-kontakter i e-post eller kalender.
- Koordinatorkandidaternas vilja och kapacitet är okänd tills Magnus ringt.
