"""Общие настройки для генерации схем (schemdraw) и графиков (matplotlib)."""
import os
import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['font.family'] = 'DejaVu Sans'
import schemdraw
import schemdraw.elements as elm
import schemdraw.flow as flow
import schemdraw.dsp as dsp

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'img')
os.makedirs(OUT, exist_ok=True)

elm.style(elm.STYLE_IEC)          # резисторы прямоугольниками, как на слайдах
schemdraw.config(fontsize=13, inches_per_unit=0.45, lw=1.6)

PINK = '#c2185b'   # цвет подписей напряжений/токов (как маркер на слайдах)
BLUE = '#1565c0'


def path(name):
    return os.path.join(OUT, name + '.png')


def drawing(name):
    """with drawing('c01') as d: ...  -> сохраняет img/c01.png"""
    d = schemdraw.Drawing(show=False, dpi=120)
    d._fname = path(name)
    return _Ctx(d)


class _Ctx:
    def __init__(self, d):
        self.d = d

    def __enter__(self):
        return self.d

    def __exit__(self, *a):
        if a[0] is None:
            self.d.save(self.d._fname, dpi=120)
            print('saved', os.path.basename(self.d._fname))
        return False


def battery_up(d, label, at=None, plus_top=True):
    """Источник постоянного напряжения снизу вверх; подпись слева, полярность явно."""
    b = elm.Battery().up()
    if at is not None:
        b = b.at(at)
    if plus_top:
        b = b.reverse()
        b = b.label(['−', label, '+'], loc='left')
    else:
        b = b.label(['+', label, '−'], loc='left')
    d += b
    return b


def src(d, name, at=None, length=3, plus_top=True, kind='dc'):
    """Источник снизу вверх. kind: 'dc' (батарея), 'ac' (синусоидальный ~), 'i' (источник тока)."""
    if kind == 'dc':
        e = elm.Battery().up(length)
        if plus_top:
            e = e.reverse()
    elif kind == 'ac':
        e = elm.SourceSin().up(length)
    elif kind == 'pulse':
        e = elm.SourceSquare().up(length)
    else:
        e = elm.SourceI().up(length)
    if at is not None:
        e = e.at(at)
    e = e.label(name, loc='top', ofst=0.35)
    d += e
    if kind == 'dc':
        top, bot = ('+', '−') if plus_top else ('−', '+')
        x = e.start[0] + 0.45
        mid = (e.start[1] + e.end[1]) / 2
        d += elm.Label().at((x, mid + 0.75)).label(top, fontsize=12)
        d += elm.Label().at((x, mid - 0.75)).label(bot, fontsize=12)
    return e


def vmark(d, top, bot, text, dx=0.0, side='right', color=PINK):
    """Розовая двусторонняя стрелка напряжения между точками top и bot (смещена на dx) + подпись."""
    x = top[0] + dx
    d += elm.Line(arrow='<->').at((x, top[1] - 0.15)).to((x, bot[1] + 0.15)).color(color).linewidth(1.2)
    y = (top[1] + bot[1]) / 2
    off = 0.25 if side == 'right' else -0.25
    d += elm.Label().at((x + off, y)).label(text, color=color, halign='left' if side == 'right' else 'right')


def hmark(d, left, right, text, dy=0.0, color=PINK, below=True):
    y = left[1] + dy
    d += elm.Line(arrow='<->').at((left[0] + 0.15, y)).to((right[0] - 0.15, y)).color(color).linewidth(1.2)
    d += elm.Label().at(((left[0] + right[0]) / 2, y + (-0.35 if below else 0.35))).label(text, color=color)


def cur(d, wire, text, direction='in', color=PINK, loc='top'):
    """Стрелка тока на проводнике wire (элемент Line)."""
    import math
    L = math.dist(tuple(wire.start), tuple(wire.end))
    d += elm.CurrentLabelInline(direction=direction, ofst=-0.15).at(wire).label(text, color=color, loc=loc).color(color)


def txt(d, xy, text, color='black', **kw):
    d += elm.Label().at(xy).label(text, color=color, **kw)
