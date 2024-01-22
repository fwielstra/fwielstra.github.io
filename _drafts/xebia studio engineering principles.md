A list of core principles and goals "we" (hopefully) want to adhere to as Studio


# Principle (drafts):

1. Mandate


  * UX in team - why?
    * Someone with mandate in team - why?
      * Reduce time between "I have a question" and "I know" - why?
        * Goal for Xebia: Speed
        * Minimize distractions / concentration breaks
        * Minimize indirection (layers of people with mandates)
        * The people with mandate (ux, lead dev, etc) need to be in the team
        *





# stuff

 * Mandate
  * if no mandate, indirectness, time, etc?


## more stuff


Goal: A short bulletpoint list of strongly worded, succinct Principles. For every major decision we validate them with the Principles.

* links / resources
  * https://infrequently.org/2018/09/the-developer-experience-bait-and-switch/
    * on how there's a focus on developer happiness instead of customer experience, how performance is a last minute consideration (if at all)

# General goals

* Minimize complexity by minimizing the amount of moving parts
  * It's very easy to add moving parts and very easy to not realize you're adding another moving part, thus adding complexity
    * e.g. adding a mock server to avoid having to contact an unreliable prd/test environment - congratulations you've got a (json?) codebase to keep up to date.

# Development

* Master = Live
  * We don't have time or arsedness to have to wonder whether we can release - the answer should always be yes. We can't be fucked to have to press a release button. We don't want to have to think about version numbers unless we're building a public library used by other people.
  * This also means that a 'broken' master is a high impact issue; IMO a broken build means every developer is affected and impacted. Broken for 30 minutes? Times 10 developers that's most of a day lost.
    * Prevent broken master by:
      * Mandatory pre-push hook that executes all tests (if trunk-based)
      * Locking down master and mandatory CI (if PR based)
  * Two strategies:
    1. Build pipeline that runs all tests (unit + e2e + etc) before going live. Probably a good idea anyway. As development team we need the confidence that if the tests pass, it's safe to deploy.
    2. Gradual rollout. Deploy to subset of users, measure error rates. This probably works better at higher load applications, where a certain baseline load is guaranteed. Depends on good end-to-end statistical error monitoring.
      * If this is done perfectly, tests are less important. Great if some downtime or errors are acceptable.

* One-Step Setup
  * Well, sort of.
  * Getting started developing on the project should be in as few steps as possible.
    * Ideally:
      * git clone <project>
      * (opt) install dependencies if need be
      * `make start` (for example)
  * there should be NO dependency on ANY remote systems
    * Test env being down should have no bearing on productivity
    * Test env being up or down should not be a requirement for releasing
      * that's symptomatic of there being a manual process in place, e.g. a person having to test and approve a feature
  * Services running in development mode (the default) should have a sane set of (test) data available.
    * This test data should be usable for both development and end-to-end testing
    * unit and single service / front-end integration tests should have their own test data
    * Avoid mock servers for 'own' servers - that is, self developed front-end should talk to self developed back-end, not a mock. Mocks take time and effort to maintain (even the 'recording proxy' type) and should be considered another project / codebase, one that is in flux due to the back-end being in development as well.
    * 3rd party services can / should be mocked, if they don't run on a developer's machine.
  * Minimize typing; if starting up requires three steps (e.g. `docker-compose up; npm start`) or a long command (`npm start-this-service-and-stuff`), make aliases. npm has a scripts segment in package.json, else make is a straightforward and ubiqutous tool for creating simple scripts. Bash scripts also work but are kind of a pain.

* Testing
  * Tests are intended to give developers confidence that releasing changes will not break existing functionality
  * Number and type of tests will vary
  * There should be an end to end test suite that fires up the whole stack, preferably with all real services and e.g. database servers.
    * The test suite should not depend on any external systems
    * The test suite should run the same tests and have the same results locally and on a build server
  * Individual parts of a larger app (e.g. front- and back-end), if they have a test suite, should work independenty
    * that is, you should not need the back-end to run the front-end tests
    * you shouldn't need a real database to test the back-end
    * etc
  * Manual tests should not be a bottleneck for development
    * prefer just releasing behind a feature flag for example
    * Also, manual tests do not scale!

* Microservices is a stupid idea
  * For most projects anyway
  * I've yet to hear good reasons at projects that use microservices why they use them
    * Often it's more about personal feeling, hip factor, or developer happiness
      * Developer happiness is, I believe, a number of factors wrt microservices:
        * The feeling of starting fresh is always good
        * A developer can only hold so much code in their head, so small codebases make sense
          * In practice / my experience, each developer works in multiple services which negates this argument. It does so in plural because next to the individual codebases, the wider architecture and cross-service functionality has to be kept in mind.
  * Microservices adds a large amount of overhead to any project:
    * Inter-service communication
      * (most lazy first attempts had services talk to one another via REST)
      * (people forget the latency tiers apparently)
      * (and the overhead of rest/json is ignored / amortized / not cared about)
        * (tbh if http overhead isn't a problem you should reconsider using microservices)
        * (and if you're not measuring overhead you should also reconsider using microservices)
    * Deployment complexity
    * Inter service dependencies
      * If you can't release service A without also releasing B, you have a distributed monolith
      * If service A is broken because service B is not accessible, you have a distributed monolith
    * Monitoring & profiling
      * You should have full end to end performance statistics
      * Having a request depend on one or more microservices adds a lot of latency
    * Tracing
      * You need to be able to follow e.g. a request through the system
  * Analogy: 1 service = 1 product.
    * Do you have a dedicated product owner (or technical lead) and 1 or more teams work on it? Good
    * Do you have 1 team work on multiple services? Not good;
      * ideally, if 1 product = 100% focus, 2 products = 50% focus each
      * in practice it's less; context switches, switching editors, etc.
      * and if it's in a monorepo and the exact same language, you have a distributed monolith. What's the benefit?

* Don't make me think
  * Prefer simple languages over clever ones
    * java / kotlin > scala
    * go > java (it depends)
    * php?
  * Prefer simple code constructs
  * Write self-documenting code BUT make sure to add context about domain matters
  * Write and maintain a README, one for the whole, one for each component. Make sure it contains:
    * A short blurb about what the project and/or component does, where it fits in the architecture, etc
    * Setup instructions - e.g. runtimes (go, java, scala), build tools (sbt, npm, make), etc
    * Development instructions - how to install dependencies and start in dev mode (this should be trivial!)
    * Test instructions - should be just simple commands! (e.g. one for unit, one for e2e, etc)
    * Deployment instructions - if need be, this should be automatic (that is, branches go to a test/acc environment, master goes to production)
    * Maintainers - unless otherwise specified, you wrote it, you own it - be available to answer questions, even after you leave the project.
    * Tips & tricks - e.g. what editors and tools you've used locally to improve productivity.
  * Code formatting should not take mental effort
    * Prefer 'standardized' formatting rules
    * Use tools like prettier, gofmt, etc
    * Have these run automatically, e.g. on save or as part of a pre-commit hook
    * Automated formatting from the start will avoid a lot of code churn
  * Validation should be automatic
    * Use pre-commit and pre-push hooks to do fast checks (formatting, linting and unit tests should be fast enough; anything <1 minute is fast enough for a pre-push hook)
    * This is to avoid pushing broken shit and having to do a 'fix' commit or an amend
      * fixing / amending requires running a number of git commands and takes at least half a minute

* Keep documentation near the codebase
  * Reference documentation for 3rd party services, detailed module / component / service documentation, etc should be in the code
  * do NOT depend on an external system (such as Confluence) to store important information
  * Rationalize and track your architectural decisions using e.g. [architecture decision records](https://www.thoughtworks.com/radar/techniques/lightweight-architecture-decision-records)
    * Don't assume a technical decision is obvious
    * Spend some time reasoning about why you want to do something (e.g. introduce microservices) and write it down so that anyone - mostly yourself - can actually understand it
    * IMO, ADRs can help combat hype-driven development

* Something something performance
  * Measure before fix
  * Measure anyway to establish a baseline, and set alerts when this goes up

* Git stuff
  * Know your tool!
  * Know what's happening!
  * Know how to use the commandline before using tools - tools obfuscate what's happening
  * Use a commit template, e.g. conventional-changelog, and if need be a validator
    * Customize this tool so that e.g. scopes or story numbers or whatever are consistent etc.
  * Do not create 'fix' commits - use (interactive) rebase, --amend, etc
    * Don't be shy with force pushes - but only in branches, and never when there's more than two persons working on a branch that aren't pairing at that time.
  * Try squash-and-merge strategies, flattening larger branches / pull requests into single commits. This summarizes the commit history and when browsing history, does not confuse history with branches and merges and such.
  * Commit log should read as a changelog; messages should be readable in that you know what changes. duh. Easier said than done.
  * Remember: git logs may be required for compliancy and audits.
  * NEVER rewrite history on master - lock that shit down, do NOT allow force pushes on master.
    * personally: avoid pushing to master in general, especially if master = live.
    * if pushing to master directly, code review remarks would be added as 'fix' commits, and in an ideal world, each 'fix' commit would trigger another release with all the waiting and shit that entails.

* Trunk-based vs Pull Request-based
  * These two don't exclude one another of course.
  * Trunk based is fine for small teams, small projects, and where downtime and disruptions are acceptable
  * Time how long master is red if that is possible
  * Prevent master being red by using pre-push hooks as much as possible
  * Have strict rules about git commit formatting and make sure to review them at all times - this shit is important
  * Prefer short lived branches for review and test purposes before integrating with master

* Curb your enthusiasm
  * Everyone wants to work with the latest and greatest and c00lest tools and tech
  * But they may not be the best choice for the job.
  * Take a step back and always employ a somewhat formal procedure before jumping in
    * Write ADRs, this helps you sort out your thoughts and makes a decision one based on facts, not emotions
  * Consider who is going to maintain it
  * You're not nearly as smart as you think you are
    * Assume you're an idiot
    * Assume whoever's going to work alongside you or after you on the project is an idiot
      * Assume they have a chainsaw and know where you live
    * Don't assume your code is obvious
  * Don't be clever
    * You can boil a lot of code down to a minimum amount
    * But prefer simple and readable code over clever code

* Testing
  * Make sure to at least have an end-to-end test
    * This test should be runnable with minimal instructions (see also: single command)
    * Test should run on all machines without extra setup if possible (that is, run both locally and remotely)
  * Tests should have minimal differences between local dev and CI
  * CI:
    * If following a pull request, ff-only approach, tests should not have to run a second time after merged with master

* CI
  * Don't skimp on expenses, get enough workers and such available. But do tune your CI so it only runs necessary stuff.
  * Allow every developer to add tweak the CI processes; automation good.

## Other shit:

* Avoid churn; don't refactor for refactoring's sake, don't touch a component you're not working on for a feature.
  * If you are refactoring, do it as a separate task / branch / etc, and do it consistently - follow through!
  * Avoid mixing styles and approaches. Realize that if you are moving to a new style (random example: using classes instead of pure functions for react components), it's YOUR responsibility to make sure ALL code is adjusted to the new style. And make sure the rest of the team is in agreement because from that moment on, they have to work in the same style / use the same approach. (another example would be e.g. switching http libraries). Don't switch if you're not going all-in. If it works it works.

* Buy over build
  * don't reinvent the wheel, we don't have time for that

# People, Team & Environment

* Team composition
  * UX in team, as proxy product owner with executive power.
    * Available 100% if possible
    * Dedicated to single product
  * 1 team = 1 product
    * evolutionary; the longer a project lasts the more product to maintain or the more products, plural
    * how to deal with this?
    * at least make it explicit: "we as team X own and maintain product a, b and c"
    * you cannot focus on more than 1 products!
      * well you can but your focus will be less than half of what it would be for one product.
    * A product owner should not own more than 1 product!
  * WIP limits
    * 5 people working on 5 things means you effectively have 5 teams.
  * Product owner or main stakeholder
    * Needs to either be available at all (most) times during the workday, or there needs to be a role who can make executive decisions in the team (e.g. ux, scrum master). Waiting for decisions is shit.

* Meetings
  * Avoid meeting cultures
    * Actually, avoid meetings.
  * Ideally meetings have no time limit and will be done ASAP
  * If meetings get out of hand, setting a time limit may be an option but that's symptoombestrijding
  * Stand-up meetings were invented to "force" a time limit so to speak, but it doesn't work since sometimes they take an hour
    * limit stand-up to 15 minutes, if they have to take longer, make it a formal one.
  * Meetings should have an agenda which should be stuck to. Meetings are finished once the agenda is finished. Avoid inflation.
  * Meetings should have an assertive leader. Preferably not the main stakeholder.

* Count people involved and their roles
  * In Scrum, a team only has to deal with ONE person - the product owner.
    * A domain expert or stakeholder can help out of course
  * Count the number of people in a meeting, how many are "inside" (working on the project) and "outside" (wanting the project)

* Overtime is not necessary
  * A lack of planning on your part does not constitute an emergency on mine
* 24/7 support should not be necessary but may be needed
  * Make sure to have a proper training setup for people on call.
    * Remote access
    * Logging (access and how to read)
    * Restarting services (if necessary)
    * Escalation procedures
  * Test remote access and recovery procedures regularly!
    * If not all the time - chaos monkey style. Allow for degraded performance (= latency for end users).

* Celebrate success
  * too many projects just grind on for too long. Soft launches are underwhelming. Random "parties" are just weird.
  * Need certain milestones and a proper break after said milestone is reached - party and a day off, or a weekend, or something like that.
    * Need achievable milestones for that

* Code Reviews
  * Make it a formal process
    * That is, get into a proper mindset, make sure to have a list of things to look out for
  * Don't review what should be automated
    * See also: Don't make me think
    * Things like code style should be automated. If a code style that doesn't match the rest of the codebase is prominent in a code review, that will become the focus, not the content itself.
  * Suggested checklist:
    * Code style and linting - this should be automated, but it's always good to double check, update the standards if necessary.
    * Test coverage
      * There's an automated metric which should be used to check for major regressions, but most likely this would be a thing that slowly creeps in over time if not caught in code reviews
      * Run through all tests and all changed code; does it cover all the cases? Should it?
      * Depending on project, make sure to check all test types have been updated
  * Set a time limit, alerting
    * More than 24 hours (excluding weekends) is a problem
    * Prefer to have a PR reviewed and merged in the same day - if necessary, have a daily moment (e.g. end of day) for reviews

* Environment
  * ~A happy worker is a mindless worker~
  * Open offices are evil and should be avoided at all times unless you don't have any expectations to get anything done
  * Software development is a job requiring high sustained concentration; open offices are the antithesis to this.
  * Prefer team sized rooms (= max 10 people per room) over both open offices and individual offices
  * Reduce noise (that is, talk quietly unless you're addressing the whole team)
    * Take phone calls outside
    * Put phones on silent
  * Reduce visual distraction - make sure there's not too much milling about in or outside the team room.
  * Make sure all required meetings and sync moments are fixed
    * And reduce them to a minimum - see other section
  * Fixed places and reserved seats for all workers
    * Having to figure out where to sit is a terrible way to start
    * Having to spend time to set up your setup is shit
  * Clean desk policy but only up to a point (e.g. for cleaning), has to be possible to keep keyboards and such on the table
    * Make sure there's plenty of storage and shelves and such on- and off desk if necessary
    * Lockers are neat
  * Natural light is good, but make sure there's good sun screens as well.
    * Screens should be positioned perpendicular to windows to reduce glare
  * A window that can open is great
    * as long as there's no smokers outside
  * Make sure temperature is below 25 degrees at all times
    * Productivity takes a shit at higher temperatures

* Tooling
  * Remember that people work on their computers for ~8 hours / day; do not skimp on these tools.
    * would you give a carpenter a €5 hammer from the budgetbak?
    * would you put a taxi driver in a secondhand fiat panda?
      * actually Uber would nvm
    * would you have your surgeon just hold a flashlight in his mouth?
    * We are highly knowledgeable, expensive knowledge workers and if you are unwilling to pay 500 - 1000 for a decent screen then why the fuck are you paying that every day for the people?
  * Dedicated fixed computers (e.g. imac pros) are great, however risk of break in and theft probably excludes those.
  * Make sure everyone has at least one large (24+ inch) external screen
    * Prefer two screens, prefer large screens, prefer high resolution screens
    * For any kind of visual work, make sure color representation is good.
    * Make it so they can be set to the proper height
      * in my case I often need 1-2 stack of paper or whatever in addition to the height the screen can reach itself
  * People should work on their own keyboards, but avoid the noisy mechanical type because they are very distracting
    * even the ones with "quiet" switches
  * Good chairs - keep in mind not everyone is the same so having multiple models available is good.
    * Remember that once someone has their seat configured just right it's hard to get it back - do NOT share chairs.
      * Label chairs too just in case
  * Height adjustable desks
    * if they can go all the way up to standing desks it's nice
  * Special chairs are a nice bonus
    * Balls
    * Springs
    * Bikes? idk

