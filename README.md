# BudFreezeSpike
Squeezing a little more useful information out of Bud Freezer data

## Goals
### 1) Import Data
Data is in long comma seperated text files, place it into lists sorted by category and indexed for cross referencing later.

Initially this will assume the 6 tray, 1 temperature, 9 peltier sensor arrangement but as I assume this is not always constant generalizing may be important.

### 2) Restrict data to interesting range
We only care about peaks that happen below -10

Resistance readings in files can be converted to temperature using a formula
> Temp = -0.007742(resistance) + 106.5

### 3) Search for peak in range
Looking for points that are far away from whatever trend is around them will be the next step. Although slopes are possible I believe I can treat the data as roughly flat by only looknig at *n* points into the future and past and keeping *n* low.

### 4) Display temperature vs time data
Printing time vs temperature data around interesting points.

Allow for human removal of points that aren't interesting that may be caused by high noise especially at colder temperatures.

### 5) Area under interesting peaks
Approximate area under peak by calculating local trend, no longer treating as necessarily flat line.

Rough riemann sum like calculation of area using a sum of differences in peak points from trend.

Print information 