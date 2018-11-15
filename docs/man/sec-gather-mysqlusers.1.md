% SEC-GATHER-MYSQLUSERS(1)
% Ferry Boender
% May 2017

# NAME

sec-gather-mysqlusers – Output MySQL users and their grants

# SYNOPSIS

 **sec-gather-mysqlusers** [**-h**] [**--version**] [**--debug**] [**--no-conn-error**]

# DESCRIPTION

**sec-gather-mysqlusers** connects to a MySQL database and outputs information
about MySQL users, their connect and database privileges.It uses a `~/.my.cnf`
to connect.


# OPTIONS

**-h**, **--help**
:   Display this help message and exit

**--version**
:   show program's version number and exit

**--debug**
:   Show debug info

**--no-conn-error**
:   If cannot connect to mysql, return empty response

# CONNECTING

**sec-gather-mysqlusers** connects to the database using a MySQL client
configuration file. This file should be present in your homedirectory as
`~/.my.cnf` and look like this:

    [mysql]
    user=root
    password=s3cre3t

Make sure the file isn't readable for other users.

# EXAMPLES


    $ sec-gather-mysqlusers
    {
        "mysqlusers": {
            "debian-sys-maint": {
                "dbs": {}, 
                "from_hosts": [
                    "localhost"
                ], 
                "rights_all_dbs": "Read/Write"
            }, 
            "mysql.sys": {
                "dbs": {
                    "sys": ""
                }, 
                "from_hosts": [
                    "localhost"
                ], 
                "rights_all_dbs": ""
            }, 
            "fboender": {
                "dbs": {}, 
                "from_hosts": [
                    "ANY"
                ], 
                "rights_all_dbs": "Read/Write"
            }
        }
    }

# COPYRIGHT

Copyright 2017, Ferry Boender.

Licensed under the MIT license. For more information, see the LICENSE file.
