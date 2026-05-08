import os
from datetime import datetime
from sqlalchemy import create_engine, String, Integer, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

RESET_INTERVAL_DAYS = 10


def _default_db_path() -> str:
    bot_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(bot_root, "bot.db")


# SQLAlchemy 2.0 declarative base — Mapped[] annotations give Pylance
# proper types (int, str, datetime) instead of Column[int].
class Base(DeclarativeBase):
    pass


class PlayerModel(Base):
    __tablename__ = "players"
    discord_id   : Mapped[str]      = mapped_column(String,  primary_key=True)
    guild_id     : Mapped[str]      = mapped_column(String,  primary_key=True)
    username     : Mapped[str]      = mapped_column(String,  default="")
    total_points : Mapped[int]      = mapped_column(Integer, default=0)
    games_played : Mapped[int]      = mapped_column(Integer, default=0)
    games_won    : Mapped[int]      = mapped_column(Integer, default=0)


class GameModel(Base):
    __tablename__ = "games"
    id        : Mapped[int]           = mapped_column(Integer,  primary_key=True, autoincrement=True)
    guild_id  : Mapped[str]           = mapped_column(String)
    played_at : Mapped[datetime]      = mapped_column(DateTime, default=datetime.now)
    winner_id : Mapped[str | None]    = mapped_column(String,   nullable=True)
    rounds    : Mapped[int]           = mapped_column(Integer,  default=0)


class ResetLog(Base):
    __tablename__ = "reset_log"
    id       : Mapped[int]      = mapped_column(Integer,  primary_key=True, autoincrement=True)
    reset_at : Mapped[datetime] = mapped_column(DateTime, default=datetime.now)


class DatabaseHandler:
    def __init__(self, db_url: str | None = None):
        if db_url is None:
            db_url = f"sqlite:///{_default_db_path()}"
        engine = create_engine(db_url, connect_args={"check_same_thread": False})
        Base.metadata.create_all(engine)
        self.Session = sessionmaker(bind=engine)

    # ── Player stats ───────────────────────────────────────────────────────

    def save_player_stats(self, guild_id: str, player, won: bool) -> None:
        with self.Session() as session:
            p = session.get(PlayerModel, (player.discord_id, guild_id))
            if not p:
                p = PlayerModel(
                    discord_id=player.discord_id,
                    guild_id=guild_id,
                    username=player.username,
                    total_points=0,
                    games_played=0,
                    games_won=0,
                )
                session.add(p)
            p.username      = player.username
            p.total_points += player.total_points
            p.games_played += 1
            if won:
                p.games_won += 1
            session.commit()

    def get_player_stats(self, discord_id: str) -> PlayerModel | None:
        with self.Session() as session:
            return (
                session.query(PlayerModel)
                .filter_by(discord_id=discord_id)
                .first()
            )

    def get_leaderboard(self, guild_id: str, limit: int = 3) -> list[PlayerModel]:
        with self.Session() as session:
            return (
                session.query(PlayerModel)
                .filter_by(guild_id=guild_id)
                .order_by(PlayerModel.total_points.desc())
                .limit(limit)
                .all()
            )

    # ── Game log ───────────────────────────────────────────────────────────

    def save_game(self, guild_id: str, rounds: list, sorted_players: list) -> None:
        with self.Session() as session:
            game = GameModel(
                guild_id=guild_id,
                winner_id=sorted_players[0].discord_id if sorted_players else None,
                rounds=len(rounds),
            )
            session.add(game)
            session.commit()

    # ── Season / reset ─────────────────────────────────────────────────────

    def get_last_reset(self) -> datetime | None:
        with self.Session() as session:
            log = (
                session.query(ResetLog)
                .order_by(ResetLog.reset_at.desc())
                .first()
            )
            return log.reset_at if log else None

    def reset_season(self) -> None:
        with self.Session() as session:
            session.query(PlayerModel).update(
                {"total_points": 0, "games_played": 0, "games_won": 0}
            )
            session.add(ResetLog(reset_at=datetime.now()))
            session.commit()

    def days_until_next_reset(self) -> int:
        last = self.get_last_reset()
        if last is None:
            return RESET_INTERVAL_DAYS
        elapsed = (datetime.now() - last).days
        return max(0, RESET_INTERVAL_DAYS - elapsed)

    def needs_reset(self) -> bool:
        last = self.get_last_reset()
        if last is None:
            return True
        return (datetime.now() - last).days >= RESET_INTERVAL_DAYS
