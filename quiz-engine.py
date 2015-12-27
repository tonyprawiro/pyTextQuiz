import sys
import os
import random
import time

# Settings
iPassPercentage = 70
iMaxQuestionLength = 50
iMaxQuestionDuration = 300
bShowOriginalQuestionNumber = False

# Command line arguments
try:
	sQuizName = sys.argv[1]
except:
	print "Usage: quiz-engine.py QuizName"
	print "E.g.: quiz-engine.py MATHGRADE6"
	sys.exit(1)

# Check for file existence

sQuizQuestionsFile = "%s-QUESTIONS.txt" % (sQuizName)
sQuizKeysFile = "%s-KEYS.txt" % (sQuizName)

if not os.path.isfile(sQuizQuestionsFile) or not os.path.isfile(sQuizKeysFile):
	print "Error: Make sure %s and %s files exist in the same directory" % (sQuizQuestionsFile, sQuizKeysFile)
	sys.exit(1)

# Parse keys

aKeys = {}
with open(sQuizKeysFile) as fKeys:
	for line in fKeys:
		sNumber, sKey = line.strip().split(':')
		aKeys[sNumber] = sKey

# Parse questions

aQuestions = {}
sCurrentQuestionNumber = ""
sCurrentQuestionText = ""
iCurrentQuestionLength = 0
aQuestionShuffler = []
with open(sQuizQuestionsFile) as fQuestions:
	for line in fQuestions:
		if line[:9] == "QUESTION ":
			sCurrentQuestionNumber = line.strip()[9:]
			if bShowOriginalQuestionNumber:
				sCurrentQuestionText = line.strip() + "\n\n"
			else:
				sCurrentQuestionText = ""
		elif line[:3] == "---":
			aQuestions[sCurrentQuestionNumber] = sCurrentQuestionText
			aQuestionShuffler.append(sCurrentQuestionNumber)
			sCurrentQuestionNumber = ""
			sCurrentQuestionText = ""
			iCurrentQuestionLength = 0
		else:
			if iCurrentQuestionLength > iMaxQuestionLength:
				print "ERROR: Question #%s is more than allowed limit of length (%d)" % (sCurrentQuestionNumber, iMaxQuestionLength)
			else:
				iCurrentQuestionLength += 1
				sCurrentQuestionText += line.strip() + "\n"

iTotalQuestions = len(aQuestions)

# Shuffle the aQuestionShuffler array

random.shuffle(aQuestionShuffler)

# Make sure all questions are answered for in keys

aUnansweredFor = []
for sQNum, sQText in aQuestions.iteritems():
	try:
		sQAns = aKeys[sQNum]
	except:
		aUnansweredFor.append(sQNum)
if len(aUnansweredFor) > 0:
	print "ERROR: Some of the questions are unanswered in keys file: "
	for sQNum in aUnansweredFor:
		print sQNum
	print "Please rectify the keys file and then try again"
	print "Three dashes (---) at the start of a line are considered question delimiter."
	print "If you're using it as part of the question (e.g. tables), please add a space before it."
	sys.exit(1)

# Initialize session

print "There are %d questions in pool" % (iTotalQuestions)

iDesiredQuestions = 0
while True:
	sDesiredQuestions = raw_input("Enter the number of questions to answer (1-%s): " % (iTotalQuestions))
	try:
		iDesiredQuestions = int(sDesiredQuestions)
	except:
		pass
	if iDesiredQuestions >= 1 and iDesiredQuestions <= iTotalQuestions:
		break
	else:
		print "ERROR: Please enter a valid number"

iDurationPerQuestion = 120
while True:
	sDurationPerQuestion = raw_input("Duration of each question (default=120s): ")
	try:
		iDurationPerQuestion = int(sDurationPerQuestion)
	except:
		pass
	if iDurationPerQuestion >= 1 and iDurationPerQuestion <= iMaxQuestionDuration:
		break
	else:
		print "ERROR: Please enter a valid number"

# Start the session

iStartTime = time.time()
iCorrect = 0
aSkipped = []
aIncorrect = []
bStop = False
iAnsweredQuestions = 0
aMyAnswers = {}
for iQIdx in range(iDesiredQuestions):

	if bStop:
		break

	sQIdx = aQuestionShuffler[iQIdx]

	os.system('clear')
	if not bShowOriginalQuestionNumber:
		print "Question %s of %d\n" % (iQIdx+1, iDesiredQuestions)
	print aQuestions[sQIdx]
	print "\n"
	print "Type your answer,"
	print "   or :k if you don't know (counted as wrong answer)"
	print "   or :s to skip and answer later (counted as wrong answer)"
	print "   or :q to abort and start assessment"

	while True:
		sMyAns = raw_input("> ")
		if len(sMyAns) > 0:
			break

	iAnsweredQuestions += 1
	if sMyAns.upper() != ":K" and sMyAns.upper() != ":S" and sMyAns.upper() != ":Q":
		aMyAnswers[sQIdx] = sMyAns.upper()
		sCorrectAns = aKeys[sQIdx]
		if sMyAns.strip().upper() == sCorrectAns.upper():
			iCorrect += 1
		else:
			aIncorrect.append(sQIdx)
	else:
		if sMyAns.upper() == ":Q":
			bStop = True
		else:
			aMyAnswers[sQIdx] = sMyAns.upper()
			aIncorrect.append(sQIdx)

# Assessment calculations

iTotalTime = time.time() - iStartTime
iAverageTimePerQuestion = iTotalTime / iAnsweredQuestions
fCorrectPercentage = iCorrect * 100 / iAnsweredQuestions 
sResult = "fail"
if fCorrectPercentage > iPassPercentage:
	sResult = "pass"

# Assessment

sAssessmentFilename = "%s-ASSESSMENT-%s.txt" % (sQuizName, time.strftime("%Y%m%d-%H%M"))
print "Session finished in %ds" % (iTotalTime)
print "Average duration per question %ds" % (iAverageTimePerQuestion)
print "Correct answers %d / %d (%.1f %%)" % (iCorrect, iAnsweredQuestions, fCorrectPercentage)
print "Result: %s" % (sResult)
print "\n"	
with open(sAssessmentFilename, 'w') as f:
	f.write("Date/time: %s\n" % (time.strftime("%Y-%m-%d %H:%M")))
	f.write("Session finished in %ds\n" % (iTotalTime))
	f.write("Correct answers %d / %d (%.1f %%)\n" % (iCorrect, iAnsweredQuestions, fCorrectPercentage))
	f.write("Result: %s\n" % (sResult))
	f.write("\nThe following are the questions that you incorrectly answered:\n")
	for sQIdx in aIncorrect:
		f.write("\nQUESTION %s\n" % (sQIdx))
		f.write(aQuestions[sQIdx])
		f.write("\n\n")
		f.write("Your answer: %s (incorrect)\n\n" % (aMyAnswers[sQIdx]))
	f.close()

print "Details have been saved to %s" % (sAssessmentFilename)
