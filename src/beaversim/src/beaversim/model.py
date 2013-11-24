import sys
import beaversim
from beaversim import gui
import thread

from react.api.model import *
from react.api.terminals import *
from react.api.types import *

MAX_BEAVERS = 3
MAX_X = 80
MAX_Y = 25

"""
  Records
"""
class Beaver(Record):
    name   = str
    pos_x  = int
    pos_y  = int
    v_x    = int
    v_y    = int

"""
  Machines
"""
class BeaverSim(Machine, CursesTerminal):
    beavers = listof(Beaver)

    def on_start(self):
        self.term = gui.start()

    def on_exit(self):
        self.term.stop()

    def every_1s(self):
        for beaver in self.beavers:
            beaver.pos_x = beaver.pos_x + beaver.v_x
            beaver.pos_y = beaver.pos_y + beaver.v_y
        draw_spec = [(b.name, b.pos_x, b.pos_y, 1) for b in self.beavers]
        self.term.draw(draw_spec)

class RemoteCtrl(Machine):
    pass

"""
  Events
"""
class CtrlEv(Event):
    sender   = { "ctrl": RemoteCtrl }
    receiver = { "sim":  BeaverSim }


class Spawn(CtrlEv):
    name     = str

    def guard(self):
        len(self.sim.beavers) < MAX_BEAVERS

    def handler(self):
        beaver = Beaver(name=self.name, pos_x=0, pos_y=0, v_x=1, v_y=0)
        self.sim.beavers.append(beaver)

class SetPos(CtrlEv):
    name     = str
    x        = int
    y        = int

    def guard(self):
        beavers = Beaver.where(name=self.name)
        if not beavers: return "Beaver %s not found" % self.name
        self._beaver = beavers[0]

    def handler(self):
        self._beaver.pos_x = self.x
        self._beaver.pos_y = self.y

class SetVel(CtrlEv):
    name     = str
    vx       = int
    vy       = int

    def guard(self):
        beavers = Beaver.where(name=self.name)
        if not beavers: return "Beaver with name %s not found" % self.name
        self._beaver = beavers[0]

    def handler(self):
        self._beaver.v_x = self.vx
        self._beaver.v_y = self.vy

class RedirectBeaverWheneverHitsTheWall(Event):
    receiver = { "sim": BeaverSim }

    def whenever(self):
        def filter_func(beaver):
            not (0 < beaver.pos_x < MAX_X and 0 < beaver.pos_y < MAX_Y)
        self.outside_beavers = filter(filter_func, self.sim.beavers)
        return len(self.outside_beavers) > 0

    def handler(self):
        for beaver in self.outside_beavers:
            if not 0 < beaver.pos_x < MAX_X: beaver.v_x = -beaver.v_x
            if not 0 < beaver.pos_y < MAX_Y: beaver.v_y = -beaver.v_y

#import pdb; pdb.set_trace()