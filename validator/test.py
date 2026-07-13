from snirf_schema import read_snirf


filename = "simple_probe_valid.snirf"

snirf = read_snirf(filename, warnings=True)

snirf.save('new_'+filename)
