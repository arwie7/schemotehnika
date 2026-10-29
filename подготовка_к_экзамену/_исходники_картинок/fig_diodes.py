from common import *
from fig_reactive import winding, tr_core


def out2(d, top, bot, text, length=2.0, dx=0.4):
    d += elm.Line().right(length).at(top)
    d += (o1 := elm.Dot(open=True))
    d += elm.Line().right(length).at(bot)
    d += (o2 := elm.Dot(open=True))
    if text:
        vmark(d, o1.center, o2.center, text, dx=dx)
    return o1, o2


def d01():
    with drawing('d01_bias') as d:
        E = src(d, '$U_{пр}$')
        d += (w := elm.Line().right(1))
        d += (D := elm.Diode().right().label('VD', loc='top'))
        d += elm.Line().right(1)
        d += elm.Line().down(3)
        d += elm.Line().left().tox(E.start)
        cur(d, w, '$I_{пр}$')
        txt(d, (2.5, -0.9), 'прямое смещение:\n«+» на аноде → открыт', color=BLUE)
        x0 = 9
        E2 = src(d, '$U_{обр}$', at=(x0, 0), plus_top=False)
        d += (w2 := elm.Line().right(1))
        d += elm.Diode().right().label('VD', loc='top')
        d += elm.Line().right(1)
        d += elm.Line().down(3)
        d += elm.Line().left().tox(x0)
        txt(d, (x0 + 2.5, -0.9), 'обратное смещение:\n«+» на катоде → закрыт\n($I_{обр}$ очень мал)', color=BLUE)


def d02():
    with drawing('d02_polarity') as d:
        E = src(d, '$E$=9 В')
        d += elm.Line().right(1)
        d += (D := elm.Diode().right().label('VD1', loc='bottom'))
        d += (w := elm.Line().right(1.5))
        d += (R := elm.Resistor().down().label('$R_н$=1 кОм', loc='bottom'))
        d += elm.Line().left().tox(E.start)
        cur(d, w, '$I_н$=8,4 мА')
        hmark(d, D.start, D.end, '$U_{пр}$≈0,6 В', dy=1.2, below=False)
        vmark(d, R.start, R.end, '$U_н=E-U_{пр}$=8,4 В', dx=2.4)


def d03():
    with drawing('d03_dynamic') as d:
        S = src(d, '$E_г$ (импульсы ±)', kind='pulse')
        d += elm.Resistor().right().label('R1')
        d += elm.Line().right(0.5)
        d += (D := elm.Diode().down().label('VD1', loc='bottom'))
        d += elm.Line().left().tox(S.start)
        d += elm.Ground().at(S.start)
        vmark(d, D.start, D.end, '$U_{VD1}$', dx=1.4)


def _limiter(name, kind):
    with drawing(name) as d:
        d += (a := elm.Dot(open=True).at((0, 0)))
        d += elm.Resistor().right(3).label('$R_б$')
        d += (n := elm.Dot())
        top = n.center
        h = 3.6
        bot = (top[0], top[1] - h)
        if kind == 'a':
            d += elm.Diode().up().at(bot).to(top).label('VD1', loc='bottom')
        elif kind == 'b':
            d += elm.Diode().up(1.8).at((top[0], top[1] - 1.8)).to(top).label('VD1', loc='bottom')
            d += elm.Battery().up(1.8).at(bot).to((top[0], top[1] - 1.8)).label('$U_{оп}$', loc='bottom')
            txt(d, (top[0] - 0.4, top[1] - 2.0), '−', fontsize=12)
            txt(d, (top[0] - 0.4, bot[1] + 0.3), '+', fontsize=12)
        elif kind == 'v':
            d += elm.Diode().up(1.8).at(bot).label('VD2', loc='top')
            d += elm.Diode().up(1.8).label('VD1', loc='top')
            d += elm.Line().right(2.2).at(top)
            d += (n2 := elm.Dot())
            d += elm.Diode().down(1.8).label('VD3', loc='bottom')
            d += elm.Diode().down(1.8).label('VD4', loc='bottom')
            top = n2.center
        elif kind == 'g':
            d += elm.Zener().up().at(bot).to(top).label('VD1', loc='top')
            d += elm.Line().right(2.2).at(n.center)
            d += (n2 := elm.Dot())
            d += elm.Zener().down(h).label('VD2', loc='bottom')
            top = n2.center
        elif kind == 'd':
            d += elm.Zener().up().at(bot).to(top).label('VD1', loc='top')
            d += elm.Line().right(2.2).at(n.center)
            d += (n2 := elm.Dot())
            d += elm.Diode().up(h).at((n2.center[0], bot[1])).to(n2.center).label('VD2', loc='bottom')
            top = n2.center
        d += elm.Line().at((0, bot[1])).to((top[0] + 1.8, bot[1]))
        d += elm.Dot(open=True).at((0, bot[1]))
        d += elm.Line().right(1.8).at(top)
        d += (o1 := elm.Dot(open=True))
        d += elm.Dot(open=True).at((top[0] + 1.8, bot[1]))
        vmark(d, (0, 0), (0, bot[1]), '$U_{вх}$', dx=-0.4, side='left')
        vmark(d, o1.center, (o1.center[0], bot[1]), '$U_{вых}$', dx=0.4)


def d04():
    for name, kind in (('d04a_lim', 'a'), ('d04b_lim', 'b'), ('d04v_lim', 'v'), ('d04g_lim', 'g'), ('d04d_lim', 'd')):
        _limiter(name, kind)


def d05():
    with drawing('d05_protect_es') as d:
        d += (a := elm.Dot(open=True).label('вход', loc='left'))
        d += elm.Resistor().right().label('$R_б$')
        d += (n := elm.Dot())
        d += elm.Diode().down().label('VD1', loc='top')
        d += (g := elm.Dot())
        d += elm.Ground()
        d += elm.Line().right(1.6).at(n.center)
        d += (n2 := elm.Dot())
        d += elm.Diode().up().at((n2.center[0], g.center[1])).to(n2.center).label('VD2', loc='bottom')
        d += elm.Line().at(g.center).to((n2.center[0], g.center[1]))
        d += elm.Line().right(1.5).at(n2.center)
        d += flow.Box(w=2.2, h=1.8).anchor('W').label('ЭС')


def d06():
    with drawing('d06_speaker') as d:
        # а) без диодов
        d += elm.Dot(open=True).at((0, 0)); d += elm.Line().right(4)
        d += elm.Dot(open=True).at((0, -1.2)); d += elm.Line().right(4)
        d += (sp := elm.Speaker().at((4, 0)).anchor('in1'))
        d += elm.Line().at((4, -1.2)).to(sp.in2)
        txt(d, (1.5, 0.6), 'линия', color=BLUE)
        txt(d, (5.6, -0.6), 'Гр1', halign='left')
        txt(d, (2.5, -2.6), 'а) без диодов', color=PINK)
        # б) с диодами
        y0 = -5
        d += elm.Dot(open=True).at((0, y0)); d += elm.Line().right(1)
        d += (p := elm.Dot())
        d += elm.Line().up(0.6); d += elm.Diode().right(2).label('VD1', loc='top'); d += elm.Line().down(0.6)
        d += elm.Line().down(0.6).at(p.center); d += elm.Diode().left(2).at((3, y0 - 0.6)).label('VD2', loc='bottom'); d += elm.Line().up(0.6).at((3, y0 - 0.6))
        d += elm.Dot().at((3, y0))
        d += elm.Line().right(1).at((3, y0))
        d += elm.Dot(open=True).at((0, y0 - 1.6)); d += elm.Line().right(4)
        d += (sp2 := elm.Speaker().at((4, y0)).anchor('in1'))
        d += elm.Line().at((4, y0 - 1.6)).to(sp2.in2)
        txt(d, (5.6, y0 - 0.8), 'Гр1', halign='left')
        txt(d, (2.5, y0 - 2.8), 'б) встречно-параллельные VD1, VD2 (кремний)', color=BLUE)


def d07():
    with drawing('d07_microammeter') as d:
        d += (a := elm.Dot(open=True))
        d += elm.Diode().right().label('VD1 (Ge)')
        d += elm.MeterA().right().label('μA', loc='bottom')
        d += elm.Line().right(0.6)
        d += elm.Line().down(2.5)
        d += elm.Line().left().tox(a.center)
        d += (b := elm.Dot(open=True))
        vmark(d, a.center, b.center, '~', dx=-0.4, side='left')


def d08():
    with drawing('d08_diodes_parallel') as d:
        d += (a := elm.Dot())
        d += elm.Line().left(1).at(a.center).label('$I_р$', loc='top')
        d += elm.Line().up(1).at(a.center)
        d += (D1 := elm.Diode().right().label('VD1'))
        d += elm.Line().down(1)
        d += (b := elm.Dot())
        d += elm.Line().down(1).at(a.center)
        d += (D2 := elm.Diode().right().label('VD2', loc='bottom'))
        d += elm.Line().up(1)
        d += elm.Line().right(1).at(b.center)
        txt(d, (1.5, -2.4), 'без резисторов', color=PINK)
        x0 = 8
        d += (a2 := elm.Dot().at((x0, 0)))
        d += elm.Line().left(1).at(a2.center).label('$I_р$', loc='top')
        d += elm.Line().up(1).at(a2.center)
        d += elm.Resistor().right(2.4).label('R1')
        d += elm.Diode().right().label('VD1')
        d += elm.Line().down(1)
        d += (b2 := elm.Dot())
        d += elm.Line().down(1).at(a2.center)
        d += elm.Resistor().right(2.4).label('R2', loc='bottom')
        d += elm.Diode().right().label('VD2', loc='bottom')
        d += elm.Line().up(1)
        d += elm.Line().right(1).at(b2.center)
        txt(d, (x0 + 2.7, -2.4), 'R1 = R2 выравнивают токи', color=PINK)


def d09():
    with drawing('d09_diodes_series') as d:
        d += elm.Dot(open=True)
        d += elm.Diode().right().label('VD1').label('$U_{обр1}$', loc='bottom', color=PINK)
        d += elm.Diode().right().label('VD2').label('$U_{обр2}$', loc='bottom', color=PINK)
        d += elm.Dot(open=True)
        txt(d, (3, -1.6), 'без шунтов: $U_{обр1}\\neq U_{обр2}$', color=PINK)
        x0 = 9
        d += (a := elm.Dot().at((x0, 0)))
        d += elm.Line().left(0.8).at(a.center)
        d += elm.Dot(open=True)
        d += elm.Diode().right().at(a.center).label('VD1')
        d += (m := elm.Dot())
        d += elm.Diode().right().label('VD2')
        d += (b := elm.Dot())
        d += elm.Line().right(0.8)
        d += elm.Dot(open=True)
        d += elm.Line().down(1.2).at(a.center)
        d += elm.Resistor().right(3).label('$R_ш$', loc='bottom')
        d += elm.Line().up(1.2)
        d += elm.Resistor().right(3).at((m.center[0], -1.2)).label('$R_ш$', loc='bottom')
        d += elm.Line().up(1.2)
        txt(d, (x0 + 3, -2.6), 'с $R_ш$: $U_{обр1}\\approx U_{обр2}$', color=PINK)


def d10():
    with drawing('d10_zener_stab') as d:
        d += (a := elm.Dot(open=True).label('+', loc='left'))
        d += (Rb := elm.Resistor().right().label('$R_б$'))
        d += (n := elm.Dot())
        d += (Z := elm.Zener().up().at((n.center[0], n.center[1] - 3)).to(n.center).label('VD1', loc='top'))
        d += elm.Line().right(2.5).at(n.center)
        d += (Rn := elm.Resistor().down(3).label('$R_н$', loc='bottom'))
        d += elm.Line().left().tox(a.center)
        d += (b := elm.Dot(open=True).label('−', loc='left'))
        hmark(d, Rb.start, Rb.end, '$U_б$', dy=1.0, below=False)
        vmark(d, a.center, b.center, '$U_{вх}$', dx=-0.5, side='left')
        vmark(d, Rn.start, Rn.end, '$U_н=U_{ст}$', dx=1.1)
        txt(d, (n.center[0] + 0.4, n.center[1] - 1.0), '$I_{ст}$', color=PINK, halign='left')


def d11():
    with drawing('d11_varicap_bias') as d:
        E = src(d, '$U_{обр}$ (регулируемое)')
        d += elm.Line().right(2.5)
        d += (V := elm.Varactor().down().reverse().label('варикап', loc='bottom'))
        d += elm.Line().left().tox(E.start)
        txt(d, (1.2, -1.4), '$U_{обр}$↑ → δ↑ → $C_п$↓', color=PINK)


def d12():
    with drawing('d12_log') as d:
        d += (I := elm.SourceI().down().label('$I_{вх}$', loc='top'))
        d += (n := elm.Dot())
        d += elm.Diode().down().label('VD', loc='bottom')
        d += elm.Ground()
        d += elm.Line().right(2.5).at(n.center)
        d += elm.Dot(open=True).label('$U_{вых}=F(I_{вх})$ — логарифм', loc='right')


def d13():
    with drawing('d13_noise') as d:
        d += (Z := elm.Zener().up(2.4).label('VD1', loc='top'))
        d += elm.Line().right(2).at(Z.end)
        d += (B := flow.Box(w=2.2, h=2.4).anchor('NW').label('ГШ'))
        d += elm.Line().at(Z.start).to((Z.start[0] + 2, Z.start[1]))
        d += elm.Line().right(1.5).at(B.E)
        d += elm.Dot(open=True).label('$U_ш$', loc='right')
        txt(d, (2.5, -1.2), 'малый ток: $I_{ст}<I_{ст\\,min}$ → шум', color=PINK)


def d14():
    with drawing('d14_magnetodiode') as d:
        E = src(d, '$U_{см}$')
        d += (D := elm.Diode().up().label('VD1', loc='top'))
        d += (n := elm.Dot())
        d += (R := elm.Resistor().right().label('$R_1$', loc='bottom'))
        d += (m := elm.Dot())
        d += elm.Line().down().toy(E.start[1])
        d += elm.Line().left().tox(E.start[0])
        d += elm.Line().up(1.2).at(n.center)
        d += elm.Line().right(4.5)
        d += (o1 := elm.Dot(open=True))
        d += elm.Line().right(1.5).at(m.center)
        d += (o2 := elm.Dot(open=True))
        txt(d, (o1.center[0] + 0.4, (o1.center[1] + o2.center[1]) / 2), '$U_{вых}=F(B)$', color=PINK, halign='left')


def d15():
    with drawing('d15_thermometer') as d:
        I = src(d, '$I_{пр}$=const', kind='i')
        d += elm.Line().right(3)
        d += (n := elm.Dot())
        d += (D := elm.Diode().down().label('VD', loc='bottom'))
        d += (g := elm.Dot())
        d += elm.Line().left().tox(I.start)
        out2(d, n.center, g.center, '$U_{пр}=F(t°)$')


def d16():
    with drawing('d16_coil_protect') as d:
        d += elm.Vdd().label('+U')
        d += elm.Inductor2().down().label('L', loc='bottom')
        d += elm.Switch().down().label('Кл1', loc='bottom')
        d += elm.Ground()
        txt(d, (0, -7.6), 'а) без защиты', color=PINK)
        x0 = 6
        d += elm.Vdd().at((x0, 0)).label('+U')
        d += (t := elm.Dot())
        d += (L := elm.Inductor2().down().label('L', loc='top'))
        d += (b := elm.Dot())
        d += elm.Switch().down().label('Кл1', loc='bottom')
        d += elm.Ground()
        d += elm.Line().right(1.6).at(t.center)
        d += elm.Diode().up().at((x0 + 1.6, b.center[1])).to((x0 + 1.6, t.center[1])).label('VD1', loc='bottom')
        d += elm.Line().at(b.center).to((x0 + 1.6, b.center[1]))
        txt(d, (x0, -7.6), 'б) с защитным диодом', color=BLUE)


def d17():
    with drawing('d17_backup_power') as d:
        d += (ip := flow.Box(w=3.0, h=1.6).label('ИП\n(сеть 220 В)'))
        d += elm.Line().right(2.0).at((ip.E[0], ip.E[1] + 0.4))
        txt(d, (ip.E[0] + 1.0, ip.E[1] + 0.9), '12 В', color=PINK)
        d += elm.Diode().right().label('VD1')
        d += (n := elm.Dot())
        d += elm.Line().right(1.5)
        d += (h := flow.Box(w=2.0, h=1.6).anchor('W').label('Н\n(9–12 В)'))
        d += (D2 := elm.Diode().up(3).at((n.center[0], n.center[1] - 3)).to(n.center).label('VD2', loc='bottom'))
        d += elm.Line().down(0.6).at(D2.start)
        d += (rb := flow.Box(w=2.0, h=1.4).anchor('N').label('РБ\n9 В'))


def d18():
    with drawing('d18_rectifier') as d:
        d += (a := elm.Dot(open=True))
        d += elm.Line().right(1)
        winding(d, 1, 0, length=3, flip=True)
        d += elm.Line().at((1, -3)).to((0, -3))
        d += elm.Dot(open=True)
        tr_core(d, 1.65, 0.3, -3.3)
        winding(d, 2.3, 0, length=3)
        d += elm.Line().at((2.3, 0)).to((2.8, 0))
        d += (D := elm.Diode().right().label('VD1').label('$I_{пр}$', loc='bottom', color=PINK))
        d += (n := elm.Dot())
        d += (C := elm.Capacitor2().down(3).label('$C_1$', loc='top').color(PINK))
        d += (g := elm.Dot())
        d += elm.Line().left().tox(2.3)
        d += elm.Line().right(2.2).at(n.center)
        d += elm.Resistor().down(3).label('$R_н$', loc='bottom')
        d += elm.Line().left().tox(g.center[0])


if __name__ == '__main__':
    for f in (d01, d02, d03, d04, d05, d06, d07, d08, d09, d10, d11, d12, d13, d14, d15, d16, d17, d18):
        try:
            f()
        except Exception as ex:
            print('FAIL', f.__name__, repr(ex))
