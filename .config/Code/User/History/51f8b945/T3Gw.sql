create table sic(
    id int auto_increment,
    date timestamp not null,
    channel varchar(255) not null,
    value int not null,
    primary key(id)
);