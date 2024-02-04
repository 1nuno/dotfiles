create table sic(
    id int auto_increment,
    date timestamp not null,
    client varchar(255) not null,
    value int not null,
    primary key(id)
);