create schema tg_bot;


create table tg_bot.users
(
    user_id       int primary key,
    username      varchar(50),
    chat_id       int,
    muted         boolean default false,
    constraint users_uk
        unique (username, user_id, chat_id)
);


create table tg_bot.schedule
(
    rw_date       varchar,
    username      varchar(50),
    chat_id       int,
    constraint reviewrs_pk
        primary key (rw_date, username, chat_id)

);
