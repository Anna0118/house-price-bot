from process_data import process_data
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)

class HousePriceBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='!', intents=intents)

    async def on_ready(self):
        # Prevent re-execution if already sent
        if getattr(self, '_sent', False): return
        self._sent = True

        channel_id = int(os.getenv('DISCORD_CHANNEL_ID') or 0)
        channel = self.get_channel(channel_id)
        if not channel:
            print(f"❌ Channel ID {channel_id} not found.")
            return
        # Fetch real estate data for multiple regions
        results = process_data()

        for file_key, records, excel_path in results:
            # Construct embed message for each region
            embed = discord.Embed(
                title=f"🏠 房價資訊 - {file_key}",
                description="每月1, 11, 21號更新",
                color=0x3498db
            )
            # Add up to 25 records as fields (Discord limit)
            for idx, item in enumerate(records[:25], start=1):
                parking_price = item['車位總價元']
                parking_price_str = f"{int(parking_price):,}元" if parking_price and str(parking_price) != 'nan' else "無"
                parking_type = item['車位類別'] if str(item['車位類別']) != 'nan' else "無"
                project_name = item['建案名稱'] if str(item['建案名稱']) != 'nan' else "—"
                price_wan = round(item['總價元'] / 10000)
                name = f"{idx}. {project_name} | {item['鄉鎮市區']} | {price_wan}萬元 | {item['交易年月日']}"
                value = (
                    f"格局：{item['建物現況格局-房']}房 "
                    f"{item['建物現況格局-廳']}廳 "
                    f"{item['建物現況格局-衛']}衛／隔間：{item['建物現況格局-隔間']}\n"
                    f"含車位：{item['含車位坪數']:.2f}坪，{item['含車位單價萬坪']:.1f}萬/坪\n"
                    f"不含車位：{item['不含車位坪數']:.2f}坪，{item['不含車位單價萬坪']:.1f}萬/坪\n"
                    f"車位：{parking_type} ({parking_price_str})\n"
                    f"樓層：{item['移轉層次']}/{item['總樓層數']}\n"
                    f"樓型：{item['建物型態']}\n"
                    f"都市土地使用分區：{item['都市土地使用分區']}\n"
                    f"建案：{project_name}\n"
                    f"棟及號：{item['棟及號']}\n"
                    f"備註：{item['備註']}"
                )
                embed.add_field(name=name, value=value, inline=False)
            # Send embed and attached Excel file to channel
            await channel.send(embed=embed)
            await channel.send("完整檔案：", file=discord.File(excel_path))
        # Close bot after processing all results
        await self.close()

def main():
    # Get bot token from environment
    token = os.getenv('DISCORD_TOKEN')
    print(token)
    if not token:
        print("❌ DISCORD_TOKEN not found.")
        return

    # Run the bot
    bot = HousePriceBot()
    bot.run(token)

if __name__ == "__main__":
    main()