# -*- coding: utf-8 -*-
"""
Define StimSeries base class for the PyNWB API.
"""
# Third party libraries
from pynwb import TimeSeries, register_class
from hdmf.utils import popargs


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
            'name': 'parameters',
            'required_name': 'parameters',
            'doc': 'Parameters corresponding to the stimulation waveforms.',
            'child': True
        }
    )

    # TODO: add docval here?
    def __init__(self, **kwargs):
        electrodes, parameters = popargs('electrodes', 'parameters', kwargs)

        super(StimSeries, self).__init__(**kwargs)
        self.electrodes = electrodes
        self.parameters = parameters
