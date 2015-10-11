---
layout: page
title: Portfolio
permalink: /portfolio/
---

A list of projects I've worked on over the past years; I will try and describe these in full if allowed by the employer and given the time to write it down.

## Schedule web application

I believe this was somewhere in 2004 or thereabouts, in the final year of my MBO (associate's degree?), and my first software development project. The basic idea was that we create a web application that can be used to schedule classes, or something like that; I don't actually remember the specifics.

What I do remember is that the main functionality was a large grid of checkboxes; probably weekdays and hours in a day. That information was stored in a MySQL database. We started out with a grey-ish theme, but we were later told that it would need high contrast for the visually impaired; yellow on blue was supposedly the best for that, so we ended up with a yellow and blue atrocity. I believe frames were involved too.

One of the things I remember best was how the checkbox grid was intially just hand-written. I asked a question about that on our forum, which a guy from Latvia I used to know (who worked as a freelance PHP developer and did pretty well for himself) answered; he came up with a triple-nested for-loop which I had trouble comprehending, but it did turn 200-300 lines of repetitive html into about 15 lines of awesome, so good on him.

Years later I found some old code of his, it was... pretty bad. However, he still deserves all the respect, because he was out there building stuff and making good money out of it - in the end, working software > quality code.

## Boatiko

Probably the most interesting project we did during our education was an interdisciplinary one. My education was in the "engineering" department of the school, and one thing they did was to get all of the different branches together to share a project. The project was to build a boat and race it with the other students - only a bit more complicated.

Part of it was engineering, building the shape of the boat and such. The other part was electrical engineering; wire up control circuits, engine controls, rudder, sensors, and a weapon to pop balloons (in our case, a nail that poked out the end). The third part and the one I was involved in was the software side.

The software part was twofold; on the one side there was to be made a client application that could take input from a controller and send it to the boat using a Bluetooth signal, as well as receive sensor data back from the boat and show that on the screen. I actually have a screenshot of that:

![Boatiko control center application]({{ site.url }}/assets/Spartaaa049.jpg)
*glorious Swing*

The other part was an embedded C program running on a chip on the boat itself. It was a tiny thing, with just a few hundred bytes of memory and IIRC a 1 MHz processor (which could be overclocked to 10 MHz iirc). That one was responsible for receiving and dealing with messages and commands coming in via bluetooth, generating a PWM signal for the engine and the 'weapon', steer the rudder, etcetera.

I believe we ended up with three of those chips; the main one was dedicated to most of the controls, the other two were just added in for additional PWM signals or something like that.

Programming it was a bit of a pain; the editor was very basic, and had a tendency to crash. I just used Notepad++ to edit the code and the other software to compile and flash the chip.

![my workspace;]({{ site.url }}/assets/Spartaaa048.jpg)
*My workspace; crappy old laptop on the left, C compiler and code on the right*

Anyway. Come race day, we were sorta ready - but only barely. The competition was stiff; one of the other teams had someone that did this as a hobby, their boat was ten times as fast as any other. Ours was kinda sluggish, kinda huge, kinda ugly, but somehow in the end we finished first. I do think this was more luck than skill though; we just chucked in a big engine that drained the battery within five minutes, and unlike the super fast boat, we did not lose the connection or control of it (the fast one made it to the end of the gracht before taking a sharp right into the wall).

The local news station even made a report of it; because our ship was the ugliest though, they didn't bother to put it in the report.

<iframe width="420" height="315" src="https://www.youtube.com/embed/hMS5j2vZbxc" frameborder="0" allowfullscreen></iframe>


![The boat]({{ site.url }}/assets/Spartaaa076.jpg)
*Isn't it pretty?*

![Boat float]({{ site.url }}/assets/Spartaaa140.jpg)
*It even floats!*

## Metrics Dashboard

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

## Clan Arena

In early 2008, in the 3rd year of my education after my internship (I believe), I did a minor in game design. I got into a team that wanted to make an FPS; I believe the main guy had it all thought out already, although then again we were halfway through the minor when we finally got some game design written down.

The main thing about this project was the usage of the [C4 Engine](http://www.terathon.com/index.php) (which apparently isn't for public use anymore?) and working in C++. It was a fully fledged game engine, with an editor and everything. We spent a lot of time just playing with it and experimenting. I myself spent an unhealthy amount of time taking the demo application and refactoring it; while I do believe the developer behind the engine knows what he's doing, the code was not really pretty IMO. I've probably posted a number of forum posts about it, proposing my improvements to the code. The engine's author didn't reply to those though. Still, that's fine, I enjoyed just refactoring and polishing the code. Performance was probably hurt by it though, but, I don't know.

In the end we did manage to make a basic game; it was mostly based on the demo game provided by the engine, but we had a semblance of our own map, working multiplayer (again thanks to the demo), and shooty things. I don't think the game was ever developed beyond that though. Googling for it now reveals a Quake mod; I doubt it's got anything to do with it.

![all hail the cookie monster]({{ site.url }}/assets/awesoemness.jpg)
*ALL HAIL THE COOKIE MONSTER*

## 2009: Oberon Interactive

[linky]({{site.url}}/portfolio/oberon)
