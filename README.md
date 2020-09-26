# ndx-electrical-stim Extension for NWB:N

Author: Jessie R. Liu

This NWB:N extension defines `StimSeries`, a new neurodata type that extends
 `TimeSeries`, and `StimTable`, a neurodata type that extends `TimeIntervals`.
This extension applies to electrical stimulation via bipolar pairs of
 electrodes.

`StimSeries` holds stimulation waveforms that are recorded from stimulation
 and can reference bipolar pairs of electrodes using `BipolarSchemeTable
 ` from [ndx-bipolar-scheme](https://github.com/catalystneuro/ndx-bipolar-scheme).
 
`StimTable` holds stimulation parameter information for every individual run
 of stimulation in a recorded file.
The table also references which parameter combinations were used with which
 bipolar electrode pairs.
 
`StimSeries` and `StimTable` can both be used or only one or the other
, depending on what information is available from a stimulation recording
 session.
 
 
## Installation
### Python (not yet implemented in PyPI).
```bash
pip install ndx_electrical_stim
```

### Local installation.
Clone this repository and locally install with:
```bash
git clone https://github.com/ChangLabUcsf/ndx-electrical-stim.git
pip install -e ndx-electrical-stim
```

## Usage
### Python
Writing the file:
```python
import numpy as np
from ndx_bipolar_scheme import BipolarSchemeTable, EcephysExt
from ndx_electrical_stim import StimSeries, StimTable
from pynwb import NWBHDF5IO, NWBFile
from pynwb.file import DynamicTableRegion

# Create a toy NWB file.
nwbfile = NWBFile(...)

# Add some dummy electrode information to build our BipolarSchemeTable from.
device = nwbfile.create_device('first')
electrode_group = nwbfile.create_electrode_group(
    name='name',
    description='description',
    device=device,
    location='brain_area')

for _ in range(10):
    nwbfile.add_electrode(x=1.0, y=1.0, z=1.0, imp=np.nan, location='', 
                          filtering='', group=electrode_group)

# Create a BipolarSchemeTable from the electrode information. How to create
# a Bipolar Scheme Table is also shown at 
# https://github.com/catalystneuro/ndx-bipolar-scheme
bipolar_scheme_table = BipolarSchemeTable(name='bipolar_scheme_table',
                                          description='desc')

bipolar_scheme_table.add_row(anodes=[0], cathodes=[1])
bipolar_scheme_table.add_row(anodes=[0, 1], cathodes=[2, 3])
bipolar_scheme_table.anodes.table = nwbfile.electrodes
bipolar_scheme_table.cathodes.table = nwbfile.electrodes

# Add the table to the file as an EcephysExt to lab metadata.
ecephys_ext = EcephysExt(name='ecephys_ext')
ecephys_ext.bipolar_scheme_table = bipolar_scheme_table
nwbfile.add_lab_meta_data(ecephys_ext)

###### Create StimSeries ######

# Create 2 stimulation waveforms, recorded from 2 different pairs of bipolar
# electrodes.
waveform = np.random.randn(500, 2)

# Create the DynamicTableRegion of which 2 bipolar pairs from the
# BipolarSchemeTable correspond to the stimulation waveforms.
bipolar_scheme_region = DynamicTableRegion(
    name='bipolar_electrodes',
    data=np.arange(2),
    description='desc',
    table=bipolar_scheme_table)

# Create the StimSeries and add it to the file as an acquisition (since the
# waveform is recorded).
ss = StimSeries(
    name='stim',
    data=waveform,
    bipolar_electrodes=bipolar_scheme_region,
    rate=200.
)
nwbfile.add_acquisition(ss)

###### Create StimTable ######
# Define stimulation parameters.
frequencies = [10., 10.]
amplitudes = [5., 5.]
pulse_widths = [2., 3.]
other_parameter = [np.nan, np.nan]

# Instantiate the StimTable, including the BipolarSchemeTable 
# that the bipolar_pair column references.
st = StimTable(
    name='stimtable',
    description='stimulation parameters',
    bipolar_table=bipolar_scheme_table
)

# Amplitude, frequency, and pulse_width are required fields, but
# other parameter columns can also be added.
st.add_column(name='other_param',
              description='some other parameter')

# Add stimulation parameters run by run. 
# The bipolar_pair column references the rows of the BipolarSchemeTable.
for i in range(2):
    st.add_run(
        np.nan, 
        np.nan, 
        amplitude=amplitudes[i], 
        frequency=frequencies[i], 
        pulse_width=pulse_widths[i],
        other_param=other_parameter[i],
        bipolar_pair=i
    )

# Add the StimTable as an intervals object to the file.
nwbfile.add_time_intervals(st)

# Write the file.
with NWBHDF5IO('toy_file.nwb', 'w') as f:
    f.write(nwbfile)
```

Reading from file:
```python
from pynwb import NWBHDF5IO
import ndx_electrical_stim  # TODO: get the namespace to load automatically

file_io = NWBHDF5IO('toy_file.nwb', 'r', load_namespaces=True)
nwbfile = file_io.read()

# Print out the anodes for the first column of the recorded stim waveform
nwbfile.acquisition['stim'].bipolar_electrodes.to_dataframe()['anodes'].iloc[0]

# Print out the cathodes for the first column of the recorded stim waveform
nwbfile.acquisition['stim'].bipolar_electrodes.to_dataframe()['cathodes'].iloc[0]

# Seems to still have this error..
nwbfile.intervals['stimtable'].to_dataframe()['bipolar_pair'].iloc[0]

# Close the file.
file_io.close()
```
