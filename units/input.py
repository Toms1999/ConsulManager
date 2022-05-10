#!/usr/bin/python3
import requests, json
import xlrd

consul_token = 'xxxxxxxxxx'
consul_url = 'http://x.x.x.x:8500/v1'


def with_open_file(file=None):
    with open(file, 'r') as file:
        lines = file.readlines()

    for line in lines:
        module, company, project, env, name, instance = line.split()
        headers = {'X-Consul-Token': consul_token}
        data = {
            "id": f"{module}/{company}/{project}/{env}@{name}",
            "name": 'blackbox_exporter',
            "tags": [module],
            "Meta": {'module': module, 'company': company, 'project': project, 'env': env, 'name': name,
                     'instance': instance}
        }

        reg = requests.put(f"{consul_url}/agent/service/register", headers=headers, data=json.dumps(data))
        if reg.status_code == 200:
            print({"code": 20000, "data": "增加成功！"})
        else:
            print({"code": 50000, "data": f'{reg.status_code}:{reg.text}'})


def read_execl(path=None):
    print(path)
    data = xlrd.open_workbook(path, encoding_override="utf-8")
    sheetnames = data.sheet_names()[1]
    table_name = data.sheet_by_name(sheetnames)
    rows = table_name.nrows
    print("开始读取")
    for row in range(rows):
        if row == 0:
            continue
        sheet_row_val = table_name.row_values(row)
        yield sheet_row_val
