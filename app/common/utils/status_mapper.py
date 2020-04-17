# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/4/8-2:25 下午
from app.common.common import StatusEnum


def status_str2int_mapper():
    # 后端返回结果转换，因为失败时后端目前还返回failed，但是新的statusenum全部用fail
    return {
        "success": int(StatusEnum.success),
        "failed": int(StatusEnum.fail),
        "fail": int(StatusEnum.fail),
        "training": int(StatusEnum.training),
        "evaluating": int(StatusEnum.evaluating),
        "online": int(StatusEnum.online),
        "processing": int(StatusEnum.processing),
        "unaudit": int(StatusEnum.reviewing),
        "audited": int(StatusEnum.approved),
        "unlabel": int(StatusEnum.unlabel),
        "labeled": int(StatusEnum.labeled),
        "ready": int(StatusEnum.available)
    }


def convert_explicit_status(entity_list, status_column_name):
    """table int status to string status"""
    is_list = True
    if type(entity_list) != list:
        entity_list = [entity_list]
        is_list = False
    for i in entity_list:
        setattr(i, status_column_name, StatusEnum(getattr(i, status_column_name)).name)
    if not is_list:
        return entity_list[0]
    return entity_list
