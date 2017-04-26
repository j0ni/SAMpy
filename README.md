# SAMpy
A python wrapper around NREL's SAM (System Advisory Model) SDK, which is primitive and not very pythonic

# External software requirements
* Requires and wraps around the SAM SDK, which you can download and extract from: https://sam.nrel.gov/node/69515 (the path to the SDK is a SAMpy config options).
* Uses resource from the SAM GUI tool, which you can download and install from: https://sam.nrel.gov/download

# Compatability
While it is expected to work with a range of versions, testing of this module currently covers SAM 2017.1.17 and SAM SDK 2017.1.17.r1.

# Example usage
```python
model_params = {
    'system_capacity': 4,
    'module_type': 0,
    'dc_ac_ratio': 1.1,
    'inv_eff': 96,
    'losses': 14.0757,
    'array_type': 0,
    'tilt': 10,
    'azimuth': 180,
    'gcr': 0.4,
    'adjust:constant': 0,
    "solar_resource_file": 'USA CA Oakland Metropolitan Arpt (TMY3).csv'
}

cols_of_interest = [
    'tamb',  #15.699999809265137, 16.299999237060547] + 8758
    'aoi',  #0.0, 0.0] + 8758
    'shad_beam_factor',  #1.0, 1.0] + 8758
    'sunup',  #0.0, 0.0] + 8758
    'gh',  #nan, nan] + 8758
    'dn',  #0.0, 0.0] + 8758
    'tcell',  #15.699999809265137, 16.299999237060547] + 8758
    'df',  #0.0, 0.0] + 8758
    'wspd',  #1.5, 0.0] + 8758
    'poa',  #0.0, 0.0] + 8758
    'tpoa',  #0.0, 0.0] + 8758
    'dc',  #0.0, 0.0] + 8758
    'ac',  #0.0, 0.0] + 8758
    'gen'  #0.0, 0.0] + 8758
]

sam = SAMEngine(debug=True)
results = sam.run_pvwatts(model_params=model_params)

sam.summarize( results )
resultsdf = sam.results_to_pandas(results,cols_of_interest)
print(resultsdf)
```
