# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook

mod = "mod4"

keys = [
    # Switch between windows in current stack pane
    Key(
        [mod], "k",
        lazy.layout.down()
    ),
    Key(
        [mod], "j",
        lazy.layout.up()
    ),

    # Move windows up or down in current stack
    Key(
        [mod, "control"], "k",
        lazy.layout.shuffle_down()
    ),
    Key(
        [mod, "control"], "j",
        lazy.layout.shuffle_up()
    ),

    # Switch window focus to other pane(s) of stack
    Key(
        [mod], "space",
        lazy.layout.next()
    ),

    # Swap panes of split stack
    Key(
        [mod, "shift"], "space",
        lazy.layout.rotate()
    ),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"], "Return",
        lazy.layout.toggle_split()
    ),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.nextlayout()),
    Key([mod], "w", lazy.window.kill()),

    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown()),
    Key([mod], "r", lazy.spawncmd()),

    Key([mod], "F2", lazy.screen.nextgroup()),
    Key([mod], "F11", lazy.window.toggle_fullscreen()),

    # applications
    Key([mod], "Return", lazy.spawn("konsole")),
    Key([], "XF86Mail", lazy.spawn("/home/fungos/Qt/Tools/QtCreator/bin/qtcreator")),
    Key([], "XF86HomePage", lazy.spawn("firefox")),
    Key([], "XF86Calculator", lazy.spawn("kcalc")),
    #Key([], "XF86Sleep", )),

    # does not work
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -c 0 -q set Master 2dB+")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -c 0 -q set Master 2dB-")),
    Key([], "XF86AudioMute", lazy.spawn("amixer -c 0 -q set Master toggle")),
    Key([], "XF86AudioStop", lazy.spawn("amixer -c 0 -q set Master toggle")),
]

groups = [Group(i) for i in "as"]

for i in groups:
    # mod1 + letter of group = switch to group
    keys.append(
        Key([mod], i.name, lazy.group[i.name].toscreen())
    )

    # mod1 + shift + letter of group = switch to & move focused window to group
    keys.append(
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name))
    )

layouts = [
    layout.Max(),
    layout.Stack(num_stacks=2),
    layout.Tile(ratio=0.50, masterWindows=2),
    #layout.Slice('left', 192, name='gimp', role='gimp-toolbox', fallback=layout.Slice('right', 256, role='gimp-dock', fallback=layout.Stack(stacks=1, border_width=1))),
]

widget_defaults = dict(
    font='Arial',
    fontsize=12,
    padding=3,
)

floating_layout = layout.Floating(auto_float_types=[
    "notification",
    "toolbar",
    "splash",
    "dialog",
])

font_color='#000000'
bg_color='cfd2d3'

screens = [
    Screen(
    ),
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(active="#ffffff", fontsize=11, foreground=font_color),
                widget.AGroupBox(border="#990000", foreground=font_color),
                widget.Prompt(foreground=font_color),
                widget.WindowName(foreground=font_color),
                widget.TextBox("fungos", name="default", foreground=font_color),
                widget.Sep(),
                widget.MemoryGraph(frequency=5),
                widget.DF(partition='/home'),
                widget.Sep(),
                widget.Net(foreground=font_color),
                widget.Sep(),
                widget.Systray(),
                widget.Volume(foreground=font_color),
                widget.Clock(format='%y-%m-%d %a %H:%M', foreground=font_color),
            ],
            24,
            background=bg_color,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
        start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
        start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating()
auto_fullscreen = True

@hook.subscribe.client_new
def floating_dialogs(window):
    dialog = window.window.get_wm_type() == 'dialog'
    transient = window.window.get_wm_transient_for()
    if dialog or transient:
        window.floating = True
