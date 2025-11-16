# MultiToggleWithDelay – CraftBeerPi 4 Plugin

This CraftBeerPi 4 plugin adds a step that can toggle up to **10 actors in sequence**, each followed by its own configurable delay in seconds.

## ✨ Features

- Control **1 to 10 actors**
- Each actor has:
  - ON / OFF toggle
  - Independent delay (in seconds)
- Executes in a chained sequence:


- Non-blocking (async)
- Uses native CBPi timer display

---

## 📦 Installation

SSH into your Raspberry Pi:

```bash
cd ~/craftbeerpi4/modules
git clone https://github.com/mikehenrytts/MultiToggleWithDelay.git
sudo systemctl restart cbpi
