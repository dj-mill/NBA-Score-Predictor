import bs4
import project
import pandas as pd
import csv
from urllib.request import urlopen as opener
from bs4 import BeautifulSoup as soup

# gets name of teams playing each other from cbs and checks stats for each team
def todays_games(update):
  #creates a new csv
  if update == True:      
    games = 'https://www.cbssports.com/nba/scoreboard/'
    uClient = opener(games)
    todays_games = uClient.read()
    uClient.close()

    todays_soup = soup(todays_games, "html.parser")
    team_names = todays_soup.findAll("a", {"class": "team"})
    games = []
    #loop creates a 2D list of each game inside the list of games
    for i in range(len(team_names) // 2):
      games.append([])
    for i in range(len(team_names) // 2):
      for j in range(len(team_names)):
        if j % 2 == 0 and j != 0:
          if i == len(team_names) // 2:
            break
          else:
            i += 1
        games[i].append(team_names[j].text)
      break
    #makes a prediction for each game based on their collected stats
    todays_games = []
    for i in range(len(games)):
      away_team = games[i][0]
      away_season = project.webpage(away_team)
      away_record, away_scored, away_allowed = project.simple_stats(away_season, "away")
      #print("Away:", away_team + "\n" + "Record:", str(away_record) + "\nPTS/G: " + str(away_scored) + " \nOPTS/G: " + str(away_allowed)) 

      home_team = games[i][1]
      home_season = project.webpage(home_team)
      home_record, home_scored, home_allowed = project.simple_stats(home_season, "home")
      #print("Home:", home_team + "\n" + "Record:", str(home_record) + "\nPTS/G: " + str(home_scored) + " \nOPTS/G: " + str(home_allowed))
      
      away_info, home_info = project.results(away_team, away_season, away_record, away_scored, away_allowed, home_team, home_season, home_record, home_scored, home_allowed)

      todays_games.append(away_info)
      todays_games.append(home_info)
    #organizes data into a table format
    data_frame = pd.DataFrame(todays_games, columns = ['Team', 'Record(L 15)', 'PTS/G', 'OPTS/G', 'CI', 'Win%', 'PTS'])
    data_frame.to_csv('Todays_games.csv', index = False, encoding = 'utf-8')
    print(data_frame)
  else:
    #prints out the previously made csv in a table format
    f = open('Todays_games.csv', 'r')
    data = list(csv.reader(f))
    f.close()
    i = 0
    for row in data:
      print("  ".join(row))
      if i % 2 == 0 and i != 0:
        print("")
      i += 1
