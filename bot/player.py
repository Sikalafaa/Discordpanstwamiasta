class Player:
    def __init__(self, discord_id: str, username: str):
        self.discord_id = discord_id
        self.username = username
        self.total_points = 0
        self.games_played = 0
        self.games_won = 0

    def add_points(self, points: int):
        self.total_points += points

    def get_stats(self) -> dict:
        return {
            "discord_id": self.discord_id,
            "username": self.username,
            "total_points": self.total_points,
            "games_played": self.games_played,
            "games_won": self.games_won,
        }
