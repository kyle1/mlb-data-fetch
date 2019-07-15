import xlwt
import requests
from random import randint
from time import sleep
from dateutil import tz
from pytz import timezone
import pytz
from datetime import datetime

# Players
def export_player_data(season):
    #get newest year to oldest so that we dont overwrite current teams with old teams
    book = xlwt.Workbook(encoding="utf-8")
    sheet = book.add_sheet("Player")
    cols = ["PlayerID", "FullName", "FirstName", "LastName", "BirthDate", "TeamID", "Position", "DebutDate", "BatSide", "PitchHand"]
    for i in range(len(cols)):
        sheet.write(0, i, cols[i])
    
    player_ids = []
    player_counter = 1
    url = "https://statsapi.mlb.com/api/v1/sports/1/players?season=" + str(season)
    print("Getting player data from " + url)
    players = requests.get(url).json()
    for player in players['people']:
        if player['id'] not in player_ids:
            sheet.write(player_counter, 0, player['id'])
            sheet.write(player_counter, 1, player['fullName'])
            sheet.write(player_counter, 2, player['firstName'])
            sheet.write(player_counter, 3, player['lastName'])
            sheet.write(player_counter, 4, player['birthDate'])
            sheet.write(player_counter, 5, player['currentTeam']['id'])
            sheet.write(player_counter, 6, player['primaryPosition']['abbreviation'])
            sheet.write(player_counter, 7, player['mlbDebutDate'])
            sheet.write(player_counter, 8, player['batSide']['code'])
            sheet.write(player_counter, 9, player['pitchHand']['code'])
            player_ids.append(player['id'])
            player_counter += 1
        sleep(10)
    book.save("data/" + season + "-Player.xls")

def export_venue_data():
    url = "https://statsapi.mlb.com/api/v1/venues"
    print("Getting venue data from " + url)
    venues = requests.get(url).json()
    book = xlwt.Workbook(encoding="utf-8")
    sheet = book.add_sheet("Venue")
    sheet.write(0, 0, "VenueID")
    sheet.write(0, 1, "Name")
    
    venue_counter = 1
    for venue in venues["venues"]:
        sheet.write(venue_counter, 0, venue["id"])
        sheet.write(venue_counter, 1, venue["name"])
        venue_counter += 1
    book.save("data/Venue.xls")

# Teams
def export_team_data():
    url = "https://statsapi.mlb.com/api/v1/teams?sportId=1"
    print("Getting team data from " + url)
    teams = requests.get(url).json()
    book = xlwt.Workbook(encoding="utf-8")
    sheet = book.add_sheet("Team")
    sheet.write(0, 0, "TeamID")
    sheet.write(0, 1, "Name")
    sheet.write(0, 2, "VenueID")
    sheet.write(0, 3, "TeamCode")
    sheet.write(0, 4, "Abbreviation")
    sheet.write(0, 5, "TeamName")
    sheet.write(0, 6, "LocationName")
    sheet.write(0, 7, "LeagueID")
    sheet.write(0, 8, "DivisionID")
    team_counter = 1
    for team in teams['teams']:
        sheet.write(team_counter, 0, team['id'])
        sheet.write(team_counter, 1, team['name'])
        sheet.write(team_counter, 2, team['venue']['id'])
        sheet.write(team_counter, 3, team['teamCode'])
        sheet.write(team_counter, 4, team['abbreviation'])
        sheet.write(team_counter, 5, team['teamName'])
        sheet.write(team_counter, 6, team['locationName'])
        sheet.write(team_counter, 7, team['league']['id'])
        sheet.write(team_counter, 8, team['division']['id'])
        team_counter += 1
    book.save('data/Team.xls')


# Schedule
def export_schedule_data():
    book = xlwt.Workbook(encoding="utf-8")
    sheet = book.add_sheet("Schedule")
    cols = ["GameID", "GameDate", "AwayTeamID", "HomeTeamID", "VenueID"]
    for i in range(len(cols)):
        sheet.write(0, i, cols[i])

    #url = "https://statsapi.mlb.com/api/v1/schedule?startDate=" + datetime.today().strftime('%m/%d/%Y') + "&endDate=10/10/2019&sportId=1"
    #url = "https://statsapi.mlb.com/api/v1/schedule?startDate=3/29/2018&endDate=10/28/2018&sportId=1"
    url = "https://statsapi.mlb.com/api/v1/schedule?startDate=3/28/2019&endDate=10/10/2019&sportId=1"
    schedule = requests.get(url).json()

    game_counter = 1
    for date in schedule['dates']:
        for game in date['games']:
            sheet.write(game_counter, 0, game['gamePk'])
            sheet.write(game_counter, 1, game['gameDate'])
            sheet.write(game_counter, 2, game['teams']['away']['team']['id'])
            sheet.write(game_counter, 3, game['teams']['home']['team']['id'])
            sheet.write(game_counter, 4, game['venue']['id'])
            game_counter += 1
    book.save("data/Schedule.xls")


# Games
def export_game_data(seasons):

    book = xlwt.Workbook(encoding="utf-8")
    sheet = book.add_sheet("Game")
    cols = ["GameID", "GameDate", "Status", "AwayTeamID", "AwayTeamScore", "AwayTeamRecordWins", "AwayTeamRecordLosses",
            "AwayTeamRecordPct", "HomeTeamID", "HomeTeamScore", "HomeTeamRecordWins", "HomeTeamRecordLosses", "HomeTeamRecordPct",
            "VenueID", "Season", "DayNight", "GamesInSeries", "SeriesGameNumber", "SeriesDescription"]
    for i in range(len(cols)):
        sheet.write(0, i, cols[i])

    date_format = xlwt.XFStyle()
    date_format.num_format_str = 'yyyy/mm/dd h:mm'    
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('America/Los_Angeles')

    finished_early_ids = []
    game_counter = 1
    for season in seasons:
        for date_range in date_ranges:
            if date_range['season'] == season:
                start_date = date_range['start_date']
                end_date = date_range['end_date']

        url = "https://statsapi.mlb.com/api/v1/schedule?startDate=" + start_date + "&endDate=" + end_date + "&sportId=1"
        print("Getting game data from " + url)
        games = requests.get(url).json()
        for date in games['dates']:
            for game in date['games']:
                if game['status']['codedGameState'] == 'F' and game['gamePk'] not in game_ids:

                    if game['status']['detailedState'] == 'Completed Early':
                        finished_early_ids.append(game['gamePk'])

                    sheet.write(game_counter, 0, game['gamePk'])

                    utc = datetime.strptime(game['gameDate'], '%Y-%m-%dT%H:%M:%SZ')
                    utc = utc.replace(tzinfo=from_zone)
                    pst = utc.astimezone(to_zone)
                    pst = pst.replace(tzinfo=None)
                    sheet.write(game_counter, 1, pst, date_format)

                    sheet.write(game_counter, 2, game['status']['detailedState'])
                    sheet.write(game_counter, 3, game['teams']['away']['team']['id'])
                    sheet.write(game_counter, 4, game['teams']['away']['score'])
                    sheet.write(game_counter, 5, game['teams']['away']['leagueRecord']['wins'])
                    sheet.write(game_counter, 6, game['teams']['away']['leagueRecord']['losses'])
                    sheet.write(game_counter, 7, game['teams']['away']['leagueRecord']['pct'])         
                    sheet.write(game_counter, 8, game['teams']['home']['team']['id'])
                    sheet.write(game_counter, 9, game['teams']['home']['score'])
                    sheet.write(game_counter, 10, game['teams']['home']['leagueRecord']['wins'])
                    sheet.write(game_counter, 11, game['teams']['home']['leagueRecord']['losses'])
                    sheet.write(game_counter, 12, game['teams']['home']['leagueRecord']['pct'])
                    sheet.write(game_counter, 13, game['venue']['id'])
                    sheet.write(game_counter, 14, game['seasonDisplay'])
                    sheet.write(game_counter, 15, game['dayNight'])
                    sheet.write(game_counter, 16, game['gamesInSeries'])
                    sheet.write(game_counter, 17, game['seriesGameNumber'])
                    sheet.write(game_counter, 18, game['seriesDescription'])
                    game_ids.append(game['gamePk'])
                    game_counter += 1
        sleep(10)
    book.save('data/Game.xls')


# Play By Play
def export_pbp_data(game_ids):
    print("Getting play-by-play data for " + str(len(game_ids)) + " games...")

    book = xlwt.Workbook(encoding="utf-8")
    sheet = book.add_sheet("PlayByPlay")
    cols = ["PlayByPlayID", "GameID", "BatterID", "BatSide", "BatterSplit", "PitcherID", "PitchHand", "PitcherSplit", "MenOnBase",
            "Event", "EventType", "IsScoringPlay", "AwayTeamScore", "HomeTeamScore", "AtBatIndex", "HalfInning", "Inning", "Outs"]
    for i in range(len(cols)):
        sheet.write(0, i, cols[i])
    pbp_counter = 1
    game_counter = 1
    game_ids = game_ids[:800] # One sheet cannot handle much more than 800 games of play-by-play data
    for game_id in game_ids:
        if game_counter > 800:
            return
        pbp = requests.get("https://statsapi.mlb.com/api/v1/game/" + str(game_id) + "/playByPlay").json()
        for play in pbp['allPlays']:
            if 'event' in play['result'] and 'eventType' in play['result']:
                sheet.write(pbp_counter, 0, pbp_counter)
                sheet.write(pbp_counter, 1, game_id)
                sheet.write(pbp_counter, 2, play['matchup']['batter']['id'])
                sheet.write(pbp_counter, 3, play['matchup']['batSide']['code'])
                sheet.write(pbp_counter, 4, play['matchup']['splits']['batter'])
                sheet.write(pbp_counter, 5, play['matchup']['pitcher']['id'])
                sheet.write(pbp_counter, 6, play['matchup']['pitchHand']['code'])
                sheet.write(pbp_counter, 7, play['matchup']['splits']['pitcher'])
                sheet.write(pbp_counter, 8, play['matchup']['splits']['menOnBase'])
                sheet.write(pbp_counter, 9, play['result']['event'])
                sheet.write(pbp_counter, 10, play['result']['eventType'])
                sheet.write(pbp_counter, 11, play['about']['isScoringPlay'])
                sheet.write(pbp_counter, 12, play['result']['awayScore'])
                sheet.write(pbp_counter, 13, play['result']['homeScore'])
                sheet.write(pbp_counter, 14, play['about']['atBatIndex'])
                sheet.write(pbp_counter, 15, play['about']['halfInning'])
                sheet.write(pbp_counter, 16, play['about']['inning'])
                sheet.write(pbp_counter, 17, play['count']['outs'])
                pbp_counter += 1
        print(str("Finished writing game " + str(game_id) + ". " + str(game_counter) + " out of " + str(len(game_ids)) + " games finished."))
        game_counter += 1
        sleep(randint(5,20))
    book.save('data/PlayByPlay.xls')


date_ranges = [
    {'season': '2005', 'start_date': '04/03/2005', 'end_date': '10/26/2005'},
    {'season': '2006', 'start_date': '04/02/2006', 'end_date': '10/27/2006'},
    {'season': '2007', 'start_date': '04/01/2007', 'end_date': '10/28/2007'},
    {'season': '2008', 'start_date': '03/25/2008', 'end_date': '10/29/2008'},
    {'season': '2009', 'start_date': '04/05/2009', 'end_date': '11/04/2009'},
    {'season': '2010', 'start_date': '04/04/2010', 'end_date': '11/01/2010'},
    {'season': '2011', 'start_date': '03/31/2011', 'end_date': '10/28/2011'},
    {'season': '2012', 'start_date': '03/28/2012', 'end_date': '10/28/2012'},
    {'season': '2013', 'start_date': '03/31/2013', 'end_date': '10/30/2013'},
    {'season': '2014', 'start_date': '03/22/2014', 'end_date': '10/29/2014'},
    {'season': '2015', 'start_date': '04/05/2015', 'end_date': '11/01/2015'},
    {'season': '2016', 'start_date': '04/03/2016', 'end_date': '11/02/2016'},
    {'season': '2017', 'start_date': '04/02/2017', 'end_date': '11/01/2017'},
    {'season': '2018', 'start_date': '03/29/2018', 'end_date': '10/28/2018'},
    {'season': '2019', 'start_date': '03/28/2019', 'end_date': datetime.today().strftime('%m/%d/%Y')}]

seasons = ['2019', '2018']
game_ids = []

#export_venue_data()
# sleep(10)
# export_team_data()
# sleep(10)
# export_player_data(seasons)
# sleep(10)
# export_schedule_data()
# sleep(10)
# export_game_data(seasons)
# sleep(10)
# export_pbp_data(game_ids)