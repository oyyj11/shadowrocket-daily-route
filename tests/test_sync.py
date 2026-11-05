"""Publication safety: invalid downloads/failed validation cannot replace good rules."""
from pathlib import Path
import io, json, shutil, sys, tempfile, unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import sync_telegram
import validate

class SyncSafety(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        shutil.copytree(ROOT/'rules',self.root/'rules')
        for f in ['DailyRoute-OriginalPlus.conf','DailyRoute-APNs-Proxy.conf','notification-sources.json','original-plus-validation.json']:
            shutil.copyfile(ROOT/f,self.root/f)
        self.nodes=json.loads((self.root/'notification-sources.json').read_text(encoding='utf-8'))['telegram']['cidrs']

    def snapshot(self):
        return {str(p.relative_to(self.root)):p.read_bytes() for p in self.root.rglob('*') if p.is_file()}

    def run_sync(self,data):
        with patch.object(sync_telegram,'ROOT',self.root),patch.object(validate,'ROOT',self.root),patch.object(sync_telegram.urllib.request,'urlopen',return_value=io.BytesIO(data)):
            sync_telegram.main()

    def test_default_route_is_rejected_without_changes(self):
        before=self.snapshot()
        with self.assertRaises(AssertionError): self.run_sync(('\n'.join(self.nodes+['0.0.0.0/0'])+'\n').encode())
        self.assertEqual(before,self.snapshot())

    def test_malformed_download_is_rejected_without_changes(self):
        before=self.snapshot()
        with self.assertRaises(ValueError): self.run_sync(('\n'.join(self.nodes+['not-a-network'])+'\n').encode())
        self.assertEqual(before,self.snapshot())

    def test_validation_failure_rolls_back_all_outputs(self):
        before=self.snapshot()
        with patch.object(sync_telegram,'validate',side_effect=RuntimeError('simulated regression')):
            with self.assertRaises(RuntimeError): self.run_sync(('\n'.join(reversed(self.nodes))+'\n').encode())
        self.assertEqual(before,self.snapshot())

    def test_success_is_idempotent_and_never_changes_personal_template(self):
        template=(self.root/'DailyRoute-OriginalPlus.conf').read_bytes()
        data=('\n'.join(reversed(self.nodes))+'\n').encode()
        self.run_sync(data)
        first=self.snapshot()
        self.run_sync(data)
        self.assertEqual(first,self.snapshot())
        self.assertEqual(template,(self.root/'DailyRoute-OriginalPlus.conf').read_bytes())

if __name__=='__main__': unittest.main()
