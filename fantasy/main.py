from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
from models import Player
from termcolor import colored


config = dotenv_values(".env")
app = FastAPI()


kTeams = {
    1: "Jimmy Mama",
    2: "glock purdy",
    3: "Now watch this draft",
    4: "2028 Olympic Roster",
    5: "Little Man Yoda",
    6: "Unga Bungas",
    7: "Kobmeister",
    8: "Maybe Nix Year",
    9: "National Footpog League",
    10: "The Third Stringers",
}

kPositionClasses = [
    "player-QB-0 odd first",
    "player-RB-0 even",
    "player-RB-1 odd",
    "player-WR-0 even",
    "player-WR-1 odd",
    "player-TE-0 even",
    "player-R/W/T-0 odd",
    "player-K-0 even",
    "player-DEF-0 odd last",
    "player-BN-1 odd first",
    "player-BN-2 even",
    "player-BN-3 odd",
    "player-BN-4 even",
    "player-BN-5 odd",
    "player-BN-6 even",
]


@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["ATLAS_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    print("Connected to the MongoDB database!")


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()


def fetchData(team_id):
    URL = "https://fantasy.nfl.com/league/10810155/team/%s/gamecenter" % team_id
    URL2 = (
        "https://fantasy.nfl.com/league/10810155/team/%s/gamecenter?gameCenterTab=track&trackType=sbs&week=5#teamMatchupFull=teamMatchupTabs-1%%2C%%2Fleague%%2F10810155%%2Fteam%%2F1%%2Fgamecenter%%253FgameCenterTab%%253Dtrack%%2526trackType%%253Dair%%2526week%%253D5%%2Creplace"
        % team_id
    )
    return requests.get(URL2)


def createPlayer(html, onBench):
    name = html.find("a", class_="playerNameFirstInitialLastName").text
    if "." not in name:
        name += " DEF"
    position_and_team = html.find("em").text
    if (position_and_team) == "R/W/T":
        position_and_team = html.find_all("em")[1].text
    opponent = html.find("td", class_="playerOpponent").text
    game_status = html.find("td", class_="playerGameStatus").text
    if game_status != None:
        game_status = game_status.removesuffix("Get Tickets")
    points = html.find("td", class_="statTotal").text
    stats = html.find("td", class_="playerStats").text

    player = Player(
        name, points, opponent, game_status, position_and_team, stats, onBench
    )
    return player


def getRosters(html, team_id):
    soup = BeautifulSoup(html.content, "html.parser")
    home_roster = []
    away_roster = []
    for position in kPositionClasses:
        positions = soup.find_all("tr", class_=position)
        try:
            home_roster.append(createPlayer(positions[0], "BN" in position))
        except:
            print("failed to create player {0} on team {1}".format(position, team_id))
        # try:
        #     away_roster.append(createPlayer(positions[1], "BN" in position))
        # except:
        #     print(
        #         "failed to create player {0} on team {1}".format(position, team_ids[1])
        #     )
    return [home_roster, away_roster]


def getBestPlayer(players, number):
    players.sort(key=lambda x: float(x.points), reverse=True)
    return players[:number]


def getOptimalLineup(roster):
    optimalLineup = []
    qbs = []
    rbs = []
    wrs = []
    tes = []
    ks = []
    defs = []
    flex = []
    for player in roster:
        if player.get_position() == "QB":
            qbs.append(player)
        if player.get_position() == "RB":
            rbs.append(player)
        if player.get_position() == "WR":
            wrs.append(player)
        if player.get_position() == "TE":
            tes.append(player)
        if player.get_position() == "K ":
            ks.append(player)
        if player.get_position() == "DEF":
            defs.append(player)

    optimalLineup.extend(getBestPlayer(qbs, 1))
    optimalLineup.extend(getBestPlayer(rbs, 2))
    optimalLineup.extend(getBestPlayer(wrs, 2))
    optimalLineup.extend(getBestPlayer(tes, 1))

    flex.extend(wrs)
    flex.extend(tes)
    flex.extend(rbs)

    flex = [player for player in flex if player not in optimalLineup]

    optimalLineup.extend(getBestPlayer(flex, 1))
    optimalLineup.extend(getBestPlayer(ks, 1))
    optimalLineup.extend(getBestPlayer(defs, 1))
    return optimalLineup


def getRosterTotal(roster):
    score = 0
    for player in roster[0:9]:
        score += float(player.points)
    return str(round(score, 3))


def printOptomizedRoster(roster):
    for player in roster:
        if player.onBench:
            player.print_name_and_points("red")
        if not player.onBench:
            player.print_name_and_points("green")


def parseHtml(html, team_id):
    print("starting lineup")
    rosters = getRosters(html, team_id)
    for player in rosters[0]:
        player.print_name_and_points()
    print("Score: " + getRosterTotal(rosters[0]))
    print("")
    print("Optimal Lineup")
    opti = getOptimalLineup(rosters[0])
    printOptomizedRoster(opti)
    print("Score: " + getRosterTotal(opti))
    print(
        "Δ: ",
        str(round(float(getRosterTotal(opti)) - float(getRosterTotal(rosters[0])), 2)),
    )

    # print("away team")
    # for player in rosters[1]:
    #     player.print_name_and_points()


# team_id = 2
# html = fetchData(team_id)
# parseHtml(html, team_id)

for i in range(1, 5):
    print(kTeams.get(i))
    parseHtml(fetchData(i), i)
    print("")
