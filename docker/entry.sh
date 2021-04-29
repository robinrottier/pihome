#!/bin/sh

# start apache
echo "Starting httpd"
httpd
echo "Done httpd"

# start mysql
# nohup mysqld_safe --skip-grant-tables --bind-address 0.0.0.0 --user mysql > /dev/null 2>&1 &
echo "Starting mariadb database"
/usr/bin/mysqld --user=root --bind-address=0.0.0.0
echo "Done mariadb database"
