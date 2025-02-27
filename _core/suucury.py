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
from vitollino import Jogo, Cena, Elemento
from random import randint

FLORA = "https://i.imgur.com/n3GnL9B.png"
MATA0 = "https://i.imgur.com/TT2FKyu.jpeg"
TORA = "https://imgur.com/0jSB27g.png"
FX, FY = 5, 4
KX, KY = 6, 1
TREES = 300
LAYERS = 8
KIRI = "https://i.imgur.com/gPnv2KM.png"


class Lax:
    def __init__(self):
        def calc_parallax(x, y, item):
            conta_, lado_ = x - 1 if x > 1 else 1, y - 1 if y > 1 else 1
            dw, dh = (100 / conta_) * (item % x), (100 / lado_) * (item // x)
            return conta_, lado_, dw, dh

        self.calc = calc_parallax
        self.walk = self.right
        self.spriter, self.spritel = 3, 2
        self.c = Cena(MATA0)
        self.c.elt.style.overflow = "hidden"
        self.c.vai()
        self.layers = [Elemento(w=4000, h=700, cena=self.c) for _ in range(LAYERS)]  # [list()]*LAYERS
        self.scenery()
        self.kiri = Elemento(KIRI, w=130, h=250, x=600, y=400, cena=self.c)
        kr = self.sprite_kiri(self.spriter, Elemento(KIRI, w=25, h=50, x=1200, y=400, cena=self.c, vai=self.right))
        kl = self.sprite_kiri(self.spritel, Elemento(KIRI, w=25, h=50, x=50, y=400, cena=self.c, vai=self.left))
        self.k = self.sprite_kiri(self.spriter, self.kiri)

    def left(self, evento):
        evento.stopPropagation()
        evento.preventDefault()
        self.spritel = (self.spritel + 1) % 3
        self.move(40)
        self.k = self.sprite_kiri(self.spritel, self.kiri)

    def right(self, evento):
        evento.stopPropagation()
        evento.preventDefault()
        self.spriter = (self.spriter - 3 + 1) % 3 + 3
        self.move(-40)
        self.k = self.sprite_kiri(self.spriter, self.kiri)

    def move(self, val=40):
        def mover(lay, val_):
            lay.x = lay.x + val_
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

