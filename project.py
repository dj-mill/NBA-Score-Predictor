import statistics
import random
import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

# league_average is NBA average of points in a game
league_average = 111.3
# sample size being examined, 15 = past 15 home or away games for team
sample = 15

#checks if team name is in NBA
def team_check(team):
  if team != "76ers":
      team = team.lower().title()
  if team in NBA:
    return team
  else:
    return "Team name not found. Try again"

#accesses website for the selected team
def webpage(team):
  team_games = "https://www.basketball-reference.com/teams/" + NBA[team] + "/2020_games.html"

  uClient = uReq(team_games)
  team_page = uClient.read()
  uClient.close()

  team_soup = soup(team_page, "html.parser")
  season = team_soup.findAll("tr")
  return season

#gives simple stats of record, points, opponent points over the given sample size of games
def simple_stats(season, location):
  game_info = []
  win_count = 0
  loss_count = 0
  points_scored = 0
  opp_scored = 0
  for game in reversed(season):
    game_info = game.findAll("td")
    if len(game_info) == 0:
      continue
    arena = (game_info[4].text)
    result = (game_info[6].text)
    if game_info[8].text == "":
      continue
    if game_info[9].text =="":
      continue
    if location == "away":
      if arena == "@":
        points_scored += int(game_info[8].text)
        opp_scored += int(game_info[9].text)
        if result == "W":
          win_count += 1
        elif result == "L":
          loss_count += 1
        else:
          continue
        if win_count + loss_count == sample:
          record = (win_count, loss_count)
          break
    else:
      if arena == "":
        points_scored += int(game_info[8].text)
        opp_scored += int(game_info[9].text)
        if result == "W":
          win_count += 1
        elif result == "L":
          loss_count += 1
        else:
          continue
        if win_count + loss_count == sample:
          record = (win_count, loss_count)
          break
  points_scored = round(int(points_scored) / sample, 1)
  opp_scored = round(int(opp_scored) / sample, 1)
  return record, points_scored, opp_scored

#calculates standard error of each score for both teams
def standard_error(season, location):
  game_info = []
  games = []
  standard_deviation = 0
  for game in reversed(season):
    game_info = game.findAll("td")
    if len(game_info) == 0 or game_info[8].text == "":
      continue
    if location == "away":
      if game_info[4].text == "@":
        games.append(int(game_info[8].text))
        if len(games) == sample:
          standard_deviation = statistics.stdev(games)
          break
        else:
          continue
      else:
        continue
    else:
      if game_info[4].text == "":
        games.append(int(game_info[8].text))
        if len(games) == sample:
          standard_deviation = statistics.stdev(games)
          break
        else:
          continue
      else:
        continue 
  standard_error = (standard_deviation * sample ** 0.5) / sample
  return standard_error

#creates a 99.7 confidence error based around the standard error 
def interval(mean, error):
  interval = round(error * 3)
  points_max = mean + interval
  points_min = mean - interval
  return points_max, points_min

# simulates a random score for each team based on their confidence interval, outputs predicted score and odds of a team winning the game
def final_stats(max_away, min_away, max_home, min_home):
  away_wins = 0
  home_wins = 0
  away_final_score = 0
  home_final_score = 0
  x = 1
  while x < 5000:
    random_away = random.randint(min_away, max_away)
    random_home = random.randint(min_home, max_home)
    if random_away > random_home:
      away_final_score += random_away
      home_final_score += random_home
      away_wins += 1
      x += 1
    elif random_home > random_away:
      away_final_score += random_away
      home_final_score += random_home
      home_wins += 1
      x += 1
    else:
      continue
  away_final_score = round(away_final_score / 5000)
  home_final_score = round(home_final_score / 5000)
  away_wins /= 50
  home_wins /= 50
  if home_wins == 100.0 or away_wins == 100.0:
    home_wins -= 0.1
    away_wins -= 0.1
  return away_final_score, home_final_score, away_wins, home_wins
#adjusts each teams scoring and formats the outputted results
def results(away_team, away_season, away_record, away_scored, away_allowed, home_team, home_season, home_record, home_scored, home_allowed):
  away_adjust = home_allowed / league_average
  away_scored = round(away_scored * away_adjust)

  home_adjust = away_allowed / league_average
  home_scored = round(home_scored * home_adjust)

  away_se = standard_error(away_season, "away")      
  home_se = standard_error(home_season, "home")

  max_points_away, min_points_away = interval(away_scored, away_se)

  max_points_home, min_points_home = interval(home_scored, home_se)
  print(away_team + " CI:(" + str(min_points_away) + "-" + str(max_points_away) + ")")
  print(home_team + " CI:(" + str(min_points_home) + "-" + str(max_points_home) + ")")
  away_final_score, home_final_score, away_wins, home_wins = final_stats(int(max_points_away), int(min_points_away), int(max_points_home), int(min_points_home))

  if away_wins > home_wins:
    print("The " + away_team + " have a " + str(away_wins) + "% chance of winning")
  else:
    print("The " + home_team + " have a " + str(home_wins) + "% chance of winning")
  if away_final_score == home_final_score:
    if away_wins > home_wins:
      away_final_score += 1
    else:
      home_final_score += 1

  print("Predicted Score: " + away_team + "-" + str(away_final_score) + " " + home_team + "-" + str(home_final_score) + "\n")
  return

#dictionary that converts each team's name into suitable format so that the team's url can be accessed
NBA = {
  "Hawks": "ATL",
  "Celtics": "BOS",
  "Nets": "BRK",
  "Hornets": "CHO",
  "Bulls": "CHI",
  "Cavaliers": "CLE",
  "Mavericks": "DAL",
  "Nuggets": "DEN",
  "Pistons": "DET",
  "Warriors": "GSW",
  "Rockets": "HOU",
  "Pacers": "IND",
  "Clippers": "LAC",
  "Lakers": "LAL",
  "Grizzlies": "MEM",
  "Heat": "MIA",
  "Bucks": "MIL",
  "Timberwolves": "MIN",
  "Pelicans": "NOP",
  "Knicks": "NYK",
  "Thunder": "OKC",
  "Magic": "ORL",
  "76ers": "PHI",
  "Suns": "PHO",
  "Trail Blazers": "POR",
  "Kings": "SAC",
  "Spurs": "SAS",
  "Raptors": "TOR",
  "Jazz": "UTA",
  "Wizards": "WAS"
}
