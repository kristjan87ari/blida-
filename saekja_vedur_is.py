#!/usr/bin/env python3
"""
Sækir gögn frá Veðurstofu Íslands sem vafri getur ekki sótt beint:

  vedur_is.json     stöðvaspár og nýjustu mælingar (xmlweather.vedur.is)
  vidvaranir.json   gular, appelsínugular og rauðar viðvaranir (CAP, í gegnum MeteoAlarm)

Vefsíðan (index.html) les skrárnar ef þær liggja við hliðina á henni.
Keyrir sjálfkrafa á klukkutíma fresti í GitHub Actions (.github/workflows/vedur_is.yml).
Krefst aðeins Python 3.9+.
"""
import json, urllib.parse, urllib.request, xml.etree.ElementTree as ET
from datetime import datetime, timezone

# ---------------------------------------------------------------- Stöðvaspár
# Spástöðvar Veðurstofunnar: auðkenni -> (nafn, breidd, lengd, lykilorð).
# Til öryggis er heitið sem Veðurstofan skilar borið saman við lykilorðið (hlutstrengur, | skilur
# að valkosti). Ef það passar ekki er stöðinni sleppt, svo rangt auðkenni getur aldrei sett spá
# einnar stöðvar á annan stað. Bættu við stöðvum að vild; rétt auðkenni má finna á vedur.is.
STODVAR = {
    "1":    ("Reykjavík",             64.127, -21.902, "reykjavík"),
    "1350": ("Reykjavíkurflugvöllur", 64.130, -21.940, "reykjavíkurflug"),
    "990":  ("Keflavíkurflugvöllur",  63.968, -22.605, "keflavík"),
    "3054": ("Akranes",               64.320, -22.080, "akranes"),
    "1596": ("Þingvellir",            64.280, -21.090, "þingv"),
    "1919": ("Bláfjöll",              63.980, -21.650, "bláfj"),
    "178":  ("Stykkishólmur",         65.074, -22.734, "stykkish"),
    "2315": ("Patreksfjörður",        65.600, -23.990, "patreks"),
    "2642": ("Ísafjörður",            66.060, -23.170, "ísafj"),
    "2738": ("Bolungarvík",           66.160, -23.250, "bolungarv"),
    "2481": ("Hólmavík",              65.700, -21.680, "hólmav"),
    "3696": ("Blönduós",              65.660, -20.280, "blönduós"),
    "3471": ("Sauðárkrókur",          65.750, -19.640, "sauðárkr"),
    "4323": ("Siglufjörður",          66.150, -18.910, "siglufj"),
    "422":  ("Akureyri",              65.685, -18.101, "akureyri"),
    "4193": ("Húsavík",               66.040, -17.330, "húsavík"),
    "4614": ("Mývatn",                65.640, -16.910, "mývatn|reykjahlíð"),
    "4912": ("Raufarhöfn",            66.450, -15.950, "raufarh"),
    "571":  ("Egilsstaðir",           65.278, -14.403, "egilsst"),
    "620":  ("Dalatangi",             65.270, -13.580, "dalatangi"),
    "5544": ("Höfn í Hornafirði",     64.267, -15.200, "höfn"),
    "772":  ("Kirkjubæjarklaustur",   63.790, -18.020, "kirkjubæjar"),
    "6272": ("Vík í Mýrdal",          63.420, -19.010, "vík í mýrdal|mýrdal"),
    "6222": ("Hella",                 63.830, -20.400, "hella"),
    "6015": ("Vestmannaeyjar",        63.443, -20.273, "vestmannaey"),
    "6935": ("Hveravellir",           64.870, -19.560, "hveravell"),
}

# ---------------------------------------------------------------- Viðvaranir
# Viðvörunarstraumur fyrir Ísland (Atom með CAP-viðvörunum). Ef Veðurstofan býður beinan
# CAP-straum má setja slóð hans hér í staðinn; kóðinn les bæði Atom og CAP.
VIDVARANA_STRAUMUR = "https://feeds.meteoalarm.org/feeds/meteoalarm-legacy-atom-iceland"

# Miðjur spásvæða, notaðar ef viðvörun fylgir enginn marghyrningur (hnit eru nálgun)
SVAEDI = {
    "austurland að glettingi": (65.55, -14.9), "norðurland vestra": (65.55, -20.0), "norðurland eystra": (65.75, -17.6),
    "höfuðborgarsvæði": (64.12, -21.85), "breiðafjörður": (65.05, -22.9), "suðausturland": (64.15, -16.3),
    "miðhálendi": (64.75, -18.0), "vestfirðir": (65.85, -23.0), "austfirðir": (64.95, -14.1), "suðurland": (63.9, -20.3),
    "faxaflói": (64.45, -21.9), "strandir": (65.6, -20.6),
    "capital region": (64.12, -21.85), "breidafjordur": (65.05, -22.9), "faxafloi": (64.45, -21.9),
    "central highlands": (64.75, -18.0), "westfjords": (65.85, -23.0), "eastfjords": (64.95, -14.1),
    "southeast": (64.15, -16.3), "northwest": (65.55, -20.0), "northeast": (65.75, -17.6), "east": (65.4, -14.8),
    "south": (63.9, -20.3), "capital": (64.12, -21.85), "highland": (64.75, -18.0),
}

UA = {"User-Agent": "BestiStadurinn/3.0"}


def saekja(url, timi=30):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timi) as r:
        return r.read()


def tala(t):
    try:
        return float((t or "").replace(",", "."))
    except ValueError:
        return None


def heiti_passar(heiti, lykilord):
    h = (heiti or "").lower()
    return any(k in h for k in lykilord.split("|"))


def saekja_xml(tegund, ids, breytur):
    url = "https://xmlweather.vedur.is/?" + urllib.parse.urlencode({
        "op_w": "xml", "type": tegund, "lang": "is", "view": "xml", "ids": ";".join(ids), "params": breytur})
    return ET.fromstring(saekja(url))


def saekja_stodvaspar():
    """Skilar (stöðvar, fjöldi sleppt). Hver stöð fær spá og nýjustu mælingu ef til."""
    stodvar, sleppt, ids = {}, [], list(STODVAR)
    for i in range(0, len(ids), 8):
        bunki = ids[i:i + 8]
        try:
            rot = saekja_xml("forec", bunki, "F;T;W;R")
        except Exception as e:
            print(f"  Spár fyrir {bunki} mistókust: {e}")
            continue
        for st in rot.iter("station"):
            sid = st.get("id")
            if st.get("valid") == "0" or sid not in STODVAR:
                continue
            nafn, lat, lon, lykill = STODVAR[sid]
            if not heiti_passar(st.findtext("name"), lykill):
                sleppt.append(f"{sid} (vænti {nafn}, fékk {st.findtext('name')})")
                continue
            spa = []
            for f in st.iter("forecast"):
                try:
                    t = datetime.strptime(f.findtext("ftime", ""), "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    continue
                spa.append({"t": t.strftime("%Y-%m-%dT%H:%M"), "T": tala(f.findtext("T")),
                            "F": tala(f.findtext("F")), "R": tala(f.findtext("R")), "W": f.findtext("W") or ""})
            if spa:
                stodvar[sid] = {"id": sid, "nafn": nafn, "lat": lat, "lon": lon, "spa": spa, "maeling": None}
    # Nýjustu mælingar
    for i in range(0, len(ids), 8):
        bunki = ids[i:i + 8]
        try:
            rot = saekja_xml("obs", bunki, "T;F;D;W")
        except Exception as e:
            print(f"  Mælingar fyrir {bunki} mistókust: {e}")
            continue
        for st in rot.iter("station"):
            sid = st.get("id")
            if st.get("valid") == "0" or sid not in STODVAR:
                continue
            nafn, lat, lon, lykill = STODVAR[sid]
            if not heiti_passar(st.findtext("name"), lykill):
                continue
            try:
                t = datetime.strptime(st.findtext("time", ""), "%Y-%m-%d %H:%M:%S")
            except ValueError:
                continue
            m = {"t": t.strftime("%Y-%m-%dT%H:%M"), "T": tala(st.findtext("T")), "F": tala(st.findtext("F")),
                 "D": st.findtext("D") or "", "W": st.findtext("W") or ""}
            if m["T"] is None and m["F"] is None:
                continue
            if sid not in stodvar:
                stodvar[sid] = {"id": sid, "nafn": nafn, "lat": lat, "lon": lon, "spa": [], "maeling": m}
            else:
                stodvar[sid]["maeling"] = m
    return list(stodvar.values()), sleppt


# --- CAP/Atom-lestur, óháður nafnrýmum
def nafn(el):
    return el.tag.rsplit("}", 1)[-1]


def finna(el, n):
    for c in el.iter():
        if nafn(c) == n and (c.text or "").strip():
            return c.text.strip()
    return ""


def utc(t):
    """ISO-tími í UTC á forminu 2026-10-20T06:00:00Z (eða '' ef ólæsilegt)."""
    if not t:
        return ""
    try:
        d = datetime.fromisoformat(t.strip().replace("Z", "+00:00"))
        if d.tzinfo is None:
            d = d.replace(tzinfo=timezone.utc)
        return d.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        return ""


def litur_ur(*textar):
    t = " ".join(x for x in textar if x).lower()
    if "red" in t or "extreme" in t or "rauð" in t:
        return "raud"
    if "orange" in t or "severe" in t or "appelsínugul" in t:
        return "appelsinugul"
    if "yellow" in t or "moderate" in t or "gul" in t:
        return "gul"
    return None


def marghyrningar(rot):
    ut = []
    for el in rot.iter():
        if nafn(el) == "polygon" and el.text:
            pts = []
            for par in el.text.split():
                hlutar = par.split(",")
                if len(hlutar) >= 2 and tala(hlutar[0]) is not None and tala(hlutar[1]) is not None:
                    pts.append([round(tala(hlutar[0]), 4), round(tala(hlutar[1]), 4)])
            if len(pts) >= 3:
                ut.append(pts)
    return ut


def midja_svaedis(texti):
    t = (texti or "").lower()
    for lykill in sorted(SVAEDI, key=len, reverse=True):
        if lykill in t:
            return list(SVAEDI[lykill])
    return None


def lesa_cap(rot, v):
    """Fyllir inn texta á hverju tungumáli, tíma, lit og marghyrninga úr CAP-skjali."""
    for info in (e for e in rot.iter() if nafn(e) == "info"):
        mal = (finna(info, "language") or "is")[:2].lower()
        v["atburdur"][mal] = finna(info, "event")
        v["fyrirsogn"][mal] = finna(info, "headline") or finna(info, "description")[:240]
        if not v["svaedi"]:
            v["svaedi"] = finna(info, "areaDesc")
        v["gildirFra"] = v["gildirFra"] or utc(finna(info, "onset") or finna(info, "effective"))
        v["gildirTil"] = v["gildirTil"] or utc(finna(info, "expires"))
        if not v["litur"]:
            params = " ".join(finna(p, "value") for p in info.iter() if nafn(p) == "parameter")
            v["litur"] = litur_ur(params, finna(info, "severity"))
    v["marghyrningar"] = v["marghyrningar"] or marghyrningar(rot)


def saekja_vidvaranir():
    nu = datetime.now(timezone.utc)
    rot = ET.fromstring(saekja(VIDVARANA_STRAUMUR))
    if nafn(rot) == "alert":
        faerslur = [rot]
    else:
        faerslur = [e for e in rot.iter() if nafn(e) == "entry"]
    vidvaranir = []
    for f in faerslur:
        v = {"litur": litur_ur(finna(f, "awareness_level"), finna(f, "severity")),
             "atburdur": {}, "fyrirsogn": {}, "svaedi": finna(f, "areaDesc"),
             "gildirFra": utc(finna(f, "onset") or finna(f, "effective")), "gildirTil": utc(finna(f, "expires")),
             "marghyrningar": marghyrningar(f), "midja": None}
        if nafn(f) == "alert":
            lesa_cap(f, v)
        else:
            for tengill in (c.get("href") for c in f.iter() if nafn(c) == "link" and c.get("href")):
                try:
                    lesa_cap(ET.fromstring(saekja(tengill)), v)
                    break
                except Exception:
                    continue
        if not v["atburdur"]:
            v["atburdur"] = {"en": finna(f, "event") or finna(f, "title")}
        if not v["litur"] or not v["gildirTil"]:
            continue  # grænt/ekkert stig eða ólæsileg viðvörun
        if datetime.fromisoformat(v["gildirTil"].replace("Z", "+00:00")) < nu:
            continue  # útrunnin
        if not v["marghyrningar"]:
            v["midja"] = midja_svaedis(v["svaedi"])
            if not v["midja"]:
                continue
        vidvaranir.append(v)
    return vidvaranir


# ---------------------------------------------------------------- Fjallalisti (vikulega) úr OpenStreetMap
# Síðan les fjoll.json af vedra.is svo hún þurfi ekki að spyrja OpenStreetMap í hvert sinn
# (OpenStreetMap-þjónninn takmarkar fjölda fyrirspurna frá hverjum notanda).
OVERPASS = ["https://overpass-api.de/api/interpreter", "https://overpass.kumi.systems/api/interpreter"]
FJALLA_FYRIRSPURN = ('[out:json][timeout:180];('
    'node["natural"~"^(peak|volcano)$"]["name"](63.2,-24.6,66.6,-13.4);'
    'nwr["natural"~"^(mountain_range|ridge)$"]["name"](63.2,-24.6,66.6,-13.4););out center tags;')


def saekja_fjoll():
    villa = None
    for slod in OVERPASS:
        try:
            gogn = urllib.parse.urlencode({"data": FJALLA_FYRIRSPURN}).encode()
            with urllib.request.urlopen(urllib.request.Request(slod, data=gogn, headers=UA), timeout=200) as r:
                j = json.loads(r.read())
            ut = []
            for e in j.get("elements", []):
                tg = e.get("tags") or {}
                nafn = tg.get("name") or tg.get("name:is")
                la = e.get("lat", (e.get("center") or {}).get("lat"))
                lo = e.get("lon", (e.get("center") or {}).get("lon"))
                if not nafn or la is None or lo is None:
                    continue
                t = {"name": nafn}
                if tg.get("ele"):
                    t["ele"] = tg["ele"]
                # Allt verður „node“ með hnitum; auðkenni haldast einkvæm (n/w/r + númer)
                ut.append({"type": "node", "id": e["type"][0] + str(e["id"]), "lat": round(la, 5), "lon": round(lo, 5), "tags": t})
            if len(ut) < 500:
                raise RuntimeError(f"of fáir tindar ({len(ut)})")
            return ut
        except Exception as e:
            villa = e
    raise RuntimeError(f"OpenStreetMap svaraði ekki: {villa}")


def fjoll_gomul(skra="fjoll.json", dagar=7):
    try:
        with open(skra, encoding="utf-8") as f:
            t = datetime.strptime(json.load(f)["uppfaert"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        return (datetime.now(timezone.utc) - t).days >= dagar
    except Exception:
        return True


def vista(skra, gogn):
    with open(skra, "w", encoding="utf-8") as f:
        json.dump(gogn, f, ensure_ascii=False)


def main():
    nu = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        stodvar, sleppt = saekja_stodvaspar()
        if not stodvar:
            raise RuntimeError("engin stöð skilaði gögnum")
        vista("vedur_is.json", {"uppfaert": nu, "stodvar": stodvar})
        print(f"Stöðvaspár: {sum(1 for s in stodvar if s['spa'])} stöðvar, mælingar: {sum(1 for s in stodvar if s['maeling'])} stöðvar")
        for x in sleppt:
            print(f"  Sleppt (heiti passar ekki): {x}")
    except Exception as e:
        print(f"Stöðvaspár mistókust: {e}")
    try:
        vidv = saekja_vidvaranir()
        vista("vidvaranir.json", {"uppfaert": nu, "vidvaranir": vidv})
        print(f"Viðvaranir í gildi: {len(vidv)}")
    except Exception as e:
        # Skrifum villuskrá svo síðan sýni aldrei gamlar eða rangar viðvaranir sem gildar
        vista("vidvaranir.json", {"uppfaert": nu, "villa": True, "vidvaranir": []})
        print(f"Viðvaranir mistókust: {e}")
    if fjoll_gomul():
        try:
            fjoll = saekja_fjoll()
            vista("fjoll.json", {"uppfaert": nu, "elements": fjoll})
            print(f"Fjallalisti uppfærður: {len(fjoll)} tindar og fjallgarðar")
        except Exception as e:
            print(f"Fjallalisti mistókst (síðan spyr þá OpenStreetMap beint): {e}")
    else:
        print("Fjallalisti er nýlegur, ekki sóttur")


if __name__ == "__main__":
    main()
