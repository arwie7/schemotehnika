from common import *


def two_terminal_out(d, top, bot, text, length=2.5, dx=0.4):
    d += elm.Line().right(length).at(top)
    d += (o1 := elm.Dot(open=True))
    d += elm.Line().right(length).at(bot)
    d += (o2 := elm.Dot(open=True))
    vmark(d, o1.center, o2.center, text, dx=dx)
    return o1, o2


# ---------------- КОНДЕНСАТОРЫ ----------------
def k01():
    with drawing('k01_cap_current_src') as d:
        I = src(d, '$I_0$', kind='i')
        d += elm.Line().right(2.5)
        d += (C := elm.Capacitor().down().label('C', loc='bottom'))
        d += elm.Line().left().tox(I.start)
        vmark(d, C.start, C.end, '$U_C$', dx=1.1)


def k02():
    with drawing('k02_rc_charge') as d:
        E = src(d, '$U_п$')
        d += (R := elm.Resistor().right().label('R', loc='bottom'))
        d += elm.Line().right(1)
        d += (n := elm.Dot())
        d += (C := elm.Capacitor().down().label('C', loc='bottom'))
        d += (g := elm.Dot())
        d += elm.Line().left().tox(E.start)
        hmark(d, R.start, R.end, '$U_R=U_п-U_C$', dy=1.0, below=False)
        two_terminal_out(d, n.center, g.center, '$U_C$', length=2)


def k03():
    with drawing('k03_rc_discharge') as d:
        d += (C := elm.Capacitor().down().label('C (заряжен до $U_п$)', loc='top'))
        d += elm.Line().right(2.5)
        d += (R := elm.Resistor().up().label('R', loc='top'))
        d += elm.Line().left(2.5)
        d += elm.Line().right(5).at(R.end).length(0)
        two_terminal_out(d, R.end, R.start, '$U_C$', length=2)


def k04():
    with drawing('k04_coupling') as d:
        d += (b1 := flow.Box(w=2.4, h=1.6).label('Схема 1'))
        d += elm.Line().right(2.2).at(b1.E)
        d += (n1 := elm.Dot())
        d += (C := elm.Capacitor().right().label('C'))
        d += (n2 := elm.Dot())
        d += elm.Line().right(2.2)
        d += (b2 := flow.Box(w=2.4, h=1.6).anchor('W').label('Схема 2'))
        gy = b1.S[1] - 0.6
        d += elm.Line().at(b1.S).to((b1.S[0], gy)); d += elm.Ground()
        d += elm.Line().at(b2.S).to((b2.S[0], gy)); d += elm.Ground()
        d += elm.Line().at((b1.S[0], gy)).to((b2.S[0], gy))
        for n, t in ((n1, '$U_1$ (есть $U_0$)'), (n2, '$U_2$ ($U_0=0$)')):
            d += elm.Line(arrow='<->').at((n.center[0], n.center[1] - 0.15)).to((n.center[0], gy + 0.15)).color(PINK).linewidth(1.2)
            txt(d, (n.center[0], n.center[1] + 0.9), t, color=PINK)


def k05():
    with drawing('k05_dc_ac') as d:
        d += (i := elm.Dot(open=True).label('вход', loc='left'))
        d += elm.Line().right(2)
        d += (top := elm.Dot())
        d += (R1 := elm.Resistor().down().label('R1', loc='top'))
        d += (m := elm.Dot())
        d += (R2 := elm.Resistor().down().label('R2', loc='top'))
        d += (g := elm.Dot())
        d += elm.Ground()
        d += elm.Line().right(2).at(m.center)
        d += (C1 := elm.Capacitor().down().label('C1', loc='bottom'))
        d += elm.Line().left().tox(g.center)
        d += elm.Line().right(1.5).at(top.center)
        d += (C2 := elm.Capacitor().right().label('C2'))
        d += elm.Line().right(1)
        d += (R3 := elm.Resistor().down(6).label('R3', loc='bottom'))
        d += elm.Line().left().tox(C1.end[0])


def k06():
    with drawing('k06_filters') as d:
        # ФВЧ
        d += (a := elm.Dot(open=True))
        d += (C := elm.Capacitor().right().label('C'))
        d += (n := elm.Dot())
        d += (R := elm.Resistor().down().label('R', loc='bottom'))
        d += (g := elm.Dot())
        d += elm.Line().left().tox(a.center)
        d += (b := elm.Dot(open=True))
        vmark(d, a.center, b.center, '$U_{вх}$', dx=-0.4, side='left')
        two_terminal_out(d, n.center, g.center, '$U_{вых}$', length=1.8)
        txt(d, (3, 1.6), 'ФВЧ (верхних частот)', color=BLUE)
        # ФНЧ
        x0 = 11
        d += (a := elm.Dot(open=True).at((x0, 0)))
        d += (R := elm.Resistor().right().label('R'))
        d += (n := elm.Dot())
        d += (C := elm.Capacitor().down().label('C', loc='bottom'))
        d += (g := elm.Dot())
        d += elm.Line().left().tox(a.center)
        d += (b := elm.Dot(open=True))
        vmark(d, a.center, b.center, '$U_{вх}$', dx=-0.4, side='left')
        two_terminal_out(d, n.center, g.center, '$U_{вых}$', length=1.8)
        txt(d, (x0 + 3, 1.6), 'ФНЧ (нижних частот)', color=BLUE)


def k07():
    with drawing('k07_cap_div_lim') as d:
        S = src(d, '', kind='ac', length=6)
        d += elm.Line().right(2)
        d += (C1 := elm.Capacitor().down().label('C1', loc='bottom'))
        d += (n := elm.Dot())
        d += (C2 := elm.Capacitor().down().label('C2', loc='bottom'))
        d += (g := elm.Dot())
        d += elm.Line().left().tox(S.start)
        two_terminal_out(d, n.center, g.center, '$U_{вых}$', length=2)
        txt(d, (1.0, 7.0), 'делитель', color=BLUE)
        x0 = 9
        d += (a := elm.Dot(open=True).at((x0, 0)))
        d += (C := elm.Capacitor().right().label('C1'))
        d += elm.Line().right(0.5)
        d += (Rn := elm.Resistor().down(4).label('$R_н$', loc='bottom'))
        d += elm.Line().left().tox(a.center)
        d += elm.Dot(open=True)
        txt(d, (x0 + 2, 1.2), 'ограничитель тока', color=BLUE)


def k08():
    with drawing('k08_cap_isolation') as d:
        d += (a := elm.Dot(open=True))
        d += elm.Capacitor().right(4).label('C → 0')
        d += (b := elm.Dot(open=True))
        d += (c := elm.Dot(open=True).at((0, -2.5)))
        d += elm.Line().right(4)
        d += (e := elm.Dot(open=True))
        vmark(d, a.center, c.center, '$U_{вх}$', dx=-0.4, side='left')
        vmark(d, b.center, e.center, '$U_{вых}$', dx=0.4)


def k09():
    with drawing('k09_cap_connect') as d:
        # параллельно
        d += (t := elm.Dot(open=True))
        d += elm.Line().right(1)
        for i, nm in enumerate(('C1', 'C2', 'Cn')):
            d.push()
            d += elm.Capacitor().down().label(nm, loc='bottom')
            d.pop()
            if i < 2:
                d += elm.Line().right(2)
        d += elm.Line().left(5).at((1 + 4, -3)).to((0, -3))
        d += elm.Dot(open=True)
        txt(d, (2.8, 1.0), 'параллельно: $C_p=\\Sigma C_i$', color=BLUE)
        # последовательно с источником
        x0 = 9
        E = src(d, '$E$', at=(x0, -3))
        d += (C1 := elm.Capacitor().right().label('C1'))
        d += (C2 := elm.Capacitor().right().label('C2'))
        d += elm.Line().down(3)
        d += elm.Line().left().tox(x0)
        hmark(d, C1.start, C1.end, '$U_1$', dy=-0.9)
        hmark(d, C2.start, C2.end, '$U_2$', dy=-0.9)
        txt(d, (x0 + 3, 1.0), 'последовательно', color=BLUE)


# ---------------- КАТУШКА И КОНТУРЫ ----------------
def l01():
    with drawing('l01_series_combos') as d:
        d += elm.Dot(open=True)
        d += elm.Capacitor().right().label('$X_C$')
        d += elm.Resistor().right().label('R')
        d += elm.Dot(open=True)
        txt(d, (8, 0), '$Z=\\sqrt{X_C^2+R^2}$', halign='left')
        d += elm.Dot(open=True).at((0, -2.2))
        d += elm.Inductor2().right().label('$X_L$')
        d += elm.Resistor().right().label('R')
        d += elm.Dot(open=True)
        txt(d, (8, -2.2), '$Z=\\sqrt{X_L^2+R^2}$', halign='left')
        d += elm.Dot(open=True).at((0, -4.4))
        d += elm.Inductor2().right().label('$X_L$')
        d += elm.Capacitor().right().label('$X_C$')
        d += elm.Dot(open=True)
        txt(d, (8, -4.4), '$X_р=X_L-X_C$', halign='left')


def l02():
    with drawing('l02_series_lc') as d:
        S = src(d, '', kind='ac')
        d += (w := elm.Line().right(1))
        d += elm.Capacitor().right().label('$C_к$')
        d += elm.Line().right(0.5)
        d += elm.Inductor2().down().label('$L_к$', loc='bottom')
        d += elm.Line().left().tox(S.start)
        cur(d, w, '$I_к$')


def l03():
    with drawing('l03_parallel_lc') as d:
        d += (L := elm.Inductor2().down().label('$L_к$', loc='top'))
        d += elm.Line().right(2.5)
        d += (C := elm.Capacitor().up().label('$C_к$', loc='top'))
        d += elm.Line().left(2.5)
        d += elm.Dot().at(C.end)
        d += elm.Dot().at(C.start)
        two_terminal_out(d, C.end, C.start, '$U_к$', length=1.8)


def l04():
    with drawing('l04_parallel_shunted') as d:
        S = src(d, '', kind='ac', length=4)
        d += elm.Line().right(2)
        d += (n1 := elm.Dot())
        d += elm.Capacitor().down(4).label('$C_к$', loc='top')
        d += elm.Line().right(2).at(n1.center)
        d += (n2 := elm.Dot())
        d += elm.Resistor().down(4).label('$R_к$', loc='top').color(BLUE)
        d += elm.Line().right(2).at(n2.center)
        d += elm.Inductor2().down(4).label('$L_к$', loc='bottom')
        d += elm.Line().left().tox(S.start)


# ---------------- ТРАНСФОРМАТОРЫ ----------------
def tr_core(d, x, y_top, y_bot, gap=0.25):
    d += elm.Line().at((x - gap, y_top)).to((x - gap, y_bot)).linewidth(2.4)
    d += elm.Line().at((x + gap, y_top)).to((x + gap, y_bot)).linewidth(2.4)


def winding(d, x, y_top, length=2.4, loops=4, flip=False, label=None, lab_loc='bottom'):
    w = elm.Inductor2(loops=loops).down(length).at((x, y_top))
    if flip:
        w = w.flip()
    if label:
        w = w.label(label, loc=lab_loc)
    d += w
    return w


def t01():
    with drawing('t01_basic') as d:
        S = src(d, '$U_1$', kind='ac', length=3.6)
        d += (w1 := elm.Line().right(2))
        P = winding(d, 2.6, S.end[1], length=S.end[1] - S.start[1], flip=True, label='$n_1$', lab_loc='top')
        d += elm.Line().at((2, S.end[1])).to((2.6, S.end[1]))
        d += elm.Line().at(S.start).to((2.6, S.start[1]))
        tr_core(d, 3.25, S.end[1] + 0.3, S.start[1] - 0.3)
        Sw = winding(d, 3.9, S.end[1], length=S.end[1] - S.start[1], label='$n_2$', lab_loc='bottom')
        d += (w2 := elm.Line().at((3.9, S.end[1])).to((6, S.end[1])))
        d += (o1 := elm.Dot(open=True))
        d += elm.Line().at((3.9, S.start[1])).to((6, S.start[1]))
        d += (o2 := elm.Dot(open=True))
        cur(d, w1, '$I_1$')
        cur(d, w2, '$I_2$', direction='out')
        vmark(d, o1.center, o2.center, '$U_2$', dx=0.4)


def t02():
    with drawing('t02_load_transform') as d:
        d += (a := elm.Dot(open=True))
        d += (w1 := elm.Line().right(2))
        winding(d, 2, 0, length=3, flip=True)
        d += elm.Line().at((2, -3)).to((0, -3))
        d += (b := elm.Dot(open=True))
        tr_core(d, 2.65, 0.3, -3.3)
        winding(d, 3.3, 0, length=3)
        d += elm.Line().at((3.3, 0)).to((5.5, 0))
        d += (Rn := elm.Resistor().down(3).label('$R_н$', loc='bottom'))
        d += elm.Line().left().tox(3.3)
        cur(d, w1, '$I_1$')
        vmark(d, a.center, b.center, '$U_1$', dx=-0.4, side='left')
        txt(d, (0.2, -4.3), "$R'_н=U_1/I_1=n^2R_н$", color=BLUE, halign='left')


def t03():
    with drawing('t03_matching') as d:
        S = src(d, '$E_г$', kind='ac', length=3)
        d += (Rg := elm.Resistor().right(2.2).label('$R_г$'))
        d += elm.Line().right(1.5)
        winding(d, 3.7, 3, length=3, flip=True)
        d += elm.Line().at(S.start).to((3.7, 0))
        tr_core(d, 4.35, 3.3, -0.3)
        winding(d, 5.0, 3, length=3)
        d += elm.Line().at((5.0, 3)).to((7.2, 3))
        d += elm.Resistor().down(3).label('$R_н$', loc='bottom')
        d += elm.Line().left().tox(5.0)
        txt(d, (1.1, -0.8), 'Г (генератор)', color=BLUE)
        txt(d, (4.35, -0.8), 'СУ', color=BLUE)
        txt(d, (6.6, -0.8), 'Н', color=BLUE)


def t04():
    with drawing('t04_split3') as d:
        S = src(d, '$E_г$', kind='ac', length=6)
        d += elm.Resistor().right(2.5).label('$R_г$')
        winding(d, 2.5, 6, length=6, loops=4, flip=True)
        d += elm.Line().at(S.start).to((2.5, 0))
        tr_core(d, 3.15, 6.3, -0.3)
        for k, y in enumerate((6, 3.9, 1.8)):
            winding(d, 3.8, y, length=1.6, loops=3)
            d += elm.Line().at((3.8, y)).to((6.2, y))
            d += elm.Resistor().down(1.6).label(f'$R_{{н{k+1}}}$ (выход {k+1})', loc='bottom')
            d += elm.Line().left().tox(3.8)


def t05():
    with drawing('t05_center_tap') as d:
        S = src(d, '$U_1$', kind='ac', length=4)
        d += elm.Line().right(1.5)
        winding(d, 1.5, 4, length=4, loops=5, flip=True)
        d += elm.Line().at(S.start).to((1.5, 0))
        tr_core(d, 2.15, 4.3, -0.3)
        winding(d, 2.8, 4, length=2, loops=3)
        winding(d, 2.8, 2, length=2, loops=3)
        d += elm.Line().at((2.8, 4)).to((5, 4))
        d += (o1 := elm.Dot(open=True))
        d += elm.Line().at((2.8, 2)).to((5, 2))
        d += (om := elm.Dot(open=True))
        d += elm.Ground().at((4.2, 2))
        d += elm.Line().at((2.8, 0)).to((5, 0))
        d += (o2 := elm.Dot(open=True))
        vmark(d, o1.center, om.center, '$U_{21}$', dx=0.4)
        vmark(d, om.center, o2.center, '$U_{22}$ (в противофазе)', dx=0.4)


def t06():
    with drawing('t06_isolation') as d:
        d += (b1 := flow.Box(w=2, h=2.6).label('ЭЦ1'))
        d += elm.Line().at((b1.E[0], b1.E[1] + 1)).to((2.5, b1.E[1] + 1))
        winding(d, 2.5, b1.E[1] + 1, length=2, flip=True)
        d += elm.Line().at((2.5, b1.E[1] - 1)).to((b1.E[0], b1.E[1] - 1))
        tr_core(d, 3.15, b1.E[1] + 1.3, b1.E[1] - 1.3)
        winding(d, 3.8, b1.E[1] + 1, length=2)
        d += elm.Line().at((3.8, b1.E[1] + 1)).to((5.2, b1.E[1] + 1))
        d += elm.Line().at((3.8, b1.E[1] - 1)).to((5.2, b1.E[1] - 1))
        d += flow.Box(w=2, h=2.6).at((5.2, b1.E[1])).anchor('W').label('ЭЦ2')
        txt(d, (3.15, b1.E[1] + 2.1), 'нет электрического соединения', color=BLUE)


def t07():
    with drawing('t07_autotransformer') as d:
        d += (a := elm.Dot(open=True))
        d += elm.Line().right(2)
        winding(d, 2, 0, length=2.4, loops=4, flip=True)
        winding(d, 2, -2.4, length=1.6, loops=3, flip=True)
        d += elm.Dot().at((2, -2.4))
        d += elm.Line().at((2, -4)).to((0, -4))
        d += (b := elm.Dot(open=True))
        tr_core(d, 2.65, 0.3, -2.0)
        d += elm.Line().at((2, -2.4)).to((4.5, -2.4))
        d += (o1 := elm.Dot(open=True))
        d += elm.Line().at((2, -4)).to((4.5, -4))
        d += (o2 := elm.Dot(open=True))
        vmark(d, a.center, b.center, '$U_1$', dx=-0.4, side='left')
        vmark(d, o1.center, o2.center, '$U_2<U_1$', dx=0.4)


def t08():
    with drawing('t08_windings') as d:
        def coil(x, y, label):
            d.__iadd__(elm.Inductor2(loops=4).right(2.6).at((x, y)).label(label, loc='bottom'))
            d.__iadd__(elm.Label().at((x + 0.15, y + 0.55)).label('●', fontsize=9))
        y = 0
        coil(0, y, '$U_1$'); coil(4, y, '$U_2$')
        d += elm.Line().at((2.6, y)).to((4, y))
        d += elm.Dot(open=True).at((0, y)); d += elm.Dot(open=True).at((6.6, y))
        hmark(d, (0, y - 1.3), (6.6, y - 1.3), '$U=U_1+U_2$', dy=0)
        txt(d, (8.0, y), '1) последовательно СОГЛАСНО:\nконец 1-й → начало 2-й', color=BLUE, halign='left')
        y = -4
        coil(0, y, '$U_1$'); coil(4, y, '$U_2$')
        d += elm.Line().at((2.6, y)).to((2.6, y + 1.2)); d += elm.Line().at((2.6, y + 1.2)).to((6.6, y + 1.2)); d += elm.Line().at((6.6, y + 1.2)).to((6.6, y))
        d += elm.Line().at((4, y)).to((4, y - 0.9)); d += elm.Dot(open=True).at((4, y - 0.9))
        d += elm.Line().at((0, y)).to((0, y - 0.9)); d += elm.Dot(open=True).at((0, y - 0.9))
        hmark(d, (0, y - 1.6), (4, y - 1.6), '$U=U_1-U_2$', dy=0)
        txt(d, (8.0, y), '2) последовательно ВСТРЕЧНО:\nконец 1-й → конец 2-й', color=BLUE, halign='left')
        y = -9
        coil(0, y, '$U_1$'); coil(4, y, '$U_2$')
        d += elm.Line().at((0, y)).to((0, y - 1.0)); d += elm.Line().at((0, y - 1.0)).to((4, y - 1.0)); d += elm.Line().at((4, y - 1.0)).to((4, y))
        d += elm.Line().at((2.6, y)).to((2.6, y + 1.2)); d += elm.Line().at((2.6, y + 1.2)).to((6.6, y + 1.2)); d += elm.Line().at((6.6, y + 1.2)).to((6.6, y))
        d += elm.Line().at((2, y - 1.0)).to((2, y - 2.0)); d += elm.Dot(open=True).at((2, y - 2.0))
        d += elm.Line().at((6.6, y + 1.2)).to((7.6, y + 1.2)); d += elm.Dot(open=True).at((7.6, y + 1.2))
        txt(d, (8.0, y - 0.6), '3) ПАРАЛЛЕЛЬНО: начала вместе, концы вместе;\nтолько если $U_1=U_2$ → $I=I_1+I_2$', color=BLUE, halign='left')


if __name__ == '__main__':
    for f in (k01, k02, k03, k04, k05, k06, k07, k08, k09, l01, l02, l03, l04, t01, t02, t03, t04, t05, t06, t07, t08):
        f()
