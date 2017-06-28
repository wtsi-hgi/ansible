import os
import os.path
import sys

sys.path.insert(0, os.path.abspath('lib'))
from ansible.release import __version__, __author__
try:
    from setuptools import setup, find_packages
except ImportError:
    print("Ansible now needs setuptools in order to build. Install it using"
          " your package manager (usually python-setuptools) or via pip (pip"
          " install setuptools).")
    sys.exit(1)

with open('requirements.txt') as requirements_file:
    install_requirements = requirements_file.read().splitlines()
    if not install_requirements:
        print("Unable to read requirements from the requirements.txt file"
              "That indicates this copy of the source code is incomplete.")
        sys.exit(2)

# pycrypto or cryptography.   We choose a default but allow the user to
# override it.  This translates into pip install of the sdist deciding what
# package to install and also the runtime dependencies that pkg_resources
# knows about
crypto_backend = os.environ.get('ANSIBLE_CRYPTO_BACKEND', None)
if crypto_backend:
    if crypto_backend.strip() == 'pycrypto':
        # Attempt to set version requirements
        crypto_backend = 'pycrypto >= 2.6'

    install_requirements = [r for r in install_requirements if not (r.lower().startswith('pycrypto') or r.lower().startswith('cryptography'))]
    install_requirements.append(crypto_backend)


SYMLINKS = {'ansible': frozenset(('ansible-console',
                                  'ansible-doc',
                                  'ansible-galaxy',
                                  'ansible-playbook',
                                  'ansible-pull',
                                  'ansible-vault'))}

for source in SYMLINKS:
    for dest in SYMLINKS[source]:
        dest_path = os.path.join('bin', dest)
        if not os.path.islink(dest_path):
            try:
                os.unlink(dest_path)
            except OSError as e:
                if e.errno == 2:
                    # File does not exist which is all we wanted
                    pass
            os.symlink(source, dest_path)

setup(
    name='ansible',
    version=__version__,
    description='Radically simple IT automation',
    author=__author__,
    author_email='info@ansible.com',
    url='https://ansible.com/',
    license='GPLv3+',
    # Ansible will also make use of a system copy of python-six and
    # python-selectors2 if installed but use a Bundled copy if it's not.
    install_requires=install_requirements,
    package_dir={'': 'lib'},
    packages=find_packages('lib'),
    package_data={
        '': [
            'module_utils/*.ps1',
            'modules/windows/*.ps1',
            'modules/windows/*.ps1',
            'galaxy/data/*/*.*',
            'galaxy/data/*/*/.*',
            'galaxy/data/*/*/*.*',
            'galaxy/data/*/tests/inventory',
            'config/data/*.yaml',
            'config/data/*.yml',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],
    scripts=[
        'bin/ansible',
        'bin/ansible-playbook',
        'bin/ansible-pull',
        'bin/ansible-doc',
        'bin/ansible-galaxy',
        'bin/ansible-console',
        'bin/ansible-connection',
        'bin/ansible-vault',
    ],
    data_files=[],
)
