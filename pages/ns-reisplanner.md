---
layout: page
title: Portfolio - NS Reisplanner
show_in_nav: false
permalink: /portfolio/ns-reisplanner/
---

In 2011 I joined my colleague in a new project that Xebia scored, the NS Reisplanner app. Until then, the NS Reisplanner app was built and managed by a supplier, I forgot which but one of the well-known app developer clubs in the Netherlands. The challenge that NS faced was that the app's codebase was owned by the developing company (apparently). NS wanted them to make a change to support the new pricing scheme that the NS was going to introduce at the end of the year, but the developing party only wanted to do it if they could rebuild the app in their own framework - or something like that, the exact details are a bit vague to me. Either way, the NS and the main guy responsible for the app was like "yeah no" and started looking for another partner, also seeing the potential that the app could have.

They opened up pitches, and two of my Xebia colleagues made a bid - they put together a simple app based on the NS public API in an afternoon and took that to pitch day. That + a competitive price got us the assignment.

I was still an apprentice at the time (in name, in skill level I could easily keep up; my colleague in that project had 15+ years of experience in all departments of Xebia and praised my skills at the time), and wasn't on any assignments at the time so I was asked to join. A few days later I was set up with a loaner Macbook and we got to work on rebuilding the app.

Because the codebase was owned by another company, we could (well, had to) work from scratch; the client wanted us to rebuild the app, reuse the design and features, and make the change in the prices. We managed to rebuild the app, about 12 or so screens, in six weeks. If I do say so myself we even improved on the existing app, it had a few graphical glitches (using iOS components the wrong way or something). We connected a number of APIs, some from the NS itself (xml, mix of Dutch and English tag names), some third party ones like TomTom Places (points of interest).

After the first version was live, we focused on enabling push notifications, to give travelers updates on their planned journeys. The NS did not have any push-based notification system for updates like that, so what we made was a system that would call the API with the user's journey information 15 minutes before departure; if there was a status change or delay, the system would send a push notification to users. Far from ideal but it worked. The push notification service was one of the first projects at Xebia that we built in Scala and Akka, and it could easily send tens of thousands of messages a minute on a single machine. It used MongoDB for persistence, which probably wasn't an ideal choice, a regular database would've sufficed.

We did some side-projects and proof-of-concepts too. During the half year or so that I worked for NS, at one point the old mechanical sign in Utrecht Centraal was slated to be replaced; the company that made it and parts for it (and the mechanical train station signs) had gone out of business a while ago, and they were running out of parts. My colleague and the UX designer that joined us later went to Utrecht Centraal to make pictures, sound recordings and observe the behaviour of the old sign. My colleague spent a weekend making an animation of one of the flipping signs, which we used in the next week to create a grid on the iPad, replicating the sign as closely as possible - even including some of the broken signs.

The result was the NS Blauwe Bord app, we built it in a week to display departure times form Utrecht Centraal. It contained animations mimicking the behaviour of the old sign, sound effects, even background sound from the station. A very popular app for display purposes, some of the management at NS had it on their desk, would show it to people, etcetera. It was planned to remove the app again after a while but there was no real reason to. I think it no longer works nowadays due to having been compiled for 32 bits at the time, but maybe we fixed it, I have a vague recollection of it.

I had to leave after six months due to financial / budget reasons, but in my absence the developer and the NS team went on to create a version 3 redesign, as well as a number of smaller sattelite apps.

In 2016 I returned after my colleague left, and together with another colleague we worked on v4 of the app. This included an overhaul of the main travel planning flow, including the landing page, location search, trip selection, trip detail and train detail pages. I mainly worked on the search page, including results from a new points of interest search engine (using Google Maps API), address search (using a database of all Dutch addresses loaded in an Elastic Search search engine / instance), and iOS' reverse geolocation APIs. The travel planner was adjusted to include results from 9292OV's API if either the from / to destinations were addresses, so the app became multi-modal.

After version 4 was released, we were asked to build the NS International app as well. We were able to reuse a lot of the components for e.g. destination searching and the UI and incorporate it into the new NS International app.

Both the NS Reisplanner and NS International app had a lot of code written and rewritten in / to Swift, Apple's new programming language that is replacing objective-C.
