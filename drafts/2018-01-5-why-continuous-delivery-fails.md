---
layout:     post
title:      Why continuous delivery fails
date:       2018-01-05 13:37:00
summary:    A personal account on why CD is actually rarely seen in the wild
---

* Intro
  * CD is going to live x times a day
  * Won't go into the why this is good, others are better at that
  * Done a number of projects but none of them did it, despite having most of the necessary steps in place. Why?

* Trust
  * Main driver is probably fear of revenue loss from business, fear of sleep loss from developers
    * latter is why no manual releases are done after (e.g.) 3 pm or on fridays
  * To always go to production one needs to be able to trust the code
  * No adequate testing means there's no trust
  * While there were often unit tests and frequently integration tests, they were often limited to individual services
  * No true end-to-end tests were made in a lot of cases
    * No isolated environment
      * Ideally you get your environment up using e.g. docker-compose, both for development and proper end to end integration testing
      * idk why this was never done, probably laziness.
    * Nobody could be bothered
      * Not built initially
      * Too much features already in place with too many nuances
        * nowadays it's very easy to build a lot of features
        * if you don't have your e2e testing set up and have it in the definition of done and everyone works on them, catching up will become a huge challenge
        * Even if you have the tests, running them will quickly take a lot of time, discouraging people from running them
    * Instability / Lack of reliability
      * Nobody wants to have to deal with a Selenium-based test that just randomly decides to not work anymore
        * timing issues
      * Cypress seems more reliable
    * Cross-browser testing wasn't done anywhere
  * In one case: "Old school" testers that refused to greenlight anything they hadn't manually tested themselves
    * Often went through a fixed test plan, easy to automate
    * Fire these people please, or at least let them do their work without impeding the normal release flow
  * Advice / Takeaways:
    * Set up your testing strategy from sprint 0
    * Use container technology or whatever and get an isolated environment up from sprint 0
    * Write proper end-to-end test scenarios
    * Adopt automatic master = live from sprint 0. Allow for breakage. You're not processing millions just yet.
    * If things do break in production, fix your tests; do NOT stop with automatic master = live.
    * Allow for failure. Most errors are bugs only affecting small subset of users / functionality. Set reasonable expectations.
    * Alternative: Staggered release. Expose new version to subset of users, pause rollout if error count or other metrics are affected

* Separate ops group
  * (was at ING, no need to mention it)
  * Team was not responsible for own servers or releases
  * .jar was delivered at the end of sprint and had to go through hoops to be released by a dedicated ops team
  * This approach can work for "finished" applications but it doesn't work for modern things, you want to go live multiple times a day

* Manual & human steps
  * One project: git tag, push, type tag in CI and submit, wait, manually update changelog, have PO and tester look at it, wait some more, type tag in CI again and press button, tester / PO doing another manual smoke test. Repeat for each release. Does not scale.

* Review process
  * Probably similar to manual & human steps, but this is completely external
  * Apple's app review process took a week; this is a clear blocker for CD
  * I believe Apple's intent was to force developers to put a bit more effort into their apps before submitting.
    * Initial submit: Better make sure it's finished and polished. oh let's review the guidelines again.
    * Following submits: Better make sure it's all good else we'll have lost a week
  * Still something of a thing but not as bad anymore
    * Rise of webapps / React Native, allowing for updates without going through app review process
    * Time reduced to ~2 days
  * I wish Google / Android did this tbf, they've got too much crapware on their app store.
  * If there is an ops group in your organization, this could also be a good thing - see the SRE book

* Culture
  * CD is a cultural change, and in most organizations there's no real pressure to do it.
  * Needs a strong leader to push for it. Again why it should be from day 0 probably.
