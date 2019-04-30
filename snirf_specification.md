
Shared Near Infrared File Format Specification
============================================================

### License: This document is in the public domain.

The file format specification uses the extension \*.snirf.  These are HDF5 
format files, renamed with the .snirf extension.  For a program to be 
“SNIRF-compliant”, it must be able to read and write the SNIRF file.  

The HDF5 specificiations are defined by the HDF5 group and found at
https://www.hdfgroup.org.  At this time, the current version of the specificiations
is version 1.10 (Feburary 2019) as the basis for the SNIRF format.  It is expected that
HDF5 future versions will remain backwards compatibility in the foreseeable future.

The HDF5 format defines "groups" (H5G class) and "datasets" (H5D class) that are the two primary 
data organization and storage classes used in the SNIRF specificiation. 


The structure of each data file has a minimum of required elements noted below. For 
each element in the data structure, one of the 4 types is assigned, including

- `group`: a structure containing sub-fields  (defined in the H5G object class).  Arrays of groups are 
denoted with numbers at the end (e.g. /nirs/data1, /nirs/data2) starting with index 1.  Array indices 
should be contiguious with no skipped values (although an empty group with no sub-members can be used 
to "zero out" an entry).

- `string`: either ASCII encoded 8bit CHAR array or UNICODE UTF-16 array.   Defined by the H5T.NATIVE_CHAR or
H5T.H5T_NATIVE_B16 datatypes in H5T.  (note, at this time HDF5 does not have a UTF16 native type, so 
H5T_NATIVE_B16 will need to be converted to/from unicode-16 within the read/write code).  

- `integer`: the native integer types H5T.NATIVE_INT H5T datatype (alias of H5T_STD_I32BE or H5T_STD_I32LE)

- `numeric`: one of the native double or floating-point types; H5T.NATIVE_DOUBLE or H5T.NATIVE_FLOAT in H5T.  
(alias of H5T_IEEE_F64BE,H5T_IEEE_F64LE [double] or H5T_IEEE_F32BE, H5T_IEEE_F32LE [float])    		   

For `integer` and `numeric` data fields, users should use HDF5's 
Datatype Interface to query the byte-length stored in the file.

Note, native datatypes are defined by the build of the software (e.g. little/big endian) and are 
autmatically converted by the HDF5 backend for consistent read/write between OS platforms.

## SNIRF file specification

The SNIRF data format must have the initial H5G group type "/nirs" at the initial file location.


### Required fields 
<dl>
<h3> /formatVersion [Required]</h3>
<dt>formatVersion</dt><tt>[Type: string] [Location: /formatVersion ]</tt>
<dd>This is a string that specifies the version of the file format.  This 
document describes format version “1.0”</dd>
	
<h3> /nirs{0} [Required]</h3>
<dt>nirs{0}</dt><tt>[Type: indexed group] [Location: /nirs{0} where {0} is the array index] </tt>
<dd> This group stores one set of NIRS data.  This can be extended adding the count number (e.g. nirs1, nirs2,...) to the group name.  This is intended to allow the storage of 1 or more complete NIRS datasets inside the single SNIRF format.  For example, two-person hyperscanning can be stored using the notation
	/nirs1 =  first subject's data
	/nirs2 =  second subject's data
The use of a non-indexed (e.g. /nirs/) entry is allowed when only one entry is present and is assumed to be entry 1. 	
</dd>



<h3> /nirs/data{0} [Required]</h3>
<dt>data{0}</dt><tt>[Type: indexed group] [Location: /nirs/data{0} where {0} is the array index]</tt>
<dd> This group stores one block of NIRS data.  This can be extended adding the count number (e.g. data1, data2,...) to the group name.  This is intended to allow the storage of 1 or more blocks of NIRS data from within the same /nirs entry
	/nirs/data1 =  block 1
	/nirs/data2 =  block 2	
</dd>
	
<h3> /nirs/data{0}/dataTimeSeries [Required] </h3>	
<dt>data{0}.dataTimeSeries</dt><tt>[Type: numeric 2D-array] [Location: /nirs/data{0}/dataTimeSeries ] </tt>
<dd>This is the actual raw data variable. This variable has dimensions of 
<tt>&lt;number of time points&gt; x &lt;number of channels&gt;</tt>.   
Columns in <i>dataTimeSeries</i> are mapped to the measurement list (<i>measurementList</i> variable described below).  

dataTimeSeries can be compressed using the Hdf5 filter (prebuilt filters 305-LZO or 307-bzip2 supported; see https://support.hdfgroup.org/services/filters.html).  

Chunked data is allowed to support real-time streaming of data in this array.   

</dd>

<h3> /nirs/data{0}/time [Required] </h3>	
<dt>data{0}.time</dt><tt>[Type: numeric 1D array] [Location: /nirs/data{0}/time ]</tt>
<dd>The <i>time</i> variable. This provides the acquisition time of the measurement 
relative to the time origin.  This will usually be a straight line with slope 
equal to the acquisition frequency, but does not need to be equal spacing.  For the special
case of equal sample spacing a shorthand <2x1> array is allowed where the first entry is the start time and the 
second entry is the sample time spacing in seconds (e.g. 0.2 = 200ms [equivelent to 5Hz]) 
		
	Option1 - The size of this variable is <number of time points x 1> and 
	corresponds to the sample time of every data point
	
	Option2-  The size of this variable is <2x1> and correponds to the start
	time and sample spacing.

Chunked data is allowed to support real-time streaming of data in this array.   

</dd>

<h3> /nirs/data{0}/measurementList{0} [Required] </h3>	
<dt>./data{0}.measurementList{0}</dt><tt>[Type: indexed group] [Location: /nirs/data{0}/measurementList{0} ]</tt>
<dd>The measurement list. This variable serves to map the data array onto the 
probe geometry (sources and detectors), data type, and wavelength.   This 
variable is an array structure that has the size <tt>&lt;number of 
channels&gt;</tt> that describes the corresponding column in the data matrix. 

For example, the *measurementList(3)* describes the third column of the data matrix (i.e. 
*dataTimeSeries(:,3)*).

Each element of the array is a structure which describes the measurement 
conditions for this data with the following fields:
</dd>

<h3> /nirs/data{0}/measurementList{0}/sourceIndex [Required] </h3>	
<dt> ./measurementList{0}.sourceIndex</dt><tt>[Type: integer] [Location: /nirs/data{0}/measurementList{0}/sourceIndex]</tt>
	<dd>: index (starting from 1) of the source</dd>
	
<h3> /nirs/data{0}/measurementList{0}/detectorIndex [Required] </h3>	
<dt> ./measurementList{0}.detectorIndex</dt><tt>[Type: integer] [Location: /nirs/data{0}/measurementList{0}/detectorIndex]</tt>
	<dd>: index (starting from 1) of the detector</dd>

<h3> /nirs/data{0}/measurementList{0}/wavelengthIndex [Required] </h3>	
<dt> ./measurementList{0}.wavelengthIndex </dt><tt>[Type: integer] [Location: /nirs/data{0}/measurementList{0}/wavelengthIndex]</tt>
	<dd>: index (starting from 1) of the wavelength</dd>
	
<h3> /nirs/data{0}/measurementList{0}/dataType [Required] </h3>	
<dt> ./measurementList{0}.dataType </dt><tt>[Type: integer] [Location: /nirs/data{0}/measurementList{0}/dataType]</tt>
	<dd>: data-type identifier, see Appendix</dd>

<h3> /nirs/data{0}/measurementList{0}/dataTypeLabel [Optional] </h3>	
<dt> ./measurementList{0}.dataTypeLabel </dt><tt>[Type: string] [Location: /nirs/data{0}/measurementList{0}/dataTypeLabel]</tt>
	<dd>: data-type label only required if dataType is "processed". See Appendix</dd>

<h3> /nirs/measurementList{0}/dataTypeIndex [Required] </h3>	
<dt> ./measurementList{0}.dataTypeIndex </dt><tt>[Type: integer] [Location: /nirs/data{0}/measurementList{0}/dataTypeIndex]</tt>
	<dd>: data-type specific parameter indices</dd>

<h3> /nirs/data{0}/measurementList{0}/sourcePower [Optional] </h3>	
<dt> ./measurementList{0}.sourcePower </dt><tt>[Type: numeric] [Location: /nirs/data{0}/measurementList{0}/sourcePower]</tt>
	<dd>: source power in milliwatt (mW) </dd>

<h3> /nirs/data{0}/measurementList{0}/detectorGain [Optional] </h3>	
<dt> ./measurementList{0}.detectorGain </dt><tt>[Type: numeric] [Location: /nirs/data{0}/measurementList{0}/detectorGain]</tt>
	<dd>: detector gain</dd>

<h3> /nirs/data{0}/measurementList{0}/moduleIndex [Optional] </h3>	
<dt> ./measurementList{0}.moduleIndex </dt><tt>[Type: integer] [Location: /nirs/data{0}/measurementList{0}/moduleIndex]</tt>
	<dd>: index (starting from 1) of a repeating module</dd>

For example, if *measurementList{5}* is a structure with *sourceIndex=2*, *detectorIndex=3*, 
*wavelengthIndex=1*, *dataType=1*, *dataTypeIndex=1* would imply that the data 
in the 5th column of the *dataTimeSeries* variable was measured with source #2 and detector 
#3 at wavelength #1.  Wavelengths (in nanometers) are described in the 
*probe.wavelengths* variable  (described later). The data type in this case is 1, 
implying that it was a continuous wave measurement.  The complete list of 
currently supported data types is found in the Appendix. The data type index 
specifies additional data type specific parameters that are further elaborated 
by other fields in the *probe* structure, as detailed below. Note that the Time 
Domain and Diffuse Correlation Spectroscopy data types have two additional 
parameters and so the data type index must be a vector with 2 elements that 
index the additional parameters.

sourcePower provides the option for information about the source power for that 
channel to be saved along with the data. The units are not defined, unless the 
user takes the option of using a *metaDataTag* described below to define, for 
instance, *sourcePowerUnit*. *detectorGain* provides the option for information 
about the detector gain for that channel to be saved along with the data.

Note:  The source indices generally refer to the optode naming (probe 
positions) and not necessarily the physical laser numbers on the instrument. 
The same is true for the detector indices.  Each source optode would generally, 
but not necessarily, have 2 or more wavelengths (hence lasers) plugged into it 
in order to calculate deoxy- and oxy-hemoglobin concentrations. The data from 
these two wavelengths will be indexed by the same source, detector, and data 
type values, but have different wavelength indices. Using the same source index 
for lasers at the same location but with different wavelengths simplifies the 
bookkeeping for converting intensity measurements into concentration changes. 
As described below, optional variables *probe.sourceLabels* and *probe.detectorLabels* are 
provided for indicating the instrument specific label for sources and detectors.


<h3>/nirs/stim{0} [Optional]</h3>
<dt>./stim</dt><tt>[Type: indexed group]</tt>
<dd>This is an array describing any stimulus conditions. Each element of the 
array has the following required fields.</dd>

<h3>/nirs/stim{0}/name [Required as part of stim{0}] </h3>
<dt>./stim{0}.name</dt><tt>[Type: string] [Location:/nirs/stim{0}/name ]</tt>
<dd>This is a string describing the n<sup>th</sup> stimulus condition.</dd>

<h3>/nirs/stim{0}/data [Required as part of stim{0}] </h3>
<dt>./stim(n).data</dt><tt>[Type: numeric 2D array] [Location:/nirs/stim{0}/data ]</tt>
<dd> This is a three-column array specifying the stimulus time course for the 
n<sup>th</sup> condition. Each row corresponds with a specific stimulus trial. 
The three columns indicate [starttime duration value].  The starttime, in 
seconds, is the time relative to the time origin when the stimulus takes on a 
value; the duration is the time in seconds that the stimulus value continues, 
and value is the stimulus amplitude.  The number of rows is not constrained. 
(see examples in the appendix).</dd>


<h3>/nirs/probe [Required] </h3>
<dt>./probe</dt><tt>[Type: group] [Location: /nirs/probe ]</tt>
<dd>This is a structured variable that describes the probe (source-detector) 
geometry.  This variable has a number of required fields.</dd>

<h3>/nirs/probe/wavelengths [Required] </h3>
<dt>./probe.wavelengths</dt><tt>[Type: numeric 1D array] [Location: /nirs/probe/wavelengths ]</tt>
<dd>This field describes the wavelengths used.  This is indexed by the 
wavelength index of the measurementList variable.
	
For example, *probe.wavelengths* = [690 780 830]; implies that the measurements were 
taken at three wavelengths (690nm, 780nm, and 830nm).  The wavelength index of 
*measurementList(k).wavelengthIndex* variable refers to this field.  *measurementList(k).wavelengthIndex* 
= 2 means the k<sup>th</sup> measurement was at 780nm.

The number of wavelengths is not limited (except that at least two are needed 
to calculate the two forms of hemoglobin).  Each source-detector pair would 
generally have measurements at all wavelengths.
</dd>


<h3>/nirs/probe/wavelengthsEmission [Optional] </h3>
<dt>./probe.wavelengthsEmission</dt><tt>[Type: numeric 1D array]</tt>
<dd>This field is required only for fluorescence data types, and describes the 
emission wavelengths used.  The indexing of this variable is the same 
wavelength index in measurementList used for <i>probe.wavelengths</i> such that the excitation wavelength 
is paired with this emission wavelength for a given measurement.</dd>


<h3>/nirs/probe/sourcePos [Required] </h3>
<dt>./probe.sourcePos</dt><tt>[Type: numeric 2D array] [Location: /nirs/probe/sourcePos ] </tt>
<dd>This field describes the position (in spatialUnit units) of each source 
optode.  This field has size <tt>&lt;number of sources&gt; x 3</tt>.  For 
example, <i>probe.sourcePos(1,:)</i> = [1.4 1 0], and <i>SpatialUnit='cm'</i>; places source 
number 1 at x=1.4 cm and y=1 cm and z=0 cm.

Dimensions are relative coordinates (i.e. to some arbitrary defined origin).  
The *qform* variable described below can be used to define the transformation 
between this SNIRF coordinate system and other coordinate systems.
</dd>


<h3>/nirs/probe/sourcePos3D [Optional] </h3>
<dt>./probe.sourcePos3D</dt><tt>[Type: numeric 2D array] [Location: /nirs/probe/sourcePos3D ] </tt>
<dd>This field describes the position (in spatialUnit units) of each source 
optode in 3D.  <dd>


<h3>/nirs/probe/detectorPos [Required] </h3>
<dt>./probe.detectorPos</dt><tt>[Type: numeric] [Location: /nirs/probe/detectorPos]</tt>
<dd>Same as <i>probe.sourcePos</i>, but describing the detector positions.</dd>


<h3>/nirs/probe/detectorPos3D [Optional] </h3>
<dt>./probe.detectorPos3D</dt><tt>[Type: numeric 2D array] [Location: /nirs/probe/detectorPos3D ] </tt>
<dd>This field describes the position (in spatialUnit units) of each detector
optode in 3D.  <dd>


<h3>/nirs/probe/frequencies [Optional] </h3>
<dt>./probe.frequencies</dt><tt>[Type: numeric 1D array] [Location: /nirs/probe/frequencies ] </tt>
<dd>This field describes the frequencies used for frequency domain measurements. This field is only required for frequency domain data types, and is indexed by  
<i>measurementList(k).dataTypeIndex</i>.  <dd>


<h3>/nirs/probe/timeDelays [Optional] </h3>
<dt>./probe.timeDelays</dt><tt>[Type: numeric 1D array] [Location: /nirs/probe/timeDelays ] </tt>
<dd>This field describes the time delays used for gated time domain measurements. This field is only required for gated time domain data types, and is indexed by  
<i>measurementList(k).dataTypeIndex</i>. The indexing of this field is paired with the indexing of <i>probe.timeDelayWidths</i>. <dd>


<h3>/nirs/probe/timeDelayWidths [Optional] </h3>
<dt>./probe.timeDelayWidths</dt><tt>[Type: numeric 1D array] [Location: /nirs/probe/timeDelayWidths ] </tt>
<dd>This field describes the time delay widths used for gated time domain measurements. This field is only required for gated time domain data types, and is indexed by  
<i>measurementList(k).dataTypeIndex</i>.  The indexing of this field is paired with the indexing of <i>probe.timeDelays</i>.<dd>


<h3>/nirs/probe/momentOrders [Optional] </h3>
<dt>./probe.momentOrders</dt><tt>[Type: numeric 1D array] [Location: /nirs/probe/momentOrders ] </tt>
<dd>This field describes the moment orders of the temporal point spread function for moment time domain measurements. This field is only required for moment time domain data types, and is indexed by  
<i>measurementList(k).dataTypeIndex</i>.  <dd>


<h3>/nirs/probe/correlationTimeDelays [Optional] </h3>
<dt>./probe.correlationTimeDelays</dt><tt>[Type: numeric 1D array] [Location: /nirs/probe/correlationTimeDelays ] </tt>
<dd>This field describes the time delays used for diffuse correlation spectroscopy measurements. This field is only required for diffuse correlation spectroscopy data types, and is indexed by  
<i>measurementList(k).dataTypeIndex</i>.  The indexing of this field is paired with the indexing of <i>probe.correlationTimeDelayWidths</i>.<dd>


<h3>/nirs/probe/correlationTimeDelayWidths [Optional] </h3>
<dt>./probe.correlationTimeDelayWidths</dt><tt>[Type: numeric 1D array] [Location: /nirs/probe/correlationTimeDelayWidths ] </tt>
<dd>This field describes the time delay widths used for diffuse correlation spectroscopy measurements. This field is only required for gated time domain data types, and is indexed by  
<i>measurementList(k).dataTypeIndex</i>. The indexing of this field is paired with the indexing of <i>probe.correlationTimeDelays</i>.  <dd>


<h3>/nirs/probe/sourceLabels [Optional] </h3>
<dt>/nirs/probe.sourceLabels{0}</dt><tt>[Type: indexed string]
[Location: /nirs/probe/sourceLabels{0} indexed from 1]</tt>
<dd>This is a string array providing user friendly or instrument specific 
labels for each source. Each element of the array must be a unique string
among both <i>probe.sourceLabels</i> and <i>probe.detectorLabels</i>.
This can be of size <tt>&lt;number of sources&gt;
x 1</tt> or <tt>&lt;number of sources&gt; x &lt;number of 
wavelengths&gt;</tt>. This is indexed by <i>measurementList(k).sourceIndex</i> and 
<i>measurementList(k).wavelengthIndex</i>.</dd>


<h3>/nirs/probe/detectorLabels [Optional] </h3>
<dt>/nirs/probe/detectorLabels{0}</dt><tt>[Type: indexed string]
[Location: /nirs/probe.detectorLabels{0} indexed from 1]</tt>
<dd>This is a string array providing user friendly or instrument specific 
labels for each detector. Each element of the array must be a unique string
among both <i>probe.sourceLabels</i> and <i>probe.detectorLabels</i>.
This is indexed by <i>measurementList(k).detectorIndex</i>.</dd>
	

<h3>/nirs/probe/landmarkPos [Optional] </h3>
<dt>./probe.landmarkPos</dt><tt>[Type: numeric 2D array] [Location: /nirs/probe/landmarkPos] </tt>
<dd>This is a 2-D array storing the neurological landmark positions measurement
from 3-D digitization and tracking systems to facilitate the registration and 
mapping of optical data to brain anatomy. This array should contain a minimum 
of 3 columns, representing the x, y and z coordinates of the digitized landmark
positions. If a 4th column presents, it stores the index to the labels of the 
given landmark. Label names are stored in the <i>probe.landmarkLabels</i> subfield.
An label index of 0 refers to an undefined landmark. </dd>


<h3>/nirs/probe/landmarkPos3D [Optional] </h3>
<dt>./probe.landmarkPos3D</dt><tt>[Type: numeric 2D array] [Location: /nirs/probe.landmarkPos3D] </tt>
<dd>This is a 2-D array storing the neurological landmark positions measurement
from 3-D digitization and tracking systems to facilitate the registration and 
mapping of optical data to brain anatomy. This array should contain a minimum 
of 3 columns, representing the x, y and z coordinates of the digitized landmark
positions. If a 4th column presents, it stores the index to the labels of the 
given landmark. Label names are stored in the <i>probe.landmarkLabels</i> subfield.
An label index of 0 refers to an undefined landmark. </dd>


<h3>/nirs/probe/landmarkLabels{0} [Optional] </h3>
<dt>./probe/landmarkLabels{0}</dt><tt>[Type: indexed string]
[Location: /nirs/probe/landmarkLabels{0} indexed from 1]</tt>
<dd>This string array stores the names of the landmarks. The first string 
denotes the name of the landmarks with an index of 1 in the 4th column of 
<i>probe.landmark</i>, and so on. One can adopt the commonly used 10-20 landmark 
names, such as "Nasion", "Inion", "Cz" etc, or use user-defined landmark 
labels. The landmark label can also use the unique source and detector labels
defined in <i>probe.sourceLabels</i> and <i>probe.detectorLabels</i>, respectively, to 
associate the given landmark to a specific source or detector. All 
strings are ASCII encoded char arrays.</dd>


<h3>/nirs/probe/useLocalIndex [Optional] </h3>
<dt>/nirs/probeuseLocalIndex</dt><tt>[Type: integer] [Location: nirs/probe/useLocalIndex]</tt>
<dd>For modular fNIRS systems, setting this flag to a non-zero integer indicates
that <i>measurementList(k).sourceIndex</i> and <i>measurementList(k).detectorIndex</i> are module-specific
local-indices. One must also include <i>measurementList(k).moduleIndex</i> in the <i>measurementList</i>
structure in order to restore the global indices of the sources/detectors.</dd>


<h3>/nirs/metaDataTags{0} [Required] </h3>
<dt>./metaDataTags{0}</dt><tt>[Type: group array] [Location: /nirs/metaDataTags ]</tt>
<dd>This is a two column string array of arbitrary length consisting of any 
key/value pairs the user (or manufacturer) would like to put in.  Each row of 
the array consists of two strings. Some possible examples:

```
['ManufacturerName','ISS'],
['Model','Imagent'],
['SubjectName', 'Pseudonym, I.M.A.'],
['DateOfBirth','20120401'],
['AcquisitionStartTime','150127.34']
['StudyID','Infant Brain Development']
['StudyDescription','We study infant cognitive development.']
['AccessionNumber','INA2S12']
['InstanceNumber','2']
['CalibrationFileName','phantomcal_121015.snirf']
```
While these tags are freeform, some conventions must be followed.  Keys should 
use only alphanumeric characters with no spaces, with individual words 
capitalized.  All values will be stored as strings, How strings are converted 
into numeric values is left to whoever defines the Key.  However, it is 
required that dates be stored as YYYYMMDD, and clock times be stored as 
HHMMSS.SSSS… (24 hour format) for consistency.  Time intervals must be in 
seconds.

The following metadata tags are required:
```
SubjectID
MeasurementDate
MeasurementTime
SpatialUnit    (allowed values are 'mm' and 'cm')
```
</dd>

The metadata tags "StudyID" and "AccessionNumber" are unique strings that can 
be used to link the current dataset to a particular study and a particular
procedure, respectively. The "StudyID" tag is similar to the DICOM tag 
"Study ID" (0020,0010) and "AccessionNumber" is similar to the DICOM tag 
"Accession Number"(0008,0050), as defined in the DICOM standard (ISO 12052).

The metadata tag "InstanceNumber" is defined similarly to the DICOM tag 
"Instance Number" (0020,0013), and can be used as the sequence number to
group multiple datasets into a larger dataset - for example, concatenating 
streamed data segments during a long measurement session.

<h3>/nirs/aux{0} [Optional] </h3>
<dt>./aux{0}</dt><tt>[Type: indexed group][Location: /nirs/aux{0} where index starting with 1]</tt>
<dd>This optional array specifies any recorded auxiliary data. Each element of 
<i>aux</i> has the following required fields:</dd>

<h3>/nirs/aux{0}/name [Optional; Required if aux{0} used] </h3>
<dt>./aux{0}.name</dt><tt>[Type: string]
[Location: /nirs/aux{0}/name]</tt>
<dd>This is string describing the n<sup>th</sup> auxiliary data timecourse.</dd>

<h3>/nirs/aux{0}/dataTimeSeries [Optional; Required if aux{0} used] </h3>
<dt>./aux(n).dataTimeSeries</dt><tt>[Type: numeric]
[Location: /nirs/aux{0}/dataTimeSeries]</tt>
<dd>This is the aux data variable. This variable has dimensions of 
<tt>&lt;number of time points&gt; x 1</tt>.

Chunked data is allowed to support real-time data streaming
</dd>

<h3>/nirs/aux{0}/time [Optional; Required if aux{0} used] </h3>
<dt>./aux{0}.time</dt><tt>[Type: numeric] [Location: /nirs/aux{0}/time]</tt>
<dd>The time variable. This provides the acquisition time of the aux 
measurement relative to the time origin.  This will usually be a straight line 
with slope equal to the acquisition frequency, but does not need to be equal 
spacing.  The size of this variable is <tt>&lt;number of time points&gt; x 1</tt> or <2x1> similar to 
definition of the /nirs/data/time field.

Chunked data is allowed to support real-time data streaming
</dd>

<h3>/nirs/aux{0}/timeOffset [Optional] </h3>
<dt>./aux{0}.timeOffset</dt><tt>[Type: numeric]
[Location: /nirs/aux{0}/timeOffset]</tt>
<dd>This variable specifies the offset of the file time origin relative to 
absolute (clock) time in seconds. </dd>


## Appendix

### Supported measurementList{0}.dataType values in “dataTimeSeries”

<p>
001-100:  Raw - Continuous Wave (CW):
<ul>
001 - Amplitude<br>
051 - Fluorescence Amplitude<br>
</ul>
</p>
	
<p>
101-200:  Raw - Frequency Domain (FD):
<ul>
101 - AC Amplitude<br>
102 - Phase<br>
151 - Fluorescence Amplitude<br>
152 - Fluorescence Phase<br>
</ul>
</p>
	
<p>
201-300: Raw - Time Domain - Gated (TD Gated):
<ul>
201 - Amplitude<br>
251 - Fluorescence Amplitude<br>
</ul>
</p>

<p class="linespacing_small">
301-400:  Raw - Time domain – Moments (TD Moments):
<ul>
301 - Amplitude<br>
351 - Fluorescence Amplitude<br>
</ul>
</p>

<p>
401-500:  Raw - Diffuse Correlation Spectroscopy (DCS):
<ul>
401 - g2<br>
410 - BFi<br>
</ul>
</p>

<p>
99999:  Processed:
</p>


### Supported measurementList{0}.dataTypeLabel values in “dataTimeSeries”
<ul>
"dOD" - Change in optical density<br>
"mua" - Absorption coefficient<br>
"musp" - Scattering coefficient<br>
"HbO" - Oxygenated hemoglobin (oxyhemoglobin) concentration<br>
"HbR" - Deoxygenated hemoglobin (deoxyhemoglobin) concentration<br>
"HbT" - Total hemoglobin concentration<br>
"HRF HbO" - Hemodynamic response function for oxyhemoglobin concentration<br>
"HRF HbR" - Hemodynamic response function for deoxyhemoglobin concentration<br>
"HRF HbT" - Hemodynamic response function for total hemoglobin concentration<br>
"H2O" - Water content<br>
"Lipid" - Lipid concentration<br>
"HRF BFi" - Hemodynamic response function for blood flow index (BFi)<br>
</ul>


### Examples of stimulus waveforms

Assume there are 10 time points, starting at zero, spaced 0.1s apart.  If we 
assume a stimulus to be a 0.2 second off, 0.2 second on repeating block, it 
would be specified as follows:
```
    [0.2 0.2 1.0]
    [0.6 0.2 1.0]
```

## Acknowledgement

This document was originally drafted by Blaise Frederic (bbfrederick at mclean.harvard.edu) and David Boas (dboas at bu.edu).

Other significant contributors to this specification include:
- Theodore Huppert (huppert1 at pitt.edu)
- Jay Dubb (jdubb at bu.edu)
- Qianqian Fang (q.fang at neu.edu)

The following individuals representing academic, industrial, software, and hardware interests are also contributing to and supporting the adoption of this specification:

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
