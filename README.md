

# Dobby

Dobby is an app that helps with managing MUNs. The primary function of Dobby is to increase the efficiency and cost of sorting and allocating schools their portfolios. When sorting portfolio the host school keeps in mind certain criteria i.e. rules to make sure the schools are spread evenly and fairly across the various Committees.<br><br>MUNs are a model united nation conference that takes place periodically and are orchestrated by a secretariat. As part of preparation for the MUN the secretariat has to assign schools portfolios to participating schools. This process includes receiving portfolios and their importance from the Chairs of the Committees. Knowing participating schools and their delegation size. Next, assigning these schools the portfolios. Finally, the school sends the names of students along with the portfolio that they give, this list has to be sorted and given to the Chairs.

[TOC]

## The Phases

While sorting and assigning delegates their portfolios, the program includes 3 stages: 

1. **initial input** - includes input of committees and their portfolios and input of schools with their delegation size
2. **basic sort** - allocates the portfolios to schools according to a criteria 
3. **assigning** - the schools sends a list of individuals and their allotted portfolios which are to be uploaded onto the application

## Inputting Committees

The secretariat will have to upload a csv file for each committee. The csv file will have to follow the following format:

| **Committee Name** |                  |
| ------------------ | ---------------- |
| *Portfolio Rank*   | *Portfolio Name* |

**Example**

| DISEC |      |
| ----- | ---- |
| 1     | Iran |
| 2      | India|
| 2 | Greece|
| 3 | Brazil|

The rank need not be sorted. The ranks must be given in the range 1-3 with 1 being the highest. Rankings are given according to a portfolios involvement in the Committee.

## Inputting Schools

The user will see 4 attributes to assign to a school in the first stage: School name, delegation size, grade, school gender respectively. The delegation size will be the number of students that will be sent from the invited school. Grade specifies the school's level of debate in an MUN. School gender asks whether the school is all boys, all girls, or co-ed.<br>The cap for delegation size is at 15. The grade of each school will be from 1 to 5 with 1 being the highest. 