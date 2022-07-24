create table categories (
    codename varchar(255) primary key,
    name varchar(255),
    aliases text
);

create table expenses(
    id integer primary key,
    amount float,
    created_time timestamp,
    category_codename varchar(255),
    raw_text text,
    FOREIGN KEY(category_codename) REFERENCES categories(codename)
);

insert into categories (codename, name, aliases)
VALUES ('grocery', 'food', 'еда, продукты, магазин, супермаркет, food, products');

insert into categories (codename, name, aliases)
values ('other', 'other', 'прочее, другое');