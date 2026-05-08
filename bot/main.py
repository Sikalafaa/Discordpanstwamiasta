import os
import sys
import logging
from datetime import datetime

# Allow running directly (python bot/main.py) as well as as a module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

import bot.game_session as gs
from bot.database import DatabaseHandler
from bot.game_session import GameSession
from bot.stats_manager import StatsManager

load_dotenv()

# ── Logowanie do pliku i konsoli ───────────────────────────────────────────
_log_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "bot.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(_log_path, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("panstwa_bot")
# Wycisz zbędne logi z bibliotek
logging.getLogger("discord").setLevel(logging.WARNING)
logging.getLogger("aiohttp").setLevel(logging.WARNING)

# ── Bot setup ──────────────────────────────────────────────────────────────

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot   = commands.Bot(command_prefix="/", intents=intents)
db    = DatabaseHandler()
stats = StatsManager(db)

sessions: dict[int, GameSession] = {}

# ── Events ─────────────────────────────────────────────────────────────────

@bot.event
async def on_ready():
    logger.info(f"Bot online: {bot.user} | Serwery: {len(bot.guilds)}")
    await _check_and_reset()
    if not season_reset_check.is_running():
        season_reset_check.start()


# ── 10-day auto-reset task ─────────────────────────────────────────────────

async def _check_and_reset():
    if db.needs_reset():
        db.reset_season()
        logger.info("Sezon zresetowany automatycznie.")
        for guild in bot.guilds:
            await stats.clear_roles(guild)


@tasks.loop(hours=24)
async def season_reset_check():
    await _check_and_reset()


@season_reset_check.before_loop
async def before_reset_check():
    await bot.wait_until_ready()


# ── Game commands ──────────────────────────────────────────────────────────

@bot.command(name="start")
@commands.guild_only()
async def start_game(ctx: commands.Context):
    if ctx.guild is None:
        return
    guild_id = ctx.guild.id
    session  = sessions.get(guild_id)
    if session and session.state in ("waiting", "active"):
        await ctx.send(
            "❌ Gra już trwa lub czeka na graczy!\n"
            "Wpisz `/dołącz` żeby dołączyć, lub `/stop` żeby przerwać."
        )
        return
    session = GameSession(ctx, db, stats)
    sessions[guild_id] = session
    await session.start()
    if guild_id in sessions and sessions[guild_id].state == "finished":
        del sessions[guild_id]


@bot.command(name="dołącz", aliases=["dolacz", "join"])
@commands.guild_only()
async def join_game(ctx: commands.Context):
    if ctx.guild is None:
        return
    guild_id = ctx.guild.id
    session  = sessions.get(guild_id)
    if session is None or not session.is_waiting:
        await ctx.send(
            "❌ Nie ma otwartej gry do dołączenia.\n"
            "Użyj `/start` żeby rozpocząć nową."
        )
        return
    discord_id = str(ctx.author.id)
    if discord_id in session.registered:
        await ctx.send(f"ℹ️ {ctx.author.mention} — już jesteś zapisany!")
        return
    session.add_player(discord_id, ctx.author.display_name)
    count = len(session.registered)
    await ctx.send(
        f"✅ {ctx.author.mention} dołączył do gry! "
        f"Zapisanych graczy: **{count}**"
    )


@bot.command(name="stop")
@commands.guild_only()
async def stop_game(ctx: commands.Context):
    if ctx.guild is None:
        return
    guild_id = ctx.guild.id
    session  = sessions.get(guild_id)
    if session is None or session.state == "finished":
        await ctx.send("❌ Żadna gra nie jest aktualnie uruchomiona.")
        return
    await session.force_stop()
    del sessions[guild_id]


# ── Stats & ranking ────────────────────────────────────────────────────────

@bot.command(name="statystyki", aliases=["stats", "stat"])
async def show_stats(ctx: commands.Context, member: discord.Member | None = None):
    target = member or ctx.author
    row    = db.get_player_stats(str(target.id))
    if not row:
        await ctx.send(f"❌ **{target.display_name}** nie ma jeszcze żadnych statystyk.")
        return
    played   = int(row.games_played or 0)
    won      = int(row.games_won or 0)
    points   = int(row.total_points or 0)
    win_rate = (won / played * 100) if played > 0 else 0
    await ctx.send(
        f"📊 **Statystyki — {target.display_name}**\n"
        f"Rozegrane gry: **{played}**\n"
        f"Wygrane:       **{won}** ({win_rate:.0f}%)\n"
        f"Łączne punkty: **{points}**"
    )


@bot.command(name="ranking", aliases=["top"])
@commands.guild_only()
async def show_ranking(ctx: commands.Context):
    if ctx.guild is None:
        return
    top = db.get_leaderboard(str(ctx.guild.id))
    if not top:
        await ctx.send("❌ Brak danych do rankingu.")
        return
    medals = ["🥇", "🥈", "🥉"]
    lines  = ["🏆 **Ranking tego sezonu:**"]
    for i, p in enumerate(top):
        lines.append(f"{medals[i]} {p.username} — **{int(p.total_points or 0)}** pkt")
    await ctx.send("\n".join(lines))


@bot.command(name="sezon", aliases=["season"])
async def show_season(ctx: commands.Context):
    days_left = db.days_until_next_reset()
    last      = db.get_last_reset()
    last_str  = last.strftime("%d.%m.%Y %H:%M") if last else "Nigdy"
    await ctx.send(
        "📅 **Informacje o sezonie**\n"
        f"Ostatni reset: **{last_str}**\n"
        f"Następny reset za: **{days_left} dni**\n"
        f"Interwał resetu: co **10 dni**"
    )


# ── Admin commands ─────────────────────────────────────────────────────────

@bot.command(name="reset")
@commands.guild_only()
@commands.has_permissions(administrator=True)
async def manual_reset(ctx: commands.Context):
    if ctx.guild is None:
        return
    db.reset_season()
    await stats.clear_roles(ctx.guild)
    await ctx.send(
        "✅ **Sezon zresetowany!**\n"
        "Wszystkie statystyki wyczyszczone, role odebrane."
    )


@bot.command(name="ustawienia", aliases=["settings"])
@commands.has_permissions(administrator=True)
async def settings_cmd(
    ctx: commands.Context,
    *args: str,
):
    """
    Użycie:
      /ustawienia                          — pokaż aktualne ustawienia
      /ustawienia rundy 5 czas 60 lobby 30 — zmień kilka naraz
    """
    # Brak argumentów — pokaż aktualne ustawienia
    if not args:
        embed = discord.Embed(title="⚙️ Ustawienia gry", color=discord.Color.blurple())
        embed.add_field(name="Liczba rund", value=f"`{gs.MAX_ROUNDS}`", inline=True)
        embed.add_field(name="Czas rundy",  value=f"`{gs.ROUND_TIME}s`", inline=True)
        embed.add_field(name="Czas lobby",  value=f"`{gs.LOBBY_TIME}s`", inline=True)
        embed.set_footer(text="Przykład zmiany: /ustawienia rundy 5 czas 60 lobby 30")
        await ctx.send(embed=embed)
        return

    # Parsuj pary klucz wartość: rundy 5 czas 60 lobby 30
    if len(args) % 2 != 0:
        await ctx.send("❌ Podaj pary: `/ustawienia rundy 5 czas 60 lobby 30`")
        return

    zmiany = {}
    for i in range(0, len(args), 2):
        klucz = args[i].lower()
        try:
            wartosc = int(args[i + 1])
        except ValueError:
            await ctx.send(f"❌ `{args[i + 1]}` nie jest liczbą.")
            return
        if wartosc < 1:
            await ctx.send(f"❌ Wartość musi być większa od 0.")
            return
        if klucz not in ("rundy", "czas", "lobby"):
            await ctx.send(f"❌ Nieznana opcja `{klucz}`. Dostępne: `rundy`, `czas`, `lobby`")
            return
        zmiany[klucz] = wartosc

    # Zastosuj zmiany
    if "rundy" in zmiany:
        gs.MAX_ROUNDS = zmiany["rundy"]
    if "czas" in zmiany:
        gs.ROUND_TIME = zmiany["czas"]
    if "lobby" in zmiany:
        gs.LOBBY_TIME = zmiany["lobby"]

    embed = discord.Embed(title="✅ Zaktualizowano ustawienia", color=discord.Color.green())
    embed.add_field(name="Liczba rund", value=f"`{gs.MAX_ROUNDS}`", inline=True)
    embed.add_field(name="Czas rundy",  value=f"`{gs.ROUND_TIME}s`", inline=True)
    embed.add_field(name="Czas lobby",  value=f"`{gs.LOBBY_TIME}s`", inline=True)
    await ctx.send(embed=embed)


# ── Help ───────────────────────────────────────────────────────────────────

@bot.command(name="pomoc", aliases=["h"])
async def help_cmd(ctx: commands.Context):
    await ctx.send(
        "📖 **Dostępne komendy:**\n"
        "`/start`               — Rozpocznij nową grę (30s lobby)\n"
        "`/dołącz`              — Dołącz do trwającego lobby\n"
        "`/stop`                — Przerwij grę\n"
        "`/statystyki [@gracz]` — Pokaż statystyki\n"
        "`/ranking`             — Top 3 tego sezonu\n"
        "`/sezon`               — Info o sezonie i dacie resetu\n"
        "\n"
        "**Admin:**\n"
        "`/reset`               — Ręczny reset sezonu\n"
        "`/ustawienia`          — Zmień parametry gry\n"
    )


# ── Error handler ──────────────────────────────────────────────────────────

@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Nieznana komenda. Wpisz `/pomoc` żeby zobaczyć dostępne komendy.")
    elif isinstance(error, commands.NoPrivateMessage):
        await ctx.send("❌ Ta komenda działa tylko na serwerze!")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Nie masz uprawnień do tej komendy!")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Brakujący argument: `{error.param.name}`")
    else:
        logger.error(f"Nieobsłużony błąd komendy '{ctx.command}': {error}", exc_info=error)


# ── Entry point ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("Brak BOT_TOKEN w pliku .env!")
    bot.run(token)
