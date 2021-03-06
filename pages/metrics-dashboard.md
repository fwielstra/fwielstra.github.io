---
layout: page
title: Portfolio - Metrics Dashboard
show_in_nav: false
permalink: /portfolio/metrics-dashboard/
---

This was my first internship project at my HBO (Bachelor's degree), done at FBTO in Leeuwarden (if you ever visit there, the big black monolith right in the city center). I believe the team I worked with / for was doing the FBTO.nl website, which sells insurances and the like.

My mentor / guidance person there was [Jurjan Woltman](https://www.linkedin.com/in/jurjanwoltman), who helped me along at first, suggesting I use the [Spring Framework](http://projects.spring.io/spring-framework/) in combination with [AppFuse](http://appfuse.org), which at the time seemed like a ready-made package of Spring and some other frameworks. He left to work for [NS](http://www.ns.nl) after a few months, but five years later, while I was working at WPG, he contacted me with a job opportunity; turns out he went to work for [Xebia](http://xebia.com) and grew to Unit Manager of the software development branch there. He contacted me, I got interested, I was hired as an apprentice, and the rest is history. Jurjan left Xebia a month later, but we were again re-acquainted a few years later; he currently works for Wehkamp, where Xebia has a pretty large team working at the moment.

But I digress. Metrics Dashboard was basically [Sonar](http://www.sonarsource.com) before it was mainstream. The objective of the assignment was, in a nutshell, to take all of the various reports generated by Maven's tools (like Checkstyle, CPD, PMD, etc) and put them all in a single overview / summary.

In those six months, I built an application that I still believe is the best application I've ever made. It was just uninterrupted coding bliss, and I had all the freedom to create the best software ever. I got elevated to a higher level of software development, thanks to learning how to use interfaces, dependency injection, unit testing, etcetera.

The application worked by taking a project folder and reading it. It read and parsed the Maven pom.xml file, which was then used for... I don't actually recall. The more important thing it did was that it read all the source files, as well as the XML versions of the code checking tools, and linked the two together; if there was a problem in a file, the web application would display it in a code window. I found some screenshots:

![Metrics Dashboard report summary]({{ site.url }}/assets/metricsscreenshot.jpg)
*Report summary*

![Metrics Dashboard group by error]({{ site.url }}/assets/metricsscreenshot2.jpg)
*Grouped by error*

![Metrics Dashboard code error highlighting]({{ site.url }}/assets/highlight.jpg)
*Code and error highlighting; not sure how helpful this was. Users would probably prefer an IDE plugin anyway*


I had enough time to do some stuff that wasn't really necessary; one thing I did was build each XML parser twice, one using DOM, another using SAX, to see which one was the more efficient; I quickly ran into the limitations of DOM parsing, which would simply not work with files bigger than 5 MB. SAX was ten times (or thereabouts) faster, too. That was the eye-opener about interfaces, dependency injection, and I guess unit testing - it was easy to take one component and replace it with another that did the same thing.

In addition I did a bunch of front-end / Javascript using the [Prototype](http://prototypejs.org) library / framework; I believe this was around the time jQuery came to be, too. The code of the program viewed was listed in a collapsing menu (accordeon style), which had fancy open/close animations. That was another thing I took a bit far; I ended up making my final presentation in the same style as the application, with the accordion menu used as a kind of index. It had keyboard navigation, transition animations, the works, all handcrafted HTML.

Unfortunately, there were only two or three people at my presentation back at school. But that's fine, the person coming after me was a no-show so I could just keep talking about the app and showing bits of it to the small but highly interested crowd.

I don't know if the application was ever really used though. Jurjan did suggest I / we should make it open source; in retrospect, we probably should've, or I should've kept working on it. A few years later, Sonar came out and did basically the same thing - although admittedly, probably better.

I emailed myself the code a couple of times; if I can get Gmail to stop keeping it hostage, I'll see if I can put it online somewhere; I doubt they care now, it's been over seven years ago.
