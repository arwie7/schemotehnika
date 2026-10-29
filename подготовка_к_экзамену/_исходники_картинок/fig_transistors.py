from common import *


def q01():
    with drawing('q01_bjt_supply') as d:
        # n-p-n
        d += (Q := elm.BjtNpn(circle=True).right().at((3, 0)).label('n-p-n', loc='right', ofst=(0.3, 0.6)))
        d += elm.Line().up(1.2).at(Q.collector)
        d += elm.Line().right(2.5)
        Ek = elm.Battery().down(2.6).reverse().label('$E_к$', loc='bottom')
        d += Ek
        txt(d, (Ek.start[0] - 0.5, Ek.start[1] - 0.3), '+'); txt(d, (Ek.end[0] - 0.5, Ek.end[1] + 0.3), '−')
        d += elm.Line().down().toy(Q.emitter[1] - 1.2)
        d += elm.Line().left().tox(Q.emitter[0])
        d += (c := elm.Dot())
        d += elm.Line().up().to(Q.emitter)
        d += (wb := elm.Line().left(1.2).at(Q.base))
        d += elm.Line().down().toy(c.center[1] + 0.0).length(0.01).color('white')
        Eb = elm.Battery().down().reverse().at(wb.end).toy(c.center[1]).label('$E_б$', loc='top')
        d += Eb
        txt(d, (Eb.start[0] + 0.5, Eb.start[1] - 0.3), '+'); txt(d, (Eb.end[0] + 0.5, Eb.end[1] + 0.3), '−')
        d += elm.Line().right().at(Eb.end).tox(c.center[0])
        cur(d, wb, '$I_б$', direction='out')
        txt(d, (Q.collector[0] + 0.7, Q.collector[1] + 0.6), '$I_к$↓', color=PINK)
        txt(d, (Q.emitter[0] + 0.7, Q.emitter[1] - 0.6), '$I_э$↓', color=PINK)
        # p-n-p
        x0 = 11
        d += (Q2 := elm.BjtPnp(circle=True).right().flip().at((x0 + 3, 0)).label('p-n-p', loc='right', ofst=(0.3, 0.6)))
        d += elm.Line().up(1.2).at(Q2.collector)
        d += elm.Line().right(2.5)
        Ek2 = elm.Battery().down(2.6).label('$E_к$', loc='bottom')
        d += Ek2
        txt(d, (Ek2.start[0] - 0.5, Ek2.start[1] - 0.3), '−'); txt(d, (Ek2.end[0] - 0.5, Ek2.end[1] + 0.3), '+')
        d += elm.Line().down().toy(Q2.emitter[1] - 1.2)
        d += elm.Line().left().tox(Q2.emitter[0])
        d += (c2 := elm.Dot())
        d += elm.Line().up().to(Q2.emitter)
        d += (wb2 := elm.Line().left(1.2).at(Q2.base))
        Eb2 = elm.Battery().down().at(wb2.end).toy(c2.center[1]).label('$E_б$', loc='top')
        d += Eb2
        txt(d, (Eb2.start[0] + 0.5, Eb2.start[1] - 0.3), '−'); txt(d, (Eb2.end[0] + 0.5, Eb2.end[1] + 0.3), '+')
        d += elm.Line().right().at(Eb2.end).tox(c2.center[0])
        txt(d, (6, -4.2), '$I_э=I_к+I_б$,  $I_к=\\beta I_б$', color=PINK)


def q02():
    with drawing('q02_two_diodes') as d:
        d += (b := elm.Dot().at((0, 0)))
        d += elm.Line().left(1.5).at(b.center)
        d += elm.Dot(open=True).label('Б', loc='left')
        d += elm.Diode().at(b.center).theta(45).label('', loc='top')
        d += elm.Dot(open=True).label('К', loc='right')
        d += elm.Diode().at(b.center).theta(-45)
        d += elm.Dot(open=True).label('Э', loc='right')
        txt(d, (0.6, -3.2), 'n-p-n: два p-n-перехода\n(анодами к базе)', color=BLUE)
        x0 = 8
        d += (b2 := elm.Dot().at((x0, 0)))
        d += elm.Line().left(1.5).at(b2.center)
        d += elm.Dot(open=True).label('Б', loc='left')
        d += elm.Diode().at(b2.center).theta(45).reverse()
        d += elm.Dot(open=True).label('К', loc='right')
        d += elm.Diode().at(b2.center).theta(-45).reverse()
        d += elm.Dot(open=True).label('Э', loc='right')
        txt(d, (x0 + 0.6, -3.2), 'p-n-p: катодами к базе', color=BLUE)


def q03():
    with drawing('q03_tr_key') as d:
        d += (Q := elm.BjtNpn(circle=True).right().at((0, 0)).label('VT1', loc='right', ofst=(0.4, -0.4)))
        xc = Q.collector[0]
        d += elm.Vdd().at((xc, 4.6)).label('$+U_п$')
        d += (R1 := elm.Resistor().down().at((xc, 4.6)).toy(1.6).label('R1', loc='top'))
        d += (n := elm.Dot())
        d += elm.Line().to(Q.collector)
        d += elm.Line().down().at(Q.emitter).toy(-1.6)
        d += (g := elm.Dot())
        d += elm.Ground()
        d += elm.Line().left(1.5).at(Q.base)
        d += elm.Dot(open=True).label('упр.', loc='left')
        d += elm.Line().right(3).at(n.center)
        d += (o1 := elm.Dot(open=True))
        d += elm.Line().right(3).at(g.center)
        d += (o2 := elm.Dot(open=True))
        vmark(d, R1.start, R1.end, '$U_1$', dx=-0.9, side='left')
        vmark(d, o1.center, o2.center, '$U_{вых}$', dx=0.4)


def q04():
    with drawing('q04_tr_var_res') as d:
        d += (Q := elm.BjtNpn(circle=True).right().at((3, 0)).label('VT1', loc='right', ofst=(0.4, -0.4)))
        xc = Q.collector[0]
        E = src(d, '$E_п$', at=(-1.5, -1.6), length=6.2)
        d += elm.Line().right().tox(xc)
        d += (R1 := elm.Resistor().down().toy(1.6).label('R1', loc='bottom'))
        d += (n := elm.Dot())
        d += elm.Line().to(Q.collector)
        d += elm.Line().down().at(Q.emitter).toy(-1.6)
        d += (g := elm.Dot())
        d += elm.Line().left().tox(-1.5)
        d += elm.Line().left(0.8).at(Q.base)
        d += elm.SourceSin().down().toy(-1.6).label('упр. ~', loc='bottom')
        d += elm.Line().right(3).at(n.center)
        d += (o1 := elm.Dot(open=True))
        d += elm.Line().right(3).at(g.center)
        d += (o2 := elm.Dot(open=True))
        vmark(d, o1.center, o2.center, '$U_2=U_{вых}$', dx=0.4)
        vmark(d, R1.start, R1.end, '$U_1$', dx=0.9)


def q05():
    with drawing('q05_lamp') as d:
        Eb = src(d, '$E_б$', at=(0, 0), length=4)
        d += elm.Line().right(2)
        d += (P := elm.Potentiometer().down(4))
        txt(d, (P.center[0] - 0.6, P.center[1] + 1.3), '$R_р$')
        d += elm.Line().left().tox(0)
        d += (Q := elm.BjtNpn(circle=True).right().at((P.tap[0] + 1.8, P.tap[1])))
        txt(d, (Q.base[0] + 1.9, Q.base[1] - 0.2), 'VT1', halign='left')
        d += elm.Line().at(P.tap).to(Q.base)
        d += elm.Line().down().at(Q.emitter).toy(0)
        d += (ge := elm.Dot())
        d += elm.Ground()
        d += elm.Line().left().at(ge.center).tox(2)
        d += elm.Line().up(1.6).at(Q.collector)
        d += (L := elm.Lamp().up(2.4).label('HL1', loc='top'))
        d += elm.Line().up(0.8)
        d += elm.Line().right(4.5)
        Ek = elm.Battery().down().reverse().label('$E_к$', loc='bottom')
        d += Ek
        txt(d, (Ek.start[0] - 0.5, Ek.start[1] - 0.4), '+'); txt(d, (Ek.end[0] - 0.5, Ek.end[1] + 0.4), '−')
        d += elm.Line().down().toy(0)
        d += elm.Line().left().tox(ge.center[0])
        vmark(d, L.start, L.end, '$U_{HL1}$', dx=1.8)
        vmark(d, Q.collector, (Q.emitter[0], 0), '$U_{кэ}$', dx=1.8)
        txt(d, (Q.base[0] - 0.9, Q.base[1] - 1.1), '$U_{бэ}$', color=PINK)


def q06():
    with drawing('q06_ce_cb_cc') as d:
        yb = -2.2
        # ОЭ: вход база, выход коллектор, эмиттер общий
        d += (Q := elm.BjtNpn(circle=True).right().at((1.5, 0)))
        d += elm.Line().left(1.5).at(Q.base); d += elm.Dot(open=True).label('Вх', loc='left')
        d += elm.Line().up(0.6).at(Q.collector); d += elm.Line().right(1.6); d += elm.Dot(open=True).label('Вых', loc='right')
        d += elm.Line().down().at(Q.emitter).toy(yb); d += elm.Dot(); d += elm.Ground()
        d += elm.Line().at((0, yb)).to((3.9, yb))
        txt(d, (2.0, -3.6), 'ОЭ (общий эмиттер)', color=BLUE)
        # ОБ: вход эмиттер, выход коллектор, база общая
        x0 = 9
        d += (Q2 := elm.BjtNpn(circle=True).right().at((x0, 0)))
        d += elm.Line().down(0.6).at(Q2.emitter); d += elm.Line().left(2.3); d += elm.Dot(open=True).label('Вх', loc='left')
        d += elm.Line().up(0.6).at(Q2.collector); d += elm.Line().right(1.6); d += elm.Dot(open=True).label('Вых', loc='right')
        d += elm.Line().left(0.6).at(Q2.base); d += elm.Line().down().toy(yb); d += elm.Dot(); d += elm.Ground()
        d += elm.Line().at((x0 - 1.6, yb)).to((x0 + 2.4, yb))
        txt(d, (x0 + 0.5, -3.6), 'ОБ (общая база)', color=BLUE)
        # ОК: вход база, выход эмиттер, коллектор общий
        x1 = 16.5
        d += (Q3 := elm.BjtNpn(circle=True).right().at((x1, 0)))
        d += elm.Line().left(1.5).at(Q3.base); d += elm.Dot(open=True).label('Вх', loc='left')
        d += elm.Line().up(0.6).at(Q3.collector); d += elm.Line().right(1.4); d += elm.Line().down().toy(yb); d += elm.Dot(); d += elm.Ground()
        d += elm.Line().down(0.6).at(Q3.emitter); d += elm.Line().right(0.9); d += elm.Dot(open=True).label('Вых', loc='right')
        d += elm.Line().at((x1 - 1.5, yb)).to((x1 + 2.6, yb))
        txt(d, (x1 + 0.6, -3.6), 'ОК (общий коллектор)', color=BLUE)


def q07():
    with drawing('q07_thermal_runaway') as d:
        d += (Q := elm.BjtNpn(circle=True).right().at((4, 3.4)).label('VT1', loc='right', ofst=(0.4, -0.4)))
        xc = Q.collector[0]
        E = src(d, '$E$', at=(0, 0), length=6)
        d += elm.Line().right().tox(xc)
        d += (t := elm.Line().down().toy(Q.collector[1]))
        d += elm.Dot().at((2.2, 6))
        d += (Rb := elm.Resistor().down().at((2.2, 6)).toy(Q.base[1]).label('$R_б$', loc='top'))
        d += elm.Line().right().tox(Q.base[0])
        d += (Rn := elm.Resistor().down().at(Q.emitter).toy(0).label('$R_н$', loc='bottom'))
        d += elm.Line().left().tox(0)
        cur(d, t, '$I_к$', loc='bottom')


def q08():
    with drawing('q08_jfet') as d:
        d += (J := elm.JFetN(circle=True).right().at((3, 4)))
        txt(d, (3.4, 6.2), 'VT (n-канал)', halign='left')
        E = src(d, '$E_с$', at=(-1.2, 0), length=5.4)
        d += elm.Line().right().tox(J.drain[0])
        d += elm.Line().down().toy(J.drain[1])
        d += elm.Line().down().at(J.source).toy(0)
        d += (g := elm.Dot())
        d += elm.Line().left().tox(-1.2)
        d += elm.Line().right(1.6).at(J.gate)
        Ug = elm.Battery().down().toy(0).label('$U_{зи}$', loc='bottom')
        d += Ug
        txt(d, (Ug.start[0] - 0.5, Ug.start[1] - 0.4), '−'); txt(d, (Ug.end[0] - 0.5, Ug.end[1] + 0.4), '+')
        d += elm.Line().left().tox(g.center[0])
        txt(d, (J.drain[0] + 0.3, J.drain[1] + 0.35), 'С', halign='left')
        txt(d, (J.source[0] - 0.3, J.source[1] - 0.2), 'И', halign='right')
        txt(d, (J.gate[0] + 0.3, J.gate[1] + 0.35), 'З', halign='left')


def q09():
    with drawing('q09_relay_key') as d:
        d += (Q := elm.BjtNpn(circle=True).right().at((0, 0)).label('VT1', loc='right', ofst=(0.4, -0.4)))
        xc = Q.collector[0]
        d += elm.Vdd().at((xc, 5)).label('$+E_к$')
        d += (t := elm.Dot())
        d += (K := elm.Inductor2().down().toy(1.8).label('обмотка K', loc='top'))
        d += (b := elm.Dot())
        d += elm.Line().to(Q.collector)
        d += elm.Line().down(0.6).at(Q.emitter); d += elm.Ground()
        d += elm.Line().right(2).at(t.center)
        d += elm.Diode().up().at((xc + 2, b.center[1])).to((xc + 2, t.center[1])).label('VD', loc='bottom')
        d += elm.Line().at(b.center).to((xc + 2, b.center[1]))
        d += elm.Resistor().left(2.4).at(Q.base).label('$R_б$')
        d += elm.Dot(open=True).label('$U_{упр}$', loc='left')


if __name__ == '__main__':
    for f in (q01, q02, q03, q04, q05, q06, q07, q08, q09):
        try:
            f()
        except Exception as ex:
            import traceback; traceback.print_exc()
            print('FAIL', f.__name__, repr(ex))
