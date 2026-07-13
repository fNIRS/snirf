from snirf_schema import read_snirf


filename = "simple_probe_valid.snirf"

snirf = read_snirf(filename, verbose=True)

snirf.model_dump(exclude_unset=True)
snirf.save('new_'+filename)
