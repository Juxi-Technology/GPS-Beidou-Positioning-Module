[English](../../en/01-overview/overview.md) | [Deutsch](../../de/01-overview/overview.md) | [Español](../../es/01-overview/overview.md) | Français | [Italiano](../../it/01-overview/overview.md) | [日本語](../../ja/01-overview/overview.md) | [한국어](../../ko/01-overview/overview.md) | [Português (BR)](../../pt-br/01-overview/overview.md) | [Português (PT)](../../pt-pt/01-overview/overview.md) | [简体中文](../../zh-hans/01-overview/overview.md) | [繁體中文](../../zh-hant/01-overview/overview.md)

# Module GPS

Le module GPS est un module de positionnement et de navigation BDS/GNSS haute performance construit autour du **ATGM336H-5N**. Il prend en charge plusieurs systèmes de navigation par satellite — tous les satellites BeiDou-2 et BeiDou-3, GPS, GLONASS et QZSS — et peut les recevoir simultanément pour un positionnement, une navigation et une synchronisation combinés. Il offre une sensibilité élevée, une faible consommation d'énergie et un coût réduit, ce qui le rend adapté à la navigation embarquée, au positionnement portable et aux objets portables connectés.

**1. Caractéristiques**

- Prend en charge tous les satellites BeiDou-2 et BeiDou-3, ID 1–63
- Positionnement mono-système sur BDS / GPS / QZSS, ou toute combinaison de ceux-ci
- Prise en charge de l'A-GNSS
- Sensibilité d'acquisition à froid : -148 dBm
- Sensibilité de poursuite : -162 dBm
- Précision de positionnement : 2,5 m (CEP50)
- Temps jusqu'au premier fix : 32 s
- Faible consommation : 25 mA @ 3,3 V en continu
- Détection d'antenne intégrée et protection contre les courts-circuits d'antenne

**2. Interface**

![interface du module](../../en/01-overview/images/1.png)

**3. Protocole de communication**

Pour le protocole complet, voir `../../datasheets/CASIC-GNSS-protocol-spec-CN.pdf` (en chinois).
