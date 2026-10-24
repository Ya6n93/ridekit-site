---
title: "Privacy Policy — RideKit"
description: "What RideKit keeps on your phone, what leaves it, where to and why. No account, no RideKit server, no ads."
permalink: /en/privacy/
alternate: /confidentialite/
layout: legal
lang: en
---

# Privacy Policy

*Last updated: 24 October 2026*

RideKit is a motorcycle riding app: it draws loops and routes, guides you, shows the
weather, and keeps your ride journal and your bike's records. This page says exactly
what data exists, where it stays, what leaves your phone, where to, and why. The
French version ([Politique de confidentialité](/confidentialite/)) prevails.

> **In short.** No account, no RideKit server. Your rides, your bike, your emergency
> contact and your settings stay on your phone: we have no copy of them. To compute a
> route or show a map or the weather, the app queries specialised services directly,
> sending them coordinates — never your name, your nickname or an advertising
> identifier. No ads, no analytics, no tracking, no data sales.

## 1. Who is responsible

The data controller is **Yassine Latrach, sole proprietor (entrepreneur individuel,
EI), trading as SZ CORP** — SIREN 884 872 623 — 200 rue de la Croix Nivert, 75015
Paris, France ("SZ CORP", "we"). Contact: **contact@ridekit-app.com**.

For Québec's Law 25, the person in charge of the protection of personal information
is Yassine Latrach, at the same address.

## 2. No account, no RideKit server

RideKit asks for no sign-up, e-mail address or phone number. SZ CORP runs no server
that would receive what you do in the app: we see neither your rides, nor your
location, nor your bike, nor your emergency contact. The only personal data we may
receive is what you send us yourself, such as a support e-mail.

## 3. What stays on your phone

Stored in the app's private storage, on your device, never sent to us:

- your nickname (optional) and settings (units, theme, alerts, speed tolerance,
  preferred road style and ride length);
- your bike: make, model, year, odometer, services logged and intervals; the photo
  you pick, copied into the app;
- your ride journal: date, distance, duration, GPS track ridden, statistics;
- the ride in progress, saved along the way so it can be resumed if the app is closed;
- routes already computed, kept so they can be shown again without being recomputed;
- GPX, KML or TCX tracks you import, and your recent or saved destinations;
- your emergency contact (name, number) and the crash alert delay;
- offline maps you download for a ride, deleted automatically after 14 days (300 MB
  at most in total);
- the official list of fixed speed cameras (for danger zones), the motorcycle make and
  model database, and the number of loops generated this month.

Depending on your phone's settings, this data may be included in its backup (iCloud,
Google), under your account and Apple's or Google's rules.

**Deleting it.** In Réglages › Données, "Effacer le carnet" deletes your rides and the
total distance; "Réinitialiser l'app" erases your bike, journal, emergency contact and
settings. Deleting the app erases everything it stored on the phone, including your
bike's photo, imported tracks and offline maps.

## 4. What leaves your phone, where to, and why

Some features need online data. The app then contacts the service directly, from your
phone, when you use the feature. Like any web server, each one receives your **IP
address** and technical details of the request. No request contains your name,
nickname, bike or an advertising identifier.

| Service | What for | What is sent |
|---|---|---|
| **TomTom** (TomTom International B.V., Netherlands) | Loops and routes, rerouting, speed limits along the way, cafés and restaurants along a ride | Coordinates of the start (usually your location), waypoints and destination; when rerouting, your location and heading; points of the route |
| **OSRM** demo server (FOSSGIS e.V., Germany) | Fallback route when TomTom doesn't answer | Waypoint coordinates |
| **Photon** (komoot GmbH, Germany) | Address and place search, your town's name for the weather, nearby passes | What you type; your location, to rank results and find your town or nearby passes |
| **Open-Meteo** (OpenMeteo GmbH, Switzerland) | Current weather, forecasts, weather at passes and along the ride | Your location, or a pass's or a ride point's |
| **RainViewer** | Rain radar | No location: only the images of the map area shown |
| **OpenFreeMap** (Hyperknot Software Kft., Hungary) | Base map, offline maps | Tiles of the area shown or of the ride's corridor; the app names itself and its version, as OpenFreeMap requires |
| **Open Topo Data** | Elevation profile of a ride, passes' elevation | Points along the route |
| **Wikipedia** (Wikimedia Foundation, USA) | Passes and sights along the ride, with summary and photo | Points along the route; the title of the page shown |
| **Fuel prices** (data.economie.gouv.fr, French Ministry of the Economy) | Fuel stations and today's prices, in France | Your location or route points |
| **data.gouv.fr** (France) | Official list of fixed speed cameras, checked at most once a week | Nothing about you |
| **Bike database** (public file published by SZ CORP) | New edition of the motorcycle list, checked at most once a week | Nothing about you |
| **Unsplash** | Illustration photos on some screens | Nothing about you |
| **Expo** (650 Industries, Inc., USA) | App updates | Technical details: system, app version, a technical installation identifier created by the update service |
{: .services}

A precise location can, combined with others, reveal places you go to: a loop often
starts at home. That is why it is only sent when a feature needs it, and only to the
service that handles it. Without a network, nothing is sent.

A few actions leave the app at your request: importing a track from a link (that
link's website receives the request), sharing an exported track (to the app you pick),
opening a Wikipedia page (in your browser), getting directions to a station (in your
phone's maps app).

Each of these services applies its own privacy policy, for instance
[TomTom](https://www.tomtom.com/privacy/), [Open-Meteo](https://open-meteo.com/en/terms)
(logs deleted after 90 days), [OpenFreeMap](https://openfreemap.org/privacy/) (logs
deleted after 7 days), [Wikimedia](https://foundation.wikimedia.org/wiki/Policy:Privacy_policy),
[Expo](https://expo.dev/privacy).

## 5. Your location

RideKit asks for your location **while using the app**. It is used to show you on the
map, start loops from where you are, guide you, measure your speed and lean angle,
record your ride in the journal, show the weather and fuel stations around you,
announce danger zones and, if you turn it on, for crash detection.

During a guided ride, guidance keeps going with the screen locked or another app in
front, as in a navigation app: the iPhone shows the blue location indicator, Android
the "RideKit · guidage en cours" notification. It stops on arrival or when you end the
ride. RideKit does not ask for "Always" location access and does not follow your
location when the app is not in use. The app also reads the phone's compass, to orient
the map.

You can refuse or withdraw access at any time in your phone's settings: the features
that need it will stop working.

## 6. Crash detection and emergency contact

Crash detection is **off by default**: you turn it on.

- **What it reads.** During a guided ride only, the phone's accelerometer and GPS
  speed, analysed on the phone. These readings are neither stored nor sent. RideKit
  uses neither the gyroscope, nor the step counter, nor your health data.
- **Your contact.** You pick them in the phone's contact picker, which gives RideKit
  only the contact chosen (name and number), or you type the number. It stays on your
  phone. RideKit doesn't read your address book and never writes to it.
- **On an alert.** An alarm rings and a countdown starts. Without an answer from you, a
  message is prepared for your contact: your nickname, the time, your last known
  location (a Google Maps link and GPS coordinates). In the current version, this
  message opens in the phone's messaging app and is only sent if someone taps "Send";
  it then goes through your carrier, like any text. RideKit sends nothing to SZ CORP
  and does not contact emergency services. If your contact opens the link, Google
  receives the coordinates, under its own policy.

Should automatic sending ever be added, this page will say, before it goes live, what
it sends, to whom and through which provider.

## 7. Photos, contacts, files

- **Photos.** For your bike's photo, RideKit opens the system photo picker: only the
  photo chosen is copied into the app. RideKit doesn't access your photo library and
  doesn't use the camera.
- **Contacts.** See above: only the contact chosen is read. On Android, the system may
  ask for contacts access to open this picker.
- **Files.** Tracks you import from Files (iCloud Drive included) are copied into the
  app. Tracks you export go to the app you pick in the share sheet.
- RideKit doesn't use the microphone.

## 8. Notifications

All of RideKit's notifications are **local**: maintenance reminders (if you turn them
on), crash alerts, and on Android the ongoing guidance notification. They are
scheduled by your phone: there is no push server, no notification token sent, and we
cannot know whether you received or opened them.

## 9. Purchases

Any in-app purchase (RideKit Pro) is processed by Apple (App Store) or Google (Google
Play). SZ CORP sees neither your payment method, nor your Apple or Google ID, nor your
address. As of today, the app contains no third-party purchase management tool; if one
is added, it will be named here, with what it receives, before it goes live.

## 10. What RideKit doesn't do

- No account, no ads, no advertising identifier, no cross-app or cross-site tracking.
- No analytics tool, no third-party crash reporting tool.
- No profiling, no automated decision about you, no sale or rental of data.

Apple and Google, who distribute the app, may give us aggregate statistics (downloads,
crashes) if you agreed, in your phone's settings, to share analytics with developers.
They do not identify you.

## 11. Legal bases (GDPR)

- **The service you ask for** (Art. 6(1)(b)): sending coordinates to compute a route
  or show a map, the weather, places or prices.
- **Your consent** (Art. 6(1)(a)): location, notifications, crash detection, the photo
  and the contact you pick. You withdraw it at any time, in the app or in your phone's
  settings.
- **Our legitimate interest** (Art. 6(1)(f)): answering your support messages, keeping
  the app up to date and secure.

## 12. How long

- **On your phone**: until you delete it or the app. Offline maps go by themselves
  after 14 days; the ride in progress as soon as it is saved or discarded.
- **At SZ CORP**: nothing, except your support e-mails, kept while we handle your
  request and at most three years after our last exchange.
- **At third-party services**: under their own policies (see section 4).

## 13. Where data goes

TomTom (Netherlands), FOSSGIS (Germany), komoot (Germany) and OpenFreeMap (Hungary) are
in the European Union; Open-Meteo is in Switzerland, which the EU recognises as
providing adequate protection. Wikipedia, Expo, Unsplash, RainViewer, Open Topo Data
and the delivery networks some of these services use may process data outside the
EU, notably in the United States, where authorities may access it under their law.

These transfers rely, as the case may be, on an adequacy decision (for example the
Data Privacy Framework for certified US companies) or on their necessity to provide the
service you ask for (Art. 49 GDPR). For Québec, Switzerland and the rest of Canada:
your information may therefore be communicated outside your province or country, to
the countries listed here.

## 14. Your rights

Wherever you live, you can ask for access to your data, its correction, erasure,
restriction, objection to its processing, its portability, and withdraw your consent.
In France, you can also give instructions on what happens to your data after your
death.

As almost everything stays on your phone, you exercise most of these rights yourself,
in the app (section 3). For the rest, write to **contact@ridekit-app.com**: we answer
within one month. We have no copy of what the app sends to third-party services, and
no way to link their requests to you; for that data, contact them directly.

You can also complain to your country's authority:

| Country | Law | Authority |
|---|---|---|
| France | GDPR, Loi Informatique et Libertés | [CNIL](https://www.cnil.fr) |
| Belgium | GDPR | [Data Protection Authority](https://www.dataprotectionauthority.be) |
| Luxembourg | GDPR | [CNPD](https://cnpd.public.lu) |
| Switzerland | Federal Act on Data Protection (nFADP) | [Federal Data Protection and Information Commissioner](https://www.edoeb.admin.ch) |
| Québec | Law 25 (Act respecting the protection of personal information in the private sector) | [Commission d'accès à l'information](https://www.cai.gouv.qc.ca) |
| Canada | PIPEDA | [Office of the Privacy Commissioner of Canada](https://www.priv.gc.ca) |
{: .authorities}

For Law 25: location is only used if you allow it (section 5), and crash detection is
off until you turn it on (section 6).

## 15. Children

RideKit is meant for riders of powered two-wheelers. It is not intended for children
under 13 and does not knowingly collect any data about them.

## 16. Security

Your data is in the app's private storage, protected by your phone's encryption and
passcode: set one. Exchanges with the services in section 4 are encrypted (HTTPS).

## 17. This website

ridekit-app.com sets no cookies, has no analytics and loads nothing from third
parties. It is hosted by GitHub (see the [legal notice](/mentions-legales/), in French),
which may log visitors' IP addresses for the security of its service.

## 18. Changes

Any change to this policy is published on this page, with a new date. A change that
would make new data leave your phone would be announced in the app before taking
effect.

## 19. Contact

**contact@ridekit-app.com** — SZ CORP (Yassine Latrach EI), 200 rue de la Croix
Nivert, 75015 Paris, France.
