---
layout:     post
title:      Moving servers
date:       2015-10-18 15:00
summary:    Moving a website from one dedicated server to another, with some upgrades and changes
tags:
 - server management
 - spambot management
 - ban all the things
---

*warning: long, unstructured ramble post*

I own a website running [Wordpress][Wordpress] and [vBulletin 3][vBulletin], both PHP/MySQL software packages, and have done so since 2007. The site has been hosted on various servers throughout the years; we started off at the Dutch shared hosting provider [MijnDomein][MijnDomein], running Wordpress and later adding [Simple Machines Forums][SMF]. The free / open source SMF was quickly replaced with the commercially licensed vBulletin; in part due to SMF having bad performance in comparison, and in part because most users in this slice of the internet are most familiar with it in terms of usage and management.

It didn't take too long before the MijnDomein server no longer suited us; the problem with shared hosting is that while they usually advertise with things like high bandwidth caps, they often limit CPU usage (usually using CPU time per minute); cross that, and your software starts to produce errors, usually in the form of an inability to connect to the MySQL database.

We moved from MijnDomein to [Hostgator][Hostgator], following a recommendation of one of our users; it was slightly more expensive (MijnDomein was about €30 a year, Hostgator twice as much or therabouts iirc), but its performance and CPU limits were higher than on MijnDomein. I think we managed to run the site from there for about two or three years. Eventually though, we ran into the same issues again - CPU usage limits. We solved that in part by removing some features from the site (like a very inefficient shoutbox), but we knew it was only a patch.

Simultaneously, I wanted to have more control. Using shared hosting, you're kinda limted to what the host gives you. In our case, with a pretty large database (think thousands of accounts, hundreds of thousands of posts), it became unmanageable - creating or restoring a back-up was just too much to ask from the built-in software, and we'd need support employees to help us out with that.

So, eventually, we decided to upgrade from shared hosting to dedicated hosting - doing our own server management. We went to [Leaseweb][Leaseweb] and rented a virtual server. I don't really recall how expensive that was back then, but it was more expensive than Hostgator (of course). That's where the fun started! Because it's not shared/managed hosting, you get a barebones server (in our case with Ubuntu Server installed), and can set it up as you please from there on out. After some fiddling, we had our LAMP stack set up.

But again, after some time, the server was giving performance issues; I don't actually recall what they were like though. In retrospect, a major issue was probably being caused by overly zealous search engines that do or at least did not respect indexing limits set in robots.txt (think Yandex and Baidu); another was spambots, which, while our anti-spam measures prevented most of them from even registering, still caused a bit of load on our server.

So we moved from virtualized hosting to dedicated (bare metal) hosting; dual-core Core 2 processor, 2 GB of memory, ~300GB hard drive, and of course Leaseweb's excellent network connection. Profit! We've been using that one for several years now; during that period, we curbed the spambot / pseudo-DDOS issue by aggressively blocking abusive IP addresses using IP tables rules (so block them at the firewall level); earlier, we had blocked some using Apache access controls, which worked too I guess but they still caused loads of lines to appear in the access logs.

Initially, we hand-picked the IPs we were blocking. Using some Bash magic, we could find the IP addresses that were doing the most calls to certain pages - one trend that became apparent very quickly was the amount of requests to the forums' register.php file, probably spambots (of which only a few got past our captcha). Here's the command used:

{% highlight text %}
grep 'register.php' /var/log/apache2/access.* | cut -d' ' -f1 | sort | uniq -c | sort | awk '$1 > 10 { print $1 " " $2 }'
{% endhighlight %}

This snippet finds all requests to 'register.php' in all access logs (including older / rotated ones), groups / counts requests coming from the same IP, and prints out a list of IP addresses and a count of calls to register.php, as long as they were more than 10 (i.e. an abnormal amount). Using this snippet, we could quickly identify some IP addresses responsible for thousands (!) of registration attempts, and IP block them with a firewall rule:

{% highlight text %}
iptables -A INPUT -s $IP_ADDRESS_HERE -j DROP
{% endhighlight %}

Another trend quickly became apparent after banning a few dozen IP addresses this way; most requests came from countries like China, Vietnam, etc. After a few days of just banning one IP after the other, we decided we'd had enough; we hardly ever get valid visitors from China or Vietnam or Russia (if they even managed to get through the [Great Firewall][Great Firewall]), so why not just outright ban all of China? After some googling, iptables-geopi (which does not have a sexy website apparently) came up; installed that, and configured it using an IP address database (from somewhere, don't recall). That sorted out a lot of issues.

Earlier this year, we had another incident; people were reporting the site to be sluggish. After checking out the access logs, there were a few IP addresses from the US that seemed to be aggressively indexing people's profile pages; the user agent was some Java-based scraper software, so I assumed it was some dude just fucking about or something. I blocked the relevant IP addresses using the above method again, and did an IP trace; all of the IPs went to some hosting provider, so I sent a mail to their abuse department too (to which they responded weeks later, not very effective but hey. If it was in the same country as our servers, there might've been criminal charges / a police investigation, but it gets very hazy very fast internationally.)

But I digress (like loads, lolol). A few weeks ago, I received an e-mail from our hosting provider. Basically, they said I was eligible for a server upgrade, for no extra costs. This was probably due to the fact our hardware was starting to get kinda old (it's probably approaching the five year mark soon enough, and I don't know if the server was used by another customer earlier). That's starting to get risky, especially in a datacenter which nowadays aren't kept at room temperature anymore. So, free upgrade; here's the old vs the new specifications, with [cpubenchmark.net][cpubenchmark]'s points for a performance comparison:

Current:
Intel T5500, dual-core, 1.66 GHz, 920 points
2 GB memory
1x160 GB hard drive

New:
Intel G850, dual-core, 2.90 GHz, 2.682 points (almost 3 times as fast)
4 GB memory
2x250 GB hard drive

Now comes the tricky part: Moving stuff over. Not only that, but I wanted to take the opportunity to upgrade to the latest server software if possible, and move from Apache to nginx (we have had issues with apache due to it running out of workers, probably again due to spambots and whatnot). I've also contemplated moving from MySQL to [MariaDB][MariaDB], a binary-compatible fork of MySQL that [promises better performance][MariaDB performance], independence from Oracle (which took over MySQL a couple of years ago), all the while being compatible with MySQL (so you can use the same tooling, PHP drivers, etc). I wasn't entirely convinced though, and I'm afraid there might be small compatibility problems arising. We haven't had database performance issues anyway, and even if it was a bottleneck right now, the new server is way faster and has more memory available.

Setting up the LEMP stack (Linux, nginx (engine-next, geddit), MySQL and PHP) was... surprisingly simple actually. You can install all of them using apt-get, and connecting nginx to the [PHP-FPM][PHP-FPM] process was a matter of uncommenting some lines:

{% highlight text %}
location ~ \.php$ {
  fastcgi_split_path_info ^(.+\.php)(/.+)$;
# With php5-cgi alone:
# fastcgi_pass 127.0.0.1:9000;
# With php5-fpm:
  fastcgi_pass unix:/var/run/php5-fpm.sock;
  fastcgi_index index.php;
  include fastcgi_params;
}
{% endhighlight %}

It took me forever to find something similar for Apache, and it's still kinda esoteric to me. I had to redo it too a while ago after I updated the old physical server's Ubuntu version to the latest LTS version (14.04), because that also updated Apache to 2.6, and Apache has a new configuration file syntax in that version (pro tip: never change your configuration file syntax, it's annoying as fuck). Googling around for "how to configure PHP and Apache" now gives you all styles, and there's a severe lack of One True Way there - but then, that's endemic in the LAMP stack ecosystem. I haven't programmed in PHP in forever, but back then everyone that ever wrote two lines of PHP started to think too highly of themselves and blog about it, leading to a lot of misinformation - which I believe was the main cause behind the wave of SQL attacks and the resulting drop in PHP's popularity and trust of sites running them (which still isn't great btw).

Anyway. That's how far along I was when I started writing this blog post. Next up is moving data from one server to another. The plan is to do a practice run first, see if everything works, then set a date for actually moving.

There's a few approaches I can do to moving data. The first one that came to mind is to use our existing backup strategy. What we do for backups right now is a homebrewed solution: there's a cron job running every week that makes a copy of /etc (i.e. all the configuration of the various packages), a copy of /var/www (the website data, including several GB worth of images used in news articles and pages, collected over the years), and a database dump of the MySQL database using mysqldump. All of those are packaged together in a .tar.gz file, which is then copied over to a [Dropbox][Dropbox] folder, which is linked to my personal (pro) account. Each backup takes up 10 GB of space, and it grows with about 100 MB a week. The main problem with Dropbox, I find, is its CPU usage. Here's a CPU usage chart from [Muninn][Muninn]:

![monthly CPU usage]({{ site.url }}/assets/moving-servers/cpu-month.png)

As you can see, CPU usage peaks every week on wednesday morning; somehow, synchronizing that 10 GB file causes Dropbox to use a heap of CPU. It's probably not a simple upload though, they probably use a technology involving loads of checksums and the like to ensure the upload goes smoothly. I just don't think it's very cool. I'd like to look into a different backup strategy; maybe use [Google Cloud Storage][Google Cloud Storage] or [Amazon Glacier][Amazon Glacier] to host the backups. They don't need to be synchronized, just stored somewhere safe. I've been using Glacier for my personal backups for a while now; the main problems Glacier has is that you need a specialized client for it (I use [FastGlacier][FastGlacier] on my Windows desktop at home), and that retrieving a backup can take up to six hours before the download even starts - that's too long, IMO. I gathered that Google Cloud Storage, or something similar to it, can compete with Glacier on costs, without the retrieval delay. Need to check that.

Anyway, the other and probably more feasible way to move data is to use SCP to transfer a backup file from the old server to the new. Given that both servers are situated at Leaseweb, and probably even in the same datacenter, this shouldn't take long. The command to use:

{% highlight text %}
scp -v -P <port> backup-2015-10-14-08:00:00.tgz root@<new server IP>:/root/backup-2015-10-14-08:00:00.tgz
{% endhighlight %}

(note that I have my SSH run on a different port than the default 22, this simple change stops the biggest part of login attempts. I should disable or change the default root account too for another level of security).

It seems to run at between 10 and 12.5 MB / second, which corresponds to a 100 mbit network; a bit disappointing, but, I can live with it. ETA 15 minutes.

![SCP progress]({{ site.url }}/assets/moving-servers/scp-progress.png)

(to be continued)

[Wordpress]: https://wordpress.org/
[vBulletin]: http://www.vbulletin.com/
[MijnDomein]: http://mijndomein.nl
[SMF]:http://www.simplemachines.org/
[Hostgator]: http://www.hostgator.com/
[Leaseweb]:https://www.leaseweb.com/
[Great Firewall]: https://en.wikipedia.org/wiki/Great_Firewall
[cpubenchmark]:https://www.cpubenchmark.net/
[MariaDB]: https://mariadb.org/
[MariaDB performance]: https://blog.mariadb.org/performance-evaluation-of-mariadb-10-1-and-mysql-5-7-4-labs-tplc/
[PHP-FPM]: http://php-fpm.org/
[Dropbox]: https://www.dropbox.com/
[Muninn]: http://munin-monitoring.org/
[Google Cloud Storage]: https://cloud.google.com/storage/
[Amazon Glacier]: https://aws.amazon.com/glacier/
[FastGlacier]: https://fastglacier.com/
