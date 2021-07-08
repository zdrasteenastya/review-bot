create_users = """
create table users
(
    user_id       int,
    username      varchar(50),
    chat_id       int,
    muted         boolean default false,
    constraint users_pk primary key(username, user_id, chat_id)
);
"""

create_schedule = """
create table schedule
(
    rw_date       varchar,
    username      varchar(50),
    chat_id       int,
    constraint reviewrs_pk
        primary key (rw_date, username, chat_id)

);
"""
