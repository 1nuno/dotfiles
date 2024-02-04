create table sic(
    id int auto_increment,
    date timestamp not null ,
    channel varchar(255) not null default urrent_timestamp,
    value int not null,
    primary key(id)
);