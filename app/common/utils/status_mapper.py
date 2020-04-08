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
        "online": int(StatusEnum.online)
    }
