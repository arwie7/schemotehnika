"""Графики к учебному файлу. Каждый воспроизводит график со слайдов/лекций (качественно, без «новых» данных)."""
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from common import OUT

plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 11, 'axes.spines.top': False,
                     'axes.spines.right': False, 'axes.titlesize': 11, 'axes.titleweight': 'bold'})
B, P, G, GR = '#1565c0', '#c2185b', '#2e7d32', '#888888'


def save(fig, name):
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, name + '.png'), dpi=120)
    plt.close(fig)
    print('saved', name)


def ax_clean(ax, xl='', yl='', ticks=False):
    ax.set_xlabel(xl, loc='right')
    if yl:
        ax.annotate(yl, xy=(0, 1), xycoords='axes fraction', xytext=(-4, 0), textcoords='offset points',
                    ha='right', va='top', fontsize=11)
    if not ticks:
        ax.set_xticks([]); ax.set_yticks([])


# ---------------- ОСНОВЫ ----------------
def g_vectors():
    fig, axs = plt.subplots(1, 3, figsize=(11, 2.8))
    def arr(ax, dx, dy, c, t):
        ax.annotate('', xy=(dx, dy), xytext=(0, 0), arrowprops=dict(arrowstyle='->', color=c, lw=2))
        ax.text(dx * 1.05 + 0.05, dy * 1.05 + 0.05, t, color=c, fontsize=12)
    arr(axs[0], 1, 0, B, 'U'); arr(axs[0], 0.7, 0, P, 'I'); axs[0].set_title('резистор:\nсдвиг 0° (cos α = 1)')
    arr(axs[1], 1, 0, B, 'U'); arr(axs[1], 0, 0.8, P, 'I'); axs[1].set_title('конденсатор:\nI опережает U на 90°')
    arr(axs[2], 0, 0.8, B, 'U'); arr(axs[2], 1, 0, P, 'I'); axs[2].set_title('катушка:\nU опережает I на 90°')
    for a in axs:
        a.set_xlim(-0.2, 1.4); a.set_ylim(-0.3, 1.1); a.axis('off')
    save(fig, 'g01_vectors')


def g_source():
    fig, ax = plt.subplots(figsize=(5.5, 3.2))
    I = np.linspace(0, 1, 50)
    for r, c, t in ((0, B, '$R_{вн}=0$ (идеальный)'), (0.25, '#8e24aa', '$R_{вн1}$'), (0.6, P, '$R_{вн2}>R_{вн1}$')):
        ax.plot(I, 1 - r * I, c=c, lw=2, label=t)
    ax.legend(frameon=False); ax.set_ylim(0, 1.15)
    ax_clean(ax, '$I_н$', '$U_н$')
    ax.set_title('$U_н=E-I_нR_{вн}$: чем больше $R_{вн}$,\nтем сильнее «проседает» $U_н$')
    save(fig, 'g02_source')


def g_sine():
    t = np.linspace(0, 1.25, 400)
    fig, axs = plt.subplots(1, 2, figsize=(9, 3))
    ax = axs[0]
    ax.plot(t, np.sin(2 * np.pi * t), c=B, lw=2); ax.axhline(0, c='k', lw=0.8)
    ax.annotate('', xy=(0.25, 1), xytext=(0.25, 0), arrowprops=dict(arrowstyle='<->', color=P))
    ax.text(0.28, 0.5, '$U_m$', color=P, fontsize=13)
    ax.annotate('', xy=(1, -1.25), xytext=(0, -1.25), arrowprops=dict(arrowstyle='<->', color=P))
    ax.text(0.5, -1.15, 'T  (f = 1/T)', color=P, ha='center')
    ax.set_ylim(-1.5, 1.3); ax_clean(ax, 't', 'u'); ax.set_title('рис.17: амплитуда, период, частота')
    ax = axs[1]
    tt = np.linspace(0, 1, 400)
    ax.plot(tt, np.sin(2 * np.pi * tt), c=B, lw=2); ax.axhline(0, c='k', lw=0.8)
    ax.fill_between([0, 0.5], 0, 1 / 1.41, color=P, alpha=0.18)
    ax.plot([0, 0.5, 0.5], [1 / 1.41, 1 / 1.41, 0], c=P)
    ax.text(0.52, 0.72, '$U_д$', color=P, fontsize=13); ax.text(0.2, 1.05, '$U_m$', color=B, fontsize=13)
    ax.set_ylim(-1.2, 1.3); ax_clean(ax, 't', 'u'); ax.set_title('рис.18: $U_m=1{,}4\\,U_д$ (220 В → ≈311 В)')
    save(fig, 'g03_sine')


def g_offset_harm():
    t = np.linspace(0, 1.5, 500)
    fig, axs = plt.subplots(1, 3, figsize=(11, 3))
    ax = axs[0]
    ax.plot(t, 1 + 0.8 * np.sin(2 * np.pi * t), c=B, lw=2); ax.axhline(1, ls='--', c=GR); ax.axhline(0, c='k', lw=0.8)
    ax.text(-0.05, 1, '$U_0$', color=P, ha='right', va='center', fontsize=12)
    ax.set_ylim(-0.2, 2); ax_clean(ax, 't', 'u'); ax.set_title('рис.19: постоянная составляющая $U_0$')
    ax = axs[1]
    h1 = np.sin(2 * np.pi * t); h3 = np.sin(6 * np.pi * t) / 3
    ax.plot(t, h1, '--', c='k', lw=1, label='1 — основная'); ax.plot(t, h3, '--', c='#00838f', lw=1, label='2 — добавочная')
    ax.plot(t, h1 + h3, c=P, lw=2, label='3 = 1 + 2'); ax.legend(frameon=False, fontsize=9, loc='lower left')
    ax_clean(ax, 't', 'u'); ax.set_title('рис.20: сумма гармоник')
    ax = axs[2]
    ax.plot(t, np.sin(2 * np.pi * t + 1.0), c=P, lw=2, label='1 (опережает)')
    ax.plot(t, np.sin(2 * np.pi * t), c=B, lw=2, label='2'); ax.axhline(0, c='k', lw=0.8)
    ax.annotate('', xy=(0.25, 1.1), xytext=(0.25 - 1 / (2 * np.pi), 1.1), arrowprops=dict(arrowstyle='<->'))
    ax.text(0.17, 1.2, 'θ'); ax.set_ylim(-1.3, 1.45); ax.legend(frameon=False, fontsize=9, loc='lower left')
    ax_clean(ax, 't', 'u'); ax.set_title('рис.22: фазовый сдвиг θ')
    save(fig, 'g04_offset_harm_phase')


# ---------------- РЕЗИСТОРЫ ----------------
def g_pot():
    a = np.linspace(0, 1, 100)
    fig, axs = plt.subplots(1, 2, figsize=(9, 3.2))
    ax = axs[0]
    ax.plot(a * 100, a * 100, c=B, lw=2, label='1 — линейная')
    ax.plot(a * 100, 100 * np.log10(1 + 9 * a), c=P, lw=2, label='2 — логарифмическая')
    ax.plot(a * 100, 100 * (10 ** a - 1) / 9, c=G, lw=2, label='3 — обратно логарифмическая')
    ax.legend(frameon=False, fontsize=9); ax.set_xlabel('α/α$_п$, %'); ax.set_ylabel('R/R$_п$, %')
    ax = axs[1]
    ax.plot(a * 100, np.where(a < 0.6, 100 * (1 - a / 0.6), 0), c='#ef6c00', lw=2, label='4 — зона насыщения')
    ax.plot(a * 100, np.where(a < 0.4, 0, 100 * (a - 0.4) / 0.6), c='#6a1b9a', lw=2, label='5 — зона нечувствительности')
    ax.legend(frameon=False, fontsize=9); ax.set_xlabel('α/α$_п$, %'); ax.set_ylabel('R/R$_п$, %')
    fig.suptitle('Функциональные характеристики переменного резистора (Лекция 2, п.9)', fontsize=11, fontweight='bold')
    save(fig, 'g05_pot_curves')


def g_varistor():
    I = np.linspace(-1, 1, 400)
    U = np.clip(2.5 * I, -1, 1) + 0.08 * I
    fig, ax = plt.subplots(figsize=(4.6, 3.2))
    ax.plot(I, U, c=B, lw=2); ax.axhline(0, c='k', lw=0.8); ax.axvline(0, c='k', lw=0.8)
    ax.axhline(1, ls='--', c=P, lw=1); ax.axhline(-1, ls='--', c=P, lw=1)
    ax.text(-1, 1.07, '$+U_{огр}$', color=P); ax.text(0.55, -0.9, '$-U_{огр}$', color=P)
    ax_clean(ax, 'I', 'U'); ax.set_title('ВАХ варистора:\nвыше $U_{огр}$ напряжение не растёт')
    save(fig, 'g06_varistor')


# ---------------- КОНДЕНСАТОРЫ ----------------
def g_cap_charge():
    t = np.linspace(0, 5, 400)
    fig, axs = plt.subplots(1, 3, figsize=(12, 3.1))
    ax = axs[0]
    ax.plot(t, np.clip(t / 1.5, 0, 2), c=P, lw=2, label='$C_1$'); ax.plot(t, np.clip(t / 3.5, 0, 2), c=B, lw=2, label='$C_2$')
    ax.legend(frameon=False); ax_clean(ax, 't', '$U_C$'); ax.set_title('рис.3: заряд током $I_0$ ($C_1<C_2$)')
    ax = axs[1]
    u = 1 - np.exp(-t)
    ax.plot(t, u, c=P, lw=2); ax.axhline(1, ls='--', c=GR); ax.plot([1, 1, 0], [0, 0.63, 0.63], ':', c='k')
    ax.text(1.05, 0.05, 'τ = RC'); ax.text(-0.1, 0.63, '0,63$U_п$', ha='right', va='center'); ax.text(-0.1, 1, '$U_п$', ha='right', va='center')
    ax_clean(ax, 't', '$U_C$'); ax.set_title('рис.4 (заряд через R)')
    ax = axs[2]
    u = np.exp(-t)
    ax.plot(t, u, c=P, lw=2); ax.plot([1, 1, 0], [0, 0.37, 0.37], ':', c='k')
    ax.text(1.05, 0.42, 'τ = RC'); ax.text(-0.1, 0.37, '0,37$U_п$', ha='right', va='center'); ax.text(-0.1, 1, '$U_п$', ha='right', va='center')
    ax_clean(ax, 't', '$U_C$'); ax.set_title('разряд через R')
    save(fig, 'g07_cap_charge')


def g_coupling():
    t = np.linspace(0, 2, 400)
    fig, axs = plt.subplots(1, 2, figsize=(9, 2.8), sharey=True)
    axs[0].plot(t, 1.2 + 0.6 * np.sin(2 * np.pi * t), c='#00838f', lw=2); axs[0].axhline(1.2, ls='--', c=GR)
    axs[0].text(-0.05, 1.2, '$U_0$', ha='right', va='center', color=P); axs[0].set_title('до конденсатора: $U_1=U_0+U_{1m}\\sin$')
    axs[1].plot(t, 0.6 * np.sin(2 * np.pi * t), c='#00838f', lw=2); axs[1].axhline(0, c='k', lw=0.8)
    axs[1].set_title('после: $U_2$, постоянной составляющей нет')
    for a in axs:
        ax_clean(a, 't', 'u')
    save(fig, 'g08_coupling')


def g_filters():
    f = np.logspace(-2, 2, 400)
    fig, axs = plt.subplots(1, 2, figsize=(9, 3))
    axs[0].semilogx(f, f / np.sqrt(1 + f ** 2), c=P, lw=2); axs[0].set_title('ФВЧ (C последовательно, R на выходе)')
    axs[1].semilogx(f, 1 / np.sqrt(1 + f ** 2), c=P, lw=2); axs[1].set_title('ФНЧ (R последовательно, C на выходе)')
    for a in axs:
        ax_clean(a, 'f', '$U_{вых}$'); a.set_ylim(0, 1.1)
    save(fig, 'g09_filters')


def g_rectifier():
    t = np.linspace(0, 3, 900)
    half = np.clip(np.sin(2 * np.pi * t), 0, None)
    # сглаженное: заряд до пика, разряд по экспоненте
    u = np.zeros_like(t); v = 0
    for i, x in enumerate(half):
        v = max(x, v * np.exp(-(t[1] - t[0]) / 1.2)); u[i] = v
    fig, axs = plt.subplots(1, 2, figsize=(10, 3))
    axs[0].plot(t, half, c='k', lw=1.5, label='без $C_1$ (пульсирует)'); axs[0].plot(t, u, c=P, lw=2, label='с $C_1$ (сглажено)')
    axs[0].legend(frameon=False, fontsize=9, loc='lower right'); ax_clean(axs[0], 't', '$U_н$'); axs[0].set_title('выпрямитель: до и после конденсатора')
    f = np.logspace(0, 3, 300)
    axs[1].semilogx(f, 1 / np.sqrt(1 + (f / 8) ** 2), c=P, lw=2); axs[1].axvline(50, ls='--', c=GR)
    axs[1].text(52, 0.6, '50 Гц', color=GR); ax_clean(axs[1], 'f', '$U_н$ (переменная составл.)')
    axs[1].set_title('на 50 Гц переменная составляющая мала')
    save(fig, 'g10_rectifier')


def g_timer():
    t = np.linspace(0, 5, 400)
    fig, axs = plt.subplots(1, 3, figsize=(12, 3))
    ax = axs[0]; u = 1 - np.exp(-t / 1.2)
    ax.plot(t, u, c=B, lw=2); ax.plot([1.0, 1.0, 0], [0, 1 - np.exp(-1 / 1.2), 1 - np.exp(-1 / 1.2)], ':', c='k')
    ax.text(1.05, 0.05, '$τ_{зад}$'); ax.text(-0.1, 0.57, '$U_{зад}$', ha='right'); ax_clean(ax, 't', '$U_C$'); ax.set_title('интервал при заряде')
    ax = axs[1]; u = np.exp(-t / 1.2)
    ax.plot(t, u, c=B, lw=2); ax.plot([1.0, 1.0, 0], [0, np.exp(-1 / 1.2), np.exp(-1 / 1.2)], ':', c='k')
    ax.text(1.05, 0.05, '$τ_{зад}$'); ax.text(-0.1, 0.43, '$U_{зад}$', ha='right'); ax_clean(ax, 't', '$U_C$'); ax.set_title('интервал при разряде')
    ax = axs[2]; ax.plot(t, t / 5, c=B, lw=2); ax.plot([2, 2, 0], [0, 0.4, 0.4], ':', c='k')
    ax.text(2.05, 0.03, 'τ'); ax.text(-0.1, 0.4, '$U_{оп}$', ha='right'); ax_clean(ax, 't', '$U_C$'); ax.set_title('рис.9: заряд $I_0$ до $U_{оп}$ → K срабатывает')
    save(fig, 'g11_timer')


def g_cap_regions():
    fig, ax = plt.subplots(figsize=(6, 3.6))
    f = np.linspace(0.12, 1, 300)
    ax.plot(f, 0.16 / f, c='#00838f', lw=2)
    ax.axhline(0.5, c='k', lw=1); ax.axhline(0.85, c='k', lw=1, xmax=0.1)
    ax.axvline(0.55, c='k', lw=1, ymax=0.5 / 1.6); ax.axvline(0.85, c='k', lw=1, ymax=0.25 / 1.6)
    ax.fill_between([0, 0.32], 0, 0.5, color=P, alpha=0.15)
    for (x, y, s) in ((0.15, 0.25, '1'), (0.45, 0.42, '2'), (0.05, 0.67, '3'), (0.05, 1.1, '4'), (0.66, 0.12, '5'), (0.9, 0.1, '6')):
        ax.text(x, y, s, fontsize=13, bbox=dict(boxstyle='circle', fc='white', ec='k'))
    ax.set_xlim(0, 1.0); ax.set_ylim(0, 1.6)
    ax.set_xticks([0.55, 0.85]); ax.set_xticklabels(['$f_{max}$', '$f_р$'])
    ax.set_yticks([0.5, 0.85]); ax.set_yticklabels(['$U_{ном}$', '$U_{пред}$'])
    ax.set_xlabel('f', loc='right')
    ax.set_title('рис.15: допустимая амплитуда\nпеременного напряжения на конденсаторе')
    save(fig, 'g12_cap_regions')


# ---------------- КОНТУР ----------------
def g_resonance():
    f = np.linspace(0.2, 3, 400)
    XL = f; XC = 1 / f
    fig, axs = plt.subplots(1, 3, figsize=(12, 3.1))
    axs[0].plot(f, XC, c=B, lw=2, label='$X_C=1/(2πfC)$'); axs[0].plot(f, XL, c=P, lw=2, label='$X_L=2πfL$')
    axs[0].axvline(1, ls=':', c='k'); axs[0].text(1.03, 3.2, '$f_р$'); axs[0].set_ylim(0, 4); axs[0].legend(frameon=False)
    ax_clean(axs[0], 'f', 'X'); axs[0].set_title('реактивные сопротивления')
    R = 0.15
    Iser = 1 / np.sqrt(R ** 2 + (XL - XC) ** 2)
    axs[1].plot(f, Iser / Iser.max(), c=B, lw=2); axs[1].axvline(1, ls=':', c='k')
    ax_clean(axs[1], 'f', '$I_к$'); axs[1].set_title('последовательный: max ТОКА на $f_0$')
    axs[2].plot(f, Iser / Iser.max(), c=P, lw=2); axs[2].axvline(1, ls=':', c='k')
    ax_clean(axs[2], 'f', '$U_к$'); axs[2].set_title('параллельный: max НАПРЯЖЕНИЯ на $f_0$')
    save(fig, 'g13_resonance')


def g_q():
    f = np.linspace(0.6, 1.4, 500)
    def curve(Q):
        return 1 / np.sqrt(1 + (Q * (f - 1 / f)) ** 2)
    fig, axs = plt.subplots(1, 2, figsize=(10, 3.2))
    c = curve(8)
    axs[0].plot(f, c, c=B, lw=2); axs[0].axhline(0.707, ls='--', c=P)
    idx = np.where(c >= 0.707)[0]; f1, f2 = f[idx[0]], f[idx[-1]]
    axs[0].annotate('', xy=(f2, 0.6), xytext=(f1, 0.6), arrowprops=dict(arrowstyle='<->', color=P))
    axs[0].text(1, 0.5, 'Δf', color=P, ha='center'); axs[0].text(0.6, 0.73, '0,7$U_0$ (−3 дБ)', color=P)
    axs[0].axvline(1, ls=':', c='k'); ax_clean(axs[0], 'f', '$U_к$'); axs[0].set_title('рис.26: Q = $f_0$/Δf')
    axs[1].plot(f, curve(8), c=P, lw=2, label='1 — без $R_к$ (Q велика)')
    axs[1].plot(f, 0.75 * curve(2), c=B, lw=2, label='2 — с шунтом $R_к$ (Q мала)')
    axs[1].legend(frameon=False, fontsize=9); ax_clean(axs[1], 'f', 'Z'); axs[1].set_title('рис.27: шунтирование «размывает» резонанс')
    save(fig, 'g14_q')


# ---------------- ТРАНСФОРМАТОР ----------------
def g_transformer():
    fig, axs = plt.subplots(1, 2, figsize=(10, 3.3))
    ax = axs[0]
    ax.plot([0, 1], [1.41, 1.0], c='k', lw=2)
    ax.set_xlim(0, 1.15); ax.set_ylim(0.95, 1.5)
    ax.set_xticks([0, 1]); ax.set_xticklabels(['0', '1']); ax.set_yticks([1.0, 1.41]); ax.set_yticklabels(['$U_{2m}/1{,}4$', '$U_{2m}$ (ХХ)'])
    ax.plot([0.4, 0.4, 0], [0.95, 1.41 - 0.41 * 0.4, 1.41 - 0.41 * 0.4], c=G)
    ax.text(0.42, 0.97, "$I'_{нт}$", color=G); ax.text(0.01, 1.26, '$U_{нт}$', color=G)
    ax.set_xlabel("$I'_н=I_н/I_{2ном}$", loc='right'); ax.set_ylabel('$U_н$', loc='top', rotation=0)
    ax.set_title('рис.7: нагрузочная прямая ($C_ф$ ≥ 200 мкФ)')
    ax = axs[1]
    I = np.linspace(0, 2, 10)
    ax.plot([0, 1], [34, 24], c='#00838f', lw=2, label='$I_{2ном}$ = 1 А')
    ax.plot([0, 2], [34, 24], c=P, lw=2, label='$I_{2ном}$ = 2 А')
    ax.axvline(0.5, ls='--', c=GR); ax.plot([0, 0.5], [29, 29], ':', c='#00838f'); ax.plot([0, 0.5], [31.5, 31.5], ':', c=P)
    ax.set_xlim(0, 2.1); ax.set_ylim(23, 35); ax.set_xlabel('$I_н$, А', loc='right'); ax.set_ylabel('$U_н$, В', loc='top', rotation=0)
    ax.set_yticks([24, 29, 31, 34]); ax.legend(frameon=False, fontsize=9)
    ax.set_title('рис.8: при 0,5 А → 29 В и ≈31 В')
    save(fig, 'g15_transformer_load')
    fig, ax = plt.subplots(figsize=(4.6, 3.0))
    x = np.linspace(0.05, 5, 400)
    ax.plot(x, 4 * x / (1 + x) ** 2, c=B, lw=2); ax.axvline(1, ls=':', c='k')
    ax.set_xticks([1]); ax.set_yticks([]); ax.set_xlabel('$R_н/R_г$', loc='right'); ax.set_ylabel('$P_н$', loc='top', rotation=0)
    ax.set_title('рис.10: $P_н$ max при $R_н=R_г$')
    save(fig, 'g15b_matching')


def g_phase_split():
    t = np.linspace(0, 1, 300)
    fig, axs = plt.subplots(1, 3, figsize=(10, 2.4), sharey=True)
    axs[0].plot(t, np.sin(2 * np.pi * t), c=G, lw=2); axs[0].set_title('$U_1$')
    axs[1].plot(t, np.sin(2 * np.pi * t), c=G, lw=2); axs[1].set_title('$U_{21}$ (относительно средней точки)')
    axs[2].plot(t, -np.sin(2 * np.pi * t), c=P, lw=2); axs[2].set_title('$U_{22}$ — в противофазе')
    for a in axs:
        a.axhline(0, c='k', lw=0.8); ax_clean(a, 't', '')
    save(fig, 'g16_phase_split')


# ---------------- ДИОДЫ ----------------
def g_diode_vac():
    fig, axs = plt.subplots(1, 2, figsize=(10, 3.4))
    ax = axs[0]
    u = np.linspace(0, 0.75, 400); i = 0.002 * (np.exp(u / 0.07) - 1); i = np.where(i > 1.2, np.nan, i)
    ax.plot(u, i, c=B, lw=2)
    ur = np.linspace(-1.5, 0, 200); ir = -0.02 * (1 - np.exp(ur / 0.05))
    ur2 = np.linspace(-1.62, -1.5, 30); ir2 = -0.02 - (ur2 + 1.5) ** 2 * 60
    ax.plot(ur, ir, c=B, lw=2); ax.plot(ur2, ir2, c=P, lw=2)
    ax.axhline(0, c='k', lw=0.8); ax.axvline(0, c='k', lw=0.8)
    ax.axvline(0.62, ls='--', c=P, lw=1); ax.text(0.5, -0.25, "$U'_{пр}$", color=P)
    ax.text(-1.6, 0.12, 'пробой', color=P); ax.text(-1.1, -0.15, '$I_{обр}$ мал', color=B)
    ax.set_ylim(-0.9, 1.25); ax_clean(ax, 'U', 'I'); ax.set_title('ВАХ диода: прямая и обратная ветви')
    ax = axs[1]
    u = np.linspace(0, 1.0, 200)
    y = 0.001 * (np.exp(u / 0.045) - 1); ax.plot(u, np.where(y > 1.2, np.nan, y), c=P, lw=2, label='Ge (германий)')
    y = 1e-5 * (np.exp(u / 0.06) - 1); ax.plot(u, np.where(y > 1.2, np.nan, y), c=G, lw=2, label='Si (кремний)')
    ax.legend(frameon=False); ax_clean(ax, '$U_{пр}$', '$I_{пр}$'); ax.set_title('рис.6: у кремния больше прямое напряжение')
    save(fig, 'g17_diode_vac')


def g_diode_temp():
    fig, axs = plt.subplots(1, 2, figsize=(10, 3.4))
    for ax, mat, shift, br in ((axs[0], 'Ge', 0.1, (-0.75, -0.55)), (axs[1], 'Si', 0.12, (-1.3, -1.6))):
        u = np.linspace(0, 1, 600)
        for s, c, lab in ((0, B, '+20 °C'), (shift, P, 'выше t°')):
            y = 1e-3 * (np.exp((u + s) / 0.07) - 1); ax.plot(u, np.where(y > 1.2, np.nan, y), c=c, lw=2, label=lab)
            b = br[0] if s == 0 else br[1]
            ur = np.linspace(b, 0, 100)
            ax.plot(ur, -0.03 * (1 - np.exp(ur / 0.05)) * (1 + s * 5), c=c, lw=2)
            ax.plot([b, b - 0.05], [-0.03 * (1 + s * 5), -0.9], c=c, lw=2)
        ax.axhline(0, c='k', lw=0.8); ax.axvline(0, c='k', lw=0.8); ax.set_ylim(-0.95, 1.25)
        ax.legend(frameon=False, fontsize=9, loc='upper left'); ax_clean(ax, 'U', 'I')
    axs[0].set_title('рис.3 Ge: t°↑ → пробой при меньшем $U_{обр}$')
    axs[1].set_title('рис.4 Si: t°↑ → пробой при большем $U_{обр}$')
    save(fig, 'g18_diode_temp')


def g_diode_dynamic():
    t = np.linspace(0, 4, 800)
    ug = np.where(t < 1, 1, -1)
    uvd = np.where(t < 1, 0.15, np.where(t < 1.9, 0.15 - 0.05 * (t - 1), -1))
    uvd = np.where((t >= 1.9) & (t < 2.4), 0.105 - 2.21 * (t - 1.9), uvd)
    uvd = np.clip(uvd, -1, 1)
    fig, axs = plt.subplots(2, 1, figsize=(6, 3.6), sharex=True)
    axs[0].plot(t, ug, c=G, lw=2); axs[0].axhline(0, c='k', lw=0.6); ax_clean(axs[0], '', '$U_г$')
    axs[1].plot(t, uvd, c=P, lw=2); axs[1].axhline(0, c='k', lw=0.6)
    axs[1].annotate('', xy=(2.4, 0.4), xytext=(1, 0.4), arrowprops=dict(arrowstyle='<->')); axs[1].text(1.6, 0.5, '$t_з$')
    ax_clean(axs[1], 't', '$U_{VD1}$')
    axs[0].set_title('рис.2 (Лекция 5, п.7): диод закрывается с задержкой $t_з$')
    save(fig, 'g19_diode_dynamic')


def g_diode_parallel():
    u = np.linspace(0, 1, 200)
    fig, ax = plt.subplots(figsize=(5, 3.2))
    ax.plot(u, np.clip(1e-3 * (np.exp(u / 0.1) - 1), 0, 10), c=B, lw=2, label='VD1')
    ax.plot(u, np.clip(1e-4 * (np.exp(u / 0.1) - 1), 0, 10), c=P, lw=2, label='VD2')
    ax.axvline(0.85, ls='--', c=GR)
    i1 = 1e-3 * (np.exp(0.85 / 0.1) - 1); i2 = 1e-4 * (np.exp(0.85 / 0.1) - 1)
    ax.plot([0, 0.85], [i1, i1], ':', c=B); ax.plot([0, 0.85], [i2, i2], ':', c=P)
    ax.text(-0.02, i1, '$I_1$', ha='right', color=B); ax.text(-0.02, i2, '$I_2$', ha='right', color=P); ax.text(0.86, 0.3, 'U')
    ax.set_ylim(0, 6); ax.legend(frameon=False); ax_clean(ax, '$U_{пр}$', '$I_{пр}$')
    ax.set_title('рис.3: одно U, но $I_1>I_2$ — разброс ВАХ')
    save(fig, 'g20_diode_parallel')


def g_hf_impulse():
    fig, axs = plt.subplots(1, 4, figsize=(15, 3))
    f = np.linspace(0, 3, 200)
    axs[0].plot(f, 1 / np.sqrt(1 + f ** 2), c=B, lw=2); axs[0].axhline(0.707, ls='--', c=P)
    axs[0].axvline(1, ls=':', c='k'); axs[0].text(1.03, 0.1, '$f_{max}$'); axs[0].text(2, 0.74, '0,7$I_0$', color=P)
    ax_clean(axs[0], 'f', '$I_{вып}$'); axs[0].set_title('ВЧ-диод: $f_{max}$ по 0,7$I_0$')
    t = np.linspace(0, 4, 400)
    u = np.where(t < 1, 0.1, 0.4 + 0.6 * np.exp(-(t - 1) / 0.8))
    axs[1].plot(t, u, c=B, lw=2); axs[1].axhline(0.4, ls='--', c=GR); axs[1].axhline(0.48, ls=':', c=P)
    tu = 1 + 0.8 * np.log(0.6 / 0.08)
    axs[1].annotate('', xy=(tu, 0.2), xytext=(1, 0.2), arrowprops=dict(arrowstyle='<->')); axs[1].text(2, 0.24, '$t_{уст}$')
    axs[1].text(3.1, 0.52, '1,2$U_{пр.уст}$', color=P, fontsize=9); axs[1].text(3.1, 0.33, '$U_{пр.уст}$', fontsize=9)
    ax_clean(axs[1], 't', '$U_{пр}$'); axs[1].set_title('рис.2: всплеск $U_{пр.имп}$ при включении')
    i = np.where(t < 1, 0.6, -1.0 * np.exp(-(t - 1) / 0.6) - 0.05)
    axs[2].plot(t, i, c=P, lw=2); axs[2].axhline(0, c='k', lw=0.6)
    axs[2].annotate('', xy=(3.0, 0.3), xytext=(1, 0.3), arrowprops=dict(arrowstyle='<->')); axs[2].text(1.8, 0.37, '$t_{восст}$')
    axs[2].text(1.05, -1.0, '$I_{обр.имп}$', color=P)
    ax_clean(axs[2], 't', 'I'); axs[2].set_title('рис.3: выброс обратного тока')
    i = np.where(t < 0.6, 0.8, np.where(t < 2.8, -0.8, -0.8 * np.exp(-(t - 2.8) / 0.08) - 0.05))
    axs[3].plot(t, i, c='#00838f', lw=2); axs[3].axhline(0, c='k', lw=0.6)
    axs[3].annotate('', xy=(2.8, 0.2), xytext=(0.6, 0.2), arrowprops=dict(arrowstyle='<->')); axs[3].text(1.5, 0.27, '$t_1$')
    axs[3].text(2.95, 0.27, '$t_2$'); ax_clean(axs[3], 't', 'I'); axs[3].set_title('ДНЗ: $t_1\\gg t_2$ — крутой фронт')
    save(fig, 'g21_hf_impulse')


def g_zener():
    fig, axs = plt.subplots(1, 3, figsize=(14, 3.4))
    ax = axs[0]
    I = np.linspace(0, 1, 100)
    ax.plot([-1, -1], [0, -1], c='#4fc3f7', lw=3, label='идеальный (и.х.)')
    ax.plot(-1 - 0.25 * I, -I, c=G, lw=2, label='реальный (р.х.)')
    ur = np.linspace(-1, 0, 100); ax.plot(ur, -0.04 * (1 - np.exp(ur / 0.1)), c=G, lw=2)
    ax.axhline(-0.15, ls='--', c=P, lw=1); ax.axhline(-0.85, ls='--', c=P, lw=1)
    ax.text(-0.95, -0.12, '$I_{ст\\,min}$', color=P); ax.text(-0.95, -0.82, '$I_{ст\\,max}$', color=P)
    ax.annotate('', xy=(-1.2, -0.85), xytext=(-1.0, -0.85), arrowprops=dict(arrowstyle='<->')); ax.text(-1.25, -0.97, '$ΔU_{ст}$')
    ax.annotate('', xy=(-0.6, -0.85), xytext=(-0.6, -0.15), arrowprops=dict(arrowstyle='<->')); ax.text(-0.55, -0.5, '$ΔI_{ст}$')
    ax.axhline(0, c='k', lw=0.8); ax.axvline(0, c='k', lw=0.8)
    ax.legend(frameon=False, fontsize=9, loc='lower right'); ax_clean(ax, '$U_{обр}$ (влево)', '$I_{обр}$ (вниз)')
    ax.set_title('рис.2: $R_д=ΔU_{ст}/ΔI_{ст}$')
    ax = axs[1]
    u = np.linspace(0, 3, 200)
    ax.plot(u, np.minimum(u, 1), c='#4fc3f7', lw=3, label='идеальный')
    ax.plot(u, np.where(u < 1, u, 1 + 0.12 * (u - 1)), c=G, lw=2, label='реальный')
    ax.axhline(1, ls='--', c=P, lw=1); ax.text(0.05, 1.05, '$U_{ст}$', color=P)
    ax.annotate('', xy=(2.8, 0.85), xytext=(1.1, 0.85), arrowprops=dict(arrowstyle='<->')); ax.text(1.8, 0.72, '$ΔU_{вх}$')
    ax.annotate('', xy=(2.9, 1.22), xytext=(2.9, 1.0), arrowprops=dict(arrowstyle='<->')); ax.text(2.6, 1.3, '$ΔU_н$')
    ax.set_ylim(0, 1.5); ax.legend(frameon=False, fontsize=9, loc='lower right'); ax_clean(ax, '$U_{вх}$', '$U_н$')
    ax.set_title('рис.4: $K_{ст}≈ΔU_{вх}/ΔU_н$')
    ax = axs[2]
    t = np.linspace(0, 1, 400); rng = np.random.default_rng(3)
    ax.plot(t, 1 + 0.06 * rng.standard_normal(400), c=P, lw=1); ax.axhline(1, ls='--', c=GR)
    ax.set_ylim(0, 1.4); ax_clean(ax, 't', '$U_{ст}$'); ax.set_title('рис.5: $I_{ст}<I_{ст\\,min}$ → шум')
    save(fig, 'g22_zener')


def g_varicap():
    U = np.linspace(0, 30, 300); phi = 0.6
    fig, ax = plt.subplots(figsize=(5.2, 3.2))
    for n, c in ((2, B), (3, P)):
        ax.plot(U, (phi / (phi + U)) ** (1 / n), c=c, lw=2, label=f'n = {n}')
    ax.legend(frameon=False); ax.set_xlabel('$U_{см}=U_{обр}$, В', loc='right'); ax.set_ylabel('$C/C_0$', loc='top', rotation=0)
    ax.set_title('$C=C_0\\,(φ_к/(φ_к+U_{см}))^{1/n}$ (форма кривой)')
    save(fig, 'g23_varicap')


def g_limiters():
    t = np.linspace(0, 1, 500); x = 3 * np.sin(2 * np.pi * t); up = 0.7
    cases = {
        'a': (np.maximum(x, -up), '$-U_{пр}$', [(-up, '$-U_{пр}$')]),
        'b': (np.maximum(x, -(up + 1.0)), '', [(-(up + 1.0), '$-(U_{пр}+U_{оп})$')]),
        'v': (np.clip(x, -2 * up, 2 * up), '', [(2 * up, '$+2U_{пр}$'), (-2 * up, '$-2U_{пр}$')]),
        'g': (np.clip(x, -up, up), '', [(up, '$+U_{пр2}$'), (-up, '$-U_{пр1}$')]),
        'd': (np.clip(x, -up, 2.0), '', [(2.0, '$+U_{ст1}$'), (-up, '$-\\min(U_{пр1},U_{пр2})$')]),
    }
    for k, (y, _, lv) in cases.items():
        fig, ax = plt.subplots(figsize=(5.2, 2.5))
        ax.plot(t, x, ':', c=GR, lw=1.5, label='$U_{вх}$')
        ax.plot(t, y, c=P, lw=2, label='$U_{вых}$')
        for (lvl, s) in lv:
            ax.axhline(lvl, ls='--', c=B, lw=0.8); ax.text(1.01, lvl, s, color=B, va='center', fontsize=10)
        ax.axhline(0, c='k', lw=0.6); ax.legend(frameon=False, fontsize=9, loc='lower left', ncol=2)
        ax_clean(ax, 't', ''); ax.set_ylim(-3.3, 3.3)
        save(fig, f'g24{k}_lim')


# ---------------- ТРАНЗИСТОРЫ ----------------
def g_bjt_chars():
    fig, axs = plt.subplots(1, 3, figsize=(14, 3.4))
    u = np.linspace(0, 0.9, 200)
    for s, c, lab in ((0.06, P, 't > 20 °C'), (0, B, 't = 20 °C'), (-0.06, '#4fc3f7', 't < 20 °C')):
        y = 1e-3 * (np.exp((u + s) / 0.08) - 1); axs[0].plot(u, np.where(y > 25, np.nan, y), c=c, lw=2, label=lab)
    axs[0].legend(frameon=False, fontsize=9); axs[0].set_ylim(0, 25); ax_clean(axs[0], '$U_{бэ}$', '$I_б$')
    axs[0].set_title('рис.1: входная характеристика')
    v = np.linspace(0, 10, 300)
    for k, ib in enumerate((1, 2, 3, 4)):
        axs[1].plot(v, ib * (1 - np.exp(-v / 0.4)) * (1 + 0.02 * v), c=B, lw=2)
        axs[1].text(10.1, ib * 1.2, f'$I_{{б{ib}}}$', color=P)
    axs[1].axvline(8.5, c='#4fc3f7'); axs[1].text(8.6, 4.8, 'О.П.', color='#4fc3f7'); axs[1].text(3.5, 4.8, 'Р.О.', color='#4fc3f7')
    axs[1].axvspan(0, 0.8, color=P, alpha=0.1); axs[1].text(0.05, 0.3, 'нас.', color=P, fontsize=8)
    ax_clean(axs[1], '$U_{кэ}$', '$I_к$'); axs[1].set_ylim(0, 5.3); axs[1].set_title('рис.3: выходные характеристики')
    f = np.logspace(0, 3, 300)
    axs[2].loglog(f, 100 / np.sqrt(1 + (f / 10) ** 2), c=B, lw=2); axs[2].axhline(1, c='k', lw=0.8)
    axs[2].axvline(1000, ls=':', c='k'); axs[2].text(600, 1.3, '$f_{гр}$ (β=1)')
    axs[2].set_xticks([]); axs[2].set_yticks([]); axs[2].set_xlabel('f', loc='right'); axs[2].set_ylabel('β', loc='top', rotation=0)
    axs[2].set_title('β падает с ростом частоты')
    save(fig, 'g25_bjt_chars')


def g_soa():
    fig, axs = plt.subplots(1, 2, figsize=(10, 3.3))
    ax = axs[0]
    u = np.linspace(0.5, 10, 300)
    Ic = np.minimum(1, 3 / u)
    ax.fill_between(u, 0, Ic, color=G, alpha=0.15)
    ax.plot(u, Ic, c=G, lw=2); ax.plot([0, 0.5], [1, 1], c=G, lw=2); ax.plot([10, 10], [0, 0.3], c=G, lw=2)
    ax.plot(u, np.minimum(1, 5 / u), '--', c=GR); ax.text(6.5, 0.85, 'τ₂ (короче)', color=GR, fontsize=9)
    ax.text(3, 0.35, 'ОБР', fontsize=14); ax.text(0.1, 1.05, '$I_{к\\,max}$', color=P); ax.text(9, -0.12, '$U_{кэ\\,max}$', color=P)
    ax.text(4.2, 0.78, '$P=U_{кэ}I_к$', color=G)
    ax.set_ylim(-0.15, 1.25); ax_clean(ax, '$U_{кэ}$', '$I_к$'); ax.set_title('рис.1: область безопасной работы')
    ax = axs[1]
    t = np.linspace(0, 3, 600)
    ax.plot(t, ((t % 1) < 0.4).astype(float), c=B, lw=2)
    ax.annotate('', xy=(0.4, 1.1), xytext=(0, 1.1), arrowprops=dict(arrowstyle='<->')); ax.text(0.15, 1.15, 'τ')
    ax.annotate('', xy=(1, -0.15), xytext=(0, -0.15), arrowprops=dict(arrowstyle='<->')); ax.text(0.45, -0.32, 'T')
    ax.set_ylim(-0.4, 1.35); ax_clean(ax, 't', '$I_к$'); ax.set_title('рис.2: импульсный режим (T = const)')
    save(fig, 'g26_soa')


def g_fet():
    fig, axs = plt.subplots(1, 4, figsize=(16, 3.3))
    u = np.linspace(-3, 0, 100)
    axs[0].plot(u, (1 + u / 3) ** 2, c=B, lw=2, label='n-канал'); axs[0].plot(-u, (1 + u / 3) ** 2, c=P, lw=2, label='p-канал')
    axs[0].axvline(0, c='k', lw=0.8); axs[0].text(0.1, 1.02, '$I_{с\\,нач}$'); axs[0].text(-3, 0.05, '$U_{отс}$'); axs[0].text(2.4, 0.05, '$U_{отс}$')
    axs[0].legend(frameon=False, fontsize=9, loc='upper left'); ax_clean(axs[0], '$U_{зи}$', '$I_с$'); axs[0].set_title('рис.4 (ПТ с p-n): $I_с(U_{зи})$')
    v = np.linspace(0, 10, 300)
    for k, (lev, lab) in enumerate(((1, '$U_{зи}=0$'), (0.75, '$U_{зи1}$'), (0.5, '$U_{зи2}$'), (0.3, '$U_{зи3}$'), (0.15, '$U_{зи4}$'))):
        axs[1].plot(v, lev * (1 - np.exp(-v / 0.8)), c=B, lw=2); axs[1].text(10.1, lev, lab, color=P, fontsize=9, va='center')
    ax_clean(axs[1], '$U_{си}$', '$I_с$'); axs[1].set_title('рис.5: выходные характеристики')
    for k, (lev, lab, c) in enumerate(((1.3, '$U_{зи2}$', G), (1.1, '$U_{зи1}$', G), (0.85, '$U_{зи}=0$', P), (0.6, '$U_{зи1}<0$', '#4fc3f7'), (0.4, '$U_{зи2}<0$', '#4fc3f7'))):
        axs[2].plot(v, lev * (1 - np.exp(-v / 0.8)), c=c, lw=2); axs[2].text(10.1, lev, lab, color=c, fontsize=9, va='center')
    ax_clean(axs[2], '$U_{си}$', '$I_с$'); axs[2].set_title('МДП со встроенным каналом')
    for k, (lev, lab) in enumerate(((1.2, '$U_{зи4}$'), (0.9, '$U_{зи3}$'), (0.6, '$U_{зи2}$'), (0.3, '$U_{зи1}$'))):
        axs[3].plot(v, lev * (1 - np.exp(-v / 0.8)), c=P, lw=2); axs[3].text(10.1, lev, lab, color=P, fontsize=9, va='center')
    ax_clean(axs[3], '$U_{си}$', '$I_с$'); axs[3].set_title('МДП с индуцированным каналом')
    save(fig, 'g27_fet')


# ---------------- УСИЛИТЕЛИ ----------------
def transfer(u, thr=0.0):
    x = np.clip((u - thr) / 1.0, 0, None)
    return 1.2 * np.tanh(x ** 1.6)


def g_classes():
    cases = [
        ('g28_class_B', 'класс B (рис.18): $U_{бэ0}=0$, $I_{к0}=0$ — проходит полуволна', 0.0, 0.0, 0.9),
        ('g29_class_wrong', 'рис.19: точка O у насыщения — $I_{кm1}<I_{кm2}$, искажения', 0.0, 1.4, 0.55),
        ('g30_class_A', 'класс A (рис.20): O в середине линейного участка, $I_{кm1}≈I_{кm2}$', 0.0, 0.8, 0.45),
        ('g31_class_AB', 'класс AB (рис.22): небольшой $I_{к0}$, угол θ > 90°', 0.0, 0.25, 0.8),
        ('g32_class_C', 'класс C (рис.24): $I_{к0}=0$, θ < 90°', 0.4, 0.0, 0.9),
    ]
    t = np.linspace(0, 2, 600)
    for name, title, thr, u0, um in cases:
        fig, axs = plt.subplots(1, 2, figsize=(10, 3.2), gridspec_kw={'width_ratios': [1, 1.3]})
        u = np.linspace(-0.3, 2.2, 300)
        axs[0].plot(u, transfer(u, thr), c=P, lw=2)
        axs[0].plot([u0], [transfer(np.array([u0]), thr)[0]], 'o', c=P); axs[0].text(u0 + 0.05, transfer(np.array([u0]), thr)[0] + 0.08, 'O', color=P)
        axs[0].axvspan(u0 - um, u0 + um, color=B, alpha=0.1)
        ax_clean(axs[0], '$U_{бэ}$', '$I_к$'); axs[0].set_title('передаточная характеристика', fontsize=10)
        uin = u0 + um * np.sin(2 * np.pi * t)
        axs[1].plot(t, transfer(uin, thr), c=P, lw=2, label='$I_к(t)$')
        axs[1].plot(t, 0.25 * np.sin(2 * np.pi * t) - 0.45, c=B, lw=1.5, label='вход $E_г$ (масштаб)')
        axs[1].axhline(transfer(np.array([u0]), thr)[0], ls='--', c=GR, lw=0.8)
        axs[1].legend(frameon=False, fontsize=8, loc='upper right'); ax_clean(axs[1], 't', '')
        axs[1].set_ylim(-0.8, 1.45)
        fig.suptitle(title, fontsize=11, fontweight='bold')
        save(fig, name)
    # ключевой режим (рис.21)
    fig, axs = plt.subplots(1, 2, figsize=(10, 3))
    t = np.linspace(0, 2, 600); sq = (np.sin(2 * np.pi * t) > 0).astype(float)
    axs[0].plot(t, sq * 2 - 1, c=B, lw=2); ax_clean(axs[0], 't', '$U_{упр}$'); axs[0].set_title('управление — прямоугольник')
    axs[1].plot(t, sq, c=P, lw=2); ax_clean(axs[1], 't', '$I_к$'); axs[1].set_title('ток — «есть / нет»: транзистор = ключ')
    fig.suptitle('рис.21: ключевой режим', fontsize=11, fontweight='bold')
    save(fig, 'g33_class_key')


def g_amp_freq():
    f = np.logspace(0, 6, 400)
    fig, axs = plt.subplots(1, 3, figsize=(14, 3.2))
    K = 1 / np.sqrt(1 + (60 / f) ** 2) / np.sqrt(1 + (f / 2e5) ** 2)
    axs[0].semilogx(f, K, c=B, lw=2); axs[0].axhline(0.707, ls='--', c=P); axs[0].axhline(1, ls=':', c=GR)
    axs[0].axvline(60, ls=':', c='k'); axs[0].axvline(2e5, ls=':', c='k'); axs[0].text(65, 0.1, '$f_н$'); axs[0].text(2.1e5, 0.1, '$f_в$')
    axs[0].text(2, 0.73, '0,707', color=P); ax_clean(axs[0], 'f', 'K'); axs[0].set_title('рис.5: полоса $f_н … f_в$ (−3 дБ)')
    axs[1].semilogx(f, 1 / np.sqrt(1 + (f / 1e4) ** 2), c=B, lw=2); ax_clean(axs[1], 'f', 'K'); axs[1].set_title('рис.7: усилитель с полосой от 0')
    axs[2].semilogx(f, 1 / np.sqrt(1 + (8 * (f / 1e3 - 1e3 / f)) ** 2), c=B, lw=2); axs[2].axvline(1e3, ls=':', c=P)
    axs[2].text(1.1e3, 0.1, '$f_0$', color=P); ax_clean(axs[2], 'f', 'K'); axs[2].set_title('рис.8: избирательный (резонансный)')
    save(fig, 'g34_amp_freq')


def g_amp_params():
    fig, axs = plt.subplots(1, 3, figsize=(14, 3.2))
    p = np.linspace(0, 1, 50)
    axs[0].plot(p, p, c=P, lw=2); axs[0].plot([0.6, 0.6, 0], [0, 0.6, 0.6], ':', c='k')
    axs[0].text(0.62, 0.03, '$P_{ном}$'); axs[0].text(0.01, 0.63, '$K_{г\\,зад}$'); ax_clean(axs[0], '$P_{вых}$', '$K_г$')
    axs[0].set_title('рис.13: $K_г=\\sqrt{U_2^2+U_3^2+…}/U_1$')
    u = np.linspace(0, 1, 200)
    y = np.where(u < 0.9, 0.08 + u, 0.98 + 0.02 * np.tanh((u - 0.9) * 5))
    axs[1].plot(u, y, c=P, lw=2); axs[1].axhline(0.08, ls=':', c=GR); axs[1].text(0.01, 0.12, '$U_ш$', color=GR)
    axs[1].axvline(0.05, ls=':', c='k'); axs[1].axvline(0.9, ls=':', c='k')
    axs[1].text(0.06, -0.08, '$U_{вх\\,min}$', fontsize=9); axs[1].text(0.78, -0.08, '$U_{вх\\,max}$', fontsize=9)
    ax_clean(axs[1], '$U_{вх}$', '$U_{вых}$'); axs[1].set_ylim(-0.12, 1.1); axs[1].set_title('рис.14: D = $U_{вх\\,max}/U_{вх\\,min}$')
    t = np.linspace(0, 6, 600)
    y = np.where(t < 0.5, 0, np.where(t < 1.5, (t - 0.5), 1.0 * np.exp(-(t - 1.5) / 6)))
    axs[2].plot(t, y, c=P, lw=2); axs[2].axhline(0.1, ls=':', c=GR); axs[2].axhline(0.9, ls=':', c=GR)
    axs[2].text(5.2, 0.12, '0,1$U_m$', fontsize=9); axs[2].text(5.2, 0.92, '0,9$U_m$', fontsize=9)
    axs[2].annotate('', xy=(1.4, -0.08), xytext=(0.5, -0.08), arrowprops=dict(arrowstyle='<->')); axs[2].text(0.8, -0.22, '$t_н$')
    axs[2].annotate('', xy=(5.0, 0.6), xytext=(1.5, 0.6), arrowprops=dict(arrowstyle='<->')); axs[2].text(3, 0.65, '$t_{сп}$')
    ax_clean(axs[2], 't', '$U_{вых}$'); axs[2].set_ylim(-0.3, 1.15); axs[2].set_title('рис.15: переходная хар-ка (вход — скачок)')
    save(fig, 'g35_amp_params')


def g_temp_shift():
    u = np.linspace(0, 2, 300)
    fig, ax = plt.subplots(figsize=(5.4, 3.4))
    for s, c, lab in ((0.25, P, 't > +20 °C'), (0, 'k', 't = +20 °C'), (-0.25, '#4fc3f7', 't < +20 °C')):
        ax.plot(u, transfer(u + s, 0.2), c=c, lw=2, label=lab)
    ax.axvline(1.0, ls='--', c=GR)
    for s, c in ((0.25, P), (0, 'k'), (-0.25, '#4fc3f7')):
        y = transfer(np.array([1.0 + s]), 0.2)[0]; ax.plot([0, 1], [y, y], ':', c=c); ax.plot([1], [y], 'o', c=c)
    ax.legend(frameon=False, fontsize=9, loc='lower right'); ax_clean(ax, '$U_{бэ}$ (фиксировано)', '$I_к$')
    ax.set_title('рис.36: при том же $U_{бэ0}$ ток покоя «уплывает»')
    save(fig, 'g36_temp_shift')


def g_ce_waveforms():
    t = np.linspace(0, 1, 300); s = np.sin(2 * np.pi * t)
    fig, axs = plt.subplots(5, 1, figsize=(5.5, 6.4), sharex=True)
    for ax, y, lab, c in zip(axs, (s, s, s, 0.6 * s, -s), ('$E_г$', '$R_{кэ}$', '$U_{кэ}$', '$U_{Cр}$', '$U_н$'), ('#8e24aa',) * 4 + (P,)):
        ax.plot(t, y, c=c, lw=2); ax.axhline(0, c='k', lw=0.6); ax.set_ylabel(lab, rotation=0, labelpad=18); ax.set_yticks([]); ax.set_xticks([])
    axs[0].set_title('рис.30 (как на слайде): $U_н$ — в противофазе с $E_г$')
    save(fig, 'g37_ce_waveforms')


def g_fb_freq():
    f = np.logspace(0, 6, 400)
    fig, axs = plt.subplots(1, 2, figsize=(10, 3.1))
    axs[0].semilogx(f, 4 / np.sqrt(1 + (300 / f) ** 2) / np.sqrt(1 + (f / 3e4) ** 2), c=P, lw=2, label='β = 0 (без ОС)')
    axs[0].semilogx(f, 1.2 / np.sqrt(1 + (30 / f) ** 2) / np.sqrt(1 + (f / 3e5) ** 2), c=B, lw=2, label='β > 0 (ООС)')
    axs[0].legend(frameon=False); ax_clean(axs[0], 'f', '$U_{вых}$'); axs[0].set_title('рис.51: ООС — усиление ниже, полоса шире')
    f2 = np.linspace(0.2, 10, 200)
    axs[1].plot(f2, 1 / f2, c='k', lw=2); ax_clean(axs[1], 'f', '$X_{Cэ}$'); axs[1].set_title('рис.53: $X_{Cэ}$ мало на рабочих частотах')
    save(fig, 'g38_fb_freq')


def g_lf_hf():
    f = np.logspace(0, 6, 400)
    fig, axs = plt.subplots(1, 2, figsize=(10, 3))
    axs[0].semilogx(f, 1 / np.sqrt(1 + (100 / f) ** 2), c='#8e24aa', lw=2); ax_clean(axs[0], 'f', '$U_{нm}$')
    axs[0].set_title('рис.31: на НЧ мешают $C_ф$ (их $X_C$ растёт)')
    axs[1].semilogx(f, 1 / np.sqrt(1 + (f / 1e5) ** 2), c='#8e24aa', lw=2); ax_clean(axs[1], 'f', '$U_{кm}$')
    axs[1].set_title('рис.32: на ВЧ шунтируют $C_{бэ}$ и $C_п$')
    save(fig, 'g39_lf_hf')


def g_pushpull():
    t = np.linspace(0, 2, 800); s = np.sin(2 * np.pi * t)
    dz = 0.25
    pos = np.clip(s - dz, 0, None); neg = np.clip(s + dz, None, 0)
    fig, axs = plt.subplots(1, 2, figsize=(10, 3))
    axs[0].plot(t, np.clip(s, 0, None), c=B, lw=2, label='ветвь 1 (+)'); axs[0].plot(t, np.clip(s, None, 0), c=P, lw=2, label='ветвь 2 (−)')
    axs[0].legend(frameon=False, fontsize=9); axs[0].axhline(0, c='k', lw=0.6); ax_clean(axs[0], 't', ''); axs[0].set_title('две ветви работают по очереди')
    axs[1].plot(t, s, ':', c=GR); axs[1].plot(t, pos + neg, c='k', lw=2)
    axs[1].axhline(0, c='k', lw=0.6); ax_clean(axs[1], 't', '$U_н$'); axs[1].set_title('класс B: «ступенька» около нуля (конспект)')
    save(fig, 'g40_pushpull')


def g_inrush():
    t = np.linspace(0, 1, 300)
    fig, ax = plt.subplots(figsize=(5, 2.8))
    ax.plot(t, np.where(t < 0.1, 0, 0.25 + 0.75 * np.exp(-(t - 0.1) / 0.08)), c=P, lw=2)
    ax.axvline(0.1, ls=':', c='k'); ax.text(0.11, 0.05, '$t_{вкл}$')
    ax_clean(ax, 't', '$I_{пр}$'); ax.set_title('Л5, п.5 (рис.5): бросок тока при включении')
    save(fig, 'g41_inrush')


if __name__ == '__main__':
    for fn in (g_vectors, g_source, g_sine, g_offset_harm, g_pot, g_varistor, g_cap_charge, g_coupling, g_filters,
               g_rectifier, g_timer, g_cap_regions, g_resonance, g_q, g_transformer, g_phase_split, g_diode_vac,
               g_diode_temp, g_diode_dynamic, g_diode_parallel, g_hf_impulse, g_zener, g_varicap, g_limiters,
               g_bjt_chars, g_soa, g_fet, g_classes, g_amp_freq, g_amp_params, g_temp_shift, g_ce_waveforms,
               g_fb_freq, g_lf_hf, g_pushpull, g_inrush):
        try:
            fn()
        except Exception as ex:
            import traceback; traceback.print_exc()
