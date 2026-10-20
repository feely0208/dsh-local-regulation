-- 三个月前的会员事件数据不再保留
DELETE FROM member_event WHERE created_at < DATE('now', '-3 months');
