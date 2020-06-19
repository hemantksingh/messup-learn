# Nuget

* Nuget cli reference: https://docs.microsoft.com/en-us/nuget/tools/nuget-exe-cli-reference 
* The NuGet configuration file: If not specified, `%AppData%\NuGet\NuGet.config` is used as configuration file.
* In Visual studio [Nuget is an add-in](https://stackoverflow.com/questions/28170913/where-does-visual-studio-keep-its-own-copy-of-nuget-exe), just DLLs no exe

## Nuget commands

* help

```sh
nuget help config
# or
nuget config -help

nuget help sources
# or
nuget sources -help
```

* default config file

```sh
cat ~/AppData/Roaming/NuGet/nuget.config
```

* update installed package 

```sh
# Ensure the package has been restored before updating
nuget update <sln-name>.sln -Id <package-name>
```

* add source

```sh
nuget source add -Name "Example Nuget" -Source "https://nuget.example.com" -username "<username>" -password "<password>"
```

* update source

```sh
nuget source update -Name "Example Nuget" -username "<username>" -password "<password>"
```


* remove source

```sh
nuget source remove -Name "Example Nuget"
```