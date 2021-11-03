#!/bin/sh
echo ##
echo ## setup_mysql
echo ##

# check if mysql data directory is nuked
# if so, install the db
echo "Checking /var/lib/mysql folder"
if [ ! -f /var/lib/mysql/ibdata1 ]; then 
    echo "Installing db"
    mariadb-install-db --user=mysql --ldata=/var/lib/mysql > /dev/null
    echo "Installed"
fi;

# from mysql official docker repo
if [ -z "$MYSQL_ROOT_PASSWORD" -a -z "$MYSQL_RANDOM_ROOT_PASSWORD" ]; then
			echo >&2 'error: database is uninitialized and password option is not specified '
			echo >&2 '  You need to specify one of MYSQL_ROOT_PASSWORD, MYSQL_RANDOM_ROOT_PASSWORD'
			exit 1
fi

# random password
if [ ! -z "$MYSQL_RANDOM_ROOT_PASSWORD" ]; then
    echo "Using random password"
    MYSQL_ROOT_PASSWORD="$(pwgen -1 32)"
    echo "GENERATED ROOT PASSWORD: $MYSQL_ROOT_PASSWORD"
    echo "Done"
fi

tfile=`mktemp`
if [ ! -f "$tfile" ]; then
    return 1
fi

cat << EOF > $tfile
    USE mysql;
    GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY "$MYSQL_ROOT_PASSWORD" WITH GRANT OPTION;
    GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost' WITH GRANT OPTION;
    UPDATE user SET password=PASSWORD("") WHERE user='root' AND host='localhost';
    GRANT ALL PRIVILEGES ON *.* TO 'pihomedbadmin'@'%' IDENTIFIED BY "pihome2018" WITH GRANT OPTION;
    GRANT ALL PRIVILEGES ON *.* TO 'pihomedbadmin'@'localhost' WITH GRANT OPTION;
    GRANT ALL PRIVILEGES ON *.* TO 'piphpmyadmin'@'%' IDENTIFIED BY "pihome2018" WITH GRANT OPTION;
    GRANT ALL PRIVILEGES ON *.* TO 'piphpmyadmin'@'localhost' WITH GRANT OPTION;
    FLUSH PRIVILEGES;
EOF

echo "Querying user"
/usr/bin/mysqld --user=root --bootstrap --verbose=0 < $tfile
rm -f $tfile
echo "Done query"

# start mysql
# nohup mysqld_safe --skip-grant-tables --bind-address 0.0.0.0 --user mysql > /dev/null 2>&1 &
#echo "Starting mariadb database"
#/usr/bin/mysqld --user=root --bind-address=0.0.0.0 &

#
# create pihome users/db etc
#
#cd /var/www/pihome/MySQL_Database
#php setup_db.php
