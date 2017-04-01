import unittest
from pybuildinfo.vcs.undefined import UndefinedVCS


class VCSUndefined(unittest.TestCase):
    def test_status(self):
        vc = UndefinedVCS()
        self.assertEqual(vc.version, "0.0.0")
        self.assertEqual(vc.name, "undefined")
        self.assertEqual(vc.alias, ["undefined"])
        self.assertEqual(vc.status(), (0, '', ''))

        revision = 'revision_short', 'revision', 'timestamp', 'author', 'author_email', 'message'
        revision = dict(zip((revision), ['undefined'] * len(revision)))
        revision['timestamp'] = 0
        revision['tags'] = []
        self.assertEqual(vc.revision(), revision)
        self.assertEqual(vc.branch(), "undefined")
        self.assertEqual(vc.all_commits(), [])
        self.assertEqual(vc.all_tags(), [])
        self.assertEqual(vc.revision_tags(None), [])
        self.assertEqual(vc.find_version(), [0, 0, 0, '0.0.0-undefined'])
        with self.assertRaises(RuntimeError) as context:
            vc.command('status')
        self.assertTrue('undefined' == str(context.exception))
