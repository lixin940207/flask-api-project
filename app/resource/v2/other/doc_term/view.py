import json
import typing
from flask_restful import Resource, abort

from app.common.extension import session
from app.common.common import Common
from app.common.patch import parse, fields
from app.common.filters import CurrentUserMixin
from app.common.redis import r
from app.service.doc_term_service import DocTermService


class GetDocTermListResource(Resource, CurrentUserMixin):
    @parse({
        "offset": fields.Integer(missing=0),
        "limit": fields.Integer(missing=10),
        "exclude_terms_ids": fields.List(fields.Integer(), missing=[]),
    })
    def get(self: Resource, args: typing.Dict) -> typing.Tuple[typing.Dict, int]:
        """
        获取所有条款，分页，可选排除条件exclude_terms_ids
        """
        nlp_task_id = Common().get_nlp_task_id_by_route()
        args.update({
            'nlp_task_id': nlp_task_id
        })
        result, count = DocTermService().get_doc_term_list(args)
        return {
                   "message": "请求成功",
                   "result": result,
                   "count": count,
               }, 200


class DocTermListResource(Resource, CurrentUserMixin):
    @parse({
        "doc_term_ids": fields.List(fields.Integer(), missing=[]),
        "offset": fields.Integer(missing=0),
        "limit": fields.Integer(missing=10),
    })
    def get(self, args: typing.Dict, doc_type_id: int) -> typing.Tuple[typing.Dict, int]:
        """
        获取所有条款，不分页
        """
        if args.get('doc_term_ids'):
            result, count = DocTermService().get_doc_term_by_doctype(doc_type_id, args['offset'], args['limit'])
        else:
            result, count = DocTermService().get_doc_term_by_doctype(doc_type_id, args['offset'], args['limit'], doc_term_ids=args.get('doc_term_ids'))
        return {
                   "message": "请求成功",
                   "result": result,
                   "count": count,
               }, 200

    @parse({
        "doc_term_name": fields.String(required=True),
        "doc_term_color": fields.String(required=True),
        "doc_term_index": fields.Integer(required=True),
        "doc_term_desc": fields.String(default=""),
        "doc_term_data_type": fields.String(required=True),
    })
    def post(self, args: typing.Dict, doc_type_id: int) -> typing.Tuple[typing.Dict, int]:
        """
        创建一个条款
        """
        result = DocTermService().create_doc_term(args, doc_type_id)
        return {
                   "message": "创建成功",
                   "result": result,
               }, 201


class ClassifyDocTermListResource(Resource, CurrentUserMixin):
    @parse({
        "doc_term_ids": fields.List(fields.Integer(), missing=[]),
        "offset": fields.Integer(missing=0),
        "limit": fields.Integer(missing=10),
    })
    def get(self, args: typing.Dict, doc_type_id: int) -> typing.Tuple[typing.Dict, int]:
        """
        获取所有条款，不分页
        """
        if args.get('doc_term_ids'):
            result, count = DocTermService().get_doc_term_by_doctype(doc_type_id, args['offset'], args['limit'])
        else:
            result, count = DocTermService().get_doc_term_by_doctype(doc_type_id, args['offset'], args['limit'], doc_term_ids=args.get('doc_term_ids'))
        return {
                   "message": "请求成功",
                   "result": result,
                   "count": count,
               }, 200

    @parse({
        "doc_term_name": fields.String(required=True),
        "doc_term_color": fields.String(required=True),
        "doc_term_index": fields.Integer(required=True),
        "doc_term_desc": fields.String(default=""),
        "doc_term_data_type": fields.String(required=True),
    })
    def post(self, args: typing.Dict, doc_type_id: int) -> typing.Tuple[typing.Dict, int]:
        """
        创建一个条款
        """
        doc_rule_list = args.pop('doc_rule_list')
        result = DocTermService().create_classify_doc_term(args, doc_type_id, doc_rule_list)
        DocTermService().update_rule_to_redis(doc_type_id)
        return {
                   "message": "创建成功",
                   "result": result,
               }, 201


class ListWordsegDocTermResource(Resource, CurrentUserMixin):
    def get(self: Resource) -> typing.Tuple[typing.Dict, int]:
        """
        获取所有条款，分页，可选排除条件exclude_terms_ids
        """
        result = Common().get_wordseg_doc_terms()
        return {
                   "message": "请求成功",
                   "result": result
               }, 200


class EntityDocTermItemResource(Resource):
    @parse({
        "doc_term_name": fields.String(),
        "doc_term_color": fields.String(),
        "doc_term_index": fields.Integer(allow_none=True, default=1),
        "doc_term_desc": fields.String(allow_none=True),
        "doc_term_data_type": fields.String(),
    })
    def patch(self: Resource, args: typing.Dict, doc_type_id: int, doc_term_id: int) -> typing.Tuple[
        typing.Dict, int]:
        """
        修改一个条款
        """
        result = DocTermService().update_doc_term(doc_term_id, args)
        return {
                   "message": "更新成功",
                   "result": result,
               }, 201

    def delete(self: Resource, doc_type_id: int, doc_term_id: int) -> typing.Tuple[typing.Dict, int]:
        """
        删除一个条款
        """
        if DocTermService().check_term_in_relation(doc_term_id):
            abort(400, message="该条款仍有关联关系，请确保条款没有关联关系后再做清除")

        DocTermService().remove_doc_term(doc_term_id)
        session.commit()
        return {
                   "message": "删除成功",
               }, 204


class WordsegDocLexiconListResource(Resource):
    @parse({
        "offset": fields.Integer(missing=0),
        "limit": fields.Integer(missing=10),
    })
    def get(self, args, doc_type_id):
        """
        规则列表
        """
        result, count = DocTermService().get_wordseg_lexicon(doc_type_id, args.get("offset"), args.get("limit"))
        return {
                   "message": "请求成功",
                   "result": result,
                   "count": count,
               }, 200

    @parse({
        "seg_type": fields.String(required=True),
        "word": fields.String(required=True),
        "state": fields.Integer(required=True)
    })
    def post(self, args, doc_type_id):
        args.update({"doc_type_id": doc_type_id})
        args.update({"is_active": args.pop("state")})
        result = DocTermService().create_wordseg_lexicon(args)

        return {
                   "message": "创建成功",
                   "result": result,
               }, 201


class WordsegDocLexiconItemResource(Resource):
    def get(self, doc_type_id, doc_lexicon_id):
        result = DocTermService().get_wordseg_lexicon_item(doc_lexicon_id)
        return {
                   "message": "请求成功",
                   "result": result,
               }, 200

    @parse({
        "seg_type": fields.String(required=True),
        "word": fields.String(required=True),
        "state": fields.Integer(required=True)
    })
    def put(self, args, doc_type_id, doc_lexicon_id):
        args.update({"is_active": args.pop("state")})
        result = DocTermService().update_wordseg_lexicon(doc_lexicon_id, args)
        return {
                   "message": "更新成功",
                   "result": result,
               }, 200

    def delete(self, doc_type_id, doc_lexicon_id):
        DocTermService().delete_wordseg_lexicon_by_id(doc_lexicon_id)
        return {
                   "message": "删除成功",
               }, 204


class ClassifyDocRuleListResource(Resource):
    @parse({
        "offset": fields.Integer(missing=0),
        "limit": fields.Integer(missing=10),
        "timestamp": fields.String(),
    })
    def get(self, args, doc_type_id):
        """
        规则列表
        """
        redis_key = f'classify:rule:{doc_type_id}'
        if args.get("timestamp"):
            try:
                result = json.loads(r.get(redis_key))
                if result['timestamp'] == args["timestamp"]:
                    result.update(update=False)
                    return result
            except Exception:
                pass
        # TODO 查询优化
        result, timestamp, count = DocTermService().get_classify_doc_rule(doc_type_id, args.get("offset"),
                                                                          args.get("limit"))
        data = {
            "message": "请求成功",
            "result": result,
            "timestamp": timestamp,
            "update": True,
            "count": count,
        }
        if args.get("timestamp"):
            r.set(redis_key, json.dumps(data), ex=24 * 60 * 60)
        return data, 200

    @parse({
        "doc_term_id": fields.Integer(required=True),
        "rule_type": fields.String(required=True),
        "rule_content": fields.Dict(required=True)
    })
    def post(self, args, doc_type_id):
        try:
            result = DocTermService().create_new_rule(doc_type_id, args)
            DocTermService().update_rule_to_redis(doc_type_id)
            r.delete(f'classify:rule:{doc_type_id}')
            return {
                       "message": "创建成功",
                       "result": result,
                   }, 201
        except ValueError as e:
            abort(400, message=str(e))


class ClassifyDocRuleItemResource(Resource):
    def get(self, doc_type_id, doc_rule_id):
        result = DocTermService().get_classify_rule(doc_rule_id)
        return {
                   "message": "请求成功",
                   "result": result,
               }, 200

    @parse({
        "rule_content": fields.Dict(),
        "state": fields.Integer()
    })
    def patch(self, args, doc_type_id, doc_rule_id):
        result = DocTermService().update_classify_rule(args, doc_rule_id)
        DocTermService().update_rule_to_redis(doc_type_id)
        r.delete(f'classify:rule:{doc_type_id}')
        return {
                   "message": "更新成功",
                   "result": result,
               }, 200

    def delete(self, doc_type_id, doc_rule_id):
        DocTermService().delete_doc_rule(doc_rule_id)
        DocTermService().update_rule_to_redis(doc_type_id)
        r.delete(f'classify:rule:{doc_type_id}')

        return {
                   "message": "删除成功",
               }, 204
