create table sic(
    id int auto_increment,
    date timestamp not null default current_timestamp,
    channel varchar(255) not null,
    value varchar(255) not null,
    primary key(id)
);