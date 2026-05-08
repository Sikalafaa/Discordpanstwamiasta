import discord
import asyncio
import random
import logging

from bot.round import Round, CATEGORIES
from bot.player import Player
from bot.voice_manager import VoiceManager
from bot.validator import validate_all_answers, clear_cache

logger = logging.getLogger("panstwa_bot.game")

LETTERS    = list("ABCDEFGHIJKLMNOPRSTUWZ")
MAX_ROUNDS = 5
ROUND_TIME = 60
LOBBY_TIME = 30

COLOR_BLUE   = discord.Color.from_rgb(88, 101, 242)
COLOR_GOLD   = discord.Color.gold()
COLOR_RED    = discord.Color.red()
COLOR_GREEN  = discord.Color.green()
COLOR_YELLOW = discord.Color.yellow()


# ── Discord UI Views ───────────────────────────────────────────────────────

class AppealButton(discord.ui.Button):
    """Przycisk zaskarżenia — klikać może tylko właściciel odpowiedzi."""

    def __init__(self, discord_id: str, category: str, answer: str, player_name: str):
        label = f"{player_name}: {answer} ({category})"
        if len(label) > 80:
            label = label[:77] + "..."
        super().__init__(label=label, style=discord.ButtonStyle.secondary)
        self.owner_id = discord_id
        self.category = category
        self.answer   = answer

    async def callback(self, interaction: discord.Interaction) -> None:
        if str(interaction.user.id) != self.owner_id:
            await interaction.response.send_message(
                "Możesz zaskarżyć tylko swoją własną odpowiedź!", ephemeral=True
            )
            return
        if self.disabled:
            await interaction.response.send_message("Już zaskarżyłeś tę odpowiedź!", ephemeral=True)
            return
        self.disabled = True
        self.style = discord.ButtonStyle.primary
        if isinstance(self.view, AppealView):
            self.view.appealed.add((self.owner_id, self.category, self.answer))
        await interaction.response.edit_message(view=self.view)


class AppealView(discord.ui.View):
    """Widok z przyciskami zaskarżenia dla odrzuconych odpowiedzi."""

    def __init__(self, rejected: list[tuple[str, str, str, str]]):
        super().__init__(timeout=60)
        self.appealed: set[tuple[str, str, str]] = set()
        for discord_id, category, answer, player_name in rejected[:20]:  # max 20 przycisków
            self.add_item(AppealButton(discord_id, category, answer, player_name))


class VoteView(discord.ui.View):
    """Widok głosowania nad zaskarżoną odpowiedzią."""

    def __init__(self, voter_ids: list[str]):
        super().__init__(timeout=30)
        self.votes:     dict[str, bool] = {}
        self.voter_ids: set[str]        = set(voter_ids)
        self.all_voted                  = asyncio.Event()

    async def _register_vote(self, interaction: discord.Interaction, choice: bool) -> None:
        uid = str(interaction.user.id)
        if uid not in self.voter_ids:
            await interaction.response.send_message("Nie jesteś uczestnikiem tej gry!", ephemeral=True)
            return
        self.votes[uid] = choice
        label = "✅" if choice else "❌"
        await interaction.response.send_message(f"Zagłosowałeś: {label}", ephemeral=True)
        if self.voter_ids <= set(self.votes):
            self.all_voted.set()
            self.stop()

    @discord.ui.button(label="✅ Akceptuj", style=discord.ButtonStyle.green)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await self._register_vote(interaction, True)

    @discord.ui.button(label="❌ Odrzuć", style=discord.ButtonStyle.red)
    async def reject(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await self._register_vote(interaction, False)

    def accepted(self) -> bool:
        if not self.votes:
            return False
        yes = sum(1 for v in self.votes.values() if v)
        return yes > len(self.voter_ids) / 2


class NextRoundView(discord.ui.View):
    """Przycisk 'Następna runda' — tylko organizator może go kliknąć."""

    def __init__(self, starter_id: str):
        super().__init__(timeout=180)
        self.starter_id = starter_id
        self.ready      = asyncio.Event()

    @discord.ui.button(label="▶ Następna runda", style=discord.ButtonStyle.green)
    async def next_round(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        if str(interaction.user.id) != self.starter_id:
            await interaction.response.send_message(
                "Tylko organizator może rozpocząć następną rundę!", ephemeral=True
            )
            return
        button.disabled = True
        button.label    = "✅ Runda rozpoczęta"
        await interaction.response.edit_message(view=self)
        self.ready.set()
        self.stop()


class GameSession:
    def __init__(self, ctx, db, stats):
        self.ctx      = ctx
        self.db       = db
        self.stats    = stats
        self.guild_id = str(ctx.guild.id)
        self.channel  = ctx.channel
        self.voice    = VoiceManager()

        self.registered: dict[str, str]    = {}   # discord_id → username
        self.players:    dict[str, Player] = {}   # discord_id → Player

        self.rounds: list[Round] = []
        self.current_round = 0
        self.state = "waiting"
        self.used_letters: set[str] = set()

    # ── Public helpers ─────────────────────────────────────────────────────

    @property
    def is_waiting(self) -> bool:
        return self.state == "waiting"

    @property
    def is_active(self) -> bool:
        return self.state == "active"

    def add_player(self, discord_id: str, username: str) -> bool:
        if self.state != "waiting":
            return False
        self.registered[discord_id] = username
        return True

    # ── Game lifecycle ─────────────────────────────────────────────────────

    async def start(self):
        embed = discord.Embed(
            title="🎮 Państwa-Miasta-Imiona!",
            description=(
                f"Wpisz `/dołącz` żeby dołączyć!\n"
                f"Gra startuje za **{LOBBY_TIME} sekund**."
            ),
            color=COLOR_BLUE,
        )
        embed.add_field(
            name="📋 Kategorie",
            value=" | ".join(CATEGORIES),
            inline=False,
        )
        embed.add_field(
            name="⚠️ Jak odpowiadać?",
            value="Odpowiedzi wysyłaj **w prywatnej wiadomości do bota** — inni gracze ich nie zobaczą!",
            inline=False,
        )
        embed.add_field(
            name="🏆 Punktacja",
            value=(
                "🥇 **10 pkt** — unikalna odpowiedź (tylko Ty ją masz)\n"
                "🥈 **5 pkt** — taka sama odpowiedź jak inny gracz\n"
                "❌ **0 pkt** — brak odpowiedzi, błędna lub zła litera"
            ),
            inline=False,
        )
        embed.set_footer(text="Format odpowiedzi: Polska, Poznań, Paweł, Panda, Pinia")
        await self.channel.send(embed=embed)

        clear_cache()   # nowa gra = świeży cache walidacji

        # Dołącz do kanału głosowego od razu i ogłoś odliczanie
        if self.ctx.author.voice:
            await self.voice.join_channel(self.ctx.author.voice.channel)
            await self.voice.announce(f"Gra rozpocznie się za {LOBBY_TIME} sekund. Dołącz wpisując komendę dołącz!")

        await asyncio.sleep(LOBBY_TIME)

        if not self.registered:
            self.state = "finished"
            await self.channel.send(
                embed=discord.Embed(
                    description="❌ Nikt się nie zapisał. Gra anulowana.",
                    color=COLOR_RED,
                )
            )
            await self.voice.leave_channel()
            return

        self.state = "active"
        names = ", ".join(self.registered.values())
        logger.info(f"[{self.guild_id}] Gra startuje | Gracze: {names}")

        await self.voice.announce("Gra się zaczyna!")

        start_embed = discord.Embed(
            title="✅ Gra zaczyna się!",
            color=COLOR_GREEN,
        )
        start_embed.add_field(name="Gracze", value=names, inline=False)
        start_embed.add_field(name="Rundy", value=str(MAX_ROUNDS), inline=True)
        start_embed.add_field(name="Czas rundy", value=f"{ROUND_TIME}s", inline=True)
        await self.channel.send(embed=start_embed)

        for _ in range(MAX_ROUNDS):
            if self.state != "active":
                break
            await self._run_round()

        await self._end_game()

    async def force_stop(self):
        self.state = "finished"
        await self.channel.send(
            embed=discord.Embed(description="🛑 Gra zatrzymana.", color=COLOR_RED)
        )
        await self.voice.leave_channel()

    # ── Round ──────────────────────────────────────────────────────────────

    async def _run_round(self):
        self.current_round += 1
        available = [l for l in LETTERS if l not in self.used_letters]
        if not available:
            available = list(LETTERS)
            self.used_letters.clear()
        letter = random.choice(available)
        self.used_letters.add(letter)
        round_ = Round(self.current_round, letter)
        self.rounds.append(round_)

        round_embed = discord.Embed(
            title=f"🔤 Runda {self.current_round}/{MAX_ROUNDS} — Litera: {letter}",
            description=(
                f"⏱️ Czas: **{ROUND_TIME} sekund**\n"
                "📩 Wyślij odpowiedzi w **wiadomości prywatnej** do bota!"
            ),
            color=COLOR_BLUE,
        )
        round_embed.add_field(
            name="Format",
            value="`Polska, Poznań, Paweł, Panda, Pinia`",
            inline=False,
        )
        round_embed.add_field(
            name="🏆 Punktacja",
            value="🥇 10 pkt unikalna  •  🥈 5 pkt powtórzona  •  ❌ 0 pkt błędna",
            inline=False,
        )
        # 1. Najpierw bot mówi literę głosowo (czekamy aż skończy)
        await self.voice.announce(
            f"Runda {self.current_round} z {MAX_ROUNDS}. "
            f"Wylosowana litera to: {letter}. "
            f"Macie {ROUND_TIME} sekund!"
        )

        # 2. Dopiero po wypowiedzeniu: embed na czacie + DM do graczy jednocześnie
        await asyncio.gather(
            self.channel.send(embed=round_embed),
            *[self._dm_round_prompt(discord_id, letter, round_.round_number)
              for discord_id in self.registered],
        )

        raw_answers = await self._collect_dm_answers()

        if not raw_answers:
            await self.channel.send(
                embed=discord.Embed(
                    description="📋 Brak odpowiedzi w tej rundzie.",
                    color=COLOR_RED,
                )
            )
            return

        await self.channel.send(
            embed=discord.Embed(description="🔍 Weryfikuję odpowiedzi…", color=COLOR_BLUE)
        )
        validated = await validate_all_answers(raw_answers, letter)

        for discord_id, cat_results in validated.items():
            round_.set_validated_answers(discord_id, cat_results)
            if discord_id not in self.players:
                self.players[discord_id] = Player(
                    discord_id, self.registered.get(discord_id) or discord_id
                )

        points = round_.calculate_points()
        for discord_id, pts in points.items():
            if discord_id in self.players:
                self.players[discord_id].add_points(pts)

        await self._show_round_results(round_, points)

        # Faza zaskarżania — gracze mogą podważyć odrzucone odpowiedzi
        bonus = await self._dispute_phase(round_)
        for discord_id, pts in bonus.items():
            if discord_id in self.players:
                self.players[discord_id].add_points(pts)

        # Organizator ręcznie startuje następną rundę (lub kończy grę)
        if self.state == "active":
            is_last = self.current_round >= MAX_ROUNDS
            await self._wait_for_next_round(is_last=is_last)

    async def _dispute_phase(self, round_: Round) -> dict[str, int]:
        """Gracze mogą zaskarżyć odrzucone odpowiedzi — inni głosują."""
        rejected = [
            (did, cat, ans, self.registered.get(did) or did)
            for did, cat_data in round_.validated_answers.items()
            for cat, (ans, valid, _) in cat_data.items()
            if not valid and ans.strip()
        ]

        if not rejected:
            return {}

        view = AppealView(rejected)
        embed = discord.Embed(
            title="⚖️ Faza zaskarżania",
            description=(
                "Jeśli uważasz że Twoja odpowiedź powinna być zaliczona — kliknij swój przycisk.\n"
                "Pozostali gracze zagłosują czy ją zaakceptować.\n"
                "⏱️ Masz **60 sekund** na zaskarżenie."
            ),
            color=COLOR_YELLOW,
        )
        await self.channel.send(embed=embed, view=view)
        await asyncio.sleep(60)
        view.stop()

        if not view.appealed:
            return {}

        bonus: dict[str, int] = {}
        for discord_id, category, answer in view.appealed:
            player_name = self.registered.get(discord_id, discord_id)
            voter_ids   = [pid for pid in self.registered if pid != discord_id]
            if not voter_ids:
                continue

            vote_view = VoteView(voter_ids)
            embed = discord.Embed(
                title=f"🗳️ Głosowanie — {player_name}",
                description=(
                    f"**Kategoria:** {category}\n"
                    f"**Odpowiedź:** {answer}\n\n"
                    "Czy ta odpowiedź powinna zostać zaliczona?\n"
                    "⏱️ **30 sekund** na zagłosowanie."
                ),
                color=COLOR_YELLOW,
            )
            await self.channel.send(embed=embed, view=vote_view)

            try:
                await asyncio.wait_for(vote_view.all_voted.wait(), timeout=30)
            except asyncio.TimeoutError:
                vote_view.stop()

            yes   = sum(1 for v in vote_view.votes.values() if v)
            total = len(voter_ids)

            if vote_view.accepted():
                bonus[discord_id] = bonus.get(discord_id, 0) + 10
                await self.channel.send(embed=discord.Embed(
                    description=f"✅ **{answer}** ({category}) zaakceptowane! **{player_name}** +10 pkt ({yes}/{total} głosów)",
                    color=COLOR_GREEN,
                ))
            else:
                await self.channel.send(embed=discord.Embed(
                    description=f"❌ **{answer}** ({category}) odrzucone przez społeczność ({yes}/{total} głosów za).",
                    color=COLOR_RED,
                ))

        return bonus

    async def _wait_for_next_round(self, is_last: bool = False) -> None:
        """Czeka aż organizator kliknie przycisk (następna runda lub zakończenie)."""
        view = NextRoundView(str(self.ctx.author.id))

        if is_last:
            for item in view.children:
                if isinstance(item, discord.ui.Button):
                    item.label = "🏁 Zakończ rozgrywkę"
                    item.style = discord.ButtonStyle.red
            desc = "To była ostatnia runda! Organizator klika aby zobaczyć wyniki końcowe."
        else:
            desc = "⏳ Podyskutujcie, a gdy będziecie gotowi — organizator klika **Następna runda**."

        await self.channel.send(
            embed=discord.Embed(description=desc, color=COLOR_BLUE),
            view=view,
        )
        try:
            await asyncio.wait_for(view.ready.wait(), timeout=180)
        except asyncio.TimeoutError:
            view.stop()

    async def _dm_round_prompt(self, discord_id: str, letter: str, round_no: int):
        member = self.ctx.guild.get_member(int(discord_id))
        if member is None:
            return
        dm_embed = discord.Embed(
            title=f"🔤 Runda {round_no}/{MAX_ROUNDS} — Litera: {letter}",
            description=(
                f"Kategorie: **{' | '.join(CATEGORIES)}**\n\n"
                "Wpisz odpowiedzi oddzielone przecinkami:"
            ),
            color=COLOR_BLUE,
        )
        dm_embed.add_field(
            name="Przykład",
            value=f"`Polska, Poznań, Paweł, Panda, Pinia`",
            inline=False,
        )
        dm_embed.set_footer(text=f"⏱️ Masz {ROUND_TIME} sekund!")
        try:
            await member.send(embed=dm_embed)
        except discord.Forbidden:
            await self.channel.send(
                embed=discord.Embed(
                    description=f"⚠️ {member.mention} — zablokowane DM! Odblokuj wiadomości prywatne.",
                    color=COLOR_RED,
                )
            )

    async def _collect_dm_answers(self) -> dict:
        player_ids = list(self.registered.keys())

        async def wait_for_player(discord_id: str):
            def check(m: discord.Message):
                return (
                    isinstance(m.channel, discord.DMChannel)
                    and str(m.author.id) == discord_id
                    and not m.author.bot
                )
            try:
                msg = await asyncio.wait_for(
                    self.ctx.bot.wait_for("message", check=check),
                    timeout=ROUND_TIME,
                )
                return discord_id, msg.content
            except asyncio.TimeoutError:
                return discord_id, None

        tasks = [asyncio.create_task(wait_for_player(pid)) for pid in player_ids]

        # Proporcjonalne ostrzeżenia: 50% i ~15% pozostałego czasu (min 10s)
        warn1_remaining = ROUND_TIME // 2
        warn2_remaining = max(10, ROUND_TIME // 6)

        def _fmt(seconds: int) -> str:
            if seconds >= 60:
                m, s = divmod(seconds, 60)
                min_str = "minuta" if m == 1 else "minuty" if m < 5 else "minut"
                return f"{m} {min_str}" + (f" i {s} sekund" if s else "")
            return f"{seconds} sekund"

        async def send_reminder(delay: int, remaining: int) -> None:
            await asyncio.sleep(delay)
            if all(t.done() for t in tasks):
                return
            fmt = _fmt(remaining)
            dm_text = f"⏰ Zostało **{fmt}**! Wyślij odpowiedzi!"
            pending = [pid for pid, t in zip(player_ids, tasks) if not t.done()]
            # DM do graczy którzy jeszcze nie wysłali
            dm_tasks = []
            for discord_id in pending:
                member = self.ctx.guild.get_member(int(discord_id))
                if member:
                    try:
                        dm_tasks.append(member.send(
                            embed=discord.Embed(description=dm_text, color=COLOR_RED)
                        ))
                    except discord.Forbidden:
                        pass
            # Voice + DM jednocześnie
            await asyncio.gather(
                self.voice.announce(f"Zostało {fmt}! Śpieszcie się!"),
                *dm_tasks,
            )

        reminder_tasks = [
            asyncio.create_task(send_reminder(ROUND_TIME - warn1_remaining, warn1_remaining)),
            asyncio.create_task(send_reminder(ROUND_TIME - warn2_remaining, warn2_remaining)),
        ]

        results = await asyncio.gather(*tasks)

        for rt in reminder_tasks:
            rt.cancel()

        raw: dict = {}
        for discord_id, content in results:
            if content is None:
                continue
            parts = [p.strip() for p in content.split(",")]
            raw[discord_id] = {
                cat: (parts[i] if i < len(parts) else "")
                for i, cat in enumerate(CATEGORIES)
            }
        return raw

    # ── Results display ────────────────────────────────────────────────────

    async def _show_round_results(self, round_: Round, points: dict):
        embed = discord.Embed(
            title=f"📋 Wyniki rundy {round_.round_number}  •  Litera: {round_.letter}",
            color=COLOR_BLUE,
        )

        sorted_ids = sorted(
            list(self.registered.keys()),
            key=lambda x: points.get(x, 0),
            reverse=True,
        )

        for discord_id in sorted_ids:
            username = self.registered.get(discord_id, discord_id)
            pts      = points.get(discord_id, 0)
            answers  = "\n".join(
                f"**{cat}:** {round_.get_answer_display(discord_id, cat)}"
                for cat in CATEGORIES
            )
            embed.add_field(
                name=f"{username}  —  {pts} pkt",
                value=answers,
                inline=True,
            )

        await self.channel.send(embed=embed)

        if points:
            winner_id   = max(points, key=lambda x: points[x])
            winner_name = self.registered.get(winner_id, winner_id)
            await self.voice.announce(f"Zwycięzca rundy: {winner_name}!")

    # ── End game ───────────────────────────────────────────────────────────

    async def _end_game(self):
        self.state = "finished"

        if not self.players:
            await self.channel.send(
                embed=discord.Embed(
                    description="🏁 Koniec gry! Nikt nie zdobył punktów.",
                    color=COLOR_RED,
                )
            )
            await self.voice.leave_channel()
            return

        sorted_players = sorted(
            self.players.values(), key=lambda p: p.total_points, reverse=True
        )

        embed = discord.Embed(
            title="🏁 Koniec gry! Wyniki końcowe",
            color=COLOR_GOLD,
        )
        medals = ["🥇", "🥈", "🥉"]
        podium = ""
        for i, p in enumerate(sorted_players):
            medal   = medals[i] if i < 3 else "•"
            podium += f"{medal} **{p.username}** — {p.total_points} pkt\n"
        embed.description = podium

        total_rounds = len(self.rounds)
        embed.set_footer(text=f"Rozegrano {total_rounds} rund{'ę' if total_rounds == 1 else 'y' if total_rounds in (2,3,4) else ''}")
        await self.channel.send(embed=embed)

        logger.info(
            f"[{self.guild_id}] Gra zakończona | "
            f"Zwycięzca: {sorted_players[0].username} ({sorted_players[0].total_points} pkt)"
        )
        await self.voice.announce(
            f"Koniec gry! Zwycięzcą zostaje: {sorted_players[0].username}, "
            f"z wynikiem {sorted_players[0].total_points} punktów. Gratulacje!"
        )

        for player in self.players.values():
            won = player is sorted_players[0]
            self.db.save_player_stats(self.guild_id, player, won)
        self.db.save_game(self.guild_id, self.rounds, sorted_players)
        await self.stats.update_roles(self.ctx.guild)
        await self.voice.leave_channel()
