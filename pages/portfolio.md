---
layout: page
title: Portfolio
permalink: /portfolio/
---

A list of projects I've worked on over the past years; I will try and describe these in full if allowed by the employer and given the time to write it down.

## 2004 - Friese Poort

[Schedule web application]({{site.url}}/portfolio/schedule-webapp/)

## 2005-2009 - NHL Hogeschool (Bachelor level education)

2007: [Boatiko]({{site.url}}/portfolio/boatiko/), a remote-controlled boat, controlled via bluetooth. Won a race.<br />
2008?: [Metrics Dashboard]({{site.url}}/portfolio/metrics-dashboard/), basically Sonar before it was mainstream <br />
2008: [Clan Arena]({{site.url}}/portfolio/clan-arena/), my / our Game Design minor project, an FPS prototype made in the C4 engine <br />
2009: [Oberon Interactive]({{site.url}}/portfolio/oberon/) internship, building "Elftal van de Maand" in GX WebManager <br />

## 2009-2011 - [WPG Uitgevers] web developer

Various projects and website / webshop setup for book and magazine publishers; part-time web developer for Voetbal International<br />

## 2011-2017 - [Xebia](https://xebia.com) apprentice, consultant, web developer, iOS developer, full-stack, etc.

- 2011: [UPC SIF GUI], a relatively simple / small project, building a web UI for call center employees; uses Java back-end and one of the first Backbone.js front-ends<br />
- 2011, 2015: [NS Reisplanner]({{site.url}}/portfolio/ns-reisplanner/), the main app for Dutch Railways, one of the most popular App Store apps in the Netherlands<br />
- 2012 - 2014, 2017: [ING Beleggen], a single-page application with dozens of pages, tens of thousands of LOC, charts, tables, the works. Written in Backbone, then Angular. This project heavily inspired the current web development practices at ING<br />
- 2016: guild lead at [TNT], an Angular 1.x application with a Scala microservices back-end.<br />

## 2017 - [Xebia Studio](https://www.xebia.studio/), sub-department of Xebia, less consultancy, more software development

Studio was intended as an agency where a focused team of Xebia employees would do software development, instead of being
mixed in with people at a customer as was usually the case.

- 2017: ING Beleggen, again. Rebuilding for the 4th time in Polymer.
- 2017: Blueriq, consultancy job; they were looking for web technology to replace their C# UI, we advised them and did a
  number of PoC's in React, Angular, Vue and Ember; they picked Angular in the end, being more an OO shop. We didn't
  continue at that assignment because they weren't ready yet to start full on development; I'm not sure if they ever
  managed to get started on it. Nice team though.
- 2018: Flora Holland
- 2018: Vandebron, a Dutch green energy company. I spent a few months there helping them build a component in their
  customer dashboard, a power usage graph built using [Victory
  Charts](https://formidable.com/open-source/victory/docs/victory-chart/) as well as some other components. Didn't
  really stay there for long (three months irrc) because I was getting more and more annoyed at being jerked around and
  being put at a customer for an unspecified amount of time. The original assignment was a month and a half, but it was
  extended by another one.
- 2018: Spent a month between assignments; got AWS certified.
- 2018-2019: Fontem Ventures, the digital / new products branch of Imperial Brands / Tobacco. They developed some
  e-cigarrete products, including Blu (vaping) and later on Pulze (heated tobacco). My colleagues had been building the
  Blu site for a while; I helped them out for a week or two before moving on to Pulze, the work for us was building
  their brand site and webshop. Interesting architecture; we used Gatsby to build the site, Contentful as CMS,
  Commercetools as webshop backend, Adyen as payment provider, and we hooked it all together using Netlify functions /
  lambda functions written in JS. Later on, the company itself shifted to an over-engineered Azure stack that pretty
  much did the same, but a lot more complicated. I should write a longer rant about that.

In 2020, Xebia Studio was shuttered and merged back into Xebia Software Development; for about three years they tried to
gain traction with the brand, but (personal opinion) when it came down to it we couldn't become more than just a dev
agency; we didn't have a unique selling point, but we did charge a premium rate. I wonder if we should've just dropped
the facade and hire cheap, no-lease-car developers instead of trying to make it work with the experienced people.

Anyway I feel like I've stayed with Xebia for too long; I was a bit pissed off after TNT fell through, not because it
was a bad employer or they didn't want to pay or whatever, but because Xebia / XSD tried something to get their devs
more involved instead of being just hands-for-hire. I frequently think I should rejoin TNT again, I feel like there may
be big career opportunities there.

But in the meantime, in 2018/2019 I lost motivation; I went to a jobs coach for a while (6+ months in the end?) where I
basically told my life story + career story, which was nice I guess but there were no major revelations to me. Very long
story short, the advice was to take matters into my own hands instead of waiting for something to happen and depending
on others to give me a good job, so that year I started to orient myself, do job applications, do technical interviews
(initially just because I wanted to prove myself, I wanted to feel like I was still worthy and not just winging it /
coasting along).

There were some interesting candidates; I got a pretty good offer from a company called Divotion (part of JDriven), but I
eventually declined because one, it would be consultancy again, and two, impostor syndrome struck; I'm going to sound
like I'm bragging, but, they found my assessment _too_ good, there was no criticism on their part; I felt like they saw
me as much more than I am. The problem with that is that I'd not be expected to sit quietly and write some code, but be
a extrovert-appearing enthusiastic thought leader / manager / consultant, which is well out of my comfort zone.

Eventually I somehow ended up (through a recruiter who I'm sure I pissed off by not accepting any of the offers and just
going to applications to do the tech assessments) at a small company in Amersfoort called BroadForward.

# 2020 - [BroadForward](https://www.broadforward.com/)

BroadForward is a smallish (~20 people) product company whose main product is a piece of critical (mobile) network
infrastructure. As it turns out, over the past decades, big companies like Oracle, Ericsson, Nokia, Huawei etc have been
installing soft & hardware applications / appliances to fulfill certain roles in mobile networking; I may one day get a
grasp of the domain and write about that, but today is not that day. Anyway, they are chipping away at those
multi-million products with their product, BFX, which is an application configurable to fulfill many roles that other
companies require different apps / appliances for. It acts as an interconnect between mobile phone network generations,
can enrich messages, etc.

The history of BroadForward starts 20-30 years ago at (IIRC) CMG, which built a SMS gateway product that ended up
generating half a billion per year in revenue. I'm not sure when or how they decided to move on, but in 2012
BroadForward was founded by some of the veterans of that company.

It's different from what I'm used to because a lot of the people there are older, average age is definitely in the 40's
and some people definitely look like they're working towards retirement.

They have two main development projects; the BFX (which they often refer to as the back-end), and the GUI. The GUI's job
is to generate configuration files that are read and used by the BFX / back-end. These config files are a combination of
module configurations in formats that look like INI files (like [FreeDiameter
config](http://www.freediameter.net/trac/browser/freeDiameter/doc/freediameter.conf.sample)), template files (XML), and
'flow' configurations (also XML). These configurations often run into the hundreds of key / values, and the UI has to
manage it.

The existing UI was built by one of the founders and (IIRC) former CTO in PHP and Dojo, but it's not very good; it
works, and supposedly it's still better than what the competitors have, but it's basically mid-2000's technology. The
author is also not a UI developer and (I'm trying to be constructive here) seems to not have developed his skills once
he got into it.

The code is basically 160.000+ lines of string concatenation; back-end concatenates XML together, then converts it to
JSON to send to the front-end. Front-end is a ton of code that concatenates HTML together to output stuff Dojo can
(apparently) work with.

Anyway they decided to rebuild the whole thing last year and looked to hire someone, which turned out to be me.

I'm being very slow in building it, because I'm trying to do the right thing. The software has to last for ten years at
least (as the existing one does), probably more, and there is a lot of complexity that has to be managed. The previous
author may not have been very good at software development practices, but I can't deny that he was productive.

I spent some time deciding (and defending in writing) technologies and libraries to use, and for now settled on Go for the back-end, TS + React for the front-end. I should write a lot more about that, but not right now.
