#!/usr/bin/env python3
# Carta di pesca - Copyright (c) 2026 Giulio Bojan (GiulioBj). Tutti i diritti riservati. Vedi il file LICENSE.
"""Prepara maree.json per la app a partire dagli open data del Centro Previsioni e Segnalazioni Maree
del Comune di Venezia (licenza CC BY): previsione ufficiale, marea astronomica, livelli misurati.

Uso:  python3 tools/maree.py USCITA.json [--prec PRECEDENTE.json] [--da CARTELLA_LOCALE]

Tutti i livelli sono in centimetri sullo zero mareografico di Punta della Salute (ZMPS).
Gli orari in uscita sono secondi Unix (UTC)."""
import json, math, sys, time, urllib.request
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo

BASE = 'https://dati.venezia.it/sites/default/files/dataset/opendata/'
SOLARE = timezone(timedelta(hours=1))          # ora solare: livelli misurati e marea astronomica
ROMA = ZoneInfo('Europe/Rome')                 # ora corrente: previsione
PS = '1025'                                    # Punta Salute Canal Grande: riferimento della previsione
STORIA_ORE = 72
# Ritardo (minuti) e ampiezza rispetto a Punta Salute usati finché non ci sono abbastanza misure.
# Ritardi medi pubblicati dal Centro Maree e da ISPRA ("La propagazione della marea in laguna", fascicolo previsioni 2026):
# Piattaforma -56, Malamocco diga nord -54, Lido diga sud -51, Chioggia diga sud -54, interno bocca di Chioggia -21,
# Chioggia Vigo -20, Burano +32. Le altre stazioni (Malamocco porto, Fusina, Saline, Misericordia, San Geremia) sono stime.
BASE_ST = {'1021': (-56, 1.03), '1022': (-51, 1.02), '1023': (-54, 1.02), '1024': (-54, 1.02), '1033': (-21, 1.0),
           '1036': (-20, 1.0), '1032': (-25, 1.0), '1025': (0, 1.0), '1045': (0, 1.0), '1029': (5, 1.0),
           '1001': (5, 1.0), '1037': (10, 1.0), '1030': (32, .95), '1028': (55, .88)}


def leggi(nome, cartella=None):
    try:
        if cartella:
            with open(f'{cartella}/{nome}', encoding='utf-8') as f:
                return json.load(f)
        req = urllib.request.Request(BASE + nome, headers={'User-Agent': 'carta-di-pesca (github.com/GiulioBj/carta-pesca)'})
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode('utf-8-sig'))
    except Exception as e:                      # un file mancante non deve fermare gli altri
        print(f'non letto {nome}: {e}', file=sys.stderr)
        return None


def ts(s, tz):
    return int(datetime.strptime(s.strip(), '%Y-%m-%d %H:%M:%S').replace(tzinfo=tz).timestamp())


def num(s):
    try:
        v = float(str(s).replace(',', '.').split()[0])
    except (ValueError, IndexError):
        return None
    return None if v <= -900 else v             # -999 = dato non pervenuto


def estremi_astro(rows):
    out = []
    for r in rows or []:
        v = num(r.get('VALORE'))
        if v is None or not r.get('DATA'):
            continue
        out.append([ts(r['DATA'], SOLARE), v, 1 if r.get('minmax') == 'max' else 0])
    return sorted(out)


def livello_medio(e):
    """Media nel tempo della curva a mezzo coseno tra estremi consecutivi."""
    tot = dur = 0
    for a, b in zip(e, e[1:]):
        d = b[0] - a[0]
        if 0 < d < 12 * 3600:
            tot += (a[1] + b[1]) / 2 * d
            dur += d
    return round(tot / dur, 1) if dur else None


def interp(serie, t):
    """serie: lista ordinata di (t, v); interpolazione lineare, None fuori dall'intervallo o su buchi oltre 2 ore."""
    lo, hi = 0, len(serie) - 1
    if hi < 1 or t < serie[0][0] or t > serie[hi][0]:
        return None
    while hi - lo > 1:
        m = (lo + hi) // 2
        if serie[m][0] <= t:
            lo = m
        else:
            hi = m
    a, b = serie[lo], serie[hi]
    if b[0] - a[0] > 7200:
        return None
    return a[1] + (b[1] - a[1]) * (t - a[0]) / (b[0] - a[0])


def taratura(storia, sid):
    """Ritardo e ampiezza della stazione rispetto a Punta Salute, dalle misure delle ultime ore.
    Restituisce (ritardo_min, ampiezza, scarto_cm, n) oppure None se le misure non bastano."""
    ps = sorted((t, v[PS]) for t, v in storia if PS in v)
    st = sorted((t, v[sid]) for t, v in storia if sid in v)
    if len(ps) < 36 or len(st) < 36 or st[-1][0] - st[0][0] < 18 * 3600:
        return None
    if max(v for _, v in ps) - min(v for _, v in ps) < .25:      # escursione troppo piccola per stimare
        return None
    best = None
    for lag in range(-150, 151, 5):
        xs, ys = [], []
        for t, y in st:
            x = interp(ps, t - lag * 60)
            if x is not None:
                xs.append(x); ys.append(y)
        n = len(xs)
        if n < 30:
            continue
        mx, my = sum(xs) / n, sum(ys) / n
        sxx = sum((x - mx) ** 2 for x in xs); syy = sum((y - my) ** 2 for y in ys)
        sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
        if sxx <= 0 or syy <= 0:
            continue
        r = sxy / math.sqrt(sxx * syy)
        if best is None or r > best[0]:
            best = (r, lag, sxy / sxx, (my - mx) * 100, n)
    if not best or best[0] < .9 or not .6 <= best[2] <= 1.4 or abs(best[1]) >= 150:
        return None
    return best[1], round(best[2], 3), round(best[3], 1), best[4]


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    uscita, prec, cartella = args[0], None, None
    if '--prec' in args:
        prec = args[args.index('--prec') + 1]
    if '--da' in args:
        cartella = args[args.index('--da') + 1]
    ora = int(time.time())
    vecchio = {}
    if prec:
        try:
            with open(prec, encoding='utf-8') as f:
                vecchio = json.load(f)
        except Exception:
            vecchio = {}
    out = {'gen': ora, 'fonte': 'Centro Previsioni e Segnalazioni Maree, Comune di Venezia (CC BY) - dati.venezia.it'}

    # previsione ufficiale: massimi e minimi a Punta Salute per circa 72 ore
    p = leggi('previsione.json', cartella)
    est = []
    for r in p or []:
        v = num(r.get('VALORE'))
        if v is None or not r.get('DATA_ESTREMALE'):
            continue
        est.append([ts(r['DATA_ESTREMALE'], ROMA), v, 1 if r.get('TIPO_ESTREMALE') == 'max' else 0])
    est.sort()
    if est:
        out['prev'] = {'t': ts(p[0]['DATA_PREVISIONE'], ROMA) if p[0].get('DATA_PREVISIONE') else ora, 'e': est}
    elif vecchio.get('prev'):
        out['prev'] = vecchio['prev']

    # marea astronomica: estremi da due giorni fa a dodici giorni avanti, e livello medio dell'anno
    anno = datetime.fromtimestamp(ora, SOLARE).year
    a0 = estremi_astro(leggi(f'as{anno}est.json', cartella))
    a1 = estremi_astro(leggi(f'as{anno + 1}est.json', cartella)) if datetime.fromtimestamp(ora, SOLARE).month == 12 else []
    astro = [e for e in a0 + a1 if ora - 2 * 86400 <= e[0] <= ora + 12 * 86400]
    out['astro'] = astro or [e for e in vecchio.get('astro', []) if e[0] >= ora - 2 * 86400]
    out['z0'] = livello_medio(a0) if len(a0) > 100 else vecchio.get('z0')

    # livelli misurati adesso, storia delle ultime ore e taratura delle stazioni
    storia = [h for h in vecchio.get('storia', []) if h[0] >= ora - STORIA_ORE * 3600]
    liv, adesso, t_mis = [], {}, None
    for r in leggi('livello.json', cartella) or []:
        v = num(r.get('valore'))
        la, lo = num(r.get('latDDN')), num(r.get('lonDDE'))
        if v is None or la is None or lo is None or not r.get('data'):
            continue
        t = ts(r['data'], SOLARE)
        sid = str(r.get('ID_stazione'))
        liv.append([sid, r.get('stazione', ''), la, lo, t, v])
        if ora - t < 3600:
            adesso[sid] = v
            t_mis = max(t_mis or 0, t)
    if adesso and t_mis and (not storia or t_mis - storia[-1][0] >= 600):
        storia.append([t_mis, adesso])
    out['liv'] = liv
    out['storia'] = storia
    noti = {s[0]: s for s in vecchio.get('st', [])}
    st = []
    for sid, nome, la, lo, _, _ in liv:
        lag, k = BASE_ST.get(sid, (0, 1.0))
        scarto, n = 0, 0
        tar = None if sid == PS else taratura(storia, sid)
        if tar:
            lag, k, scarto, n = tar
        elif sid in noti and noti[sid][6] > 0:              # tengo l'ultima taratura riuscita
            lag, k, scarto, n = noti[sid][4:8]
        st.append([sid, nome, la, lo, lag, k, scarto, n])
    out['st'] = st or vecchio.get('st', [])

    # temperatura dell'acqua misurata
    tq = []
    for r in leggi('tempacqua.json', cartella) or []:
        v = num(r.get('valore'))
        la, lo = num(r.get('latDDN')), num(r.get('lonDDE'))
        if v is None or la is None or lo is None or not r.get('data') or not 0 < v < 35:
            continue
        tq.append([r.get('stazione', ''), la, lo, ts(r['data'], SOLARE), v])
    out['tacqua'] = tq

    # vento misurato: "gradi, m/s, raffica m/s"; le coordinate vengono dalle stazioni di livello con lo stesso codice
    dove = {s[0]: (s[2], s[3]) for s in liv}
    dove.update({k: v for k, v in {'1029': (45.4453, 12.3361), '1037': (45.412, 12.2615), '1046': (45.25, 12.7727)}.items() if k not in dove})
    vento = []
    for r in leggi('vento.json', cartella) or []:
        sid = str(r.get('ID_stazione'))
        pezzi = [num(x) for x in str(r.get('valore', '')).split(',')]
        if sid not in dove or len(pezzi) < 2 or pezzi[0] is None or pezzi[1] is None or not r.get('data'):
            continue
        raffica = pezzi[2] if len(pezzi) > 2 and pezzi[2] is not None else None
        vento.append([r.get('stazione', ''), dove[sid][0], dove[sid][1], ts(r['data'], SOLARE), round(pezzi[0]) % 360,
                      round(pezzi[1] * 1.94384, 1), None if raffica is None else round(raffica * 1.94384, 1)])
    out['vento'] = vento

    with open(uscita, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, separators=(',', ':'))
    print(f"previsione: {len(out.get('prev', {}).get('e', []))} estremi; astronomica: {len(out['astro'])}; "
          f"livello medio: {out['z0']}; stazioni: {len(liv)}; storia: {len(storia)} rilievi; "
          f"tarate: {sum(1 for s in out['st'] if s[7] > 0)}")
    if not out.get('prev') and not out['astro']:
        sys.exit('nessun dato di marea letto')


if __name__ == '__main__':
    main()
