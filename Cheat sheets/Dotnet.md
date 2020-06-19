# .NET

## OWIN (Open Web Interface for .Net)

OWIN provided a standard interface for separation between Webapp framework (like ASP.Net) and Webserver (like IIS). It allowed ASP.Net apps to be self hosted running in a console process and to be hosted on linux running mono. Self hosted apps do not have to go through IIS pipelines and allow greater control over configuration and handling of HTTP requests.

Katana - Implementation of OWIN specification by Microsoft

.Net core replaced Katana

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
```

### solution

```sh
# add new solution
dotnet new sln -n Example

# add project to solution
dotnet sln add ./src/example-project/example-project.csproj
```


