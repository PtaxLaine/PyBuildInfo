# -*- coding: UTF-8 -*-
"""
Python Build Info Tool
Logic
"""
import subprocess
import time
from string import Template
import pybuildinfo.vcs as vcs
import platform
import os
import pybuildinfo
from pybuildinfo.vcs.undefined import UndefinedVCS

try:
    import pwd
except ModuleNotFoundError:
    pass


C_PREDEF_ARCH = '\n' \
                '#if (defined(__amd64__) || defined(_M_AMD64))\n"x86_64"\n' \
                '#elif (defined(__i386__) || defined(__i386) || defined(_M_IX86) || defined(__X86__) || ' \
                       'defined(_X86_) || defined(__THW_INTEL__) || defined(__I86__) || ' \
                       'defined(__INTEL__) || defined(__386))\n"x86"\n' \
                '#elif (defined(__arm__) || defined(_ARM) || defined(_M_ARM) || defined(__arm))\n"ARM"\n' \
                '#elif (defined(__aarch64__) || defined(_M_ARM64))\n"ARM64"\n' \
                '#elif (defined(__IA64__) || defined(__ia64) || defined(_M_IA64) || defined(__itanium__))\n"IA-64"\n' \
                '#elif (defined(__mips__) || defined(__mips) || defined(__MIPS__))\n"MIPS"\n' \
                '#elif (defined(__ppc__) || defined(_M_PPC) || defined(_ARCH_PPC) || defined(__ppc))\n"PPC"\n' \
                '#else\n'


def ut_to_rfc2822(timestamp):
    if isinstance(timestamp, time.struct_time):
        return time.strftime("%a, %d %b %Y %H:%M:%S +0000", timestamp)
    else:
        return time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime(int(timestamp)))


def unpack_revision(vc):
    revision = vc.revision()

    revision['time'] = time.gmtime(int(revision['timestamp']))
    revision['time_rfc2822'] = ut_to_rfc2822(revision['timestamp'])
    revision['branch'] = vc.branch()
    revision['name'] = vc.name
    revision['author_name'] = revision['author']
    revision['author'] = "{} <{}>".format(revision['author_name'], revision['author_email'])
    revision['tags_c'] = "{{ {} }}".format(', '.join(['"{}"'.format(x) for x in revision['tags']]))
    
    ver = vc.find_version()
    revision['version'] = '.'.join(str(x) for x in ver[:3])
    revision['version_tag'] = ver[3]
    revision['version_major'] = ver[0]
    revision['version_minor'] = ver[1]
    revision['version_patch'] = ver[2]
    revision['version_stable'] = (0x01 - (int(ver[1]) & 0x01)) if int(ver[0]) > 0 else 0x00

    return revision


def unpack_station():
    def username():
        try:
            return os.getlogin()
        except FileNotFoundError:
            return pwd.getpwuid(os.getuid())[0]

    def os_version():
        version = platform.version()
        if 'linux' in platform.system().lower():
            try:
                with subprocess.Popen(['lsb_release', '-d'], stdout=subprocess.PIPE, stderr=subprocess.PIPE) as lbs:
                    lbs.wait()
                    version = lbs.stdout.readlines()[0].decode()
                    description = 'description:'
                    if version.lower().startswith(description):
                        version = version[len(description):].strip()
                    else:
                        raise RuntimeError()
            except:
                version = platform.release()
        return [platform.system(), version]

    ut = int(time.time())
    return {
        'time': time.gmtime(ut),
        'timestamp': ut,
        'time_rfc2822': ut_to_rfc2822(ut),
        'node': platform.node(),
        'user': username(),
        'arch': platform.machine(),
        'system': os_version()[0],
        'system_version': os_version()[1]
    }


def repack(data):
    result = {}
    for section in data:
        for node in data[section]:
            result["{}_{}".format(section, node)] = data[section][node]
    return result


def pick_vcs(vcs_root, vcs_force, version_regex, quiet):
    if not vcs_force:
        vc = vcs.detect_vcs(vcs_root)
        if not vc and not quiet:
            raise RuntimeError('vcs not found')
        elif not vc:
            return UndefinedVCS()
        else:
            return vc(path=vcs_root, version_regex=version_regex)
    else:
        vc = vcs.vcs_by_name(vcs_force)
        if not vc:
            raise ValueError('{} bad vcs'.format(vcs_force))
        vc = vc(path=vcs_root, version_regex=version_regex)
        if vc.status()[0] != 0:
            raise RuntimeError('{} repository not found in {}'.format(vc.name, vcs_root))
        return vc


def run(usr_dict, vcs_root, output, vcs_force, template, version_regex, quiet):
    vc = pick_vcs(vcs_root, vcs_force, version_regex, quiet)

    result = {
        'vcs': unpack_revision(vc),
        'station': unpack_station(),
        'pbi': {
            'version': pybuildinfo.version_dict()['version']
        },
        'build': {
            'toolchain': 'undefined',
            'toolchain_version': 'undefined',
            'target_system': 'undefined',
            'target_arch': 'undefined',
        }
    }
    result = repack(result)
    result.update(usr_dict)
    result['c_predef_arch'] = C_PREDEF_ARCH

    output.write(Template(template.read()).safe_substitute(result).encode())
    output.write(b'\n')
    output.flush()
