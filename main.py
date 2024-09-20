import os

import discord
from dotenv.main import load_dotenv
from google.cloud import translate_v2


languages = {
    "🇮🇳": 'hi',
    "🇦🇷": 'es',
    "🇦🇺": 'en',
    "🇧🇩": 'bn',
    "🇧🇷": 'pt',
    "🇨🇦": 'en',
    "🇨🇳": 'zh-CN',
    "🇨🇿": 'cs',
    "🇭🇷": 'hr',
    "🇵🇱": 'pl',
    "🇷🇴": 'ro',
    "🇷🇺": 'ru',
    "🇸🇰": 'sk',
    "🇹🇷": 'tr',
    "🇬🇧": 'en',
    "🇺🇸": 'en',
    "🇫🇷": 'fr',
    "🇩🇪": 'de',
    "🇪🇸": 'es',
    "🇳🇱": 'nl',
    "🇮🇹": 'it',
    "🇬🇦": 'ga',
    "🇵🇹": 'pt',
    "🇳🇵": 'ne',
    "🇸🇷": 'sr',
    "🇺🇦": 'uk',
    "🇻🇳": 'vi',
    "🇮🇩": 'id',
    "🇵🇭": 'tl',
    "🇯🇵": 'ja',
    "🇭🇺": 'hu',
    "🇮🇸": 'is',
    "🇫🇮": 'fi',
    "🇧🇼": 'et',
    "🇧🇬": 'bg',
    "🇮🇱": 'he',
    "🇰🇷": 'ko',
    "🇱🇻": 'lv',
    "🇱🇧": 'lb',
    "🇺🇿": 'uz',
    "🇸🇦": 'ar',
    "🇿🇦": 'af'
}


class Translator:
    def __init__(self):
        print(f'Connecting to Google Cloud with {os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")}')
        self.client = translate_v2.Client()

    def translate(self, original_text: str, target_language: str) -> str:
        result = self.client.translate(original_text, target_language=target_language)
        # dict keys: input, translatedText, detectedSourceLanguage
        return result['translatedText']


def main():
    load_dotenv()
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    translator = Translator()

    @client.event
    async def on_ready():
        print(f'We logged in as {client.user}')

    @client.event
    async def on_reaction_add(reaction, user):
        print(f'got reaction {reaction} from {user}')
        print(f'reaction.emoji={reaction.emoji}')
        if not reaction.emoji:
            return
        
        target_language = languages.get(reaction.emoji)
        print(f'target_language={target_language}')
        if not target_language:
            return
        
        source_message = str(reaction.message.content)
        print(f'Translating {source_message!r} to {target_language} for {user}')
        target_message = translator.translate(source_message, target_language)
        print(f"Translation is {target_message}")
        await reaction.message.channel.send(target_message)

    token = os.getenv('DISCORD_TOKEN')
    client.run(token)


if __name__ == '__main__':
    main()
