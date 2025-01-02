# SNIRF Release Procedure

This document describes the process for releasing a new version of the SNIRF specification.
This procedure should be completed by a steering committee member in accordance with [governance policy](GOVERNMENT.md).

1. Raise an issue at least one week prior to a planed release date to inform the community that a release is imminent.
   Ensure that the issue clearly states the exact next proposed version number (e.g., `v1.0.0`).
2. Unanimous approval is required from the steering committee.
   Ensure all steering committee members have explicitly given their approval as a public github comment in the issue.
3. Open a pull request that makes the following modifications:
   a. Modify the version number in the opening lines of the specification to match the version to be released (e.g., `1.0.0`).
4. Ensure at least one other admin approves the pull request, then it can be merged.
5. Create a new release and git tag by:
   a. Press the `Create a new release` button on the repository home page.
   b. Click on the `Choose a tag` and type in the release version proceeded by a v, for example `v1.0.0`.
   c. Set the release title to the same as the tag name.
   d. Copy the dot points for this release from the CHANGELOG.md document to the release description field.
   e. Hit `Publish release`
6. Update the README.md document to reflect the new release by:
   a. Change the path of the "View the most recent release version of the format" link to reflect the tagged version.
      This will be something like https://github.com/fNIRS/snirf/blob/v1.0/snirf_specification.md
7. Modify the repository to indicate that it is now a development version by:
   a. Increase the version number in the SNIRF specification and append the word "development" to it. E.g., `v1.1.0-development`.
      This ensures that people can differentiate between released versions of the draft and work-in-progress versions.
   a. Update the change log file by adding a link to the released version, specifying the release data, and adding the next development version.
8. Send an email out on the mailing list via: https://mailchi.mp/89a906ec22cf/snirf
9. Increase the version number listed on the Society for fNIRS website: https://fnirs.org/resources/software/snirf/


## Supplementary Information

### Version Numbers

SNIRF uses the [Semantic Versioning](https://semver.org) scheme.
Some relevant information about this scheme for SNIRF releases is:

> Given a version number MAJOR.MINOR.PATCH, increment the:
> - MAJOR version when you make incompatible API changes
> - MINOR version when you add functionality in a backward compatible manner
> - PATCH version when you make backward compatible bug fixes

> Is “v1.2.3” a semantic version?
> 
> No, “v1.2.3” is not a semantic version. However, prefixing a semantic version with a “v” is a common way (in English) to indicate it is a version number. Abbreviating “version” as “v” is often seen with version control. Example: git tag v1.2.3 -m "Release version 1.2.3", in which case “v1.2.3” is a tag name and the semantic version is “1.2.3”.
