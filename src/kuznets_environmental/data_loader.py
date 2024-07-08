import pandas as pd
from dbnomics import fetch_series

def load_gdp_percap():
    gdp_percap = fetch_series([
        'WB/WDI/A-NY.GDP.PCAP.KD-USA',
        'WB/WDI/A-NY.GDP.PCAP.KD-CHN',
        'WB/WDI/A-NY.GDP.PCAP.KD-GBR',
        'WB/WDI/A-NY.GDP.PCAP.KD-FRA',
        'WB/WDI/A-NY.GDP.PCAP.KD-RUS',
        'WB/WDI/A-NY.GDP.PCAP.KD-TUR',
        'WB/WDI/A-NY.GDP.PCAP.KD-SAU',
        'WB/WDI/A-NY.GDP.PCAP.KD-IND'
    ])
    
    columns_keep = ['original_period', 'value', 'country (label)']
    df_gdp = gdp_percap[columns_keep].rename(columns={'country (label)': 'country', 'value': 'gdp per capita'}).dropna()
    
    return df_gdp

def load_data_depletion():
    nature_depl = fetch_series([
        'WB/WDI/A-NY.ADJ.DRES.GN.ZS-USA',
        'WB/WDI/A-NY.ADJ.DRES.GN.ZS-CHN',
        'WB/WDI/A-NY.ADJ.DRES.GN.ZS-GBR',
        'WB/WDI/A-NY.ADJ.DRES.GN.ZS-FRA', 
        'WB/WDI/A-NY.ADJ.DRES.GN.ZS-RUS',
        'WB/WDI/A-NY.ADJ.DRES.GN.ZS-TUR',
        'WB/WDI/A-NY.ADJ.DRES.GN.ZS-SAU', 
        'WB/WDI/A-NY.ADJ.DRES.GN.ZS-IND'
    ])
    
    columns_keep = ['original_period', 'value', 'country (label)']
    df_depl = nature_depl[columns_keep].rename(columns={'country (label)': 'country', 'value': 'natural depletion'}).dropna()
    
    df_gdp = load_gdp_percap()

    return df_gdp, df_depl

def merge_country_depletion(dfs):
    df_gdp, df_depl = dfs
    countries = df_gdp['country'].unique()
    
    merged_dfs = {}
    for country in countries:
        country_dfs = [df[df['country'] == country] for df in dfs]
        merged_df = country_dfs[0]
        for df in country_dfs[1:]:
            merged_df = pd.merge(merged_df, df, on="original_period", how="left")
        merged_dfs[country] = merged_df
    
    return merged_dfs

def load_data_greenhouse():
    green_emission = fetch_series([
        'WB/WDI/A-EN.ATM.GHGT.KT.CE-USA',
        'WB/WDI/A-EN.ATM.GHGT.KT.CE-CHN',
        'WB/WDI/A-EN.ATM.GHGT.KT.CE-GBR',
        'WB/WDI/A-EN.ATM.GHGT.KT.CE-FRA', 
        'WB/WDI/A-EN.ATM.GHGT.KT.CE-RUS',
        'WB/WDI/A-EN.ATM.GHGT.KT.CE-TUR',
        'WB/WDI/A-EN.ATM.GHGT.KT.CE-SAU', 
        'WB/WDI/A-EN.ATM.GHGT.KT.CE-IND'
    ])
    
    columns_keep = ['original_period', 'value', 'country (label)']
    df_green = green_emission[columns_keep].rename(columns={'country (label)': 'country', 'value': 'greenhouse emission'}).dropna()
    
    df_gdp = load_gdp_percap()

    return df_gdp, df_green

def merge_country_greenhouse(newdfs):
    df_gdp, df_green = newdfs
    countries = df_gdp['country'].unique()
    
    merged_newdfs = {}
    for country in countries:
        country_newdfs = [newdf[newdf['country'] == country] for newdf in newdfs]
        merged_newdf = country_newdfs[0]
        for newdf in country_newdfs[1:]:
            merged_newdf = pd.merge(merged_newdf, newdf, on="original_period", how="left")
        merged_newdfs[country] = merged_newdf
    
    return merged_newdfs
