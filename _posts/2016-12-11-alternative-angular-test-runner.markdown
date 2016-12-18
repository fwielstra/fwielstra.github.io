---
layout:     post
title:      An Alternative Angular Test Runner
date:       2016-12-11 14:23:00
summary:    A post on how to test your Angular application without Karma and a browser
tags:
 - javascript
 - angular
 - testing
---

When building an Angular application, we usually stick to the suggested or auto-generated solution of unit testing; the [Karma test runner](https://karma-runner.github.io/1.0/index.html) and server, the [Jasmine testing framework](https://jasmine.github.io/), and [PhantomJS](http://phantomjs.org/) as the environment to run it all in.

In this blog post I'll explain how this is rather silly, and will provide an alternative and lightweight approach to writing and running unit tests. It will depend on having a certain way of defining your Angular components, and may not be a full 1:1 drop-in replacement, but I can say with a certainty that it'll make your tests faster, the overhead of running them a lot smaller, and improve the quality of tests by having less to worry about.

<!-- more -->

## Disclaimer, background and project structure

First, some disclaimers:

1. The title says Angular, but it's not really Angular specific. I am targeting it because Angular by default comes with the 'heavy' test setup by default.
2. It's been written with Angular 1.x in mind; at my assignment where we're building this we'll probably go to Angular 2 at some point. Small steps. I do think this approach can also be applied for Angular 2 and probably other frameworks, but I haven't gone there yet.

Second, some background; you can skip this part if you're familiar with how Angular applications should be structured:

At my current assignment, we mostly follow the [John Papa AngularJS style guide](https://github.com/johnpapa/angular-styleguide/blob/master/a1/README.md)'s approach of developing components, which dictates files and components to be very small and defined, having a single purpose, and have a filename descriptive of the content:

 * foo.controller.js
 * foo.view.html
 * foo.service.js
 * foo.component.js
 * routes.js
 * index.js

Now, the various .js files themselves usually contain little to no Angular-specific code; they're just functions that take a few arguments such as services and constants, or in the case of the component, just a configuration object that points to the template file and imports the controller via regular ES6 imports.

The index.js file ties it all together. It will include the service and component files, and register them within Angular. Something like this:

```javascript
import FooService from './foo.service';
import Foo from './foo.component';

angular.module('foo', [])
  .service('FooService', FooService)
  .component('Foo', Foo);
```

(note how we're not registering the controller; with Angular 1.5's [components](https://docs.angularjs.org/guide/component), you don't need to anymore.)

The index.js is either included by the main application index.js file, or by another application if it's a shared component.

When starting the test task, the default Angular test runner will boot up Karma, which generates a .html file test runner and starts a simple web browser, which in turn loads implementation and test files and runs then, usually in PhantomJS but it can also run it in any browser.

That last detail - can be run in any browser - is actually a Good Idea, it allows you to test your code in a number of browsers and detect browser-specific issues early on.

In practice however, I haven't actually seen this being used. It's pretty complicated for a company to set up a cluster of machines (virtual or otherwise) that is able to boot up multiple browsers to run tests in. There's 3rd parties (I believe) that offer test running services, but with any nontrivial application the costs of those services quickly outweigh the benefits. Another problem with using a 3rd party test runner service is the legal or perceived security issues in uploading code to a 3rd party; security is a non-issue in that case since it's usually client-side code, but there are a lot of companies that have strict rules about this kind of thing. This is usually the same kind of company that doesn't allow applications to be deployed on cloud providers. No judgment, just something to keep in mind.

## You may not need Karma

Complexity, cost, legal and performance reasons aside, honestly, you neither need nor should run your unit tests in multiple browsers nowadays. Two reasons:

1. If you're writing browser-specific JS, you're doing it wrong. Or you're writing a library, in which case, disregard this blog post. Libraries and tools like Babel, TSC and related polyfills should take away most if not all browser-specific issues. Second, it's 2016, usage of older browser has dropped to trivial amounts, and most browsers will support most features that tools like Babel will compile down to without needing polyfills. It shouldn't be a problem for any modern webapp to run under IE 9 and newer.

2. Unit tests should test logic, not browser quirks. What a unit test should do is go "if I call this function with these arguments, I expect this to happen". Nothing browser-specific in there. Don't waste time on things that are unlikely to happen. Unless you're writing a library or being clever, in which case, stop being clever. 

TL;DR: in my opinion, you don't need the complexity of running in multiple browsers, and therefore, you don't need the overhead of serving files and running your tests in a headless browser.

## A different approach to running tests

What I propose is simple: Run your tests in a simple NodeJS environment. Node starts fast, will run your JS and unit tests just as well as PhantomJS, and because if your applilcation is structured properly, you'll be able to test your application logic completely independent from AngularJS's dependency injection system, which is another source of both runtime overhead and mental overhead. If you have to write anything that isn't directly related to the component at hand, it's boilerplate and mental overhead (this includes a testing library's structural code and matchers, btw).

As a second advantage, with this approach we don't need all possible dependencies and modules to be loaded, and we can test files in isolation instead of having to build, assemble and load the entire application.

## Setting up the test runner

To enable this, we need to do only a few things:

 * Install `babel-cli` - unfortunately, NodeJS still doesn't support `import`, so just for that we're going to need a transpilation step. There might be a more lightweight version of adding support to `import` that doesn't transpile the whole application; Node 6 and newer should be able to run most if not all of the ES6 code natively.
 * Set up a Jasmine config and test runner. You can replace that with your favorite test framework and utilities if you want.
 * ?????
 * profit

We run this new test runner alongside of our existing tests at the moment; doing a full rewrite costs a lot of time and effort, it's boring work, and we still need to build features at the end of the day. Second, this runner is focused entirely on "logic" code - controllers, services, etc. I haven't figured out how to apply it to testing directives or views yet, which can also be tested.

So here's the new setup:

```json
// jasmine.json
{
  "spec_dir": "",
  "spec_files": [
    "src/**/*.spec.js"
  ]
}
```

Sprinkle options where applicable. Second, the test runner:

```javascript
// jasmine.js
import Jasmine from 'jasmine';

const jasmine = new Jasmine();
jasmine.loadConfigFile('jasmine.json')

// insert your favorite reporter here

// an onComplete handler is required to stop pre-push hooks and the like from pushing failing tests.
jasmine.onComplete(passed => process.exit(passed ? 0 : 1));

jasmine.execute();

```

Finally, add some tasks to `package.json` for convenience:

```json
{
  "scripts": {
    "test": "babel-node tools/run-jasmine.js",
    "watch": "babel-watch tools/run-jasmine.js --watch"
  }
}
```

Running `npm run test` should now start the test runner.

As for the tests themselves, which need to be rewritten to not have any trace of Angular left, here is a simple example:

```javascript
import FooController from './foo.controller'

let fooService, fooController

describe('The FooController', () {
  beforeEach(() => {
    fooService = jasmine.createMock('fooService', ['bar'])
    fooController = new FooController(fooService)
  })

  it('should prove something', () => {
    fooController.doTheThing();
    expect(fooService.bar).toHaveBeenCalledWith('9/11 was an inside job')
  })
})
```

This will run very fast due to a lack of overhead and a minimal amount of code loaded, and there's no trace of Angular or anything browser-specific. Profit!

This approach should work for most of the important parts of your application: controllers and services. Dependencies will need to be mocked out or replaced with their more native versions; what we do in our tests for example is load the nodejs version of [q](https://github.com/kriskowal/q) as a drop-in replacement for `$q`. An alternative would be to replace `$q` with a full mock service, but it's pretty challenging to reproduce actual promise mechanics.

## Testing asynchronous code

On that note, we need to replace another mechanic that is very commonly used in Angular when dealing with asynchronous code and promises: `$scope.$apply()`. In the browser-run tests, this triggers a digest loop and a JS cycle, allowing for callbacks to be executed before doing your assertions.

In NodeJS, the equivalent is `process.nextTick()`, but using it in this context can be a bit tricky, since you have to tell Jasmine when you're done. It basically goes something like this:

```javascript
it('should do something async', done => {
  fooService.doSomethingAsync();
  process.nextTick(() => {
    expect(fooService.result).toEqual('resolved result!1one')
    done();
  })
})

// alternatively, call nextTick in a beforeEach function;
// jasmine will only execute the "it"s when the beforeEach's done() is called.

describe('when a promise is resolved', () => {
  beforeEach(done => {
    fooService.doSomethingAsync()
    process.nextTick(done)
  })

  it('should have done something async', () => {
    expect(fooService.result).toEqual('resolved')
  })
})

// alternatively, you could also declare multiple beforeEach-es

beforeEach(() => fooService.doSomethingAsync())
beforeEach(promise.nextTick)
```

## Testing DOM-manipulating code

Here's where it becomes tricky and vague because I haven't actually gotten to this part yet, but, my colleague experimented a bit with this and managed to use [jsdom](https://github.com/tmpvar/jsdom) to run tests, which also included having Angular run. This partially defeats the purpose, but it will allow you to create and run specs that test DOM manipulation, mostly directives, components and/or views outside of the context of a browser. Of course, it's always possible to have multiple test runners in your application, separate between DOM manipulating tests and logical tests.

## Conclusion

This test runner should allow you to rewrite your tests - or mostly your test runner - in such a way that it should run a lot faster with a lot less memory and CPU overhead. In addition, it makes your tests simpler, reduces boilerplate, and reduces mental overhead because you no longer have to deal with loading the correct Angular modules, registering mocks with Angular's DI system, and injecting the service under test into the application. If you're suffering from long test runs, consider using this approach.

In our current project, we have (only) about a hundred or so test cases running (vs a thousand for the traditional test runner), but they run in approx 0.06 seconds on my machine, versus several seconds for the other tests. The main overhead in running tests is booting up node-babel, which relies on in-memory buffers and the like before it reaches maximal speed. Shouldn't be a problem for running tests in 'watch' mode. It might be possible to run Babel in daemon mode, to reduce this (short) overhead.

Finally, this approach might work for Angular 2; it depends on whether Typescript and Angular 2 allow you to write your logic in one file, and add Angular or framework-specific boilerplate in another file. This is true for Angular 1, but Angular 2 relies on annotations, which might cause problems. Of course, it should be possible to just ignore the annotations while running tests. 

_note: this post was cross-posted to [the Xebia blog](http://blog.xebia.com/an-alternative-angularjs-test-runner/)_