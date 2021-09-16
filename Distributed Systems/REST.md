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

[Caching in HTTP](https://datatracker.ietf.org/doc/html/rfc2616#page-74) supports a bunch of headers: 

* Responses with `Cache-Control: public` can be cached using the normal rules. A proxy will not cache a page if it is marked as `private`. The `no-cache` option just implies that the proxy should verify each time the page is requested if the page is still valid, but it may still store the page. A better option to add is `no-store` which will prevent request and response from being stored by the cache. 
* Responses to requests with `Authorization` header are automatically private, and aren't be cached by shared caches e.g. reverse proxies
* The `vary` header is used to ignore certain header fields in requests. You may decide to deliver the same content independent of the user agent, and as a result, `Vary: User-Agent` would help the proxy to identify that you don't care about the user agent.

A safe set of HTTP response headers may look like:

```sh
Cache-Control: private, no-cache, no-store, max-age=0, no-transform
Expires: 0
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