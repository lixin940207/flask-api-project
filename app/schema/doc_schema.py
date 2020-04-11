from flask_marshmallow import Schema


class DocSchema(Schema):  # type: ignore
    class Meta:
        fields = (
            'doc_id',
            'doc_unique_name',
            'doc_raw_name',
            'rich_content_path',
            'status',
            'convert_state'
        )
