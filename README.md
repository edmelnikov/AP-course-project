# AP-course-project
App Development course project

PSQL setup:

=> CREATE ROLE store_db_admin PASSWORD 'store_db_admin' LOGIN;

=> CREATE DATABASE store_db OWNER store_db_admin;


$ cd siteroot
 
$ python manage.py migrate
