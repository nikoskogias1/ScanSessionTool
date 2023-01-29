# Testing Scan Session Tool
In order to verify the correct functioning of Scan Session Tool, we provide
instructions as well as test data to test several aspects of its core
functionality (i.e scan session documentation and data archiving). Since Scan
Session Tool is a graphical application, these tests have to be performed
manually.

## Scan session documentation
The following instructions will test the functionality of documenting scan
session information as well as saving and loading this information to and from
scan protocol files.

1. Click on "Open" (either in the main area of the user interface, or in the
_File_ menu) and select the file
`ScanProtocol_TestData_sub-001_ses-007-Transfer_20211203.txt`. This should
fill Scan Session Tool with the scan session information from that protocol
file.

2. Make changes to the session information. That is, change fields in "General
Information", "Documents" and "Measurements" (including adding or deleting
entire measurements).

3. Click on "Save" (either in the main area of the user interface, or in the
_File_ menu) and save the scan session information into a
new protocol file (e.g. `ScanProtocol_SaveTest.txt`).

4. Close and re-open Scan Session Tool

5. Click on "Open" (either in the main area of the user interface, or in the
_File_ menu) and select the previously saved file (e.g.
`ScanProtocol_SaveTest.txt`). This should fill Scan Session Tool with the scan
session information from that protocol file, including the changes you made
earlier.

# Data archiving
The following instruction will test the functionality of using the information
from scan session documentation to archive the recorded data relatd to it (i.e.
all DICOM images as well as any optional additional files).

1. Click on "Open" (either in the main area of the user interface, or in the
_File_ menu) and selecting the file
`ScanProtocol_TestData_sub-001_ses-007-Transfer_20211203.txt`. This should fill
Scan Session Tool with the scan session information from the protocol file.

2. Click on "Archive" (either in the main area of the user interface, or in the
_File_ menu). A dialogue window should open.

3. Click on "Browse" next to _Source_ and select on of the test data
directories (i.e. `TestData_1` or `TestData_2`).

4. Click on "Browse" next to _Target_ and select a directory to save the
archived data to (e.g. `ArchivingTest`).

5. Under _Options_ tick both "Create BrainVoyager links" and "Create
Turbo-Brain Voyager links".

6. Click on "GO". This will start the archiving process (which will take
a couple of minutes; progress is shown in a green overlay window).

7. Once finished, confirm that the data has been written into the target
directory (e.g. `ArchivingTest`) as `TestData`. The
[Data Integrity Fingerprint](https://expyriment.org/dataintegrityfingerprint/)
of the `TestData` directory withing the target directory should be
DIF [SHA256]: 556cdb4f011c1ebc36f489ecbf5cafa5292be8ded8837b96d96faecae56ad837.
In case it is not, compare it to the checksum file `TestData.sha256` to find
out what the deviations are (e.g. your operating system or file manager might
have written some hidden files to that directory without your knowledge).