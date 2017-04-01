# -*- coding: UTF-8 -*-
"""
Python Build Info Tool
Undefined VCS
"""


class UndefinedVCS:
    def __init__(self, path=None, version_regex=None, void=False):
        pass

    @property
    def version(self):
        return '0.0.0'

    @property
    def name(self):
        return 'undefined'

    @property
    def alias(self):
        return ['undefined']

    def status(self):
        return 0, '', ''

    def revision(self, revision=None):
        di = 'revision_short', 'revision', 'timestamp', 'author', 'author_email', 'message'
        result = dict(zip((di), ['undefined'] * len(di)))
        result['timestamp'] = 0
        result['tags'] = []
        return result

    def branch(self):
        return 'undefined'

    def all_commits(self):
        return []

    def all_tags(self):
        return []

    def revision_tags(self, revision):
        return []

    def find_version(self):
        return [0, 0, 0, '0.0.0-undefined']

    def command(self, *args, raw=False):
        raise RuntimeError('undefined')
