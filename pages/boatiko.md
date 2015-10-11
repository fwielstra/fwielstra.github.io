---
layout: page
title: Portfolio - Boatiko
show_in_nav: false
permalink: /portfolio/boatiko/
---

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
