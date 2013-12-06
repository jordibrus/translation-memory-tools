# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Jordi Mas i Hernandez <jmas@softcatala.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

from fileset import FileSet
from findfiles import FindFiles

import os
import sys


class GitFileSet(FileSet):
 
    def _get_filename(self):
        filename = self.url.split('/')[-1]
        return filename
        
    def _remove_non_translation_files(self):
        findFiles = FindFiles()

        for filename in findFiles.find(self.temp_dir, '-ca.po'):
            if re.match(self.pattern, filename) is None and \
                    os.path.exists(filename):
                os.remove(filename)

    def convert_android_resources_files_to_po(self):
    
        filename = self._get_filename()
        
        src = os.path.join(self.temp_dir, "res/values/strings.xml")
        trg = os.path.join(self.temp_dir, "res/values-ca/strings.xml")

        # See: https://pypi.python.org/pypi/android2po/1.2.0
        cmd = 'cd {0}/{1} && a2po init ca'.format(self.temp_dir, filename)
        os.system(cmd)

    def do(self):
        self.create_tmp_directory()

        os.system('cd {0} && git clone --depth=1 {1}'.format(
            self.temp_dir,
            self.url
        ))

        self.convert_android_resources_files_to_po()
        self._remove_non_translation_files()
        self.add_comments()
        self.build()

        self.remove_tmp_directory()
