import time
from tenable.sc import TenableSC
from flask import Flask, jsonify, request, send_file
from threading import Lock
from getpass import getpass

apikey = open('apikey.txt').read().splitlines()

sc = TenableSC(host='something.somewhere.com',
               access_key=apikey[0],
               secret_key=apikey[1])

mylock = Lock()

myscan_prefix = '@SCB - '
myscan = next(
    x for x
    in sc.scans.list()['usable']
    if x['name'].startswith(myscan_prefix)
)['id']

print('my scan:', myscan)
app = Flask(__name__)


@app.route('/')
def index():
    return send_file('./index.html')


@app.route('/scan_details')
def scan_details():
    uid = int(request.args['id'])
    assert uid
    r = sc.scan_instances.details(uid)
    if r['name'].startswith(myscan_prefix):
        r['name'] = r['name'][len(myscan_prefix):]
    return jsonify(r)


@app.route('/scan_results')
def scan_results():
    uid = int(request.args['id'])
    assert uid
    return jsonify([
        item for item in sc.analysis.scan(uid)
        if item['severity']['id'] != '0'
        or item['pluginName'].startswith('Authentication ')
    ])


@app.route('/new_scan')
def new_scan():
    target = str(request.args['target']).strip()
    assert target
    for c in target:
        assert c.isalnum() or c in "_.-"
    with mylock:
        sc.scans.edit(myscan, targets=[target], name=myscan_prefix+target)
        s = sc.scans.launch(myscan)
        time.sleep(3)
    return jsonify({'id': s['scanResult']['id']})


app.run(host='127.0.0.1')
