# TextUI

A text-first theme for small screens (320x240, 480x272, 480x320, 640x480): lists of names,
the selected one in a pill, the selected game's art at the right, nothing else.

Written directly in REG-Station's theme v2 format (REG-Station `docs/arch/THEME-V2-FORMAT.md`):
no ES source, no converter. Needs a REG-Station build that loads themes written in v2.

Install: copy this directory to `/userdata/themes/TextUI` and pick TextUI as the theme.

| file | holds |
|---|---|
| `v2/theme.json` | the include list |
| `v2/vars.json` | the look by name: colours, font, row height, text sizes |
| `v2/components.json` | the shared nodes: background, title, help bar, list row / pill, buttons, task |
| `v2/views/system.json` | the systems |
| `v2/views/gamelist/basic.json` | a system's games (every gamelist view mode falls back to it) |
| `v2/views/menu.json` | every menu |
| `v2/views/dialog.json` | questions, the keyboard, text viewers, busy / progress, the media viewer |
| `v2/views/screen.json` | over everything: status, notifications, volume, tasks, screensaver |
| `v2/facts.json` | what the frontend reads besides the drawing: the views, no transition |

The font is the frontend's own (`:/Rubik-Regular.ttf`): the theme ships no file but its JSON.

Pictures (from a REG-Station checkout): `tools/textui/shot.sh TextUI 320x240 <dir> "shot=system,ok,wait 300,shot=games"`.
