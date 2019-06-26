import sqlite

MALE = 1
FEMALE = 0


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def upload_database(filename):
'''csv into .db file'''	

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

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None

def schoolAssign():
'''Gives schools portfolios in terms of rank/grade'''
	# select all male students
	maleStudents = cur.execute("SELECT * FROM students WHERE gender = ? ORDER BY committee_id", MALE)
	# select all portfolios assigned to males
	# sort school by rank
	# sort portfolio by committee
	# assign each school a top rank
	# 
