# Shared Near Infrared Spectroscopy Format (SNIRF)

This repository stores the Shared Near Infrared Spectroscopy Format (SNIRF).  
SNIRF is designed by the community in an effort to facilitate sharing and analysis of NIRS data.

View the most recent release version of the format: [here](https://github.com/fNIRS/snirf/blob/v1.1/snirf_specification.md).  
View the development version of the format: [here](snirf_specification.md).   


## Validating SNIRF files

[pysnirf2](https://pypi.org/project/pysnirf2/) is the currently actively maintained tool for reading, writing and validating SNIRF files. pysnirf2 can be easily installed in a Python 3 environment using pip.

See the [pysnirf2 README](https://github.com/BUNPC/pysnirf2#validating-a-snirf-file) for usage examples.

## User Information

To browse the latest version of the SNIRF Specification document, you may click on 
[this link](snirf_specification.md). A history of changes to the specification and
information on released versions is available in the [change log](CHANGELOG.md).

The following software packages support reading and/or writing SNIRF files.

| Software       |Platform|                   URL                        |
|----------------|--------|----------------------------------------------|
| Homer2         | MATLAB | https://homer-fnirs.org                      |
| Homer3         | MATLAB | https://github.com/BUNPC/Homer3              |
| NIRS-Toolbox   | MATLAB | https://github.com/huppertt/nirs-toolbox     |
| FieldTrip      | MATLAB | https://www.fieldtriptoolbox.org             |
| NIRStorm       | MATLAB | https://github.com/Nirstorm/nirstorm         |
| MNE-Python     | Python | https://mne.tools                            |
| pysnirf2       | Python | https://pypi.org/project/pysnirf2/           |
| ICNNA          | MATLAB | https://github.com/forihuelaespina/ICNNA     |


The following vendors export data in SNIRF format.

| Vendor         |              URL                 |
|----------------|----------------------------------|
| NIRx           | https://nirx.net                 |
| Kernel         | https://www.kernel.com           |
| Cortivision    | https://www.cortivision.com      |
| Gowerlabs      | https://www.gowerlabs.co.uk      |
| Artinis        | https://www.artinis.com          |


## Governance

SNIRF is a community guided project with oversight from academic and industry partners.
The governance of the project is described in the [government.md](GOVERNMENT.md) document.
The current steering committee is:

| Name           |          Institution             |
|----------------|----------------------------------|
| David Boas     | Boston University                |
| Robert Luke    | AE Studio                        |
| Samuel Powell  | Gowerlabs                        |
| Jörn Horschig  | Artinis Medical Systems B.V. |

We are in the process of establishing the maintainers team,
please contact us if you would like to contribute.


## Development Information

Please read the procedure for [making contributions to SNIRF](CONTRIBUTING.md).

To download the latest specification document alone click on this
[download link](https://github.com/fNIRS/snirf/archive/master.zip),
or use the below command
```
   git clone https://github.com/fNIRS/snirf.git
```

You may optionally download the sample data, or a parser that you need. To do so, you need
to first `cd` the folder where the snirf repository was cloned, and then run the below commands
```
   cd snirf                                # cd the folder where the repo was cloned
   git submodule update samples            # checkout the sample data files (needs >240MB)
   git submodule update lib/matlab/easyh5  # checkout a specific matlab parsers, or
   git submodule update --init --remote    # checkout all components
```

To download the entire package at once, including the latest specification document, 
sample files and all currently supported parsers, you should use the below command
```
   git clone --recursive https://github.com/fNIRS/snirf.git
```


### Sample files and parsers

The latest versions of the individual submodules, including sample data and parsers, can also 
be downloaded by clicking on the the below links. After download, please follow the README
file in each package for instructions on how to use.

| Submodule      |                               URL                         |
|----------------|-----------------------------------------------------------|
| BIDS sample data | https://github.com/rob-luke/BIDS-NIRS-Tapping/archive/master.zip |
| Artinis sample data | https://github.com/Artinis-Medical-Systems-B-V/snirf_data_example |
| EasyH5 Toolbox | https://github.com/fangq/easyh5/archive/v0.8.tar.gz       |
| JSNIRF Toolbox | https://github.com/fangq/jsnirfy/archive/v0.4.tar.gz      |

[This page](https://github.com/BUNPC/Homer3/wiki/Standalone-SNIRF-loading-and-saving)
provides examples of how to work with SNIRF files using the
[Homer3](https://github.com/BUNPC/Homer3) interface.
