#!/usr/bin/env python3
from flask import Flask
from units import consul_kv
import uuid
from flask_cors import CORS
import sys
skey_path = 'ConsulManager/assets/secret/skey'


if consul_kv.get_kv_dict(skey_path) == {}:
    consul_kv.put_kv(skey_path,{'sk':''.join(str(uuid.uuid4()).split('-'))})

from views import login, blackbox, consul, jobs, nodes
from units.cloud import huaweicloud,alicloud,tencent_cloud
app = Flask(__name__)

#跨域CORS配置
CORS(app, supports_credentials=True)

app.register_blueprint(login.blueprint)
app.register_blueprint(blackbox.blueprint)
app.register_blueprint(consul.blueprint)
app.register_blueprint(jobs.blueprint)
app.register_blueprint(nodes.blueprint)

class Config(object):
    JOBS = []
    SCHEDULER_API_ENABLED = True
init_jobs = consul_kv.get_kv_dict('ConsulManager/jobs')
if init_jobs is not None:
    for k,v in init_jobs.items():
        print(f'初始化任务：{k}:\n    {v}', flush=True)
    Config.JOBS = init_jobs.values()
app.config.from_object(Config())

if __name__ == "__main__":
    print(sys.argv)
    scheduler = jobs.init()
    scheduler.init_app(app)
    scheduler.start()
    app.run(host='0.0.0.0', port=2026)
