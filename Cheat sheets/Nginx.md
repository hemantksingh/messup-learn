# Architecture

Nginx employs an [event driven architecture](http://www.aosabook.org/en/nginx.html) with non blocking IO to distribute requests amongst worker processes as compared to Apache that spawns a process per connection.

* master process - read and evaluate configuration, and maintain worker processes
* worker processes - do actual processing of requests you generally run one worker process per CPU core

Get the list of all running nginx processes: `ps -ax | grep nginx`

## Configuration

By default the nginx configuration file is called `nginx.conf` and placed in the directory:

* `/usr/local/nginx/conf` 
* `/etc/nginx` 
* `/usr/local/etc/nginx`

Reloading configuration or an nginx upgrade doesn't require restarting nginx - just reload even if the binary gets updated

```sh
nginx -v 
nginx -s reload
```

### Configuration file structure

Nginx [processes requests](https://nginx.org/en/docs/http/request_processing.html) based on the following constructs:

* listen: IP and port
* server: define multiple virtual servers for host based routing
* default_server: used when can't match listen or server

## Logging

Default log location: `/var/log/nginx`

* access logs: `/var/log/nginx/access.log`
* error logs: `/var/log/nginx/error.log`









