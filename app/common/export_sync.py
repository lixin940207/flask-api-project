# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/4/10-5:59 下午
import os


def get_last_export_file(predict_job, export_file_path):
    # 检查上一次导出的结果，如果没有最近更新的话，就直接返回上次的结果
    if os.path.exists(export_file_path) and os.listdir(export_file_path):
        last_file = sorted(os.listdir(export_file_path), reverse=True)[0]
        last_file_time = last_file.split('.')[0]
        last_updated_time = predict_job.last_updated_time.strftime("%Y%m%d%H%M%S") if predict_job.last_updated_time else ''
        if (not last_updated_time) or (last_file_time >= last_updated_time):  # 如果距离上次导出之后，job没有改动（一般都没有改动），就直接返回上次导出结果
            return os.path.join(export_file_path, last_file)
    return None


def generate_extract_file(predict_task_and_doc_list, export_fileset, doc_terms, offset=50):
    results = []
    for task, doc in predict_task_and_doc_list:
        results.append([doc.doc_raw_name, '', '', '', ''])
        with open(os.path.join('upload', doc.doc_unique_name), 'r') as f:
            content = f.read()
        task_results = task.task_result
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


def generate_classify_file(predict_task_and_doc_list, export_fileset):
    results = []
    for task, doc in predict_task_and_doc_list:
        row = [doc.doc_raw_name, task.predict_task_result[0]['label_name'] if task.predict_task_result else '']
        results.append(row)
    csv_path = export_fileset.export_to_csv(results=results, header=['content', 'result'])
    return csv_path


def generate_wordseg_file(predict_task_and_doc_list, export_fileset):
    results = []
    for task, _ in predict_task_and_doc_list:
        task_results = task.task_result
        tagged_content = ''
        for entity in task_results:
            tagged_content += '{}/{}  '.format(entity[0], entity[1])
        results.append(tagged_content)
    txt_path = export_fileset.export_to_txt(results=results)
    return txt_path