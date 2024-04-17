import discord
from discord.ext import commands
from api import get_market_movers
#from api import spy_info
#from api import get_spy_data
#from api import get_qqq_data
from api import get_stock_info

# Define the intents that your bot will use
intents = discord.Intents.all()
intents.messages = True
intents.message_content = True
intents.dm_messages = True

# Initialize your bot with the specified intents
bot = commands.Bot(command_prefix='/', intents=intents)

# Define a command that the bot can respond to
@bot.command(name='hello')
async def say_hello(ctx):
    await ctx.send('Hello!')

"""
@bot.command(name="spy", description="Get SPY market data")
async def spy_info(ctx):
    spy_data = get_spy_data()
    message = f"SPY Data:\n" \
              f"Previous Close: {spy_data['Previous Close']}\n" \
              f"Close: {spy_data['Close']}\n" \
              f"Percent Change: {spy_data['Percent Change']:.2f}%\n" \
              f"Market Cap: {spy_data['Market Cap']}"
    await ctx.send(message)
"""


"""
@bot.command(name="qqq", description="Get SPY market data")
async def qqq_info(ctx):
    await ctx.send("Fetching QQQ data, please wait...")

    qqq_data = get_qqq_data()

    if qqq_data['Open'] != 'N/A':
        message = (f"**{qqq_data['Symbol']} Data:**\n"
                   f"Open: {qqq_data['Open']}\n"
                   f"Close: {qqq_data['Close']}\n"
                   f"Percent Change: {qqq_data['Percent Change']:.2f}%\n"
                   f"Market Cap: {qqq_data['Market Cap']}")
    else:
        message = "QQQ data is not available at the moment."

    await ctx.send(message)

@bot.command(name="movers", description="Get movers market data")
async def market_movers(ctx):
    message="This will take up to a minute..."
    await ctx.send(message)
    spy_data = get_market_movers()
    if not spy_data.empty:
        for index, row in spy_data.iterrows():
            message = (f"Data for {row['Symbol']}:\n"
                       f"Previous Close: {row['Previous Close']}\n"
                       f"Close: {row['Close']}\n"
                       f"Percent Change: {row['Percent Change']:.2f}%\n"
                       f"Market Cap: {row['Market Cap']}")
            await ctx.send(message)
    else:
        await ctx.send("No market movers found.")
"""


@bot.command(name="info", description="Individual Stock info")
async def info(ctx, ticker: str):
    # Fetch stock information
    stock_data = get_stock_info(ticker)

    # Format and send the message
    message = (f"**{stock_data['name']} ({ticker.upper()})**\n"
               f"Current Price: ${stock_data['current_price']}\n"
               f"Open: ${stock_data['open']}\n"
               f"Previous Day Close: ${stock_data['close']}\n"
               f"Percent Change: {stock_data['percent_change']}%\n"
               f"Market Cap: ${stock_data['market_cap']}\n"
               f"Index: {stock_data['index_name']}")

    await ctx.send(content=message)


@bot.event
async def on_message(message):
    # Process commands first
    await bot.process_commands(message)

    # Then check if the message is a DM and not from the bot itself
    if message.guild is None and not message.author.bot:
        target_guild_id = 1223756905512439988  # Replace with your server ID
        target_channel_id = 1223756905512439993  # Replace with your channel ID

        guild = bot.get_guild(target_guild_id)
        if guild:
            channel = guild.get_channel(target_channel_id)
            if channel:
                # Send text content to the channel
                if message.content:
                    await channel.send(f"New Message: {message.content}")

                # Check if the message has any attachments and send them
                if message.attachments:
                    for attachment in message.attachments:
                        file = await attachment.to_file()
                        await channel.send(f"New Attachment:", file=file)
            else:
                print(f"Channel with ID {target_channel_id} not found.")
        else:
            print(f"Guild with ID {target_guild_id} not found.")

# Run the bot with your token
bot.run('token')
