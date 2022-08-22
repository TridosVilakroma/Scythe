'''Module for handling game related time functions

You must call Time.init() to set all time markers before calling Time.update().
'''

import time

class TimeVariables:pass

class Period:
    '''Creates an instance to manipulate specific isolated
    time sectioning.
    
    Useful for creating an instance to track a timed event.

    age() returns time since being created(in game time)

    frame() returns a boolean to indicate weather you are within the timeframe
    passed in relative to the instance creation time.
    
    grow() and regress() allow you to age or reverse the age of your instance
    by the amount passed in.
    '''
    def __init__(self) -> None:
        self.origin=game_clock()

    def age(self):
        return game_clock()-self.origin

    def frame(self,start,end):
        return True if self.age()>=start and self.age()<end else False

    def grow(self,value):
        self.age+=value

    def regress(self,value):
        self.age-=value

def init():
    '''Initializes the Time module.

    Only call this a single time from your main script,
    regardless of additional modules needing access to Time functions.

    Calling Time.init() multiple times may have undesired effects.'''
    now=time.time()
    TimeVariables.game_start=now
    TimeVariables.game_time=0#now-TimeVariables.game_start
    TimeVariables.game_time_ref=now
    TimeVariables.delta=now
    TimeVariables.delta_ref=now
    TimeVariables._game_clock_running=True
def update():
    '''handles basic updating functions on a per-frame basis
    independent of processor speed.

    This should be placed in the main game loop.
    '''
    game_clock_update()
    delta_update()

def start_clock():
    TimeVariables._game_clock_running=True

def stop_clock():
    TimeVariables._game_clock_running=False

def run_time():
    return time.time()-TimeVariables.game_start

def game_clock(*args):
    return TimeVariables.game_time

def game_clock_update():
    if TimeVariables._game_clock_running:
        TimeVariables.game_time=time.time()-TimeVariables.game_time_ref
    else:
        TimeVariables.game_time_ref=time.time()-TimeVariables.game_time

def delta():
    return TimeVariables.delta

def delta_update():
    if TimeVariables._game_clock_running:
        TimeVariables.delta=time.time()-TimeVariables.delta_ref
        TimeVariables.delta_ref=time.time()
    else:
        TimeVariables.delta_ref+=time.time()-TimeVariables.delta_ref

