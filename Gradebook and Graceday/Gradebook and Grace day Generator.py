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


# maxHour, _, _ = maxLateness("00:29:00", "00:00:00")
# print(graceDaysUsed(maxHour))

class hwData:
     def __init__(self, hwNum: int, writtenLoc: str, progLoc: str, rosterLoc: str, gracedays: pd.DataFrame = None, gradebook: pd.DataFrame = None):
          self.hwNum = hwNum
          self.writtenLoc = writtenLoc
          self.progLoc = progLoc
          self.roster = pd.read_csv(rosterLoc)
          
          self.writtenData = pd.read_csv(writtenLoc).set_index("Email")
          self.progData = pd.read_csv(progLoc).set_index("Email")
          self.gradebook = gradebook
          self.gracedays = gracedays

     def updateGraceDays(self) -> pd.DataFrame:
          if self.gracedays is None:
               self.gracedays = self.roster[["Last Name", "Preferred/First Name", "Email"]].set_index("Email")
               # If the initial grace days is something else, change this value!
               self.gracedays["Remaining"] = 8
               
          self.gracedays[f"hw{self.hwNum}WriteLate"] = self.writtenData["Lateness (H:M:S)"].fillna("00:00:00")
          self.gracedays[f"hw{self.hwNum}ProgLate"] = self.progData["Lateness (H:M:S)"].fillna("00:00:00")
          self.gracedays[f"hw{self.hwNum}Latness"] = self.gracedays[[f"hw{self.hwNum}WriteLate", f"hw{self.hwNum}ProgLate"]].apply(lambda x: graceDaysUsed(maxLateness(x[f"hw{self.hwNum}WriteLate"], x[f"hw{self.hwNum}ProgLate"])[0]), axis=1)
          self.gracedays["Remaining"] = self.gracedays["Remaining"] - self.gracedays[f"hw{self.hwNum}Latness"]
          return self.gracedays
     

     def updateGradebook(self) -> pd.DataFrame:
          if self.gradebook is None:
               self.gradebook = self.roster[["Last Name", "Preferred/First Name", "Email"]].set_index("Email")
          
          self.gradebook[f"hw{self.hwNum}Write"] = self.writtenData["Total Score"].fillna(0)
          writtenTotal = self.writtenData["Max Points"].iloc[1]
          if (self.writtenData['Status'] == "Ungraded").any():
               print(f"Warning some written submissions in hw {self.hwNum} are ungraded!!!") 
          self.gradebook[f"hw{self.hwNum}Prog"] = self.progData["Total Score"].fillna(0)
          progTotal = self.progData["Max Points"].iloc[1]
          if (self.progData['Status'] == "Ungraded").any():
               print(f"Warning some programming submissions in hw {self.hwNum} are ungraded!!!") 
          
          self.gradebook[f"hw{self.hwNum} Percent"] = 100 * (self.gradebook[f"hw{self.hwNum}Write"] + self.gradebook[f"hw{self.hwNum}Prog"])/(writtenTotal + progTotal)

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
          

          

          

          
          

hw1 = hwData(1, "homework/Homework_1_Written_scores.csv", "homework/Homework_1_Programming_scores.csv",
             "roster/CourseRosters_M25_Selected_05.27.2025.csv")
gracedays = hw1.updateGraceDays()
gradebook = hw1.updateGradebook()

hw2 = hwData(2, "homework/Homework_2_Written_scores.csv", "homework/Homework_2_Programming_scores.csv",
             "roster/CourseRosters_M25_Selected_05.27.2025.csv", gracedays, gradebook)
gracedays = hw2.updateGraceDays()
gradebook = hw2.updateGradebook()

gradebook = hw2.addQuizScore(1, "quiz/Quiz_Week_1_scores.csv")
gradebook = hw2.addQuizScore(2, "quiz/Quiz_Week_2_scores.csv")

hw3 = hwData(3, "homework/Homework_3_Written_scores.csv", "homework/Homework_3_Programming_scores.csv",
             "roster/CourseRosters_M25_Selected_05.27.2025.csv", gracedays, gradebook)
gracedays = hw3.updateGraceDays()
gradebook = hw3.updateGradebook()

hw4 = hwData(4, "homework/Homework_4_Written_scores.csv", "homework/Homework_4_Programming_scores.csv",
             "roster/CourseRosters_M25_Selected_05.27.2025.csv", gracedays, gradebook)
gracedays = hw4.updateGraceDays()
gradebook = hw4.updateGradebook()






# hw3 = hwData(3, "homework/Homework_3_Written_scores.csv", "homework/Homework_3_Programming_scores.csv",
#              "roster/CourseRosters_M25_Selected_05.27.2025.csv", gracedays, gradebook)
# gracedays = hw3.updateGraceDays()
# gradebook = hw3.updateGradebook()
# print(gracedays.head(20))
gracedays.to_csv("gracedays.csv")
gradebook.to_csv("gradebook.csv")

     

     
     
          
    


# roster = pd.read_csv("roster/CourseRosters_M25_Selected_05.27.2025.csv")

# hw1Write = pd.read_csv("homework/Homework_1_Written_scores.csv").set_index("Email")
# hw1prog = pd.read_csv("homework/Homework_1_Programming_scores.csv").set_index("Email")

# hw2Write = pd.read_csv("homework/Homework_2_Written_scores.csv").set_index("Email")
# hw2prog = pd.read_csv("homework/Homework_2_Programming_scores.csv").set_index("Email")
# # hw3 = pd.read_csv("homework/")
# # hw3prog = pd.read_csv("homework/")
# # hw4 = pd.read_csv("homework/")
# # hw4prog = pd.read_csv("homework/")
# # hw5 = pd.read_csv("homework/")
# # hw5prog = pd.read_csv("homework/")

# quiz1 = pd.read_csv("quiz/Quiz_Week_1_scores.csv")

# gradebook = roster[["Last Name", "Preferred/First Name", "Email"]].set_index("Email")
# gracedays = gradebook.copy()
# gracedays["Remaining"] = 8

# # print(hw1.columns)

# gracedays["hw1WriteLate"] = hw1Write["Lateness (H:M:S)"].fillna("00:00:00")
# gracedays["hw1ProgLate"] = hw1prog["Lateness (H:M:S)"].fillna("00:00:00")
# gracedays["hw1Latness"] = gracedays[["hw1WriteLate","hw1ProgLate"]].apply(lambda x: graceDaysUsed(maxLateness(x["hw1WriteLate"], x["hw1ProgLate"])[0]), axis=1)
# gracedays["Remaining"] = gracedays["Remaining"] - gracedays["hw1Latness"]

# gracedays["hw2WriteLate"] = hw2Write["Lateness (H:M:S)"].fillna("00:00:00")
# gracedays["hw2ProgLate"] = hw2prog["Lateness (H:M:S)"].fillna("00:00:00")
# gracedays["hw2Latness"] = gracedays[["hw2WriteLate","hw2ProgLate"]].apply(lambda x: graceDaysUsed(maxLateness(x["hw2WriteLate"], x["hw2ProgLate"])[0]), axis=1)
# gracedays["Remaining"] = gracedays["Remaining"] - gracedays["hw2Latness"]

# homework = [1,2]
# for h in homework:
#      write = f"hw{h}WriteLate"
#      prog = f"hw{h}ProgLate"




# print(type(gracedays))








