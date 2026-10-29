from common import *


def c01_ohm():
    with drawing('c01_ohm') as d:
        E = src(d, '$E$')
        d += (w := elm.Line().right(2.5))
        d += (R := elm.Resistor().down().label('R', loc='bottom'))
        d += elm.Line().left().tox(E.start)
        cur(d, w, 'I')
        vmark(d, R.start, R.end, '$U$', dx=1.0)


def c02_series():
    with drawing('c02_series') as d:
        d += (A := elm.Dot(open=True).label('A', loc='left'))
        d += (R1 := elm.Resistor().right().label('R1').label(['+', '', '−'], loc='bottom', color=PINK))
        d += (w := elm.Line().right(1.2))
        d += (R2 := elm.Resistor().right().label('R2').label(['+', '', '−'], loc='bottom', color=PINK))
        d += (B := elm.Dot(open=True).label('B', loc='right'))
        cur(d, w, 'I')
        hmark(d, R1.start, R1.end, '$U_1$', dy=-1.0)
        hmark(d, R2.start, R2.end, '$U_2$', dy=-1.0)
        hmark(d, A.center, B.center, '$U_{AB}=U_1+U_2$', dy=-2.2)


def c03_key_logic():
    with drawing('c03_key') as d:
        d += elm.Vdd().label('$+U_п$')
        d += (R1 := elm.Resistor().down().label('R1', loc='bottom'))
        d += (n := elm.Dot())
        d += (K := elm.Switch().down().label('Кл1', loc='bottom'))
        d += (g := elm.Dot())
        d += elm.Ground()
        d += elm.Line().right(3).at(n.center)
        d += (o1 := elm.Dot(open=True))
        d += elm.Line().right(3).at(g.center)
        d += (o2 := elm.Dot(open=True))
        vmark(d, R1.start, R1.end, '$U_1$', dx=0.9)
        vmark(d, o1.center, o2.center, '$U_{вых}$', dx=0.4)


def c04_divider():
    with drawing('c04_divider') as d:
        E = src(d, '$E_п$', length=6)
        d += (w := elm.Line().right(2.5))
        d += (R1 := elm.Resistor().down().label('R1', loc='bottom'))
        d += (n := elm.Dot())
        d += (R2 := elm.Resistor().down().label('R2', loc='bottom'))
        d += (g := elm.Dot())
        d += elm.Line().left().tox(E.start)
        d += elm.Line().right(3).at(n.center)
        d += (o1 := elm.Dot(open=True))
        d += elm.Line().right(3).at(g.center)
        d += (o2 := elm.Dot(open=True))
        cur(d, w, 'I')
        vmark(d, R1.start, R1.end, '$U_1$', dx=0.9)
        vmark(d, R2.start, R2.end, '$U_2$', dx=0.9)
        vmark(d, o1.center, o2.center, '$U_{вых}=U_2$', dx=0.4)


def c05_mixed():
    with drawing('c05_mixed') as d:
        E = src(d, '$E_п$')
        d += (w1 := elm.Line().right(1))
        d += (R1 := elm.Resistor().right().label('R1'))
        d += (n := elm.Dot())
        d += (R2 := elm.Resistor().down().label('R2', loc='bottom'))
        d += (m := elm.Dot())
        d += elm.Line().left().tox(E.start)
        d += (w3 := elm.Line().right(3).at(n.center))
        d += (R3 := elm.Resistor().down().label('R3', loc='bottom'))
        d += elm.Line().left().tox(m.center)
        cur(d, w1, '$I_1$')
        cur(d, w3, '$I_3$')
        txt(d, (n.center[0] + 0.5, n.center[1] - 0.6), '$I_2\\downarrow$', color=PINK)
        hmark(d, R1.start, R1.end, '$U_1$', dy=0.9, below=False)
        vmark(d, R3.start, R3.end, '$U_{23}$', dx=1.0)


def c06_kirchhoff():
    for name, aiding in (('c06a_kirch_plus', True), ('c06b_kirch_minus', False)):
        with drawing(name) as d:
            E2 = src(d, '$E_2$', length=3)
            E1 = src(d, '$E_1$', length=3, plus_top=aiding)
            d += elm.Line().right(0.5)
            d += (R1 := elm.Resistor().right().label('R1'))
            d += elm.Line().right(0.5)
            d += (R2 := elm.Resistor().down(6).label('R2', loc='bottom'))
            d += (bot := elm.Line().left().tox(E2.start))
            cur(d, bot, 'I', direction='in')
            hmark(d, R1.start, R1.end, '$U_1$', dy=-0.9)
            vmark(d, R2.start, R2.end, '$U_2$', dx=1.1)


def c07_real_source():
    with drawing('c07_real_source') as d:
        E = src(d, '$E$')
        d += (Rv := elm.Resistor().right().label('$R_{вн}$', loc='bottom'))
        d += elm.Line().right(1)
        d += (a := elm.Dot(open=True))
        d += (w := elm.Line().right(2))
        d += (Rn := elm.Resistor().down().label('$R_н$', loc='bottom'))
        d += elm.Line().left(2)
        d += (b := elm.Dot(open=True))
        d += elm.Line().left().tox(E.start)
        cur(d, w, '$I_н$')
        hmark(d, Rv.start, Rv.end, '$U_{вн}=I_нR_{вн}$', dy=1.3, below=False)
        vmark(d, a.center, b.center, '$U_н$', dx=0.6)
        d += elm.EncircleBox([E, Rv], padx=0.5, pady=0.8).linestyle('--').label('ИН', loc='bottom').color(BLUE)
        d += elm.EncircleBox([Rn], padx=0.9, pady=0.6).linestyle('--').label('Н', loc='bottom').color(BLUE)


def c08_amp_resistor():
    with drawing('c08_amp_res') as d:
        E = src(d, '$E_п$', length=6)
        d += (w := elm.Line().right(2.5))
        d += (R1 := elm.Resistor().down().label('R1', loc='bottom'))
        d += (n := elm.Dot())
        d += (R2 := elm.ResistorVar().down().label('R2', loc='bottom'))
        d += (g := elm.Dot())
        d += elm.Line().left().tox(E.start)
        d += elm.Line().right(3).at(n.center)
        d += (o1 := elm.Dot(open=True))
        d += elm.Line().right(3).at(g.center)
        d += (o2 := elm.Dot(open=True))
        cur(d, w, 'I')
        vmark(d, R1.start, R1.end, '$U_1,\\ P_1$', dx=1.5)
        vmark(d, R2.start, R2.end, '$U_2,\\ P_2$', dx=1.5)
        vmark(d, o1.center, o2.center, '$U_{вых}\\sim$', dx=0.5)
        txt(d, (R2.center[0] - 1.6, R2.center[1]), '$P_{вх}\\sim$\n(ручка)', color=BLUE)


def c03b_key_states():
    """Схема 1.3 в двух состояниях: где течёт ток и где «падает» напряжение."""
    for name, closed in (('c03b_key_closed', True), ('c03c_key_open', False)):
        x0 = 0
        with drawing(name) as d:
            d += elm.Vdd().at((x0, 0)).label('$+U_п$')
            d += (w1 := elm.Line().down(1.2).at((x0, 0)))
            d += (R1 := elm.Resistor().down().label('R1', loc='bottom'))
            d += (n := elm.Dot())
            if closed:
                d += (K := elm.Line().down(3).color(BLUE))
            else:
                d += (K := elm.Switch().down(3))
            d += (g := elm.Dot())
            d += elm.Ground()
            d += elm.Line().right(3.5).at(n.center)
            d += (o1 := elm.Dot(open=True))
            d += elm.Line().right(3.5).at(g.center)
            d += (o2 := elm.Dot(open=True))
            if closed:
                cur(d, w1, '$I = U_п/R1$', loc='bottom')
                vmark(d, R1.start, R1.end, '$U_1 = I·R1 = U_п$', dx=1.3)
                vmark(d, o1.center, o2.center, '$U_{вых} = I·0 = 0$', dx=0.4)
                txt(d, (x0 - 0.3, K.center[1]), 'Кл1 замкнут\n= провод (R = 0)', color=BLUE, halign='right')
                txt(d, (x0 + 2.2, 1.6), 'Кл1 замкнут → «0»', fontsize=15)
            else:
                txt(d, (x0 - 0.3, w1.center[1]), '$I = 0$', color=PINK, halign='right')
                vmark(d, R1.start, R1.end, '$U_1 = 0·R1 = 0$', dx=1.3)
                vmark(d, o1.center, o2.center, '$U_{вых} = U_п − 0 = U_п$', dx=0.4)
                txt(d, (x0 - 0.5, K.center[1]), 'Кл1 разомкнут\n= разрыв (R = ∞)', color=BLUE, halign='right')
                txt(d, (x0 + 2.2, 1.6), 'Кл1 разомкнут → «1»', fontsize=15)


if __name__ == '__main__':
    for f in (c01_ohm, c02_series, c03_key_logic, c03b_key_states, c04_divider, c05_mixed, c06_kirchhoff, c07_real_source, c08_amp_resistor):
        f()
