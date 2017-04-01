import unittest
from tests.resource import Repo
from pybuildinfo.vcs.hg import Hg


class VCSHg(unittest.TestCase):
    def test_names(self):
        self.assertEqual(Hg(void=True).name, 'Mercurial')
        self.assertEqual(sorted(Hg(void=True).alias), sorted(['mercurial', 'hg']))

    def test_status(self):
        with Repo('hg') as path:
            vc = Hg(path=path)
            status, stdout, stderr = vc.status()
            self.assertEqual(status, 0)
            self.assertFalse(stderr)

    def test_revision(self):
        with Repo('hg') as path:
            vc = Hg(path=path)
            rev = vc.revision()
            self.assertEqual(rev['revision'], '5491a15ea2921e4b40f92fdfaa8bd2654a1ae9f9')
            self.assertEqual(rev['revision_short'], '5491a15ea292')
            self.assertEqual(rev['author'], 'Andrei V')
            self.assertEqual(rev['author_email'], 'andrei@ptaxa.net')
            self.assertEqual(rev['message'], 'Added tag super_commit for changeset 5114a47c4b94')
            self.assertEqual(rev['timestamp'], 1491076600)
            self.assertEqual(rev['tags'], [])

            rev = vc.revision('5114a47c4b94a97579a8ad12134e06cb9e6e1fdb')
            self.assertEqual(rev['revision'], '5114a47c4b94a97579a8ad12134e06cb9e6e1fdb')
            self.assertEqual(rev['revision_short'], '5114a47c4b94')
            self.assertEqual(rev['author'], 'Andrei V')
            self.assertEqual(rev['author_email'], 'andrei@ptaxa.net')
            self.assertEqual(rev['message'], 'hg-commit-0x02')
            self.assertEqual(rev['timestamp'], 1491076573)
            self.assertEqual(rev['tags'], ['super_commit'])

            rev = vc.revision('bb79b')
            self.assertEqual(rev['revision'], 'bb79bbcfa99d02348e8216759ead9f6c09b797f3')
            self.assertEqual(rev['revision_short'], 'bb79bbcfa99d')
            self.assertEqual(rev['author'], 'Andrei V')
            self.assertEqual(rev['author_email'], 'andrei@ptaxa.net')
            self.assertEqual(rev['message'], 'hg-commit-0x00')
            self.assertEqual(rev['timestamp'], 1491076548)
            self.assertEqual(rev['tags'], ['v1.0.5-rc'])

    def test_branch(self):
        with Repo('hg') as path:
            vc = Hg(path=path)
            self.assertEqual(vc.branch(), 'default')

    def test_all_commits(self):
        with Repo('hg') as path:
            vc = Hg(path=path)
            self.assertEqual(vc.all_commits(), [
                '5491a15ea2921e4b40f92fdfaa8bd2654a1ae9f9',
                '5114a47c4b94a97579a8ad12134e06cb9e6e1fdb',
                'a83106fce2d1fe0be0cfd0690abeddd0faf4e298',
                'dfbf2cb40830183496be2731f595861b9e0f491a',
                'bb79bbcfa99d02348e8216759ead9f6c09b797f3',
            ])

    def test_tags(self):
        with Repo('hg') as path:
            vc = Hg(path=path)
            tags = list(vc.all_tags())
            self.assertEqual(tags, [
                ['v1.0.5-rc', 'bb79bbcfa99d02348e8216759ead9f6c09b797f3'],
                ['super_commit', '5114a47c4b94a97579a8ad12134e06cb9e6e1fdb'],
            ])
            for tag in tags:
                self.assertEqual(vc.tag_hash(tag[0]), tag[1])

            self.assertEqual(vc.revision_tags('5491a15ea2921e4b40f92fdfaa8bd2654a1ae9f9'), [])
            self.assertEqual(vc.revision_tags('5114a47c4b94a97579a8ad12134e06cb9e6e1fdb'), ['super_commit'])
            self.assertEqual(vc.revision_tags('a83106fce2d1fe0be0cfd0690abeddd0faf4e298'), [])
            self.assertEqual(vc.revision_tags('dfbf2cb40830183496be2731f595861b9e0f491a'), [])
            self.assertEqual(vc.revision_tags('bb79bbcfa99d02348e8216759ead9f6c09b797f3'), ['v1.0.5-rc'])

    def test_find_version(self):
        with Repo('hg') as path:
            vc = Hg(path=path)
            self.assertEqual(vc.find_version(), [1, 0, 5, 'v1.0.5-rc'])
