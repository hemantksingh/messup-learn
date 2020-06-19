# Troubleshooting

```sh
dotnet --info

dotnet --list-runtimes
```

## Event viewer logs

*  `Win+R` -> `eventvwr`
* `Windows Logs` -> `Application` for application logs e.g. .net framework runtime errors
* `Windows Logs` -> `System` for IIS logs e.g.

## List services

* `Win+R` -> `services.msc`

### HTTP Error 503. The service is unavailable, App Pool Stopped

* Most probably the windows account under which the app pool is running has been disabled or expired. Reset the app pool with the new credentials. 

* You may also have to reset the login for sql server services running under that account on the sql server

https://stackoverflow.com/questions/19652709/http-error-503-the-service-is-unavailable-app-pool-stops-on-accessing-website

### HTTP Error 502.5 - Process Failure in ASP.NET Core 2.1 application

Try to run the application dll by navigating to the installation directory: `dotnet application.dll`

https://stackoverflow.com/questions/51304726/http-error-502-5-process-failure-in-asp-net-core-2-1-application

### Permission issues

* Service can also fail to start if IIS does not have the required permissions to the installation files. Add `IIS_IUSRS` users to the installation dir to fix this.