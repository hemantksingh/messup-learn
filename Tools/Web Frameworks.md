# Web Frameworks

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

Popular web application framework by Google that helps you organise HTML and CSS for building Single Page Applications. It uses MVC architecture and features like Dependency Injection and separates concerns with **loosely coupled technical units** - Model, Views and Controllers.

Note that Angular is a complete rewrite of AngularJS, based on TypeScript

## React

React is a library for building web application User Interfaces (UI) that was originally written and used by Facebook. It is incredibly popular, and well supported. In an MVC (Model, View, Controller) architecture, it is the *View* part but it could be considered the controller too. It embraces the fact that rendering logic is inherently coupled with other UI logic: how events are handled, how the state changes over time, and how the data is prepared for display. Instead of artificially separating technologies by putting markup (View) and logic (Controller) in separate files, React separates concerns with **loosely coupled functional units** called “components” that contain both.

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

Next.js is a web application framework built on top of Node.js, enabling React-based web application functionalities, such as server-side rendering, and allowing the ability to generate static websites.

React is not a fully developed application framework - it is a **library for creating HTML** that can be used by applications or frameworks such as Next.js. Out of the box React doesn't focus on routing, API integration, data fetching and server side rendering, it largely relies on 3rd party libraries to accomplish this. Next.js is a [full-stack React framework](https://react.dev/learn/start-a-new-react-project) and adds all those features, plus it also provides: hybrid static and server rendering, TypeScript support, smart bundling, fast refresh and inbuilt CSS support with zero configuration.

## Node.js

Node.js is a Javascript runtime built on the Chrome V8 JavaScript Engine. We often run JavaScript in a web browser, but Node.js allows us to easily run JavaScript outside of the browser and use JS on the server.  It uses event loop - a single-threaded, event-driven, non-blocking I/O model, making it lightweight, efficient, and simple to use for performing **asynchronous tasks** like

- Fetching data over a network
- Writing to a database
- Reading data from a file

Node.js is best for building real-time data-driven, I/O bound single-page applications, for example, live chats, and audio and video conferencing, etc. Node.js is not recommended for CPU-intensive applications that involve complex synchronous calculations with waiting times. As the load on the CPU increases, its efficiency decreases.

## ASP.NET

Server side rendoring (SSR) technology for creating dynamic web content using HTML and C#. There are a [number of options](https://learn.microsoft.com/en-us/aspnet/core/tutorials/choose-web-ui?view=aspnetcore-8.0) for creating web apps using ASP.NET Core but these options can be used together as well

- Blazor
- Razor Pages
- MVC
- SPA with frontend [JS frameworks](../Tools/Javascript%20Frameworks.md) like React, Angular, Vue

The template engine (or View Engine in MVC) is used to generate the HTML from data. In SSR the HTML is generated on the server and sent back to the client browser. The preferred template engine for ASP.NET MVC is Razor. It allows you to write C# code inside HTML that is converted to plain HTML for the browser.

## Web application rendering

Depending upon the type of web application you require and the performance and user experience goals, [you can decide](https://www.freecodecamp.org/news/rendering-patterns/) the way in which HTML, CSS and JavaScript is processed and rendered in a web application or website.

1. **Server-side rendering (SSR)**: The web server generates the HTML content of a web page on the server-side and sends it to the client's browser. This is a good choice for
   - initial page loads, especially for users with slower internet connections or older devices. By providing a faster, more responsive experience, SSR can help to ensure that your website is accessible to a wider range of users.
   - SEO, as the HTML is available to be crawled allowing search engines to index the webpage.
   - accessibility or users with disabilities, as many assistive technologies, such as screen readers, rely on the HTML content of a page to provide information to users. With client-side rendering, the HTML content may not be fully generated until the JavaScript code has been executed, which can cause issues for users relying on assistive technologies.
   - simplicity of website's codebase. By moving some of the rendering logic to the server, developers can often simplify the client-side code, making it easier to maintain and update state. This can lead to a more [stable and reliable website](https://www.timr.co/server-side-rendering-is-a-thiel-truth/), helping improve the user experience for all visitors.
2. **Client-side rendering (CSR)**: In CSR, the client's browser first loads Javascript, any JSON and then generates the HTML content of a web page on the client-side using JavaScript.
   - Provides a fast and interactive user experience but can be slower for initial loading times and bad for SEO.
   - Typically suited for Single Page Applications (SPA) that require rich, interactive and complex interactions with extremely low latency. e.g. Figma or Google Docs. Such apps require only the necessary content to be loaded and rendered dynamically, **reducing the need for full page reloads**.
3. **Static site generation (SSG)**: In SSG, the HTML content of a web page is generated at build time and served to the client as a static file. A static site generator tool like Jekyll, Hugo, or Gatsby.js is used to compile the website's content from data sources such as markdown files, JSON files, or CMS data.
   - SSG pre-renders web pages at build time, there is no need to generate pages dynamically on the server or client-side, resulting in faster loading times and enhanced security but can be less flexible for dynamic content.
   - Suited for frequently updated content like blog posts or static product pages.

A hybrid approach might be more suitable using

- SSR for initial page loads, product listing and SEO
- CSR for interactive features like shopping carts, wishlists, and user accounts
- SSG for frequently updated static content like product, about us, or contact pages

### Implications for Micro-Frontends

- SSR and CSR are more suitable: Micro-Frontends work well with SSR and CSR because they allow for independent development and deployment of frontend functionalities.
- SSG might be less ideal: Since SSG builds the entire site at once, it's less flexible for independent micro-frontend deployments.

### Component Gallery

A centralised set of reusable UI components can serve as a single source of truth for developers, designers and other stakeholders across agile teams to discover, understand, and integrate these components into their projects.

- Reduced Development Time: Developers can quickly find and integrate pre-built components instead of starting from scratch.
- Improved Design Consistency: Galleries promote a unified look and feel across applications by providing a single source of design elements.
- Enhanced Collaboration: Galleries improve communication between designers and developers by providing a shared understanding of components.

Component galleries are a natural fit for React due to its component-based nature but Vue.js and Angular can also be used for building shared user interfaces. While some galleries might be framework-specific, consider designing them with a **technology-agnostic approach** when possible. This allows showcasing components that could be integrated with multiple frameworks or vanilla JavaScript.

Component galleries are a good fit for SSG pipelines.

- The component gallery defines data about each component (e.g. component name, description, usage examples code snippets, accessibility considerations, visual examples and demos) and stores it in JSON or Markdown files.
- SSG framework can utilise the component data and documentation files during the build process to generate static HTML pages for each component in the gallery.
- Live Previews: You can introduce live previews and interactive elements using client-side JavaScript within the generated HTML.
- CMS Integration: If you have a large number of components or need frequent updates, consider integrating the SSG gallery with a CMS. This allows content editors to manage component information without rebuilding the entire site.