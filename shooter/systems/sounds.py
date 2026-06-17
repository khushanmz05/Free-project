"""
sounds.py
---------
Procedurally generated sound effects using numpy + pygame.
No external audio files needed.
"""

import pygame
import numpy as np

SAMPLE_RATE = 44100
pygame.mixer.pre_init(SAMPLE_RATE, -16, 1, 512)


def _make_sound(samples):
    """Convert a numpy float array [-1, 1] to a pygame Sound."""
    data = np.clip(samples, -1, 1)
    data = (data * 32767).astype(np.int16)
    return pygame.sndarray.make_sound(data)


def _sine(freq, duration, volume=1.0, fade_out=True):
    t      = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    wave   = np.sin(2 * np.pi * freq * t) * volume
    if fade_out:
        fade   = np.linspace(1, 0, len(wave))
        wave  *= fade
    return wave


def _noise(duration, volume=0.5):
    samples = int(SAMPLE_RATE * duration)
    return (np.random.uniform(-1, 1, samples) * volume)


def _env(wave, attack=0.01, decay=0.1):
    n       = len(wave)
    atk     = int(attack * SAMPLE_RATE)
    dcy     = int(decay  * SAMPLE_RATE)
    env     = np.ones(n)
    env[:atk]       = np.linspace(0, 1, atk)
    if atk + dcy < n:
        env[atk:atk+dcy] = np.linspace(1, 0, dcy)
        env[atk+dcy:]    = 0
    return wave * env


def _make_pistol():
    t    = np.linspace(0, 0.12, int(SAMPLE_RATE * 0.12), False)
    freq = np.linspace(800, 200, len(t))
    wave = np.sin(2 * np.pi * freq * t / SAMPLE_RATE * SAMPLE_RATE)
    wave += _noise(0.12, 0.4)
    return _make_sound(_env(wave * 0.6, attack=0.001, decay=0.10))


def _make_shotgun():
    t    = np.linspace(0, 0.25, int(SAMPLE_RATE * 0.25), False)
    freq = np.linspace(300, 80, len(t))
    wave = np.sin(2 * np.pi * freq * t / SAMPLE_RATE * SAMPLE_RATE)
    wave += _noise(0.25, 0.7)
    return _make_sound(_env(wave * 0.8, attack=0.001, decay=0.20))


def _make_smg():
    t    = np.linspace(0, 0.07, int(SAMPLE_RATE * 0.07), False)
    freq = np.linspace(600, 300, len(t))
    wave = np.sin(2 * np.pi * freq * t / SAMPLE_RATE * SAMPLE_RATE)
    wave += _noise(0.07, 0.3)
    return _make_sound(_env(wave * 0.5, attack=0.001, decay=0.06))


def _make_sniper():
    t    = np.linspace(0, 0.30, int(SAMPLE_RATE * 0.30), False)
    freq = np.linspace(1200, 100, len(t))
    wave = np.sin(2 * np.pi * freq * t / SAMPLE_RATE * SAMPLE_RATE)
    wave += _noise(0.30, 0.2)
    return _make_sound(_env(wave * 0.9, attack=0.001, decay=0.28))


def _make_hit():
    wave = _noise(0.06, 0.6)
    wave += _sine(300, 0.06, 0.3)
    return _make_sound(_env(wave, attack=0.001, decay=0.05))


def _make_death():
    t    = np.linspace(0, 0.35, int(SAMPLE_RATE * 0.35), False)
    freq = np.linspace(400, 80, len(t))
    wave = np.sin(2 * np.pi * freq * t / SAMPLE_RATE * SAMPLE_RATE)
    wave += _noise(0.35, 0.3)
    return _make_sound(_env(wave * 0.7, attack=0.002, decay=0.30))


def _make_pickup():
    w1   = _sine(600,  0.08, 0.5)
    w2   = _sine(800,  0.08, 0.5)
    w3   = _sine(1000, 0.08, 0.5)
    wave = np.concatenate([w1, w2, w3])
    return _make_sound(_env(wave, attack=0.01, decay=0.20))


def _make_low_hp():
    w1   = _sine(440, 0.10, 0.4)
    gap  = np.zeros(int(SAMPLE_RATE * 0.05))
    w2   = _sine(440, 0.10, 0.4)
    wave = np.concatenate([w1, gap, w2])
    return _make_sound(wave)


def _make_wave_start():
    w1   = _sine(300, 0.12, 0.4)
    w2   = _sine(400, 0.12, 0.4)
    w3   = _sine(600, 0.20, 0.5)
    wave = np.concatenate([w1, w2, w3])
    return _make_sound(_env(wave, attack=0.01, decay=0.35))


def _make_boss_hit():
    wave = _noise(0.10, 0.5)
    wave += _sine(150, 0.10, 0.6)
    return _make_sound(_env(wave * 0.9, attack=0.001, decay=0.09))


class SoundManager:
    def __init__(self):
        pygame.mixer.init(SAMPLE_RATE, -16, 1, 512)
        self.sounds = {
            "pistol":     _make_pistol(),
            "shotgun":    _make_shotgun(),
            "smg":        _make_smg(),
            "sniper":     _make_sniper(),
            "hit":        _make_hit(),
            "death":      _make_death(),
            "pickup":     _make_pickup(),
            "low_hp":     _make_low_hp(),
            "wave_start": _make_wave_start(),
            "boss_hit":   _make_boss_hit(),
        }
        self.set_volume(0.6)
        self._low_hp_timer = 0

    def set_volume(self, vol):
        for s in self.sounds.values():
            s.set_volume(vol)

    def play(self, name):
        s = self.sounds.get(name)
        if s:
            s.play()

    def play_shoot(self, weapon_name):
        mapping = {
            "Pistol":  "pistol",
            "Shotgun": "shotgun",
            "SMG":     "smg",
            "Sniper":  "sniper",
        }
        self.play(mapping.get(weapon_name, "pistol"))

    def update(self, player):
        """Call once per frame for timed sounds like low HP warning."""
        now = pygame.time.get_ticks()
        if player.hp <= 30 and now - self._low_hp_timer > 1500:
            self.play("low_hp")
            self._low_hp_timer = now