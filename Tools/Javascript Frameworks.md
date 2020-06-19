# AngularJS

Popular framework for building Single Page applications

## React and Knockout

Both try to solve the problem of 2 way binding:

1. Keeping the DOM synchronized with the changes to the model
2. Publishing, handling and managing events.
3. Both are declarative.

Knockout - wraps model properties in observables so that model changes can be detected and propagated back to the dom via events.

React - manually (write code) notify components when the model has changed.

Backbone - imperative (much more control to the programmer). React can be used as an alternative to the view component of Backbone

## Javascript testing

Javascript can run either in the browser or on a Javascript runtime like `nodejs` that is built on Chrome's V8 Javascript engine (written in C++ and used in the Google Chrome browser).

### Jasmine and Mocha

Jasmine and Mocha are test frameworks for writing and executing unit tests in JS.

Tests are run via an html file (e.g. spec-runner.html) that includes references to your source and test js files. It is possible to run Jasmine tests programmatically by using a test runner like `karma` rather than opening a browser each time you want to run tests.

Mocha is a mature JS testing framework running on nodejs and in the browser. Jasmine is more commonly used in angular projects, including the angular project itself.

### Karma

Test runner with nodejs dependency for running tests programmatically cross browsers and cross devices. You can target specific browser(s) like Chrome, Firefox, IE or PhantomJS (headless browser for faster test feedback) while running your tests.

## Javascript api testing framework

Testing REST apis with outside-in tests exploiting BDD test narratives

* http://dareid.github.io/chakram/
* https://github.com/apickli/apickli
