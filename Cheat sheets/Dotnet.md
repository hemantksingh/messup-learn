# .NET

## OWIN (Open Web Interface for .Net)

OWIN provided a standard interface for separation between Webapp framework (like ASP.Net) and Webserver (like IIS). It allowed ASP.Net apps to be self hosted running in a console process and to be hosted on linux running mono. Self hosted apps do not have to go through IIS pipelines and allow greater control over configuration and handling of HTTP requests.

Katana - Implementation of OWIN specification by Microsoft

.Net core replaced Katana

## ASP.NET

Server side technology for creating dynamic web content using HTML and C#. A View Engine in MVC is the component used to produce HTML that is sent back to the client browser. The preferred view engine for ASP.NET MVC is Razor. The Razor view engine basically allows you to write C# code inside HTML that is converted to plain HTML for the browser.

Template + Data = Generated Data

* .cshtml -> C# Razor 
* .vbhtml -> VB Razor
* .aspx, .ascx -> WebForms (Legacy)

For client side apps ASP.NET integrates with JavaScript frameworks like React or Angular, using preconfigured templates. Rendering a Mini SPA view can be done in isolation based on Html CSS and JS. The data for this SPA can be pulled through a web api using fully qualified URLs and Cross Origin Support configuration - needed for making AJAX calls across different domains. (For example: going from http://example.com to http://actual.com)

View Engine's like Razor can help in preventing XSS by HTML encoding the data i.e treating the script embedded in the data as raw text. This ensures that the browser does not run unwanted scripts and renders it as text only.

## Dotnet cli

### list .net sdk and runtime (s) installed

```sh
dotnet --info
```

### templates

```sh
# list installed templates
dotnet new -l

# install new template
dotnet new -i IdentityServer4.Templates

# create a new project (ASP.NET Core Empty) from an installed template
dotnet new web -n example-project
```

### solution

```sh
# add new solution
dotnet new sln -n Example

# add project to solution
dotnet sln add ./src/example-project/example-project.csproj
```
