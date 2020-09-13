# -*- coding: utf-8 -*-
"""
Define StimSeries & StimTable classes for the PyNWB API.
"""
# import warnings

from hdmf.common import DynamicTableRegion, DynamicTable
from hdmf.utils import popargs, get_docval, docval

from pynwb import TimeSeries, register_class
from pynwb.epoch import TimeIntervals


@register_class('StimTable', 'ndx-electrical-stim')
class StimTable(TimeIntervals):
    """
    Parameters corresponding to events of stimulation with indicated bipolar
    pairs of electrodes.
    """
    __nwbfields__ = (
        {
            'name': 'bipolar_table',
            'doc': 'BipolarSchemeTable that the bipolar_pair regions '
                   'reference.',
            'child': True
        }
    )

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
            'description': 'Pulse width of stimulation waveform, in meters',
            'required': True
        },
        {
            'name': 'bipolar_pair',
            'description': 'The bipolar pair of electrodes used for this '
                           'stimulation run.',
            'required': True#,
            # TODO: does table need to be true actually? since it's just a
            #  region
            # 'table': True
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
            'name': 'bipolar_electrode_table',
            'type': DynamicTable,
            'doc': 'The table of bipolar electrode pairs that the '
                   '*bipolar_pair* column indexes',
            'default': None
        },
        *get_docval(TimeIntervals.__init__, 'id', 'columns', 'colnames')
    )
    def __init__(self, **kwargs):
        bipolar_electrode_table = popargs('bipolar_electrode_table', kwargs)
        super(StimTable, self).__init__(**kwargs)
        self.__electrode_table = bipolar_electrode_table

    @docval(
        {
            'name': 'start_time',
            'type': float,
            'doc': 'the start time of the stimulation run',
            'default': None
        },
        {
            'name': 'stop_time',
            'type': float,
            'doc': 'the stop time of the stimulation run',
            'default': None
        },
        {
            'name': 'frequency',
            'type': float,
            'doc': 'the frequency of the stimulation waveform',
            'default': None
        },
        {
            'name': 'amplitude',
            'type': float,
            'doc': 'the amplitude of the stimulation waveform',
            'default': None
        },
        {
            'name': 'pulse_width',
            'type': float,
            'doc': 'the pulse width of the stimulation waveform',
            'default': None
        },
        {
            'name': 'bipolar_pair',
            'type': 'DynamicTableRegion',
            'doc': 'the bipolar pair of electrodes used',
            'default': None
        },
        allow_extra=True
    )
    def add_run(self, **kwargs):
        """
        Add a stimulation parameters for a specific run.
        """
        super(StimTable, self).add_interval(**kwargs)
        # if 'bipolar_pair' in self:
        #     elec_col = self['bipolar_pair'].target
        #     if elec_col.table is None:
        #         if self.__electrode_table is None:
        #             nwbfile = self.get_ancestor(data_type='NWBFile')
        #             try:
        #                 elec_col.table = nwbfile.lab_meta_data[
        #                     'ecephys_ext'].bipolar_scheme_table
        #             except KeyError:
        #                 warnings.warn('Reference to BipolarSchemeTable that '
        #                               'does not yet exist.')
        #         else:
        #             elec_col.table = self.__electrode_table


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
