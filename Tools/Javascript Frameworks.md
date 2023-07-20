# Javascript Frameworks

You need to manipulate HTML and CSS to create interactive websites. There are libraries and frameworks that allow you to manage the interactions between the HTML, CSS, and JavaScript according to their own rules. Libraries are more like tool kits that provide specific functions where as frameworks provide cross cutting application features and structure to your code, so that developers can focus on the parts unique to their application.

**Document Object Model (DOM)** is a programming interface for web documents. It is a JavaScript representation of the HTML in a page so that programs can change the document structure, style, and content. The DOM represents the document (HTML or XML document) as nodes and objects in memory; that way, programming languages like JavaScript can interact with the page.

The browser uses the HTML page to create the DOM tree, and it utilizes the DOM tree to render and display the content according to the specified styles and layout instructions. Therefore, your HTML source page and the contents of the DOM (represented in the Elements tab in DevTools) can be different.

```JavaScript

// Modify a page by adding an h3 element to the DOM
document.body.appendChild(document.createElement('h3'));
document.querySelector('h3').innerText = " I am not in the HTML source file";

```

The DOM structure should be identical for browsers with the same capabilities, meaning any desktop browser should be loading the same DOM structure for the same document. However mobile browsers may be loading a different DOM structure if the UI is made responsive.

## jQuery

Small, feature-rich Javascript library - collection of JS functions to manipulate HTML and CSS. With jQuery, DOM manipulation, AJAX calls, event handling, and animations become simple. For example, performing AJAX calls can be quite complex and can take many lines of code when done using vanilla JavaScript. jQuery, on the other hand, provides us functions that we can directly call to perform an AJAX call. It reduces complexity through abstraction.

## Angular

Popular web application framework by Google that helps you organise HTML and CSS for building Single Page applications. It uses MVC architecture and features like Dependency Injection, thus providing separation of concerns in your application.

Note that Angular is a complete rewrite of AngularJS, based on TypeScript

## React

React is a library for building web application User Interfaces (UI) that was originally written and used by Facebook. It is incredibly popular, and well supported. In an MVC (Model, View, Controller) architecture, it is the *View* part but it could be considered the controller too. It embraces the fact that rendering logic is inherently coupled with other UI logic: how events are handled, how the state changes over time, and how the data is prepared for display. Instead of artificially separating technologies by putting markup and logic in separate files, React separates concerns with loosely coupled units called “components” that contain both.

React uses JSX - a declarative syntax to embed JavaScript into HTML

```javascript
// React JSX allows switching from HTML to JavaScript using '{}'
function App() {
    const names = ['foo', 'bar', 'lol']
     
    function renderWelcome(name) {
        
        return <h1>Hello {name}!</h1>
    }

    return (
        <div>
            {
                // Entire JS is available inside braces, including functions
                names.map(name =>renderWelcome(name))
            }
        </div>
    )
}
```

### Next.js

React is not a fully developed application framework - it is a **library for creating HTML** that can be used by applications or web application frameworks such as Next.js

Out of the box React doesn't focus on routing, API integration, data fetching and server side rendering, it largely relies on 3rd party libraries to accomplish this. Next.js however adds all those features, plus it provides hybrid static and server rendering, TypeScript support, smart bundling, fast refresh and inbuilt CSS support with zero configuration.

Next.js is built on top of Node.js, enabling React-based web application functionalities, such as server-side rendering, and allowing the ability to generate static websites.

## Node.js

Node.js is a Javascript runtime built on the Chrome V8 JavaScript Engine. We often run JavaScript in a web browser, but Node.js allows us to easily run JavaScript outside of the browser and use JS on the server.  It uses event loop - a single-threaded, event-driven, non-blocking I/O model, making it lightweight, efficient, and simple to use for performing **asynchronous tasks** like

- Fetching data over a network
- Writing to a database
- Reading data from a file

Node.js is best for building real-time data-driven, I/O bound single-page applications, for example, live chats, and audio and video conferencing, etc. Node.js is not recommended for CPU-intensive applications that involve complex synchronous calculations with waiting times. As the load on the CPU increases, its efficiency decreases.

## Web application rendering

Depending upon the type of web application you require and the performance and user experience goals, [you can decide](https://www.freecodecamp.org/news/rendering-patterns/) the way in which HTML, CSS and JavaScript code is all processed and rendered in a web application or website.

1. **Server-side rendering (SSR)**: The web server generates the HTML content of a web page on the server-side and sends it to the client's browser. This approach can improve
   - initial load times, as the HTML is already generated and ready to be displayed as soon as the page loads, especially for users with slower internet connections or older devices. By providing a faster, more responsive experience, SSR can help to ensure that your website is accessible to a wider range of users.
   - SEO, as the HTML is available to be crawled allowing search engines to index the webpage.
   - accessibility or users with disabilities, as many assistive technologies, such as screen readers, rely on the HTML content of a page to provide information to users. With client-side rendering, the HTML content may not be fully generated until the JavaScript code has been executed, which can cause issues for users relying on assistive technologies.
   - simplicity of website's codebase. By moving some of the rendering logic to the server, developers can often simplify the client-side code, making it easier to maintain and update. This can lead to a more stable and reliable website, which can help to further improve the user experience for all visitors.
2. **Client-side rendering (CSR)**: In CSR, the client's browser generates the HTML content of a web page on the client-side using JavaScript. This approach can provide a fast and interactive user experience but can be slower for initial loading times and bad for SEO. These are typically suited for **Single Page Applications** (SPA) that provide a fast and interactive user experience because only the necessary content is loaded and rendered dynamically, reducing the need for full page reloads.
3. **Static site generation (SSG)**: In SSG, the HTML content of a web page is generated at build time and served to the client as a static file. A static site generator tool like Jekyll, Hugo, or Gatsby.js is used to compile the website's content from data sources such as markdown files, JSON files, or CMS data. Since SSG renders web pages at build time, there is no need to generate pages dynamically on the server or client-side. This approach reduces the processing overhead and enables faster loading times and enhanced security but can be less flexible for dynamic content.

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
