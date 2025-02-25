""""Pique de avaliação da paralaxe para a plataforma Sucuri.

Classes neste módulo:
    - :py:class:`LAX` Spike to demonstrate a crude parallax mechanism.

.. codeauthor:: Carlo Oliveira <carlo@nce.ufrj.br>

Changelog
---------
.. versionadded::    25.02
   |br| Crude scenery creation (18).
   |br| key capture and paralax calculation (20).

|   **Open Source Notification:** This file is part of open source program **Suucurijuba**
|   **Copyright © 2025  Carlo Oliveira** <carlo@nce.ufrj.br>,
|   **SPDX-License-Identifier:** `GNU General Public License v3.0 or later <http:#is.gd/3Udt>`_.
|   `Labase <http:#labase.selfip.org/>`_ - `NCE <https:#portal.nce.ufrj.br>`_ - `UFRJ <https:#ufrj.br/>`_.
"""
from vitollino import Jogo, Cena, Elemento
def main():
    Jogo(style=dict(height="650px", width="1300px"), did="app").z()
    from random import randint
    FLORA = "https://i.imgur.com/n3GnL9B.png"
    MATA0 = "https://i.imgur.com/TT2FKyu.jpeg"
    Cena(MATA0).vai()

