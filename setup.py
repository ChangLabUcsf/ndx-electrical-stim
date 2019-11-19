# -*- coding: utf-8 -*-

import os

from setuptools import setup, find_packages
from shutil import copy2

setup_args = {
    'name': 'ndx-electrical-stim',
    'version': '0.1.0',
    'description': 'An NWB extension for storing waveforms associated with '
                   'neural stimulation using ECoG.',
    'author': 'Jessie R. Liu',
    'author_email': 'jrliu95@gmail.com',
    'url': '',
    'license': 'BSD 3-Clause',
    'install_requires': [
        'pynwb>=1.1.2'
    ],
    'packages': find_packages('src/pynwb'),
    'package_dir': {'': 'src/pynwb'},
    'package_data': {'ndx_electrical_stim': [
        'spec/ndx-electrical-stim.namespace.yaml',
        'spec/ndx-electrical-stim.extensions.yaml',
    ]},
    'classifiers': [
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
    ],
    'zip_safe': False
}


def _copy_spec_files(project_dir):
    ns_path = os.path.join(project_dir, 'spec', 'ndx-electrical-stim.namespace.yaml')
    ext_path = os.path.join(project_dir, 'spec', 'ndx-electrical-stim.extensions.yaml')

    dst_dir = os.path.join(project_dir, 'src', 'pynwb', 'ndx_electrical_stim',
                           'spec')
    if not os.path.exists(dst_dir):
        os.mkdir(dst_dir)

    copy2(ns_path, dst_dir)
    copy2(ext_path, dst_dir)


if __name__ == '__main__':
    _copy_spec_files(os.path.dirname(__file__))
    setup(**setup_args)
