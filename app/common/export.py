import os
import typing
import requests
from app.common.fileset import FileSet, DEFAULTS
from app.config.config import get_config_from_app as _get
from app.common.log import logger


class ExportBase(object):
    """
    导出文件基类
    """

    def __init__(self, folder: str = 'upload', unique_name: str = '', file_name: str = None) -> None:
        self.unique_name = unique_name
        self.file_name = file_name
        self.fileset = FileSet(folder, DEFAULTS)

    def export(self, replace_ext=None, suffix=None) -> typing.Dict:
        export_file_abspath = self.fileset.get_abspath(self.unique_name, replace_ext=replace_ext, suffix=suffix)
        export_file_path = self.fileset.get_relative_path(self.unique_name, replace_ext=replace_ext, suffix=suffix)

        if not self.check_exist(export_file_abspath):
            raise Exception("文件不存在，请检查操作是否正确")

        return {
            "file_name": self.file_name if self.file_name else self.unique_name,
            "path": export_file_path
        }

    @staticmethod
    def check_exist(file_path: str = None) -> bool:
        return os.path.exists(file_path)


class PDFAnnotationExport(ExportBase):
    """
    带标注pdf导出
    """
    def export_with_annotation(self, labels: typing.List[typing.Dict]) -> typing.Dict:
        """
        :param labels: 标注数据
        支持格式为[{
            "index": 12                     # 全文下标位置,
            "word": "中国"                   # 正文内容
            "color": "#ccc"                 # 颜色，必须是#开头
            "annotation": "注释名称"         # tooltip展示内容
        }]
        :return:
        {
            "file_name": '',
            "path": ''
        }
        """
        annotation_fileset = FileSet(folder='')

        for label in labels:
            label["color"] = self.hex_to_int(label["color"])

        data = {
            "input_path": annotation_fileset.get_relative_path(self.unique_name, replace_ext='pdf'),
            "output_path": annotation_fileset.get_relative_path(self.unique_name, replace_ext='pdf', suffix='_print'),
            "pdf_json_path": annotation_fileset.get_relative_path(self.unique_name, replace_ext='json'),
            "content_path": annotation_fileset.get_relative_path(self.unique_name, replace_ext='txt'),
            "labels": labels
        }

        r = requests.post(_get('PDF_PRINTER'), json=data, timeout=600)

        if r.status_code != 200:
            logger.error(f'label export request failed, response is {r.text}')
            raise Exception("导出PDF服务出现异常，请联系运维人员进行解决")

        return self.export(replace_ext='pdf', suffix='_print')

    @staticmethod
    def hex_to_int(rgb):
        """十六进制颜色码转换成RGB颜色值 #3cf20f =>60,242,15
        """
        return [int(rgb[1:3], 16), int(rgb[3:5], 16), int(rgb[5:], 16)]
