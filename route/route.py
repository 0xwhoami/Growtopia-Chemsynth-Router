#!/usr/bin/env python

"""
Copyright (c) 2020-End_Of_Life
See the file 'LICENSE' for copying permission
"""

# absolute import
from chemsynth.chempoint import ChemsynthPoint

# relative import
from .point_based import point_route
from .smart_catalyst import smart_catalyst

__all__ = ['route']

def route(dom, tar):
    '''
    return to_do_list which is list of [function, index] that will help
    '''
    # prepare
    chem = ChemsynthPoint(dom, tar)
    to_do_list = []

    # routing as possible
    while True:
        # routing
        temp = point_route(chem)
        temp += smart_catalyst(chem)

        # if route failed
        if temp == []:
            break

        # append to the to_do_list
        to_do_list += temp

    # return to_do_list
    return to_do_list
