# Synchronous request/response‑based integration

Gregor Hohpe and Bobby Woolf provide 65 [integration patterns](http://www.enterpriseintegrationpatterns.com/patterns/messaging/) for integration and coordination between disparate services. These include shared database, file transfer and [messaging](http://www.enterpriseintegrationpatterns.com/patterns/messaging/toc.html) but here we look at synchronous request/response based integration where services are often built as APIs - https://blog.apisyouwonthate.com/

## REST

REST is about a client-server relationship, where server-side data are made available through representations of data in simple formats, often JSON and XML. These representations for resources, or collections of resources, which are then potentially modifiable, with actions and relationships being made discoverable via a method known as hypermedia. Hypermedia is the concept of providing links to other resources and is fundamental to REST.

HTTP based REST is a familiar standard. HTTP helps to enforce REST constraints such as modelling resources, providing a uniform interface, stateless requests and discoverability and self describing relationships through hypermedia. [Maturity model for REST](https://martinfowler.com/articles/richardsonMaturityModel.html) can be used as a technique for incrementally enforcing REST constraints in your APIs.

With HTTP REST you end up with API endpoints with the same path but different behaviour depending upon the verb (GET, POST) or the Content-Type.

Getting a resource

```
GET /avatars HTTP/1.1
Host: localhost:3000
Content-Type: application/json
Content-Length: 284

{
  "name" : "hemantksingh",
  "image" : "http://example.org/pic.png"
}
```

Uploading an image in the HTTP body

```
POST /avatars HTTP/1.1
Host: localhost:3000
Content-Type: image/jpeg
Content-Length: 284

raw image content
```

Support `application/json` requests on the same endpoint to handle the upload slightly differently

```
POST /avatars HTTP/1.1
Host: localhost:3000
Content-Type: application/json

{
  "image_url" : "https://example.org/pic.png"
}
```

### Standardising REST APIs

[JSON API](http://jsonapi.org/) is a spec for standardising REST APIS with a designated media type ` application/vnd.api+json` for content negotiation. It has a predefined format for fetching data, related resources, sorting, pagination and filtering.

At first glance, it appears very verbose obfuscating your resource data under JSON API exchange semantics. Is it worth adopting for every API you are going to build ? Is there a universal standard that covers every use case? This [thread](https://news.ycombinator.com/item?id=9280058) captures the essence of the argument about standardising APIs.

We should not confuse and API with a transport protocol (which is what JSON API seems to do). Making transports human readable appears to be a waste of resources. Those API's are meant to be consumed by machines and debugging can and should be done with tools, not by enforcing a standard. Lets work on improving the semantics and documentation around what constitutes an API e.g. Swagger.

If you have large and/or public API which needs to be stable, extensible, will be developed for years, JSON API maybe a good choice. It is a lot of overhead for a private API between one client and one server which might be completely reworked in a year.

## RPC

RPC is the technique of making a local call and having it execute on a remote service somewhere. RPC-over-HTTP enables client programs to use the internet to execute procedures provided by server programs on distant networks. HTTP and RPC run on top of (use) TCP. TCP allows computers to send arbitrary length data to each other with guaranteed delivery. RPC is at layer 5 (Session) in the OSI model. It is dependent on having a **common interface definition** for describing message data types and service definition (available service methods) which happens to be either

* SOAP: SOAP uses **UDDI** - XML based registry for service description and discovery and **WSDL** for interface definition.
* [Thrift](https://thrift.apache.org/) originally developed by Facebook based on their Scalable cross-language services  [paper](https://thrift.apache.org/static/files/thrift-20070401.pdf)
* [Protocol buffers](https://developers.google.com/protocol-buffers/docs/overview) by Google used in gRPC - is a stricter type system than Xml or Json

In earlier RPC implementations like *.Net Remoting* and *Java RMI* the interface definition was platform dependent. This meant a Java based service could not be invoked by a .Net client and vice versa. Xml being platform independent, XML-RPC or SOAP based APIs attempted to resolve this interoperability problem.

However ensuring data types of XML payloads in XML-RPC is tough. In XML, a lot of things are just strings, so you need to layer meta data on top in order to describe things such as which fields correspond to which data types. This means a SOAP envelope (message) can be incredibly verbose as compared to a JSON message in a JSON based API such as [Slack](https://api.slack.com/web)

SOAP is a network protocol which is routed over HTTP but ignores the existing well understood HTTP specification (HTTP verbs and the error codes are ignored). Moreover there are inconsistencies in different implementations of SOAP by different vendors therefore it still suffered from some degree of **platform coupling**.

### Thrift and gRPC

gRPC largely follows HTTP semantics over HTTP/2 but explicitly allows for full-duplex streaming.

* It diverges from typical REST conventions as it uses static paths during call dispatch for performance reasons. Parsing call parameters from paths, query parameters and payload body adds latency and complexity.
* It also has a formalized set of errors that are more directly applicable to API use cases than the HTTP status codes.

A comparison of Thrift and gRPC can be found [here](https://groups.google.com/forum/#!msg/grpc-io/JeGybvbz8nc/wpqQdAfuBwAJ)

## REST or RPC

https://www.smashingmagazine.com/2016/09/understanding-rest-and-rpc-for-http-apis/

REST helps you model your domain as resource or entities whereas RPC based APIs are great for actions i.e. commands. RPC may be a better fit if you are writing your API in a functional language.

The fact that a remote procedure appears to be executing locally may lead to

* over use and over reliance on the network. Assumption that the network is reliable is a **fallacy of distributed computing**.
* chatty APIs that break encapsulation and expose the API's internal behavior and state leading to **behavioral coupling**.

Rather than coupling to procedures in RPC a so called REST based API could easily suffer from coupling to URLs that expose functions. Therefore a single URL per resource in HTTP based REST is quite crucial to avoid behavioral coupling. Adopting a design based upon **coarse-grained message exchange** can help alleviate over reliance on the network and behavioral coupling.

Compared to REST conventions RPC uses static paths during call dispatch for performance reasons as parsing call parameters from paths, query parameters and payload body adds latency.

## GraphQL

https://philsturgeon.uk/api/2017/01/24/graphql-vs-rest-overview/

GraphQL allows you to specify the fields you would like to be returned (**sparse fieldsets**), allowing you to skip all data that is not relevant to your response. This makes the request a little bit faster to download over the network, as the tubes do not get quite so full.

GraphQL allows to track field usage by clients that prevents introduction of breaking changes into your API, thus makes deprecations easy.

GraphQL devloves power to clients by allowing them to write their own queries - Having diverse client apps like iOS, Andrioid and web app accessing the same API can be a limiting choice as the data required by each could be very different. In the REST world this might mean:

* Creating custom endpoints: `/iphone`
* Create custom representations using `Content-Type: application/vnd.turtlefans.com+v1+iphone+json`
* Custom APIs - APIS for each client (Back ends for Front ends)

GraphQL's query language moves the responsibility out of the hands of the API devs and into the clients.