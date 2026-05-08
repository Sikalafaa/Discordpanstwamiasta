import asyncio
import logging
import os
import tempfile
from functools import partial

import discord
import pyttsx3
from gtts import gTTS

logger = logging.getLogger("panstwa_bot.voice")


class VoiceManager:
    def __init__(self):
        self.voice_client: discord.VoiceClient | None = None

    async def join_channel(self, channel: discord.VoiceChannel) -> None:
        try:
            if self.voice_client and self.voice_client.is_connected():
                await self.voice_client.move_to(channel)
            else:
                self.voice_client = await channel.connect()
            logger.info(f"Dołączono do kanału głosowego: {channel.name}")
        except Exception as e:
            logger.error(f"Błąd dołączania do voice: {e}", exc_info=True)

    async def leave_channel(self) -> None:
        if self.voice_client and self.voice_client.is_connected():
            try:
                await self.voice_client.disconnect()
                logger.info("Rozłączono z kanałem głosowym.")
            except Exception as e:
                logger.warning(f"Błąd rozłączania: {e}")
            finally:
                self.voice_client = None

    async def announce(self, text: str) -> None:
        if not self.voice_client or not self.voice_client.is_connected():
            return
        if self.voice_client.is_playing():
            self.voice_client.stop()

        audio_path = None
        try:
            loop = asyncio.get_event_loop()

            # 1. Próbuj gTTS (dobra jakość, wymaga internetu)
            try:
                audio_path = _tmp_path(".mp3")
                await asyncio.wait_for(
                    loop.run_in_executor(None, partial(_gtts_save, text, audio_path)),
                    timeout=6,
                )
                logger.debug(f"TTS (gTTS): {text[:40]}")
            except Exception as e:
                logger.warning(f"gTTS niedostępne ({e}) — używam lokalnego TTS.")
                _safe_delete(audio_path)

                # 2. Fallback — pyttsx3 (offline, wbudowany w Windows)
                audio_path = _tmp_path(".wav")
                await loop.run_in_executor(None, partial(_pyttsx3_save, text, audio_path))
                logger.debug(f"TTS (pyttsx3): {text[:40]}")

            if not audio_path or not os.path.exists(audio_path):
                logger.error("Plik audio nie został wygenerowany.")
                return

            size = os.path.getsize(audio_path)
            if size < 512:
                logger.error(f"Plik audio zbyt mały ({size}B) — pomijam.")
                _safe_delete(audio_path)
                return

            await self._play(audio_path, loop)

        except Exception as e:
            logger.error(f"Błąd announce(): {e}", exc_info=True)
            _safe_delete(audio_path)

    async def _play(self, path: str, loop: asyncio.AbstractEventLoop) -> None:
        done = asyncio.Event()

        def _after(error):
            if error:
                logger.error(f"Błąd odtwarzania: {error}")
            _safe_delete(path)
            loop.call_soon_threadsafe(done.set)

        if not self.voice_client:
            return
        self.voice_client.play(
            discord.FFmpegPCMAudio(path, before_options="-loglevel quiet"),
            after=_after,
        )
        try:
            await asyncio.wait_for(done.wait(), timeout=30)
        except asyncio.TimeoutError:
            logger.warning("Timeout odtwarzania — przerywam.")
            if self.voice_client and self.voice_client.is_playing():
                self.voice_client.stop()


# ── Helpers ────────────────────────────────────────────────────────────────

def _tmp_path(ext: str) -> str:
    with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as f:
        return f.name


def _gtts_save(text: str, path: str) -> None:
    gTTS(text=text, lang="pl", slow=False).save(path)


def _pyttsx3_save(text: str, path: str) -> None:
    engine = pyttsx3.init()
    # Ustaw polski głos jeśli dostępny
    voices = engine.getProperty("voices")
    for voice in (voices if isinstance(voices, list) else []):
        name = (voice.name or "").lower()
        vid  = (voice.id  or "").lower()
        if "polish" in name or "paulina" in name or "pl" in vid:
            engine.setProperty("voice", voice.id)
            logger.debug(f"Polski głos pyttsx3: {voice.name}")
            break
    engine.setProperty("rate", 150)
    engine.setProperty("volume", 1.0)
    engine.save_to_file(text, path)
    engine.runAndWait()
    engine.stop()


def _safe_delete(path: str | None) -> None:
    if path and os.path.exists(path):
        try:
            os.remove(path)
        except OSError:
            pass
