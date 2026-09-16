# Search Engine Optimization

* [Google SEO Guide](http://static.googleusercontent.com/media/www.google.com/en//webmasters/docs/search-engine-optimization-starter-guide.pdf)

* Decreased keyword density for the words being targeted in the URL, the longer the URL the less emphasis is being placed on the keywords being targeted in the URL

* Decreased emphasis on the importance of the page from a search engine standpoint, the further the page rests off of the root the less importance is attributed to that page

* Decreased adaptability over time, for example when time comes to redesign the site again in the future, suppose the navigation changes, by incorporating the folder you have reduced your ability to re-use the URLs on the new site and minimize any slippage in the search results

* Decreased usability for advertising the URL, suppose [company] wants to run a print campaign on a particular [product], the shorter URL would be more user friendly and more likely to lead to a conversion

Pages with faster response times [reduce bounce rate](https://blog.kissmetrics.com/loading-time/) and they can even [improve your ranking in Google searches](https://webmasters.googleblog.com/2010/04/using-site-speed-in-web-search-ranking.html). 

## Website Performance Tools

There are various tools for measuring website performance from free ones to paid

* Google PageSpeed Insights (PSI) and Lighthouse (available in Chrome DevTools) analyse web performance, generating a report (available on a URL) of the overall speed of your website and SEO indicators.
  * PSI uses the lighthouse APIs to calculate the overall performance score for your website and enriches it with real world data. The performance score is a weighted average of the metrics score. The weightings keep changing based on the research and feedback to understand what is the biggest impact on user-perceived performance.
  * To provide a good user experience, sites should strive to have a good score (90-100). More [heavily weighted metrics](https://developer.chrome.com/docs/lighthouse/performance/performance-scoring/?utm_source=lighthouse&utm_medium=lr#lighthouse-10) have a bigger effect on your Performance score like
    * **Total blocking time** - Sum of all time periods between First Contentful paint and Time to Interactive
    * **Largest contentful paint** - time at which the largest text/image is painted.  Top-performing sites render LCP in about 1,220ms
    * **Cumulative layout shift** - measures the movement of visible elements within the viewport
  * The scoring distribution is a log-normal distribution derived from the performance metrics of real website performance data on [HTTP Archive](https://httparchive.org/).
  * You can integrate Lighthouse API into your systems and run audits programmatically

* [WebPageTest](http://www.webpagetest.org/) can be used to get some numbers to start with. After getting the test results, the big question is: **What do the results mean**?
  
  * **Time to first byte** - Measured from the time the request is made to the host server to the time the first byte of the response is received by the browser. It primarily highlights issues with the back end server. It does not impact the overall user experience **significantly** as reducing it would only mean the first byte downloads quicker but the user is still seeing a blank page after this is measured until the page is fully loaded and rendered.
  
  * **Start render** - Indicates when content begins to display in the user’s browser. This term seems to have evolved as an alternative to “end-user response time”, but it’s not yet widely used outside of hardcore performance circles
  
  * **Load time** - The time it takes for all page resources to render in the browser — from those you can see, such as text and images, to those you can’t, such as third-party analytics scripts. Load time is also known as “document complete time” or “onLoad time”. It’s measured when the browser fires an `onLoad` event after all the page resources (DOM) have fully loaded. The ideal load time is thought to be **[2 seconds or less](http://www.webperformancetoday.com/2010/12/14/the-quest-for-the-holy-grail-of-website-speed-2-second-page-load-times/)**. Roughly speaking, load time includes:

    * Getting all markup, replaced element content and embeds from server
    * Parsing the markup
    * Applying the CSS cascade to the markup
    * Rendering the page
    * Running all scripts that need to run on page load (which may include scripts that get more content and cause further parsing and rendering)
    * From the user's point of view, load time is the time between navigating to a page and being able to access, visually and every other way, the finished output.

  * **Time to interactive (TTI)** - Even if the page resources have loaded, some asynchronous resources may still be downloading. This could be the time the entire page is ready post this asynchronous download, to be interacted with by the user
