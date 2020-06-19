# SQL Server

Help

```sh
sqlcmd -?

```

Test Setup using windows auth (trusted connection)

```powershell

sqlcmd -S <server> -E
1>select @@Version
2>go

```

Test setup using db user

```powershell

sqlcmd -S <server> -U <dbuser> -P <dbpass>

```


List databases

```powershell

sqlcmd
1>select name from master.dbo.sysdatabases
2>go

```

or

```powershell

sqlcmd
1>exec sp_databases
2>go

```