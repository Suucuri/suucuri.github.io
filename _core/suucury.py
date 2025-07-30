""""Pique de avaliação da paralaxe para a plataforma Sucuri.

Classes neste módulo:
    - :py:class:`LAX` Spike to demonstrate a crude parallax mechanism.

.. codeauthor:: Carlo Oliveira <carlo@nce.ufrj.br>

Changelog
---------
.. versionadded::    25.02
   |br| Crude scenery creation (18).
   |br| key capture and paralax calculation (20).
   |br| port code to Suucuri github (26).
.. versionadded::    25.07
   |br| Added Monsters (28).
   |br| Monster jinx (29).
   |br| Path and front vegetation (30).

|   **Open Source Notification:** This file is part of open source program **Suucurijuba**
|   **Copyright © 2025  Carlo Oliveira** <carlo@nce.ufrj.br>,
|   **SPDX-License-Identifier:** `GNU General Public License v3.0 or later <http:#is.gd/3Udt>`_.
|   `Labase <https:#labase.github.io/>`_ - `NCE <https:#portal.nce.ufrj.br>`_ - `UFRJ <https:#ufrj.br/>`_.
"""
from secrets import choice

from vitollino import Jogo, Cena, Elemento
from random import randint

FLORA = "../_media/flora.png"
RAST = "../_media/rasteira.png"
MATA0 = "https://i.imgur.com/TT2FKyu.jpeg"
TORA = "https://imgur.com/0jSB27g.png"
BALL = "https://i.imgur.com/rf8yRt0.png"
FX, FY = 5, 5
KX, KY = 6, 1
TREES = 300
LAYERS = 8
KIRI = "https://i.imgur.com/gPnv2KM.png"
MAPU = "../_media/mapinguariup.png"
MAPI = "../_media/mapinguari.png"
IMPT = "../_media/imptikuna.png"
TIMP = "../_media/ticunaimp.png"
CURU = "../_media/curupira.png"
MONS = [MAPU, IMPT, TIMP, MAPI, CURU, CURU]
RANG = 200
TOPO = 350


class Lax:
    def __init__(self):
        def calc_shrub(shrub):
            shrub.w, shrub.h, shrub.y, = 80, 60, 350

        def calc_parallax(x, y, item):
            conta_, lado_ = x - 1 if x > 1 else 1, y - 1 if y > 1 else 1
            dw, dh = (100 / conta_) * (item % x), (100 / lado_) * (item // x)
            return conta_, lado_, dw, dh

        self.calc = calc_parallax
        self.walk = self.right
        self.is_calm = True
        self.spriter, self.spritel = 3, 2
        self.c = Cena(MATA0)
        self.c.elt.style.overflow = "hidden"
        self.c.vai()
        self.sprites = []
        self.layers = [Elemento(w=4000, h=600, cena=self.c) for _ in range(LAYERS)]  # [list()]*LAYERS
        [ly.elt.style.setProperty("pointer-events", "none") for ly in self.layers]  # [list()]*LAYERS
        self.scenery()
        self.kiri = Elemento(KIRI, w=130, h=250, x=600, y=TOPO, cena=self.c, vai=self.fire)
        self.mapu = Elemento(MAPU, w=130, h=250, x=1020, y=TOPO, cena=self.c)
        self.mapu.img = TIMP
        self.mapu_h = None
        self.range = [600 + RANG * rg for rg in (-1, 1)]
        self.monster(fig=choice(MONS), x=choice(self.range))
        self.ball = Elemento(BALL, w=4, h=4, x=680, y=TOPO + 100, cena=self.c, vai=self.fire)
        self.ball.elt.bind("transitionend", self.hexed)
        # self.ball.elt.style.display = "none"
        self.sp = sp = 0.5
        self.kiri_x = 0
        self.kiri_go = 1
        self.tr = f"width {sp}s, height {sp}s, left {sp}s, top {sp}s, opacity {sp}s, transform {sp}s, easy-in 0.5s"
        self.ball.elt.style.transition = self.tr
        self.k = self.sprite_kiri(self.spriter, self.kiri)
        grass = self.layers[-1]
        solo = self.layers[-2]
        solo.img = "../_media/solo.jpg"
        solo.h = 50
        solo.y = 550
        solo.elt.style.backgroundRepeat = "repeat-x"
        solo.elt.style.backgroundSize = "100px"
        solo.elt.style.filter = "blur(0.03rem)"
        grass.entra(self.c)
        grass.y = 50
        grass.h = 450
        grass.x = 1000
        grass.w = 4000
        _ = [calc_shrub(shrub) for shrub in self.sprites[-1]]
        kr = self.sprite_kiri(self.spriter,
                              Elemento(KIRI, w=25, h=50, x=1200, y=TOPO - 150, cena=self.c, vai=self.right))
        kl = self.sprite_kiri(self.spritel, Elemento(KIRI, w=25, h=50, x=50, y=TOPO - 150, cena=self.c, vai=self.left))

    def monster(self, fig=None, x=None, o=0.0, calm=True):
        self.is_calm = calm
        if fig is not None:
            self.mapu.img = fig
        if x is not None:
            self.mapu.x = x
        self.mapu.o = o
        self.mapu_h = 1
        self.kiri_x = 0
        self.mapu.elt.style.filter = f"hue-rotate(0deg)"

    def hexed(self, evento):
        evento.stopPropagation()
        evento.preventDefault()
        if evento.propertyName != "left":
            print(evento.propertyName)
            return
        self.ball.elt.style.setProperty("transition", "none", "important")
        self.ball.elt.style.transform = "rotate(0deg)"
        self.mapu.elt.style.filter = f"hue-rotate({self.mapu_h * 40}deg)"
        self.mapu.o = 1.0 - (0.20 * self.mapu_h)
        self.mapu_h += 1
        self.ball.o = 0
        self.ball.x = 680
        self.ball.y = TOPO + 100
        self.ball.w = self.ball.h = 4
        self.monster(fig=choice(MONS), x=choice(self.range), o=0.0) if self.mapu_h > 3 else None

    def fire(self, evento):
        evento.stopPropagation()
        evento.preventDefault()
        if self.is_calm:
            return
        self.ball.elt.style.transition = self.tr
        self.ball.elt.style.transform = "rotate(720deg)"
        self.ball.o = 1.0
        self.ball.w = self.ball.h = 180
        self.ball.x = 600 + self.kiri_go * RANG
        # self.ball.x = 1000
        self.ball.y = TOPO

    def left(self, evento):
        evento.stopPropagation()
        evento.preventDefault()
        self.spritel = (self.spritel + 1) % 3
        self.kiri_go = -1
        self.move(40)
        self.k = self.sprite_kiri(self.spritel, self.kiri)

    def right(self, evento):
        evento.stopPropagation()
        evento.preventDefault()
        self.spriter = (self.spriter - 3 + 1) % 3 + 3
        self.kiri_go = 1
        self.move(-40)
        self.k = self.sprite_kiri(self.spriter, self.kiri)

    def move(self, val=40):
        def mover(lay, val_):
            lay.x = lay.x + val_

        print(self.layers[0].x)
        self.kiri_x += 1
        if self.kiri_x > 3:
            self.monster(o=1.0, calm=False)
        [mover(lay, val * (layer + 1)) for layer, lay in enumerate(self.layers)]

    def scenery(self, trees=32):
        def off_lay(layer, off):
            scale = 1.0 + off / 5.0
            layer.y = 150 + 100 * off - 300
            layer.x = layer.x + 65 * off
            layer.elt.style.scale = scale
            layer.elt.style.transition = "left 1s"

        last = len(self.layers) - 2
        self.sprites = [[self.sprite(
            150 * item - 3000, 350, randint(0, 15), 1, layer, FLORA if layer < last else RAST)
            for item in range(0, trees if layer < last else trees * 3)]
            for layer, lay in enumerate(self.layers)]
        _ = [lay.elt <= sprite.elt for lay, sprites in zip(self.layers, self.sprites) for sprite in sprites]
        [off_lay(lay, layer) for layer, lay in enumerate(self.layers)]

    def sprite_kiri(self, item, e):
        """Near layer should be more spaced"""
        conta_, lado_, dw, dh = self.calc(KX, KY, item)
        bp = f"{dw:.2f}% {dh:.2f}%"
        e.elt.style.backgroundSize = f"{KX * 100}% {KY * 100}%"
        e.elt.style.backgroundPosition = bp
        return e.elt

    def sprite(self, x, y, item, layer, ly, sheet=FLORA, elt=None):
        """Near layer should be more spaced"""
        item = randint(0, 25)
        layer_delta_y = 400 // LAYERS
        conta_, lado_, dw, dh = self.calc(FX, FY, item)
        bp = f"{dw:.2f}% {dh:.2f}%"
        size = TREES - layer * 30
        dx = 1 if sheet == FLORA else 3
        e = elt or Elemento(sheet, w=size - 10, h=size, x=x//dx, y=y - layer * layer_delta_y, cena=self.c)
        e.elt.style.backgroundSize = f"{FX * 100}% {FY * 100}%"
        e.elt.style.backgroundPosition = bp
        return e


def main():
    Jogo(style=dict(height="650px", width="1300px"), did="app").z()
    Lax()
