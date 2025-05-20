import discord
from discord.ext import commands, tasks
import os
from datetime import datetime, time
from download_data import download_plvr_data
import process_data
from dotenv import load_dotenv

class HousePriceBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='!', intents=intents)
        load_dotenv(override=True)  # ← 一定要先載入 env

    async def setup_hook(self):
        # 這裡 bot 已經 logged in，cache 也建立好了
        # 在 setup_hook 或 on_ready 裡啟動你的週期任務
        if not self.check_and_send_updates.is_running():
            self.check_and_send_updates.start()
        print("Bot setup complete!")

    async def on_ready(self):
        print(f"Bot {self.user} is ready! 連接的伺服器數量: {len(self.guilds)}")

    # @tasks.loop(time=time(hour=10, minute=0, second=0))  # 每天 10:00 執行
    async def check_and_send_updates(self):
        channel_id = int(os.getenv('DISCORD_CHANNEL_ID') or 0)
        channel = self.get_channel(channel_id)
        if not channel:
            print(f"找不到頻道 ID {channel_id}，請確認 bot 有權限讀取該頻道。")
            return

        # 下載並處理資料
        filename = download_plvr_data()
        if filename:
            formatted_message = process_data()
            await channel.send("房價資料更新完成！")
            await channel.send(formatted_message)
            await channel.send(file=discord.File(filename))
        else:
            await channel.send("下載資料失敗，請稍後再試。")

def main():
    bot = HousePriceBot()
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        print("錯誤：找不到 Discord Token，請檢查 .env")
        return
    bot.run(token)

if __name__ == "__main__":
    main()
