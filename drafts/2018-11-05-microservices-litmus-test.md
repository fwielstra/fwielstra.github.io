 * Is this microservice an independent product?
  * Does it have its own dedicated dev/ops team?
  * Does it have its own product owner?

* How many engineers do you have?
  * you cannot maintain more products than you have developers
  * you cannot expect all your developers to be versed in all services
  * Who will be the architect(s)?
    * Managing a microservices architecture / ecosystem requires a 'meta' role / team that makes sure
      the system is set up correctly, that communication is in order, that messages between services are standardized.
      Too often this is not addressed, causing the microservices architecture to be a patchwork that only works because computers are fast enough. There needs to be a vision / visionary.

* Are you enforcing one language, framework, code style, etc for services?
  * Then you're too small for microservices

* How many users do you have? How many requests?
  * That is, do you have a component in your application / architecture that is getting, or is expected to, need to scale 10x compared to the rest of the application?
    * 10x - 100x performance is another reason to look at using an alternative language or architecture

* Would you build a Service Oriented Architecture?
  * given they're the same thing, bascially. I mean come on.
