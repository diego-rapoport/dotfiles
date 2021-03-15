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

import sh, subprocess, time, os, random, json, re

# FUNÇÔES
def get_colors():
    with open('/home/dinhego/.cache/wal/colors.json') as f:
        colors = json.load(f)
    #colors['special']['background']
    bg = colors['special']['background']
    fg = colors['special']['foreground']
    cursor = colors['special']['cursor']
    color1 = colors['colors']['color1']
    color2 = colors['colors']['color2']
    color3 = colors['colors']['color3']
    color4 = colors['colors']['color4']
    color5 = colors['colors']['color5']
    color6 = colors['colors']['color6']
    color7 = colors['colors']['color7']
    color8 = colors['colors']['color8']

    return bg, fg, cursor, color1, color2, color3, color4, color5, color6, color7, color8

def num_monitors():
    return int(sh.head(sh.xrandr('--listmonitors'), '-1').stdout.decode('utf-8')[-2])

def playerctl():
    players = ['ncspot', 'cmus', 'mpv']
    args = ['playerctl', f'--player={", ".join(players)}', 'metadata', '--format', '{{ status }}: {{ artist }} - {{ title }}']
    text = subprocess.run(args, capture_output=True, encoding='utf-8').stdout[:-1]
    limit = len(text) - text.find('-')
    dash = text.find('-')
    if dash > 40:
        front = text[:35]+'...'
    else:
        front = text[:dash]
    if limit > 40:
        rear = text[dash:dash+27]+'...'
    else:
        rear = text[dash:]
    data = front+rear
    d = dict(Playing = '', Paused = '')
    try:
        return [re.sub('\w+:', d[chave], data) for chave in d.keys() if chave in data][0]
    except:
        if 'Stopped' in data:
            return ''
        else:
            return ''

# VARIÁVEIS DE CORES
bg, fg, cursor, color1, color2, color3, color4, color5, color6, color7, color8 = get_colors()

mod = "mod4"
ctrl = 'control'
alt = 'mod1'
shift = 'shift'
terminal = guess_terminal() # default qtile

keys = [

# MOVIMENTO DAS TELAS
    Key([alt], 'h', lazy.spawn('qtile cmd-obj -o cmd -f next_screen')),
    Key([alt], 'l', lazy.spawn('qtile cmd-obj -o cmd -f previous_screen')),

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
    Key([mod, ctrl], "h", lazy.layout.grow_left(),
        desc="Aumenta a janela pra esquerda"),
    Key([mod, ctrl], "l", lazy.layout.grow_right(),
        desc="Aumenta a janela pra direita"),
    Key([mod, ctrl], "j", lazy.layout.grow_down(),
        desc="Aumenta a janela pra baixo"),
    Key([mod, ctrl], "k", lazy.layout.grow_up(), desc="Aumenta a janela pra cima"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reseta o tamanho de todas as janelas"),

# QTILE GERAL
    Key([mod], "Tab", lazy.next_layout(), desc='Troca tipo de layout'),
    Key([mod, ctrl], "w", lazy.window.kill(), desc='Fecha a janela focada'),
    Key([mod, ctrl], "r", lazy.restart(), desc="Restart qtile"),
    Key([mod, ctrl], "q", lazy.shutdown(), desc='Fecha o Qtile'),
    Key([alt], "p", lazy.spawncmd(), desc='Abre o widget Prompt pra executar comando'),

# TECLAS DE AUDIO
    Key([], 'XF86AudioPlay', lazy.spawn('playerctl play-pause'), desc='Play ou Pause'),
    Key([], 'XF86AudioNext', lazy.spawn('playerctl next'), desc='Próxima faixa'),
    Key([], 'XF86AudioPrev', lazy.spawn('playerctl previous'), desc='Faixa anterior'),
    Key([], 'XF86AudioRaiseVolume', lazy.spawn('amixer -c 0 -q set Master 2dB+'), desc='Aumenta o volume'),
    Key([], 'XF86AudioLowerVolume', lazy.spawn('amixer -c 0 -q set Master 2dB-'), desc='Diminui o volume'),
    Key([], 'XF86AudioMute', lazy.spawn('pulsemixer --toggle-mute'), desc='Muta/Desmuta o volume'),

# TECLAS DE BRILHO
    Key([], 'XF86MonBrightnessUp', lazy.spawn('xbacklight -inc 5'), desc='Aumenta o brilho da tela'),
    Key([], 'XF86MonBrightnessDown', lazy.spawn('xbacklight -dec 5'), desc='Diminui o bilho da tela'),

# PROGRAMAS
    Key([mod], "Return", lazy.spawn(terminal), desc='Abre o terminal'),
    Key([mod], 'a', lazy.spawn('alacritty --class Ranger,Ranger -e env COLUMNS= LINES= ranger'), desc='Abre o gerenciador de arquivos Ranger'),
    Key([mod], 'c', lazy.spawn('calibre'), desc='Abre o calibre'),
    Key([mod], 'd', lazy.spawn('discord'), desc='Abre o Discord'),
    Key([mod], 'e', lazy.spawn('alacritty --class Mail,Mail --title Neomutt -e neomutt'), desc='Abre o email em CLI'),
    Key([mod], 'f', lazy.spawn('firefox'), desc='Abre o Firefox'),
    Key([mod, ctrl], 'l', lazy.spawn('lutris'), desc='Abre o Lutris'),
    Key([mod], 'm', lazy.spawn('musescore'), desc='Abre o Musescore'),
    Key([mod], 'n', lazy.spawn('alacritty --class Newsboat,Newsboat --title "RSS Newsboat" -e newsboat'), desc='Abre o leitor de RSS Newsboat'),
    Key([mod], 'p', lazy.spawn('alacritty --class MusicPlayer,MusicPlayer --title Cmus -e cmus'), desc='Abre o player de música cmus'),
    Key([mod], 'q', lazy.spawn('qutebrowser'), desc='Abre o navegador qutebrowser'),
    Key([mod], 'r', lazy.spawn('alacritty --class TTRV,TTRV --title "Reddit ttrv" -e ttrv --enable-media'), desc='Abre o Reddit em CLI'),
    Key([mod], 's', lazy.spawn('alacritty --class Spotify,Spotify --title Spotify -e ncspot'), desc='Abre o Spotify em CLI'),
    Key([mod], 't', lazy.spawn('alacritty --class telegram,telegram --title "Telegram CLI" -e tg'), desc='Abre o Telegram em CLI'),
    Key([], 'XF86Search', lazy.spawn('rofi -show drun'), desc='Abre o menu do rofi'),
    Key([shift], 'Print', lazy.spawn('scrot -s /home/dinhego/Imagens/Print/%d-%m-%Y-%Hh%Mmin%S.jpg'), desc='Tira print da área selecionada'),
    Key([], 'Print', lazy.spawn('scrot /home/dinhego/Imagens/Print/%d-%m-%Y-%Hh%Mmin.png'), desc='Tira print de todo o desktop'),
]

# Categorias dos grupos
web = [Match(wm_class='firefox'), Match(wm_class='qutebrowser')]
terminal = [Match(wm_class='Alacritty'), Match(wm_class='fim')]
office = [Match(wm_class='Io.elementary.files'), Match(wm_class='Mail'), Match(wm_class='Ranger')]
social = [Match(wm_class='telegram'), Match(wm_class='discord'), Match(wm_class='TelegramDesktop')]
musica = [Match(wm_class='Spotify'), Match(wm_class='MuseScore3'), Match(wm_class='MusicPlayer')]
jogos = [Match(wm_class='lutris'), Match(wm_class='epicgameslauncher.exe'), Match(wm_class='modlauncher.exe'), Match(wm_class='torchlight2.exe')]
leitura = [Match(wm_class='Zathura'), Match(wm_class='TTRV'), Match(wm_class='calibre'), Match(wm_class='Newsboat')]
video = [Match(wm_class='mpv')]

groups = [
    Group('1', label='爵', matches=[*web], exclusive=True, layout='max'),
    Group('2', label='', matches=[*terminal], exclusive=True, layout='monadtall'),
    Group('3', label='', matches=[*office], layout='monadtall'),
    Group('4', label='', matches=[*social], exclusive=True, layout='monadtall'),
    Group('5', label='龎', matches=[*leitura], exclusive=True, layout='max'),
    Group('6', label='', matches=[*musica], exclusive=True, layout='monadwide'),
    Group('7', label='', matches=[*jogos], exclusive=True, layout='max'),
    Group('8', label='辶', matches=[*video], exclusive=True, layout='max'),
    Group('9', label='')
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
    border_focus = color7,
    border_normal = bg,
    margin = 1,
    border_width = 3
)

layouts = [
    layout.Max(),
    #layout.Stack(num_stacks=2),
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
    font = 'Arimo Nerd Font',
    fontsize = 16,
    fontshadow = '#121212',
    padding = 2,
)
extension_defaults = widget_defaults.copy()

sep_defaults = dict(
    foreground = cursor,
    padding = 1,
    size_percent = 70,
    linewidth = 2
)

tasklist_defaults = dict(
        border = color1,
        borderwidth = 0,
        highlight_method = 'block',
        margin = 2,
        markup_focused = '<b>{}</b>',
        markup_normal = '<span alpha="25%">{}</span>',
        padding = 2,
        title_width_method = 'uniform',
        txt_minimized = '🗕',
        unfocused_border = color8
)

groupbox_defaults = dict(
        highlight_method = 'block',
        highlight_color = color3,
        inactive = color6,
        this_current_screen_border = color3,
        this_screen_border = fg,
        other_current_screen_border = color3,
        other_screen_border = fg,
        fontshadow = bg,
        fontsize = 22,
        disable_drag = True,
)

#### CALLBACKS ####

# DMENU NETWORK MANAGER
def net_opts(qtile):
    qtile.cmd_spawn('networkmanager_dmenu')

# PLAYERCTL
def play_pause(qtile):
    sh.playerctl('play-pause')

def stop(qtile):
    sh.playerctl('stop')

def next(qtile):
    sh.playerctl('next')

def previous(qtile):
    sh.playerctl('previous')

# SCREENS
if num_monitors() >= 2:
    screens = [
        Screen(
            top=bar.Bar(
                [
                    widget.CurrentLayoutIcon(scale=0.70),
                    widget.GroupBox(**groupbox_defaults),
                    widget.Prompt(prompt=' '),
                    widget.Sep(**sep_defaults),
                    widget.TaskList(**tasklist_defaults),
                    widget.Chord(
                        chords_colors={
                            'launch': ("#ff0000", "#ffffff"),
                        },
                        name_transform=lambda name: name.upper(),
                    ),
                    widget.Sep(**sep_defaults),
                    widget.KhalCalendar(longdateformat='%d/%m/%Y', remindertime=60),
                    widget.Sep(**sep_defaults),
                    widget.Volume(emoji=True, fontshadow=None, fontsize=22),
                    widget.GenPollText(func=playerctl, update_interval=1, mouse_callbacks={'Button1': play_pause, 'Button3': stop, 'Button4': next, 'Button5': previous}),
                    widget.Sep(**sep_defaults),
                    widget.Clock(format=f' %A | %d/%m/%Y | %H:%M '),
                    widget.Sep(**sep_defaults),
                    widget.QuickExit(default_text=' ', countdown_format='{} segundos'),
                ], 25, margin=[3,5,2,5], background=[color1, color2]
            ),
        ),
        Screen(
            bottom=bar.Bar(
                [
                    widget.CurrentLayoutIcon(scale=0.70),
                    widget.Sep(**sep_defaults),
                    widget.Systray(),
                    widget.Sep(**sep_defaults),
                    widget.TaskList(**tasklist_defaults),
                    widget.Sep(**sep_defaults),
                    widget.TextBox('', fontsize=18),
                    widget.CheckUpdates(
                        distro='Arch_checkupdates',
                        display_format='{updates}',
                        update_interval=180,
                        no_update_string='0'
                    ),
                    widget.ThermalSensor(fmt='{}'),
                    widget.TextBox(''),
                    widget.CPUGraph(type='box'),
                    widget.TextBox(''),
                    widget.NetGraph(mouse_callbacks={'Button1': net_opts}),
                ], 23, margin=[2,5,3,5], background=[color2, color1]
            ),
        ),
    ]
else:
    screens = [
        Screen(
            top=bar.Bar(
                [
                    widget.CurrentLayoutIcon(scale=0.70),
                    widget.GroupBox(**groupbox_defaults),
                    widget.Prompt(prompt=' '),
                    widget.Sep(**sep_defaults),
                    widget.TaskList(**tasklist_defaults),
                    widget.Chord(
                        chords_colors={
                            'launch': ("#ff0000", "#ffffff"),
                        },
                        name_transform=lambda name: name.upper(),
                    ),
                    widget.Sep(**sep_defaults),
                    widget.KhalCalendar(longdateformat='%d/%m/%Y', remindertime=60),
                    widget.Sep(**sep_defaults),
                    widget.Volume(emoji=True, fontshadow=None, fontsize=22),
                    widget.GenPollText(func=playerctl, update_interval=1, mouse_callbacks={'Button1': play_pause, 'Button3': stop, 'Button4': next, 'Button5': previous}),
                    widget.Sep(**sep_defaults),
                    widget.Clock(format=f' %A | %d/%m/%Y | %H:%M '),
                    widget.Sep(**sep_defaults),
                    widget.QuickExit(default_text=' ', countdown_format='{} segundos'),
                ], 25, margin=[3,5,2,5], background=[color1, color2]
            ),
            bottom=bar.Bar(
                [
                    widget.CurrentLayoutIcon(scale=0.70),
                    widget.Sep(**sep_defaults),
                    widget.Systray(),
                    widget.Sep(**sep_defaults),
                    widget.TaskList(**tasklist_defaults),
                    widget.Sep(**sep_defaults),
                    widget.TextBox('', fontsize=18),
                    widget.CheckUpdates(
                        distro='Arch_checkupdates',
                        display_format='{updates}',
                        update_interval=180,
                        no_update_string='0'
                    ),
                    widget.ThermalSensor(fmt='{}'),
                    widget.TextBox(''),
                    widget.CPUGraph(type='box'),
                    widget.TextBox(''),
                    widget.NetGraph(mouse_callbacks={'Button1': net_opts}),
                ], 23, margin=[2,5,3,5], background=[color2, color1]
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
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
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
    Match(wm_class='save'),
    Match(wm_class='albert'),
    Match(wm_class='xscreensaver-demo'),
    Match(wm_class='kwalletd5'),
    Match(wm_class='yad'),
    Match(wm_class='grc-prompter'),
    Match(wm_class='ffplay'),
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
    Match(title='pinentry-gtk-2'),
])
auto_fullscreen = True
focus_on_window_activation = "smart"

wmname = "Qtile"

@hook.subscribe.startup_once
def autostart():
    sh.xrandr('--output', 'HDMI-1', '--primary', '--right-of', 'eDP-1')

@hook.subscribe.startup_complete
def completado():
    sh.autostart()
