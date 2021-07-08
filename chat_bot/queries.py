insert_schedule = """
    insert into schedule (rw_date, username, chat_id) 
    values {} 
    on conflict
    do nothing;
"""

truncate_schedule = """
    delete from schedule;
"""

get_reviewers = """
select distinct schedule.username, users.user_id
from schedule
join users
on schedule.username = users.username
where rw_date=\'{rw_date}\' and schedule.chat_id={chat_id};
"""

insert_user = """
    insert into users (user_id, username, chat_id) 
    values ({user_id}, \'{username}\', {chat_id}) 
    on conflict (username, user_id, chat_id)
    do update set muted = false;
"""

select_reviewers = """
    select username
    from users
    where chat_id = {chat_id} and muted = false;
"""

update_user = """
    update users
    set muted = true
    where user_id = {user_id};
"""