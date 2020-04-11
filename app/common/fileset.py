import typing
import os
import csv

from flask_restful import abort
from marshmallow.exceptions import ValidationError
from app.config.config import BASE_PATH
from app.common.utils.name import get_ext, generate_unique_name
from app.common.utils.dir import make_dirs
from app.common.utils.time import get_now_with_format

DEFAULTS = ()  # allow any
TEXT = ('txt',)
EXECUTABLES = ('so', 'exe', 'dll')
SCRIPTS = ('js', 'php', 'pl', 'py', 'rb', 'sh')
AUDIO = ('wav', 'mp3', 'aac', 'ogg', 'oga', 'flac')
ARCHIVES = ('gz', 'bz2', 'zip', 'tar', 'tgz', 'txz', '7z')
IMAGES = ('jpg', 'jpe', 'jpeg', 'png', 'gif', 'svg', 'bmp')
DATA = ('csv', 'ini', 'json', 'plist', 'xml', 'yaml', 'yml')
DOCUMENTS = ('rtf', 'odf', 'ods', 'gnumeric', 'abw', 'doc', 'docx', 'xls', 'xlsx', 'pdf')


class FileSet(object):
    def __init__(self, folder: str = 'tmp', exts: typing.Tuple = DEFAULTS) -> None:
        self.folder = folder
        self.exts = exts
        self.path = os.path.join(BASE_PATH, folder)
        make_dirs(self.path)

    def check_ext(self, ext: str) -> bool:
        return not self.exts or ext.lower() in self.exts

    def get_abspath(self, filename: str, replace_ext: str = None, suffix: str = None) -> str:
        """
        获取文件的绝对路径
        :param filename: 文件名
        :param replace_ext: 替换文件类型后缀
        :param suffix: 文件名后缀，对文件名的补充，在.分隔内容前半段
        :return:
        """
        filename_split = filename.rsplit(".", 1)

        if suffix:
            filename_split[0] = f'{filename_split[0]}{suffix}'

        if not replace_ext:
            return os.path.join(self.path, '.'.join(filename_split))

        return os.path.join(self.path, f'{filename_split[0]}.{replace_ext}')

    def get_relative_path(self, filename: str, replace_ext: str = None, suffix: str = None) -> str:
        """
        获取文件的相对路径
        :param filename: 文件名
        :param replace_ext: 替换文件类型后缀
        :param suffix: 文件名后缀，对文件名的补充，在.分隔内容前半段
        :return:
        """
        filename_split = filename.rsplit(".", 1)

        if suffix:
            filename_split[0] = f'{filename_split[0]}{suffix}'

        if not replace_ext:
            return os.path.join(self.folder, '.'.join(filename_split))

        return os.path.join(self.folder, f'{filename_split[0]}.{replace_ext}')

    def save_file(self, filename: str, filebin: bytearray or str, is_ocr=False) -> typing.Tuple:
        ext = get_ext(filename)
        if not self.check_ext(ext):
            raise ValidationError({
                filename: [
                    f'{ext} is illegal suffix'
                ]
            })

        unique_name = generate_unique_name(ext)
        if is_ocr:
            path_split = os.path.splitext(unique_name)
            unique_name = "{}_ocr{}".format(path_split[0], path_split[1])
        unique_path = self.get_abspath(unique_name)

        with open(unique_path, 'wb') as f:
            if isinstance(filebin, str):
                f.write(filebin.encode("utf-8"))
            else:
                f.write(filebin)

        # 很多时候都需要拼接相对路由，例如：/file/upload/ocr/xxxx.jpg
        return unique_name, self.get_relative_path(unique_name)

    def export_to_csv(self, results: list, header: list) -> str:
        unique_name = generate_unique_name('csv')
        unique_path = self.get_abspath(unique_name)
        with open(unique_path, 'w+', newline='', encoding='utf-8') as f:
            f_csv = csv.writer(f)
            f_csv.writerow(header)
            f_csv.writerows(results)
        return self.get_relative_path(unique_name)

    def export_to_txt(self, results: list) -> str:
        unique_name = '{}.txt'.format(get_now_with_format())
        unique_path = self.get_abspath(unique_name)
        with open(unique_path, 'w+', newline='', encoding='utf-8') as f:
            f.write('\n'.join(results))
        return self.get_relative_path(unique_name)

    @staticmethod
    def read_csv(file_path):
        content_list = []
        try:
            with open(file_path, newline='', encoding='utf-8-sig') as csv_file:
                reader = csv.reader(csv_file)
                next(reader)
                for row in reader:
                    if len(row[0].strip()) < 2:
                        continue
                    content_list.append(row[0])
        except UnicodeDecodeError:
            abort(400, message="文件编码错误 请上传utf-8编码文件")
        except Exception:
            abort(400, message="文件格式不合规 请查看csv文件模版")
        return content_list


upload_fileset = FileSet(folder='upload', exts=DEFAULTS)
corpus_fileset = FileSet(folder='corpus', exts=DOCUMENTS + ARCHIVES + TEXT + DATA)
