#!/usr/bin/env python3
"""
Orange Voice Listener - Discord to TTS
Listens for Orange's Discord messages and speaks them aloud.
"""

import discord
import asyncio
import os
import sys

# TTS support
try:
    import pyttsx3
except ImportError:
    print("❌ pyttsx3 not installed!")
    print("   Install with: pip3 install pyttsx3")
    sys.exit(1)


class OrangeVoiceListener(discord.Client):
    def __init__(self, *args, **kwargs):
        # Orange's Discord bot user ID
        self.orange_user_id = kwargs.pop('orange_user_id', None)
        
        # Channels to monitor
        self.monitored_channels = kwargs.pop('channels', [])
        
        super().__init__(*args, **kwargs)
        
        # Initialize TTS
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 180)  # Orange energy!
        self.tts_engine.setProperty('volume', 0.9)
        
        print("🍊 Orange Voice Listener initialized!")
        print(f"   Monitoring user ID: {self.orange_user_id}")
        print(f"   Channels: {self.monitored_channels}")

    async def on_ready(self):
        print(f"✅ Connected as {self.user}!")
        print(f"🎧 Listening for Orange messages...")

    async def on_message(self, message):
        # DEBUG: Show all messages
        channel_name = message.channel.name if hasattr(message.channel, 'name') else str(message.channel)
        print(f"[DEBUG] Message from {message.author.name} (ID: {message.author.id}) in #{channel_name}")
        
        
        # Check if this is Orange's message
        if str(message.author.id) != str(self.orange_user_id):
            print(f"  → Ignoring (wrong user, want {self.orange_user_id})")
            return
        
        # Check if in monitored channel
        if self.monitored_channels and channel_name not in self.monitored_channels:
            print(f"  → Ignoring (wrong channel, want {self.monitored_channels})")
            return
        
        # Speak the message!
        print(f"🍊 [{channel_name}] Orange: {message.content}")
        
        if message.content:
            self.tts_engine.say(message.content)
            self.tts_engine.runAndWait()
        else:
            print("  → No text content to speak")


def main():
    # Configuration
    BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
    ORANGE_USER_ID = os.getenv('ORANGE_USER_ID', '1423002008192815134')
    CHANNELS = os.getenv('MONITOR_CHANNELS', 'amy-🍊').split(',')
    
    if not BOT_TOKEN:
        print("❌ DISCORD_BOT_TOKEN not set!")
        print("   Set it in environment or create .env file")
        sys.exit(1)
    
    # Create client with message content intent
    intents = discord.Intents.default()
    intents.message_content = True
    
    client = OrangeVoiceListener(
        intents=intents,
        orange_user_id=ORANGE_USER_ID,
        channels=CHANNELS
    )
    
    print("🎤 Starting Orange Voice Listener...")
    client.run(BOT_TOKEN)


if __name__ == '__main__':
    main()
