# -*- coding: utf-8 -*-
"""
Define ndx_electrical_stim (StimSeries class) for the PyNWB API.
"""
# Standard libraries

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

    @docval(*get_docval(TimeSeries.__init__, 'name'),
            {
                'name': 'data',
                'type': ('array_data', 'data', TimeSeries),
                'shape': ((None,), (None, None)),
                'doc': 'The data this TimeSeries dataset stores. Can also '
                       'store binary data e.g. image frames'
            },
            {
                'name': 'electrodes',
                'type': DynamicTableRegion,
                'doc': 'the table region pointing to the bipolar electrode '
                       'pairs corresponding to the stimulation waveform.'
            },
            {
                'name': 'unit',
                'type': str,
                'doc': 'unit for the stimulation waveform',
                'default': 'amp'
            },
            {
                'name': 'metadata',
                'type': 'bytes',
                'doc': 'JSON serialized metadata for creating the recorded '
                       'stimulation waveform',
                'default': None
            },
            *get_docval(TimeSeries.__init__, 'resolution', 'conversion',
                        'timestamps', 'starting_time', 'rate', 'comments',
                        'description', 'control', 'control_description'))
    def __init__(self, **kwargs):
        name, electrodes, data, unit, metadata = popargs(
            'name', 'electrodes', 'data', 'unit', 'metadata', kwargs)

        # Ensure that the units are correct.
        if unit not in ['amp', 'volt']:
            raise ValueError('Stimulation waveform unit must be "amp" or '
                             '"volt".')

        # For each period of stimulation, confirm that the required
        # parameters of amplitude, pulsewidth, and frequency are defined.
        # for stim_run in metadata.keys():
        #
        #     if 'amplitude' not in metadata[stim_run].keys():
        #         raise ValueError('Must define stimulation amplitude for {'
        #                          '}.'.format(stim_run))
        #
        #     if 'pulse_width' not in metadata[stim_run].keys():
        #         raise ValueError('Must define stimulation pulse_width for {'
        #                          '}.'.format(stim_run))
        #
        #     if 'frequency' not in metadata[stim_run].keys():
        #         raise ValueError('Must define stimulation frequency for {'
        #                          '}.'.format(stim_run))

        # TODO: ensure that the size of the electrode region corresponds to
        #  number of waveforms?

        super(StimSeries, self).__init__(name, data, unit, **kwargs)
        self.electrodes = electrodes
        # self.metadata = metadata

