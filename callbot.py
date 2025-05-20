# 在你的 discord_helper.py
from process_data import process_data
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# 一開始就載入環境變數
load_dotenv(override=True)

class HousePriceBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='!', intents=intents)

    async def on_ready(self):
        if getattr(self, '_sent', False): return
        self._sent = True

        channel_id = int(os.getenv('DISCORD_CHANNEL_ID') or 0)
        channel = self.get_channel(channel_id)
        if not channel:
            print(f"❌ 找不到頻道 ID {channel_id}")
            return

        # 處理資料並取得前 5 筆 + 檔案路徑
        records, excel_path = process_data()

        # 建立 Embed
        embed = discord.Embed(
            title="🏠 頭份市 & 竹南鎮 房價前五筆快覽",
            description="— 前20筆成交資料 —",
            color=0x3498db
        )
        for idx, item in enumerate(records, start=1):
            name = f"{idx}. {item['交易年月日']} | {item['鄉鎮市區']} | {item['總價元']}元"
            value = (
                f"層次：{item['移轉層次']}／總樓層：{item['總樓層數']}\n"
                f"樓型：{item['建物型態']} ({item['主要用途']})\n"
                f"格局：{item['建物現況格局-房']}房 "
                f"{item['建物現況格局-廳']}廳 "
                f"{item['建物現況格局-衛']}衛／隔間：{item['建物現況格局-隔間']}\n"
                f"車位：{item['車位類別']} ({item['車位總價元']}元)\n"
                f"建案：{item['建案名稱']}／{item['棟及號']}"
            )
            embed.add_field(name=name, value=value, inline=False)

        # 傳 Embed
        await channel.send(embed=embed)
        # 再附完整 Excel
        await channel.send("完整 Excel 檔：", file=discord.File(excel_path))
        await self.close()


def main():
    token = os.getenv('DISCORD_TOKEN')
    print(token)
    if not token:
        print("❌ 找不到 DISCORD_TOKEN")
        return
    bot = HousePriceBot()
    bot.run(token)

if __name__ == "__main__":
    main()