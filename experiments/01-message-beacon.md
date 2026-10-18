# 01 — Message beacon

**Question:** Can the LED matrix get someone's attention across the room —
without shouting, without a phone notification?

**Answer:** Yes. It flashes until you press the joystick. Then it tells you
what's up, once, and goes quiet.

## The idea

A physical "you've got mail" light for the house. Someone (a parent, a
housemate) writes a one-line message into a file; the Sense HAT starts
flashing; whoever's near the desk presses the joystick; the message scrolls
by once; the display goes dark until the next message. No app, no account, no
pairing — just light and a button.

That night it carried real cargo: chore reminders.
`"Tommaso help me washing dishes"`, `"Alessandro help with dishes"`, and the
evening's first test, `"Ciao Davide, ricordati di andare a letto!"`.

## What was built

`src/msg-flash.py` — a small state machine:

- **Idle, no message** (`~/led-message.txt` empty): display dark.
- **Message waiting**: hard white/blue blink, ~2.5 Hz. Impossible to ignore,
  easy on the eyes.
- **Button pressed**: clear the matrix, scroll the message once in yellow,
  *empty the message file*, back to dark.

The message file is the entire "API": write a line to it from anywhere
(`echo "dishes!" > ~/led-message.txt`) and the beacon starts flashing. The
button press is the acknowledgment.

## How it works

The Sense HAT joystick appears to Linux as an input device
(`"Raspberry Pi Sense HAT Joystick"` on `/dev/input/event4`). One honest
debugging detour from the night: the `sense_hat` library's `stick.get_events()`
returned **zero events** on this kernel — the presses were happening, the
library just never saw them. The fix was to read the hardware directly with
`evdev`:

```python
joy = InputDevice("/dev/input/event4")   # the Sense HAT joystick
r, _, _ = select.select([joy.fd], [], [], 0.05)
for ev in joy.read():
    if ev.type == 1 and ev.value == 1:    # key press
        pressed = True
```

Any joystick direction counts as a press — no fumbling for the center click.

## What was observed

- The blink is visible across a dim room; the dark-idle state means "no news",
  which is itself information.
- The physicality matters: walking over and pressing the button is a tiny
  ritual that a phone notification can't replicate. The message feels
  *delivered*, not just displayed.
- Clearing the file on read gives exactly-once semantics for free. No
  duplicates, no stale reminders.

## Try it

```bash
pip install --break-system-packages evdev sense-hat
echo "Take out the trash" > ~/led-message.txt
python3 src/msg-flash.py
# press the joystick → message scrolls once → display goes dark
```

## Ideas for extension

- **Per-person colors**: `alice: message` flashes red, `bob: message` blue.
- **Message queue**: keep unread lines, show oldest first, keep flashing
  until the queue drains.
- **Escalation**: blink faster the longer a message waits unread.
- **Two-way**: joystick left/right to reply "ok" / "later", logged with a
  timestamp.
- **Sound**: a piezo buzzer for the truly unreachable teenager.
