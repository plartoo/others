import pandas as pd
import os
import sys

assert (len(sys.argv) == 2), "You must provide input file name"
fname= sys.argv[1]
fname_split = os.path.splitext(fname)
foutname = fname_split[0] + '_cleaned' + fname_split[1]

df = pd.read_csv(fname,encoding="ANSI",delimiter=";",skiprows=1,decimal=",")
df.rename(columns={'Unnamed: 63':'EUR','Unnamed: 64':'Anzhal','GRP.15':'HHF_20_59J'},inplace=True)
cols_to_use = ['Wirtschaftsbereich', 'Wirtschaftsbereich Code', 'Produktgruppe',
       'Produktgruppe Code', 'Produktfamilie', 'Produktfamilie Code', 'Firma',
       'Firma Code', 'Dachmarke', 'Dachmarke Code', 'Marke', 'Marke Code',
       'Haendlerkennzeichen', 'Haendlerkennzeichen Code', 'Produkt',
       'Produkt Code', 'Motiv', 'Motiv Code', 'Mediengattung',
       'Mediengattung Code', 'Mediengruppe', 'Mediengruppe Code',
       'Medienuntergruppe', 'Medienuntergruppe Code', 'Verlag/Vermarkter',
       'Verlag/Vermarkter Code', 'Werbetraeger', 'Werbetraeger Code',
       'Hauptwerbetraeger', 'Hauptwerbetraeger Code', 'Zusatz Werbeform',
       'Zusatz Werbeform Code', 'Werbeform', 'Werbeform Code',
       'Erscheinungsmodus', 'Erscheinungsmodus Code', 'Anzeigengroesse',
       'Anzeigenhoehe in mm', 'Heftumfang', 'Position der Anzeige', 'Seite',
       'Spottyp (GfK)', 'Spottyp (GfK) Code', 'Spotlaenge',
       'Spotanzahl im Block', 'Tandemkennzeichen',
       'Tandemkennzeichen Tandemkennzeichen Code', 'Werbeblock',
       'Werbeblocklaenge', 'Blockanfangszeit', 'Position im Block', 'Uhrzeit',
       'Tarifart', 'Umfeld vor', 'Umfeld nach', 'Anzahl Spalten', 'Standard',
       'Standard ZeitSchema Code', 'ACNielsen Gebiete', 'Bundesland',
       'Ortsgroesse', 'Verbundkennzeichen', 'Datum', 'EUR', 'Anzhal', 'GRP',
       'GRP.1', 'GRP.2', 'GRP.3', 'GRP.4', 'GRP.5', 'GRP.6', 'GRP.7', 'GRP.8',
       'GRP.9', 'GRP.10', 'GRP.11', 'GRP.12', 'GRP.13', 'GRP.14', 'HHF_20_59J',
       'GRP.16', 'GRP.17', 'GRP.18', 'GRP.19', 'GRP.20', 'GRP.21', 'GRP.22',
       'GRP.23', 'GRP.24']
# https://github.com/pandas-dev/pandas/issues/13159
df.to_csv(foutname, index=False, columns=cols_to_use, float_format='%.5f')
# we may get dtype warning. we can specify 'dtype' as such https://stackoverflow.com/a/27232309
