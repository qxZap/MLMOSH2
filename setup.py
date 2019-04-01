#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
u"""Hunt the Wumpus"""
from __future__ import absolute_import
from io import open
__author__ = (u'Lance Finn Helsten',)
__version__ = u'1.2'
__copyright__ = u"Copyright (C) 2014 Lance Finn Helsten, All rights reserved."
__license__ = u"""
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice,
this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
THE POSSIBILITY OF SUCH DAMAGE.
"""

import sys
if sys.version_info < (3, 0):
    #raise Exception("pyzombie requires Python 3.0 or higher.")
    pass
from distutils.core import setup

setup(
    name=u'pywumpus',
    version=__version__,
    author=u'Lance Finn Helsten',
    author_email=u'lanhel@me.com',
	#maintainer='',
    #maintainer_email='',
    url=u'http://code.google.com/p/pywumpus/',
    description=u'Hunt the Wumpus (1972) Python translation.',
    long_description=open(u'README.rst').read(),
    platforms=[u'OS Independent'],
    download_url=u'http://code.google.com/p/pywumpus/downloads/list',
    license=u"GNU General Public License",
    classifiers=[
		u'Development Status :: 5 - Production/Stable',
		u'Environment :: Console',
		u'Intended Audience :: Developers',
		u'Intended Audience :: Education',
		u'Intended Audience :: End Users/Desktop',
		u'License :: OSI Approved :: GNU General Public License (GPL)',
		u'Operating System :: OS Independent',
		u'Programming Language :: Python :: 3',
		u'Topic :: Education',
		u'Topic :: Games/Entertainment'
    ],
    scripts=[u'pywumpus.py'],
)


