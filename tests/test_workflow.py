import csv
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]

def load(path, name):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

prep=load(ROOT/'scripts'/'prepare_origin_data.py','prepare_origin_data')
auditor=load(ROOT/'scripts'/'audit_evidence.py','audit_evidence')

class WorkflowTest(unittest.TestCase):
    def test_prepare_real_zero_and_interval(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'rows.csv'
            with p.open('w',newline='') as f:
                w=csv.DictWriter(f,fieldnames=['panel','series','replicate','x','y']);w.writeheader()
                for rep,val in [('1',0),('2',2)]:
                    for x in [0,1]:w.writerow(dict(panel='a',series='baseline',replicate=rep,x=x,y=val+x))
            rows,meta=prep.summarize(p,'sd','seed')
            self.assertEqual(rows[0]['mean'],1.0)
            self.assertEqual(rows[0]['n'],2)
            self.assertGreater(rows[0]['err_minus'],0)
            self.assertEqual(meta['n_raw'],4)

    def test_reject_unequal_grid_and_duplicate(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'data.csv'
            p.write_text('panel,series,replicate,x,y\na,b,1,0,0\na,b,2,1,0\n')
            with self.assertRaisesRegex(ValueError,'Unequal X'):
                prep.summarize(p)
            p.write_text('panel,series,replicate,x,y\na,b,1,0,0\na,b,1,0,1\n')
            with self.assertRaisesRegex(ValueError,'Duplicate'):
                prep.summarize(p)

    def test_ledger_planned_and_unsupported(self):
        data=json.loads((ROOT/'assets'/'evidence-ledger.json').read_text())
        errors,warnings=auditor.audit(data,ROOT)
        self.assertEqual(errors,[])
        data['claims'][0]['status']='supported'
        self.assertTrue(auditor.audit(data,ROOT)[0])

    def test_cpu_runner_budget_and_freeze(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp=Path(tmp);project=tmp/'demo'
            shutil.copytree(ROOT/'assets'/'demo',project)
            state=tmp/'state'
            runner=ROOT/'scripts'/'autoresearch_loop.py'
            def run(*args):
                return subprocess.run([sys.executable,str(runner),*args],capture_output=True,text=True)
            a=run('init','--config',str(project/'autoresearch.json'),'--state',str(state))
            self.assertEqual(a.returncode,0,a.stderr)
            a=run('run','--state',str(state),'--role','baseline','--hypothesis','H0','--seed','7')
            self.assertEqual(a.returncode,0,a.stderr)
            baseline=json.loads((state/'trials'/'000001'/'record.json').read_text())
            self.assertGreater(baseline['metric'],0)
            (project/'train_config.json').write_text('{"learning_rate":0.2,"steps":15}')
            a=run('run','--state',str(state),'--role','candidate','--hypothesis','H1','--seed','7')
            self.assertEqual(a.returncode,0,a.stderr)
            candidate=json.loads((state/'trials'/'000002'/'record.json').read_text())
            self.assertEqual(candidate['decision'],'candidate_keep')
            self.assertLess(candidate['metric'],baseline['metric'])
            a=run('run','--state',str(state),'--role','confirmation','--hypothesis','H1','--seed','101')
            self.assertEqual(a.returncode,0,a.stderr)
            self.assertEqual(json.loads((state/'trials'/'000003'/'record.json').read_text())['decision'],'confirmation_recorded')
            (project/'evaluate.py').write_text('print("tampered")')
            a=run('run','--state',str(state),'--role','candidate','--hypothesis','H2','--seed','5')
            self.assertNotEqual(a.returncode,0)
            self.assertIn('Protected file hash',a.stderr)
            # Invalid start is rejected before allocating a trial.
            self.assertFalse((state/'trials'/'000004').exists())

if __name__=='__main__':unittest.main()
