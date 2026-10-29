from common import *
from fig_reactive import winding, tr_core
from fig_amps import stage, YT, XB, YB, XR, KC_Y


def h01():
    with drawing('h01_varicond') as d:
        d += (L := elm.Inductor2().down(4).at((0, 4)).label('L', loc='top'))
        d += elm.Line().right(2).at((0, 4))
        d += (n := elm.Dot())
        d += elm.Capacitor().down(2).label('$C_1$', loc='top')
        d += (m := elm.Dot())
        d += elm.CapacitorVar().down(2).label('$C_2$ (вариконд)', loc='top').color(PINK)
        d += elm.Line().left().tox(0)
        d += elm.Resistor().right(3).at(m.center).label('$R_д$ (большой)', loc='bottom').color(BLUE)
        d += elm.Line(arrow='->').right(1.2)
        xp = d.here[0] + 0.45
        d += (P := elm.Potentiometer().down(4).at((xp, 4.0)).flip())
        txt(d, (xp - 0.9, 3.4), '$R_р$', halign='right')
        d += elm.Line().at((xp, 4.0)).to((xp + 2.2, 4.0))
        E = elm.Battery().down(4).reverse().label('E', loc='bottom')
        d += E
        txt(d, (xp + 1.7, 3.4), '+'); txt(d, (xp + 1.7, 0.6), '−')
        d += elm.Line().at((xp + 2.2, 0)).to((0, 0))


def h02():
    with drawing('h02_detector_radio') as d:
        d += elm.Antenna().at((2, 4))
        d += (L := elm.Inductor2().down(3.5).at((0, 4)).label('$L_к$', loc='top'))
        d += elm.Line().right(2).at((0, 4))
        d += (n := elm.Dot())
        d += elm.CapacitorVar().down(3.5).label('$C_к$', loc='bottom')
        d += (g := elm.Dot())
        d += elm.Ground()
        d += elm.Line().left().at(g.center).tox(0)
        d += elm.Diode().right(3).at(n.center).label('VD1').color(PINK)
        d += (k := elm.Dot())
        d += elm.Capacitor().down(3.5).label('$C_1$', loc='bottom').color(BLUE)
        d += elm.Line().left().tox(g.center[0])
        d += elm.Line().right(2).at(k.center)
        d += (ph := elm.Resistor().down(3.5).label('ТЛФ1\n(наушники)', loc='bottom'))
        d += elm.Line().left().tox(k.center[0])


def h03():
    with drawing('h03_receiver_urch') as d:
        d += elm.Antenna().at((2, 4))
        d += elm.Inductor2().down(3.5).at((0, 4)).label('$L_к$', loc='top')
        d += elm.Line().right(2).at((0, 4))
        d += (n := elm.Dot())
        d += elm.CapacitorVar().down(3.5).label('$C_к$', loc='bottom')
        d += (g := elm.Dot())
        d += elm.Ground()
        d += elm.Line().left().at(g.center).tox(0)
        d += elm.Line().right(5.5).at(n.center)
        d += elm.Line().down(0.5)
        d += flow.Box(w=2.6, h=2.5).anchor('N').label('УРЧ /\nВЧТРП')
        d += elm.Line().at((g.center[0], 0)).to((g.center[0] + 5.5, 0))
        d += elm.Line().up(0.5)


def h04():
    with drawing('h04_timer') as d:
        I = src(d, '$I_0$', kind='i', length=4)
        d += elm.Line().right(2)
        d += (n := elm.Dot())
        d += elm.Switch().down(4).label('Кл1', loc='top')
        d += (g := elm.Dot())
        d += elm.Line().left().tox(0)
        d += elm.Line().right(2).at(n.center)
        d += (m := elm.Dot())
        d += elm.Capacitor().down(4).label('$C_1$', loc='bottom')
        d += elm.Line().left().tox(g.center[0])
        d += elm.Line().right(2.0).at(m.center)
        x0 = m.center[0] + 2.0
        d += (K := flow.Box(w=2.6, h=2.6).at((x0, 4.6)).anchor('NW').label('K'))
        d += elm.Line().at((m.center[0], 0)).to((x0 + 1.3, 0))
        d += (Uo := elm.Battery().up().at((x0 + 1.3, 0)).toy(2.0).reverse().label('$U_{оп}$', loc='bottom'))
        d += elm.Arrow().right(2.5).at(K.E).label('выход', loc='top')
        txt(d, (x0 + 1.3, 5.2), 'компаратор', color=BLUE)


def h05():
    with drawing('h05_generator') as d:
        d += elm.Line().at((0, 0)).to((2, 0))
        d += elm.Dot().at((2, 0))
        d += elm.Arrow().at((2, 0)).to((3, 0))
        d += flow.Box(w=2.4, h=1.4).at((3, 0)).anchor('W').label('K\n(усилитель)')
        d += elm.Line().at((5.4, 0)).to((7, 0))
        d += elm.Dot().at((7, 0))
        d += elm.Arrow().at((7, 0)).to((8.6, 0)).label('$U_{вых}$', loc='top')
        d += elm.Line().at((7, 0)).to((7, 2.6))
        d += elm.Arrow().at((7, 2.6)).to((6.2, 2.6))
        d += flow.Box(w=3.4, h=1.2).at((6.2, 2.6)).anchor('E').label('ЧЗПОС (R, C)')
        d += elm.Line().at((2.8, 2.6)).to((2, 2.6))
        d += elm.Arrow().at((2, 2.6)).to((2, 0.1))
        txt(d, (1.8, 1.4), '$U_{ос}=\\beta U_{вых}$', halign='right', color=PINK)


def h06():
    """Линейный источник питания: трансформатор → выпрямитель → C_ф → стабилизатор → нагрузка."""
    with drawing('h06_linear_psu') as d:
        d += (a := elm.Dot(open=True).label('~220 В', loc='left'))
        d += elm.Line().right(1)
        winding(d, 1, 0, length=3, flip=True)
        d += elm.Line().at((1, -3)).to((0, -3))
        d += elm.Dot(open=True)
        tr_core(d, 1.65, 0.3, -3.3)
        winding(d, 2.3, 0, length=3)
        d += elm.Line().at((2.3, 0)).to((2.8, 0))
        d += elm.Diode().right().label('VD1')
        d += (n := elm.Dot())
        d += elm.Capacitor2().down(3).label('$C_ф$', loc='top').color(BLUE)
        d += (g := elm.Dot())
        d += elm.Line().left().tox(2.3)
        d += elm.Resistor().right(3).at(n.center).label('$R_б$').color(PINK)
        d += (s := elm.Dot())
        d += elm.Zener().up().at((s.center[0], -3)).to(s.center).label('VD2', loc='top').color(PINK)
        d += elm.Line().right(2.2).at(s.center)
        d += elm.Resistor().down(3).label('$R_н$', loc='bottom')
        d += elm.Line().left().tox(g.center[0])
        txt(d, (1.65, -4.1), 'трансформатор', color=BLUE)
        txt(d, (4.3, 1.5), 'выпрямитель', color=BLUE)
        txt(d, (5.8, -4.1), 'фильтр', color=BLUE)
        txt(d, (9.6, 1.5), 'стабилизатор', color=PINK)


if __name__ == '__main__':
    for f in (h01, h02, h03, h04, h05, h06):
        try:
            f()
        except Exception as ex:
            import traceback; traceback.print_exc()
