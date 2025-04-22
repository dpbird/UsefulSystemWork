import pandas as pd


file = pd.read_csv("submission_metadata.csv")

data = file[["Email", "First Name", "Last Name", "Status","Submission ID", "Question 1.1 Response", "Question 1.2 Response", "Question 1.3 Response"]]
data = data.set_index(["Email"])
data = data[data.Status != "Missing"]


def getPaperLink(s: str):
    s = s.replace("\n", " ")
    splitS = s.split(" ")
    if splitS[0] == "Other":
        # print("OTHER!")
        return pd.NA, pd.NA
    paperTitle = " ".join(splitS[:-1])
    paperLink = splitS[-1]
    # print(paperTitle, " PAPER LINK:", paperLink)

    return paperTitle, paperLink

data = data[data["Question 1.2 Response"].isna() == False]
# data["Question 1.2 Response"].apply(lambda x: print(x))
data["Paper Title"] = data.apply(lambda x: getPaperLink(x["Question 1.2 Response"])[0] if x["Question 1.2 Response"]!="Other (Please Specify in 1.3)" else getPaperLink(x["Question 1.3 Response"])[0], axis=1)
data["Paper Link"] = data.apply(lambda x: getPaperLink(x["Question 1.2 Response"])[1] if x["Question 1.2 Response"]!="Other (Please Specify in 1.3)" else getPaperLink(x["Question 1.3 Response"])[1], axis=1)

submissionURL = "https://www.gradescope.com/courses/937967/assignments/5641632/submissions/"

data["Link"] = data["Submission ID"].apply(lambda x: submissionURL + str(x)[:-2])


data[["First Name", "Last Name", "Question 1.1 Response", "Paper Title", "Paper Link", "Link"]].to_csv("Formatted Output.csv")