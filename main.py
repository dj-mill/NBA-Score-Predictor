import project
import automatic
x = True
# if update is true a new csv will be created, else the program will gather data from the previously made csv
update = True
while x == True:
  #Gives choice to predict all of today's games automatically or let the user manually input games
  choice = input("Automatically(a) or manually(m) predict today's games?")
  if choice == 'm':
    while x == True:
      away_team = input("Away: ")
      away_team = project.team_check(away_team)
      if away_team == "Team name not found. Try again":
        print(away_team)
        continue
      away_season = project.webpage(away_team)
      away_record, away_scored, away_allowed = project.simple_stats(away_season, "away")
      print("Record:" + str(away_record) + "\nPTS/G: " + str(away_scored) + " \nOPTS/G: " + str(away_allowed)) 

      while x == True:
        home_team = input("Home: ")
        home_team = project.team_check(home_team)
        if home_team == "Team name not found. Try again":
          print(home_team)
          continue
        home_season = project.webpage(home_team)
        home_record, home_scored, home_allowed = project.simple_stats(home_season, "home")
        print("Record:" + str(home_record) + "\nPTS/G:" + str(home_scored) + " \nOPTS/G:" + str(home_allowed))
        break

      project.results(away_team, away_season, away_record, away_scored, away_allowed, home_team, home_season, home_record, home_scored, home_allowed)
      next_game = input("Any more games? (y/n)")
      if next_game == "y":
        continue
      else:
        x = False
  elif choice == 'a':
    teams = automatic.todays_games(update)
    break
  else:
    continue
