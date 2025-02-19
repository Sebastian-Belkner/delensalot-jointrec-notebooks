import numpy as np
import healpy as hp
import os
from os.path import join as opj

import delensalot
from delensalot.config.metamodel import DEFAULT_NotAValue as DNaV

import delensalot.core.power.pospace as pospace
from delensalot.utility.utils_hp import gauss_beam
from delensalot.config.config_helper import LEREPI_Constants as lc
from delensalot.config.metamodel.delensalot_mm_v2 import *
from plancklens import utils

delensalot_model = DELENSALOT_Model(
    defaults_to = 'default_jointrec',
    job = DELENSALOT_Job(
        jobs = ["generate_sim", "QE_lensrec", "MAP_lensrec"]
    ),
    analysis = DELENSALOT_Analysis(
        TEMP_suffix = 'jointrec4',
        key = 'pf_p',
        simidxs = np.array([0]),
        simidxs_mf = np.array([]),
        beam = 1.0,
        LM_max = (4000, 4000),
        lm_max_pri = (4200, 4200),
        lm_max_sky = (3800, 3800),
        Lmin = {'p': 2, 'w': 3, 'f': 1},
        lmin_teb = (2, 2, 200),
        transfunction_desc = 'gauss_no_pixwin',
    ),
    simulationdata = DELENSALOT_Simulation(
        flavour = 'pri',
        sec_info = {
            'lensing': {'component': ['p','w'],},
            # 'birefringence': {'component': ['f']},
        },
        obs_info = {
            'noise_info': {
                'nlev': {'P': 0.5, 'T': 0.5/np.sqrt(2)},
            },
            'transfunction': gauss_beam(1.0/180/60 * np.pi, lmax=4096),
        },
    ),
    noisemodel = DELENSALOT_Noisemodel(
        nlev = {'P': 0.5, 'T': 0.5/np.sqrt(2)},
        geominfo = ('healpix', {'nside': 2048}),
    ),
    qerec = DELENSALOT_Qerec(
        tasks = ["calc_fields"],
        cg_tol = 1e-5,
        subtract_QE_meanfield = True,
    ),
    itrec = DELENSALOT_Itrec(
        tasks = ["calc_fields"],
        itmax = 5,
        cg_tol = 1e-7,
    ),
)