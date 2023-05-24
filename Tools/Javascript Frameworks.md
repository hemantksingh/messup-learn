# Angular

Popular web application framework for building Single Page applications

## React

React is a library for building web application user interfaces that was originally written and used by Facebook. It is incredibly popular, and well supported. React is not a fully developed application framework - it is a **library for creating HTML** that can
be used by applications or frameworks such as Next.js.

It uses declarative syntax and tries to solve the problem of 2 way binding:

1. Keeping the DOM synchronized with the changes to the model by manually (write code) notifying components when the model has changed.
2. Publishing, handling and managing events.

## Javascript testing

Javascript can run either in the browser or on a Javascript runtime like `nodejs` that is built on Chrome's V8 Javascript engine (written in C++ and used in the Google Chrome browser).

### Jasmine and Mocha

Jasmine and Mocha are test frameworks for writing and executing unit tests in JS.

Tests are run via an html file (e.g. spec-runner.html) that includes references to your source and test js files. It is possible to run Jasmine tests programmatically by using a test runner like `karma` rather than opening a browser each time you want to run tests.

Mocha is a mature JS testing framework running on nodejs and in the browser. Jasmine is more commonly used in angular projects, including the angular project itself.

### Karma

Test runner with nodejs dependency for running tests programmatically cross browsers and cross devices. You can target specific browser(s) like Chrome, Firefox, IE or PhantomJS (headless browser for faster test feedback) while running your tests.

### Javascript API testing framework

Testing REST apis with outside-in tests exploiting BDD test narratives

* http://dareid.github.io/chakram/
* https://github.com/apickli/apickli
