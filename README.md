# ndx-electrical-stim Extension for NWB:N

Author: Jessie R. Liu

This NWB:N extension defines `StimSeries`, a new neurodata type that extends
 `TimeSeries`. `StimSeries` holds stimulation waveforms (`data`) and can map
  the waveforms to corresponding bipolar electrode pairs by
   `DynamicTableRegion`'s. `StimSeries` also holds the `metadata` that is
    associated with the stimulation. `metadata` is defined as a JSON
     serialized dictionary (example below).
 
 
## Installation
### Python
```bash
pip install ndx_electrical_stim
```

## Usage
### Python
write:
```python
import json
import numpy as np
from pynwb import NWBHDF5IO, NWBFile
from ndx_electrical_stim import StimSeries

# Create a toy NWB file with some electrode information.
nwbfile = NWBFile(...)

# 2 stimulation waveforms and the corresponding 2 rows from a DynamicTable.
waveform = np.random.randn(500, 2)
elec_region = nwbfile.create_electrode_table_region(
    [0, 2],
    'electrodes'
)

# Example stimulation parameters for two periods of stimulation. Required
# fields are frequency, amplitude, and pulse_width.
stim_params = {
    "run1": {
        "frequency": 10,
        "amplitude": 5,
        "pulse_width": 2
    },
    "run2": {
        "frequency": 10,
        "amplitude": 5,
        "pulse_width": 2,
        "other_param": "value"
    }
}

# JSON serialize the metadata to a string.
stim_meta = json.dumps(stim_params)

# Create the StimSeries and add to the NWB file.
ss = StimSeries(
    name='stim',
    data=waveform,
    electrodes=elec_region,
    unit='amp',
    rate=200.,
    metadata=stim_meta
)
nwbfile.add_stimulus(ss)

# Write the file.
with NWBHDF5IO('toy_file.nwb', 'w') as f:
    f.write(nwbfile)
```

read:
```python
import ndx_electrical_stim
from pynwb import NWBHDF5IO

file_io = NWBHDF5IO('toy_file.nwb', 'r')
nwbfile = file_io.read()
nwbfile.stimulus['stim']
```
