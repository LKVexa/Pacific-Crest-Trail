import sys
import json,sqlite3,subprocess,time,urllib.request,urllib.error,uuid
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];REPO=ROOT
PYTHON=Path(sys.executable)
DATA=ROOT/'tests'/('experience_http_'+uuid.uuid4().hex[:8]);PORT=8770;ORIGIN=f'http://127.0.0.1:{PORT}'
nonce=None;process=None;checks=[]
def api(path,body=None,expected=200):
    headers={'Content-Type':'application/json','Origin':ORIGIN}
    if nonce:headers['X-PCT-Nonce']=nonce
    request=urllib.request.Request(ORIGIN+path,data=json.dumps(body).encode() if body is not None else None,headers=headers)
    try:
        with urllib.request.urlopen(request,timeout=30) as response:status=response.status;data=json.load(response)
    except urllib.error.HTTPError as error:status=error.code;data=json.load(error)
    assert status==expected,(path,status,data)
    return data
def start():
    global nonce,process
    process=subprocess.Popen([str(PYTHON),str(REPO/'app'/'server.py'),'--root',str(REPO),'--data-dir',str(DATA),'--port',str(PORT),'--instance-id',str(uuid.uuid4()),'--launch-id',str(uuid.uuid4())],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    for _ in range(100):
        if process.poll() is not None:raise RuntimeError(process.communicate())
        try:
            b=api('/api/bootstrap');nonce=b['nonce'];return b
        except urllib.error.URLError:time.sleep(.1)
    raise RuntimeError('Service did not start')
def stop():
    health=api('/api/health');api('/api/shutdown',{'instance_id':health['instance_id']});process.wait(20)
def mutate(action,exp,**extra):
    body={'day_id':exp['day_id'],'operation_id':str(uuid.uuid4()),'expected_experience_revision':exp['experience_revision'],'expected_campaign_revision':exp['campaign_revision'],**extra}
    result=api('/api/'+action,body)
    assert result['receipt']['operation_id']==body['operation_id']
    return result['experience'],body,result
try:
    start();assert api('/api/state')['revision']==0
    exp=api('/api/experience?day=day-001');assert not exp['eligibility']['eligible']
    denied=api('/api/complete',{'day_id':'day-001','operation_id':str(uuid.uuid4()),'expected_revision':0},409)
    assert denied['error']['code']=='day_requirements_unmet';checks.append('Unprepared day cannot complete')
    exp,assignment_body,_=mutate('assignment',exp,activity_category='walking',title='Synthetic fixture',duration_minutes=15,distance=1,distance_unit='mi')
    exp,workout_body,_=mutate('workout',exp,duration_minutes=5,distance=.1,distance_unit='km',purpose='walking')
    assert exp['actual_totals']['distance_meters']==100 and not exp['eligibility']['walking_assignment_met']
    checks.append('Partial physical activity is distinct from virtual route distance and assignment completion')
    stale={**assignment_body,'operation_id':str(uuid.uuid4())};api('/api/assignment',stale,409)
    replay=api('/api/workout',workout_body);assert replay['replayed'];assert replay['experience']['workout_count']==1
    recovered=api('/api/operations/'+workout_body['operation_id']);assert recovered['receipt']['workout_id']==replay['receipt']['workout_id']
    checks.append('Stale revisions rejected, exact replay and committed receipt recovery preserve one workout')
    bad={'day_id':exp['day_id'],'operation_id':str(uuid.uuid4()),'expected_experience_revision':exp['experience_revision'],'expected_campaign_revision':exp['campaign_revision'],'option_id':exp['scenario']['options'][0]['id'],'duration_minutes':500}
    api('/api/decision',bad,400);checks.append('Fiction cannot submit physical assignment changes')
    before_assignment=exp['assignment'].copy()
    for number in range(1,267):
        day=f'day-{number:03}'
        if number>1:exp=api('/api/experience?day='+day)
        exp,prep_body,_=mutate('preparation',exp,reviewed_dossier=True)
        free=next(o for o in exp['scenario']['options'] if o['cost_planning_tokens']==0)
        exp,decision_body,_=mutate('decision',exp,option_id=free['id'],acknowledged=True)
        exp,journal_body,_=mutate('journal',exp,text=f'Synthetic reflection for test section {number}',expected_journal_revision=0,acknowledge_empty=False)
        assert exp['eligibility']['eligible']
        if number==1:
            assert exp['assignment']==before_assignment
            api('/api/complete',{'day_id':day,'operation_id':prep_body['operation_id'],'expected_revision':0},409)
            conflict={**journal_body,'operation_id':str(uuid.uuid4()),'expected_experience_revision':exp['experience_revision'],'text':'Conflicting proposed text'}
            api('/api/journal',conflict,409)
            assert api('/api/experience?day='+day)['journal']['text']==journal_body['text']
            checks.append('Choices preserve real targets, operation identities cannot cross actions, reflection conflicts retain original text')
        body={'day_id':day,'operation_id':str(uuid.uuid4()),'expected_revision':number-1}
        result=api('/api/complete',body);assert result['state']['revision']==number
        repeated=api('/api/complete',body);assert repeated['replayed'] and repeated['state']['revision']==number
        if number==150:
            stop();b=start();assert b['current_day_id']=='day-151' and b['revision']==150
            checks.append('Restart resumes day151 after150 eligible durable completions')
        if number%50==0:print('Completed',number,'isolated eligible days',flush=True)
    end=api('/api/state');assert end['expedition_complete'] and end['current_day_id'] is None and end['revision']==266
    api('/api/experience?day=day-267',expected=404)
    stop();b=start();assert b['expedition_complete'] and b['revision']==266
    checks.append('Full266-day completion and endpoint restart produce no267th day')
    exported=api('/api/export',{'operation_id':str(uuid.uuid4())})
    text=json.dumps(exported['history']);assert 'Synthetic reflection for test section 266' in text and nonce not in text and 'instance_id' not in text
    checks.append('Private export retains real and fictional domain history while excluding service credentials')
    stop()
    db=sqlite3.connect(DATA/'hike.sqlite')
    assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and db.execute('PRAGMA foreign_key_check').fetchall()==[]
    assert db.execute('SELECT COUNT(*) FROM completion').fetchone()[0]==266
    assert db.execute('SELECT COUNT(*) FROM experience_workout').fetchone()[0]==1
    assert db.execute('SELECT COUNT(*) FROM experience_journal').fetchone()[0]==266
    db.close();checks.append('Database integrity, foreign keys and exact causal counts reconcile')
    report={'passed':True,'sections_completed':266,'original_user_data_used':False,'test_data_directory':str(DATA),'checks':checks}
    (ROOT/'tests'/'experience_http_validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report,indent=2))
finally:
    if process is not None and process.poll() is None:
        try:stop()
        except Exception:process.terminate();process.wait(10)
