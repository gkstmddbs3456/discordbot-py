import discord
import random
import asyncio

client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
    print(f'{client.user}으로 로그인 성공!')
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content == "!인증":
        embed = discord.Embed(title="인증코드 발급", description="DM으로 인증코드를 발송했습니다. DM을 확인해주세요!")
        await message.channel.send(embed=embed)
        code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890', k=8))
        embed = discord.Embed(title="인증코드", description=f"아래의 인증코드를 60초 이내에 !인증 (인증코드)로 입력해주세요.\n`{code}`")
        await message.author.send(embed=embed)
        
        def check(msg):
            return msg.author == message.author and msg.content == f"!인증 {code}"
        
        try:
            await client.wait_for('message', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            embed = discord.Embed(title="인증 시간 초과", description="인증 시간이 초과되었습니다. 다시 시도해주세요.")
            await message.author.send(embed=embed)
        else:
            role = discord.utils.get(message.guild.roles, name="[ 인증완료유저 ]")
            await message.author.add_roles(role)
            embed = discord.Embed(title="인증 완료", description="인증이 완료되었습니다. 인증완료유저 역할이 부여되었습니다.")
            await message.author.send(embed=embed)
            
client.run('MTA4OTA1Mjc1NjQxNDgyODU1NA.GrdO0m.a2JuJns3EpWYm9EGJ6RiKa4RCP2MjkfZSNhw6E')
