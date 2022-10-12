# Governance

## Mission Statements
### SNIRF
The SNIRF specification serves to provide a binary file format for functional near-infrared spectroscopy data which is portable and widely applicable. In particular, the SNIRF specification seeks to capture:
- Acquired raw data in various modalities, including auxiliary physiological and stimulus signals
- Probe geometry and optode parameters
- Simple derivative signals and post-processed data
- Subject information and simple experimental metadata

### SNIRF Government
The mission of the SNIRF government is to ensure the format's longevity and to encourage its adoption. Critical to this mission is the ability of the fNIRS community to expand or correct the specification as new developments emerge without creating issues and conflicts for users. The SNIRF government is responsible for moderating this process, and for collecting and disseminating important information to SNIRF users.

SNIRF's government is composed of two groups: a Steering Committee ultimately responsible for motivating and justifying changes to the specification, and a group of Maintainers who are authorized to draft these changes. Membership is open to any user of the SNIRF format.

## Bylaws

## Definitions

"SNIRF Contributors" are individuals who have contributed changes, revisions, issues, or points of discussion to the SNIRF specification via GitHub.

## Article I. Steering Committee

**Section 1.** Steering Committee Definition. The SNIRF Steering Committee is ultimately responsible for guiding the development of SNIRF in accordance with its mission. The committee must unanimously approve the releases of official and final changes to the specification, as well as changes to the SNIRF government or mission statement.

**Section 2.** Election. Steering committee members must be nominated or self-nominated in advance of the end of a sitting member's term. The departing member is responsible for the organization of the election, and cannot be elected to remain in the same seat. All SNIRF Contributors, Maintainers, and Steering Committee members are eligble to vote in the election.

**Section 3.** Terms. The Steering Committee is composed of 3 or 5 members of the fNIRS community who are elected to serve 3 year terms. The number of members should remain odd.

**Section 4.** Meetings. A majority of Steering Committee members must meet at least biannually. At least one Maintainer must be present at these meetings. These meetings should review the following:
- The most recent Maintainers Report
- Any pending releases or critical changes
- project priorities and progress towards goals
- Delegation of resources (i.e maintainers' attention) towards completion of goals

The meeting should result in the authorship of a brief report.

**Section 5.** Steering Committee Reports. The Steering Committee must author a brief report following each of its required biannaual meetings. This report must document the actions and considerations of the committee, and must be archived and disseminated via the GitHub repository. The report must include the names of the Steering Committee's members.

**Section 6.** GitHub Repository Role. Steering Committee members must have the role of `Admin` on the GitHub repository.  

**Section 7.** Specification Releases. The Steering Committee must unanimously approve official releases and publish them via GitHub. Releases must be thoroughly documented and properly formatted as described in RELEASE.md. The Committee is subsequently responsible for alerting the community to the release.

**Section 8.** Maintainer Election. Any member of the Steering Committee may at any time approve the addition of a Maintainer. The Steering Committee member must give the Maintainer the role of `Maintain`.

## Article II. Maintainers

**Section 1.** Maintainer Definition. Maintainers are responsible for directing and moderating changes and fixes to the specification and its repository. This includes the merging of pull requests, the management of issues, and the preparation and validation of pending official releases. Maintainers are expected to advance the specification towards the goals laid out by the steering committee.

**Section 2.** Election. Maintainers may be nominated or self-nominated at any time. A single member of the Steering Committee must approve them. Maintainers may serve subsequent terms.

**Section 3.** Terms. Maintainers serve 2 year terms. At the end of their term, they must step down or seek the renewal of their title from a member of the Steering Committee.

**Section 4.** Maintainers' Report. Maintainers must collectively author a biannual report summarizing the prominent actions and considerations of the Maintainers since the previous report. This report must include any critical issues or pending releases which the Steering Committee must consider. 

**Section 5.** GitHub Repository Role. Maintainers must have the role of `Maintainer` on the GitHub repository.

## Article III. Additional Bylaws

**Section 1.** Pull Requests. Maintainers are ultimately responsible for the merging of pull requests into the working branches of the SNIRF specification, but both Steering Committee Members and Maintainers have the authority to do so. Pull requests must receive reviews from 2 Committee members or Maintainers prior to merging, and should remain open for at least 2 weeks. Changes may be merged immediately following review only in the case of minor corrections and administrative changes.

**Section 2.** Scheduling of Meetings. Meetings may be organized by anyone. No more than 7 months should elapse between meetings such that they remain biannual.
