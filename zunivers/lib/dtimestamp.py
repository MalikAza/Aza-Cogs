from discord.utils import snowflake_time
from datetime import datetime

class SnowflakeTo():
    """Converting Discord Snowflakes to Discord timestamps."""
    def __init__(self, snowflake):
        tt = snowflake_time(snowflake).timestamp()
        d_timestamp = f"<t:{int(tt)}"

        self.relative = d_timestamp + ":R>"
        self.very_long = d_timestamp + ":F>"
        self.longdate = d_timestamp + ":f>"
        self.longdate_nohour = d_timestamp + ":D>"
        self.short_d = d_timestamp + ":d>"
        self.long_t = d_timestamp + ":T>"
        self.short_t = d_timestamp + ":t>"

class DateTo():
    """Converting date to Discord timestamps."""
    def __init__(self, date):
        date_o = datetime.strptime(date , "%d/%m/%Y %H:%M")
        tt = date_o.timestamp()
        d_timestamp = f"<t:{int(tt)}"

        self.relative = d_timestamp + ":R>"
        self.very_long = d_timestamp + ":F>"
        self.longdate = d_timestamp + ":f>"
        self.longdate_nohour = d_timestamp + ":D>"
        self.short_d = d_timestamp + ":d>"
        self.long_t = d_timestamp + ":T>"
        self.short_t = d_timestamp + ":t>"