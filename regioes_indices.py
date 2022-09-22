"""Modelos de dados do DocumentDB."""

from pydantic import BaseModel


class Indices(BaseModel):
    """
    Schema de dados do índice Nino.
    """

    id: int
    latitude: tuple
    longitude: tuple
    nome: str


# delimitação das regiões Niño segundo:
# https://climatedataguide.ucar.edu/climate-data/nino-sst-indices-nino-12-3-34-4-oni-and-tni?qt-climatedatasetmaintabs=4#qt-climatedatasetmaintabs

# delimitação de região CBM segundo:
# https://www.scielo.br/j/rbmet/a/TmNk6J3bcqGC85hvgfPzkJj/?lang=pt

# Delimitação de região TNA e TSA segundo:
# https://agupubs.onlinelibrary.wiley.com/doi/full/10.1002/2015GL063184



regioes = [
    # Niño 1+2 (0-10S, 90W-80W)
    Indices(latitude=(0, -10), longitude=(-90, -80), nome="TSM Niño 1+2", id=12),
    # Niño 3 (5N-5S, 150W-90W)
    Indices(latitude=(5, -5), longitude=(-63, -48), nome="TSM Niño 3", id=3),
    # Niño 3.4 (5N-5S, 170W-120W)
    Indices(latitude=(5, -5), longitude=(-170, -120), nome="TSM Niño 3.4", id=34),
    # Niño 4 (5N-5S, 160E-150W)
    Indices(latitude=(5, -5), longitude=(-150, 160), nome="TSM Niño 4", id=4),
    # CBM (43ºS - 33ºS, 63ºW - 48ºW)
    Indices(latitude=(-33, -43), longitude=(-63, -48), nome="TSM CBM", id=5),
    # Atlântico tropical norte - TNA (5N-25N, 55W-15W)
    Indices(latitude=(25, 5), longitude=(-55, -15), nome="TSM TNA", id=6),
    # Atlântico tropical sul - TSA (20S-0,30W-10E)
    Indices(latitude=(0, -20), longitude=(-30,10), nome="TSM TSA", id=7),
]