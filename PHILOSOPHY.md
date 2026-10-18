# Experiment-first tinkering

*Why a night of Raspberry Pi demos belongs in a lab notebook, and what
disappears when the friction does.*

## The scene

It's 11:30 PM. On the desk: two Raspberry Pi 4s, a Sense HAT with its 8×8 LED
matrix, a USB camera, and a micro:bit. The goal isn't a product. There is no
sprint board. There is just curiosity and a string of small questions:

- *Can the LED matrix nag someone about the dishes?*
- *Can 64 pixels look like fire?*
- *What does counting to a thousand feel like, one second at a time?*
- *Can the camera become a light meter?*
- *Can the Pi see its own display?*

By 1:15 AM, all seven questions had answers — running on real hardware,
observed with real eyes. Nothing about that night was remarkable except the
speed, and the speed is the whole point.

## The old way: anatomy of friction

Consider what the *first* experiment — the message beacon — would have cost
a year ago, done by hand:

1. **Unbox and identify.** Which HAT revision? Is I2C enabled? (`raspi-config`,
   reboot.)
2. **Library roulette.** `sense-hat` vs `sensehat` vs RTIMU; a pinned version
   from a 2019 blog post that no longer installs on Bookworm.
3. **The joystick problem.** The `sense_hat` stick API silently returns no
   events on this kernel (we hit exactly this). Now you're reading DAPLink
   source, `evdev` docs, and `/proc/bus/input/devices` at midnight.
4. **Process management.** `nohup`, `setsid`, log files, the classic
   `pkill -f` that matches its own SSH command line and kills your session.
5. **Iteration tax.** Every behavior change — "flash harder", "any button, not
   just the middle one", "stop flashing once read" — is another edit, another
   `scp`, another restart, another round of "did it pick up the new file?"

None of this is *hard*. That's the insult of it. It's all *tax* — a dozen
small tolls between the question and the observation. Most evenings, the tax
exceeds the curiosity budget, and the HAT goes back in the drawer.

## The gadget way: conversation as compiler

That night, the loop looked like this instead:

> **Human:** "make it flash"
> **A few minutes later:** the matrix is flashing.
>
> **Human:** "make it that if there is a new message, it flashes; once I click
> the button and read the message, clear the message and don't flash anymore"
> **A few minutes later:** exactly that behavior, running.

The requests got *shorter* as the night went on — "Show me the fire simulator",
"Make a display that count 1-1000", "One sec interval", "Do it. Fast." Each
one is barely a sentence. Behind each sentence, an agent did the unglamorous
work: SSH hops between the Pis, `pip install --break-system-packages evdev`,
killing the process whose name matched its own kill command, restarting the
Flask server, copying the script across. The human never typed a command.

This is what "Muse Gadgets" means in practice here: **the plumbing still
exists, but it stopped being the human's job.** The scripts in `src/` are the
receipts — real, readable Python, reproducible any time. The difference is who
paid the tax.

## What changes when the HOW disappears

With the friction delegated, three things move to the foreground — the only
three things that were ever the point:

**1. The question.** "Can the Pi see its own display?" is a better evening
than "why is `get_events()` empty?" The first is science; the second is
toil. That night's questions were small, but they were *questions*, asked and
answered.

**2. The observation.** When the color wheel spun under the camera and the
dashboard's red trace spiked, then green, then blue — that was observed live,
on a phone, at 1 AM. Nobody was watching a terminal for tracebacks. The
reward loop stayed tight: change something, *see* something.

**3. The data.** The RGB dashboard exists because someone wanted to *watch a
signal move* — hand over the lens, traces fall; hand away, traces rise. The
artifact of the night isn't the Flask app. It's the habit of asking "what
would I measure?" before "how would I build it?"

## An honest ledger

Nothing here claims the friction is *gone*. It moved. Someone — or something
— still debugged the silent joystick, still restarted the dead process, still
chose `opencv-python-headless` over the full build. The honest claim is
narrower: **the human's evening was spent on decisions only a human can make**
— what to try, what counts as working, what's interesting — while everything
below that line was delegated.

There's a second honest point: speed has a failure mode, which is shallowness.
Seven demos in two hours can be seven toys. What keeps it science is the
notebook habit — which is why this repo exists. Each experiment records the
question, the build, the observation, and the next question. The demos are
disposable. The *record* compounds.

## The real demo

The most telling experiment wasn't the fire or the dashboard. It was the
message beacon, because it left the lab: "Alessandro help with dishes,"
flashing on a desk until a button press cleared it. A tiny domestic
notification system, specified in one rambling sentence at 11:31 PM, working
by 11:35.

That's the pitch, stripped of romance: **an idea you have at night should be
running before the idea cools.** Everything else — the repos, the Pages site,
the diagrams — is scaffolding around that one capability.

Midland is the notebook. The night was the argument.
