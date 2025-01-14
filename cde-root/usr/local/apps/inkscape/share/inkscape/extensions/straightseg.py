#!/usr/bin/env python 
'''
Copyright (C) 2005 Aaron Spike, aaron@ekips.org

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
import math, inkex, simplepath, sys

def pointAtPercent((x1, y1), (x2, y2), percent):
    percent /= 100.0
    x = x1 + (percent * (x2 - x1))
    y = y1 + (percent * (y2 - y1))
    return [x,y]

class SegmentStraightener(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.OptionParser.add_option("-p", "--percent",
                        action="store", type="float", 
                        dest="percent", default=10.0,
                        help="move curve handles PERCENT percent closer to a straight line")
        self.OptionParser.add_option("-b", "--behavior",
                        action="store", type="int", 
                        dest="behave", default=1,
                        help="straightening behavior for cubic segments")
    def effect(self):
        for id, node in self.selected.iteritems():
            if node.tagName == 'path':
                d = node.attributes.getNamedItem('d')
                p = simplepath.parsePath(d.value)
                last = []
                subPathStart = []
                for cmd,params in p:
                    if cmd == 'C':
                        if self.options.behave <= 1:
                            #shorten handles towards end points
                            params[:2] = pointAtPercent(params[:2],last[:],self.options.percent)    
                            params[2:4] = pointAtPercent(params[2:4],params[-2:],self.options.percent)
                        else:
                            #shorten handles towards thirds of the segment                            
                            dest1 = pointAtPercent(last[:],params[-2:],33.3)
                            dest2 = pointAtPercent(params[-2:],last[:],33.3)
                            params[:2] = pointAtPercent(params[:2],dest1[:],self.options.percent)    
                            params[2:4] = pointAtPercent(params[2:4],dest2[:],self.options.percent)
                    elif cmd == 'Q':
                        dest = pointAtPercent(last[:],params[-2:],50)
                        params[:2] = pointAtPercent(params[:2],dest,self.options.percent)
                    if cmd == 'M':
                        subPathStart = params[-2:]
                    if cmd == 'Z':
                        last = subPathStart[:]
                    else:
                        last = params[-2:]
                d.value = simplepath.formatPath(p)

e = SegmentStraightener()
e.affect()
