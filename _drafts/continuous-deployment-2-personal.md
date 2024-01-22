## Personal experiences

At Xebia, CD has been one of the main disciplines that we have been advertising for years; from [trainings](https://training.xebia.com/continuous-delivery-devops) to [craftsmanship best practices](http://essentials.xebia.com/) to [promoting agile methodologies](https://xebia.com/agile-transformations). However, and this is probably partially my fault, "true" CD has never been achieved in any of the projects I've worked at. I can go over them in short:

At Dutch Railways, we were developing an iOS app in a small team (of two, plus a UX/UI designer directing us). We mostly employed trunk-based development at first, at a later stage moving towards feature branching as the features became larger and larger and could not be deployed in a granular fasion (this is a lie, we just never implemented feature toggles). Our main constraint there was the [week-long review cycle](https://developer.apple.com/app-store/review/) on the one hand, and the advice to try and limit the amount of updates to publish; back then, people had to manually update, which for many apps turned into a marketing moment because people would often read at least the first few lines of the changelog. However, having an update there every week would make them roll their eyes. Late last year though, review times [dropped from a week down to a day](http://appreviewtimes.com/ios/annual-trend-graph), averaging to about 2.5 days nowadays. Second, [Apple started automatically updating apps in the background](https://support.apple.com/en-us/HT202180), so people wouldn't notice updates as much. Facebook changed their changelog to a generic "We always work to improve the app", which, I think, points towards them doing heavy CD on their app - updating the changelog is always a manual process, and manual processes do not scale.

At ING, we worked on the front- and back-end systems for their customer-facing investment banking service. At first we simply could not deliver to production, because the third-party back-end systems were simply not ready yet. Later, CD was impeded because we depended on a different department within ING to deploy the software, via tickets and such - there was no deployment automation yet. Later again, deployment automation was enabled when ING started using [Nolio](https://www.ca.com/us/products/ca-release-automation.html), but going live multiple times a day was still not an option; I mentioned issues with Selenium earlier, which plagued us (before that, it was performance issues with FitNesse, which we tried to fix by contributing to their script engine and by parallelising the tests over runners on everyone's beefy developer machines). Of course, another factor was that going live multiple times a day was simply not necessary - we worked in two-week sprints, we had a relatively low volume of users, plenty of work on the backlog, a stable market, etc. However, we did try and have a lot of the factors for successful CD in place, because they are simply good software development practices, they improve productivity and quality of the software even when you don't go live multiple times a day. As explained at the very start of this article, Continuous Delivery is most of the practices that would *allow* going live multiple times a day, but Continuous Deployment is actually going live.

Finally, at TNT we took a lot of the lessons from ING and moved it into this decade. Instead of releasing to Java application servers, we had [dockerized](https://www.docker.com/) everything that could be released to production, from our microservices back-end systems to the Angular front-end running in an nginx docker image. Every pull request opened on our Github repository made an automatic deployment to a test environment, and releases were a matter of making a tag and pushing a button. However, it was this last one that was the main bottleneck; releasing to production was very much a manual process. It involved:

 * Creating a tag
 * Pushing the tag to the remote repository
 * Building the tag in Jenkins, which deployed it to the TST environment
 * Updating the changelog in Jira
 * Waiting for a manual tester to do a sanity check (often took half a day)
 * Releasing to production (manually filling in the tag name again in Jenkins)
 * Often the testers would do another manual test to make sure nothing was broken

Two factors impeded continuous deployment here; having to manually do the deployment rituals, and having manual testers and sometimes the product owner that needed to sign off on going to production. Still, even with these constraints in place, going live could be done multiple times a day, depending on the willingness of developers. Why the process was never automated is probably something I'm to blame for myself, given how all developers were empowered and encouraged to contribute to the build scripts and systems.

## Ideals

 * Master -> live
 * Unit tests, maybe component tests in pre-push hooks
  * prefer good monitoring, reporting, and the ability to release to small groups of users for both front- and back-end.
 * I like feature branches for multi-person / multi-team projects.
 * I like feature branches and the GH pull request flow for code reviews
   * caveat: focus on style vs overall picture.
