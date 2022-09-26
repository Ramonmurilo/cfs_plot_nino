session = botree.session("us-east-1")
bucket = 'noaa-cfs-pds'

ciclo_base = '00'
resolucao_temporal = 'monthly_grib'
ciclos = ['00', '06', '12', '18']

dados = list()
for data in datas:
    for ciclo in ciclos:

        data_fmt = data.format('%Y%m%d')
        for membro in ['1']:
            prefixo = f"cfs.{data_fmt}/{ciclo}/{resolucao_temporal}_{membro.zfill(2)}/ocnf.{membro.zfill(2)}"

            dir_membro = Path(data_fmt, membro)
            dir_membro.mkdir(exist_ok=True, parents=True)

            arquivos_ocn = session.s3.bucket(bucket).list_objects(prefixo)


            diretorio_ciclo = dir_membro.joinpath(ciclo)
            diretorio_ciclo.mkdir(exist_ok=True, parents=True)
            arquivos_ja_baixados = list(diretorio_ciclo.glob("*grb2"))

            arquivos_da_rodada = list()
            for arquivo in arquivos_ocn:
                if arquivo.endswith(f'{ciclo}Z.grb2'):
                    arquivo_path = Path(arquivo)
                    arquivo_local = diretorio_ciclo.joinpath(arquivo_path.name)
                    if arquivo_local in arquivos_ja_baixados:
                        pass
                    else:
                        session.s3.bucket(bucket).download(arquivo, arquivo_local)
                    arquivos_da_rodada.append(arquivo_local)
            
            arquivos_locais = [diretorio_ciclo.joinpath(Path(arquivo).name) for arquivo in arquivos_da_rodada]
            ds = xr.open_mfdataset(
                arquivos_locais[:],
                engine='cfgrib',
                combine='nested',
                concat_dim='valid_time',
                backend_kwargs=dict(
                    filter_by_keys=dict(
                        typeOfLevel='surface', shortName='t'
                    )
                )
            )
                
            ds_padronizado = padronizar_longitude(ds)
            nino = delimitar_regiao2(obj=ds_padronizado, indice=ninos[3])
            #ds_celsius = converter_para_celsius(nino)
            nino_df = nino.to_dataframe()

            nino_df.drop(columns=['time', 'step', 'surface'], inplace=True)
            nino_df.rename(columns={'t': f"{data.format('%Y%m%d')}_{membro}_{ciclo}"}, inplace=True)

            n_passos = len(nino_df.index)
            passos = range(1, n_passos + 1, 1)
            meses_previstos = [data.add(months=passo).replace(day=1) for passo in passos]
            nino_df = nino_df.assign(data=meses_previstos)
            nino_df.set_index('data', inplace=True)
            
            dados.append(nino_df)

df_mensal = pd.concat(dados, axis=1)
datas_e_ciclos = df_mensal.columns
df_mensal = df_mensal.assign(mes=df_mensal.index.month)