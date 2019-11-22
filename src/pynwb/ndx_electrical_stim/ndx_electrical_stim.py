# # -*- coding: utf-8 -*-
# """
# Define ndx_electrical_stim (StimSeries class) for the PyNWB API.
# """
# # Standard libraries
# import json
#
# # Third party libraries
# from hdmf.common import DynamicTableRegion
# from hdmf.utils import docval, popargs, get_docval
# from pynwb import TimeSeries, register_class
#
#
# @register_class('StimSeries', 'ndx-electrical-stim')
# class StimSeries(TimeSeries):
#     __nwbfields__ = (
#         {
#             'name': 'electrodes',
#             'required_name': 'electrodes',
#             'doc': 'DynamicTableRegion pointer to the '
#                    'bipolar electrode pairs corresponding to the '
#                    'stimulation waveforms.',
#             'child': True
#         },
#         {
#             'name': 'metadata',
#             'required_name': 'metadata',
#             'doc': 'JSON serialized metadata for creating the recorded '
#                    'stimulation waveform.',
#             'child': True
#         }
#     )
#
#     @docval(*get_docval(TimeSeries.__init__, 'name'),
#             {
#                 'name': 'data',
#                 'type': ('array_data', 'data', TimeSeries),
#                 'shape': ((None,), (None, None)),
#                 'doc': 'The data this TimeSeries dataset stores. Can also '
#                        'store binary data e.g. image frames. Data should be '
#                        'of shape (n_time,) for a single electrode pair or of '
#                        '(n_time, n_electrodes).',
#                 'default': None
#             },
#             {
#                 'name': 'electrodes',
#                 'type': DynamicTableRegion,
#                 'doc': 'the table region pointing to the bipolar electrode '
#                        'pairs corresponding to the stimulation waveform.',
#                 'default': None
#             },
#             {
#                 'name': 'unit',
#                 'type': str,
#                 'doc': 'unit for the stimulation waveform',
#                 'default': 'amp'
#             },
#             {
#                 'name': 'metadata',
#                 'type': str,
#                 'doc': 'JSON serialized metadata for creating the recorded '
#                        'stimulation waveform',
#                 'default': None
#             },
#             *get_docval(TimeSeries.__init__, 'resolution', 'conversion',
#                         'timestamps', 'starting_time', 'rate', 'comments',
#                         'description', 'control', 'control_description'))
#     def __init__(self, **kwargs):
#         name, electrodes, data, unit, metadata = popargs(
#             'name', 'electrodes', 'data', 'unit', 'metadata', kwargs)
#
#         # Ensure that the units are correct.
#         if unit not in ['amp', 'volt']:
#             raise ValueError('Stimulation waveform unit must be "amp" or '
#                              '"volt".')
#         #
#         # print(unit)
#         #
#         # # For each period of stimulation, confirm that the required
#         # # parameters of amplitude, pulsewidth, and frequency are defined.
#         # metadata_json = json.loads(metadata)
#         # for stim_run in metadata_json.keys():
#         #
#         #     if 'amplitude' not in metadata_json[stim_run].keys():
#         #         raise ValueError('Must define stimulation amplitude for {'
#         #                          '} metadata.'.format(stim_run))
#         #
#         #     if 'pulse_width' not in metadata_json[stim_run].keys():
#         #         raise ValueError('Must define stimulation pulse_width for {'
#         #                          '} metadata.'.format(stim_run))
#         #
#         #     if 'frequency' not in metadata_json[stim_run].keys():
#         #         raise ValueError('Must define stimulation frequency for {'
#         #                          '} metadata.'.format(stim_run))
#         #
#         # # Ensure that the size of the electrode region corresponds to
#         # #  number of waveforms.
#         # if data is not None:
#         #     if data.shape[-1] != len(electrodes):
#         #         raise ValueError('Data passed contains {} waveforms but '
#         #                          '{} corresponding electrode pairs '
#         #                          'specified'.format(data.shape[-1],
#         #                                             len(electrodes)))
#
#         super(StimSeries, self).__init__(name, data, unit, **kwargs)
#         self.electrodes = electrodes
#         self.metadata = metadata
