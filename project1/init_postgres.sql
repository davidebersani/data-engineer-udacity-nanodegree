CREATE ROLE student WITH ENCRYPTED PASSWORD 'student';
ALTER ROLE student WITH LOGIN;
ALTER ROLE student CREATEDB;
CREATE DATABASE sparkifydb OWNER student;
