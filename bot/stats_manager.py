import discord

ROLE_NAMES = {
    0: "🥇 Champion",
    1: "🥈 Runner-up",
    2: "🥉 Third Place",
}


class StatsManager:
    def __init__(self, db):
        self.db = db

    async def update_roles(self, guild: discord.Guild):
        """Remove all existing game roles, then award them to the current top 3."""
        await self.clear_roles(guild)

        top = self.db.get_leaderboard(str(guild.id), limit=3)
        colours = [discord.Colour.gold(), discord.Colour.light_grey(), discord.Colour.from_rgb(205, 127, 50)]

        for i, player in enumerate(top):
            if player.total_points == 0:
                continue
            role_name = ROLE_NAMES[i]
            role = discord.utils.get(guild.roles, name=role_name)
            if not role:
                try:
                    role = await guild.create_role(
                        name=role_name,
                        colour=colours[i],
                        reason="Państwa-Gra: automatyczne nadanie roli",
                    )
                except discord.Forbidden:
                    continue
            member = guild.get_member(int(player.discord_id))
            if member:
                try:
                    await member.add_roles(role)
                except discord.Forbidden:
                    pass

    async def clear_roles(self, guild: discord.Guild):
        """Remove all three game roles from every member who holds them."""
        for role_name in ROLE_NAMES.values():
            role = discord.utils.get(guild.roles, name=role_name)
            if role is None:
                continue
            for member in list(role.members):
                try:
                    await member.remove_roles(role)
                except discord.Forbidden:
                    pass

    def get_top3(self, guild_id: str):
        return self.db.get_leaderboard(guild_id, limit=3)
