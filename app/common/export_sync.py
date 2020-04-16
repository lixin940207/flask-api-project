# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/4/10-5:59 下午
import os


def get_last_export_file(job, export_file_path):
    # 检查上一次导出的结果，如果没有最近更新的话，就直接返回上次的结果
    if os.path.exists(export_file_path) and os.listdir(export_file_path):
        last_file = sorted(os.listdir(export_file_path), reverse=True)[0]
        last_file_time = last_file.split('.')[0]
        last_updated_time = job.updated_time.strftime("%Y%m%d%H%M%S") if job.updated_time else ''
        if (not last_updated_time) or (last_file_time >= last_updated_time):  # 如果距离上次导出之后，job没有改动（一般都没有改动），就直接返回上次导出结果
            return os.path.join(export_file_path, last_file)
    return None


def generate_extract_file(task_and_doc_list, export_fileset, doc_terms, offset=50):
    results = []
    doc_terms = dict([[doc_term.doc_term_id, doc_term.doc_term_name] for doc_term in doc_terms])
    for task, doc in task_and_doc_list:
        results.append([doc.doc_raw_name, '', '', '', ''])
        # got dp file
        dp_file = os.path.join('upload', doc.doc_unique_name.rsplit('.',1)[0] + '.txt')
        if os.path.exists("{}_dp.txt".format(dp_file.rsplit('.', 1)[0])):
            dp_file = "{}_dp.txt".format(dp_file.rsplit('.', 1)[0])
        with open(dp_file, 'r') as f:
            content = f.read()
        task_results = getattr(task, "predict_task_result", None) or getattr(task, "mark_task_result", None)
        for idx, entity in enumerate(task_results):
            row = ["",
                    doc_terms[int(entity['doc_term_id'])],
                    content[max(0, entity['index'] - offset):entity['index']],
                    entity['value'],
                    content[entity['index'] + len(entity['value']):
                        min(len(content), entity['index'] + len(entity['value']) + offset)]]
            results.append(row)
        results.append(['', '', '', '', ''])
    csv_path = export_fileset.export_to_csv(results=results, header=["文件列表", "字段", "上文", "抽取结果", "下文"])
    return csv_path


def generate_classify_file(task_and_doc_list, export_fileset):
    results = []
    for task, doc in task_and_doc_list:
        with open(os.path.join('upload', doc.doc_unique_name), 'r') as f:
            content = f.read()
        task_result = getattr(task, "predict_task_result", None) or getattr(task, "mark_task_result", None)
        row = [doc.doc_raw_name, content, task_result[0]['label_name'] if task_result else '']
        results.append(row)
    csv_path = export_fileset.export_to_csv(results=results, header=["doc_name", 'content', 'result'])
    return csv_path


def generate_wordseg_file(task_and_doc_list, export_fileset):
    results = []
    for task, _ in task_and_doc_list:
        task_results = getattr(task, "predict_task_result", None) or getattr(task, "mark_task_result", None)
        tagged_content = ''
        for entity in task_results:
            tagged_content += '{}/{}  '.format(entity[0], entity[1])
        results.append(tagged_content)
    txt_path = export_fileset.export_to_txt(results=results)
    return txt_path
