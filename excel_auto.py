import requests
import json
import math
import os
import openpyxl
import subprocess
import xlsxwriter

URL = 'api website'
API_PLAYERS = '/api/v1/players/?search='
API_AVERAGES = '/api/v1/season_averages/?season='
stat_end = '&player_ids[]='

print("Important:\nFor stat lookups, you will need the player "
      "ID for your query.\n\n"
      "The player ID can be retrieved via the "
      "player look up option (1), unless\n"
      "you already know the player ID of the specified player.\n\n")


def fetch_players(query):
    return requests.get(URL + API_PLAYERS + query).json()
    

def fetch_stats(query):
    return requests.get(URL + API_STATS + query).json()


def fetch_AVERAGES(query):
    year = input("what year would you like to look up:\t")
    return requests.get(URL + API_AVERAGES + year + stat_end + query).json()


def display_players(player):
    spreadsheet = input("Would you like to print to excel? \n"
                   "Press 1: Yes\n"
                   "Press Any button: No\n")
    print(f"Information for query below:\n")
    if spreadsheet == "1":
        row = 0
        col = 0
        nbawb = xlsxwriter.Workbook('nbapy2.xlsx')
        worksheet = nbawb.add_worksheet("Player Info")
        cell_format = nbawb.add_format()
        cell_format.set_bg_color('red')
        cell_format.set_align('center')
        cell_format.set_align('vcenter')
        worksheet.write('A1', 'Player ID', cell_format)
        worksheet.write('B1', 'First Name', cell_format)
        worksheet.write('C1', 'Last Name', cell_format)
        worksheet.write('D1', 'Position', cell_format)
        worksheet.write('E1', 'Team', cell_format)
        for entry in player['data']:
            ID = entry['id']
            f_name = entry["first_name"]
            l_name = entry["last_name"]
            p_position = entry["position"]
            f_height = entry["height_feet"]
            f_inches = entry["height_inches"]
            weight = entry["weight_pounds"]
            team = entry["team"]['full_name']
            print(f"ID: {ID}\nName: {f_name} {l_name} \nPosition: {p_position} \n"
                  f"Feet: {f_height}\nInches: {f_inches}\n"
                  f"Weight: {weight}\nTeam: {team}\n")
            row += 1
            worksheet.write(row + 1, col, ID)
            worksheet.write(row + 1, col + 1, f_name)
            worksheet.write(row + 1, col + 2, l_name)
            worksheet.write(row + 1, col + 3, p_position)
            worksheet.write(row + 1, col + 4, team)
            worksheet.set_column('A:E', 20)
        nbawb.close()
    else:
        for entry in player['data']:
            ID = entry['id']
            f_name = entry["first_name"]
            l_name = entry["last_name"]
            p_position = entry["position"]
            f_height = entry["height_feet"]
            f_inches = entry["height_inches"]
            weight = entry["weight_pounds"]
            team = entry["team"]['full_name']
            print(f"ID: {ID}\nName: {f_name} {l_name} \nPosition: {p_position} \n"
                  f"Feet: {f_height}\nInches: {f_inches}\n"
                  f"Weight: {weight}\nTeam: {team}\n")


def display_stats(ID):
    print(f"stats for query: \n")
    for entry in ID['data']:
        games = entry['games_played']
        year = entry['season']
        minutes = entry['min']
        fg_percent = entry['fg_pct']
        threept_percent = entry['fg3_pct']
        ft_percent = entry['ft_pct']
        ppg = entry['pts']
        rebounds = entry['reb']
        assists = entry['ast']
        turnovers = entry['turnover']
        print(f"Games Played: {games}\nSeason: {year}\nMPG: {minutes} \n"
              f"FG %: {fg_percent}\n3PT %: {threept_percent}\n"
              f"FT %: {ft_percent}\n"
              f"Points Per Game: {ppg}\nRebounds: {rebounds}\n"
              f"Assists {assists}\nTurnovers: {turnovers}\n")


def player_info():
    try:
        player_lookup = ''
        while not player_lookup:
            player_lookup = input("What player do you want to lookup? ")
        nba_player = fetch_players(player_lookup)
        if len(player_lookup) == 0:
            print("Not coming up with anything, check the spelling")
        else:
            ID = nba_player
            display_players(ID)
    except requests.exceptions.ConnectionError:
        print("Couldn't connect to server!")


def player_stats():
    stat_lookup = input("What is the player ID: \t")
    nba_stat = fetch_AVERAGES(stat_lookup)
    while stat_lookup >= "1":
        print(f"Stats for ID {stat_lookup} are below: \n")
        return display_stats(nba_stat)
        break


def type_lookup():
    NBA = input("Do you want to look up player info or player stats?\n"
                "Press 1: Player look up\n"
                "Press 2: Regular Season Stat Lookup\n"
                "Press 3: Quit\n")
    if NBA == "1":
        player_info()
    elif NBA == "2":
        player_stats()
    elif NBA == "3":
        print("\nCome back again for the latest stats & info")
        quit()
    else:
        print("Please choose option 1 or 2")
        type_lookup()


if __name__ == '__main__':
    while True:
        type_lookup()

