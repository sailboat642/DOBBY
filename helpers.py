import sqlite

MALE = 1
FEMALE = 0

def create_database(filename):
	filename = "./databases/" + name + ".db"
	try:
    	conn = sqlite3.connect(filename)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        conn.close()

def upload_database(filename):
	

def genderSplit():			# take database as input?
'''splits the committees in an optimal gender ratio'''

	# Make gender ratio
	maleCount = cur.execute("SELECT COUNT(gender) FROM student WHERE gender = ?", MALE)[0]
	totalStudents = cur.execute("SELECT COUNT(*) FROM students")[0]
	ratio = maleCount/totalStudents

	# fix each committee to the same ratio
	committees = cur.execute("SELECT committee FROM committees")
	for committee in committees:
		ranks = (int) cur.execute("SELECT COUNT(DISTINCT rank) FROM ?", committee)[0]
		splitCommitteByGender(ranks, committee, ratio)

def splitCommitteByGender(ranks, committee, ratio)
'''splits the committees in an optimal gender ratio'''

	# split ranks individually
	for i in range(1, ranks + 1):
		portfoliosWithRank = cur.execute("SELECT portfolio FROM ? WHERE rank = ?", committee, i)
		portfoliosWithRankCount = len(portfoliosWithRank)
		assignedMale = round(ratio * portfoliosWithRankCount)
		for j in portfoliosWithRank:
			if portfoliosWithRankCount > 0:
				cur.execute("UPDATE ? SET gender = 1 WHERE portfolio = ?", committe, j["portfolio"])
				portfoliosWithRankCount--
			else:
				cur.execute("UPDATE ? SET gender = 0 WHERE portfolio = ?", committe, j["portfolio"])

def schoolAssign():
'''Gives schools portfolios in terms of rank/grade'''
	# select all male students
	maleStudents = cur.execute("SELECT * FROM students WHERE gender = ? ORDER BY committee_id", MALE)
	# select all portfolios assigned to males
	# sort school by rank
	# sort portfolio by committee
	# assign each school a top rank
	# 
