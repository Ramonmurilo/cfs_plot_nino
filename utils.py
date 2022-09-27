import xarray as xr
from typing import Any


def padronizar_longitude(ds: xr.Dataset, xdim: str = "lon") -> xr.Dataset:
    """
    Padroniza a longitude de um dataset de -180 a 180.
    Parameters
    ----------
    ds : xr.Dataset
        Dataset da rodada.
    xdim : str, optional
        Nome da dimensão longitudinal no Dataset, by default "lon".
    Returns
    -------
    xr.Dataset
        Dataset com a longitude padronizada.
    """
    lon_con = ((ds[xdim] + 180) % 360) - 180
    ds_padronizado = ds.assign_coords({xdim: lon_con}).sortby(xdim)
    return ds_padronizado


def delimitar_regiao(obj: xr.DataArray, indice: Any) -> xr.DataArray:
    """
    Delimitação de regiões do oceano Atlântico e seu valor médio na região.
    Para um dado índice.
    Parameters
    ----------
    obj : xr.DataArray
        Dados da rodada do modelo
    indice : Any
        Informações sobre o índice vindos do módulo schema.nino
    Returns
    -------
    xr.DataArray
        Série com as temperaturas previstas.
    """
    try:
        rec = obj.sel(
            lat=slice(indice.latitude[0], indice.latitude[1]),
            lon=slice(indice.longitude[0], indice.longitude[1]),
        ).mean(dim=["lat", "lon"])

    except:
        rec = obj.sel(
            latitude=slice(indice.latitude[0], indice.latitude[1]),
            longitude=slice(indice.longitude[0], indice.longitude[1]),
        ).mean(dim=["latitude", "longitude"])

    valor = rec.compute()

    return valor


def converter_para_celsius(dado: Any) -> Any:
    """
    Converte dados em unidade Kelvin para Celsius.
    Função com variável generalizada para permitir diversos tipos de dado de entrada.
    Parameters
    ----------
    dado : Any
        Dados em Kelvin a serem convertidos. Aceita [int, array, xr.Dataset].
    Returns
    -------
    Any
        Dados convertidos em celsius no respectivo tipo.
    """
    ds_celsius = dado - 273.15

    return ds_celsius