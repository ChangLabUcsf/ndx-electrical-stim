import json
import os

from pynwb import load_namespaces, get_class
from hdmf.utils import popargs

# Set path of the namespace.yaml file to the expected install location
ndx_electrical_stim_specpath = os.path.join(
    os.path.dirname(__file__),
    'spec',
    'ndx-electrical-stim.namespace.yaml'
)

# If the extension has not been installed yet but we are running directly from
# the git repo
if not os.path.exists(ndx_electrical_stim_specpath):
    ndx_electrical_stim_specpath = os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        '..', '..', '..',
        'spec',
        'ndx-electrical-stim.namespace.yaml'
    ))

# Load the namespace
load_namespaces(ndx_electrical_stim_specpath)

# Load the class
baseStimSeries = get_class('StimSeries', 'ndx-electrical-stim')

# Use the base class to define a new __init__ with variable checks.
class StimSeries(baseStimSeries):

    def __init__(self, **kwargs):
        electrodes, data, unit, metadata = popargs(
            'electrodes', 'data', 'unit', 'metadata', kwargs)

        if unit not in ['amp', 'volt']:
            raise ValueError('Stimulation waveform unit must be "amp" or "volt".')

        # For each period of stimulation, confirm that the required
        # parameters of amplitude, pulsewidth, and frequency are defined.
        metadata_json = json.loads(metadata)
        for stim_run in metadata_json.keys():

            if 'amplitude' not in metadata_json[stim_run].keys():
                raise ValueError('Must define stimulation amplitude for {'
                                 '} metadata.'.format(stim_run))

            if 'pulse_width' not in metadata_json[stim_run].keys():
                raise ValueError('Must define stimulation pulse_width for {'
                                 '} metadata.'.format(stim_run))

            if 'frequency' not in metadata_json[stim_run].keys():
                raise ValueError('Must define stimulation frequency for {'
                                 '} metadata.'.format(stim_run))

        # Ensure that the size of the electrode region corresponds to
        #  number of waveforms.
        if data is not None:

            # Check the dimensionality of data.
            if len(data.shape) == 1:
                data_shape = 1
            else:
                data_shape = data.shape[-1]

            if data_shape != len(electrodes):
                raise ValueError('Data passed contains {} waveforms but '
                                 '{} corresponding electrode pairs '
                                 'specified'.format(data_shape,
                                                    len(electrodes)))

        # Add the kwargs.
        super(baseStimSeries, self).__init__(**kwargs)
        self.electrodes = electrodes
        self.metadata = metadata
