drop table if exists student;
create table student (
  id integer primary key autoincrement,
  name string not null,
  age string not null
);