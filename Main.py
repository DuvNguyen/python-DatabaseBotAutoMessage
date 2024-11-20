import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Sử dụng token trực tiếp (Không nên làm điều này trong thực tế - hãy lưu token trong biến môi trường để bảo mật)
load_dotenv()
discord_token = os.getenv("DISCORD_TOKEN")
TOKEN = discord_token

if TOKEN is None:
    raise ValueError("Token không tìm thấy trong biến môi trường.")

# Tạo intents để bot hoạt động đúng
intents = discord.Intents.default()
intents.messages = True  # Cho phép bot lắng nghe sự kiện tin nhắn
intents.message_content = True  # Cho phép bot truy cập nội dung tin nhắn

# Tạo bot với command_prefix và intents
bot = commands.Bot(command_prefix="!", intents=intents)

# Sự kiện khi bot kết nối đến Discord
@bot.event
async def on_connect():
    print("[on_connect] Connected as", bot.user.name)

# Sự kiện khi bot đã sẵn sàng hoạt động
@bot.event
async def on_ready():
    print("[on_ready] Ready as", bot.user.name)

# Từ điển lưu các lệnh và phản hồi tương ứng
my_commands = {
    '!test': 'Hello World!'
}

# Lệnh để thêm cặp lệnh-phản hồi mới vào từ điển
@bot.command('create')
async def create(ctx, *args):
    if len(args) >= 2:
        # Ghép nối các từ còn lại thành chuỗi, bao gồm xuống dòng
        key = '!' + args[0]  # Lấy lệnh chính (key)
        val = ' '.join(args[1:])  # Ghép toàn bộ phần còn lại thành giá trị (value)

        # Thay thế ký tự xuống dòng
        val = val.replace(r'\n', '\n')  # Thay tất cả '\n' trong văn bản thành dấu xuống dòng thực tế

        # Lưu lệnh vào từ điển
        my_commands[key] = val
        await ctx.reply(f"Đã tạo lệnh `{key}` với nội dung:\n{val}")
    else:
        await ctx.reply("Vui lòng cung cấp đủ tham số. Ví dụ: `!create help <nội dung>`")

# Sự kiện xử lý tin nhắn
@bot.event
async def on_message(msg):
    # Bỏ qua tin nhắn từ bot
    if msg.author.bot:
        return

    # Tách lệnh và các tham số từ nội dung tin nhắn
    cmd, *args = msg.content.split(' ')

    # Nếu lệnh có trong my_commands, trả lời tương ứng
    if cmd in my_commands:
        answer = my_commands[cmd]
        await msg.reply(answer)
    else:
        # Xử lý các lệnh khác
        await bot.process_commands(msg)

# Chạy bot
bot.run(TOKEN)
