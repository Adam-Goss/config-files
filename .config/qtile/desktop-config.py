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

import os
import re
import socket
import subprocess
from libqtile import qtile
from libqtile.config import Click, Drag, Group, KeyChord, Key, Match, Screen
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.lazy import lazy
from typing import List  # noqa: F401


mod = "mod4"
#terminal = guess_terminal()
terminal = "gnome-terminal tmux"
terminal2 = "alacritty"

keys = [
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(),
        desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(),
        desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(terminal2 + " -e tmux"), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(),
        desc="Spawn a command using a prompt widget"),

    # start ulauncher
    Key([mod], "s", lazy.spawn("ulauncher"),desc="Launch ulauncher"),

    # start file manager
    Key([mod], "f", lazy.spawn("nautilus"),desc="Launch file manager"),

    # start obsidian
    Key([mod], "o", lazy.spawn("obsidian"),desc="Launch obsidian notes"),

    # screenshot with flameshot
    Key([], "Print", lazy.spawn("flameshot gui"),desc="Launch flameshot"),


    # volume controls
    Key([mod], "F11", lazy.spawn("amixer set 'Master' 5%-"),desc="decrease volume"),
    Key([mod], "F12", lazy.spawn("amixer set 'Master' 5%+"),desc="decrease volume"),
    
    ### Switch focus to specific monitor (out of three)
    Key([mod], "w",
        lazy.to_screen(0),
        desc='Keyboard focus to monitor 1'
        ),
    Key([mod], "e",
        lazy.to_screen(1),
        desc='Keyboard focus to monitor 2'
        ),
    # Key([mod], "r",
    #     lazy.to_screen(2),
    #     desc='Keyboard focus to monitor 3'
    #     ),
    ### Switch focus of monitors
    Key([mod], "period",
        lazy.next_screen(),
        desc='Move focus to next monitor'
        ),
    Key([mod], "comma",
        lazy.prev_screen(),
        desc='Move focus to prev monitor'
        ),

]

groups = [Group(i) for i in "123456789"]
for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name)),
        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(i.name)),
        # Or, use below if you prefer not to switch to that group.
        # # mod1 + shift + letter of group = move focused window to group
        Key([mod, "control"], i.name, lazy.window.togroup(i.name),
            desc="move focused window to group {}".format(i.name)),
    ])


layout_theme = {"border_width": 2,
                "margin": 20,
                "border_focus": "e1acff",
                "border_normal": "1D2330"
}


layouts = [
    layout.Columns(border_focus_stack='#d75f5f'),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    #layout.Bsp(),
    #layout.Matrix(),
    layout.MonadTall(**layout_theme),
    layout.MonadWide(),
    #layout.RatioTile(),
    #layout.Tile(),
    #layout.TreeTab(),
    #layout.VerticalTile(),
    # layout.Zoomy(),
]


colors = [["#282c34", "#282c34"], # panel background
          ["#3d3f4b", "#434758"], # background for current screen tab
          ["#ffffff", "#ffffff"], # font color for group names
          ["#ff5555", "#ff5555"], # border line color for current tab
          ["#74438f", "#74438f"], # border line color for 'other tabs' and color for 'odd widgets'
          ["#4f76c7", "#4f76c7"], # color for the 'even widgets'
          ["#e1acff", "#e1acff"], # window name
          ["#ecbbfb", "#ecbbfb"]] # backbround for inactive screens

prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())

##### DEFAULT WIDGET SETTINGS #####
widget_defaults = dict(
    font="Ubuntu Mono",
    fontsize = 16,
    padding = 2,
    background=colors[5]
)
extension_defaults = widget_defaults.copy()

def init_widgets_list():
    prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())

    widgets_list = [
                widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       foreground = colors[2],
                       background = colors[0]
                       ),
                widget.Image(
                       filename = "~/.config/qtile/icons/Fsociety_logo.jpg",
                       scale = "False",
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn("code /home/adam/.config/qtile/config.py")}
                       ),
               widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       foreground = colors[2],
                       background = colors[0]
                       ),
                widget.GroupBox(
                       font = "Ubuntu Bold",
                       fontsize = 11,
                       margin_y = 3,
                       margin_x = 0,
                       padding_y = 5,
                       padding_x = 3,
                       borderwidth = 3,
                       active = colors[2],
                       inactive = colors[7],
                       rounded = False,
                       highlight_color = colors[1],
                       highlight_method = "line",
                       this_current_screen_border = colors[6],
                       this_screen_border = colors [4],
                       other_current_screen_border = colors[6],
                       other_screen_border = colors[4],
                       foreground = colors[2],
                       background = colors[0]
                       ),
                # widget.Prompt(
                #        prompt = prompt,
                #        font = "Ubuntu Mono",
                #        padding = 5,
                #        foreground = colors[3],
                #        background = colors[1],
                #        fontsize = 7,
                #        ),
                widget.TextBox(
                    text = ' | ',
                    background = colors[0],
                    foreground = colors[4],
                    padding = 0,
                    fontsize = 20
                ),
                widget.WindowName(
                       foreground = colors[6],
                       background = colors[0],
                       padding = 0,
                       fontsize = 15,
                       font = "Ubuntu Mono",
                       ),
                # widget.Systray(
                #        background = colors[0],
                #        padding = 5
                #        ),
                widget.TextBox(
                    text = '',
                    background = colors[0],
                    foreground = colors[4],
                    padding = 0,
                    fontsize = 60
                ),
                widget.CurrentLayoutIcon(
                        custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
                        foreground = colors[0],
                        background = colors[4],
                        padding = 0,
                        scale = 0.5
                        ),
                widget.CurrentLayout(
                        foreground = colors[2],
                        background = colors[4],
                        padding = 4,
                        fontsize = 15,
                        font = "Ubuntu Mono",
                        ),
            #  widget.Net(
            #            interface = "enp3s0",
            #            foreground = colors[2],
            #            background = colors[5],
            #            padding= 6
            #            ),
            #   widget.TextBox(
            #            #text = '☛',
            #            background = colors[4],
            #            foreground = colors[5],
            #            padding = 0,
            #            fontsize = 37
                    #    ),
            # widget.BatteryIcon(
            #             background = colors[4],
            #             padding = 10
	        #             ),
            # widget.Battery(
            #             font="Noto Sans",
            #             update_interval = 10,
            #             fontsize = 12,
            #             format = "{char} {percent:2.0%}",
            #             foreground = colors[2],
            #             background = colors[4],
            #             padding = 6
	        #             ),
            # widget.Memory(
            #             #font="Noto Sans",
            #             #format = '{MemUsed}M/{MemTotal}M',
            #             update_interval = 1,
            #             fontsize = 12,
            #             foreground = colors[5],
            #             background = colors[1],
            #            ),
            # widget.Bluetooth(
            #     background = colors[5],
            #     padding = 6,
            #     hci = "hci0"
            # ),
            # widget.TextBox(
            #         text = '',
            #         background = colors[4],
            #         foreground = colors[5],
            #         padding = 0,
            #         fontsize = 37
            #         ),
            widget.TextBox(
                    text = '',
                    background = colors[4],
                    foreground = colors[5],
                    padding = 0,
                    fontsize = 60
                ),
            widget.TextBox(
                    text = "",
                    foreground = colors[2],
                    background = colors[5],
                    padding = 0,
                    mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal2 + " -e alsamixer")},
                    fontsize = 14,
                    ),
            widget.Volume(
                    foreground = colors[2],
                    background = colors[5],
                    padding = 5,
                    fontsize = 15,
                    font = "Ubuntu Mono",
                    ),
            widget.TextBox(
                    text = '',
                    background = colors[5],
                    foreground = colors[4],
                    padding = 0,
                    fontsize = 60
                ),
            widget.Clock(
                    foreground = colors[2],
                    background = colors[4],
                    format = "%A, %B %d - %H:%M ",
                    padding = 0,
                    mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn("gnome-calendar")},
                    fontsize = 15,
                    font = "Ubuntu Mono",
                    ),
            widget.TextBox(
                    text = '',
                    background = colors[4],
                    foreground = colors[5],
                    padding = 0,
                    fontsize = 60
                ),
           widget.TextBox(
                text = ' ',
                background = colors[5],
                foreground = colors[2],
                padding = 0,
                fontsize = 13,
                mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal2 + " -e systemctl suspend")},
                ),
            widget.Sep(
                foreground = colors[2],
                padding = 0,
            ),
            widget.TextBox(
                text = '  ',
                background = colors[5],
                foreground = colors[2],
                padding = 0,
                fontsize = 12,
                mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal2 + " -e poweroff")},
                ),
            widget.Sep(
                foreground = colors[2],
                padding = 0,
            ),
             widget.QuickExit(
                default_text = "  ",
                padding = 0,
                countdown_start = 5,
                fontsize = 14,
            ),
            widget.TextBox(
                text = ' ',
                background = colors[5],
                foreground = colors[2],
                padding = 0,
                ),
              ]
    return widgets_list


widgets_list = init_widgets_list()


def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1

def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    return widgets_screen2

widgets_screen1 = init_widgets_screen1()
widgets_screen2 = init_widgets_screen2()


def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), size=26, opacity=0.9)),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), size=26, opacity=0.9))]
screens = init_screens()










# screens = [
#     Screen(
#         top=bar.Bar(
#             [
#                 widget.CurrentLayout(),
#                 widget.GroupBox(),
#                 widget.Prompt(),
#                 widget.WindowName(),
#                 widget.Systray(),
#                 widget.Clock(format='%d/%m %a %I:%M %p'),
#                 widget.QuickExit(),
#             ],
#             24,
#         ),
#     ),
# ]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
    Match(title='virtualbox'),  # VirtualBox
])
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True


@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autorun.sh'])

@hook.subscribe.startup
def start_always():
    # set cursor to something sane in X
    subprocess.Popen(['xsetroot','-cursor_name','left_ptr'])

@hook.subscribe.client_new
def set_floating(window):
    if(window.window.get_wm_transient_for()
            or window.window.get_wm_type() in floating_types):
        window.floating=True

floating_types = ["notifications","toolbar","splash","dialog"]



# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
