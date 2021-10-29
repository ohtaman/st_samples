import pandas as pd
import pydeck as pdk
import streamlit as st
import mapbox


def geocoding(address):
    """
    ジオコーディング（住所からの座標検索）を行う

    Arguments:
        address {str} -- 住所

    Returns:
        list -- (緯度, 経度)
    """
    api = mapbox.Geocoder()
    res = api.forward(address)
    return res.geojson()['features'][0]['geometry']['coordinates']


def get_path(origin, dest):
    """
    MapBox APIを用いてルート探索を行う

    Arguments:
        origin {list} -- 出発地の緯度経度
        dest {list} -- 到着地の緯度経度

    Returns:
        list -- ルート探索結果
    """
    api = mapbox.Directions()
    res = api.directions([{
        'type': 'Feature',
        'geometry': {
            'type': 'Point',
            'coordinates': origin
        }
    }, {
        'type': 'Feature',
        'geometry': {
            'type': 'Point',
            'coordinates': dest
        }
    }])
    return res.geojson()['features'][0]['geometry']['coordinates']


def main():
    with st.sidebar:
        with st.form(key='input'):
            origin_address = st.text_input('From:', '白金台')
            dest_address = st.text_input('To:', '世田谷')
            run = st.form_submit_button('Run')

    st.markdown('# MapBox を用いたルート探索')
    
    if run:
        origin = geocoding(origin_address)
        dest = geocoding(dest_address)
        coordinates = get_path(origin, dest)
        path = pd.DataFrame([{
            'coordinates': coordinates
            }]
        )
        view_state = pdk.ViewState(
            longitude=origin[0],
            latitude=origin[1],
            zoom=11
        )
        
        path_layer = pdk.Layer(
            type='PathLayer',
            data=path,
            get_color=(255, 0, 0),
            width_scale=2,
            width_min_pixels=2,
            get_width=5,
            get_path='coordinates'
        )

        deck = pdk.Deck(
            layers=[path_layer],
            initial_view_state=view_state,
            map_style='road',
            tooltip={'text': '{name}'}
        )

        st.pydeck_chart(deck)


if __name__ == '__main__':
    main()
