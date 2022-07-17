create table category(
    codename varchar(255) primary key,
    name varchar(255),
    aliases text
);

create table expenses(
    id integer primary key,
    amount float,
    created_time datetime,
    category_codename varchar(255),
    raw_text text,
    FOREIGN KEY(category_codename) REFERENCES category(codename)
);

insert into category (codename, name, aliases)
values
    ("grocery", "food", "еда, продукты, магазин, супермаркет, food, products"),
    ("other", "other", "прочее, другое");