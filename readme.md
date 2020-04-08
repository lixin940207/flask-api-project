
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

### 生成User-Info：
```python
import base64
import json
a = json.dumps({"app_id":1,"id":1,"username":"james","roles":[{"name": "管理员"}]})
b = a.encode("utf-8")
c = base64.b64encode(b)
print(c.decode("utf-8"))
```
Postman Header中增加:
`User-Info`: `eyJhcHBfaWQiOiAxLCAiaWQiOiAxLCAidXNlcm5hbWUiOiAiamFtZXMiLCAicm9sZXMiOiBbeyJuYW1lIjogIlx1N2JhMVx1NzQwNlx1NTQ1OCJ9XX0=`

管理员：
`{"app_id":1,"id":1,"username":"james","roles":[{"name": "管理员"}],"groups":[{"id": 1}]}`
`eyJhcHBfaWQiOiAxLCAiaWQiOiAxLCAidXNlcm5hbWUiOiAiamFtZXMiLCAicm9sZXMiOiBbeyJuYW1lIjogIlx1N2JhMVx1NzQwNlx1NTQ1OCJ9XSwgImdyb3VwcyI6IFt7ImlkIjogMX1dfQ==`

审核员：
`{"app_id": 1, "id": 2, "username": "reviewer", "roles": [{"name": "审核员"}],"groups":[{"id": 1}]}`
`eyJhcHBfaWQiOiAxLCAiaWQiOiAyLCAidXNlcm5hbWUiOiAicmV2aWV3ZXIiLCAicm9sZXMiOiBbeyJuYW1lIjogIlx1NWJhMVx1NjgzOFx1NTQ1OCJ9XSwgImdyb3VwcyI6IFt7ImlkIjogMX1dfQ==`

标注员：
`{"app_id": 1, "id": 3, "username": "annotator", "roles": [{"name": "标注员"}],"groups":[{"id": 1}]}`
`eyJhcHBfaWQiOiAxLCAiaWQiOiAzLCAidXNlcm5hbWUiOiAiYW5ub3RhdG9yIiwgInJvbGVzIjogW3sibmFtZSI6ICJcdTY4MDdcdTZjZThcdTU0NTgifV0sICJncm91cHMiOiBbeyJpZCI6IDF9XX0=`

超级管理员：
`{"app_id":1,"id":99,"username":"superadmin","roles":[{"name": "超级管理员"}],"groups":[{"id": 1}]}`
`eyJhcHBfaWQiOiAxLCAiaWQiOiA5OSwgInVzZXJuYW1lIjogInN1cGVyYWRtaW4iLCAicm9sZXMiOiBbeyJuYW1lIjogIlx1OGQ4NVx1N2VhN1x1N2JhMVx1NzQwNlx1NTQ1OCJ9XSwgImdyb3VwcyI6IFt7ImlkIjogMX1dfQ==`


##### TODO List:
1. 所有上传的文档都要用chardet检测编码模式
2. doc_type.is_favorite要改成每个人不同，新增user_doctype_favorite表