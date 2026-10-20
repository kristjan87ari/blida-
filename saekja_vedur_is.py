#!/usr/bin/env python3
"""
Sækir gögn frá Veðurstofu Íslands sem vafri getur ekki sótt beint:

  vedur_is.json     stöðvaspár (xmlweather.vedur.is)
  vidvaranir.json   gular, appelsínugular og rauðar viðvaranir (CAP, í gegnum MeteoAlarm)

Vefsíðan (index.html) les skrárnar ef þær liggja við hliðina á henni.
Keyrir sjálfkrafa á klukkutíma fresti í GitHub Actions (.github/workflows/vedur_is.yml).
Krefst aðeins Python 3.9+.
"""
import json, urllib.parse, urllib.request, xml.etree.ElementTree as ET
from datetime import datetime, timezone

# ---------------------------------------------------------------- Stöðvaspár
# Auðkenni spástöðva hjá Veðurstofunni. Staðfestu á vedur.is og bættu við að vild;
# ógild auðkenni eru einfaldlega hunsuð.
STODVAR = {
    "1":    ("Reykjavík",      64.127, -21.902),
    "422":  ("Akureyri",       65.685, -18.101),
    "571":  ("Egilsstaðir",    65.278, -14.403),
    "178":  ("Stykkishólmur",  65.074, -22.734),
    "2642": ("Ísafjörður",     66.060, -23.170),
    "6015": ("Vestmannaeyjar", 63.443, -20.273),
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


def saekja_stodvaspar():
    url = "https://xmlweather.vedur.is/?" + urllib.parse.urlencode({
        "op_w": "xml", "type": "forec", "lang": "is", "view": "xml",
        "ids": ";".join(STODVAR), "params": "F;T;W;R"})
    rot = ET.fromstring(saekja(url))
    stodvar = []
    for st in rot.iter("station"):
        sid = st.get("id")
        if st.get("valid") == "0" or sid not in STODVAR:
            continue
        nafn, lat, lon = STODVAR[sid]
        spa = []
        for f in st.iter("forecast"):
            try:
                t = datetime.strptime(f.findtext("ftime", ""), "%Y-%m-%d %H:%M:%S")
            except ValueError:
                continue
            spa.append({"t": t.strftime("%Y-%m-%dT%H:%M"), "T": tala(f.findtext("T")),
                        "F": tala(f.findtext("F")), "R": tala(f.findtext("R")), "W": f.findtext("W") or ""})
        if spa:
            stodvar.append({"id": sid, "nafn": nafn, "lat": lat, "lon": lon, "spa": spa})
    return stodvar


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


def vista(skra, gogn):
    with open(skra, "w", encoding="utf-8") as f:
        json.dump(gogn, f, ensure_ascii=False)


def main():
    nu = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        stodvar = saekja_stodvaspar()
        vista("vedur_is.json", {"uppfaert": nu, "stodvar": stodvar})
        print(f"Stöðvaspár: {len(stodvar)} stöðvar")
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


if __name__ == "__main__":
    main()
