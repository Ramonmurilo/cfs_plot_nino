import rioxarray
from shapely.geometry.geo import shape
from xarray.core import dataset
import sys

def preparar_para_recorte_grib(dataset:dataset, crs="epsg:4326", xdim="longitude", ydim="latitude") -> dataset:
    """Trata coordenadas e dados para recorte | funcional para arquivos grib somente.
    Args:
        dataset (dataset): Dataset com a variável de interesse selecionada.
        crs (str, optional): Projeção cartográfica. Defaults to "epsg:4326".
        xdim (str, optional): Nome da dimensão x. Defaults to "longitude".
        ydim (str, optional): Nome da dimensão y. Defaults to "latitude".
    Returns:
        dataset: DataSet pré-cortado
    """
    dataset = dataset.assign_coords(longitude=(((dataset.longitude + 180) % 360) - 180)).sortby(xdim)
    dataset = dataset.rio.set_spatial_dims(x_dim=xdim, y_dim=ydim) 
    dataset = dataset.rio.write_crs(crs)
    return dataset

def preparar_para_recorte_nc(dataset:dataset, crs="epsg:4326", xdim="lon", ydim="lat") -> dataset:
    """Trata coordenadas e dados para recorte | funcional para arquivos netcdf4 somente.
    Args:
        dataset (dataset): Dataset com a variável de interesse selecionada.
        crs (str, optional): Projeção cartográfica. Defaults to "epsg:4326".
        xdim (str, optional): Nome da dimensão x. Defaults to "lon".
        ydim (str, optional): Nome da dimensão y. Defaults to "lat".
    Returns:
        dataset: DataSet pré-cortado
    """
    dataset = dataset.assign_coords(lon=(((dataset.lon + 180) % 360) - 180)).sortby(xdim)
    dataset = dataset.rio.set_spatial_dims(x_dim=xdim, y_dim=ydim) 
    dataset = dataset.rio.write_crs(crs)
    return dataset


def main(dados: dataset, contorno_tipo:str='lon_lat',tipo:str='grib', dado_contorno:any=None, latitude=None, longitude=None) -> dataset:
    """Recorta dados de chuva com base em um shapefile de bacia ou coordenadas.
    Esta função foi criada para trabalhar com shapefiles disponibilizados por Lis Andrade 
    em seu repositório do LAMMOC | outros arquivos podem precisar de alterações no código.
    Args:
        dados (dataset): Arquivo com a variável já selecionada. Obs.: forneça já na unidade convertida, caso necessário.
        contorno_tipo (str): Se a base para recorte é par ordenado ou shapefile (recebe 'lat_lon' ou 'shapefile'). Defaults to 'lon_lat'
        tipo (str, optional): aceita 'grib' ou 'nc'. Defaults to 'grib'.
        dado_contorno (None): Contorno utilizado para recorte ou pares ordenados
        latitude (None): tupla com par latitude.
        longitude (None): tupla com par longitude.
    Returns:
        dataset: Dados recortados
    """
    if tipo == 'grib':
        dados_preparados = preparar_para_recorte_grib(dados)
    elif tipo == 'nc':
        dados_preparados = preparar_para_recorte_nc(dados)
    else:
        sys.exit('variável "tipo" incompatível. Selecione {grib ou nc}')
        
    if contorno_tipo == 'shapefile':
        try:
            dados_recortados = dados_preparados.rio.clip(dado_contorno, "epsg:4326")
        except:
            print('Erro no recorte comum. Aplicando opção all_touched=True')
            dados_recortados = dados_preparados.rio.clip(dado_contorno, "epsg:4326", all_touched=True)
    elif contorno_tipo == 'lat_lon':
        try:
            dados_recortados = dados_preparados.sel(longitude=slice(longitude[0], longitude[1]), latitude=slice(latitude[0], latitude[1]))
        except:
            dados_recortados = dados_preparados.sel(lon=slice(longitude[0], longitude[1]), lat=slice(latitude[0], latitude[1]))
    else:
        sys.exit('variável "contorno_tipo" incompatível. Selecione {lon_lat ou shapefile}')
        
    return dados_recortados