# Javascript Frameworks

You need to manipulate HTML and CSS to create interactive websites. There are libraries and frameworks that allow you to manage the interactions between the HTML, CSS, and JavaScript according to their own rules. Libraries are more like tool kits that provide specific functions where as frameworks provide cross cutting application features and structure to your code, so that developers can focus on the parts unique to their application.

DOM - Document Object Model is a programming interface for web documents. It represents the page so that programs can change the document structure, style, and content. The DOM represents the document (HTML or XML document) as nodes and objects in memory; that way, programming languages like JavaScript can interact with the page.

The browser uses the HTML page to create the DOM tree, and it utilizes the DOM tree to render and display the content according to the specified styles and layout instructions. Therefore, your HTML source page and the contents of the DOM (represented in the Elements tab in DevTools) can be different.

```JavaScript

// Modify a page by adding an h3 element to the DOM
document.body.appendChild(document.createElement('h3'));
document.querySelector('h3').innerText = " I am not in the HTML source file";

```

## jQuery

Small, feature-rich Javascript library - collection of JS functions to manipulate HTML and CSS. With jQuery, DOM manipulation, AJAX calls, event handling, and animations become simple. For example, performing AJAX calls can be quite complex and can take many lines of code when done using vanilla JavaScript. jQuery, on the other hand, provides us functions that we can directly call to perform an AJAX call. It reduces complexity through abstraction.

## Angular

Popular web application framework by Google that helps you organise HTML and CSS for building Single Page applications. It uses MVC architecture and features like Dependency Injection, thus providing separation of concerns in your application.

Note that Angular is a complete rewrite of AngularJS, based on TypeScript

## React

React is a library for building web application User Interfaces (UI) that was originally written and used by Facebook. It is incredibly popular, and well supported. If you are familiar with the MVC (Model, View, Controller) architecture, it is the *View* part of it. Because it is just a View part, that means you may have to integrate it into an MVC framework, which can become complicated.

It uses declarative syntax and manages state by:

1. Keeping the DOM synchronized with the changes to the model by manually (write code) notifying components when the model has changed.
2. Publishing, handling and managing HTML events.

### React with Next.js

React is not a fully developed application framework - it is a **library for creating HTML** that can be used by applications or frameworks such as Next.js. Out of the box React doesn't focus on routing, API integration and server side rendering, it largely relies on 3rd party libraries to accomplish this. Next.js however adds all those features, plus it provides hybrid static and server rendering, TypeScript support, smart bundling, fast refresh and inbuilt CSS support with zero configuration.

Next.js is built on top of Node.js, enabling React-based web application functionalities, such as server-side rendering, and allowing the ability to generate static websites.

## Node.js

Node.js is a Javascript runtime built on the Chrome V8 JavaScript Engine. We often run JavaScript in a web browser, but Node.js allows us to easily run JavaScript outside of the browser and use JS on the server.  It uses event loop - a single-threaded, event-driven, non-blocking I/O model, making it lightweight, efficient, and simple to use for performing **asynchronous tasks** like

- Fetching data over a network
- Writing to a database
- Reading data from a file

Node.js is best for building real-time data-driven, I/O bound single-page applications, for example, live chats, and audio and video conferencing, etc. Node.js is not recommended for CPU-intensive applications that involve complex synchronous calculations with waiting times. As the load on the CPU increases, its efficiency decreases.

## Web application rendering

Depending upon the type of web application you require and the performance and user experience goals, [you can decide](https://www.freecodecamp.org/news/rendering-patterns/) the way in which HTML, CSS and JavaScript code is all processed and rendered in a web application or website.

1. **Server-side rendering (SSR)**: The web server generates the HTML content of a web page on the server-side and sends it to the client's browser. This approach can improve initial loading times and SEO (search engine optimization) but can be slower for dynamic content. Therefor it is mostly suitable for static content.
2. **Client-side rendering (CSR)**: In CSR, the client's browser generates the HTML content of a web page on the client-side using JavaScript. This approach can provide a fast and interactive user experience but can be slower for initial loading times and bad for SEO. These are typically suited for **Single Page Applications** (SPA) that provide a fast and interactive user experience because only the necessary content is loaded and rendered dynamically, reducing the need for full page reloads.
3. **Static site generation (SSG)**: In SSG, the HTML content of a web page is generated at build time and served to the client as a static file. This approach can provide excellent performance and security but can be less flexible for dynamic content.

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
