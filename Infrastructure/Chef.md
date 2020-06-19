# Chef

Chef is a Ruby framework for automating, reusing and documenting server configuration. Server means the machine that runs your web server or database.

*Chef is like a unit test for your servers -  Ezra Zygmuntowicz*

## Terminology

* **Node** is a single server is called a node where the Chef client will run. This for example can run a web server, a database server or a background queue worker.
* **Chef Client** is the command line tool that performs the server (node) configuration. Typically you log in to the server (node), run the Chef Client on the command line on that node.
* **Chef Server** is a database backed web server that stores searchable information about nodes. It is REST based, can be self hosted or by *[Opscode](https://manage.opscode.com/)*, the creators of Chef.
* **Chef Solo** is the standalone version of Chef Client that doesn't rely on the server for configuration, it can point directly at Chef recipes.
* **Chef Recipe** is a single file of Ruby code containing a series of commands that are executed in order on a node. e.g. The Nginx SSL module for encrypting web content.
* **Resources** are built in commands that Chef builds around configuration file templates, restarting services and so on.
* **Cookbook** is a collection of recipes and the files associated with them.  
* **Role** groups some functionality together for reuse. A highly trafficked website might have 5 web servers and 2 database servers. These are roles: 'web', 'database'.
* **Run list** is a list of recipes and roles that defines what gets run on a node. Chef figures out the intersection of these and configures a node accordingly.
* **Attributes** are variables that are passed through Chef and used in recipes and templates. e.g. - the version number of Nginx to install.
* **Template** is an erb file similar to Rails view with placeholders for attributes. This will be used to create and update configuration files.
* **Notification** allows a change in a resource to trigger an update in another one. e.g. Nginx configuration file gets updated and the Nginx process is restarted to reload the Nginx server process.
