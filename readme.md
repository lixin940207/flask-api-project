
### Migration

- 启动本地的mysql，推荐brew install
- create数据库：szse
- cd app && flask db init
- flask db migrate
- flask db upgrade


### 如果出现mysql插入不了中文：
```sql
ALTER TABLE szse.doc_type MODIFY COLUMN doc_type_desc text
    CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL;
```
