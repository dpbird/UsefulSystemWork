Grace Day and Gradebook Generator ReadMe

The file must be stored in a directory with the following subdirectories:
- homework: Where downloaded csv homework grades from Gradescope are stored
- quiz (OPTIONAL): Where downloaded csv quiz/exam grades from Gradescope are stored
- roster: Where the downloaded csv roster from S3 are stored

HOW TO USE:
Make your chances under the "Make your updates here" comment:
- graceDayCount - The initial number of grace days your course provides.
- hwXWriteLoc and hwXProgLoc - The file paths for your written and programming csvs which you downloaded from Gradescope for the corresponding homework X. 
hwXProg Loc is optional if you don't have a programming, if not required, set it to 'None'
- quizXLoc and examXloc - The file paths for your quizzes and exams grades csvs which you have downloaded from Gradescope. If you don't have quizzes or exams then feel free to not use these, you can get the program to ignore them with a future variable, just set these to 'None'
- homeworkCount - The number of homework which you want the model to process. For example if you have 5 homework and have provided 5 file locations you should set this to 5 (who would have guessed :P)
- quizCount - The number of quizzes which you want your model to process, make sure you have provided the file locations for all of the quizzes which you want to process.
- examCount - The number of exams which you want your model to process, make sure you have provided the file locations for all of the exams which you want to process. 

Grace Days:
The program will generate grace days and will also prompt you if you want to penalize students who sumbit late with 0 grace days remaining. Follow the prompts:
- "What is the penalty per day late?": You have two options here:
    - Give it a value between 0 and 1, for example if the student loses 20% every late day then put 0.2.  
    - Give it 'manual' - this will overwrite the method to let you set the penalty for each student yourself. Useful if you don't have a fixed per day penalty.
- "(Y/N) Apply penalty to late penalty to Homework X of STUDENTNAME":
    - Y - The penalty will be applied, or, if you are in 'manual mode' you will be prompted what the penalty will be. At the end of penalizing the gradebook it sets the students grace days to 0, so that these negative grace days don't follow forward to penalize future homework.
    - N - No penalty will be applied to that student and it will set the students grace days count to 0. This is useful if you have ODR students with permission to use as many grace days as they want.
- (Manual Mode Only:) "Penalty percentage applied to Homework X for STUDENT NAME who submitted Y day(s) late?
    - Give it a value between 0 and 1 which represents the percentage which will be applied. If you put 0.7 this means that the student will get 70% of their score.

Output:
It will output the files as gradebook.csv and gracedays.csv