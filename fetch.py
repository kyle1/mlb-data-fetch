import xlwt
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
    url = "https://statsapi.mlb.com/api/v1/teams?sportId=1"
    print("Getting team data from " + url)
    teams = requests.get(url).json()
    book = xlwt.Workbook(encoding="utf-8")
    sheet = book.add_sheet("Team")
    for i in range(len(cols)):
        sheet.write(0, i, cols[i])

    team_counter = 1
    for team in teams['teams']:
        col_count = 0
        if "TeamID" in cols:
            sheet.write(team_counter, col_count, team['id'])
            col_count += 1
        if "Name" in cols:
            sheet.write(team_counter, col_count, team['name'])
            col_count += 1
        if "VenueID" in cols:
            sheet.write(team_counter, col_count, team['venue']['id'])
            col_count += 1
        if "TeamCode" in cols:
            sheet.write(team_counter, col_count, team['teamCode'])
            col_count += 1
        if "Abbreviation" in cols:
            sheet.write(team_counter, col_count, team['abbreviation'])
            col_count += 1
        if "TeamName" in cols:
            sheet.write(team_counter, col_count, team['teamName'])
            col_count += 1
        if "LocationName" in cols:
            sheet.write(team_counter, col_count, team['locationName'])
            col_count += 1
        if "LeagueID" in cols:
            sheet.write(team_counter, col_count, team['league']['id'])
            col_count += 1
        if "DivisionID" in cols:
            sheet.write(team_counter, col_count, team['division']['id'])
            col_count += 1
        team_counter += 1
    book.save(path + "/Team.xls")


def export_venue_data(cols, path):
    url = "https://statsapi.mlb.com/api/v1/venues"
    print("Getting venue data from " + url)
    venues = requests.get(url).json()
    book = xlwt.Workbook(encoding="utf-8")
    sheet = book.add_sheet("Venue")
    for i in range(len(cols)):
        sheet.write(0, i, cols[i])
    
    venue_counter = 1
    for venue in venues["venues"]:
        col_count = 0
        if "VenueID" in cols:
            sheet.write(venue_counter, col_count, venue["id"])
            col_count += 1
        if "Name" in cols:
            sheet.write(venue_counter, col_count, venue["name"])
            col_count += 1
        venue_counter += 1
    book.save(path + "/Venue.xls")


# Players
def export_player_data(season, cols, path):
    book = xlwt.Workbook(encoding="utf-8")
    sheet = book.add_sheet("Player")
    for i in range(len(cols)):
        sheet.write(0, i, cols[i])
    player_counter = 1
    url = "https://statsapi.mlb.com/api/v1/sports/1/players?season=" + str(season)
    print("Getting player data from " + url)
    players = requests.get(url).json()
    for player in players['people']:
        col_count = 0
        if "PlayerID" in cols:
            sheet.write(player_counter, col_count, player['id'])
            col_count += 1
        if "Season" in cols:
            sheet.write(player_counter, col_count, season)
            col_count += 1
        if "FullName" in cols:
            sheet.write(player_counter, col_count, player['fullName'])
            col_count += 1
        if "FirstName" in cols:
            sheet.write(player_counter, col_count, player['firstName'])
            col_count += 1
        if "LastName" in cols:
            sheet.write(player_counter, col_count, player['lastName'])
            col_count += 1
        if "BirthDate" in cols:
            sheet.write(player_counter, col_count, player['birthDate'])
            col_count += 1
        if "Age" in cols:
            sheet.write(player_counter, col_count, player['currentAge'])
            col_count += 1
        if "Height" in cols:
            sheet.write(player_counter, col_count, player['height'])
            col_count += 1
        if "Weight" in cols:
            sheet.write(player_counter, col_count, player['weight'])
            col_count += 1
        if "TeamID" in cols:
            if ('id' in player['currentTeam']):
                sheet.write(player_counter, col_count, player['currentTeam']['id'])
            else:
                sheet.write(player_counter, col_count, "")
            col_count += 1
        if "Position" in cols:
            sheet.write(player_counter, col_count, player['primaryPosition']['abbreviation'])
            col_count += 1
        if "DebutDate" in cols:
            sheet.write(player_counter, col_count, player['mlbDebutDate'])
            col_count += 1
        if "BatSide" in cols:
            sheet.write(player_counter, col_count, player['batSide']['code'])
            col_count += 1
        if "PitchHand" in cols:
            sheet.write(player_counter, col_count, player['pitchHand']['code'])
            col_count += 1
        player_counter += 1
    book.save(path + "/Player" + str(season) + ".xls")


# Schedule
def export_schedule_data(season, cols, path):
    book = xlwt.Workbook(encoding="utf-8")
    sheet = book.add_sheet("Schedule")
    for i in range(len(cols)):
        sheet.write(0, i, cols[i])

    date_format = xlwt.XFStyle()
    date_format.num_format_str = 'yyyy/mm/dd h:mm'    
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('America/Los_Angeles')

    for date_range in date_ranges:
        if date_range['season'] == season:
            start_date = date_range['start_date']
            end_date = date_range['end_date']

    url = "https://statsapi.mlb.com/api/v1/schedule?startDate=" + start_date + "&endDate=" + end_date + "&sportId=1"
    print("Getting schedule data from " + url)
    schedule = requests.get(url).json()

    game_counter = 1
    for date in schedule['dates']:
        for game in date['games']:
            col_count = 0
            if "GameID" in cols:
                sheet.write(game_counter, col_count, game['gamePk'])
                col_count += 1
            if "GameDate" in cols:
                utc = datetime.strptime(game['gameDate'], '%Y-%m-%dT%H:%M:%SZ')
                utc = utc.replace(tzinfo=from_zone)
                pst = utc.astimezone(to_zone)
                pst = pst.replace(tzinfo=None)
                sheet.write(game_counter, col_count, pst, date_format)
                col_count += 1
            if "AwayTeamID" in cols:
                sheet.write(game_counter, col_count, game['teams']['away']['team']['id'])
                col_count += 1
            if "HomeTeamID" in cols:
                sheet.write(game_counter, col_count, game['teams']['home']['team']['id'])
                col_count += 1
            if "VenueID" in cols:
                sheet.write(game_counter, col_count, game['venue']['id'])
                col_count += 1
            game_counter += 1
    book.save(path + "/Schedule" + str(season) + ".xls")


# Games
def export_game_data(season, cols, path):
    book = xlwt.Workbook(encoding="utf-8")
    sheet = book.add_sheet("Game")
    for i in range(len(cols)):
        sheet.write(0, i, cols[i])

    date_format = xlwt.XFStyle()
    date_format.num_format_str = 'yyyy/mm/dd h:mm'    
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
            col_count = 0
            if game['status']['codedGameState'] == 'F' and game['gamePk'] not in game_ids:

                # if game['status']['detailedState'] == 'Completed Early':
                #     finished_early_ids.append(game['gamePk'])

                if "GameID" in cols:
                    sheet.write(game_counter, col_count, game['gamePk'])
                    col_count += 1
                if "Season" in cols:
                    sheet.write(game_counter, col_count, game['seasonDisplay'])
                    col_count += 1
                if "GameDate" in cols:
                    utc = datetime.strptime(game['gameDate'], '%Y-%m-%dT%H:%M:%SZ')
                    utc = utc.replace(tzinfo=from_zone)
                    pst = utc.astimezone(to_zone)
                    pst = pst.replace(tzinfo=None)
                    sheet.write(game_counter, col_count, pst, date_format)
                    col_count += 1
                if "Status" in cols:
                    sheet.write(game_counter, col_count, game['status']['detailedState'])
                    col_count += 1
                if "AwayTeamID" in cols:
                    sheet.write(game_counter, col_count, game['teams']['away']['team']['id'])
                    col_count += 1
                if "AwayTeamScore" in cols:
                    sheet.write(game_counter, col_count, game['teams']['away']['score'])
                    col_count += 1
                if "AwayTeamRecordWins" in cols:
                    sheet.write(game_counter, col_count, game['teams']['away']['leagueRecord']['wins'])
                    col_count += 1
                if "AwayTeamRecordLosses" in cols:
                    sheet.write(game_counter, col_count, game['teams']['away']['leagueRecord']['losses'])
                    col_count += 1
                if "AwayTeamRecordPct" in cols:
                    sheet.write(game_counter, col_count, game['teams']['away']['leagueRecord']['pct'])
                    col_count += 1
                if "HomeTeamID" in cols:
                    sheet.write(game_counter, col_count, game['teams']['home']['team']['id'])
                    col_count += 1
                if "HomeTeamScore" in cols:
                    sheet.write(game_counter, col_count, game['teams']['home']['score'])
                    col_count += 1
                if "HomeTeamRecordWins" in cols:
                    sheet.write(game_counter, col_count, game['teams']['home']['leagueRecord']['wins'])
                    col_count += 1
                if "HomeTeamRecordLosses" in cols:
                    sheet.write(game_counter, col_count, game['teams']['home']['leagueRecord']['losses'])
                    col_count += 1
                if "HomeTeamRecordPct" in cols:
                    sheet.write(game_counter, col_count, game['teams']['away']['leagueRecord']['pct'])
                    col_count +=1
                if "VenueID" in cols:
                    sheet.write(game_counter, col_count, game['venue']['id'])
                    col_count += 1
                if "DayNight" in cols:
                    sheet.write(game_counter, col_count, game['dayNight'])
                    col_count += 1
                if "GamesInSeries" in cols:
                    sheet.write(game_counter, col_count, game['gamesInSeries'])
                    col_count += 1
                if "SeriesGameNumber" in cols:
                    sheet.write(game_counter, col_count, game['seriesGameNumber'])
                    col_count += 1
                if "SeriesDescription" in cols:
                    sheet.write(game_counter, col_count, game['seriesDescription'])
                    col_count += 1

                game_ids.append(game['gamePk'])
                game_counter += 1
    book.save(path + "/Game" + str(season) + ".xls")


# Play By Play
def export_pbp_data(season, cols, min_sec, max_sec, path):

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
            game_ids.append(game['gamePk'])

    book_count = 0
    books_needed = math.ceil(len(game_ids)/800)

    while book_count < books_needed:
        book = xlwt.Workbook(encoding="utf-8")
        sheet = book.add_sheet("PlayByPlay")
        for i in range(len(cols)):
            sheet.write(0, i, cols[i])
        book_count += 1
        pbp_counter = 1
        game_counter = 1
        book_game_ids = game_ids[800*(book_count-1):800*book_count] # One sheet cannot handle much more than 800 games of play-by-play data

        print("Getting play-by-play data for " + str(len(book_game_ids)) + " games...")
        for game_id in book_game_ids:
            pbp = requests.get("https://statsapi.mlb.com/api/v1/game/" + str(game_id) + "/playByPlay").json()
            for play in pbp['allPlays']:
                col_count = 0
                if 'event' in play['result'] and 'eventType' in play['result']:
                    if "PlayByPlayID" in cols:
                        sheet.write(pbp_counter, col_count, pbp_counter)
                        col_count += 1
                    if "GameID" in cols:
                        sheet.write(pbp_counter, col_count, game_id)
                        col_count += 1
                    if "BatterID" in cols:
                        sheet.write(pbp_counter, col_count, play['matchup']['batter']['id'])
                        col_count += 1
                    if "BatSide" in cols:
                        sheet.write(pbp_counter, col_count, play['matchup']['batSide']['code'])
                        col_count += 1
                    if "PitcherID" in cols:
                        sheet.write(pbp_counter, col_count, play['matchup']['pitcher']['id'])
                        col_count += 1
                    if "PitchHand" in cols:
                        sheet.write(pbp_counter, col_count, play['matchup']['pitchHand']['code'])
                        col_count += 1
                    if "MenOnBase" in cols:
                        sheet.write(pbp_counter, col_count, play['matchup']['splits']['menOnBase'])
                        col_count += 1
                    if "Event" in cols:
                        sheet.write(pbp_counter, col_count, play['result']['event'])
                        col_count += 1
                    if "EventType" in cols:
                        sheet.write(pbp_counter, col_count, play['result']['eventType'])
                        col_count += 1
                    if "IsScoringPlay" in cols:
                        sheet.write(pbp_counter, col_count, play['about']['isScoringPlay'])
                        col_count += 1
                    if "AwayTeamScore" in cols:
                        sheet.write(pbp_counter, col_count, play['result']['awayScore'])
                        col_count += 1
                    if "HomeTeamScore" in cols:
                        sheet.write(pbp_counter, col_count, play['result']['homeScore'])
                        col_count += 1
                    if "AtBatIndex" in cols:
                        sheet.write(pbp_counter, col_count, play['about']['atBatIndex'])
                        col_count += 1
                    if "HalfInning" in cols:
                        sheet.write(pbp_counter, col_count, play['about']['halfInning'])
                        col_count += 1
                    if "Inning" in cols:
                        sheet.write(pbp_counter, col_count, play['about']['inning'])
                        col_count += 1
                    if "Outs" in cols:
                        sheet.write(pbp_counter, col_count, play['count']['outs'])
                        col_count += 1
                    pbp_counter += 1
            print(str("Finished writing game " + str(game_id) + ". " + str(game_counter) + " out of " + str(len(book_game_ids)) + " games finished."))
            game_counter += 1
            sleep(randint(min_sec,max_sec))
        book.save(path + "/PlayByPlay" + str(season) + "_" + str(book_count) + ".xls")