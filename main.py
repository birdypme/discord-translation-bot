import os

import argostranslate.package
import argostranslate.translate
import discord
from dotenv.main import load_dotenv
import langdetect


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
        print('Initializing Argos Translate package')
        argostranslate.package.update_package_index()
        self.available_packages = argostranslate.package.get_available_packages()
        self.installed_packages = argostranslate.package.get_installed_packages()

    def ensure_package(self, from_code: str, to_code: str):
        for package in self.available_packages:
            if package.from_code != from_code or package.to_code != to_code:
                continue
            if package in self.installed_packages:
                break
            print(f'Translator: Installing package {package}...')
            argostranslate.package.install_from_path(package.download())
            self.installed_packages.append(package)
            break
        else:
            raise ValueError(f'Package not found: {from_code}->{to_code}')

    def translate(self, original_text: str, target_language: str) -> str:
        source_language = langdetect.detect(original_text)
        self.ensure_package(source_language, target_language)
        result = argostranslate.translate.translate(original_text, source_language, target_language)
        return result


def main():
    load_dotenv()
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    translator = Translator()

    @client.event
    async def on_ready():
        print(f'We logged in Discord as {client.user}')

    @client.event
    async def on_reaction_add(reaction, user):
        target_language = languages.get(reaction.emoji)
        if not target_language:
            return
        
        source_message = str(reaction.message.content)
        target_message = translator.translate(source_message, target_language)
        await reaction.message.channel.send(target_message)

    token = os.getenv('DISCORD_TOKEN')
    client.run(token)


if __name__ == '__main__':
    main()
