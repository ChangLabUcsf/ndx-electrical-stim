# -*- coding: utf-8 -*-
"""
Define ndx_electrical_stim (StimSeries class) for the PyNWB API.
"""
# Third party libraries
from hdmf.common import DynamicTableRegion
from hdmf.utils import docval, popargs, get_docval
from pynwb import TimeSeries, register_class


@register_class('StimSeries', 'ndx-electrical-stim')
class StimSeries(TimeSeries):
    __nwbfields__ = (
        {
            'name': 'electrodes',
            'required_name': 'electrodes',
            'doc': 'DynamicTableRegion pointer to the electrodes '
                   'corresponding to the stimulation waveforms.',
            'child': True
        },
    )

    @docval(*get_docval(TimeSeries.__init__, 'name'),
            {
                'name': 'data',
                'type': ('array_data', 'data', TimeSeries),  # required
                'shape': ((None,), (None, None)),
                'doc': 'The data this TimeSeries dataset stores. Can also '
                       'store binary data e.g. image frames'
            },
            {
                'name': 'electrodes',
                'type': DynamicTableRegion,  # required
                'doc': 'the table region corresponding to the electrodes '
                       'receiving the stimulation waveforms.'
            },
            {
                'name': 'unit',
                'type': str,  # required
                'doc': 'unit for the stimulation waveform',
                'default': 'amp'
            },
            *get_docval(TimeSeries.__init__, 'resolution', 'conversion',
                        'timestamps', 'starting_time', 'rate', 'comments',
                        'description', 'control', 'control_description'))
    def __init__(self, **kwargs):
        name, electrodes, data, unit = popargs(
            'name', 'electrodes', 'data', 'unit', kwargs)

        # Ensure that the units are correct.
        if unit not in ['amp', 'volt']:
            raise ValueError('Unit must be "amp" or "volt".')

        super(StimSeries, self).__init__(name, data, unit, **kwargs)
        self.electrodes = electrodes
