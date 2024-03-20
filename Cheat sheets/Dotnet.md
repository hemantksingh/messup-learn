# .NET

## OWIN (Open Web Interface for .Net)

OWIN provided a standard interface for separation between Webapp framework (like ASP.Net) and Webserver (like IIS). It allowed ASP.Net apps to be self hosted running in a console process and to be hosted on linux running mono. Self hosted apps do not have to go through IIS pipelines and allow greater control over configuration and handling of HTTP requests.

Katana - Implementation of OWIN specification by Microsoft

.Net core replaced Katana

## ASP.NET

Server side rendoring (SSR) technology for creating dynamic web content using HTML and C#. There are a [number of options](https://learn.microsoft.com/en-us/aspnet/core/tutorials/choose-web-ui?view=aspnetcore-8.0) for creating web apps using ASP.NET Core but these options can be used together as well

* Blazor
* Razor Pages
* MVC
* SPA with frontend [JS frameworks](../Tools/Javascript%20Frameworks.md) like React, Angular, Vue

The template engine (or View Engine in MVC) is used to generate the HTML from data. In SSR the HTML is generated on the server and sent back to the client browser. The preferred template engine for ASP.NET MVC is Razor. It allows you to write C# code inside HTML that is converted to plain HTML for the browser.

Template + Data = HTML
* .cshtml -> C# Razor 
* .vbhtml -> VB Razor
* .aspx, .ascx -> WebForms (Legacy)

Template engines should be configured to enforce strict syntax rules to prevent arbitrary code execution or injection. They should provide 
* contextual escaping - treat input as raw data
* encoding - convert potentially dangerous characters e.g. script tags into their HTML entity equivalents, ensuring that user-supplied data is rendered as inert text rather than executable code

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
# framework can be "net6.0", "net7.0", "net8.0", if ommitted latest is used be default
cd src/example
dotnet new web -n example -f net6.0
```

### solution

```sh
# add new solution
dotnet new sln -n Example

# add project to solution
dotnet sln add ./src/example/example.csproj
```

### packages
```sh
# navigate to the project dir
cd tests/example.tests
# add nuget package
dotnet add package Microsoft.AspNetCore.TestHost -v 6.0.28

# list installed packages
dotnet list package

Project 'example.tests' has the following package references
   [net6.0]: 
   Top-level Package                    Requested   Resolved
   > coverlet.collector                 6.0.0       6.0.0   
   > Microsoft.AspNetCore.TestHost      6.0.28      6.0.28  
   > Microsoft.NET.Test.Sdk             17.6.0      17.6.0  
   > xunit                              2.4.2       2.4.2   
   > xunit.runner.visualstudio          2.4.5       2.4.5  
```
