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

    def age(self,minimum=0):
        '''age() returns the time the current Period
        has been alive in game time.

        If a minimum age is specified, a bool will be returned instead.
        if age>minimum:True
        if age<minimum:False'''
        if minimum>0:
            return True if (game_clock()-self.origin)>minimum else False
        return game_clock()-self.origin

    def frame(self,start,end=None):
        if end:
            return True if self.age()>=start and self.age()<end else False
        else:
            return True if self.age()>=start else False

    def grow(self,value):
        self.age+=value

    def regress(self,value):
        self.age-=value

    def interval(self,frequency,precision=.02):
        '''return boolean on call;True at given interval(seconds)

        only returns true within the precision range; due to the clock being 
        slightly unprecise it may miss an interval if the precision is too small.
        multiple Trues may be returned if the precision is left too large.
        '''
        return True if self.age()%frequency<=precision else False

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

