import unittest
from tests.resource import Repo
from pybuildinfo.vcs.git import Git


class VCSGit(unittest.TestCase):
    def test_names(self):
        self.assertEqual(Git(void=True).name, 'Git')
        self.assertEqual(sorted(Git(void=True).alias), sorted(['git']))

    def test_status(self):
        with Repo('git') as path:
            vc = Git(path=path)
            status, stdout, stderr = vc.status()
            self.assertEqual(status, 0)
            self.assertFalse(stderr)

    def test_revision(self):
        with Repo('git') as path:
            vc = Git(path=path)
            rev = vc.revision()
            self.assertEqual(rev['revision'], 'c64708a209ecec56f1988eb2c2be49a0cb22082c')
            self.assertEqual(rev['revision_short'], 'c64708a')
            self.assertEqual(rev['author'], 'Andrei V')
            self.assertEqual(rev['author_email'], 'andrei@ptaxa.net')
            self.assertEqual(rev['message'], 'git-commit-0x02')
            self.assertEqual(rev['timestamp'], 1491075783)
            self.assertEqual(rev['tags'], ['super_commit'])

            rev = vc.revision('e9fbb0c6cad7efbb03833d5c5ab5461fce0774ee')
            self.assertEqual(rev['revision'], 'e9fbb0c6cad7efbb03833d5c5ab5461fce0774ee')
            self.assertEqual(rev['revision_short'], 'e9fbb0c')
            self.assertEqual(rev['author'], 'Andrei V')
            self.assertEqual(rev['author_email'], 'andrei@ptaxa.net')
            self.assertEqual(rev['message'], 'git-commit-0x01')
            self.assertEqual(rev['timestamp'], 1491075753)
            self.assertEqual(rev['tags'], [])

    def test_branch(self):
        with Repo('git') as path:
            vc = Git(path=path)
            self.assertEqual(vc.branch(), 'master')

    def test_all_commits(self):
        with Repo('git') as path:
            vc = Git(path=path)
            self.assertEqual(vc.all_commits(), [
                'c64708a209ecec56f1988eb2c2be49a0cb22082c',
                'e9fbb0c6cad7efbb03833d5c5ab5461fce0774ee',
                '4b15c8def9bfd087fe03912b4f3639a8f5d44106',
            ])

    def test_tags(self):
        with Repo('git') as path:
            vc = Git(path=path)
            tags = list(vc.all_tags())
            self.assertEqual(tags, [
                ['v1.0.5-rc', '4b15c8def9bfd087fe03912b4f3639a8f5d44106'],
                ['super_commit', 'c64708a209ecec56f1988eb2c2be49a0cb22082c'],
            ])
            for tag in tags:
                self.assertEqual(vc.tag_hash(tag[0]), tag[1])

            self.assertEqual(vc.revision_tags('c64708a209ecec56f1988eb2c2be49a0cb22082c'), ['super_commit'])
            self.assertEqual(vc.revision_tags('e9fbb0c6cad7efbb03833d5c5ab5461fce0774ee'), [])
            self.assertEqual(vc.revision_tags('4b15c8def9bfd087fe03912b4f3639a8f5d44106'), ['v1.0.5-rc'])

    def test_find_version(self):
        with Repo('git') as path:
            vc = Git(path=path)
            self.assertEqual(vc.find_version(), [1, 0, 5, 'v1.0.5-rc'])
