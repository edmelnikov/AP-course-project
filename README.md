# AP-course-project
App Development course project.

It is a website representing an online store, made using Django Framework. The database used is PostgreSQL. 

PSQL setup:

=> CREATE ROLE store_db_admin PASSWORD 'store_db_admin' LOGIN;

=> CREATE DATABASE store_db OWNER store_db_admin;


$ cd siteroot
 
$ python manage.py migrate
