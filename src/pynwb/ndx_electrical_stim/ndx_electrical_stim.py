# -*- coding: utf-8 -*-
"""
Define StimSeries base class for the PyNWB API.
"""
# Third party libraries
from pynwb import TimeSeries, register_class


@register_class('StimSeries', 'ndx-electrical-stim')
class StimSeries(TimeSeries):
    __nwbfields__ = (
        {
            'name': 'electrodes',
            'required_name': 'electrodes',
            'doc': 'DynamicTableRegion pointer to the '
                   'bipolar electrode pairs corresponding to the '
                   'stimulation waveforms.',
            'child': True
        },
        {
            'name': 'metadata',
            'required_name': 'metadata',
            'doc': 'JSON serialized metadata for creating the recorded '
                   'stimulation waveform.',
            'child': True
        }
    )
