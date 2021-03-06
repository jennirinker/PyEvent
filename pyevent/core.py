# -*- coding: utf-8 -*-
"""Base classes used in the module

Author
------
Jenni Rinker
GitHub: @jennirinker
"""
import os

import pandas as pd


class PyEventError(ValueError):
    """Custom error class for raising gui message windows
    """
    def __init__(self, arg):
        self.strerror = arg
        self.args = {arg}


class EventData():
    """Overall class to contain event information
    """

    _task_cols = ['task_id', 'task_name', 'task_desc', 'task_start',
                  'task_end', 'event', 'category', 'num_vols', 'rsc_list',
                  'owner']  # columns in task csv
    _vol_cols = ['task_id', 'vol_id', 'vol_name',
                 'vol_contact']  # columns in volunteer csv

    def __init__(self, task_path=None, vol_path=None,
                 **kwargs):
        """Can initialized with paths to task and/or volunteer csvs
        """
        super().__init__()
        self._task_df = None
        self._vol_df = None
        if task_path:
            self.read_csv(task_path, **kwargs)
        if vol_path:
            self.read_csv(vol_path, **kwargs)

    def __getitem__(self, k):
        """make class subscriptable
        """
        return getattr(self, k)

    def get_tasks(self, event=None, category=None,
                  start='2000-01-01 00:00', end='2050-12-31 23:59'):
        """return dataframe of tasks
        """
        task_df = self._task_df  # pull out task dataframe for easier access
        task_df['task_start'] = pd.to_datetime(task_df['task_start'])
        task_df['task_end'] = pd.to_datetime(task_df['task_end'])
        if event is not None:  # filter by event
            task_df = task_df.loc[task_df.event == event]
        if category is not None:  # filter by category
            task_df = task_df.loc[task_df.category == category]
        try:  # filter by time stamp
            task_df = task_df.loc[(task_df.task_start <= end) &
                                  (task_df.task_end >= start)]
        except TypeError as e:
            raise PyEventError('Invalid start or end time')
        return task_df

    def read_csv(self, file_path, **kwargs):
        """load tasks or volunteers from csv
        """
        kwargs.pop('keep_default_na', None)
        try:
            df = pd.read_csv(file_path, keep_default_na=False,
                             **kwargs)
        except ValueError:
            raise PyEventError('Invalid file path')
        except FileNotFoundError:
            raise PyEventError('File does not exist')
        if set(df.columns.values) == set(self._vol_cols):  # volunteer df
            self._vol_df = df
        elif set(df.columns.values) == set(self._task_cols):  # task df
            self._task_df = df
        else:  # unrecognized csv
            raise PyEventError('CSV columns don\'t match volunteer' + \
                               ' or task format')

    def to_csv(self, name, dir_path='.'):
        """save tasks and volunteer csvs to directory with name

        task_name = '{name}_task_list.csv'
        vol_name = '{name}_volunteer_list.csv'
        """
        if self._task_df is not None:
            task_path = os.path.join(dir_path, f'{name}_task_list.csv')
            self._task_df.to_csv(task_path, index=False)
        if self._vol_df is not None:
            vol_path = os.path.join(dir_path, f'{name}_volunteer_list.csv')
            self._vol_df.to_csv(vol_path, index=False)
