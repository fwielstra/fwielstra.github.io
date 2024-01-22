DO NOT PUBLISH

 * on Git, commits, commit messages, branching strategies, pull request flows, code reviews, traceability and audits, etc
  * link to e.g. commits where that apple fallthrough came up
  * CI server blocking merging
  * Why directly committing to master is a bad thing
  * and locking down master is a good thing
  * fuck develop etc, just go for master - simplicity is good
  * Anecdotal aside; forking as a means of access control
    * TODO: Make sure access control is the reason, if so, it's not for security that's for sure.
  * Commitizen
    * make sure to have a list of components to choose from
    * Using story numbers or issues
    * Why story numbers alone aren't enough - make sure to outline the feature in a commit message
        * System in which stories are described may become inaccessible or obsolete
        * e.g. if you use GH issue numbers, what if GH goes bust and doesn't have a good means of recovering data?
        * Git is a distributed, asynchronous system, issue trackers are not - different philosophies. Same goes for other means of communication. Git and version control are permanent and sacred, other systems are transient (words?)

 * On choosing a framework for front-end work
    * TL;DR it doesn't really matter; outline what I think is a good architecture, explain why all the major frameworks do roughly the same.
    * More important is that you set out a structure and all your team members are following it (see also git thing)
    * Technology is fleeting, but don't feel obliged to follow it. Backbone, Angular 1.x, etc are still functional frameworks, and anything made in them will not suddenly break.
    * On separating presentation from state
     * Not sure tbf whether any project would actually rewrite only the presentation part. If you avoid framework of the week/year syndrome, it shouldn't matter much.
     * Developers wanting to rewrite in technology of the month are very expensive, and RoI is very hard to explain.
    * On Angular vs React vs $framework
     * IMO, all major frameworks are objectively good frameworks
     * All of them are viable to create high-quality software
     * Major factor is developer preference, hiring, etc;
      * Angular, Ember are probably the easiest to get into, most enterprisey, probably safer for less-technical front-enders etc
      * React + ecosystem seem more suitable for developers leaning towards more functional programming; more focus on pure functions, extending it to components and state management. Inclined to believe it's more suitable for larger projects.
    * Polymer can die in a fire, should not be used as a primary tool for making webapps. Components, fine, especially if you have a set of standardized components like e.g. the paper- series.
    * IDK where Vue falls, looks like web components, described as the good parts of Angular's view rendering
    * On critical mass
        * Notable: Ember, doesn't have critical mass, but has been moderately (<10%) popular for a very long time
        * Don't bother with something with low adoption (Durandal, Polymer 1); they will be viable and probably high quality, but I don't expect them to have development or maintenance for longer periods of time. Only go for them if you're willing to completely take over ownership of the project.
        * Actually, this is something I'm missing from all major businesses we've built webapps for - contributing back to the community. IMO we, or our employers, should donate time and / or money to the frameworks they use. Biggest ones should have at least one FTE working full-time on the frameworks and libraries used. Contributing back to open source is something we don't do nearly enough.

 * On choosing a language / Typescript
  * Something JS developers (myself included) have forgotten are some of the core rules of software development; [Rob Pike's 5th rule of development](http://users.ece.utexas.edu/~adnan/pike.html) says "Data dominates. If you've chosen the right data structures and organized things well, the algorithms will almost always be self-evident. Data structures, not algorithms, are central to programming.". Git flowed from its data structure, not its algorithms. Design data well and performance will follow. That kinda stuff. Not really relevant to webapps in terms of development, but, managing your datastructures is one of the most important things to do. Forms and API calls flow from the data. If you have a clear definition of your data (and its constraints), making a form to match becomes fairly trivial. TODO: linus / git quotes? idk.

 * on continuous deployment
   * Never seen it in action yet;
    * Still some manual steps (tagging, releasing button, changelog)
    * Manual testing - bottleneck
   * Guarantees needed:
    * One option is continuous, comprehensive tests;
    * git feature branch model: branches get rebased on top of master (or merged, like TNT), then run through test / CI
     * This model does not scale, can only realistically have one feature 'ready to release' at any given time. When there's five features 'ready', they have to run through the CI thing one at a time.
     * Only way to make that work is to go with smaller applications; microservices front- and back.
     * However this also does not scale, becuase what I'm also missing is proper comprehensive end-to-end tests
     * Do not do microservices or whatever if you do not have real end-to-end tests.
   * Thing that will scale: Releasing to small groups, like e.g. facebook. Start with 1%, monitor errors. Go to 5%, 10%, 25%, 50%, finally 100%, etc. Maybe less increments depending.
   * Never revert, always go forward. Reverting means the whole development cycle has to be paused. This does not scale.


 * (not in the series): rant on how developer "fun" influences technology choice. Software should be boring, but developers will make it exciting for their own selfish reasons. Find the guy I talked to earlier that agreed.
  * Not fun but to the point: Go, Java, etc
  * Fun but complicated, self-fellating developer friendly: Scala, etc.
  * TODO: Get people to explain in objective terms why Scala would be a good choice.
  * On picking technology for hiring purposes
   * Also happens with e.g. development practices - ING's scrum/devops/spotify lies, Wehkamp and TNT's choice for Scala just for hiring purposes.
   * Criticism of Xebia tbf, we're not helping the customer that way, we're helping ourselves and stroking our own egoes.
