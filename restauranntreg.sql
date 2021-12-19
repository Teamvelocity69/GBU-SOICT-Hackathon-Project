create database restaurants;

use restaurants;

create table r1(
orderno varchar(10) primary key not null,
name varchar(20),
phonenum varchar(10),
date date,
time varchar(7),
paymode varchar(20),
mode varchar(20),
amount varchar(7));

