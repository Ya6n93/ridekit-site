---
title: "Privacy Policy — RideKit"
description: "What RideKit keeps on your phone, what leaves it, where to and why. No account, no ads, one server: the crash alert's."
permalink: /en/privacy/
alternate: /confidentialite/
layout: legal
lang: en
---

# Privacy Policy

*Last updated: 25 October 2026*

RideKit is a motorcycle riding app: it draws loops and routes, guides you, shows the
weather, and keeps your ride journal and your bike's records. This page says exactly
what data exists, where it stays, what leaves your phone, where to, and why. The
French version ([Politique de confidentialité](/confidentialite/)) prevails.

> **In short.** No account. Your rides, your bike, your emergency contact and your
> settings stay on your phone: we have no copy of them. One exception, if you turn
> crash detection on: so that an alert goes out even if you can't answer, RideKit's
> alert server receives, at that moment, what the text says, and has it sent to your
> contact. It keeps neither your location, nor the text, nor your contact's number
> (section 6). To compute a route or show a map or the weather, the app queries
> specialised services directly, sending them coordinates — never your name, your
> nickname or an advertising identifier. No ads, no analytics, no tracking, no data
> sales.

## 1. Who is responsible

The data controller is **Yassine Latrach, sole proprietor (entrepreneur individuel,
EI), trading as SZ CORP** — SIREN 884 872 623 — 200 rue de la Croix Nivert, 75015
Paris, France ("SZ CORP", "we"). Contact: **contact@ridekit-app.com**.

For Québec's Law 25, the person in charge of the protection of personal information
is Yassine Latrach, at the same address.

## 2. No account, one server

RideKit asks for no sign-up, e-mail address or phone number. We see neither your
rides, nor your bike, nor your settings.

SZ CORP runs one server only: the **alert server**, which sends the crash alert to
your contact without anyone touching the phone (section 6). It receives something at
three moments only: when you register your contact, on an alert, and when you test
it. It keeps only what it needs to know whom to text and to prevent abuse.

The other personal data we may receive is what you send us yourself, such as a
support e-mail.

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

Added to it, if automatic alert sending is set up: the random token the alert server
gave your phone, which the app shows it with each request (section 6).

Depending on your phone's settings, this data may be included in its backup (iCloud,
Google), under your account and Apple's or Google's rules.

**Deleting it.** In Réglages › Données, "Effacer le carnet" deletes your rides and the
total distance; "Réinitialiser l'app" erases your bike, journal, emergency contact and
settings, and asks the alert server to forget your phone and your contact. Deleting the app erases everything it stored on the phone, including your
bike's photo, imported tracks and offline maps.

## 4. What leaves your phone, where to, and why

Some features need online data. The app then contacts the service directly, from your
phone, when you use the feature. Like any web server, each one receives your **IP
address** and technical details of the request. No request contains your name, bike
or an advertising identifier; your nickname only goes to the alert server, for the
text.

| Service | What for | What is sent |
|---|---|---|
| **TomTom** (TomTom International B.V., Netherlands) | Loops and routes, rerouting, speed limits along the way, cafés and restaurants along a ride; address and place search outside France, or when IGN finds nothing, and naming a place outside France | Coordinates of the start (usually your location), waypoints and destination; when rerouting, your location and heading; points of the route; for a search, what you type and your location, to rank results around you; the coordinates of a point to name |
| **OSRM** demo server (FOSSGIS e.V., Germany) | Fallback route when TomTom doesn't answer | Waypoint coordinates |
| **IGN** Géoplateforme (French national mapping agency, France) | Address and place search in France, your town's name (home, weather) and the names of points placed on the map, nearby passes when Photon doesn't answer | What you type; your location, to rank results around you; the coordinates of a point to name |
| **Photon** (komoot GmbH, Germany) | Nearby passes; address and place search and naming a point when IGN and TomTom don't answer | What you type; your location, to rank results and find nearby passes; the coordinates of a point to name |
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
| **RideKit's alert server**, hosted by **Cloudflare** (Cloudflare, Inc., USA) | Automatic sending of the crash alert (section 6), if detection is on with a contact | When the contact is registered: their number, nothing else. On an alert or a test: their number, your nickname, the time of the impact and the phone's time zone, your speed just before, your location and how precise it is, the battery |
| **Brevo** (Brevo SAS, formerly Sendinblue, France), for the alert server | Sending RideKit's alert to your contact, as a single text | Your contact's number and the text: your nickname, the time, your location and how precise it is, the battery and, if there is room, your speed |
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
[Expo](https://expo.dev/privacy), [Cloudflare](https://www.cloudflare.com/privacypolicy/),
[Brevo](https://www.brevo.com/legal/privacypolicy/).

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

- **What it reads.** During a guided ride only, the phone's accelerometer and
  gyroscope and the GPS speed, analysed on the phone. These readings are neither
  stored nor sent. RideKit uses neither the step counter nor your health data.
- **Your contact.** You pick them in the phone's contact picker, which gives RideKit
  only the contact chosen (name and number), or you type the number. It stays on your
  phone; the alert server keeps only a fingerprint of it (below). RideKit doesn't read
  your address book and never writes to it.
- **On an alert.** An alarm rings and a countdown starts. Without an answer from you,
  or if you ask for help, a single text goes to your contact: your nickname, the time
  of the impact, your last known location and how precise it is (a Google Maps link,
  which carries the GPS coordinates), the phone's battery level and, if there is
  room, your speed just before. It goes by itself, through the alert server and
  Brevo. If the server can't be reached or refuses, the message opens in the phone's messaging app and is only sent if someone
  taps "Send"; it then goes through your carrier, like any text. RideKit lets your
  close one know: it does not call emergency services. If your contact opens the
  link, Google receives the coordinates, under its own policy.
- **Automatic sending.** It comes with crash detection: as soon as detection is on
  with a contact, the alert goes by itself. To stop it, turn detection off or remove
  your contact.
  - *When your contact is registered*, as you pick them with detection on: the server
    gives your phone a random token, then receives your contact's number, and only
    that. It sends your contact nothing. It keeps a fingerprint of the number (a
    keyed HMAC, from which the number can't be recovered), not the number itself, nor
    their name.
  - *On an alert, or a test* ("Tester l'envoi automatique", once a day, a RideKit Pro
    feature; without Pro, the test text is prepared on your phone): the app sends the
    server your contact's number, your nickname, the time of the impact and the
    phone's time zone, your speed just before, your location and how precise it is,
    the battery. The server checks it is the contact registered for your phone,
    writes the text itself, a single one, and hands it to Brevo. Without a network,
    the app keeps trying for 5 minutes.
  - *What is kept.* Neither your location, nor the texts, nor your nickname, nor your
    IP address. Only: your phone's token and the fingerprint of your contact's number;
    the day's counters (per phone, per number and IP address fingerprint, for the
    whole service), which cap sending against abuse and are deleted the next day; the
    id of each of the day's alerts, so it is never sent twice. The server's logs say
    what happened (sent, refused), with no number or location, and are kept 3 days.
  - *When it forgets.* Turn detection off or remove your contact: the server
    forgets your contact. "Réinitialiser l'app" makes it forget your phone. Without
    news from your phone for 400 days, it forgets it by itself.
  - *Providers.* The server runs on Cloudflare, what it keeps being placed in the
    European Union where Cloudflare offers it; texts go through Brevo, in France,
    which keeps its data in the European Union. Both act on behalf of SZ CORP. Brevo
    keeps the log of each text (the number, the text, its status) for one month, then
    deletes it. To deliver it, Brevo goes through partner carriers, some of them
    American, which may keep a technical record of it
    under their own policy.
  - *Countries.* For now, automatic sending only goes to French mobile numbers. For
    any other number, the text is prepared on your phone, as without the server.
- **Your contact, informed by you.** RideKit only texts them on an alert or a test.
  You are the one who tells them: as soon as you pick them, the app prepares a text
  saying they are your emergency contact and what would follow. It goes from your
  phone, when you tap "Send". If they don't want to receive alerts, remove them or
  turn detection off; they can also write to us at
  **contact@ridekit-app.com**.

## 7. Photos, contacts, files

- **Photos.** For your bike's photo, RideKit opens the system photo picker, or the
  camera if you choose to take it: only that photo is copied into the app. RideKit
  doesn't access your photo library. The camera only opens when you tap "Camera",
  once you've allowed it.
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
- **Your consent** (Art. 6(1)(a)): location, notifications, crash detection and its
  automatic sending, the photo and the contact you pick. You withdraw it at any time,
  in the app or in your phone's settings.
- **Your vital interests** (Art. 6(1)(d) and 9(2)(c)): on an unanswered alert, letting
  your contact know when you may no longer be able to, an alert suggesting you may be
  hurt.
- **Our legitimate interest** (Art. 6(1)(f)): answering your support messages, keeping
  the app up to date and secure, preventing abuse of the alert server; for your
  contact, getting them the alert you wanted, which you tell them about yourself,
  with the text the app prepares for you.

## 12. How long

- **On your phone**: until you delete it or the app. Offline maps go by themselves
  after 14 days; the ride in progress as soon as it is saved or discarded.
- **At SZ CORP**: your support e-mails, kept while we handle your request and at most
  three years after our last exchange; and, if automatic sending is set up, what the
  alert server keeps (section 6): the token and your contact's number fingerprint as
  long as they are registered (at most 400 days without news), the counters until the
  next day; at Brevo, on our behalf, the log of each text sent (number, text, status),
  one month.
- **At third-party services**: under their own policies (see section 4).

## 13. Where data goes

IGN (France), TomTom (Netherlands), FOSSGIS (Germany), komoot (Germany), OpenFreeMap (Hungary) and
Brevo (France, the alert server's texts) are in the European Union; Open-Meteo is in
Switzerland, which the EU recognises as providing adequate protection. Wikipedia,
Expo, Unsplash, RainViewer, Open Topo Data, Cloudflare (alert server), the carriers
Brevo delivers some texts through (to a Canadian mobile, Twilio) and the delivery
networks some of these services use may process data outside the EU, notably in the
United States, where authorities may access it under their law.

These transfers rely, as the case may be, on an adequacy decision (for example the
Data Privacy Framework for certified US companies, such as Cloudflare), on
the European Commission's standard contractual clauses, or on their necessity to
provide the service you ask for (Art. 49 GDPR). For Québec, Switzerland and the rest of Canada:
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
no way to link their requests to you; for that data, contact them directly. The alert
server knows neither your name nor your contact's number in clear: to have it forget
your contact, turn detection off, remove your contact or reset the app. The log of an alert text at
Brevo, we delete on request, without waiting for the month.

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
passcode: set one. Exchanges with the services in section 4 are encrypted (HTTPS). The alert
server only sends texts for a phone it gave a signed token to, only to the contact
registered for that phone, only to mobile numbers in the five countries of section 6,
and in limited numbers each day.

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
