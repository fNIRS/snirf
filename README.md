# SNIRF Format Specification Development Guide

We use this repository to gather feedback from the community regarding the 
["Shared Near Infrared File Format Specification"](snirf_specification.md), or SNIRF format. Such 
feedback is crucial to finalize this file specification and help to improve
it in the future once disseminated. 

The latest version of the SNIRF specification can be found in the file named 
[snirf_specification.md](snirf_specification.md). The specification is written
in the [Markdown format](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet) 
for convenient editing and version control.

## How to download the specification, sample files and parsers

To browse the latest version of the SNIRF Specification document, you may click on 
[this link](snirf_specification.md).

To download the latest specification document alone, you should use the below command
```
   git clone https://github.com/fNIRS/snirf.git
```
or click on this [download link](https://github.com/fNIRS/snirf/archive/master.zip).

If you use [TortoiseGit](https://tortoisegit.org/) on Windows, you should open a file browser, navigate to a folder
where you want to store the files, right click, and select "Git Clone ..." from the 
pop-up menu, then type in `https://github.com/fNIRS/snirf.git` as the URL.

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
If you use TortoiseGit, you must check the "Recursive" checkbox in the clone dialog.

## How to participate

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
  - once your revision is complete, please "commit" and "push" it to your forked
    git repository. Then you should create a pull-request agaist the upstream
    repository (i.e., fNIRS/snirf). Please select "Compare cross forks" and 
    select "fNIRS/snirf" as "base fork". Please write a descriptive title for
    your pull-request. The project maintainer will review your updates
    and choose to merge to the upstream files or request revision from you.
    
