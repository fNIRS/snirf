# Change Log For The SNIRF File Format

SNIRF uses the [Semantic Versioning](https://semver.org) scheme.


### `1.0.1` In development

* Add dataUnit to indexed groups aux and measurementList
* Uses of the word "numerical" were replaced with "numeric" for consistency.
* stim/data was incorrectly described as `[<f>,...]+` in the table when it should be `[[<f>,...]]+`
* aux/dataTimeSeries was incorrectly described as `[[<f>,...]]+` in the table when it should be `[<f>,...]+`
* aux/dataTimeSeries and aux/time were described as `numeric` in the document when they should be `1-D numeric array`
* probe/detectorPos2D was described as `numeric` in the document when it should be `2-D array`
* Added "Data format" section
* Specified that non-array fields must be saved using scalar dataspaces, and that array fields must be saved using simple dataspaces of the specified rank
* Specified that all strings must be saved in a variable length format
* Added writing code samples
* Removed ambiguity in the units of the `nirs(i)/data(j)/measurementList(k)/sourcePower` field, which were defined as both being in mW, and arbitrary. Only the latter definition is retained.
* Changed `/nirs(i)/data(j)/time` and `/nirs(i)/aux(j)/time` to specify the variable be stored as a rank-1 array, rather than a rank-2 array with a singleton trailing dimension.
* Specified that `probe/sourceLabels` is 2D string array. In wavelength-less case, spec describes 2nd dimension of 1
* Specified that `aux{i}/dataTimeSeris` is a 2D array. Multiple channels of data can be present, otherwise 2nd dimension should be 1.
* Add language preventing `metaDataTags` sub-groups
* Add notice that the summary table is intended to be machine-readable
  
### `1.0` (September 23 2021)

[View this version of the specification](https://github.com/fNIRS/snirf/blob/v1.0/snirf_specification.md)  

* General clarification of wording throughout the specification.
* Remove sourcePos, detectorPos, and landmarkPos.
* Add wavelengthActual and wavelengthEmissionActual.
* Change stim/data names from attribute to regular dataset.
* Require either 2D or 3D positions, not just 2D.
* Add list of supported aux name values including accel, gyro, magn
* Add datatypes for processed TD moment data.

### `1.0 - Draft 3` (November 11 2019)

[View this version of the specification](https://github.com/fNIRS/snirf/tree/da550abf7ec70084e31ba428df09a9dcbf3e6036)  

* Initial version with change log.
