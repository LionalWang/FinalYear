drop table if exists user;
create table user (
  id BIGINT  primary key AUTO_INCREMENT ,
  username TEXT  not null,
  password TEXT  not null