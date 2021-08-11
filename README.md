# Shared Near Infrared File (SNIRF) Format

This repository stores the Shared Near Infrared Spectroscopy Format (SNIRF).  
SNIRF is designed by the community in an effort to facilitate sharing and analysis of NIRS data.

View the most recent release version of the format: [here](https://github.com/fNIRS/snirf/blob/da550abf7ec70084e31ba428df09a9dcbf3e6036/snirf_specification.md).  
View the development version of the format: [here](snirf_specification.md).   


## User Information

To browse the latest version of the SNIRF Specification document, you may click on 
[this link](snirf_specification.md). A history of changes to the specification and
information on released versions is available in the [change log](CHANGELOG.md).

The following software packages support reading and/or writing SNIRF files.

| Software       |                   URL                        |
|----------------|----------------------------------------------|
| Homer2         | https://homer-fnirs.org                      |
| Homer3         | https://github.com/BUNPC/Homer3              |
| MNE-Python     | https://mne.tools                            |
| NIRS-Toolbox   | https://github.com/huppertt/nirs-toolbox     |
| FieldTrip      | https://www.fieldtriptoolbox.org             |
| NIRStorm       | https://github.com/Nirstorm/nirstorm         |


The following vendors export data in SNIRF format.

| Vendor         |              URL                 |
|----------------|----------------------------------|
| NIRx           | https://nirx.net                 |


## Development Information

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
   git submodule update samples            # checkout the sample data files 
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
| sample data    | https://github.com/fNIRS/snirf-samples/archive/master.zip |
| EasyH5 Toolbox | https://github.com/fangq/easyh5/archive/v0.8.tar.gz       |
| JSNIRF Toolbox | https://github.com/fangq/jsnirfy/archive/v0.4.tar.gz      |
| SNIRF_HOMER3   | https://github.com/fNIRS/snirf_homer3/archive/master.zip  |
| pysnirf        | https://github.com/fNIRS/pysnirf/archive/master.zip       |

[This page](https://github.com/BUNPC/Homer3/wiki/Standalone-SNIRF-loading-and-saving) provides examples of how to work with Snirf files using the [Homer3](https://github.com/BUNPC/Homer3) interface.

### How to participate

We use this repository to gather feedback from the community regarding the 
["Shared Near Infrared File Format Specification"](snirf_specification.md), or SNIRF format. Such 
feedback is crucial to finalize this file specification and help to improve
it in the future once disseminated. 

The latest version of the SNIRF specification can be found in the file named 
[snirf_specification.md](snirf_specification.md). The specification is written
in the [Markdown format](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet) 
for convenient editing and version control.

You can use a number of methods to provide your feedback to the working 
draft of this file specification, including

- [Create an "Issue"](https://github.com/fNIRS/snirf/issues)
  - This is the most recommended method to provide detailed feedback or 
    discussion. An "Issue" in github is highly versatile. One can ask a 
    question, report a bug, provide a feature request, or simply propose
    general discussions. Please use URLs or keywords to link your discussion 
    to a specific line/section/topic in the document.
- [Write short comments on Request for Comments (RFC) commits](https://github.com/fNIRS/snirf/commit/88baa2a2ed3347e868ec184b9daa4b357ddbbfd1)
  - A milestone version of the specification will be associated with an
    RFC (Request for comments) commit (where the entire file is removed
    and re-added so that every line appears in such comment). One can
    write short comments as well as post replies on this RFC page. 
  - The latest RFC commit is based on version from Dec. 5, 2018 please use
    [this link](https://github.com/fNIRS/snirf/commit/88baa2a2ed3347e868ec184b9daa4b357ddbbfd1) to comment.
  - To add a comment, you need to first register a github account, and then 
    browse the above RFC page. When hovering your cursor over each line, a 
    "plus" icon is displayed, clicking it will allow one to comment on a 
    specific line (or reply to other's comments).
  - The RFC page can get busy if too many comments appear. Please consider 
    using the Issues section if this happens.
  - One can browse the commit history of the specification document. If
    anyone is interested in commenting on a particular updated, you can also
    comment on any of the commit page using the same method.
- [Use the snirf mailing list](http://fnirs.org/resources/software/snirf/)
  - You may send your comments to the snirf mailing list (snirf at fnirs.org). 
    Subscribers will discuss by emails, and if a motion is reached, proposals
    will be resubmitted as an Issue, and changes to the specification will be
    associated with this issue page.

For anyone who wants to contribute to the writing or revision of this document,
please browse [this tutorial](https://kwafoo.coe.neu.edu/~fangq/share/snirf/tutorial.htm)
first, and then follow the below steps

- Fork this repository and make updates, then create a pull-request
  - Please first register an account on github, then, browse the 
    [SNIRF repository](https://github.com/fNIRS/snirf);
    on the top-right of this page, find and click the "Fork" button.
  - once you fork the SNIRF project to your own repository, you may edit the
    files in your browser directly, or download to your local folder, and 
    edit the files using a text editor;
  - if you make a change to the specification (i.e. not a trivial change to the README)
    then add a line item to the CHANGELOG.md file;
  - once your revision is complete, please "commit" and "push" it to your forked
    git repository. Then you should create a pull-request against the upstream
    repository (i.e., fNIRS/snirf). Please select "Compare cross forks" and 
    select "fNIRS/snirf" as "base fork". Please write a descriptive title for
    your pull-request. The project maintainer will review your updates
    and choose to merge to the upstream files or request revision from you.
    
