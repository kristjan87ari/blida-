# Besta veðrið

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

## Topp 5, 10 eða 20

Fyrir ofan listann velurðu hve margir staðir birtast. Valið gildir fyrir alla flokka og er munað í vafranum. Við Topp 20 er lágmarksfjarlægð milli punkta 22 km í stað 30, svo þeir komist fyrir. Í skíðaflokknum eru alltaf öll níu svæðin sýnd.

## Upplýsingaspjald

Þegar smellt er á rauðan punkt eða stað í listanum opnast upplýsingaspjald í stað sprettiglugga. Valinn punktur stækkar og fær bláan hring.

- **Í tölvu** er spjaldið neðst til vinstri á kortinu. Kortið er frjálst á meðan; hægt er að draga það og þysja.
- **Í síma** er spjaldið neðst á skjánum. Smelltu á haus þess til að brjóta það saman, svo aðeins nafn og einkunn sjáist. Valinn staður færist sjálfkrafa upp fyrir spjaldið.

Spjaldinu er lokað með × eða Esc-takkanum.

## Veðurtákn og leiðarlýsing

Hver staður fær veðurtákn eftir spánni: ☀️ sólríkt, 🌤️ léttskýjað, ⛅ skýjað, ☁️ alskýjað, 🌧️ rigning, 🌨️ slydda, ❄️ snjókoma, 🌫️ þoka, 🌙 heiðskír nótt, og 💨 bætist við í hvassviðri. Gildin eru líka merkt táknum: 🌡️ hiti, 💨 vindur, 🌬️ hviður, 💧 úrkoma, ☀️ sól, 📏 snjódýpt og 🌙 næturhiti.

Í glugga hvers staðar er hnappurinn **🧭 Hvernig kemst ég þangað?**. Hann opnar leiðarlýsingu frá staðsetningu þinni, í Apple Maps á iPhone, iPad og Mac en annars í Google Maps. Þar er líka tengill á færð á vegum á umferdin.is. Ef staðurinn er á hálendinu (yfir 450 m eða meira en 45 km frá strönd) birtist viðvörun um að hálendisvegir séu oft lokaðir.

Leiðarlýsingin vísar á punktinn sjálfan. Hann getur verið utan vega, svo Google og Apple leiða þig að næsta vegi.

## Öryggi: næsta aðstoð

Þegar smellt er á stað birtist neðst í glugganum kaflinn **🛟 Öryggi: næsta aðstoð**, með næstu gistingu (hótel, gistiheimili, tjaldsvæði), næsta skála eða neyðarskýli og næstu byggð eða bæ, ásamt fjarlægð. Smelltu á nafn til að fá leiðarlýsingu þangað. Neðst er hnappur sem hringir í 112.

Upplýsingarnar koma úr OpenStreetMap í gegnum Overpass-þjónustuna og eru sóttar þegar smellt er á stað. Leitað er innan 40 km. Fjarlægð er í beinni línu, ekki eftir vegum. OpenStreetMap er unnið af sjálfboðaliðum og getur vantað staði, svo ekki treysta á það eitt.

## Vefir skíðasvæða

Í skíðaflokknum er tengill á vef hvers svæðis. Slóðirnar eru í `SKIDA_VEFIR` í `index.html`. **Smelltu á hverja þeirra til að staðfesta að hún sé rétt**, því ég gat ekki prófað þær. Tindastóll og Seljalandsdalur fá leitartengil þar til rétt slóð er sett inn.

## Sundlaugar og tjaldsvæði

Í flokkunum **Sund og pottar** og **Útilega** eru raunverulegar sundlaugar, baðstaðir og tjaldsvæði borin saman, ekki reitir. Staðsetningarnar koma úr OpenStreetMap, sóttar einu sinni og geymdar í vafranum í viku. Sundlaugar og pottar á sama stað sameinast í einn stað. Í glugga hvers staðar er tengill á vef hans (ef skráður) og á sundlaugar.is eða tjalda.is.

sundlaugar.is og tjalda.is bjóða ekki opna gagnaveitu sem vefsíða getur lesið, svo þær eru notaðar sem tenglar fyrir opnunartíma og verð. Ef OpenStreetMap svarar ekki birtist listi yfir um 16–18 þekktustu staðina, ásamt ábendingu um það.

Staðir sem vantar má bæta inn í OpenStreetMap (openstreetmap.org); þá birtast þeir hér innan viku.

## Leiðrétta staðsetningu

GPS í tölvu byggir oft á netsambandi og getur skeikað um marga kílómetra. Ef staðsetningin er ónákvæm birtist óvissuhringur á kortinu og ábending. Þú getur leiðrétt hana á þrjá vegu:

- **dregið bláa punktinn** á réttan stað á kortinu,
- smellt á **Velja á korti** og svo á réttan stað, eða
- slegið inn bæ, til dæmis Kópavogur, Hafnarfjörður, Garðabær eða Mosfellsbær.

## Velja svæði

Smelltu á **⬚ Velja svæði** efst til vinstri á kortinu. Svo annaðhvort:

- **dregurðu ramma** með músinni (eða fingri í síma) yfir svæðið sem þú stefnir á, eða
- **smellir einu sinni** á kortið; þá er valið um 45 × 45 km svæði í kringum smellinn.

Síðan sækir nákvæmari spá fyrir allt að 100 punkta innan rammans og sýnir bestu staðina þar, Topp 5, 10 eða 20, fyrir þann flokk sem er valinn. Því minni rammi, því þéttari punktar: í litlum ramma geta þeir verið með um 4 km millibili. Í skíðaflokknum birtast skíðasvæðin innan rammans.

Hnappurinn **↺ Hreinsa leit**, undir „Velja svæði“ á kortinu, byrjar upp á nýtt: hættir við valið svæði, lokar upplýsingaspjaldinu, fjarlægir niðurstöður nákvæmari leitar og sýnir allt landið aftur. Flokkur, dagur og staðsetning þín haldast.

Í listanum birtist kassinn **Valið svæði** með hnappinum **Klæðnaður fyrir besta staðinn**. **Allt landið** fer aftur í yfirlit yfir allt Ísland. Esc-takkinn eða **Hætta við** hættir við val.

## Hverju á ég að klæðast?

Efst í listanum er hnappurinn **👕 Hverju á ég að klæðast?**. Þú velur staðsetningu á einn af þremur vegu:

- **Nota staðsetningu mína:** GPS í síma eða tölvu. Vafrinn spyr um leyfi fyrst. Virkar aðeins á https-síðu, eins og á Cloudflare.
- **Sláðu inn stað:** Bæir, ferðamannastaðir og skíðasvæði birtast sem tillögur meðan þú skrifar.
- **Velja á korti:** Smelltu svo hvar sem er á landinu.

Einnig má smella á rauðan punkt og velja **Hverju á ég að klæðast hér?**.

Síðan sækir spá fyrir nákvæmlega þann stað og stingur upp á klæðnaði fyrir þann flokk og dag sem er valinn. Ráðin skiptast í „Í fötin“, „Taktu með“ og „Gott að vita“, og taka mið af:

- **upplifuðum hita** (vindkælingu),
- **hreyfingu:** á fjallgöngu, hjóli og skíðum hitnar þú og þarft minna, en við norðurljósaskoðun stendurðu kyrr og þarft meira,
- **úrkomu og vindi:** skeljajakki og regnbuxur,
- **hálku:** mannbroddar, eða jöklabroddar á fjöllum í snjó,
- **sól og snjó:** sólgleraugu, skíðagleraugu og sólarvörn,
- **myrkri:** höfuðljós frá október til mars,
- **flokknum sjálfum:** svefnpoki fyrir útilegu miðað við næturhitann, appelsínugult vesti fyrir rjúpnaveiði, hitabrúsi og handhitarar fyrir norðurljós, og fleira,
- **viðvörunum** Veðurstofunnar á staðnum.

Staðsetningin er aðeins notuð í vafranum og til að sækja spá frá Open-Meteo. Hún er munuð í vafranum milli heimsókna en ekki send annað. Reglurnar eru í fallinu `klaednadur` í `index.html`, ef þú vilt breyta þeim.

## Gögn frá Veðurstofu Íslands

Síðan notar þrennt frá Veðurstofunni, allt sótt af sjálfvirkninni á GitHub á tveggja tíma fresti:

- **Stöðvaspár** frá allt að 26 spástöðvum, teknar með í útreikning staða innan 20 km frá stöð.
- **Nýjustu mælingar** frá sömu stöðvum, sýndar í upplýsingaspjaldi nálægra staða („📡 Mælt kl. 14:00 á Akureyri …“). Mælingar eldri en 6 klst. eru ekki sýndar.
- **Viðvaranir** (sjá næsta kafla).

Undir **Stillingar** sérðu hvað er tengt og hve margar stöðvar skila gögnum.

Stöðvarnar eru í `STODVAR` efst í `saekja_vedur_is.py`. Hverri stöð fylgir lykilorð, og forritið ber það saman við heitið sem Veðurstofan skilar. Ef það passar ekki er stöðinni sleppt, svo rangt stöðvanúmer getur aldrei sett spá einnar stöðvar á annan stað. Í keyrsluskrá sjálfvirkninnar á GitHub sérðu hve margar stöðvar skiluðu gögnum og hverjum var sleppt. Rétt stöðvanúmer má finna á vedur.is.

Veðurstofan býður ekki opinn aðgang að sínu eigin reiknilíkani, en HARMONIE-AROME frá dönsku veðurstofunni er sama líkanagerð og nær yfir Ísland.

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

## Tákn og merkingar

Á síðunni „Um síðuna“, fyrir ofan „Hafa samband“, eru öll tákn síðunnar útskýrð: flokkar, veðurtákn, gildi, önnur tákn og litir einkunna og viðvarana. Kaflinn er byggður úr sömu textum og síðan notar, svo hann fylgir tungumálavalinu og uppfærist sjálfkrafa ef texta er breytt. Fallið heitir `taknskyring` í `index.html`.

## Hafa samband

Neðst á síðunni „Um síðuna“ er kaflinn **Hafa samband** með netfanginu hello@vedra.is, á öllum tungumálum. Til að breyta netfanginu finnurðu `const NETFANG=` í `index.html`.

## Athugið

Þetta er hjálpartæki, ekki öryggisspá. Fyrir fjallaferðir og veiði skaltu líka skoða vedur.is, snjóflóðaspá og safetravel.is.
