Piazza Poll Score Calculate README

This simple script takes the raw poll csv's downloaded from Piazza and combines them with the roster to calculate the piazza poll score.

Assumptions made: 
- Credit is given to students for participating and NOT for selecting a specific choice.
- All students have an Andrew email address attached to their Piazza account. The script will warn you if a poll answer does not have an Andrew email address tied to the account. 

Directories and Files
- "roster" - Contains one csv which is the roster pulled from CMU S3.
- "polls" - Contains all of the csv files downloaded from each Piazza poll, the naming format by default should be piazzaPoll-COURSENUMBER-PollX-MONTH-DAY.csv This is used to name your poll columns.
- "output" - This is where the output is saved.
- PiazzaPollScoreCalc.py - This is the script which should be ran. It should like outside of the above three directories.
- [OPTIONAL] "missedpolls/missedpolls.csv" - This allows for accommodations to be made for missed polls. It must follow a specific format see section below. 

What to change:
- requiredPercent - if your class has a grace amount on polls, for example students only need to get  > 80 percent of the polls in order to get full participation credit, this script can account for this by setting requiredPercent = 80


missedpolls.csv:
Must have at least the following columns:
- "Andrew Email" - This should match the Andrew emails on the polls and your roster. There can be multiple rows with the same student if necessary, provided the "Poll Number" is different for each of them.
- "Poll Number" - This should be a column which lists the polls missed. If a student missed poll 1 then put poll1 in the entry. Only one poll per row.
Example: 
Student,Andrew Email,Poll Number,Note
Daniel Bird,dpbird@andrew.cmu.edu,poll5,Flu and still contageous
Brynn Edmunds,bedmunds@andrew.cmu.edu,poll6,Showed up late
Daniel Bird,dpbird@andrew.cmu.edu,poll6,Showed up late


