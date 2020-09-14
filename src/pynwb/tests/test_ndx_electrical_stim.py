from datetime import datetime

import numpy as np
from pynwb import NWBFile, NWBHDF5IO
from ndx_electrical_stim import StimSeries

from ndx_bipolar_scheme import BipolarSchemeTable, EcephysExt
from ndx_electrical_stim import StimTable


def test_io():
    nwbfile = NWBFile('description', 'id', datetime.now().astimezone())
    device = nwbfile.create_device('device_test')
    group = nwbfile.create_electrode_group(
        name='electrodes',
        description='label',
        device=device,
        location='brain')

    for i in range(4):
        nwbfile.add_electrode(x=float(i), y=float(i), z=float(i), imp=np.nan,
                              location='', filtering='', group=group)

    bipolar_scheme_table = BipolarSchemeTable(name='bipolar_scheme_table',
                                              description='desc')

    bipolar_scheme_table.anodes.table = nwbfile.electrodes
    bipolar_scheme_table.cathodes.table = nwbfile.electrodes

    bipolar_scheme_table.add_row(anodes=[0], cathodes=[1])
    bipolar_scheme_table.add_row(anodes=[0, 1], cathodes=[2, 3])

    ecephys_ext = EcephysExt(name='ecephys_ext')
    ecephys_ext.bipolar_scheme_table = bipolar_scheme_table
    nwbfile.add_lab_meta_data(ecephys_ext)

    st = StimTable(
        name='stimtable',
        description='stimulation parameters',
        # bipolar_table=bipolar_scheme_table
    )

    # calling this before `add_run` obviates bipolar_table=bipolar_scheme_table above.
    # You can add it to the NWBFile later, but you'll need to specify bipolar_table manually

    nwbfile.add_time_intervals(st)

    frequencies = [10., 10.]
    amplitudes = [5., 5.]
    pulse_widths = [2., 3.]

    for i in range(2):
        st.add_run(
            start_time=np.nan,
            stop_time=np.nan,
            frequency=frequencies[i],
            amplitude=amplitudes[i],
            pulse_width=pulse_widths[i],
            bipolar_pair=i
        )

    with NWBHDF5IO('test_file.nwb', 'w') as io:
        io.write(nwbfile)

    # Make a 300 timepoint waveform time series for 2 electrodes (one
    # cathode, and one anode).
    current_data = np.random.randn(300, 2)
