#!/usr/bin/env python 
'''
Copyright (C) 2006 Aaron Spike, aaron@ekips.org

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
'''
import inkex, cubicsuperpath, simplepath, cspsubdiv

class MyEffect(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.OptionParser.add_option("-f", "--flatness",
                        action="store", type="float", 
                        dest="flat", default=10.0,
                        help="Minimum flatness of the subdivided curves")
    def effect(self):
        for id, node in self.selected.iteritems():
            if node.tagName == 'path':
                d = node.attributes.getNamedItem('d')
                p = cubicsuperpath.parsePath(d.value)
                cspsubdiv.cspsubdiv(p, self.options.flat)
                np = []
                for sp in p:
                    first = True
                    for csp in sp:
                        cmd = 'L'
                        if first:
                            cmd = 'M'
                        first = False
                        np.append([cmd,[csp[1][0],csp[1][1]]])
                        d.value = simplepath.formatPath(np)

e = MyEffect()
e.affect()