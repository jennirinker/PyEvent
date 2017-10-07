# -*- coding: utf-8 -*-
"""Tests for core module

Author
------
Jenni Rinker
GitHub: @jennirinker
"""
import os

import pandas as pd
import pytest

from pyevent.core import EventData, PyEventError


_kinds = ['task', 'vol']
_csv_keys = {'task': 'task',
             'vol': 'volunteer'}
_paths = {'task': os.path.join('data', 'demo_task_list.csv'),
          'vol': os.path.join('data', 'demo_volunteer_list.csv')}
_shapes = {'task': pd.read_csv(_paths['task']).shape,
           'vol': pd.read_csv(_paths['vol']).shape}

def test_empty_event_data():
    """creating an empty event
    """
    val = None  # given
    event_data = EventData()  # when
    assert event_data._vol_df == val  # then...
    assert event_data._task_df == val


def test_error_bad_path():
    """PyEventError raised with bad paths
    """
    bad_paths = [1234, 'beafrecw.rsw']  # list of bad paths
    for bad_path in bad_paths:
        with pytest.raises(PyEventError):  # just task path bad
            EventData(task_path=bad_path)
        with pytest.raises(PyEventError):  # just vol path bad
            EventData(vol_path=bad_path)
        with pytest.raises(PyEventError):  # both paths bad
            EventData(task_path=bad_path, vol_path=bad_path)

def test_read_csv():
    """load volunteer or task list
    """
    # ==== method 1: empty, then read ====
    event_data = EventData()
    for kind in _kinds:
        event_data.read_csv(_paths[kind])
        assert event_data[f'_{kind}_df'].shape == _shapes[kind]
    # ==== method 2: initialize full ====
    event_data2 = EventData(task_path=_paths['task'], vol_path=_paths['vol'])
    for kind in _kinds:
        assert event_data2[f'_{kind}_df'].shape == _shapes[kind]

def test_to_csv():
    """writing task and volunteer csvs
    """
    event_data = EventData(task_path=_paths['task'], vol_path=_paths['vol'])
    test_name = 'test'
    # ==== method 1: default is save here ====
    test_dir = '.'
    event_data.to_csv(test_name)  # default directory
    for kind in _kinds:
        csv_key = _csv_keys[kind]
        csv_path = os.path.join(test_dir, f'{test_name}_{csv_key}_list.csv')
        reloaded_df = pd.read_csv(csv_path)
        assert reloaded_df.shape == _shapes[kind]
        os.remove(csv_path)
    # ==== method 2: save to ./data/ ====
    test_dir = 'data'
    event_data.to_csv(test_name, dir_path=test_dir)
    for kind in _kinds:
        csv_key = _csv_keys[kind]
        csv_path = os.path.join(test_dir, f'{test_name}_{csv_key}_list.csv')
        reloaded_df = pd.read_csv(csv_path)
        assert reloaded_df.shape == _shapes[kind]
        os.remove(csv_path)

def test_get_tasks_raise_error():
    """raise an error when a bad date is passed in
    """
    event_data = EventData(task_path=_paths['task'], vol_path=_paths['vol'])
    with pytest.raises(PyEventError):  # just start is bad
        event_data.get_tasks(start=42, end='2017-07-31 12:00')
    with pytest.raises(PyEventError):  # just end is bad
        event_data.get_tasks(start='2017-07-31 12:00', end=42)
    with pytest.raises(PyEventError):  # both are bad
        event_data.get_tasks(start=42, end=42)

def test_get_tasks_filter_event():
    """filter tasks by event name
    """
    event, n_rows = 'final_party', 1  # event and no. associated tasks
    event_data = EventData(task_path=_paths['task'], vol_path=_paths['vol'])
    filt_df = event_data.get_tasks(event=event)
    assert filt_df.shape[0] == n_rows

def test_get_tasks_filter_category():
    """filter tasks by category
    """
    category, n_rows = 'urban', 1  # category and no. associated tasks
    event_data = EventData(task_path=_paths['task'], vol_path=_paths['vol'])
    filt_df = event_data.get_tasks(category=category)
    assert filt_df.shape[0] == n_rows

def test_get_tasks_filter_time():
    """filte tasks by time range
    """
    start, end, n_rows = '2017-07-31 08:00', '2017-07-31 12:00', 3
    event_data = EventData(task_path=_paths['task'], vol_path=_paths['vol'])
    filt_df = event_data.get_tasks(start=start, end=end)
    assert filt_df.shape[0] == n_rows
    