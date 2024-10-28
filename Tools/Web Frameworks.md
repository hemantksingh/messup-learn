# Web Frameworks

You need to manipulate HTML and CSS to create interactive websites. There are libraries and frameworks that allow you to manage the interactions between the HTML, CSS, and JavaScript according to their own rules.

## Web application rendering

Depending upon the type of web application you require and the performance and user experience goals, [you can decide](https://www.freecodecamp.org/news/rendering-patterns/) the way in which HTML, CSS and JavaScript is processed and rendered in a web application or website.

1. **Server-side rendering (SSR)**: The web server generates the HTML content of a web page on the server-side and sends it to the client's browser. This is a good choice for
   - faster initial page loads, because UI rendering is performed quickly on the server without the need to download a large JavaScript bundle. By providing a faster, more responsive experience, SSR can help to ensure that your website is accessible to a wider range of users, especially those with slower internet connections or older devices.
   - SEO, as the HTML is available to be crawled allowing search engines to index the webpage.
   - accessibility or users with disabilities, as many assistive technologies, such as screen readers, rely on the HTML content of a page to provide information to users. With client-side rendering, the HTML content may not be fully generated until the JavaScript code has been executed, which can cause issues for users relying on assistive technologies.
   - simplicity of website's codebase. By moving some of the rendering logic to the server, developers can often simplify the client-side code, making it easier to maintain and update state. This can lead to a more [stable and reliable website](https://www.timr.co/server-side-rendering-is-a-thiel-truth/), helping improve the user experience for all visitors.
2. **Client-side rendering (CSR)**: In CSR, the client's browser first loads Javascript, any JSON and then generates the HTML content of a web page on the client-side using JavaScript.
   - Provides a fast and interactive user experience but can be slower for initial loading times and bad for SEO.
   - Typically suited for Single Page Applications (SPA) that require rich, interactive and complex interactions with extremely low latency. e.g. Figma or Google Docs. Such apps require only the necessary content to be loaded and rendered dynamically, **reducing the need for full page reloads**.
3. **Static site generation (SSG)**: In SSG, the HTML content of a web page is generated at build time and served to the client as a static file. A static site generator tool like Jekyll, Hugo, or Gatsby.js is used to compile the website's content from data sources such as markdown files, JSON files, or CMS data.
   - SSG pre-renders web pages at build time, there is no need to generate pages dynamically on the server or client-side, resulting in faster loading times and enhanced security but can be less flexible for dynamic content.
   - Suited for content that doesn't change frequently like blog posts, news articles or product details pages.

A hybrid rendering can significantly optimise SEO, performance, and user experience.

- SSR for initial page loads like home page, product listing. 
  - If the homepage content is relatively stable (e.g., promotional banners, featured products), SSG is preferred as it offers very fast load times. If the homepage features personalized or frequently changing content (like real-time promotions or user-specific product recommendations), SSR would be more suitable. 
  - Product listings are highly dynamic, often changing with stock updates, pricing adjustments, and promotions. SSR ensures that users and search engines get the latest information on the page each time it’s loaded.
  - Both SSG and SSR are effective for SEO, but SSG will be faster for repeat visits as it can be served from the cache.
- CSR for interactive features like basket/shopping carts, checkout, user accounts and order history
  - highly personalized, with user-specific data that doesn’t require search engine indexing
- SSG for static content that doesn't change often like about us, or contact pages.
  - SSG reduces server load by caching these pages and improves performance by serving them directly from the CDN.

### Micro-Frontend Impact

- Micro frontends can lead to complexity in SSR content 
  - Because each micro frontend might need to call its own backend API, coordinating these calls during SSR can lead to performance bottlenecks. For instance, a product listing micro frontend calling its service while an authentication micro frontend also fetches user data can increase the total server response time.
  - To mitigate this, SSR-based micro frontends should be carefully managed to avoid redundant data fetching, possibly by consolidating backend calls through an orchestrator or using a shared data layer
  - An orchestrator (such as a composition layer on the server) is often necessary to render the final HTML by combining outputs from each micro frontend. This composition layer must manage the layout, hydration, and routing of each micro frontend, adding a layer of complexity to SSR-based micro frontend applications.v
- CSR aligns well with micro frontend architectures, as each micro frontend can independently handle its client-side logic, making it ideal for interactive and user-specific content (e.g., cart, checkout, account pages).
  - Each micro frontend can be loaded asynchronously, reducing the initial bundle size and improving initial load performance. This approach also enhances modularity, allowing teams to update micro frontends independently.
  - Since CSR renders the content in the browser, each micro frontend must handle data loading on the client side, which can impact performance if not optimized with lazy loading, caching, or background data fetching
- SSG works well with micro frontends because it allows each micro frontend to be pre-rendered independently, making it easy to generate static content for parts of the application that don’t change often, such as product detail pages, blog posts, or FAQs.
  - With micro frontends, each part of the site can be re-deployed independently, making it easier to apply incremental static generation (e.g., only regenerate product details that were updated) to each micro frontend.
  - SSG micro frontends are well-suited to be served from a CDN, providing fast, cached responses for static content like product pages or marketing content, boosting load times across regions.

## jQuery

Small, feature-rich Javascript library - collection of JS functions to manipulate HTML and CSS.

### Document Object Model (DOM)

DOM is a programming interface for web documents. It is a JavaScript representation of the HTML in a page so that programs can change the document structure, style, and content. The DOM represents the document (HTML or XML document) as nodes and objects in memory; that way, programming languages like JavaScript can interact with the page.

The browser uses the HTML page to create the DOM tree, and it utilizes the DOM tree to render and display the content according to the specified styles and layout instructions. Therefore, your HTML source page and the contents of the DOM (represented in the Elements tab in DevTools) can be different.

```JavaScript

// Modify a page by adding an h3 element to the DOM
document.body.appendChild(document.createElement('h3'));
document.querySelector('h3').innerText = " I am not in the HTML source file";

```

The DOM structure should be identical for browsers with the same capabilities, meaning any desktop browser should be loading the same DOM structure for the same document. However mobile browsers may be loading a different DOM structure if the UI is made responsive.

### jQuery DOM manipulation

With jQuery, DOM manipulation, AJAX calls, event handling, and animations become simple. For example, performing AJAX calls can be quite complex and can take many lines of code when done using vanilla JavaScript. jQuery, on the other hand, provides us functions that we can directly call to perform an AJAX call. It reduces complexity through abstraction.

## Angular

Popular web application framework by Google that helps you organise HTML and CSS for building Single Page Applications. It uses MVC architecture and features like Dependency Injection and separates concerns with **loosely coupled technical units** - Model, Views and Controllers.

Note that Angular is a complete rewrite of AngularJS, based on TypeScript

## React

React is a library for building web application User Interfaces (UI) that was originally written and used by Facebook. It is incredibly popular, and well supported. In an MVC (Model, View, Controller) architecture, it is the *View* part but it could be considered the controller too. It embraces the fact that rendering logic is inherently coupled with other UI logic: how events are handled, how the state changes over time, and how the data is prepared for display. Instead of artificially separating technologies by putting markup (View) and logic (Controller) in separate files, React separates concerns with **loosely coupled functional units** called “components” that contain both.

React uses JSX - a declarative syntax to embed JavaScript into HTML

```javascript
// React JSX allows switching from HTML to JavaScript using curly braces '{}'
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

Next.js is a JavaScript/TypeScript-based React framework built on top of Node.js, that provides server-side rendering (SSR), static site generation (SSG), and client-side rendering (CSR) in a single application.

React is not a fully developed web application framework - it is a **library for creating HTML** that can be used by applications or frameworks such as Next.js. Out of the box React doesn't focus on routing, API integration, data fetching and server side rendering, it largely relies on 3rd party libraries to accomplish this. Next.js is a [full-stack React framework](https://react.dev/learn/start-a-new-react-project) and adds all those features, plus it also provides:

- Hybrid static (SSR), client (CSR) and server (SSR) rendering. Developers can decide at a per-page level to serve content using SSR, pre-render with SSG, or fetch data client-side, which allows for greater control over performance.
- It also supports Incremental Static Regeneration (ISR), which automatically regenerates static content at runtime, combining the performance of SSG with the freshness of SSR.
- This flexibility makes Next.js ideal for high-traffic and SEO-focused sites, where varying levels of content freshness are required.
- Next.js supports **PWA features** natively, enabling offline caching and background sync with service workers. This is particularly useful for mobile-first applications that need to work offline or in low-connectivity areas.

## Node.js

Node.js is a Javascript runtime built on the Chrome V8 JavaScript Engine. We often run JavaScript in a web browser, but Node.js allows us to easily run JavaScript outside of the browser and use JS on the server.  It uses event loop - a single-threaded, event-driven, non-blocking I/O model, making it lightweight, efficient, and simple to use for performing **asynchronous tasks** like

- Fetching data over a network
- Writing to a database
- Reading data from a file

Node.js is best for building real-time data-driven, I/O bound single-page applications, for example, live chats, and audio and video conferencing, etc. Node.js is not recommended for CPU-intensive applications that involve complex synchronous calculations with waiting times. As the load on the CPU increases, its efficiency decreases.

## ASP.NET

Server side rendoring (SSR) technology for creating dynamic web content using HTML and C#. There are a [number of options](https://learn.microsoft.com/en-us/aspnet/core/tutorials/choose-web-ui?view=aspnetcore-8.0) for creating web apps using ASP.NET Core but these options can be used together as well

- Blazor - supports both SSR and client interactivity in a single programming model where UI interactions are handled from the server over a real-time connection with the browser using SignalR. Minimises initial load times but each user requires a persistent connection to the server, impacting scalability for high-traffic apps.
- Razor Pages - page based model for building SSR apps with Razor as the template engine (or View Engine in MVC). Razor can work in both SSR mode (with MVC) and hybrid rendering mode with:
  - Blazor Server - SSR with persistent connections, enabling real-time interactivity and a reduced initial load.
  - Blazor WebAssembly - runs .NET code in the browser without the need for a persistent server connection, but initial download size, including the .NET runtime can impact performance.
- MVC - enables SSR apps using the MVC pattern where user requests are routed to a controller responsible for handling user actions or retrieve data for queries. The controller chooses the view to display to the user and provides it with any model data it requires.
- SPA with frontend [JS frameworks](../Tools/Javascript%20Frameworks.md) like React, Angular, Vue

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