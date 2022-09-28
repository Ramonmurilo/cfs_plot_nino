import requests
import pendulum
from pathlib import Path
import os
import sys
import utils

"""
Caso não exista a pasta 'downloads', ela é criada ao chamar este módulo
"""
#caminho_base = ""#utils.dir_abs
diretorio_saida = Path(f'cfs_clima_91_20_daily/')
diretorio_saida.mkdir(exist_ok=True, parents=True)


def auxiliar_download(url_base:str, data_requerida:pendulum.datetime, nome_arquivo:str) -> bool:
    """ Subfunção de download(). Não é chamada diretamente.
    Faz a requisição do dado de TSM no repositório da NOAA.
    Args:
        url_base (str): Parte imutável do link de endereço.
        data_requerida (pendulum.datetime): data do dado procurado.
        nome_arquivo (str): [description] Nome do arquivo a ser requisitado.
    Returns:
        bool: True = dado baixado, False= erro 404 | arquivo não disponível.
    """

    url=f'{url_base}/{data_requerida.format("YYYYMM")}/{nome_arquivo}'
    resp=requests.get(url)

    if resp.status_code == 200:
        resp=requests.get(url).content
        diretorio = Path(diretorio_saida, nome_arquivo)

        with open(diretorio, "wb") as arquivo_:
            arquivo_.write(resp)
            print(f"{nome_arquivo} [ok]")
            mensagem_de_sucesso = True

    elif resp.status_code == 404:
        print(f'Erro 404. {nome_arquivo} ainda não disponível')
        mensagem_de_sucesso = False

    return mensagem_de_sucesso


def download(data_string:str=None, hoje:bool=False) -> str:
    """Chama a função de download dos dados de temperatura oceânica do NOAA.
    Caso o dado final não esteja pronto, baixa o preliminar.
    Args:
        data_string (str, optional): [DD-MM-YYYY] data do dado procurado. Defaults to None.
        hoje (bool, optional): Habilita o dia atual na hora da execução. Sobrescreve o data_string. Defaults to False.
    Returns:
        str: Nome do arquivo baixado
    """

    data_requerida = pendulum.now('America/Sao_Paulo') if hoje else pendulum.from_format(data_string, 'DD-MM-YYYY')
    url_base = 'https://www.ncei.noaa.gov/data/sea-surface-temperature-optimum-interpolation/v2.1/access/avhrr'

    nome_arquivo = f'oisst-avhrr-v02r01.{data_requerida.format("YYYYMMDD")}.nc'
    sucesso = auxiliar_download(url_base, data_requerida, nome_arquivo)

    if sucesso:
        tipo = "consistido"
        return nome_arquivo, tipo
    else :
        nome_arquivo = f'oisst-avhrr-v02r01.{data_requerida.format("YYYYMMDD")}_preliminary.nc'
        sucesso = auxiliar_download(url_base, data_requerida, nome_arquivo)
        
        if sucesso:
            tipo = "preliminar"
            return nome_arquivo, tipo
        else:
            sys.exit('A data solicitada ainda não possui dados')