import pandas as pd
import numpy as np

def maxLateness(time1, time2):
    time1 = time1.split(":")
    hour1 = int(time1[0])
    minute1 = int(time1[1])
    second1 = int(time1[2])
    lateSeconds1 = hour1 * 60**2 + minute1 * 60 + second1

    if time2 != None:
        time2 = time2.split(":")
        hour2 = int(time2[0])
        minute2 = int(time2[1])
        second2 = int(time2[2])
        lateSeconds2 = hour2 * 60**2 + minute2 * 60 + second2 
        if lateSeconds1 > lateSeconds2:
            maxHour = hour1
            maxMinute = minute1
            maxSecond = second1
        else:
            maxHour = hour2
            maxMinute = minute2
            maxSecond = second2
    else:
            maxHour = hour1
            maxMinute = minute1
            maxSecond = second1

    # Remove 30 minutes to allow for a 30 minute grace window
    if maxMinute < 30:
         maxHour -= 1
         maxMinute = (60 - 30) + maxMinute
    else:
         maxMinute = maxMinute - 30
    # Can comment this out if you don't want a grace window
    return maxHour, maxMinute, maxSecond
     

def graceDaysUsed(maxHour):

    graceDays = 0
    while maxHour >= 0:
         graceDays += 1
         maxHour -= 24

    return graceDays

class genGradebookGracedays:
     def __init__(self, rosterLoc: str):
          self.roster = pd.read_csv(rosterLoc)
          self.gradebook = self.roster[["Last Name", "Preferred/First Name", "Email"]].set_index("Email")
          self.gracedays = self.roster[["Last Name", "Preferred/First Name", "Email"]].set_index("Email")
          self.gracedays["Remaining"] = 8   #Update this value if initial grace days is something else!

     def updateGraceDays(self, hwNum: int, writtenLoc: str, progLoc: str = None) -> pd.DataFrame:
          writtenData = pd.read_csv(writtenLoc).set_index("Email")
          self.gracedays[f"hw{hwNum}WriteLate"] = writtenData["Lateness (H:M:S)"].fillna("00:00:00")

          if progLoc != None:
               progData = pd.read_csv(progLoc).set_index("Email")
               self.gracedays[f"hw{hwNum}ProgLate"] = progData["Lateness (H:M:S)"].fillna("00:00:00")
               self.gracedays[f"hw{hwNum}Latness"] = self.gracedays[[f"hw{hwNum}WriteLate", f"hw{hwNum}ProgLate"]].apply(lambda x: graceDaysUsed(maxLateness(x[f"hw{hwNum}WriteLate"], x[f"hw{hwNum}ProgLate"])[0]), axis=1)
          else:
               self.gracedays[f"hw{hwNum}Latness"] = self.gracedays[[f"hw{hwNum}WriteLate"]].apply(lambda x: graceDaysUsed(maxLateness(x[f"hw{hwNum}WriteLate"], None)[0]), axis = 1)
          self.gracedays["Remaining"] = self.gracedays["Remaining"] - self.gracedays[f"hw{hwNum}Latness"]

          # NEED TO ADD A PENALTY AND GRACE DAY UPDATE FOR STUDENTS WHO HIT NEGATIVE GRACE DAYS.

          return self.gracedays
     
     def updateGradebook(self, hwNum: int, writtenLoc: str, progLoc: str = None) -> pd.DataFrame:
          writtenData = pd.read_csv(writtenLoc).set_index("Email")
          self.gradebook[f"hw{hwNum}Write"] = writtenData["Total Score"].fillna(0)
          writtenTotal = writtenData["Max Points"].iloc[1]
          if (writtenData['Status'] == "Ungraded").any():
               print(f"Warning some written submissions in hw {hwNum} are ungraded!!!") 
          
          if progLoc != None:
               progData = pd.read_csv(progLoc).set_index("Email")
               self.gradebook[f"hw{hwNum}Prog"] = progData["Total Score"].fillna(0)
               progTotal = progData["Max Points"].iloc[1]
               if (progData['Status'] == "Ungraded").any():
                    print(f"Warning some programming submissions in hw {hwNum} are ungraded!!!") 
          
               self.gradebook[f"hw{hwNum} Percent"] = 100 * (self.gradebook[f"hw{hwNum}Write"] + self.gradebook[f"hw{hwNum}Prog"])/(writtenTotal + progTotal)
          
          else:
               self.gradebook[f"hw{hwNum} Percent"] = 100 * (self.gradebook[f"hw{hwNum}Write"])/writtenTotal

          return self.gradebook
     
     def addQuizScore(self, quizNum: int, quizLoc: str) -> pd.DataFrame:
          if self.gradebook is None:
               self.gradebook = self.roster[["Last Name", "Preferred/First Name", "Email"]].set_index("Email")

          quizData = pd.read_csv(quizLoc).set_index("Email")
          quizTotal = quizData["Max Points"].iloc[1]
          self.gradebook[f"quiz {quizNum} percent"] = 100 * quizData["Total Score"].fillna(0)/quizTotal
          
          if (quizData['Status'] == "Ungraded").any():
               print(f"Warning some quiz submissions in quiz {quizNum} are ungraded!!!") 

          return self.gradebook
     
     def addExamScore(self, examNum: int, examLoc: str) -> pd.DataFrame:
          if self.gradebook is None:
               self.gradebook = self.roster[["Last Name", "Preferred/First Name", "Email"]].set_index("Email")

          examData = pd.read_csv(examLoc).set_index("Email")
          examTotal = examData["Max Points"].iloc[1]
          self.gradebook[f"exam {examNum} percent"] = 100 * examData["Total Score"].fillna(0)/examTotal
          
          if (examData['Status'] == "Ungraded").any():
               print(f"Warning some exam submissions in exam {examNum} are ungraded!!!") 

          return self.gradebook
     



if __name__ == "__main__":

     rosterLoc = "roster/CourseRosters_M25_Selected_06.10.2025.csv"
               
     hw1WriteLoc = "homework/Homework_1_Written_scores.csv"
     hw1ProgLoc = "homework/Homework_1_Programming_scores.csv" # Can be None if no programming

     hw2WriteLoc = "homework/Homework_2_Written_scores.csv"
     hw2ProgLoc = "homework/Homework_2_Programming_scores.csv" # Can be None if no programming

     hw3WriteLoc = "homework/Homework_3_Written_scores.csv"
     hw3ProgLoc = "homework/Homework_3_Programming_scores.csv" # Can be None if no programming

     hw4WriteLoc = "homework/Homework_4_Written_scores.csv"
     hw4ProgLoc = "homework/Homework_4_Programming_scores.csv" # Can be None if no programming     

     hw5WriteLoc = "homework/Homework_5_Written_scores.csv"
     hw5ProgLoc = "homework/Homework_5_Programming_scores.csv" # Can be None if no programming     

     hw6WriteLoc = None
     hw6ProgLoc = None # Can be None if no programming     

     hw7WriteLoc = None
     hw7ProgLoc = None # Can be None if no programming     

     hw8WriteLoc = None
     hw8ProgLoc = None # Can be None if no programming     

     quiz1Loc = "quiz/Quiz_Week_1_scores.csv"
     quiz2Loc = "quiz/Quiz_Week_2_scores.csv"
     exam1Loc = "quiz/Exam_1_scores.csv"   # Exam 1 
     quiz3Loc = None 
     quiz4Loc = None
     exam2Loc = None   # Exam 2

               
     generated = genGradebookGracedays(rosterLoc)
     
     
     homeworkCount = 5
     for i in range(homeworkCount):
          i += 1
          print(f"Processing homework {i}!")
          gradebook = generated.updateGradebook(i, globals()[f"hw{i}WriteLoc"], globals()[f"hw{i}ProgLoc"])
          gracedays = generated.updateGraceDays(i, globals()[f"hw{i}WriteLoc"], globals()[f"hw{i}ProgLoc"])

     quizCount = 2
     for i in range(quizCount):
          i += 1
          print(f"Processing quiz {i}!")
          gradebook = generated.addQuizScore(i, globals()[f"quiz{i}Loc"])

     examCount = 1
     for i in range(examCount):
          i += 1
          print(f"Processing exam {i}!")
          gradebook = generated.addExamScore(i, globals()[f"exam{i}Loc"])


     
     
     # gradebook = generated.updateGradebook(1, hw1WriteLoc, hw1ProgLoc)
     # gracedays = generated.updateGradebook(1, hw1WriteLoc, hw1ProgLoc)
     # gradebook = generated.updateGradebook(2, hw2WriteLoc, hw2ProgLoc)
     # gracedays = generated.updateGradebook(2, hw2WriteLoc, hw2ProgLoc)


     gracedays.to_csv("gracedays.csv")
     gradebook.to_csv("gradebook.csv")



     

     
     
          
    





