"""Усилительные каскады (p-n-p, как на слайдах: «минус» E_к сверху)."""
from common import *

YT = 8.0      # верхняя шина (−E_к)
XB, YB = 6.0, 3.6   # база транзистора
XR = 4.0      # x цепей базы
KC_Y = 6.0    # узел коллектора


def stage(name, bias='divider', emitter='gnd', load='parallel', rf=False, cf=False,
          thermistor=False, notes=(), show_u=True):
    with drawing(name) as d:
        Q = elm.BjtPnp(circle=True).right().flip().at((XB, YB))
        d += Q
        txt(d, (Q.collector[0] + 0.5, YB + 0.1), 'VT1', halign='left')
        XC = Q.collector[0]
        x_ek = 15.5 if rf else 13.5
        x_left = -1.5 if bias == 'series_divider' else 0
        # ---- коллекторная цепь
        if load == 'series':
            d += elm.Resistor().down().at((XC, YT)).toy(KC_Y).label('$R_н$', loc='top').color(BLUE)
        else:
            d += elm.Resistor().down().at((XC, YT)).toy(KC_Y).label('$R_к$', loc='top')
        d += (kc := elm.Dot().at((XC, KC_Y)))
        d += elm.Line().at((XC, KC_Y)).to(Q.collector)
        x_load = XC + 4.0
        if load == 'parallel':
            d += elm.Line().right(1.0).at((XC, KC_Y))
            d += elm.Capacitor().right(2.0).label('$C_р$')
            d += elm.Line().right().tox(x_load)
            d += elm.Resistor().down().toy(0).label('$R_н$', loc='bottom').color(BLUE)
            d += elm.Dot()
        # ---- эмиттерная цепь
        if emitter == 'gnd':
            d += elm.Line().down().at(Q.emitter).toy(0)
        elif emitter == 're':
            d += elm.Resistor().down().at(Q.emitter).toy(0).label('$R_э$', loc='bottom').color(PINK)
        elif emitter == 're_ce':
            d += elm.Resistor().down().at(Q.emitter).toy(0).label('$R_э$', loc='top').color(PINK)
            d += elm.Dot().at(Q.emitter)
            d += elm.Line().right(1.4).at(Q.emitter)
            d += elm.Capacitor().down().toy(0).label('$C_э$', loc='bottom').color(PINK)
        elif emitter == 're_split':
            ym = Q.emitter[1] / 2
            d += elm.Resistor().down().at(Q.emitter).toy(ym).label('$R_{э1}$', loc='top').color(PINK)
            d += elm.Dot()
            d += elm.Resistor().down().toy(0).label('$R_{э2}$', loc='top').color(PINK)
            d += elm.Line().right(1.4).at((XC, ym))
            d += elm.Capacitor().down().toy(0).label('$C_э$', loc='bottom').color(PINK)
        d += elm.Dot().at((XC, 0))
        # ---- питание E_к (+ снизу, − сверху)
        top_right = x_ek
        if rf:
            d += elm.Line().at((XC, YT)).to((12.0, YT))
            d += (A := elm.Dot().label('A', loc='top'))
            d += elm.Resistor().right().tox(x_ek).label('$R_ф$').color(PINK)
        Ek = elm.Battery().up().at((x_ek, 0)).toy(YT).label('$E_к$', loc='bottom')
        d += Ek
        txt(d, (x_ek - 0.5, YT - 1.2), '−'); txt(d, (x_ek - 0.5, 1.2), '+')
        if cf:
            d += elm.Line().at((x_ek, YT)).to((x_ek - 1.4, YT))
            d += elm.Capacitor().down().toy(0).label('$C_{ф2}$', loc='top').color(BLUE)
        # ---- базовая цепь и генератор
        gen_top = None
        if bias in ('divider', 'divider_collector', 'rb_collector', 'rb_eb'):
            # генератор через Cб
            S = elm.SourceSin().up(1.8).at((0, 0)).label('$E_г$', loc='top')
            d += S
            d += elm.Resistor().up(1.8).label('$R_г$', loc='top')
            d += elm.Line().right(0.4)
            d += elm.Capacitor().right(1.8).label('$C_б$')
            d += elm.Line().right().tox(XR)
            d += (bn := elm.Dot())
            d += elm.Line().to(Q.base)
            if bias == 'divider':
                d += elm.Resistor().down().at((XR, YT)).toy(YB).label('$R_{б1}$', loc='top')
                R2 = elm.Thermistor() if thermistor else elm.Resistor()
                d += R2.down().at((XR, YB)).toy(0).label('$R_{б2}$' + (' (t°)' if thermistor else ''), loc='top').color(PINK if thermistor else 'black')
            elif bias == 'divider_collector':
                d += elm.Line().at((XC, KC_Y)).to((XR, KC_Y))
                d += elm.Resistor().down().at((XR, KC_Y)).toy(YB).label('$R_{б1}$', loc='top').color(PINK)
                d += elm.Resistor().down().at((XR, YB)).toy(0).label('$R_{б2}$', loc='top')
            elif bias == 'rb_collector':
                d += elm.Line().at((XR, YB)).to((XR, KC_Y))
                d += elm.Resistor().right().at((XR, KC_Y)).tox(XC).label('$R_б$').color(PINK)
            elif bias == 'rb_eb':
                d += elm.Resistor().down(1.8).at((XR, YB)).label('$R_б$', loc='top').color(PINK)
                Eb = elm.Battery().down().toy(0).label('$E_б$', loc='top')
                d += Eb
                txt(d, (XR + 0.5, Eb.start[1] - 0.3), '−'); txt(d, (XR + 0.5, 0.3), '+')
            if bias != 'divider' or True:
                pass
            d += elm.Line().at((0, 0)).to((x_ek, 0))
            if bias in ('divider',):
                d += elm.Line().at((XR, YT)).to((XC, YT))
            if not rf:
                d += elm.Line().at((XC, YT)).to((x_ek, YT))
            if rf and bias == 'divider':
                d += elm.Line().at((XR, YT)).to((XC, YT))
        elif bias == 'eb_series':
            S = elm.SourceSin().up(1.8).at((0, 1.2)).label('$E_г$', loc='top')
            d += S
            d += elm.Resistor().up().toy(YB).label('$R_г$', loc='top')
            d += elm.Line().right().tox(Q.base[0])
            d += elm.Line().at((0, 1.2)).to((0, 0))
            d += elm.Line().right(0.6)
            Eb = elm.Battery().right(2.4).label('$E_б$', loc='top')
            d += Eb
            txt(d, (Eb.start[0] + 0.2, -0.5), '−'); txt(d, (Eb.end[0] - 0.2, -0.5), '+')
            d += elm.Line().right().tox(x_ek)
            if cf:
                d += elm.Line().at((0.3, 0)).to((0.3, -1.4))
                d += elm.Capacitor().right().tox(Eb.end[0] + 0.4).label('$C_{ф1}$', loc='bottom').color(BLUE)
                d += elm.Line().up().toy(0)
            d += elm.Line().at((XC, YT)).to((x_ek, YT))
        elif bias == 'series_divider':
            S = elm.SourceSin().up(1.8).at((0, 0)).label('$E_г$', loc='top')
            d += S
            d += elm.Resistor().up().toy(YB).label('$R_г$', loc='top')
            d += elm.Line().right().tox(Q.base[0])
            d += elm.Resistor().down().at((-1.5, YT)).toy(0).label('$R_{б1}$', loc='top').color(PINK)
            d += elm.Line().right().tox(0)
            d += elm.Dot()
            d += elm.Resistor().right(3.2).label('$R_{б2}$', loc='bottom').color(PINK)
            txt(d, (0.5, 0.45), '−', color=PINK); txt(d, (2.9, 0.45), '+', color=PINK)
            d += elm.Line().right().tox(x_ek)
            d += elm.Line().at((-1.5, YT)).to((x_ek, YT))
        for (xy, t, c) in notes:
            txt(d, xy, t, color=c, halign='left')


def a_stages():
    stage('a04_ce_series_load', bias='eb_series', load='series', cf=True)
    stage('a05_ce_parallel_load', bias='eb_series', load='parallel', cf=True)
    stage('a06_bias_rb_eb', bias='rb_eb')
    stage('a07_bias_series_div', bias='series_divider')
    stage('a08_bias_divider', bias='divider')
    stage('a09_thermistor', bias='divider', thermistor=True)
    stage('a10_emitter_stab', bias='divider', emitter='re')
    stage('a11_collector_stab', bias='rb_collector')
    stage('a12_collector_divider', bias='divider_collector')
    stage('a13_combined', bias='divider', emitter='re', rf=True)
    stage('a15_re_ce', bias='divider', emitter='re_ce')
    stage('a16_re_split', bias='divider', emitter='re_split')


def a01():
    with drawing('a01_block') as d:
        d += (G := flow.Box(w=2, h=1.6).label('Г'))
        d += elm.Arrow().right(2.6).at(G.E).label('$U_{вх}, I_{вх}, P_{вх}$', fontsize=10)
        d += (U := flow.Box(w=2.6, h=1.8).anchor('W').label('>  (У)'))
        d += elm.Arrow().right(2.6).at(U.E).label('$U_{вых}, I_{вых}, P_{вых}$', fontsize=10)
        d += flow.Box(w=2, h=1.6).anchor('W').label('Н')
        d += (I := flow.Box(w=2.4, h=1.2).at((U.N[0], U.N[1] + 1.4)).anchor('S').label('ИП'))
        d += elm.Arrow().down(1.4).at(I.S)
        txt(d, (U.S[0], U.S[1] - 0.6), '$R_{вх}$ — слева, $R_{вых}$ — справа', color=BLUE)


def a03():
    with drawing('a03_equiv') as d:
        S = src(d, '$E_г$', kind='ac', length=3)
        d += elm.Resistor().right(2).label('$R_г$').color(PINK)
        d += elm.Dot(open=True)
        d += elm.Line().right(1.2)
        d += (Rin := elm.Resistor().down(3).label('$R_{вх}$', loc='bottom'))
        d += elm.Line().left().tox(0)
        x1 = 6.5
        d += elm.Line().at((x1, 0)).to((x1, 0.6))
        d += elm.SourceSin().up(1.2).label('$E_{вых}$', loc='top')
        d += elm.Resistor().up(1.2).label('$R_{вых}$', loc='top')
        d += elm.Line().right(1.4)
        d += elm.Dot(open=True)
        d += elm.Line().right(1.2)
        d += elm.Resistor().down(3).label('$R_н$', loc='bottom').color(PINK)
        d += elm.Line().left().tox(x1)
        d += elm.EncircleBox([Rin], padx=0.6, pady=0.3).linestyle('--').color(BLUE)
        txt(d, (5.0, 3.7), 'усилитель «изнутри»', color=BLUE)


def a17():
    with drawing('a17_fb_block') as d:
        d += elm.Line().right(2).at((0, 0)).label('$U_{вх}$', loc='top')
        d += (Sx := elm.Dot())
        d += elm.Arrow().right(1.2)
        d += (Y := flow.Box(w=2.4, h=1.6).anchor('W').label('У (K)'))
        d += elm.Line().right(1.4).at(Y.E)
        d += (o := elm.Dot())
        d += elm.Arrow().right(2).label('$U_{вых}$', loc='top')
        d += elm.Line().up(2.4).at(o.center)
        d += elm.Arrow().left(1.4)
        d += (B := flow.Box(w=2.4, h=1.4).anchor('E').label('ОС (β)'))
        d += elm.Line().left().at(B.W).tox(Sx.center[0])
        d += elm.Arrow().down().toy(0.1).label('$U_{ос}$', loc='bottom')


def a18():
    with drawing('a18_jfet_amp') as d:
        J = elm.JFetN(circle=True).right().at((6.0, 4.6))
        d += J
        # гейт справа у элемента schemdraw → зеркалим через reverse
        d.elements.remove(J)
        J = elm.JFetN(circle=True).right().reverse().at((6.0, 4.6))
        d += J
        xd = J.drain[0]
        d += elm.Resistor().down().at((xd, YT)).toy(J.drain[1] + 0.6).label('$R_с$', loc='bottom')
        d += (kc := elm.Dot())
        d += elm.Line().to(J.drain)
        d += elm.Resistor().down().at(J.source).toy(0).label('$R_и$', loc='bottom').color(PINK)
        txt(d, (J.source[0] - 0.4, J.source[1] - 0.6), '+', color=PINK); txt(d, (J.source[0] - 0.4, 0.4), '−', color=PINK)
        d += elm.Line().right(1.0).at(kc.center)
        d += elm.Capacitor().right(2.0).label('$C_р$')
        d += elm.Line().right(0.8)
        d += elm.Resistor().down().toy(0).label('$R_н$', loc='bottom').color(BLUE)
        S = elm.SourceSin().up(1.8).at((0, 0)).label('$E_г$', loc='top')
        d += S
        d += elm.Resistor().up().toy(J.gate[1]).label('$R_г$', loc='top')
        d += elm.Line().right(0.4)
        d += elm.Capacitor().right(1.8).label('$C_з$')
        d += elm.Line().right().tox(XR)
        d += elm.Dot()
        d += elm.Line().right().tox(J.gate[0])
        d += elm.Resistor().down().at((XR, J.gate[1])).toy(0).label('$R_з$', loc='top')
        d += elm.Line().at((0, 0)).to((13.5, 0))
        d += elm.Line().at((xd, YT)).to((13.5, YT))
        Ec = elm.Battery().down().at((13.5, YT)).toy(0).label('$E_с$', loc='bottom')
        d += Ec
        txt(d, (13.0, YT - 1.2), '+'); txt(d, (13.0, 1.2), '−')


def a21():
    with drawing('a21_pp_block') as d:
        d += elm.Arrow().right(1.6).at((0, 0)).label('±', loc='top')
        d += (F := flow.Box(w=2, h=1.6).anchor('W').label('ФИ'))
        d += elm.Line().up(1.8).at(F.N)
        d += elm.Arrow().right(2.2).label('+', loc='top')
        d += (K1 := flow.Box(w=2, h=1.2).anchor('W').label('1КУ'))
        d += elm.Line().down(2.6).at(F.S)
        d += elm.Arrow().right(2.2).label('−', loc='bottom')
        d += (K2 := flow.Box(w=2, h=1.2).anchor('W').label('2КУ'))
        d += (S := flow.Box(w=1.6, h=1.6).at((K1.E[0] + 2.2, 0)).anchor('W').label('Σ'))
        d += elm.Line().right().at(K1.E).tox(S.N[0])
        d += elm.Arrow().down().toy(S.N[1])
        d += elm.Line().right().at(K2.E).tox(S.S[0])
        d += elm.Arrow().up().toy(S.S[1])
        d += elm.Arrow().right(1.6).at(S.E).label('±', loc='top')


def a22():
    with drawing('a22_pp_complementary') as d:
        d += (Q1 := elm.BjtNpn(circle=True).right().at((5, 5)))
        d += (Q2 := elm.BjtPnp(circle=True).right().at((5, 1)))
        txt(d, (Q1.base[0] + 1.6, 5.6), 'VT1 (n-p-n)', halign='left')
        txt(d, (Q2.base[0] + 1.6, 0.4), 'VT2 (p-n-p)', halign='left')
        xe = Q1.emitter[0]
        d += elm.Line().at(Q1.emitter).to(Q2.emitter)
        d += (m := elm.Dot().at((xe, 3)))
        d += elm.Resistor().right(3.5).at((xe, 3)).label('$R_н$').color(BLUE)
        d += (mid := elm.Dot())
        d += elm.Ground()
        d += elm.Line().up().at(Q1.collector).toy(7.5)
        d += elm.Line().right().tox(mid.center[0] + 1.5)
        E1 = elm.Battery().down().toy(3).label('$E_к/2$', loc='bottom')
        d += E1
        txt(d, (E1.start[0] - 0.5, 7.0), '+'); txt(d, (E1.start[0] - 0.5, 3.6), '−')
        E2 = elm.Battery().down().toy(-1.5).label('$E_к/2$', loc='bottom')
        d += E2
        txt(d, (E1.start[0] - 0.5, 2.4), '+'); txt(d, (E1.start[0] - 0.5, -1.0), '−')
        d += elm.Line().at((mid.center[0], 3)).to((mid.center[0] + 1.5, 3))
        d += elm.Line().at((mid.center[0] + 1.5, -1.5)).to((xe, -1.5))
        d += elm.Line().at(Q2.collector).to((xe, -1.5))
        # смещение
        d += elm.Resistor().down().at((3.4, 7.5)).toy(Q1.base[1]).label('$R_{б1}$', loc='top')
        d += elm.Line().at((3.4, 7.5)).to((xe, 7.5))
        d += elm.Line().at((3.4, Q1.base[1])).to(Q1.base)
        d += elm.Line().at((3.4, Q1.base[1])).to((3.4, Q2.base[1]))
        d += elm.Dot().at((3.4, 3))
        d += elm.Line().at((3.4, Q2.base[1])).to(Q2.base)
        d += elm.Resistor().down().at((3.4, Q2.base[1])).toy(-1.5).label('$R_{б2}$', loc='top')
        d += elm.Line().at((3.4, -1.5)).to((xe, -1.5))
        d += elm.Capacitor().left(1.6).at((3.4, 3)).label('$C_б$')
        d += elm.Resistor().left(1.6).label('$R_г$')
        d += elm.SourceSin().down(1.6).label('$E_г$', loc='bottom')
        d += elm.Ground()


def a23():
    with drawing('a23_pp_two_npn') as d:
        d += (Q1 := elm.BjtNpn(circle=True).right().at((5, 5)))
        d += (Q2 := elm.BjtNpn(circle=True).right().at((5, 1)))
        txt(d, (Q1.base[0] + 1.6, 5.6), 'VT1', halign='left'); txt(d, (Q2.base[0] + 1.6, 1.6), 'VT2', halign='left')
        xe = Q1.emitter[0]
        d += elm.Line().at(Q1.collector).to((xe, 7.5))
        d += elm.Line().at(Q1.emitter).to(Q2.collector)
        d += elm.Dot().at((xe, 3))
        d += elm.Line().at(Q2.emitter).to((xe, -1.0))
        d += elm.Line().right(1.0).at((xe, 3))
        d += elm.Capacitor().right(1.8).label('$C_р$')
        d += elm.Line().right(0.6)
        d += elm.Resistor().down().toy(-1.0).label('$R_н$', loc='bottom').color(BLUE)
        xr = 10.6
        d += elm.Line().at((0.8, 7.5)).to((xr + 1.6, 7.5))
        E = elm.Battery().down().at((xr + 1.6, 7.5)).toy(-1.0).label('$E_к$', loc='bottom')
        d += E
        txt(d, (xr + 1.1, 6.6), '+'); txt(d, (xr + 1.1, 0), '−')
        d += elm.Line().at((0.8, -1.0)).to((xr + 1.6, -1.0))
        for (x, yb, n1, n2, inp) in ((3.4, Q1.base[1], '$R_{б1}$', '$R_{б2}$', '$U_{вх1}$'), (1.6, Q2.base[1], '$R_{б3}$', '$R_{б4}$', '$U_{вх2}$')):
            pass
        d += elm.Resistor().down().at((3.6, 7.5)).toy(Q1.base[1]).label('$R_{б1}$', loc='bottom')
        d += elm.Dot(); d += elm.Line().to(Q1.base)
        d += elm.Resistor().down().at((3.6, Q1.base[1])).toy(-1.0).label('$R_{б2}$', loc='bottom')
        d += elm.Resistor().down().at((2.0, 7.5)).toy(Q2.base[1]).label('$R_{б3}$', loc='top')
        d += elm.Dot(); d += elm.Line().to(Q2.base)
        d += elm.Resistor().down().at((2.0, Q2.base[1])).toy(-1.0).label('$R_{б4}$', loc='top')
        d += elm.Capacitor().left(2.4).at((3.6, Q1.base[1] + 0.0)).label('$C_{б1}$')
        d += elm.Dot(open=True).label('$U_{вх1}$', loc='left')
        d += elm.Capacitor().left(1.4).at((2.0, Q2.base[1])).label('$C_{б2}$', loc='bottom')
        d += elm.Dot(open=True).label('$U_{вх2}$', loc='left')
        d += elm.Line().at((0.8, 7.5)).to((0.8, 7.5))


def a24():
    with drawing('a24_phase_inverter') as d:
        Q = elm.BjtNpn(circle=True).right().at((XB, YB))
        d += Q
        XC = Q.collector[0]
        d += elm.Resistor().down().at((XC, YT)).toy(KC_Y).label('$R_к$', loc='top')
        d += elm.Dot()
        d += elm.Line().to(Q.collector)
        d += elm.Line().right(1.0).at((XC, KC_Y)); d += elm.Capacitor().right(1.6).label('$C_{р1}$'); d += elm.Dot(open=True).label('$U_{вых1}$', loc='right')
        d += elm.Line().down(0.5).at(Q.emitter)
        d += (en := elm.Dot())
        d += elm.Resistor().down().toy(0).label('$R_э$', loc='top')
        d += elm.Line().right(1.0).at(en.center); d += elm.Capacitor().right(1.6).label('$C_{р2}$'); d += elm.Dot(open=True).label('$U_{вых2}$', loc='right')
        S = elm.SourceSin().up(1.8).at((0, 0)).label('$E_г$', loc='top')
        d += S
        d += elm.Resistor().up(1.8).label('$R_г$', loc='top')
        d += elm.Line().right(0.4)
        d += elm.Capacitor().right(1.8).label('$C_б$')
        d += elm.Line().right().tox(XR)
        d += elm.Dot(); d += elm.Line().to(Q.base)
        d += elm.Resistor().down().at((XR, YT)).toy(YB).label('$R_{б1}$', loc='top')
        d += elm.Resistor().down().at((XR, YB)).toy(0).label('$R_{б2}$', loc='top')
        d += elm.Line().at((0, 0)).to((13.5, 0))
        d += elm.Line().at((XR, YT)).to((13.5, YT))
        E = elm.Battery().down().at((13.5, YT)).toy(0).label('$E_к$', loc='bottom')
        d += E
        txt(d, (13.0, YT - 1.2), '+'); txt(d, (13.0, 1.2), '−')


if __name__ == '__main__':
    for f in (a_stages, a01, a03, a17, a18, a21, a22, a23, a24):
        try:
            f()
        except Exception as ex:
            import traceback; traceback.print_exc()


def a25():
    stage('a25_final', bias='divider', emitter='re_ce', rf=True)


if __name__ == '__main__':
    a25()
