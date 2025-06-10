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


class hwData:
     def __init__(self, hwNum: int, writtenLoc: str, progLoc: str, rosterLoc: str, gracedays: pd.DataFrame = None, gradebook: pd.DataFrame = None):
          self.hwNum = hwNum
          self.writtenLoc = writtenLoc
          self.progLoc = progLoc
          self.roster = pd.read_csv(rosterLoc)
          
          self.writtenData = pd.read_csv(writtenLoc).set_index("Email")
          if self.progLoc != None:
               self.progData = pd.read_csv(progLoc).set_index("Email")
          self.gradebook = gradebook
          self.gracedays = gracedays

     def updateGraceDays(self) -> pd.DataFrame:
          if self.gracedays is None:
               self.gracedays = self.roster[["Last Name", "Preferred/First Name", "Email"]].set_index("Email")
               # If the initial grace days is something else, change this value!
               self.gracedays["Remaining"] = 8
               
          self.gracedays[f"hw{self.hwNum}WriteLate"] = self.writtenData["Lateness (H:M:S)"].fillna("00:00:00")
          if self.progLoc != None:
               self.gracedays[f"hw{self.hwNum}ProgLate"] = self.progData["Lateness (H:M:S)"].fillna("00:00:00")
               self.gracedays[f"hw{self.hwNum}Latness"] = self.gracedays[[f"hw{self.hwNum}WriteLate", f"hw{self.hwNum}ProgLate"]].apply(lambda x: graceDaysUsed(maxLateness(x[f"hw{self.hwNum}WriteLate"], x[f"hw{self.hwNum}ProgLate"])[0]), axis=1)
          else:
               self.gracedays[f"hw{self.hwNum}Latness"] = self.gracedays[[f"hw{self.hwNum}WriteLate"]].apply(lambda x: graceDaysUsed(maxLateness(x[f"hw{self.hwNum}WriteLate"], None)[0]), axis = 1)
          self.gracedays["Remaining"] = self.gracedays["Remaining"] - self.gracedays[f"hw{self.hwNum}Latness"]

          # NEED TO ADD A PENALTY AND GRACE DAY UPDATE FOR STUDENTS WHO HIT NEGATIVE GRACE DAYS.

          return self.gracedays
     

     def updateGradebook(self) -> pd.DataFrame:
          if self.gradebook is None:
               self.gradebook = self.roster[["Last Name", "Preferred/First Name", "Email"]].set_index("Email")
          
          self.gradebook[f"hw{self.hwNum}Write"] = self.writtenData["Total Score"].fillna(0)
          writtenTotal = self.writtenData["Max Points"].iloc[1]
          if (self.writtenData['Status'] == "Ungraded").any():
               print(f"Warning some written submissions in hw {self.hwNum} are ungraded!!!") 
          
          if self.progLoc != None:
               self.gradebook[f"hw{self.hwNum}Prog"] = self.progData["Total Score"].fillna(0)
               progTotal = self.progData["Max Points"].iloc[1]
               if (self.progData['Status'] == "Ungraded").any():
                    print(f"Warning some programming submissions in hw {self.hwNum} are ungraded!!!") 
          
               self.gradebook[f"hw{self.hwNum} Percent"] = 100 * (self.gradebook[f"hw{self.hwNum}Write"] + self.gradebook[f"hw{self.hwNum}Prog"])/(writtenTotal + progTotal)
          
          else:
               self.gradebook[f"hw{self.hwNum} Percent"] = 100 * (self.gradebook[f"hw{self.hwNum}Write"])/writtenTotal

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

     rosterLoc = "roster/CourseRosters_M25_Selected_05.27.2025.csv"
               
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

               
               

     hw1 = hwData(1, hw1WriteLoc, hw1ProgLoc,
               rosterLoc)
     gracedays = hw1.updateGraceDays()
     gradebook = hw1.updateGradebook()

     hw2 = hwData(2, hw2WriteLoc, hw2ProgLoc,
               rosterLoc, gracedays, gradebook)
     gracedays = hw2.updateGraceDays()
     gradebook = hw2.updateGradebook()

     gradebook = hw2.addQuizScore(1, quiz1Loc)
     gradebook = hw2.addQuizScore(2, quiz2Loc)

     hw3 = hwData(3, hw3WriteLoc, hw3ProgLoc,
               rosterLoc, gracedays, gradebook)
     gracedays = hw3.updateGraceDays()
     gradebook = hw3.updateGradebook()

     gradebook = hw3.addExamScore(1, exam1Loc)

     hw4 = hwData(4, hw4WriteLoc, hw4ProgLoc,
               rosterLoc, gracedays, gradebook)
     gracedays = hw4.updateGraceDays()
     gradebook = hw4.updateGradebook()

     gradebook = hw3.addExamScore(1, exam1Loc)


     hw5 = hwData(5, hw5WriteLoc, hw5ProgLoc,
                  rosterLoc, gracedays, gradebook)
     gracedays = hw5.updateGraceDays()
     gradebook = hw5.updateGradebook()

     # hw4 = hwData(4, hw4WriteLoc, hw4ProgLoc,
     #              rosterLoc, gracedays, gradebook)
     # gracedays = hw4.updateGraceDays()
     # gradebook = hw4.updateGradebook()



     gracedays.to_csv("gracedays.csv")
     gradebook.to_csv("gradebook.csv")

     

     
     
          
    





