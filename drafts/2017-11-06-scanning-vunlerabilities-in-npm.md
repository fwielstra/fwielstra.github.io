* auditjs
  * free and open source
  * uses multiple lists
  * install & go, exits with error if something was found

* snyk
  * paid for non open source or small projects (100 tests / month)
  * $99 / month
  * requires authentication to run, might be tricky to include safely in CI
  * idk yet
  * Works locally with a wizard, allowing you to select a resolution for each issue (if found).
    * One issue was fixable by reinstaling a package (`react-scripts-ts@2.8.0`, which had 6 dependencies with vulnerabilities.
    * Another issue was not fixable yet, and could be ignored
    * Ignored issues are stored in a .snyk file in the repo itself, will reappear after 30 days.
  * Sends emails when something has been found
  * Offers a log on their website, allowing for detailed monitoring of vulnerabilities in the app and whether they have been fixed yet.
  * Patches vulnerabilities manually if none is in an official release yet, it seems?

* nsp
  * [github](https://github.com/nodesecurity/nsp)
  * main library / tool for nodesecurity.io database, also used by auditjs and (probably) snyk.
