---
title:      "Extending AngularJS services with the Decorate method"
pubDate:       2014-08-08 11:00:54
description:    "Many large Angular applications tend to see a lot of repetition - same API endpoint, same method of dealing with and transforming data, etcetera. One technique you can use to at least alleviate that is using AngularJS's `decorate` method, which allows you to extend, adjust or even fully replace any existing service."
tags:
 - javascript
 - angularjs
 - promises
 - xebia blog
---

*Note: This post was originally published on [the Xebia blog](http://blog.xebia.com/2014/08/08/extending-angularjs-services-with-the-decorate-method/) ([archived copy](https://web.archive.org/web/20140919153051/http://blog.xebia.com/2014/08/08/extending-angularjs-services-with-the-decorate-method/)) on August 8th, 2014 by me; the published date of this repost has been backdated to match. Markup has been converted from WordPress HTML to Markdown.*

---

Many large Angular applications tend to see a lot of repetition - same API endpoint, same method of dealing with and transforming data, etcetera. One technique you can use to at least alleviate that is using AngularJS's `decorate` method, which allows you to extend, adjust or even fully replace any existing service.

As you'll see in this post, using this allows you to modify and extend the framework you build your app in, which will lead to a cleaner, more legible codebase, written in a more functional style (the what, not the how).

**Update 11/8:** [The follow-up is now live](http://blog.xebia.com/2014/08/11/the-angularjs-promise-dsl/), along with [the GitHub repository](https://github.com/fwielstra/ngPromiseDsl).

A feature not often used when developing AngularJS applications is the `$provide` service, which is the primary service used to register components with the `$injector`. More commonly, a developer would use methods like `$provide.service()` or `$provide.factory` to do so, but those are merely utility methods defined in the `$provide` service and exposed via `angular.module()`.

The main reasons to use `$provide` over the `service()` and `factory()` methods is to configure the service before it's instantiated, for example. While there may be more advanced use-cases for using `$provide`, I haven't yet encountered them while developing regular applications and I'm sure they won't occur often.

One of the methods listed at the very bottom of the `$provide` documentation is the `decorate()` method. It doesn't look like much (it's at the bottom, after all), but its documentation hints that it's very powerful:

> "A service decorator intercepts the creation of a service, allowing it to override or modify the behaviour of the service. The object returned by the decorator may be the original service, or a new service object which replaces or wraps and delegates to the original service."

Nothing to add there. You can use `decorate()` to change, add to, or completely replace the behaviour of services without having to edit its code. This can be done on any code not your own - core AngularJS services, but also third-party libraries. It's the equivalent of overriding methods in OO languages or monkey-patching in the more dynamic languages.

“Isn’t that evil?”, I hear you ask. As with every programming-related question, the only correct answer is: it depends. I’m going to give a few practical examples of when I believe using `decorate()` is appropriate. In a future blog post, I'll expand on this example, showing how relatively simple code can positively influence your entire application architecture.

Here’s a practical example, a neat follow-up on my previous blog about angular promises: decorating `$q` to add methods to the promise object. The [promise](http://wiki.commonjs.org/wiki/Promises) API itself defines only one method: `then()`. `$q` adds a few simple methods to that like `catch()` and `finally()`, but for your own application you can add a few more.

If you’ve been working with promises for a little while in your AngularJS application, you’ve probably noticed some operations are pretty common; assigning the promise result to the scope (or any object), logging the result in the console, or calling some other method. Using `decorate()`, we can add methods to the promise object to simplify those. Here's a bit of code from my previous post; we'll add a method to $q to remove the need for a callback:

```javascript
CustomerService.getCustomer(currentCustomer)
 .then(CartService.getCart)
 .then(function(cart) {
   $scope.cart = cart;
 })
 .catch($log.error);
```

First, we’ll need to do some boilerplate: we create a function that adds our methods to the promise object, and then we replace all the default promise methods. Note that the decorating function will also apply itself to the given promise.then method again, so that our customisations aren’t lost further down a promise chain:

```javascript
angular.module('ngPromiseDsl', [])
  .config(function ($provide) {
    $provide.decorator('$q', function ($delegate, $location) {

      // decorating method

      function decoratePromise(promise) {
        var then = promise.then;

        // Overwrite promise.then. Note that $q's custom methods (.catch and .finally) are implemented by using .then themselves, so they're covered too.

        promise.then = function (thenFn, errFn, notifyFn) {
          return decoratePromise(then(thenFn, errFn, notifyFn));
        };

        return promise;
      }

      // wrap and overwrite $q's deferred object methods

      var defer = $delegate.defer,
        when = $delegate.when,
        reject = $delegate.reject,
        all = $delegate.all;

      $delegate.defer = function () {
        var deferred = defer();
        decoratePromise(deferred.promise);
        return deferred;
      };

      $delegate.when = function () {
        return decoratePromise(when.apply(this, arguments));
      };

      $delegate.reject = function () {
        return decoratePromise(reject.apply(this, arguments));
      };

      $delegate.all = function () {
        return decoratePromise(all.apply(this, arguments));
      };

      return $delegate;

    });
  });
```

With that boilerplate in place, we can now start adding methods. As I mentioned earlier, one of the most common uses of a `then()` function is to set the result onto the scope (or some other object). This is a fairly trivial operation, and it’s pretty straightforward to add it to the promise object using our decorator, too:

```javascript
function decoratePromise(promise) {
  var then = promise.then;

  promise.then = function (thenFn, errFn, notifyFn) {
    return decoratePromise(then(thenFn, errFn, notifyFn));
  };

  // assigns the value given to .then on promise resolution to the given object under the given varName
  promise.thenSet = function (obj, varName) {
    return promise.then(function (value) {
      obj[varName] = value;
      return value;
    });
  };

  return promise;
}
```

That’s all. Put this .config block in your application's module definition, or create a new module and add a dependency to it, and you can use it throughout your application. Here's the same piece of code, now with our new thenSet method:

```javascript
CustomerService.getCustomer(currentCustomer)
  .then(CartService.getCart)
  .thenSet($scope, 'cart')
  .catch($log.error);
```

This particular example can be extended in a multitude ways to add useful utilities to promises. In my current project we’ve added a number of methods to the promise object, which allows us to reduce the number of callback definitions in our controllers and thus create cleaner, more legible code.

Replacing custom callbacks with named methods allows for a more functional programming style, and allows readers to read and write code as a list of “whats”, instead of “hows” - and it's also fully asynchronous.

Extending `$q` is just the start though: Every angular service can be extended for various purposes - add performance monitoring and logging to `$http`, set common prefixes or fixed properties on `$resource` urls or template paths, you name it. Leave a remark in the comments about how you've used `decorate()` to create a better application.

Stay tuned for an upcoming post where I release a small open source project that extends angular’s promise objects with a number of helpful methods to perform common tasks.

Further reading, resources, helpful links:

- [AngularJS documentation on $Provide](https://docs.angularjs.org/api/auto/service/$provide)
- [Ng-decorate](https://github.com/damienklinnert/angular-decorate), a library to simplify decorating services ([and a presentation about it](http://www.slideshare.net/damienklinnert/angular-decorate))
- [How to extend $q / promises](http://dorp.io/blog/extending-q-promises.html); this post was used as inspiration to get started.
- [Decorating core directives](http://briantford.com/blog/angular-hacking-core.html)
- How [Angular Batarang decorates $rootScope to work](https://github.com/angular/angularjs-batarang/blob/master/js/inject/debug.js#L712) ([source](http://www.cli-nerd.com/blog/2014/05/08/%24provide-dot-decorator/))
- [The Decorator pattern on Wikipedia](https://en.wikipedia.org/wiki/Decorator_pattern)
