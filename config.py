#
#██████╗ ██╗███╗   ██╗██╗  ██╗███████╗ ██████╗  ██████╗
#██╔══██╗██║████╗  ██║██║  ██║██╔════╝██╔════╝ ██╔═══██╗
#██║  ██║██║██╔██╗ ██║███████║█████╗  ██║  ███╗██║   ██║
#██║  ██║██║██║╚██╗██║██╔══██║██╔══╝  ██║   ██║██║   ██║
#██████╔╝██║██║ ╚████║██║  ██║███████╗╚██████╔╝╚██████╔╝
#╚═════╝ ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝ ╚═════╝  ╚═════╝
#


from typing import List  # noqa: F401

from libqtile import bar, layout, widget, hook, qtile
from libqtile.config import Click, Drag, Group, Key, Screen, Match
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

import sh, subprocess, time, os, random

from PegaPaleta import wpp, bg, borda, scrativa, scrinativa, fginativo

mod = "mod4"
ctrl = 'control'
alt = 'mod1'
shift = 'shift'
terminal = guess_terminal() # default qtile

keys = [

    # MOVIMENTO DAS TELAS
    Key([alt], 'h', lazy.spawn('qtile-cmd -o cmd -f next_screen')),
    Key([alt], 'l', lazy.spawn('qtile-cmd -o cmd -f previous_screen')),

	# FOCUS DA JANELA
    Key([mod], "j", lazy.layout.down(), desc='Foco na janela de baixo'),
    Key([mod], "k", lazy.layout.up(), desc='Foco na janela de cima'),
    Key([mod], 'h', lazy.layout.left(), desc='Foco na janela da esquerda'),
    Key([mod], 'l', lazy.layout.right(), desc='Foco na janela da direita'),
	Key([mod], "space", lazy.layout.next(), desc='Foco na próxima janela'),

	# MOVIMENTO DA JANELA FOCADA
    Key([mod, shift], "j", lazy.layout.shuffle_down(), desc='Move a janela pra baixo'),
    Key([mod, shift], "k", lazy.layout.shuffle_up(), desc='Move a janela pra cima'),
    Key([mod, shift], 'h', lazy.layout.swap_left(), desc='Move a janela pra esquerda'),
    Key([mod, shift], 'l', lazy.layout.swap_right(), desc='Move a janela pra direita'),
	Key([mod, shift], "space", lazy.layout.rotate(), desc='Move a janela para a próxima na sequência'),

	# TAMANHO DA JANELA
	Key([mod], 'equal', lazy.layout.grow(), desc='Aumenta o tamanho da janela'),
    Key([mod], 'minus', lazy.layout.shrink(), desc='Diminui o tamanho da janela'),
    Key([mod, shift], "Return", lazy.layout.toggle_split(), desc='Muda entre janelas separadas ou maximizadas'),

	# QTILE GERAL
    Key([mod], "Tab", lazy.next_layout(), desc='Troca tipo de layout'),
    Key([mod, ctrl], "w", lazy.window.kill(), desc='Fecha a janela focada'),
    Key([mod, "control"], "r", lazy.restart(), desc="Restart qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc='Fecha o Qtile'),
    Key([mod], "r", lazy.spawncmd(), desc='Abre o widget Prompt pra executar comando'),

	# TECLAS DE AUDIO
    Key([], 'XF86AudioPlay', lazy.spawn('playerctl play-pause'), desc='Play ou Pause'),
    Key([], 'XF86AudioNext', lazy.spawn('playerctl next'), desc='Próxima faixa'),
    Key([], 'XF86AudioPrev', lazy.spawn('playerctl previous'), desc='Faixa anterior'),
    Key([], 'XF86AudioRaiseVolume', lazy.spawn('amixer -c 0 -q set Master 2dB+'), desc='Aumenta o volume'),
    Key([], 'XF86AudioLowerVolume', lazy.spawn('amixer -c 0 -q set Master 2dB-'), desc='Diminui o volume'),
    Key([], 'XF86AudioMute', lazy.spawn('pulsemixer --toggle-mute'), desc='Muta/Desmuta o volume'),

	# PROGRAMAS
	Key([mod], "Return", lazy.spawn(terminal), desc='Abre o terminal'),
	Key([mod], 'e', lazy.spawn('io.elementary.files'), desc='Abre a pasta de arquivos'),
    Key([mod], 'f', lazy.spawn('firefox'), desc='Abre o Firefox'),
    Key([mod], 'g', lazy.spawn('google-chrome-stable'), desc='Abre o Google Chrome'),
    Key([mod], 't', lazy.spawn('telegram-desktop'), desc='Abre o Telegram'),
    Key([mod], 'a', lazy.spawn('atom'), desc='Abre o Atom'),
    Key([mod], 'i', lazy.spawn('python3 -m idlelib.idle'), desc='Abre o console idle do Python3'),
    Key([mod], 's', lazy.spawn('flatpak run com.spotify.Client'), desc='Abre o Spotify'),
    Key([mod], 'm', lazy.spawn('musescore'), desc='Abre o Musescore'),
    Key([mod], 'w', lazy.spawn('steam'), desc='Abre a Steam jogos'),
    Key([], 'XF86Search', lazy.spawn('rofi -show drun'), desc='Abre o menu do rofi'),
    Key([shift], 'Print', lazy.spawn('escrotum -s /home/dinhego/Imagens/Print/%d-%m-%Y-%Hh%Mmin.png'), desc='Tira print da área selecionada'),
]

web = Match(wm_class=['firefox', 'chrome', 'google-chrome'])
terminal = Match(wm_class=['Alacritty', 'terminal', 'shell', 'bash', 'terminator'])
arq = Match(wm_class=['nautilus', 'files', 'gedit', 'Io.elementary.files'])
social = Match(wm_class=['whatsapp', 'Gtkwhats', 'telegram', 'TelegramDesktop', 'Discord', 'discord'])
python = Match(wm_class=['python', 'Python', 'atom', 'ipython', 'py', 'Designer', 'Qt', 'idle', 'Toplevel'])
musica = Match(wm_class=['spotify', 'Spotify', 'MuseScore3', 'musescore'], title=['Spotify Premium'])
steam = Match(wm_class=['Steam', 'WAKFU', 'game', 'steam'], title=['Steam', 'steam'])

groups = [
	Group('1', label='🌐:1', matches=[web], exclusive=True, layout='max'),
	Group('2', label='🐚:2', matches=[terminal], exclusive=True, layout='monadtall'),
	Group('3', label='📂:3', matches=[arq], layout='monadwide'),
	Group('4', label='🤳:4', matches=[social], exclusive=True, layout='monadtall'),
	Group('5', label='🐍:5', matches=[python], exclusive=True, layout='max'),
	Group('6', label='📻:6', matches=[musica], exclusive=True, layout='max'),
	Group('7', label='👾:7', matches=[steam], exclusive=True, layout='max'),
	Group('8', label='🌌:8')
]

for i in groups:
    keys.extend([
        # mod4 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name)),

        # mod4 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(i.name)),
    ])

layout_config = dict(
    border_focus = borda,
    margin = 1,
    border_width = 3
)

layouts = [
    layout.Max(),
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Columns(),
    layout.Matrix(columns=3, **layout_config),
    layout.MonadTall(**layout_config),
    layout.MonadWide(**layout_config),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font='Cantarell Bold',
    fontsize=15,
    padding=2,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayoutIcon(scale=0.70),
                widget.GroupBox(
                    highlight_method = 'block',
                    highlight_color=bg,
                    inactive = fginativo,
                    this_current_screen_border = scrativa,
                    this_screen_border = scrinativa,
                    other_current_screen_border = scrativa,
                    other_screen_border = scrinativa,
                    font_shadow='e9e9e9',
                    disable_drag=True,
                ),
                widget.Prompt(prompt='Executar: '),
                widget.WindowName(fmt='❝{}❞', for_current_screen=True),
                widget.Chord(
                    chords_colors={
                        'launch': ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.Volume(emoji=True),
                widget.Sep(foreground=fginativo, padding=1, size_percent=100, linewidth=3),
                widget.Clock(format='%a %d/%m/%Y %H:%M'),
                widget.Sep(foreground=fginativo, padding=1, size_percent=100, linewidth=3),
                widget.QuickExit(default_text='DESLIGAR', countdown_format='{} segundos'),
            ], 25, margin=[3,5,2,5], background=bg
        ), wallpaper=wpp, wallpaper_mode='fill'
    ),
    Screen(
    	bottom=bar.Bar(
    		[
    			widget.CPU(),
    			widget.CurrentLayoutIcon(scale=0.70),
    			widget.Spacer(length=bar.STRETCH),
    			widget.Systray(),
                widget.CheckUpdates(
                    display_format='Atualizações:{updates}',
                	update_interval=180
                ),
    			widget.ThermalSensor(fmt='🌡️CPU:{}'),
    			widget.TextBox('📡'),
    			widget.NetGraph(),
    		], 23, margin=[2,5,3,5], background=bg[::-1]
    	), wallpaper=wpp, wallpaper_mode='fill'
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
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
    {'wmclass': 'save'},
    {'wmclass': 'xmessage'},
])
auto_fullscreen = True
focus_on_window_activation = "smart"

# For java UI toolkits
wmname = "LG3D"

@hook.subscribe.startup_once
def autostart():
	sh.xrandr('--output', 'HDMI-1', '--primary', '--right-of', 'eDP-1')

@hook.subscribe.startup_complete
def completado():
	sh.autostart()
