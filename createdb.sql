PRAGMA encoding = "UTF-8";

CREATE TABLE budget(
    codename varchar(255) primary key,
    daily_limit integer);

CREATE TABLE category(
    codename varchar(255) primary key,
    name varchar(255),
    is_base_expense boolean,
    aliases text);

CREATE TABLE expense(
    id integer primary key,
    amount integer,
    created datetime,
    category_codename integer,
    raw_text text,
    FOREIGN KEY(category_codename) REFERENCES category(codename));

INSERT INTO category (codename, name, is_base_expense, aliases)
VALUES
    ("products", "продукты", true, "еда"),
    ("coffee", "кофе", true, ""),
    ("flat", "квартира",  true,"аренда"),
    ("entertainment", "развлечения", true,"кино, хоккей"),
    ("dinner", "обед", true, "столовая, ланч, столовка, обед"),
    ("cafe", "кафе", true, "ресторан, рест, мак, макдональдс, макдак, kfc"),
    ("transport", "общ. транспорт", false, "метро, автобус, metro"),
    ("taxi", "такси", false, "яндекс такси, yandex taxi"),
    ("phone", "телефон", false, "мтс, связь"),
    ("books", "книги", false, "литература, литра, лит-ра"),
    ("internet", "интернет", false, "инет, inet"),
    ("subscriptions", "подписки", false, "подписка"),
    ("other", "прочее", false, "");

INSERT INTO budget(codename, daily_limit) VALUES ('base', 50);
