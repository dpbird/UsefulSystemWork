import pandas as pd
import os


if __name__ == "__main__":
    rosters = list(os.walk("Rosters"))[0][-1]
    print(rosters)

    fullRoster = pd.read_csv(f"Rosters/{rosters[0]}")

    print(fullRoster.shape)
    for roster in rosters[1:]:
        fullRoster = pd.concat([fullRoster, pd.read_csv(f"Rosters/{roster}")])

    fullRoster.to_csv(f"Generated Full Roster {fullRoster.shape[0]} Students.csv")