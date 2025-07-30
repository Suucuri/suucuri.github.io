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

|   **Open Source Notification:** This file is part of open source program **Suucurijuba**
|   **Copyright © 2025  Carlo Oliveira** <carlo@nce.ufrj.br>,
|   **SPDX-License-Identifier:** `GNU General Public License v3.0 or later <http:#is.gd/3Udt>`_.
|   `Labase <https:#labase.github.io/>`_ - `NCE <https:#portal.nce.ufrj.br>`_ - `UFRJ <https:#ufrj.br/>`_.
"""
from secrets import choice

from vitollino import Jogo, Cena, Elemento
from random import randint
from random import randint
FLORA = "https://i.imgur.com/n3GnL9B.png"
MATA0 = "https://i.imgur.com/TT2FKyu.jpeg"
TORA = "https://imgur.com/0jSB27g.png"
BALL = "https://i.imgur.com/rf8yRt0.png"
FX, FY = 5, 4
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


class Lax:
    def __init__(self):
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
        self.layers = [Elemento(w=4000, h=700, cena=self.c) for _ in range(LAYERS)]  # [list()]*LAYERS
        self.scenery()
        self.kiri = Elemento(KIRI, w=130, h=250, x=600, y=400, cena=self.c, vai=self.fire)
        self.mapu = Elemento(MAPU, w=130, h=250, x=1020, y=400, cena=self.c)
        self.mapu.img = TIMP
        self.mapu_h = None
        self.monster(fig=choice(MONS), x=choice((200, 1000)))
        self.ball = Elemento(BALL, w=4, h=4, x=680, y=500, cena=self.c, vai=self.fire)
        self.ball.elt.bind("transitionend", self.hexed)
        # self.ball.elt.style.display = "none"
        self.sp = sp = 0.5
        self.kiri_x = 0
        self.kiri_go = 1
        self.tr = f"width {sp}s, height {sp}s, left {sp}s, top {sp}s, opacity {sp}s, transform {sp}s, easy-in 0.5s"
        self.ball.elt.style.transition = self.tr
        kr = self.sprite_kiri(self.spriter, Elemento(KIRI, w=25, h=50, x=1200, y=400, cena=self.c, vai=self.right))
        kl = self.sprite_kiri(self.spritel, Elemento(KIRI, w=25, h=50, x=50, y=400, cena=self.c, vai=self.left))
        self.k = self.sprite_kiri(self.spriter, self.kiri)

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
        self.ball.y = 500
        self.ball.w = self.ball.h = 4
        self.monster(fig=choice(MONS), x=choice((200, 1000)), o=0.0) if self.mapu_h > 3 else None

    def fire(self, evento):
        evento.stopPropagation()
        evento.preventDefault()
        if self.is_calm:
            return
        self.ball.elt.style.transition = self.tr
        self.ball.elt.style.transform = "rotate(720deg)"
        self.ball.o = 1.0
        self.ball.w = self.ball.h = 180
        self.ball.x = 600 + self.kiri_go * 400
        # self.ball.x = 1000
        self.ball.y = 400

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

        _ = [lay.elt <= self.sprite(150 * item - 3000, 350, randint(0, 15), 1, layer)
         for layer, lay in enumerate(self.layers) for item in range(0, trees)]
        [off_lay(lay, layer) for layer, lay in enumerate(self.layers)]

    def sprite_kiri(self, item, e):
        """Near layer should be more spaced"""
        conta_, lado_, dw, dh = self.calc(KX, KY, item)
        bp = f"{dw:.2f}% {dh:.2f}%"
        e.elt.style.backgroundSize = f"{KX * 100}% {KY * 100}%"
        e.elt.style.backgroundPosition = bp
        return e.elt

    def sprite(self, x, y, item, layer, ly, elt=None):
        """Near layer should be more spaced"""
        item = randint(0, 14)
        layer_delta_y = 400 // LAYERS
        conta_, lado_, dw, dh = self.calc(FX, FY, item)
        bp = f"{dw:.2f}% {dh:.2f}%"
        size = TREES - layer * 30
        e = elt or Elemento(FLORA, w=size - 10, h=size, x=x, y=y - layer * layer_delta_y, cena=self.c)
        e.elt.style.backgroundSize = f"{FX * 100}% {FY * 100}%"
        e.elt.style.backgroundPosition = bp
        return e.elt


def main():
    Jogo(style=dict(height="650px", width="1300px"), did="app").z()
    Lax()

