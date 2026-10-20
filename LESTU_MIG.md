# Besti staðurinn

Vefsíða sem sýnir kort af Íslandi með rauðum punktum þar sem aðstæður eru bestar fyrir það sem þú ætlar að gera: besta veðrið, útilegu, rjúpnaveiði, fjallgöngu, norðurljós, hjólreiðar, gönguskíði eða sund og potta. Síðan sækir nýjustu spár beint frá veðurveitunum í hvert sinn sem þú opnar hana eða smellir á **Sækja nýjustu spá**, og sjálfkrafa á klukkutíma fresti.

## Prófa á eigin tölvu

Ekkert þarf að setja upp. Tvísmelltu á `index.html` og hún opnast í vafranum þínum.

## Setja upp sem vefsíðu á Cloudflare Pages

Cloudflare Pages hýsir síðuna ókeypis, með öruggri https-slóð á borð við `besti-stadurinn.pages.dev`, opna öllum.

### Leið A: Fljótlegast (um 10 mínútur)

Allt virkar nema viðvaranir og stöðvaspár Veðurstofunnar; í stað þeirra birtist tengill á vedur.is.

1. Stofnaðu aðgang á dash.cloudflare.com (ókeypis), eða skráðu þig inn.
2. Veldu **Workers & Pages** í valmyndinni vinstra megin, svo **Create** og flipann **Pages**.
3. Veldu **Upload assets** (eða „Drag and drop your files“).
4. Gefðu verkefninu nafn, t.d. `besti-stadurinn`. Nafnið verður hluti af slóðinni.
5. Dragðu möppuna `besti-stadurinn` (úr zip-skránni) inn í gluggann og smelltu á **Deploy site**.
6. Eftir nokkrar sekúndur er síðan komin á `https://besti-stadurinn.pages.dev`.

Til að uppfæra síðar: opnaðu verkefnið, veldu **Create deployment** og dragðu möppuna inn aftur.

### Leið B: Með viðvörunum Veðurstofunnar (um 30 mínútur)

Hér geymir GitHub skrárnar og sækir gögn Veðurstofunnar á tveggja tíma fresti, og Cloudflare birtir síðuna sjálfkrafa í hvert sinn sem gögnin breytast.

1. **GitHub:** Stofnaðu aðgang á github.com. Smelltu á **+** efst til hægri, svo **New repository**. Nefndu safnið `besti-stadurinn`. Það má vera **Private**. Smelltu á **Create repository**.
2. **Skrárnar:** Í nýja safninu smellirðu á **uploading an existing file** og dregur inn `index.html`, `saekja_vedur_is.py` og `LESTU_MIG.md`. Smelltu á **Commit changes**.
3. **Sjálfvirknin:** Mappan `.github` er falin og kemst oft ekki með þegar dregið er. Smelltu því á **Add file → Create new file**, skrifaðu `.github/workflows/vedur_is.yml` sem nafn, afritaðu innihald samnefndrar skrár úr zip-skránni og smelltu á **Commit changes**.
4. **Leyfi:** Farðu í **Settings → Actions → General**, veldu **Read and write permissions** neðst undir „Workflow permissions“ og smelltu á **Save**.
5. **Fyrsta keyrsla:** Farðu í flipann **Actions**, veldu „Sækja spá og viðvaranir Veðurstofunnar“ og smelltu á **Run workflow**. Eftir mínútu ættu `vedur_is.json` og `vidvaranir.json` að birtast í safninu. Ef keyrslan verður rauð, smelltu á hana til að sjá villuna.
6. **Cloudflare:** Á dash.cloudflare.com velurðu **Workers & Pages → Create → Pages → Connect to Git**. Tengdu GitHub-aðganginn og veldu safnið `besti-stadurinn`.
7. **Stillingar:** Undir „Build settings“ velurðu **Framework preset: None**, skilur **Build command** eftir autt og setur `/` sem **Build output directory**. Smelltu á **Save and Deploy**.
8. Síðan er komin á `https://besti-stadurinn.pages.dev`. Hún uppfærist sjálf á tveggja tíma fresti þegar GitHub sækir ný gögn, og líka í hvert sinn sem þú breytir skrá í safninu.

Ókeypis áskrift Cloudflare Pages leyfir 500 uppfærslur á mánuði. Sjálfvirknin keyrir á tveggja tíma fresti, um 370 sinnum á mánuði, svo það er nægt svigrúm fyrir þínar eigin breytingar. Ekki stilla hana á tíðari keyrslu.

### Eigið lén (valfrjálst)

Viljirðu slóð eins og `bestistadurinn.is` kaupirðu lénið hjá ISNIC (isnic.is) og tengir það undir **Custom domains** í Cloudflare-verkefninu. Cloudflare leiðir þig í gegnum það.

### Aðrar leiðir

GitHub Pages og Netlify virka líka. Á GitHub Pages þarf safnið að vera opið (Public) í ókeypis áskrift.

## Kortið

Hægt er að þysja inn á kortið alveg niður á götu- og slóðastig með músarhjólinu, tveimur fingrum í síma eða +/− tökkunum. Efst til hægri velurðu kortagrunn:

- **Landslag:** hæðarlínur, fjöll og slóðar (OpenTopoMap). Hentar vel fyrir fjallgöngu og rjúpnaveiði.
- **Loftmynd:** gervihnattamyndir (Esri). Gott til að sjá skóglendi, hraun, jökla og vegslóða.

(OpenStreetMap-kortið var tekið út, því það lokar á síður sem opnaðar eru beint af tölvu.)

Þegar þú smellir á rauðan punkt þysjar kortið að honum og rammar inn reitinn sem spáin gildir fyrir (um 28 × 23 km). Smelltu þá á **Finna besta blettinn innan reitsins**. Síðan sækir þá nákvæmari spá fyrir 49 punkta innan reitsins, með um 4 km millibili, og merkir þrjá bestu blettina. Sá besti er merktur með stjörnu. Við hvern stað eru nákvæm hnit og tenglar á Google Maps og OpenStreetMap, svo þú getir fengið leiðsögn þangað.

Athugaðu að jafnvel nákvæmasta líkanið (HARMONIE, 2 km) sér ekki einstaka gil eða skjól bak við kletta. Spáin segir til um svæðið, en á staðnum er það þitt mat sem gildir.

## Hvaðan koma gögnin

| Heimild | Hvernig |
|---|---|
| ECMWF (Evrópska reiknimiðstöðin) | Beint í vafranum, í gegnum Open-Meteo |
| HARMONIE-AROME (DMI) | Beint í vafranum. Sama líkanagerð og Veðurstofan keyrir, í meiri upplausn |
| ICON (Þýska veðurstofan) | Beint í vafranum |
| GFS, UKMO, Météo-France | Hægt að kveikja á undir Stillingar |
| Veðurstofa Íslands, stöðvaspár | Valfrjálst, í gegnum GitHub Actions (vafrar mega ekki sækja beint frá vedur.is) |
| Veðurstofa Íslands, viðvaranir | Valfrjálst, í gegnum GitHub Actions. Sóttar á CAP-sniði í gegnum MeteoAlarm |
| belgingur.is og blika.is | Ekki með: hvorug veitan býður opið forritaskil |

Síðan reiknar stig fyrir hvert líkan sérstaklega og tekur meðaltalið. Ef líkönin eru ósammála stendur „óvissa“ við staðinn.

Open-Meteo er ókeypis til einkanota upp að um 10.000 köllum á dag. Hver uppfærsla notar nokkur hundruð, svo það dugar vel fyrir þig og nokkra aðra. Ef síðan verður mikið notuð þarf greiddan aðgang hjá Open-Meteo.

## Flokkarnir

Hver flokkur metur sína þætti á sínum tíma dags:

- **Besta veðrið** (kl. 9–18): hiti, lítill vindur, sól, þurrt. Láglendi.
- **Útilega** (hádegi til kl. 9 næsta morgun): hlýr dagur, mild nótt, logn, þurrt. Undir 300–700 m.
- **Rjúpnaveiði** (kl. 9–17): hægur vindur, lítil lágský og gott skyggni, þurrt, kalt í lagi, snjór kostur. Heiðar og hlíðar í 200–750 m.
- **Fjallganga** (kl. 8–18): litlar hviður, skýlausir tindar, þurrt. Fjalllendi í 350–1100 m.
- **Norðurljós** (kl. 21–02): heiðskírt, fjarri ljósum þéttbýlis. Metur ekki norðurljósavirkni sjálfa.
- **Hjólreiðar** (kl. 9–19): mjög lítill vindur og hviður, þurrt, milt.
- **Gönguskíði** (kl. 9–17): snjódýpt úr líkönum, kalt, lítill vindur, bjart.
- **Sund og pottar** (kl. 10–21): logn og þurrt.
- **Skíði** (kl. 10–17): ber saman skíðasvæðin níu (Bláfjöll, Skálafell, Hlíðarfjall, Oddsskarð, Stafdal, Tindastól, Siglufjörð, Dalvík og Ísafjörð) eftir snjó, vindi sem stöðvar lyftur, skyggni og frosti. Opnunartímar koma ekki fram; kannaðu vef svæðisins. Hnit svæðanna eru nálgun og má leiðrétta í `SKIDASVAEDI` í `index.html`.
- **Versta veðrið** (allur sólarhringurinn): hvar er hvassast, kaldast og blautast í byggð. Há tala er slæm. Hálendið er undanskilið, annars væru jöklarnir alltaf verstir.
- **Snjóflóðahætta** (allur sólarhringurinn): sýnir hvar *veðrið* eykur líkur á snjóflóðum: nýsnjór síðustu þrjá sólarhringa, skafrenningur í hvassviðri og hlýnun eða regn á snjó. Rauðu punktarnir og appelsínugulu reitirnir sýna hvar þessir þættir eru verstir.

  **Þetta er ekki snjóflóðaspá.** Kerfið metur hvorki landslag, halla né snjóalög, og lágur hættuvísir þýðir ekki að svæði sé öruggt. Snjóflóðaspá Veðurstofunnar á vedur.is er eina áreiðanlega heimildin.

Viljir þú breyta vægi eða bæta við flokki, finnurðu `FLOKKAR` ofarlega í `index.html`. Hver flokkur er nokkrar línur.

## Viðvaranir Veðurstofunnar

Gular, appelsínugular og rauðar viðvaranir birtast sem lituð svæði á kortinu og í kassa efst í listanum. Smelltu á viðvörun til að þysja að henni. Staðir innan viðvörunarsvæðis fá lægri einkunn: gul viðvörun lækkar hana um 15%, appelsínugul um 40% og rauð um 70%. Það gildir þó ekki í flokkunum Versta veðrið og Snjóflóðahætta.

Viðvaranirnar eru sóttar af `saekja_vedur_is.py` í GitHub Actions á klukkutíma fresti og vistaðar í `vidvaranir.json`. Þær virka því aðeins þegar síðan er á GitHub Pages með sjálfvirknina í gangi; annars birtist tengill á vedur.is. Ef sóknin mistekst skrifar forritið villuskrá, svo síðan sýni aldrei gamlar viðvaranir sem gildar.

Forritið sækir viðvaranirnar úr straumi MeteoAlarm fyrir Ísland (`VIDVARANA_STRAUMUR` efst í skránni), þar sem Veðurstofan birtir viðvaranir sínar á alþjóðlega CAP-sniðinu. Ég gat ekki prófað strauminn sjálfan, aðeins lesturinn á tilbúnum CAP-gögnum. Eftir fyrstu keyrslu í GitHub Actions sérðu í keyrsluskránni línuna „Viðvaranir í gildi: N“ eða villuboð. Ef straumurinn virkar ekki má setja slóð á beinan CAP-straum Veðurstofunnar í staðinn, því forritið les bæði sniðin.

Ef viðvörun fylgja ekki nákvæm svæðismörk er hún teiknuð sem 60 km hringur um miðju spásvæðisins.

## Tungumál

Síðan er á íslensku en hægt er að velja ensku, dönsku, sænsku, pólsku, frönsku, kínversku og spænsku efst til hægri. Valið er munað í vafranum. Allar þýðingar eru í `I18N` ofarlega í `index.html`. Til að bæta við tungumáli afritarðu `en`-hlutann, gefur honum nýjan kóða (t.d. `de`) og þýðir textana.

Þýðingarnar voru gerðar af gervigreind. Láttu móðurmálsfólk lesa þær yfir, sérstaklega fyrirvarann.

## Síðurnar „Um síðuna“ og „Hvernig virkar þetta“

Þær eru í valmyndinni efst og á slóðunum `#um` og `#hvernig`. Textinn er í `sidur` í hverju tungumáli í `I18N`.

Fyrirvarinn um ábyrgð er almennur texti, ekki lögfræðiráðgjöf. Ef síðan verður mikið notuð eða tengd rekstri er skynsamlegt að láta lögfræðing fara yfir hann. Samkvæmt íslenskum lögum er til dæmis ekki hægt að undanskilja ábyrgð á stórfelldu gáleysi eða ásetningi; þess vegna stendur „að því marki sem lög leyfa“.

## Gestateljari

Teljarinn efst sýnir hve margir eru á síðunni samtímis. Venjulegt vefsvæði veit það ekki sjálft, svo teljarinn þarf þjónustu sem fylgist með opnum tengingum. Hann notar ókeypis Firebase Realtime Database frá Google:

1. Farðu á console.firebase.google.com og stofnaðu verkefni (ókeypis „Spark“-áskrift dugar).
2. Veldu „Build → Realtime Database → Create database“, veldu staðsetningu í Evrópu og „Start in locked mode“.
3. Undir „Rules“ seturðu þessar reglur og smellir á „Publish“:
   ```json
   {
     "rules": {
       "gestir": {
         ".read": true,
         "$id": { ".write": true, ".validate": "newData.isNumber() || !newData.exists()" }
       }
     }
   }
   ```
4. Farðu í „Project settings → General → Your apps“, veldu vefapp (`</>`), og afritaðu `firebaseConfig`.
5. Í `index.html` finnurðu línuna `const TELJARI={firebase:null ...` og setur stillingarnar í stað `null`, t.d.:
   ```js
   const TELJARI={firebase:{apiKey:"AIza…",authDomain:"verkefni.firebaseapp.com",databaseURL:"https://verkefni-default-rtdb.europe-west1.firebasedatabase.app",projectId:"verkefni"}};
   ```

Ef ekkert er stillt birtist teljarinn einfaldlega ekki. Hann geymir aðeins tímastimpil fyrir hverja opna tengingu, engar persónuupplýsingar.

## Athugið

Þetta er hjálpartæki, ekki öryggisspá. Fyrir fjallaferðir og veiði skaltu líka skoða vedur.is, snjóflóðaspá og safetravel.is.
