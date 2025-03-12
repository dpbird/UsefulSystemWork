import numpy as np
import pandas as pd
import os


def getAndrewEmail(emails):
    emails = emails.split(",")
    for email in emails:
        if "@andrew.cmu.edu" in email:
            return email
    print(f"No Andrew email address found in {emails}")   
    return None



def generatePollResults(polls, outputCSV, requiredPercent):
    for poll in polls:
        pollName = poll.split("-")[2]
        polldf = pd.read_csv(f"polls/{poll}")


        polldflen = polldf[polldf["emails"].isna()==True].index[0]
        polldf = polldf.iloc[0:polldflen]


        polldf["Andrew Email"] = polldf["emails"].map(lambda x: getAndrewEmail(x))
        polldf = polldf.drop(["emails", "vote", "name"], axis=1).set_index("Andrew Email")
        polldf[f"{pollName}"] = 1 
        outputCSV[f"{pollName}"] = polldf[f"{pollName}"]
        outputCSV = outputCSV.fillna(0)

        outputCSV["Total Poll Score"] += outputCSV[f"{pollName}"]
        

    outputCSV["Total Poll Score"] = outputCSV["Total Poll Score"]/len(polls)*100 

    if requiredPercent != None:
        outputCSV["Total Poll Score"] = outputCSV["Total Poll Score"].apply(lambda x: 100 if x >= requiredPercent else x)


    outputCSV.to_csv(f"output/Piazza Poll Grades.csv")

if __name__ == "__main__":
    requiredPercent = None
    
    rosterCSV = os.listdir("roster")[0]
    roster = pd.read_csv(f"roster/{rosterCSV}")
    outputCSV = roster[["Last Name","Preferred/First Name","Email"]].set_index("Email")
    outputCSV["Total Poll Score"] = 0 

    polls = os.listdir('polls')

    generatePollResults(polls, outputCSV, requiredPercent)


