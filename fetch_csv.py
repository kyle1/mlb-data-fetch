import csv
import requests
from random import randint
from time import sleep
from dateutil import tz
from pytz import timezone
import pytz
from datetime import datetime
import math

date_ranges = [
    {'season': 2005, 'start_date': '04/03/2005', 'end_date': '10/26/2005'},
    {'season': 2006, 'start_date': '04/02/2006', 'end_date': '10/27/2006'},
    {'season': 2007, 'start_date': '04/01/2007', 'end_date': '10/28/2007'},
    {'season': 2008, 'start_date': '03/25/2008', 'end_date': '10/29/2008'},
    {'season': 2009, 'start_date': '04/05/2009', 'end_date': '11/04/2009'},
    {'season': 2010, 'start_date': '04/04/2010', 'end_date': '11/01/2010'},
    {'season': 2011, 'start_date': '03/31/2011', 'end_date': '10/28/2011'},
    {'season': 2012, 'start_date': '03/28/2012', 'end_date': '10/28/2012'},
    {'season': 2013, 'start_date': '03/31/2013', 'end_date': '10/30/2013'},
    {'season': 2014, 'start_date': '03/22/2014', 'end_date': '10/29/2014'},
    {'season': 2015, 'start_date': '04/05/2015', 'end_date': '11/01/2015'},
    {'season': 2016, 'start_date': '04/03/2016', 'end_date': '11/02/2016'},
    {'season': 2017, 'start_date': '04/02/2017', 'end_date': '11/01/2017'},
    {'season': 2018, 'start_date': '03/29/2018', 'end_date': '10/28/2018'},
    {'season': 2019, 'start_date': '03/28/2019', 'end_date': datetime.today().strftime('%m/%d/%Y')}]

# Teams
def export_team_data(cols, path):
    with open(path + "/Team.csv", mode="w", newline="\n") as f:
        f = csv.writer(f)
        f.writerow(cols)
        url = "https://statsapi.mlb.com/api/v1/teams?sportId=1"
        print("Getting team data from " + url)
        teams = requests.get(url).json()
        for team in teams['teams']:
            row = []
            if "TeamID" in cols:
                row.append(team['id'])
            if "Name" in cols:
                row.append(team['name'])
            if "VenueID" in cols:
                row.append(team['venue']['id'])
            if "TeamCode" in cols:
                row.append(team['teamCode'])
            if "Abbreviation" in cols:
                row.append(team['abbreviation'])
            if "TeamName" in cols:
                row.append(team['teamName'])
            if "LocationName" in cols:
                row.append(team['locationName'])
            if "LeagueID" in cols:
                row.append(team['league']['id'])
            if "DivisionID" in cols:
                row.append(team['division']['id'])
            f.writerow(row)


def export_venue_data(cols, path):
    with open(path + "/Venue.csv", mode="w", newline="\n") as f:
        f = csv.writer(f)
        f.writerow(cols)
        url = "https://statsapi.mlb.com/api/v1/venues"
        print("Getting venue data from " + url)
        venues = requests.get(url).json()    
        for venue in venues["venues"]:
            row = []
            if "VenueID" in cols:
                row.append(venue["id"])
            if "Name" in cols:
                row.append(venue["name"])
            f.writerow(row)


# Players
def export_player_data(season, cols, path):
    with open(path + "/Player" + str(season) + ".csv", mode="w", newline="\n") as f:
        f = csv.writer(f)
        f.writerow(cols)
        url = "https://statsapi.mlb.com/api/v1/sports/1/players?season=" + str(season)
        print("Getting player data from " + url)
        players = requests.get(url).json()
        for player in players['people']:
            row = []
            if "PlayerID" in cols:
                row.append(player['id'])
            if "Season" in cols:
                row.append(season)
            if "FullName" in cols:
                row.append(player['fullName'])
            if "FirstName" in cols:
                row.append(player['firstName'])
            if "LastName" in cols:
                row.append(player['lastName'])
            if "BirthDate" in cols:
                row.append(player['birthDate'])
            if "Age" in cols:
                row.append(player['currentAge'])
            if "Height" in cols:
                row.append(player['height'])
            if "Weight" in cols:
                row.append(player['weight'])
            if "TeamID" in cols:
                if ('id' in player['currentTeam']):
                    row.append(player['currentTeam']['id'])
                else:
                    row.append("")
            if "Position" in cols:
                row.append(player['primaryPosition']['abbreviation'])
            if "DebutDate" in cols:
                row.append(player['mlbDebutDate'])
            if "BatSide" in cols:
                row.append(player['batSide']['code'])
            if "PitchHand" in cols:
                row.append(player['pitchHand']['code'])
            f.writerow(row)


# Schedule
def export_schedule_data(season, cols, path):
    with open(path + "/Schedule" + str(season) + ".csv", mode="w", newline="\n") as f:
        f = csv.writer(f)
        f.writerow(cols)

        #date_format = xlwt.XFStyle()
        #date_format.num_format_str = 'yyyy/mm/dd h:mm'    
        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz('America/Los_Angeles')

        for date_range in date_ranges:
            if date_range['season'] == season:
                start_date = date_range['start_date']
                end_date = date_range['end_date']

        url = "https://statsapi.mlb.com/api/v1/schedule?startDate=" + start_date + "&endDate=" + end_date + "&sportId=1"
        print("Getting schedule data from " + url)
        schedule = requests.get(url).json()

        game_ids = []
        for date in schedule['dates']:
            for game in date['games']:
                series_desc = game['seriesDescription']
                if "Training" not in series_desc and "Exhibition" not in series_desc and "All-Star" not in series_desc and game['status']['codedGameState'] == 'F' and game['gamePk'] not in game_ids:
                    row = []
                    if "GameID" in cols:
                        row.append(game['gamePk'])
                    if "GameDate" in cols:
                        utc = datetime.strptime(game['gameDate'], '%Y-%m-%dT%H:%M:%SZ')
                        utc = utc.replace(tzinfo=from_zone)
                        pst = utc.astimezone(to_zone)
                        pst = pst.replace(tzinfo=None)
                        #sheet.write(game_counter, col_count, pst, date_format)
                        row.append(pst) #todo: check how the date is formatted in file
                    if "AwayTeamID" in cols:
                        row.append(game['teams']['away']['team']['id'])
                    if "HomeTeamID" in cols:
                        row.append(game['teams']['home']['team']['id'])
                    if "VenueID" in cols:
                        row.append(game['venue']['id'])
                    f.writerow(row)
                    game_ids.append(game['gamePk'])


# Games
def export_game_data(season, cols, path):
    with open(path + "/Game" + str(season) + ".csv", mode="w", newline="\n") as f:
        f = csv.writer(f)
        f.writerow(cols)

        #date_format = xlwt.XFStyle()
        #date_format.num_format_str = 'yyyy/mm/dd h:mm'    
        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz('America/Los_Angeles')

        for date_range in date_ranges:
            if date_range['season'] == season:
                start_date = date_range['start_date']
                end_date = date_range['end_date']

        url = "https://statsapi.mlb.com/api/v1/schedule?startDate=" + start_date + "&endDate=" + end_date + "&sportId=1"
        print("Getting game data from " + url)
        games = requests.get(url).json()

        game_ids = []
        game_counter = 1
        for date in games['dates']:
            for game in date['games']:
                series_desc = game['seriesDescription']
                if "Training" not in series_desc and "Exhibition" not in series_desc and "All-Star" not in series_desc and game['status']['codedGameState'] == 'F' and game['gamePk'] not in game_ids:
                    row = []
                    # if game['status']['detailedState'] == 'Completed Early':
                    #     finished_early_ids.append(game['gamePk'])

                    if "GameID" in cols:
                        row.append(game['gamePk'])
                    if "Season" in cols:
                        row.append(game['seasonDisplay'])
                    if "GameDate" in cols:
                        utc = datetime.strptime(game['gameDate'], '%Y-%m-%dT%H:%M:%SZ')
                        utc = utc.replace(tzinfo=from_zone)
                        pst = utc.astimezone(to_zone)
                        pst = pst.replace(tzinfo=None)
                        #sheet.write(game_counter, col_count, pst, date_format)
                        row.append(pst)
                    if "Status" in cols:
                        row.append(game['status']['detailedState'])
                    if "AwayTeamID" in cols:
                        row.append(game['teams']['away']['team']['id'])
                    if "AwayTeamScore" in cols:
                        row.append(game['teams']['away']['score'])
                    if "AwayTeamRecordWins" in cols:
                        row.append(game['teams']['away']['leagueRecord']['wins'])
                    if "AwayTeamRecordLosses" in cols:
                        row.append(game['teams']['away']['leagueRecord']['losses'])
                    if "AwayTeamRecordPct" in cols:
                        row.append(game['teams']['away']['leagueRecord']['pct'])
                    if "HomeTeamID" in cols:
                        row.append(game['teams']['home']['team']['id'])
                    if "HomeTeamScore" in cols:
                        row.append(game['teams']['home']['score'])
                    if "HomeTeamRecordWins" in cols:
                        row.append(game['teams']['home']['leagueRecord']['wins'])
                    if "HomeTeamRecordLosses" in cols:
                        row.append(game['teams']['home']['leagueRecord']['losses'])
                    if "HomeTeamRecordPct" in cols:
                        row.append(game['teams']['away']['leagueRecord']['pct'])
                    if "VenueID" in cols:
                        row.append(game['venue']['id'])
                    if "DayNight" in cols:
                        row.append(game['dayNight'])
                    if "GamesInSeries" in cols:
                        row.append(game['gamesInSeries'])
                    if "SeriesGameNumber" in cols:
                        row.append(game['seriesGameNumber'])
                    if "SeriesDescription" in cols:
                        row.append(game['seriesDescription'])
                    f.writerow(row)
                    game_ids.append(game['gamePk'])


# Play By Play
def export_pbp_data(season, cols, min_sec, max_sec, path):
    with open(path + "/PlayByPlay" + str(season) + ".csv", mode="w", newline="\n") as f:
        f = csv.writer(f)
        f.writerow(cols)
        for date_range in date_ranges:
            if date_range['season'] == season:
                start_date = date_range['start_date']
                end_date = date_range['end_date']

        url = "https://statsapi.mlb.com/api/v1/schedule?startDate=" + start_date + "&endDate=" + end_date + "&sportId=1"
        print("Getting game data from " + url)
        games = requests.get(url).json()
        game_ids = []
        for date in games['dates']:
            for game in date['games']:
                series_desc = game['seriesDescription']
                if "Training" not in series_desc and "Exhibition" not in series_desc and "All-Star" not in series_desc and game['status']['codedGameState'] == 'F' and game['gamePk'] not in game_ids:
                    game_ids.append(game['gamePk'])

        pbp_counter = 1
        game_counter = 1
        print("Getting play-by-play data for " + str(len(game_ids)) + " games...")
        for game_id in game_ids:
            pbp = requests.get("https://statsapi.mlb.com/api/v1/game/" + str(game_id) + "/playByPlay").json()
            for play in pbp['allPlays']:
                row = []
                if 'event' in play['result'] and 'eventType' in play['result']:
                    if "PlayByPlayID" in cols:
                        row.append(pbp_counter)
                    if "GameID" in cols:
                        row.append(game_id)
                    if "BatterID" in cols:
                        row.append(play['matchup']['batter']['id'])
                    if "BatSide" in cols:
                        row.append(play['matchup']['batSide']['code'])
                    if "PitcherID" in cols:
                        row.append(play['matchup']['pitcher']['id'])
                    if "PitchHand" in cols:
                        row.append(play['matchup']['pitchHand']['code'])
                    if "MenOnBase" in cols:
                        row.append(play['matchup']['splits']['menOnBase'])
                    if "Event" in cols:
                        row.append(play['result']['event'])
                    if "EventType" in cols:
                        row.append(play['result']['eventType'])
                    if "IsScoringPlay" in cols:
                        if play['about']['isScoringPlay'] == True:
                            row.append(1)
                        else:
                            row.append(0)
                    if "AwayTeamScore" in cols:
                        row.append(play['result']['awayScore'])
                    if "HomeTeamScore" in cols:
                        row.append(play['result']['homeScore'])
                    if "AtBatIndex" in cols:
                        row.append(play['about']['atBatIndex'])
                    if "HalfInning" in cols:
                        row.append(play['about']['halfInning'])
                    if "Inning" in cols:
                        row.append(play['about']['inning'])
                    if "Outs" in cols:
                        row.append(play['count']['outs'])
                    f.writerow(row)
                    pbp_counter += 1
            print(str("Finished writing game " + str(game_id) + ". " + str(game_counter) + " out of " + str(len(game_ids)) + " games finished."))
            game_counter += 1
            sleep(randint(min_sec,max_sec))