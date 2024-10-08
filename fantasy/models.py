import uuid
from typing import NewType, Optional
from pydantic import BaseModel, Field
from termcolor import colored


# class FantasyTeam(BaseModel):
#     id: str = Field(default_factory=uuid.uuid4, alias="_id")
#     team_id: int = Field(...)
#     name: str = Field(...)

#      class Config:
#         allow_population_by_field_name = True
#         schema_extra = {
#             "example": {
#                 "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
#                 "team_id": "1",
#                 "name": "Jimmy Mama"
#             }
#         }

# class Matchup(BaseModel)
#      id: str = Field(default_factory=uuid.uuid4, alias="_id")
#      team1: self.FantasyTeam = Field(...)

#     class FantasyTeam(BaseModel):
#         id: str = Field(default_factory=uuid.uuid4, alias="_id")
#         team_id: int = Field(...)
#         name: str = Field(...)

#         class Config:
#             allow_population_by_field_name = True
#             schema_extra = {
#                 "example": {
#                 "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
#                 "team_id": "1",
#                 "name": "Jimmy Mama"
#                 }
#             }

#     class Config:
#         allow_population_by_field_name = True
#             schema_extra = {
#             "example": {
#                 "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
#                 "team_id": "1",
#                 "name": "Jimmy Mama"
#             }
#         }


# class Book(BaseModel):
#     id: str = Field(default_factory=uuid.uuid4, alias="_id")
#     title: str = Field(...)
#     author: str = Field(...)
#     synopsis: str = Field(...)

#     class Config:
#         allow_population_by_field_name = True
#         schema_extra = {
#             "example": {
#                 "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
#                 "title": "Don Quixote",
#                 "author": "Miguel de Cervantes",
#                 "synopsis": "..."
#             }
#         }


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class Player:
    name = ""
    points = 0
    opponent = ""
    position_and_team = ""
    stats = ""
    game_status = ""
    onBench = False

    def print_info(self):
        print(self.name)
        print(self.points)
        print(self.opponent)
        print(self.game_status)
        print(self.position_and_team)
        print(self.stats)
        print(self.onBench)

    def get_position(self):
        if "QB" in self.position_and_team[0:2]:
            return "QB"
        if "RB" in self.position_and_team[0:2]:
            return "RB"
        if "WR" in self.position_and_team[0:2]:
            return "WR"
        if "TE" in self.position_and_team[0:2]:
            return "TE"
        if "K" in self.position_and_team[0]:
            return "K "
        if "DEF" in self.position_and_team[0:3]:
            return "DEF"
        return self.position_and_team

    def print_name_and_points(self, color=None):
        if color is None:
            print(self.get_position() + " | " + self.name + ": " + self.points)
        else:
            print(
                colored(
                    self.get_position() + " | " + self.name + ": " + self.points, color
                )
            )

    def __init__(
        self, name, points, opponent, game_status, position_and_team, stats, onBench
    ):
        self.name = name
        self.points = points
        self.opponent = opponent
        self.position_and_team = position_and_team
        self.stats = stats
        self.game_status = game_status
        self.onBench = onBench
