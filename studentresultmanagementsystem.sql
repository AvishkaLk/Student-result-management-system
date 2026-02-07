create database edutech;

use edutech;

create table students
(
student_id int not null primary key auto_increment,
name varchar(255) not null,
total_marks float,
grade char
);

create table marks
(
student_id int,
subject_name varchar(50),
marks int check (marks between 0 and 100),
primary key (student_id, subject_name),
foreign key (student_id) references students (student_id)
);