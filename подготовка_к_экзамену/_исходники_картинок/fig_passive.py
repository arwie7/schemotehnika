from common import *


# ---------------- РЕЗИСТОРЫ ----------------
def r01_redistribution():
    with drawing('r01_redistr_U') as d:
        E = src(d, '$E_п$', length=6)
        d += elm.Line().right(1.5)
        tops = []
        for i, (a, b, c) in enumerate((('R1', 'R2', 'C1'), ('R3', 'R4', 'C2'), ('R5', 'R6', 'C3'))):
            d.push()
            d += (Ra := elm.Resistor().down().label(a, loc='bottom'))
            d += (n := elm.Dot())
            d += (Rb := elm.Resistor().down().label(b, loc='bottom'))
            d += (g := elm.Dot())
            d += elm.Line().right(1.2).at(n.center)
            d += (bx := flow.Box(w=1.4, h=1.1).anchor('N').label(c))
            d += elm.Line().down().at(bx.S).toy(g.center[1])
            d += elm.Line().left().tox(g.center[0])
            vmark(d, Rb.start, Rb.end, f'$U_{i+1}$', dx=-0.6, side='left')
            d.pop()
            if i < 2:
                d += elm.Line().right(4.5)
        d += elm.Line().down(6).at(E.start).length(0)
        d += elm.Line().right().at(E.start).tox(n.center[0] + 1.9)

    with drawing('r02_redistr_I') as d:
        E = src(d, '$E_п$')
        d += (w := elm.Line().right(1))
        cur(d, w, 'I')
        d += (n := elm.Dot())
        for i, (r, c, L) in enumerate((('R1', 'C3', 7), ('R2', 'C2', 5), ('R3', 'C1', 3))):
            d.push()
            if i:
                d += elm.Line().down(1.4 * i)
            d += (wr := elm.Line().right(0.6))
            d += elm.Resistor().right().label(r)
            d += (wi := elm.Line().right(L - 3))
            cur(d, wi, f'$I_{i+1}$')
            d += flow.Box(w=1.4, h=1.0).anchor('W').label(c)
            d += elm.Ground().at((d.here[0] + 1.4 + 0.6, d.here[1])) if False else elm.Line().length(0)
            d.pop()
        d += elm.Line().down().at(E.start).length(0.1)
        d += elm.Ground().at(E.start)


def r03_divider_load():
    with drawing('r03_divider_load') as d:
        E = src(d, '$E_п$', length=6)
        d += (w := elm.Line().right(2.5))
        d += (R1 := elm.Resistor().down().label('R1', loc='bottom'))
        d += (n := elm.Dot())
        d += (R2 := elm.Resistor().down().label('R2', loc='bottom'))
        d += (g := elm.Dot())
        d += elm.Line().left().tox(E.start)
        d += (wn := elm.Line().right(3).at(n.center))
        d += (Rn := elm.Resistor().down().label('$R_н$', loc='bottom'))
        d += elm.Line().left().tox(g.center)
        cur(d, w, '$I_д+I_н$')
        cur(d, wn, '$I_н$')
        txt(d, (R2.end[0] - 0.55, R2.end[1] + 0.35), '$I_д$', color=PINK)
        vmark(d, Rn.start, Rn.end, '$U_н$', dx=1.1)


def r04_bias_divider():
    with drawing('r04_bias_divider') as d:
        E = src(d, '$E_п$=9 В', length=7)
        d += (top := elm.Line().right(3))
        d += (R1 := elm.Resistor().down().label('R1', loc='bottom'))
        d += (n := elm.Dot())
        d += (R2 := elm.Resistor().down(4).label('R2', loc='bottom'))
        d += (g := elm.Dot())
        d += elm.Line().left().tox(E.start)
        d += (wb := elm.Line().right(1.5).at(n.center))
        d += (Q := elm.BjtNpn(circle=True).anchor('base').label('VT1', loc='right'))
        d += elm.Line().down().at(Q.emitter).toy(g.center[1])
        d += elm.Line().left().tox(g.center[0])
        d += elm.Line().up().at(Q.collector).length(0.6)
        d += (Rk := elm.Resistor().up().toy(top.end[1]).label('$R_к$', loc='bottom'))
        d += elm.Line().left().tox(top.end[0])
        cur(d, wb, '$I_б$')
        txt(d, (Q.base[0] + 0.3, Q.base[1] - 1.5), '$U_{бэ}$=0,25 В', color=PINK, halign='left')


def r05_led():
    with drawing('r05_led') as d:
        d += (a := elm.Dot(open=True).label('+', loc='left'))
        d += (R := elm.Resistor().right().label('$R_{огр}$', loc='bottom'))
        d += (w := elm.Line().right(2.5))
        d += elm.Line().down(0.8)
        d += (D := elm.LED().down().label('VD1', loc='bottom'))
        d += elm.Line().down(0.8)
        d += elm.Line().left().tox(a.center)
        d += (b := elm.Dot(open=True).label('−', loc='left'))
        vmark(d, a.center, b.center, '$U_{вх}$=15 В', dx=-0.3, side='left')
        vmark(d, D.start, D.end, '$U_д$≈1,5 В', dx=2.2)
        cur(d, w, '$I_д$=15 мА')
        hmark(d, R.start, R.end, '$U_R$=13,5 В', dy=1.0, below=False)


def r06_shunt():
    with drawing('r06_shunt') as d:
        d += (a := elm.Dot(open=True).label('+', loc='left'))
        d += (Rn := elm.Resistor().right().label('$R_н$ (нагрузка)'))
        d += (w := elm.Line().right(1))
        d += (n := elm.Dot())
        d += (Rs := elm.Resistor().down().label('$R_{дт}$', loc='bottom'))
        d += (g := elm.Dot())
        d += elm.Line().left().tox(a.center)
        d += (b := elm.Dot(open=True).label('−', loc='left'))
        d += elm.Line().right(2).at(n.center)
        d += (o1 := elm.Dot(open=True))
        d += elm.Line().right(2).at(g.center)
        d += (o2 := elm.Dot(open=True))
        vmark(d, a.center, b.center, '$U_{вх}$', dx=-0.3, side='left')
        cur(d, w, '$I_н$')
        vmark(d, o1.center, o2.center, '$U_{вых}=R_{дт}I_н$', dx=0.4)


def r07_thermistor():
    with drawing('r07_thermistor') as d:
        d += (a := elm.Dot(open=True).label('+', loc='left'))
        d += (Rk := elm.Thermistor().right().label('$R_к$ (терморезистор, t°)'))
        d += elm.Line().right(1)
        d += (n := elm.Dot())
        d += (R := elm.Resistor().down().label('R', loc='bottom'))
        d += (g := elm.Dot())
        d += elm.Line().left().tox(a.center)
        d += (b := elm.Dot(open=True).label('−', loc='left'))
        d += elm.Line().right(2).at(n.center)
        d += (o1 := elm.Dot(open=True))
        d += elm.Line().right(2).at(g.center)
        d += (o2 := elm.Dot(open=True))
        vmark(d, a.center, b.center, 'U=const', dx=-0.3, side='left')
        vmark(d, o1.center, o2.center, '$U_{вых}=f(t°)$', dx=0.4)


def r08_varistor():
    with drawing('r08_varistor') as d:
        d += (a := elm.Dot(open=True))
        d += (Rb := elm.Resistor().right().label('$R_б$ (балласт)'))
        d += elm.Line().right(1)
        d += (n := elm.Dot())
        d += (Rv := elm.ResistorVar().down().label('RU\n(варистор)', loc='top'))
        d += (g := elm.Dot())
        d += elm.Line().left().tox(a.center)
        d += (b := elm.Dot(open=True))
        d += elm.Line().right(2).at(n.center)
        d += (o1 := elm.Dot(open=True))
        d += elm.Line().right(2).at(g.center)
        d += (o2 := elm.Dot(open=True))
        vmark(d, a.center, b.center, '$U_{вх}$', dx=-0.3, side='left')
        vmark(d, o1.center, o2.center, '$U_{вых}≤U_{огр}$', dx=0.5)


def r09_pot():
    with drawing('r09_pot_divider') as d:
        E = src(d, '$E_п$', length=5)
        d += elm.Line().right(2)
        d += (P := elm.Potentiometer().down(5))
        txt(d, (P.center[0] + 0.9, P.center[1] + 1.0), '$R_п$')
        d += elm.Line().left().tox(E.start)
        d += elm.Line().right(2).at(P.tap)
        d += (Rn := elm.Resistor().down().toy(P.end[1]).label('$R_н$', loc='bottom'))
        d += elm.Line().left().tox(P.end[0])
        vmark(d, P.start, P.tap, '$r_1$', dx=-0.8, side='left', color=BLUE)
        vmark(d, P.tap, P.end, '$r_2$', dx=-0.8, side='left', color=BLUE)


def r10_rheo_vs_pot():
    with drawing('r10_rheo_pot') as d:
        # реостатное включение: движок соединён с концом резистора
        d += (a := elm.Dot(open=True))
        d += (P1 := elm.Potentiometer().down(3))
        d += (n := elm.Dot())
        d += elm.Line().right(0.8).at(P1.tap)
        d += elm.Line().down().toy(n.center[1])
        d += elm.Line().left().tox(n.center[0])
        d += (R2 := elm.Resistor().down(3).at(n.center))
        d += (b := elm.Dot(open=True))
        txt(d, (P1.center[0] - 0.9, P1.center[1]), 'R1', halign='right')
        txt(d, (R2.center[0] - 0.9, R2.center[1]), 'R2', halign='right')
        d += elm.Line().right(3.2).at(n.center)
        d += (o1 := elm.Dot(open=True))
        d += elm.Line().right(3.2).at(b.center)
        d += (o2 := elm.Dot(open=True))
        vmark(d, a.center, b.center, '$U_{вх}$', dx=-1.9, side='left')
        vmark(d, o1.center, o2.center, '$U_{вых}$', dx=0.4)
        txt(d, (1.6, 1.2), 'реостатное', color=BLUE)
        # потенциометрическое включение
        x0 = 11
        d += (c := elm.Dot(open=True).at((x0, 0)))
        d += (P := elm.Potentiometer().down(6))
        d += (e := elm.Dot(open=True))
        txt(d, (P.center[0] - 0.9, P.center[1] + 1.2), 'R1', halign='right')
        d += elm.Line().right(2.5).at(P.tap)
        d += (n2 := elm.Dot())
        d += (R2b := elm.Resistor().down().toy(P.end[1]))
        txt(d, (R2b.center[0] - 0.9, R2b.center[1]), 'R2', halign='right')
        d += elm.Line().left().tox(P.end[0])
        d += elm.Line().right(1.8).at(n2.center)
        d += (o3 := elm.Dot(open=True))
        d += elm.Line().right(1.8).at(R2b.end)
        d += (o4 := elm.Dot(open=True))
        vmark(d, c.center, e.center, '$U_{вх}$', dx=-1.9, side='left')
        vmark(d, o3.center, o4.center, '$U_{вых}$', dx=0.4)
        txt(d, (x0 + 1.6, 1.2), 'потенциометрическое', color=BLUE)


if __name__ == '__main__':
    for f in (r01_redistribution, r03_divider_load, r04_bias_divider, r05_led, r06_shunt, r07_thermistor, r08_varistor, r09_pot, r10_rheo_vs_pot):
        f()
