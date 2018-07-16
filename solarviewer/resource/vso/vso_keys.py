entries = {}
entries["INSTRUMENT"] = sorted(
    ['AIA', 'HMI', 'chp', 'dpm', 'mk4', 'BCS', 'HXT', 'WBS', 'SXT', 'Spectroheliograph', 'Spectromagnetograph',
     '512-channel Magnetograph', 'Solar FTS Spectrometer', 'VSM', 'OVSA', 'CDS', 'CELIAS', 'COSTEP', 'EIT', 'ERNE',
     'GOLF', 'LASCO', 'MDI', 'SUMER', 'SWAN', 'UVCS', 'VIRGO', 'Big Bear', 'Udaipur', 'Mauna Loa', 'Learmonth',
     'El Teide', 'Cerro Tololo', 'MOTH', 'MOF/60', 'Tenerife', 'SXI-0', 'RHESSI'])
entries["PROVIDER"] = sorted(['HANET', 'HAO', 'JSOC', 'KIS', 'KSO', 'LASP', 'LMSAL', 'MSFC', 'MWSPADP' 'MSU', 'NSO',
                              'OVRO', 'SDAC', 'SHA', 'OBSPM', 'NGDC', 'LSSP', 'SDAC_2', 'OMP', 'ROB', 'SAO', 'SSC'])
entries["SOURCE"] = sorted(
    ['BBSO', 'KANZ', 'OACT', 'OBSPM', 'YNAO', 'MLSO', 'SDO', 'YOHKOH', 'Evans', 'KPVT', 'McMath', 'SOLIS', 'OVRO',
     'SOHO', 'GONG', 'JSPO', 'MtWilson', 'TON', 'Nancay', 'Pic du Midi', 'GOES-12', 'RHESSI', 'TRACE'])
entries["PHYSOBS"] = sorted(
    ['intensity', 'equivalent_width', 'polarization_vector', 'LOS_magnetic_field', 'vector_magnetic_field',
     'LOS_velocity', 'vector_velocity', 'wave_power', 'wave_phase', 'oscillation_mode_parameters', 'number_density',
     'particle_flux', 'particle_velocity', 'thermal_velocity', 'composition'])


def instruments():
    return entries["INSTRUMENT"]


def providers():
    return entries["PROVIDER"]


def sources():
    return entries["SOURCE"]


def phys_obs():
    return entries["PHYSOBS"]
