
Shared Near Infrared File Format V1.0 Specification
============================================================

* **Document Version**: Draft 3
* **License**: This document is in the public domain.

## Table of Content

- [Introduction](#introduction)
- [SNIRF file specification](#snirf-file-specification)
  * [SNIRF data format summary](#snirf-data-format-summary)
  * [SNIRF data container definitions](#snirf-data-container-definitions)
- [Appendix](#appendix)
- [Acknowledgement](#acknowledgement)


## Introduction

The file format specification uses the extension `*.snirf`.  These are HDF5 
format files, renamed with the `.snirf` extension.  For a program to be 
“SNIRF-compliant”, it must be able to read and write the SNIRF file.

The HDF5 specificiations are defined by the HDF5 group and found at 
https://www.hdfgroup.org. It is expected that HDF5 future versions will remain 
backwards compatibility in the foreseeable future.

The HDF5 format defines "groups" (`H5G` class) and "datasets" (`H5D` class) 
that are the two primary data organization and storage classes used in the 
SNIRF specificiation. 


The structure of each data file has a minimum of required elements noted below. 
For each element in the data structure, one of the 4 types is assigned, 
including

- `group`: a structure containing sub-fields  (defined in the `H5G` object 
  class).  Arrays of groups, also known as the indexed-groups, are denoted 
  with numbers at the end (e.g. `/nirs/data1`, `/nirs/data2`) starting with 
  index 1.  Array indices should be contiguious with no skipped values 
  (an empty group with no sub-member is permitted).
- `string`: either a H5T.C_S1 (null terminated string) type or as ASCII encoded 8bit `char` array or UNICODE UTF-16 array.
  Defined by the `H5T.NATIVE_CHAR` or
  `H5T.H5T_NATIVE_B16` datatypes in `H5T`.  (note, at this time HDF5 does not 
  have a UTF16 native type, so 
  `H5T_NATIVE_B16` will need to be converted to/from unicode-16 within the 
  read/write code).
- `integer`: the native integer types `H5T_NATIVE_INT` `H5T` datatype (alias of 
  `H5T_STD_I32BE` or `H5T_STD_I32LE`)
- `numeric`: one of the native double or floating-point types; 
  `H5T_NATIVE_DOUBLE` or `H5T_NATIVE_FLOAT` in `H5T`. (alias of 
  `H5T_IEEE_F64BE`,`H5T_IEEE_F64LE`, i.e. "double", or `H5T_IEEE_F32BE`, 
  `H5T_IEEE_F32LE`, i.e. "float")

For `integer` and `numeric` data fields, users should use HDF5's Datatype 
Interface to query the byte-length stored in the file.

Note, native datatypes are defined by the build of the software (e.g. 
little/big endian) and are autmatically converted by the HDF5 backend for 
consistent read/write between OS platforms.

## SNIRF file specification

The SNIRF data format must have the initial `H5G` group type `"/nirs"` at the 
initial file location.

All indices (source, detector, wavelength, datatype etc) start at 1.

All SNIRF data elements are associated with a unique HDF5 location path in the
form of `/root/parent/.../name`. All paths must use `/nirs` or `/nirs#` (indexed group array).  
Note that the root '/nirs' can be either indexed or a non-indexed single entry. 

If a data element is an HDF5 group and contains multiple sub-groups, it is referred
to as an **indexed group**. Each element of the sub-group is uniquely identified 
by appending a string-formatted index (starting from 1) in the name, for example, 
`/.../name1` denotes the first sub-group of data element `name`, and `/.../name2` 
denotes the 2nd element, and so on.

In the below sections, we use the notations `"(i)"` `"(j)"` or `"(k)"` inside the 
HDF5 location paths to denote the indices of sub-elements when multiplicity presents.


### SNIRF data format summary

|  SNIRF-formatted NIRS data structure  |            Meaning of the data               |     Type       |
|---------------------------------------|----------------------------------------------|----------------|
| `/formatVersion`                      | * SNIRF format version                       |   `"s"`      * |
| `/nirs{i}`                            | * Root-group for 1 or more NIRS datasets     |   `{i}`      * |
|     `metaDataTags`                    | * Metadata headers                           |   `{.}`      * |
|        `"SubjectID"`                  | * Subject identifier                         |   `"s"`      * |
|        `"MeasurementDate"`            | * Date of the measurement                    |   `"s"`      * |
|        `"MeasurementTime"`            | * Time of the measurement                    |   `"s"`      * |
|        `"LengthUnit"`                 | * Length unit                                |   `"s"`      * |
|        `"TimeUnit"`                   | * Time unit                                  |   `"s"`      * |
|        `"SubjectName"`                | * Subject name                               |   `"s"`        |
|        `"StudyID"`                    | * Study identifier                           |   `"s"`        |
|        `"ManufacturerName"`           | * NIRS system manufacturer name              |   `"s"`        |
|        `"Model"`                      | * NIRS system model number                   |   `"s"`        |
|         ...                           | * Additional user-defined metadata entries   |                |
|     `data{i}`                         | * Root-group for 1 or more data blocks       |   `{i}`      * |
|        `dataTimeSeries`               | * Time-varying signals from all channels     | `[[<f>,...]]`* |
|        `time`                         | * Time (in `TimeUnit` defined in metaDataTag)|  `[<f>,...]` * |
|        `measurementList{i}`           | * Per-channel source-detector information    |   `{i}`      * |
|            `sourceIndex`              | * Source index for a given channel           |   `<i>`      * |
|            `detectorIndex`            | * Detector index for a given channel         |   `<i>`      * |
|            `wavelengthIndex`          | * Wavelength index for a given channel       |   `<i>`      * |
|            `dataType`                 | * Data type for a given channel              |   `<i>`      * |
|            `dataTypeLabel`            | * Data type name for a given channel         |   `"s"`        |
|            `dataTypeIndex`            | * Data type index for a given channel        |   `<i>`      * |
|            `sourcePower`              | * Source power for a given channel           |   `<f>`        |
|            `detectorGain`             | * Detector gain for a given channel          |   `<f>`        |
|            `moduleIndex`              | * Index of the parent module (if modular)    |   `<i>`        |
|     `stim{i}`                         | * Root-group for the stimulus measurements   |   `{i}`        |
|         `name`                        | * Name of the stimulus data                  |   `"s"`      + |
|         `data`                        | * Data stream of the stimulus channel        |  `[<f>,...]` + |
|     `probe`                           | * NIRS probe information                     |   `{.}`      * |
|         `wavelengths`                 | * List of wavelengths                        |  `[<f>,...]` * |
|         `wavelengthsEmission`         | * List of emission wavelengths               |  `[<f>,...]`   |
|         `sourcePos`                   | * Source 2-D positions in `LengthUnit`       | `[[<f>,...]]`* |
|         `sourcePos3D`                 | * Source 3-D positions in `LengthUnit`       | `[[<f>,...]]`  |
|         `detectorPos`                 | * Detector 2-D positions in `LengthUnit`     | `[[<f>,...]]`* |
|         `detectorPos3D`               | * Detector 3-D positions in `LengthUnit`     | `[[<f>,...]]`  |
|         `frequencies`                 | * Modulation frequency list                  |  `[<f>,...]`   |
|         `timeDelays`                  | * Time delays for gated time-domain data     |  `[<f>,...]`   |
|         `timeDelayWidths`             | * Time delay width for gated time-domain data|  `[<f>,...]`   |
|         `momentOrders`                | * Moment orders of the moment TD data        |  `[<f>,...]`   |
|         `correlationTimeDelays`       | * Time delays for DCS measurements           |  `[<f>,...]`   |
|         `correlationTimeDelayWidths`  | * Time delay width for DCS measurements      |  `[<f>,...]`   |
|         `sourceLabels`                | * String arrays specifying the source names  |  `["s",...]`   |
|         `detectorLabels`              | * String arrays specifying the detector names|  `["s",...]`   |
|         `landmarkPos`                 | * Anatomical landmark 2-D positions          | `[[<f>,...]]`  |
|         `landmarkPos3D`               | * Anatomical landmark 3-D positions          | `[[<f>,...]]`  |
|         `landmarkLabels`              | * String arrays specifying the landmark names|  `["s",...]`   |
|         `useLocalIndex`               | * If source/detector index is within a module|   `<i>`        |
|     `aux{i}`                          | * Root-group for the auxiliary measurements  |   `{i}`        |
|         `name`                        | * Name of the auxiliary channel              |   `"s"`      + |
|         `dataTimeSeries`              | * Data acquired from the auxiliary channel   | `[[<f>,...]]`+ |
|         `time`                        | * Time (in `TimeUnit`) for auxiliary data    |  `[<f>,...]` + |
|         `timeOffset`                  | * Time offset of the auxiliary channel data  |  `[<f>,...]`   |

In the above table, the notations are explained below

* `{.}` represents a simple HDF5 group
* `{i}` represents an HDF5 group with one or multiple sub-groups (i.e. an indexed-group)
* `<i>` represents an integer value
* `<f>` represents an numeric value
* `"s"` represents a string of arbitrary length
* `[...]` represents a 1-D vector, can be empty
* `[[...]]` represents a 2-D array, can be empty
* `...` (optional) additional elements similar to the previous element
* `*` in the last column indicates a required subfield
* `+` in the last column indicates a required subfield if the optional parent object is included

### SNIRF data container definitions

#### /formatVersion 
* **Presence**: required
* **Type**:  string
* **Location**: `/formatVersion`

This is a string that specifies the version of the file format.  This document 
describes format version “1.0”
	
#### /nirs(i) 
* **Presence**: required
* **Type**:  indexed group
* **Location**: `/nirs(i)`

This group stores one set of NIRS data.  This can be extended by adding the count 
number (e.g. `/nirs1`, `/nirs2`,...) to the group name. This is intended to 
allow the storage of 1 or more complete NIRS datasets inside a single SNIRF 
document.  For example, a two-subject hyperscanning can be stored using the notation
* `/nirs1` =  first subject's data
* `/nirs2` =  second subject's data
The use of a non-indexed (e.g. `/nirs/`) entry is allowed when only one entry 
is present and is assumed to be entry 1.


#### /nirs(i)/metaDataTags(j) 
* **Presence**: required 
* **Type**:  group array
* **Location**: `/nirs(i)/metaDataTags(j)`
The metaDataTag indexed array consists of key/value pairs the user 
(or manufacturer) would like to put in.  Each entry of 
the array consists of a string key and a value.

#### /nirs(i)/metaDataTags(j).key 
* **Presence**: required  as part of metaDataTags(j) 
* **Type**:  string
* **Location**: `/nirs(i)/metaDataTags(j)/key`


#### /nirs(i)/metaDataTags(j).value 
* **Presence**: required  as part of metaDataTags(j) 
* **Type**:  string or numeric
* **Location**: `/nirs(i)/metaDataTags(j)/value`

 Some possible examples:

```
['ManufacturerName','ISS'],
['Model','Imagent'],
['SubjectName', 'Pseudonym, I.M.A.'],
['DateOfBirth','20120401'],
['AcquisitionStartTime','150127.34']
['StudyID','Infant Brain Development']
['StudyDescription','We study infant cognitive development.']
['AccessionNumber','INA2S12']
['InstanceNumber',2]
['CalibrationFileName','phantomcal_121015.snirf']
```

While the name of these tags are freeform, some conventions must be followed.  Keys should 
use only alphanumeric characters with no spaces, with individual words 
capitalized.  All values will be stored as strings, How strings are converted 
into numeric values is left to whoever defines the Key.  However, it is 
required that dates be stored as `YYYYMMDD`, and clock times be stored as 
`HHMMSS.SSSS…` (24 hour format) for consistency.  Time intervals must be in 
seconds.

The following metadata tags are required:

```
SubjectID
MeasurementDate
MeasurementTime
LengthUnit    (allowed values are 'mm' and 'cm')
TimeUnit      (allowed values are 'ms' and 's')
```

The metadata tags `"StudyID"` and `"AccessionNumber"` are unique strings that 
can be used to link the current dataset to a particular study and a particular 
procedure, respectively. The `"StudyID"` tag is similar to the DICOM tag "Study 
ID" (0020,0010) and `"AccessionNumber"` is similar to the DICOM tag "Accession 
Number"(0008,0050), as defined in the DICOM standard (ISO 12052).

The metadata tag `"InstanceNumber"` is defined similarly to the DICOM tag 
"Instance Number" (0020,0013), and can be used as the sequence number to group 
multiple datasets into a larger dataset - for example, concatenating streamed 
data segments during a long measurement session.


#### /nirs(i)/data(j) 
* **Presence**: required
* **Type**:  indexed group
* **Location**: `/nirs(i)/data(j)`

This group stores one block of NIRS data.  This can be extended adding the 
count number (e.g. `data1`, `data2`,...) to the group name.  This is intended to 
allow the storage of 1 or more blocks of NIRS data from within the same `/nirs` 
entry
* `/nirs/data1` =  data block 1
* `/nirs/data2` =  data block 2	

	
#### /nirs(i)/data(j)/dataTimeSeries 
* **Presence**: required
* **Type**:  numeric 2-D array
* **Location**: `/nirs(i)/data(j)/dataTimeSeries`

This is the actual raw or processed data variable. This variable has dimensions 
of `<number of time points> x <number of channels>`. Columns in 
`dataTimeSeries` are mapped to the measurement list (`measurementList` variable 
described below).

`dataTimeSeries` can be compressed using the HDF5 filter (prebuilt filters 
`305-LZO` or `307-bzip2` supported; see 
https://support.hdfgroup.org/services/filters.html).

Chunked data is allowed to support real-time streaming of data in this array. 

#### /nirs(i)/data(j)/time 
* **Presence**: required
* **Type**:  numeric 1-D array
* **Location**: `/nirs(i)/data(j)/time`

The `time` variable. This provides the acquisition time of the measurement 
relative to the time origin.  This will usually be a straight line with slope 
equal to the acquisition frequency, but does not need to be equal spacing.  For 
the special case of equal sample spacing a shorthand `<2x1>` array is allowed 
where the first entry is the start time and the 
second entry is the sample time spacing in `TimeUnit` specified in the 
`metaDataTags`. The default time unit is in second ("s"). For example, 
a time spacing of 0.2 (s) indicates a sampling rate of 5 Hz.
		
* **Option 1** - The size of this variable is `<number of time points x 1>` and 
             corresponds to the sample time of every data point
* **Option 2**-  The size of this variable is `<2x1>` and correponds to the start
	     time and sample spacing.

Chunked data is allowed to support real-time streaming of data in this array.

#### /nirs(i)/data(j)/measurementList(k) 
* **Presence**: required
* **Type**:  indexed group
* **Location**: `/nirs(i)/data(j)/measurementList(k)`

The measurement list. This variable serves to map the data array onto the probe 
geometry (sources and detectors), data type, and wavelength. This variable is 
an array structure that has the size `<number of channels>` that 
describes the corresponding column in the data matrix. For example, the 
`measurementList3` describes the third column of the data matrix (i.e. 
`dataTimeSeries(:,3)`).

Each element of the array is a structure which describes the measurement 
conditions for this data with the following fields:


#### /nirs(i)/data(j)/measurementList(k)/sourceIndex 
* **Presence**: required
* **Type**:  integer
* **Location**: `/nirs(i)/data(j)/measurementList(k)/sourceIndex`

Index of the source.
	
#### /nirs(i)/data(j)/measurementList(k)/detectorIndex 
* **Presence**: required
* **Type**:  integer
* **Location**: `/nirs(i)/data(j)/measurementList(k)/detectorIndex`

Index of the detector.

#### /nirs(i)/data(j)/measurementList(k)/wavelengthIndex 
* **Presence**: required
* **Type**:  integer
* **Location**: `/nirs(i)/data(j)/measurementList(k)/wavelengthIndex`

Index of the wavelength.
	
#### /nirs(i)/data(j)/measurementList(k)/dataType 
* **Presence**: required
* **Type**:  integer
* **Location**: `/nirs(i)/data(j)/measurementList(k)/dataType`

Data-type identifier. See Appendix for list possible values.

#### /nirs(i)/data(j)/measurementList(k)/dataTypeLabel 
* **Presence**: optional
* **Type**:  string
* **Location**: `/nirs(i)/data(j)/measurementList(k)/dataTypeLabel`

Data-type label. Only required if dataType is "processed" (`99999`). See Appendix 
for list of possible values.

#### /nirs/measurementList(k)/dataTypeIndex 
* **Presence**: required
* **Type**:  integer
* **Location**: `/nirs(i)/data(j)/measurementList(k)/dataTypeIndex`

Data-type specific parameter indices. One use of this parameter is as a 
stimulus condition index when `measurementList(k).dataType = 99999` (i.e, `processed` and 
`measurementList(k).dataTypeLabel = 'HRF ...'` .

#### /nirs(i)/data(j)/measurementList(k)/sourcePower 
* **Presence**: optional
* **Type**:  numeric
* **Location**: `/nirs(i)/data(j)/measurementList(k)/sourcePower`

Source power in milliwatt (mW). 

#### /nirs(i)/data(j)/measurementList(k)/detectorGain 
* **Presence**: optional
* **Type**:  numeric
* **Location**: `/nirs(i)/data(j)/measurementList(k)/detectorGain`

Detector gain

#### /nirs(i)/data(j)/measurementList(k)/moduleIndex 
* **Presence**: optional
* **Type**:  integer
* **Location**: `/nirs(i)/data(j)/measurementList(k)/moduleIndex`

Index of a repeating module. 
			
For example, if `measurementList5` is a structure with `sourceIndex=2`, 
`detectorIndex=3`, `wavelengthIndex=1`, `dataType=1`, `dataTypeIndex=1` would 
imply that the data in the 5th column of the `dataTimeSeries` variable was 
measured with source #2 and detector #3 at wavelength #1.  Wavelengths (in 
nanometers) are described in the `probe.wavelengths` variable  (described 
later). The data type in this case is 1, implying that it was a continuous wave 
measurement.  The complete list of currently supported data types is found in 
the Appendix. The data type index specifies additional data type specific 
parameters that are further elaborated by other fields in the `probe` 
structure, as detailed below. Note that the Time Domain and Diffuse Correlation 
Spectroscopy data types have two additional parameters and so the data type 
index must be a vector with 2 elements that index the additional parameters.

`sourcePower` provides the option for information about the source power for 
that channel to be saved along with the data. The units are not defined, unless 
the user takes the option of using a `metaDataTag` described below to define, 
for instance, `sourcePowerUnit`. `detectorGain` provides the option for 
information about the detector gain for that channel to be saved along with the 
data.

Note:  The source indices generally refer to the optode naming (probe 
positions) and not necessarily the physical laser numbers on the instrument. 
The same is true for the detector indices.  Each source optode would generally, 
but not necessarily, have 2 or more wavelengths (hence lasers) plugged into it 
in order to calculate deoxy- and oxy-hemoglobin concentrations. The data from 
these two wavelengths will be indexed by the same source, detector, and data 
type values, but have different wavelength indices. Using the same source index 
for lasers at the same location but with different wavelengths simplifies the 
bookkeeping for converting intensity measurements into concentration changes. 
As described below, optional variables `probe.sourceLabels` and 
`probe.detectorLabels` are provided for indicating the instrument specific 
label for sources and detectors.

#### /nirs(i)/stim(j) 
* **Presence**: optional
* **Type**:  indexed group
* **Location**: `/nirs(i)/stim(j)`

This is an array describing any stimulus conditions. Each element of the array 
has the following required fields.


#### /nirs(i)/stim(j)/name 
* **Presence**: required  as part of stim(i) 
* **Type**:  string
* **Location**: `/nirs(i)/stim(j)/name`

This is a string describing the j<sup>th</sup> stimulus condition.


#### /nirs(i)/stim(j)/data 
* **Presence**: required  as part of stim(i) 
* **Type**:  numeric 2-D array
* **Location**: `/nirs(i)/stim(j)/data`

This is a three-column array specifying the stimulus time course for the 
j<sup>th</sup> condition. Each row corresponds with a specific stimulus trial. 
The three columns indicate `[starttime duration value]`.  The starttime, in 
seconds, is the time relative to the time origin when the stimulus takes on a 
value; the duration is the time in seconds that the stimulus value continues, 
and value is the stimulus amplitude.  The number of rows is not constrained. 
(see examples in the appendix).


#### /nirs(i)/probe 
* **Presence**: required 
* **Type**:  group
* **Location**: `/nirs(i)/probe `

This is a structured variable that describes the probe (source-detector) 
geometry.  This variable has a number of required fields.

#### /nirs(i)/probe/wavelengths 
* **Presence**: required 
* **Type**:  numeric 1-D array
* **Location**: `/nirs(i)/probe/wavelengths`

This field describes the wavelengths used.  This is indexed by the wavelength 
index of the measurementList variable. For example, `probe.wavelengths` = [690 
780 830]; implies that the measurements were taken at three wavelengths (690nm, 
780nm, and 830nm).  The wavelength index of 
`measurementList(k).wavelengthIndex` variable refers to this field.
`measurementList(k).wavelengthIndex` = 2 means the k<sup>th</sup> measurement 
was at 780nm.

The number of wavelengths is not limited (except that at least two are needed 
to calculate the two forms of hemoglobin).  Each source-detector pair would 
generally have measurements at all wavelengths.



#### /nirs(i)/probe/wavelengthsEmission 
* **Presence**: optional 
* **Type**:  numeric 1-D array
* **Location**: `/nirs(i)/probe/wavelengthsEmission`

This field is required only for fluorescence data types, and describes the 
emission wavelengths used.  The indexing of this variable is the same 
wavelength index in measurementList used for `probe.wavelengths` such that the 
excitation wavelength 
is paired with this emission wavelength for a given measurement.


#### /nirs(i)/probe/sourcePos 
* **Presence**: required 
* **Type**:  numeric 2-D array
* **Location**: `/nirs(i)/probe/sourcePos`

This field describes the position (in `LengthUnit` units) of each source 
optode.  This field has size `<number of sources> x 3`. For example, 
`probe.sourcePos(1,:) = [1.4 1 0]`, and `LengthUnit='cm'`; places source 
number 1 at x=1.4 cm and y=1 cm and z=0 cm.

Dimensions are relative coordinates (i.e. to some arbitrary defined origin). 

#### /nirs(i)/probe/sourcePos3D 
* **Presence**: optional 
* **Type**:  numeric 2-D array
* **Location**: `/nirs(i)/probe/sourcePos3D`

This field describes the position (in `LengthUnit` units) of each source 
optode in 3D.


#### /nirs(i)/probe/detectorPos 
* **Presence**: required 
* **Type**:  numeric
* **Location**: `/nirs(i)/probe/detectorPos`

Same as `probe.sourcePos`, but describing the detector positions.


#### /nirs(i)/probe/detectorPos3D 
* **Presence**: optional 
* **Type**:  numeric 2-D array
* **Location**: `/nirs(i)/probe/detectorPos3D`

This field describes the position (in `LengthUnit` units) of each detector 
optode in 3D.


#### /nirs(i)/probe/frequencies 
* **Presence**: optional 
* **Type**:  numeric 1-D array
* **Location**: `/nirs(i)/probe/frequencies`

This field describes the frequencies used for frequency domain measurements. 
This field is only required for frequency domain data types, and is indexed by 
`measurementList(k).dataTypeIndex`.


#### /nirs(i)/probe/timeDelays 
* **Presence**: optional 
* **Type**:  numeric 1-D array
* **Location**: `/nirs(i)/probe/timeDelays`

This field describes the time delays used for gated time domain measurements. 
This field is only required for gated time domain data types, and is indexed by 
`measurementList(k).dataTypeIndex`. The indexing of this field is paired with 
the indexing of `probe.timeDelayWidths`. 


#### /nirs(i)/probe/timeDelayWidths 
* **Presence**: optional 
* **Type**:  numeric 1-D array
* **Location**: `/nirs(i)/probe/timeDelayWidths`

This field describes the time delay widths used for gated time domain 
measurements. This field is only required for gated time domain data types, and 
is indexed by `measurementList(k).dataTypeIndex`.  The indexing of this field 
is paired with the indexing of `probe.timeDelays`.


#### /nirs(i)/probe/momentOrders 
* **Presence**: optional 
* **Type**:  numeric 1-D array
* **Location**: `/nirs(i)/probe/momentOrders`

This field describes the moment orders of the temporal point spread function 
for moment time domain measurements. This field is only required for moment 
time domain data types, and is indexed by `measurementList(k).dataTypeIndex`.  


#### /nirs(i)/probe/correlationTimeDelays 
* **Presence**: optional 
* **Type**:  numeric 1-D array
* **Location**: `/nirs(i)/probe/correlationTimeDelays`

This field describes the time delays used for diffuse correlation spectroscopy 
measurements. This field is only required for diffuse correlation spectroscopy 
data types, and is indexed by `measurementList(k).dataTypeIndex`.  The indexing 
of this field is paired with the indexing of `probe.correlationTimeDelayWidths`.


#### /nirs(i)/probe/correlationTimeDelayWidths 
* **Presence**: optional 
* **Type**:  numeric 1-D array
* **Location**: `/nirs(i)/probe/correlationTimeDelayWidth`

This field describes the time delay widths used for diffuse correlation 
spectroscopy measurements. This field is only required for gated time domain 
data types, and is indexed by `measurementList(k).dataTypeIndex`. The indexing 
of this field is paired with the indexing of `probe.correlationTimeDelays`.  


#### /nirs(i)/probe/sourceLabels 
* **Presence**: optional 
* **Type**:  string array
* **Location**: `/nirs(i)/probe/sourceLabels(j)`

This is a string array providing user friendly or instrument specific labels 
for each source. Each element of the array must be a unique string among both 
`probe.sourceLabels` and `probe.detectorLabels`.This can be of size `<number 
of sources>x 1` or `<number of sources> x <number of 
wavelengths>`. This is indexed by `measurementList(k).sourceIndex` and 
`measurementList(k).wavelengthIndex`.


#### /nirs(i)/probe/detectorLabels 
* **Presence**: optional 
* **Type**:  string array
* **Location**: `/nirs(i)/probe/detectorLabels(j)`

This is a string array providing user friendly or instrument specific labels 
for each detector. Each element of the array must be a unique string among both 
`probe.sourceLabels` and `probe.detectorLabels`. This is indexed by 
`measurementList(k).detectorIndex`.
	

#### /nirs(i)/probe/landmarkPos 
* **Presence**: optional 
* **Type**:  numeric 2-D array
* **Location**: `/nirs(i)/probe/landmarkPos`

This is a 2-D array storing the neurological landmark positions measurement 
from 3-D digitization and tracking systems to facilitate the registration and 
mapping of optical data to brain anatomy. This array should contain a minimum 
of 3 columns, representing the x, y and z coordinates of the digitized landmark 
positions. If a 4th column presents, it stores the index to the labels of the 
given landmark. Label names are stored in the `probe.landmarkLabels` subfield. 
An label index of 0 refers to an undefined landmark. 


#### /nirs(i)/probe/landmarkPos3D 
* **Presence**: optional 
* **Type**:  numeric 2-D array
* **Location**: `/nirs(i)/probe.landmarkPos3D`

This is a 2-D array storing the neurological landmark positions measurement 
from 3-D digitization and tracking systems to facilitate the registration and 
mapping of optical data to brain anatomy. This array should contain a minimum 
of 3 columns, representing the x, y and z coordinates of the digitized landmark 
positions. If a 4th column presents, it stores the index to the labels of the 
given landmark. Label names are stored in the `probe.landmarkLabels` subfield. 
An label index of 0 refers to an undefined landmark. 


#### /nirs(i)/probe/landmarkLabels(j) 
* **Presence**: optional 
* **Type**:  string array
* **Location**: `/nirs(i)/probe/landmarkLabels(j)`

This string array stores the names of the landmarks. The first string denotes 
the name of the landmarks with an index of 1 in the 4th column of 
`probe.landmark`, and so on. One can adopt the commonly used 10-20 landmark 
names, such as "Nasion", "Inion", "Cz" etc, or use user-defined landmark 
labels. The landmark label can also use the unique source and detector labels 
defined in `probe.sourceLabels` and `probe.detectorLabels`, respectively, to 
associate the given landmark to a specific source or detector. All strings are 
ASCII encoded char arrays.


#### /nirs(i)/probe/useLocalIndex 
* **Presence**: optional 
* **Type**:  integer
* **Location**: `/nirs(i)/probe/useLocalIndex`

For modular NIRS systems, setting this flag to a non-zero integer indicates 
that `measurementList(k).sourceIndex` and `measurementList(k).detectorIndex` 
are module-specific local-indices. One must also include 
`measurementList(k).moduleIndex` in the `measurementList` structure in order to 
restore the global indices of the sources/detectors.


#### /nirs(i)/aux(j) 
* **Presence**: optional 
* **Type**:  indexed group
* **Location**: `/nirs(i)/aux(j)`

This optional array specifies any recorded auxiliary data. Each element of 
`aux` has the following required fields:

#### /nirs(i)/aux(j)/name 
* **Presence**: optional; required if `aux` is used
* **Type**:  string
* **Location**: `/nirs(i)/aux(j)/name`

This is string describing the j<sup>th</sup> auxiliary data timecourse.

#### /nirs(i)/aux(j)/dataTimeSeries 
* **Presence**: optional; required if `aux` is used
* **Type**:  numeric
* **Location**: `/nirs(i)/aux(j)/dataTimeSeries`

This is the aux data variable. This variable has dimensions of `<number of 
time points> x 1`.

Chunked data is allowed to support real-time data streaming

#### /nirs(i)/aux(j)/time 
* **Presence**: optional; required if `aux` is used
* **Type**:  numeric
* **Location**: `/nirs(i)/aux(j)/time`

The time variable. This provides the acquisition time of the aux measurement 
relative to the time origin.  This will usually be a straight line with slope 
equal to the acquisition frequency, but does not need to be equal spacing. The 
size of this variable is `<number of time points> x 1` or `<2x1>` similar 
to definition of the /nirs/data/time field.

Chunked data is allowed to support real-time data streaming

#### /nirs(i)/aux(j)/timeOffset 
* **Presence**: optional 
* **Type**:  numeric
* **Location**: `/nirs(i)/aux(j)/timeOffset`

This variable specifies the offset of the file time origin relative to absolute 
(clock) time in seconds. 


## Appendix

### Supported `measurementList(k).dataType` values in `dataTimeSeries`

+ 001-100:  Raw - Continuous Wave (CW)
   - 001 - Amplitude
   - 051 - Fluorescence Amplitude

+ 101-200:  Raw - Frequency Domain (FD)
   - 101 - AC Amplitude
   - 102 - Phase
   - 151 - Fluorescence Amplitude
   - 152 - Fluorescence Phase

+ 201-300: Raw - Time Domain - Gated (TD Gated)
   - 201 - Amplitude
   - 251 - Fluorescence Amplitude
+ 301-400:  Raw - Time domain – Moments (TD Moments)
   - 301 - Amplitude
   - 351 - Fluorescence Amplitude
+ 401-500:  Raw - Diffuse Correlation Spectroscopy (DCS):
   - 401 - g2
   - 410 - BFi
+ 99999:  Processed


### Supported `measurementList(k).dataTypeLabel` values in `dataTimeSeries`

| Tag Name  |                           Meanings                               |
|-----------|------------------------------------------------------------------|
|"dOD"      | Change in optical density                                        |
|"mua"      | Absorption coefficient                                           |
|"musp"     | Scattering coefficient                                           |
|"HbO"      | Oxygenated hemoglobin (oxyhemoglobin) concentration              |
|"HbR"      | Deoxygenated hemoglobin (deoxyhemoglobin) concentration          |
|"HbT"      | Total hemoglobin concentration                                   |
|"H2O"      | Water content                                                    |
|"Lipid"    | Lipid concentration                                              |
|"BFi"      | Blood flow index                                                 |
|"HRF dOD"  | Hemodynamic response function for change in optical density      |
|"HRF HbO"  | Hemodynamic response function for oxyhemoglobin concentration    |
|"HRF HbR"  | Hemodynamic response function for deoxyhemoglobin concentration  |
|"HRF HbT"  | Hemodynamic response function for total hemoglobin concentration |
|"HRF BFi"  | Hemodynamic response function for blood flow index               |


### Examples of stimulus waveforms

Assume there are 10 time points, starting at zero, spaced 0.1s apart.  If we 
assume a stimulus to be a 0.2 second off, 0.2 second on repeating block, it 
would be specified as follows:
```
  [0.2 0.2 1.0]
  [0.6 0.2 1.0]
```

## Acknowledgement

This document was originally drafted by Blaise Frederic (bbfrederick at 
mclean.harvard.edu) and David Boas (dboas at bu.edu).

Other significant contributors to this specification include:
- Theodore Huppert (huppert1 at pitt.edu)
- Jay Dubb (jdubb at bu.edu)
- Qianqian Fang (q.fang at neu.edu)

The following individuals representing academic, industrial, software, and 
hardware interests are also contributing to and supporting the adoption of this 
specification:

### Software
- Ata Akin, Acıbadem University
- Hasan Ayaz, Drexel University
- Joe Culver, University of Washington, neuroDOT
- Hamid Deghani, University of Birmingham, NIRFAST
- Adam Eggebrecht, University of Washington, neuroDOT
- Christophe Grova, McGill University, NIRS Storm
- Felipe Orihuela-Espina, Instituto Nacional de Astrofísica, Óptica y Electrónica, ICNNA
- Luca Pollonini, Houston Methodist, Phoebe
- Sungho Tak, Korea Basic Science Institute, NIR-SPM
- Alessandro Torricelli, Politecnico di Milano
- Stanislaw Wojtkiewicz, University of Birmingham, NIRFAST

### Hardware
- Hirokazu Asaka, Hitachi
- Rob Cooper, Gower Labs Inc
- Mathieu Coursolle, Rogue
- Rueben Hill, Gower Labs Inc
- Jorn Horschig, Artinis Inc
- Takumi Inakazu, Hitachi
- Lamija Pasalic, NIRx
- Davood Tashayyod, fNIR Devices and Biopac Inc
- Hanseok Yun, OdeLab Inc
