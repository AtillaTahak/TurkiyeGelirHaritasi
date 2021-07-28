import pandas as pd  # pip install pandas
import numpy as np  # pip install numpy
import plotly.express as px  # pip install plotly
import plotly.graph_objects as go  # pip install plotly
# pip install plotly | subplot'lar yapmak için kullanacağız
from plotly.subplots import make_subplots
import requests  # pip install requests
import json



df = pd.read_csv('Kitap1.csv')


response = requests.get(
    'https://gist.githubusercontent.com/mebaysan/9be56dd1ca5659c0ff7ea5e2b5cf6479/raw/6d7a77d8a2892bd59f401eb87bd82d7f48642a58/turkey-geojson.json')
# Gist üzerindeki raw dataya erişmek için adrese istek (get) atıyoruz

# dönen response içerisindeki json'u değişkene atıyoruz ki bu json bizim istediğimiz GeoJSON
geojson = response.json()
df.describe().T  # veri seti hakkında betimsel istatistikler
df.info()  # değişkenler hakkında bilgiler


df.dtypes  # değişkenlere ait veri tipleri
# Burada görüyoruz ki Nüfus tahminleri object olarak gözükmekte. Bunları integer olarak güncellemeliyiz
df.rename(columns={'İl': 'name' }, inplace=True)

df['Nüfus'] = df['Nüfus'].apply(lambda x: ''.join(x.split(',')))

df['Nüfus'] = pd.to_numeric(df['Nüfus'])


geoDict = {}
geojson['features'][0]['properties']  # ilk şehre ait geojson properties'i


for i in geojson['features']: geoDict[i['properties']['name']] = i['id']

df.loc[:, 'GeoID'] = 'Yok'
df.loc[df['name'] == 'Afyonkarahisar'] = df.loc[df['name']
                                                == 'Afyonkarahisar'].replace('Afyonkarahisar', 'Afyon')
df.loc[df['name'] == 'Elâzığ'] = df.loc[df['name']
                                        == 'Elâzığ'].replace('Elâzığ', 'Elazığ')
df.loc[df['name'] == 'Hakkâri'] = df.loc[df['name']
                                         == 'Hakkâri'].replace('Hakkâri', 'Hakkari')

df['GeoID'] = df['name'].apply(lambda x: geoDict[x])
fig = px.choropleth_mapbox(df,  # hangi veri seti
                           geojson=geojson,  # hangi geojson dosyası
                           locations='GeoID',  # geojson dosyasında id'e denk gelen, veri setindeki hangi değişken
                           color='Kişi başına yıllık gelir (USD)',  # hangi Değişkene göre renk paleti
                           color_continuous_scale="dense",  # hangi renk paleti
                           # renklendirme için min ve max değerler aralığı
                           range_color=(df['Kişi başına yıllık gelir (USD)'].min(),
                                        df['Kişi başına yıllık gelir (USD)'].max()),
                           # map başlangıç lat & lon
                           center={'lat': 38.7200, 'lon': 34.0000},
                           # labellar değişecek mi
                           labels={'Kişi başına yıllık gelir (USD)': 'Kişi başına yıllık gelir (USD)'},
                           mapbox_style="carto-positron",  # mapbox stil
                           zoom=4.8,  # yakınlık
                           opacity=0.5,  # opacity
                           custom_data=[df['name'],
                                        df['Kişi başına yıllık gelir (USD)'], df['Nüfus']]  # figure'e göndereceğimiz ekstra veriler
                           )

fig.update_layout(title='Türkiye Kişi başına yıllık gelir (USD)',  # figure başlığı
                  title_x=0.5  # Title'ın x eksenindeki pozisyonu
                  )
#  gönderdiğimiz customdata'nın ilk elemanı
hovertemp = '<i style="color:red;">Şehir Adı:</i> %{customdata[0]}<br>'
hovertemp += '<i>Şehir Nüfüs:</i> %{customdata[2]}<br>'
hovertemp += '<i>Kişi başına yıllık gelir (USD):</i> %{customdata[1]}<br>'
# figure üzerine gelince oluşturduğum stringi göster
fig.update_traces(hovertemplate=hovertemp)
fig.show()
 

