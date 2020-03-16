
### Migration + Create Seeds

- 启动本地的mysql，推荐brew install
- create数据库：szse
- cd app && flask db init
- flask db migrate
- flask db upgrade
- flask seed run