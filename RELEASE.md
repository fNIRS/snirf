# SNIRF Release Procedure

This document describes the process for releasing a new version of the SNIRF specification.
Only someone with write access to the `fNIRS/snirf` repository can complete this procedure.

1. Raise an issue at least one week prior to a planed release date to inform the community that a release is imminent.
   Ensure that the issue clearly states the exact next proposed version number (e.g., `v1.0`).
2. Ensure at least one other admin (someone with write access) agrees with the planned release,
   and confirms that there are no known blocking issues (open issues in the tracker are ok, but they should not be of critical nature). 
   Approval should be provided as a comment in the issue, not via personal communication.
3. Open a pull request that makes the following modifications:
   1. Modify the version number in the opening lines of the specification to match the version to be released (e.g., `v1.0`).
4. Ensure at least one other admin approves the pull request, then it can be merged.
5. Create a new release and git tag by:
   1. Press the `Create a new release` button on the repository home page.
   2. Click on the `Choose a tag` and type in the release version proceeded by a v, for example `v1.0`.
   3. Set the release title to the same as the tag name.
   4. Copy the dot points for this release from the CHANGELOG.md document to the release description field.
   5. Hit `Publish release`
6. Update the README.md document to reflect the new release by:
   1. Change the path of the "View the most recent release version of the format" link to reflect the tagged version.
      This will be something like https://github.com/fNIRS/snirf/blob/v1.0/snirf_specification.md
7. Modify the repository to indicate that it is now a development version by:
   1. Increase the version number in the SNIRF specification and append the word "development" to it. E.g., `v1.1-development`.
      This ensures that people can differentiate between released versions of the draft and work-in-progress versions.
   2. Update the change log file by adding a link to the released version, specifying the release data, and adding the next development version.
8. Send an email out on the mailing list via: https://mailchi.mp/89a906ec22cf/snirf
9. Increase the version number listed on the Society for fNIRS website: https://fnirs.org/resources/software/snirf/
