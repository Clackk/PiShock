from .pishock import PiShock


def setup(bot):
    bot.add_cog(PiShock(bot))