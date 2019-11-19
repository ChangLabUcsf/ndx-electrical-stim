# -*- coding: utf-8 -*-
from datetime import datetime
import os
import unittest
import numpy as np
from pynwb import NWBFile, NWBHDF5IO
from ndx_electrical_stim import StimSeries

class StimSeriesTest(unittest.TestCase):
    def setUp(self):
        self.nwbfile = NWBFile('description', 'id', datetime.now().astimezone())
        device = self.nwbfile.create_device('device_test')
        group = self.nwbfile.create_electrode_group(
                name='electrodes',
                description='label',
                device=device,
                location='brain')

        for _ in range(3):
            self.nwbfile.add_electrode(x=np.nan, y=np.nan, z=np.nan, imp=np.nan,
                                       location='', filtering='', group=group)

        # Make a 300 timepoint waveform time series for 2 electrodes (one
        # cathode, and one anode).
        self.current_data = np.random.randn((300, 2))

    def test_init_stim_series(self):
        pass

    # Copied from ndx-ecog
    # def test_init_ecog_subject(self):
    #     cortical_surfaces = CorticalSurfaces()
    #     cortical_surfaces.create_surface('test', vertices=self.vertices, faces=self.faces)
    #     self.nwbfile.subject = ECoGSubject(subject_id='id', cortical_surfaces=cortical_surfaces)
    #     np.testing.assert_allclose(self.nwbfile.subject.cortical_surfaces.surfaces['test'].vertices, self.vertices)
    #     np.testing.assert_allclose(self.nwbfile.subject.cortical_surfaces.surfaces['test'].faces, self.faces)
    # def test_add_cs_to_ecog_subject(self):
    #     cortical_surfaces = CorticalSurfaces()
    #     cortical_surfaces.create_surface('test', vertices=self.vertices, faces=self.faces)
    #     self.nwbfile.subject = ECoGSubject()
    #     self.nwbfile.subject.cortical_surfaces = cortical_surfaces
    # def test_io(self):
    #     cortical_surfaces = CorticalSurfaces()
    #     cortical_surfaces.create_surface('test', vertices=self.vertices, faces=self.faces)
    #     self.nwbfile.subject = ECoGSubject(subject_id='id', cortical_surfaces=cortical_surfaces)
    #     with NWBHDF5IO('test.nwb', 'w') as io:
    #         io.write(self.nwbfile)
    #     with NWBHDF5IO('test.nwb', 'r') as io:
    #         nwbfile = io.read()
    #         np.testing.assert_allclose(
    #             self.nwbfile.subject.cortical_surfaces.surfaces['test'].vertices,
    #             nwbfile.subject.cortical_surfaces.surfaces['test'].vertices)
    #         np.testing.assert_allclose(
    #             self.nwbfile.subject.cortical_surfaces.surfaces['test'].faces,
    #             nwbfile.subject.cortical_surfaces.surfaces['test'].faces)
    #     os.remove('test.nwb')