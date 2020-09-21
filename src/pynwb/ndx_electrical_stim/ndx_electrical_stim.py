# -*- coding: utf-8 -*-
"""
Define StimSeries & StimTable classes for the PyNWB API.
"""
import warnings

from hdmf.common import DynamicTableRegion
from hdmf.common.io.table import DynamicTableMap
from hdmf.utils import popargs, get_docval, docval
from ndx_bipolar_scheme import BipolarSchemeTable
from pynwb import TimeSeries, register_class
from pynwb import register_map
from pynwb.epoch import TimeIntervals


@register_class('StimTable', 'ndx-electrical-stim')
class StimTable(TimeIntervals):
    """
    Parameters corresponding to events of stimulation with indicated bipolar
    pairs of electrodes.
    """

    # TODO: optional time_series ObjectReference to the StimSeries
    __columns__ = (
        {
            'name': 'start_time',
            'description': 'Start time of stimulation, in seconds',
            'required': True
        },
        {
            'name': 'stop_time',
            'description': 'Stop time of stimulation, in seconds',
            'required': True
        },
        {
            'name': 'frequency',
            'description': 'Frequency of stimulation waveform, in Hz',
            'required': True
        },
        {
            'name': 'amplitude',
            'description': 'Amplitude of stimulation waveform, in meters',
            'required': True
        },
        {
            'name': 'pulse_width',
            'description': 'Pulse width of stimulation waveform, '
                           'in seconds/phase',
            'required': True
        },
        {
            'name': 'bipolar_pair',
            'description': 'The bipolar pair of electrodes used for this '
                           'stimulation run.',
            'required': True,
            'table': True
        }
    )

    @docval(
        {
            'name': 'name',
            'type': str,
            'doc': 'Name of this StimTable',
            'default': 'StimTable'
        },
        {
            'name': 'description',
            'type': str,
            'doc': 'Description of what is in this StimTable',
            'default': 'stimulation parameters'
        },
        {
            'name': 'bipolar_table',
            'type': BipolarSchemeTable,
            'doc': 'The table of bipolar electrode pairs that the '
                   '*bipolar_pair* column indexes',
            'default': None
        },
        *get_docval(TimeIntervals.__init__, 'id', 'columns', 'colnames')
    )
    def __init__(self, **kwargs):
        bipolar_table = popargs('bipolar_table', kwargs)
        super(StimTable, self).__init__(**kwargs)
        self.bipolar_table = bipolar_table

    @docval(
        {
            'name': 'start_time',
            'type': float,
            'doc': 'the start time of the stimulation run',
        },
        {
            'name': 'stop_time',
            'type': float,
            'doc': 'the stop time of the stimulation run',
        },
        {
            'name': 'frequency',
            'type': float,
            'doc': 'the frequency of the stimulation waveform',
        },
        {
            'name': 'amplitude',
            'type': float,
            'doc': 'the amplitude of the stimulation waveform',
        },
        {
            'name': 'pulse_width',
            'type': float,
            'doc': 'the pulse width of the stimulation waveform',
        },
        allow_extra=True
    )
    def add_run(self, **kwargs):
        """
        Add a stimulation parameters for a specific run.
        """
        super(StimTable, self).add_interval(**kwargs)
        bipolar_col = self['bipolar_pair']
        if bipolar_col.table is None:
            if self.bipolar_table is None:
                nwbfile = self.get_ancestor(data_type='NWBFile')
                try:
                    bipolar_col.table = nwbfile.lab_meta_data['ecephys_ext'].bipolar_scheme_table
                except KeyError:
                    warnings.warn('Reference to BipolarSchemeTable that '
                                  'does not yet exist.')
            else:
                bipolar_col.table = self.bipolar_table


@register_class('StimSeries', 'ndx-electrical-stim')
class StimSeries(TimeSeries):
    """
    Stores the recorded waveform from stimulation using bipolar pairs of
    electrodes. The waveform is stored in Amperes.
    """

    # TODO: is the 'doc' here unecessary with docval?
    __nwbfields__ = (
        {
            'name': 'bipolar_electrodes',
            'required_name': 'bipolar_electrodes',
            'doc': 'DynamicTableRegion pointer to the '
                   'bipolar electrode pairs corresponding to the '
                   'stimulation waveforms.',
            'child': True
        },
    )

    @docval(
        {
            'name': 'name',
            'type': str,
            'doc': 'Name of this StimSeries dataset',
            'default': 'StimSeries'
        },
        *get_docval(TimeSeries.__init__, 'data'),
        {
            'name': 'bipolar_electrodes',
            'type': DynamicTableRegion,
            'doc': 'DynamicTableRegion pointer to the bipolar electrode '
                   'pairs corresponding to the stimulation waveforms.'
        },
        *get_docval(TimeSeries.__init__, 'resolution', 'conversion',
                    'timestamps', 'starting_time', 'rate', 'comments',
                    'description', 'control', 'control_description')
    )
    def __init__(self, **kwargs):
        name, data, bipolar_electrodes = popargs('name',
                                                 'data',
                                                 'bipolar_electrodes',
                                                 kwargs)

        super(StimSeries, self).__init__(name, data, 'amperes', **kwargs)
        self.bipolar_electrodes = bipolar_electrodes


## IO


@register_map(StimTable)
class StimTableMap(DynamicTableMap):
    @DynamicTableMap.object_attr("bipolar_pair")
    def bipolar_column(self, container, manager):
        ret = container.get('bipolar_pair')
        if ret is None:
            return ret
        # set the electrode table if it hasn't been set yet
        if getattr(ret, 'table', None) is None:
            ret.table = container.get_ancestor('NWBFile').lab_meta_data['ecephys_ext'].bipolar_scheme_table
        return ret