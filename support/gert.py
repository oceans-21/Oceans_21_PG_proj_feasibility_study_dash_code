# -*- coding: utf-8 -*-
"""
.. module:: Gert
    :platform: Windows 7, Python 3.7.
    :synopsis: This module holds the functions developed by Gert Wessels.
.. moduleauthor:: Gert Wessels <gwessels@csir.co.za>


"""

# import system modules here:
import datetime as dt
import pathlib as pl
import sys

# import other modules here:
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_daq as daq
import dash_table as tab
import pandas as pd
import numpy as np


# this is your class :-)
class Gert():
    """
        :synopsis: This class contains Gert's functions.

        How to instantiate this class

        >>> Gert()


        .. note::

            **The `gert###()` functions will return the Dash components that need to be displayed (where # are numbers)**.

        """

    ## functions go here:
    ###############################################
    # you can put your own functions here:
    # ...
    def i_do_something(whatever_parameters,another_param):
        """
            Purpose: Fill this in.

            :param whatever_parameters: Fill this in.
            :type whatever_parameters: str
            :param another_param: make copies of the param/type for more arguments to the functions.
            :type another_param: bool

            :returns:  None -- Fill here if something is returned.

            How to use this function

            >>> Gert.i_do_something("hello",11)


            .. note::

                You can put a not here if you want.

            """


        # please comment your codes as you code :-)
        print(whatever_parameters,another_param)

        return None

    ###############################################
    # put the functions returning Dash objects here
    # ...
    ## note it is advisable to return one object per function, eg. you have three static graphs one under the other,
    ## then have three functions that return each graph, it helps to seperate your own work flow.

    def gert(debug=False):
        """
        Purpose: Draws graph of ocean colour.

        :param path: The path with file name of the log file.
        :type path: str
        :param function: The name of the function and file currently within. Has format of file_name.py, function_name.
        :type function: str
        :keyword detail: Description of current performed activity.
        :type detail: str
        :keyword debug: Printing information for debugging purposes.
        :type debug: bool

        :returns:  None -- This function only writes/appends to log file.

        How to use this function

        >>> Gert.gert("","logging.py, logging:","This is an example log message.")


        .. note::

            This log file has a standard name called measuredLog.dat and if the file is removed, the log file will be created again.

        """

        # do your stuff here...
        the_graph = dcc.Graph(
                # id='example-graph',
                figure={
                    'data': [
                        {'x': [0, 2, 3], 'y': [40, 1, 2],
                         'type': 'bar', 'name': 'SF'},
                        {'x': [0, 2, 3], 'y': [2, 4, 5],
                         'type': 'bar', 'name': u'Montréal'},
                    ]
                }
            )



        return the_graph