# -*- coding: UTF-8 -*-
"""
Python Build Info Tool
Mercurial VCS
"""
import os
import re
import logging
from subprocess import Popen, PIPE


class Hg:
    def __init__(self, path=None, version_regex=None, void=False):
        if not void:
            self.__path = path
            logging.info("{} {} detected".format(self.name, self.version))

            if not version_regex:
                self.__version_regex = re.compile(r'^(v|ver|version)\.? ?([0-9]+)\.([0-9]+)\.?([0-9]+)?.*$')
            else:
                self.__version_regex = re.compile(version_regex)

    @property
    def version(self):
        version = self.command('version')
        mark = 'Mercurial Distributed SCM (version'
        if version.startswith(mark):
            return version.splitlines()[0][len(mark):].strip(')').strip()
        else:
            return version

    @property
    def name(self):
        return "Mercurial"

    @property
    def alias(self):
        return ['mercurial', 'hg']

    def status(self):
        return self.command('status', raw=True)

    def revision(self, revision='.'):
        cmd = self.command('log', '-l', '1', '-r', revision, '--template', '{node|short}\t{node}\t{date|hgdate}\t{author|person}\t{author|email}\t{desc}')
        result = dict(zip(('revision_short', 'revision', 'timestamp', 'author', 'author_email', 'message'), cmd.split('\t', maxsplit=5)))
        for x in result:
            result[x] = (result[x].strip()).encode('unicode_escape').decode()
        result['timestamp'] = int(result['timestamp'].split()[0])
        result['tags'] = self.revision_tags(result['revision'])
        return result

    def branch(self):
        return self.command('identify', '-b')

    def all_commits(self):
        return self.command('log', '--template', '{node}\n').splitlines()

    def all_tags(self):
        tmp = self.command('log', '-r', 'tag()', '--template', '{node}\t{tags}\n')
        tmp = [x.split() for x in tmp.splitlines()]
        result = []
        for x in tmp:
            for tag in x[1:]:
                result.append([tag, x[0]])
        return result

    def tag_hash(self, tag):
        return self.command('log', '-l', '1', '-r', tag, '--template', '{node}')

    def revision_tags(self, revision):
        all_tags = self.all_tags()
        ref_tags = []
        for tag in all_tags:
            if tag[1] == revision:
                ref_tags.append(tag[0])
        return ref_tags

    def find_version(self):
        all_tags = self.all_tags()
        for commit in self.all_commits():
            for tag in all_tags:
                if tag[1].lower() == commit:
                    x = self.__version_regex.match(tag[0])
                    if x:
                        x = [x.group(2), x.group(3), x.group(4)]
                        return [int(t if t.strip() else 0) if t else 0 for t in x] + [tag[0]]
        return [0, 0, 0, '0.0.0']

    def command(self, *args, raw=False):
        assert isinstance(raw, bool)
        original_wd = os.getcwd()
        try:
            os.chdir(self.__path)
            with Popen(('hg',) + args, stdout=PIPE, stderr=PIPE, shell=False) as pipe:
                stdout = bytearray()
                stderr = bytearray()
                while pipe.returncode is None:
                    o, e = pipe.communicate()
                    stdout.extend(o)
                    stderr.extend(e)
                if raw:
                    return pipe.returncode, stdout.decode().strip(), stderr.decode().strip()
                else:
                    if pipe.returncode != 0:
                        raise RuntimeError(stderr.decode())
                    return stdout.decode().strip()
        except FileNotFoundError as ex:
            raise OSError("Mercurial not found")
        finally:
            os.chdir(original_wd)
