from snirfblueprint.snirfblueprint import read_snirf


filename = "./snirfblueprint/tests/data/valid_ml.snirf"

snirf = read_snirf(filename, verbose=True)

snirf.model_dump(exclude_unset=True)
snirf.save('./test.snirf')
