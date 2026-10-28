---
title: "Importer un GPX sur iPhone pour la moto : trace, route et pièges"
date: 2026-10-28 00:21:00 +0100
description: "Importer un GPX sur iPhone pour la moto : trace ou route, où trouver des traces gratuites, ouvrir le fichier avec Fichiers ou AirDrop, et les pièges à éviter."
category: applis
tags: [gpx, iphone, trace, navigation]
keyword: "importer gpx iphone moto"
lede: "Un GPX est un petit fichier qui décrit un parcours. Sur iPhone, tu le retrouves dans l'app Fichiers, puis tu l'ouvres dans l'app qui va le suivre. Dans RideKit, l'import GPX, KML, KMZ et TCX est gratuit, dans un sens ou dans l'autre."
faq:
  - q: "Comment ouvrir un fichier GPX sur iPhone ?"
    a: "Un GPX téléchargé dans Safari arrive dans le dossier Téléchargements de l'app Fichiers. De là, maintiens le doigt sur le fichier, touche Partager et choisis l'app de navigation, ou ouvre cette app et importe le fichier depuis Fichiers."
  - q: "Quelle différence entre une trace et une route GPX ?"
    a: "Une trace est une suite de points qui dessine le chemin exact. Une route est une liste de points de passage : l'application recalcule elle-même le chemin entre eux, qui peut différer de celui prévu par l'auteur."
  - q: "Où trouver des traces GPX moto gratuites ?"
    a: "Le Roadbook de RideKit propose une trace GPX gratuite sur chacune de ses 97 pages de road trip. Les offices de tourisme et certains départements, comme l'Hérault sur data.gouv.fr, publient aussi des circuits moto en données ouvertes."
  - q: "Peut-on suivre une trace GPX sans réseau ?"
    a: "Oui si l'application propose des cartes hors ligne. Dans RideKit, l'import de la trace est gratuit et le téléchargement de la carte pour rouler hors ligne fait partie de RideKit Pro."
sources:
  - title: "GPX 1.1 Schema Documentation"
    publisher: "TopoGrafix"
    url: "https://www.topografix.com/GPX/1/1/"
  - title: "GPX: the GPS Exchange Format"
    publisher: "TopoGrafix"
    url: "https://www.topografix.com/gpx.asp"
  - title: "Fichiers KMZ"
    publisher: "Google for Developers"
    url: "https://developers.google.com/kml/documentation/kmzarchives?hl=fr"
  - title: "Training Center XML"
    publisher: "Wikipédia (en anglais)"
    url: "https://en.wikipedia.org/wiki/Training_Center_XML"
  - title: "Où trouver des téléchargements sur votre iPhone ou iPad"
    publisher: "Assistance Apple"
    url: "https://support.apple.com/fr-fr/102440"
  - title: "Envoyer des fichiers depuis l'app Fichiers sur l'iPhone"
    publisher: "Assistance Apple"
    url: "https://support.apple.com/fr-fr/guide/iphone/iphf2746307f/ios"
  - title: "Utiliser AirDrop sur l'iPhone pour envoyer des éléments à des appareils à proximité"
    publisher: "Assistance Apple"
    url: "https://support.apple.com/fr-fr/guide/iphone/iphcd8b9f0af/ios"
  - title: "Circuits moto de l'Hérault"
    publisher: "Département de l'Hérault, data.gouv.fr"
    url: "https://www.data.gouv.fr/datasets/circuits-moto-de-lherault"
---

Pour importer un GPX sur iPhone et le suivre à moto, il faut deux choses : **retrouver le fichier** (presque toujours dans l'app Fichiers) et **l'ouvrir dans une app de navigation** qui sait le lire. Avant ça, un mot sur ce que contient vraiment un GPX, parce que c'est là que naissent la plupart des mauvaises surprises.

## Ce qu'est un fichier GPX : trace, route, points de passage

GPX est un format ouvert, en XML, fait pour échanger des données GPS entre applications et appareils. Sa version actuelle, la 1.1, date de 2004 ([TopoGrafix](https://www.topografix.com/gpx.asp)). Un fichier peut contenir trois choses, que la [documentation officielle](https://www.topografix.com/GPX/1/1/) définit ainsi :

- **Les points de passage** (wpt) : un point d'intérêt ou un lieu nommé sur la carte. Un café, un col, un point de rendez-vous.
- **La route** (rte) : une liste ordonnée de points de passage, les points où tourner pour aller à destination.
- **La trace** (trk) : une liste ordonnée de points qui décrit un chemin, découpée en segments.

### Trace ou route GPX : la différence qui compte

Une **trace** dessine le chemin exact, point par point : c'est ce que tu veux pour suivre la route choisie par quelqu'un d'autre. Une **route** ne donne que les étapes : c'est l'application qui recalcule le chemin entre elles, avec ses propres réglages. Deux applis peuvent donc tracer deux chemins différents à partir du même fichier route, et aucun n'est forcément celui que l'auteur avait en tête. Pour une balade sur petites routes, préfère une trace.

### GPX, KML, KMZ, TCX : les autres formats

| Format | D'où il vient | Ce qu'il contient | Dans RideKit |
|---|---|---|---|
| GPX | Standard ouvert (TopoGrafix) | Points de passage, routes, traces | Import gratuit, export avec Pro |
| KML | Google Earth | Points, lignes, formes, styles d'affichage | Import gratuit |
| KMZ | Google Earth | Un KML et ses fichiers, compressés en zip ([Google](https://developers.google.com/kml/documentation/kmzarchives?hl=fr)) | Import gratuit |
| TCX | Garmin (Training Center) | Activités sportives : tours, temps, données d'entraînement | Import gratuit |

## Où trouver une trace GPX moto gratuite

- **Le [Roadbook de RideKit](/roadbook-moto/)** : 97 road trips moto en France, chacun avec sa page et sa **trace GPX gratuite** à télécharger. Les itinéraires viennent de données ouvertes, publiées par les acteurs du tourisme via DATAtourisme et par le Département de l'Hérault.
- **Les offices de tourisme et agences départementales** : beaucoup publient des circuits « motorisés » ou « moto ». Le road trip de 5 jours en Aveyron, par exemple, a été tracé par l'agence touristique du département.
- **data.gouv.fr** : le Département de l'Hérault y publie ses [circuits moto](https://www.data.gouv.fr/datasets/circuits-moto-de-lherault) sous Licence Ouverte.
- **Les copains et les clubs** : une trace exportée d'une autre appli ou d'un GPS se partage comme n'importe quel fichier.

{% include trip-card.html url="/roadbook-moto/occitanie/l-aveyron-a-moto-de-laguiole-a-millau/" %}

Le détail de ce road trip, étape par étape, est dans [notre article sur l'Aveyron à moto](/blog/road-trip-moto-aveyron/).

## Ouvrir un fichier GPX sur iPhone

Le fichier arrive par trois chemins. Dans tous les cas, fais-le **à l'arrêt, avant de partir**.

1. **Téléchargé dans Safari** : il va dans le dossier **Téléchargements** de l'app **Fichiers** (onglet Explorer, iCloud Drive, Téléchargements). Juste après le téléchargement, le bouton Téléchargements à côté du champ de recherche de Safari y mène directement ([Assistance Apple](https://support.apple.com/fr-fr/102440)).
2. **Reçu par AirDrop**, depuis un Mac ou un autre iPhone : touche Accepter. Entre tes propres appareils connectés au même compte Apple, c'est accepté automatiquement. Sur iPhone, certains éléments sont enregistrés dans l'app Fichiers ([Assistance Apple](https://support.apple.com/fr-fr/guide/iphone/iphcd8b9f0af/ios)).
3. **Reçu en pièce jointe** (Mail, Messages) : maintiens le doigt sur la pièce jointe et enregistre-la dans Fichiers, ou partage-la directement vers ton app.

Ensuite, deux façons d'ouvrir le fichier :

- **Depuis Fichiers** : maintiens le doigt sur le fichier, touche **Partager** et choisis l'application ([Assistance Apple](https://support.apple.com/fr-fr/guide/iphone/iphf2746307f/ios)). Les apps de navigation qui savent lire ce type de fichier y apparaissent.
- **Depuis l'application** : ouvre-la et utilise sa fonction d'import, qui te fait choisir le fichier dans Fichiers.

> **Bon à savoir.** Si ton app de navigation n'apparaît pas dans la feuille Partager, ouvre-la et passe par sa propre fonction d'import : le résultat est le même.
{: .note}

## Suivre la trace dans RideKit

Dans RideKit, l'**import de traces est gratuit**, en GPX, KML, KMZ et TCX.

{% include shot.html name="gpx-import" caption="Importer un GPX dans RideKit : ici, un fichier qui contient deux traces." %}

1. Sur l'accueil, touche **Importer un GPX**, puis **Choisir un fichier**, et sélectionne-le dans Fichiers. RideKit apparaît aussi dans la feuille Partager de l'iPhone pour ces fichiers.
2. Si le fichier contient plusieurs traces, RideKit te les montre avant l'import.
3. La trace s'affiche sur la carte avec sa distance, sa durée estimée et sa sinuosité.
4. Si tu veux faire la boucle à l'envers, touche **Inverser le sens**.
5. Touche **Démarrer** : le guidage vocal tour par tour est gratuit, écran verrouillé compris.

{% include shot.html name="gpx-trace" caption="Une trace importée, du lac d'Annecy aux Aravis : 81 km, sinuosité 6,6 sur 10." %}

Avant de partir, regarde le **profil d'altitude** et la liste des **cols** sur le parcours : ça dit tout de suite si la journée sera tranquille ou montagnarde.

{% include shot.html name="gpx-profil-cols" caption="Le profil d'altitude d'une trace importée, 2 174 m de montée, et les cols sur le parcours." %}

> **RideKit Pro.** Avec RideKit Pro, tu peux **exporter tes balades en GPX** pour les partager ou les charger dans un GPS, et **télécharger la carte** d'une balade pour rouler hors ligne. Le détail est sur la page [GPX moto](/gpx-moto/).
{: .note-pro}

## Les pièges d'une trace GPX à moto

- **La route recalculée.** Un fichier route (rte), ou une appli qui « recalcule » la trace pour la caler sur ses propres routes, peut te faire passer ailleurs que prévu. Compare le tracé affiché avec la carte d'origine avant de partir.
- **La trace trop dense.** Une trace enregistrée par un GPS ou une montre peut compter des dizaines de milliers de points, un point toutes les secondes. Certaines applis et certains GPS lisent mal ces fichiers lourds : une version simplifiée suffit pour suivre la route.
- **Les routes fermées.** Une trace ne sait rien des travaux, des cols fermés l'hiver ou des routes coupées après un orage. Elle a pu être tracée il y a des années. En montagne, vérifie l'ouverture des cols avant de partir.
- **Le sens interdit et les chemins interdits.** Une trace enregistrée à vélo, à pied ou en tout-terrain peut emprunter une voie à sens unique, un chemin fermé aux véhicules à moteur ou une piste. Les panneaux priment toujours sur la trace : le Code de la route s'applique.
- **Le mauvais sens de la boucle.** Une boucle se fait dans les deux sens, mais le point de départ et le sens changent tout : soleil dans les yeux, montées ou descentes, pauses. Inverse-la si besoin avant de démarrer.
- **La batterie.** Suivre une trace avec l'écran allumé consomme. Pars chargé, avec un câble sur la moto si possible, et un support qui protège le téléphone : voir [téléphone sur la moto, support et vibrations](/blog/telephone-moto-support-vibrations/).

> **Attention.** Ne manipule pas ton téléphone en roulant. Charge la trace, vérifie-la et lance le guidage à l'arrêt, puis laisse la voix te guider.
{: .note-warn}

## Pas de GPX sous la main ?

Tu n'as pas besoin d'un fichier pour rouler. RideKit trace une [boucle en un tap](/generateur-balade-moto/) autour de toi selon la durée et le type de route, ou un [itinéraire](/itineraire-moto/) de A à B ou par points. Et pour comparer les applications qui lisent les GPX, voir notre [comparatif des applications GPS moto](/blog/comparatif-applications-gps-moto/).
