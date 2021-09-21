# What is REST

We think of resources as something the server sends to the client. The server sends a representation of the state of a resource. The client sends a representation that it would like the resource to have. This is **representational state transfer**.

* Resources have identity - can be identified by a URI (Universal resource Identifier).
* Resources have representations, renditions of their state in one or more formats. The representation could be XML, JSON document, HTML form’s post data or some binary format.
* Communication is stateless - can interact with each Resource independent of other requests.
* Common Interface -  If you are using HTTP, utilize HTTP features (HTTP verbs, status codes, headers ) whenever possible, instead of inventing conventions.
* A Restful API guides the client through its usage by describing in its responses how it can be used. By providing URLs to other allowed actions, it enables a client to discover a path through the application’s possible state transitions by means of hypermedia. Describing business workflows using hypermedia is termed **HATEOAS** Hypermedia as the engine of application state 

## Why bother with REST?

* Uniform interface means your resources is documentation is familiar (due to HTTP semantics) therefore it becomes easier to consume your API.
* Stateless communication means resources are loosely coupled. Service is reliable, performant, easy to scale and test.
* Hypermedia driven application means the consumer uses just one URI, and from that URI is able to deduce how to interact with the API by following links, as one would when using a website. In theory only one URI is needed to interact with the API. This [talk](https://vimeo.com/20781278) explains it in more detail.

### Resource modelling

Nouns, rather than verbs. Breaking information into hypermedia-linked structures reduces the load on a service by reducing the amount of data that has to be served. Instead of downloading the entire information model, the application transfers only the parts pertinent to the user.Information can be lazy loaded.

### HTTP semantics

* POST - Resource created acknowledgement with the resource state, the newly created URI in the response body and Http status code - 201

* PUT - PUT is **idempotent**. It can be used safely for absolute updates not relative updates, for example incrementing or decrementing state through PUT would make it non idempotent.

    * 200 OK with response body is more descriptive and actively confirms the server side state.
    * 204 No Content is more efficient since it returns no state and indicates that the server has accepted the request representation verbatim.
    * 409 Conflict - A request fails because of incompatibility between the consumer and service's view of the resource state, for example attempt to change an order when it has already been dispatched.

* PATCH - [RFC 5789](https://tools.ietf.org/html/rfc5789) is used for partial modifications to a resource. PUT overwrites the resource with a complete new body, whereas PATCH provides a change-set (delta) to the server to apply. A PATCH request can be idempotent, which helps prevent collisions between two PATCH requests on the same resource in a similar time frame.

* DELETE - Successful deletion should return a
    * 204 No Content response from the server as a confirmation.
    * 405 Method Not Allowed If the resource cannot be deleted, for example attempt to delete an order that has already been dispatched.

#### PUT or POST

[When to use PUT or POST](https://restfulapi.net/rest-put-vs-post/) can be a puzzle. For creating resources use PUT when the request URL of the resource is already known.

#### PUT or PATCH

*PATCH is update, PUT is replace*

Use PATCH when the client knows the diff between the server's representation & its own representation of the resource. The server must apply this change-set atomically & in isolation i.e. the operation is not guaranteed to succeed if the resource state on the server has changed from what the client received.

```sh
PATCH /user/foo HTTP/1.1
{  
   "user":{  
      "email":{  
         "from":"foo@yahoo.com",
         "to":"bar@gmail.com"
      }
   }
}
```

This request is going to replace the resource state regardless of what the state originally was, since there is no way for the server to know the validity of the request except from inclusion of additional header (If-Unmodified-Since or If-Match)  

```sh
PUT /user/foo HTTP/1.1

{  
   "user":{  
      "email":"foo@gmail.com"
   }
}

```

If the patch document size is larger than the size of the new resource data that would be used in a PUT, then it might make sense to use PUT instead of PATCH.

### Safety and Idempotency

PATCH is neither necessarily safe nor idempotent.

The idempotent semantics of PUT, GET and DELETE greatly simplifies dealing with intermittent problems and crash recovery by allowing the operation to be repeated in event of failure. Should PUT or DELETE fail due to a transient network or server error (e.g. a 503 response), the operation can safely be repeated. This helps proxies and caches and even clients and servers to be resilient based on the result of the operation.

### Caching in REST APIs

Being [cacheable](https://restfulapi.net/caching/) is one of the architectural constraints of REST. GET requests should be cachable by default – until special condition arises. Usually, browsers treat all GET requests cacheable. POST requests are not cacheable by default but can be made cacheable if either an Expires header or a Cache-Control header with a directive, to explicitly allows caching, is added to the response. Responses to PUT and DELETE requests are not cacheable at all.

[HTTP Caching](https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching) can be done in the browser/client, at the reverse proxy/CDN or at the origin/server. It supports a bunch of headers:

* [Cache-Control](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control)
  * `public` means a resource can be cached at the server. A proxy will not cache a resource if it is marked as `private`, the resource could be specific to a user and is only meant to be cached at the client.
  * `no-cache` option doesn't mean the cache wouldn't store the resource, it can. It just implies that the proxy should verify with the server each time the resource is requested whether the resource is still valid. The server can use an **ETag** which uniquely identifies the resource (e.g. by performing a hash) or **Last-Modified** to check if the resource has changed.
  * `no-store` option will prevent resources from being stored by the cache at all.
  * `must-revalidate` doesn't necessarily mean "must revalidate", it means the local resource can be younger than the provided `max-age`, so only revalidate if the content has expired.
  * `proxy-revalidate` Like `must-revalidate`, but only for shared caches (e.g., proxies). Ignored by private caches.
  * `max-age` the resource can be cached for the specified duration in seconds. This works well for independent resources but for mutable content with dependencies [max-age is the wrong choice](https://jakearchibald.com/2016/caching-best-practices/) as it can lead to the inter dependent resources getting out of sync.
* Responses to requests with `Authorization` header are automatically private, and aren't generally cached by shared/public caches e.g. reverse proxies
* `Vary` - Specifies a header value that can be different for different requests. When a cache receives a request that has a `Vary` header field, it must not use a cached response by default unless all header fields specified in the Vary header match in both the original (cached) request and the new request. For example
  * `Vary: Accept-Encoding` specifies `Accept-Encoding` value can be different for different requests e.g. `Accept-Encoding: gzip,deflate,sdch` A server can set `Vary: Accept-Encoding` to ensure that a separate version of a resource is cached for all requests that specify support for a particular set of encodings. You may want to allow a resource to be cached in uncompressed and (various) compressed forms, and served appropriately to user agents based on the encodings that they support.
  * `Vary: User-Agent` specifies `User-Agent` value can be different for mobile and desktop clients. This is useful for serving different content to desktop and mobile users

#### Caching authenticated requests

The rules for caching authenticated responses can be [tricky](https://stackoverflow.com/questions/39060208/authorization-check-for-http-caches). Section 14.8 of [RFC 2616](https://datatracker.ietf.org/doc/html/rfc2616#section-14.8) talks about the conditions under which shared caches can store and reuse such responses. They can be cached only when one of the following Cache-Control headers is present: `s-maxage`, `must-revalidate` or `public`.

The default behavior for responses that require authentication is to not be cached by shared proxies.

```sh
Cache-Control: private, s-maxage=0
```

But if you want to override this behavior you can ignore certain Cache-Control headers from the origin server and set your own Cache-Control header before sending the response. This will depend upon the sensitivity of the data, e.g. if you simply use expiration caching with `public` modifier, you run the risk of storing the data specific to a user in a public cache. This may still be okay as long as the request is being validated and authorized by the origin server.

```sh
Cache-Control: public ,no-cache 
# or 
Cache-Control: public, proxy-revalidate
```

### Modelling states of the business process as resources

Using hypermedia to drive business process through HTTP -> Possible next steps in the process. Instead of explicit choreography, use HTTP and hypermedia- friendly formats to describe transition between resources and allowing clients to choose among them at runtime.

Separate the act of defining links and adding meaning to the links. Use of rel attribute to represent the application semantics of a particular link. This identifies the relationships and interactions between resources.

On each interaction the service and consumer exchange representations of resource state not application state. But the application state isn’t recorded explicitly in the representation received by the consumer; it’s inferred by the consumer based on the state of all the resources—potentially distributed across many services—with which the consumer is currently interacting. *Hypermedia as the engine of application state* HATEOAS where application state is a snapshot of the entire system at a given instance.

Consumers in a hypermedia system cause state transitions by visiting and manipulating resource state. Interestingly, the application state changes that result from a consumer driving a hypermedia system resemble the execution of a business process. This suggests that our services can advertise workflows using hypermedia.

Robust services obey **Postel’s Law**, which states, “be conservative in what you do; be liberal in what you accept from others.” that is, a good service implementation is very strict about the resource representations it generates, but is permissive about any representations it receives.

### Domain specific hypermedia

A good hypermedia format conveys both Domain specific and protocol information. Domain specific information includes the values of elements used to model a business resources and protocol information defines the business flow.

Separate the act of defining links and adding meaning to the links. `rel` attribute is used to represent the application semantics of a particular link. It identifies the relationships and interactions between resources. For example if a payment needs to be cancelled

```javascript
"link": {
    "rel": "http://example.com/payment/cancel",
    "href": "http://example.com/payment/123"
 }
```

or

```javascript
"link": {
    "rel": "cancelPayment",
    "href": "http://example.com/payment/123"
 }
```

`href` indicates the payment to cancel whereas the `rel` relation link gives semantics to this link.

## Event driven systems

Event driven systems generally exhibit high degree of loose coupling, which allows failure isolation in services and independent evolution of services and consumers.

### Atom Based Pub Sub

In a system **Reference Data** is the kind of data other applications refer to in order to compete their own tasks. e.g. product and promotions data.

In order to decouple producers and consumers of reference data, this data can be published as a time-ordered atom feed continuously polled by a set of consumers. Consumers maintain their own local copy of the reference data until it becomes stale. Distributing information this way allows dependent services to continue to function even if network partitions or depending services (e.g. Reference Data) become temporarily available. This is exactly how the web scales.

A polling solution provides guaranteed delivery and ensures messages always arrive in order. Atom trades scalability for latency making it unsuitable for low latency notifications. In a system where messages can take seconds, minutes or even hours to arrive publishing Atom feeds works really well.

### Messaging or REST based feeds

For extremely low latency notifications, appropriate proprietary messaging middleware specific to the domain may be considered. The tradeoff is scalability for latency, but with added complication of middleware lock in. AMQP and JMS style messaging brokers are based on a centralised server that store and routes all the messages, therefore the broker can be a single point of failure. Since every service talks to a single broker, for every service sending a single message to the broker the broker needs to receive the message and send another message to the next service. With multiple services talking through the broker this can very quickly lead to bottlenecks. Services can be scaled in isolation but the broker would need to scale more than the services. Clustering is often utilized in production environments to avoid this.

Polling solution moves the **guaranteed message delivery** responsibility from the service or middleware to the consumer, where each consumer becomes responsible for ensuring that it retrieves all relevant information. Since messages are collocated in time-ordered feeds, there is no chance of  **out-of-order arrival** of messages.

Polling can result in bottlenecks as the number of consumers increase, with each consumer repeatedly asking the publisher - Is there any new data? The workload on the publisher can be reduced by introducing intermediate caching. This could be on the consumer or the publishing server.