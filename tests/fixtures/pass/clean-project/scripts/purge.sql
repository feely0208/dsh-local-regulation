-- 三个月前的会员事件数据不再保留；审批与销毁记录见 docs/数据安全管理制度.md
DELETE FROM member_event WHERE created_at < DATE('now', '-3 months');
