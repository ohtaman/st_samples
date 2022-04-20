from collections import defaultdict
from dataclasses import dataclass
import datetime
import json
import math
import pathlib
from typing import Iterable

import pulp
import pandas as pd
import pydeck as pdk
import streamlit as st
from streamlit_sortables import sort_items


@dataclass
class Position:
    longitude: float
    latitude: float


@dataclass
class Node:
    name: str
    position: Position


@dataclass
class Edge:
    src: Node
    dest: Node
    cost: float
    steps: Iterable[Position]


@dataclass
class Color:
    red: int
    green: int
    blue: int

    def as_rgb_array(self):
        return (self.red, self.green, self.blue)


class Deck:
    ICON_DATA = {
        'url': 'https://raw.githubusercontent.com/ohtaman/st_samples/main/st_tsp/marker.png',
        'width': 128,
        'height': 128,
        'anchorY': 128,
    }

    def __init__(self):
        self.path_layers = []
        self.icon_layers = []

    def show(self, center: Position=None, zoom: int=None):
        view_state = pdk.ViewState(
            longitude=center.longitude,
            latitude=center.latitude,
            zoom=zoom
        )
        deck = pdk.Deck(
            layers=self.path_layers + self.icon_layers,
            initial_view_state=view_state,
            map_style='road',
            tooltip={'text': '{name}\nlat:{latitude}\nlon:{longitude}'},
        )
        st.pydeck_chart(deck)

    def add_path_layer(self, path: Iterable[Position], color: Color=None):
        if color is None:
            color = self.get_color(len(self.path_layers))

        df = pd.DataFrame()
        df['path'] = [[[position.longitude, position.latitude] for position in path]]

        self.path_layers.append(
            pdk.Layer(
                type='PathLayer',
                data=df,
                get_color=color.as_rgb_array(),
                width_scale=1,
                width_min_pixels=2,
                get_width=5,
                get_path='path',
            )
        )

    def add_icon_layer(self, nodes: Iterable[Node]):
        df = pd.DataFrame()
        df['name'] = [node.name for node in nodes]
        df['longitude'] = [node.position.longitude for node in nodes]
        df['latitude'] = [node.position.latitude for node in nodes]
        df['icon_data'] = df.index.map(lambda x: self.ICON_DATA)

        self.icon_layers.append(
            pdk.Layer(
                type="IconLayer",
                data=df,
                get_icon='icon_data',
                get_size=4,
                size_scale=15,
                get_position=['longitude', 'latitude'],
                pickable=True,
            )
        )

    def get_color(self, n:int) -> Color:
        r = int(255*n/13 + 0*(13 - n)/13)%255
        g = int(0*n/17 + 0*(17 - n)/17)%255
        b = int(0*n/19 + 255*(19 - n)/19)%255
        return Color(r, g, b)

    @staticmethod
    def get_center(nodes: Iterable[Node]) -> Position:
        longitudes = [node.position.longitude for node in nodes]
        latitudes = [node.position.latitude for node in nodes]

        return Position(
            longitude=(min(longitudes) + max(longitudes))/2,
            latitude=(min(latitudes) + max(latitudes))/2
        )


    @staticmethod
    def get_zoom(nodes: Iterable[Node]) -> int:
        longitudes = [node.position.longitude for node in nodes]
        latitudes = [node.position.latitude for node in nodes]

        center_latitude = (min(longitudes) + max(longitudes))/2
        diff_x = abs((max(longitudes) - min(longitudes))*math.cos(math.radians(center_latitude)))
        diff_y = max(latitudes) - min(latitudes)

        for zoom in range(20, -1, -1):
            degree_per_pixel = 360./2**zoom/256
            if diff_x/degree_per_pixel < 256 and diff_y/degree_per_pixel < 256:
                return zoom

        return zoom

@st.cache
def get_optimal_route(nodes: Iterable[Node], edges: Iterable[Node]) -> list[Node]:
    if len(nodes) <= 2:
        return nodes

    model = pulp.LpProblem(name='tsp')
    nodes = pd.Series(nodes)
    edges = pd.Series(edges)
    nodes.index = [node.name for node in nodes]


    # 1 if We use the edge from node i to node j.
    x = {(i, j): pulp.LpVariable(f'x_{i}_{j}', cat='Binary')
        for i in nodes.index for j in nodes.index if i != j
    }

    # potentials (order index) of the nodes
    p = {
        i:pulp.LpVariable(f'p_{i}', 0, len(nodes), cat='Integer')
        for i in nodes.index
    }

    # objectivve
    model.objective = pulp.lpSum(
        x[i, j]*edges[(i, j)].cost
        for i in nodes.index
        for j in nodes.index
        if i != j
    )

    # constraints
    for j in nodes.index:
        model += pulp.lpSum(x[i, j] for i in nodes.index if i != j) == 1

    for i in nodes.index:
        model += pulp.lpSum(x[i, j] for j in nodes.index if i != j) == 1

    for i in nodes.index:
        for j in nodes.index[1:]:
            if i == j:
                continue
            model += p[i] + 1 - (len(nodes) - 1)*(1 - x[i, j]) <= p[j]

    # solve
    status = model.solve()
    if status != 1:
        st.warning('Failed to get optimal solution.')
        return list(nodes.index)

    used_path = {k[0]:k[1] for k, v in x.items() if v.value() > 0}
    route = [nodes[0]]
    while True:
        next_node = nodes[used_path[route[-1].name]]
        if next_node == route[0]:
            break
        route.append(next_node)
    return route


def initialize_app():
    st.set_page_config(
        page_title='Traveling Salesman Problem',
        page_icon='🚗',
        layout='wide'
    )
    if 'routes' not in st.session_state:
        st.session_state['routes'] = defaultdict(dict)


@st.cache
def _read_csv(fname: str) -> pd.DataFrame:
    data_dir = pathlib.Path(__file__).parent.joinpath('data')
    return pd.read_csv(data_dir.joinpath(fname))

def load_data(cost_type: str='duration') -> tuple[pd.Series, pd.Series]:
    ward_offices = _read_csv('tokyo_ward_offices.csv')
    cost_and_path = _read_csv('distance_duration_and_steps.csv')

    nodes = ward_offices.apply(
        lambda x: Node(
            name=x['English Name'],
            position=Position(longitude=x['Longitude'], latitude=x['Latitude'])
        ),
        axis=1
    )
    nodes.index = nodes.map(lambda x: x.name)

    edges = cost_and_path.apply(
        lambda x: Edge(
            src=x['from'],
            dest=x['to'],
            cost=x[cost_type],
            steps=[Position(longitude=y[0], latitude=y[1]) for y in json.loads(x['steps'])]
        ),
        axis=1
    )
    edges.index = edges.map(lambda x: (x.src, x.dest))
    return nodes, edges


def select_nodes(nodes: Iterable[Node], default: bool=True) -> Iterable[Node]:
    selected = []
    with st.expander('訪問対象を選択'):
        col1, col2 = st.columns(2)
        # Select all
        if col1.button('全てを選択'):
            for node in nodes:
                st.session_state[f'select-{node.name}'] = True
        # Clear all
        if col2.button('全てを解除'):
            for node in nodes:
                if f'select-{node.name}' in st.session_state:
                    st.session_state[f'select-{node.name}'] = False
        # Select
        for node in nodes:
            if st.checkbox(node.name, key=f'select-{node.name}'):
                selected.append(node)
    return selected


def save_route(name: str, route: Iterable[Node]):
    key = '-'.join(sorted(node.name for node in route))
    st.session_state['routes'][key][name] = route


def list_saved_routes(nodes: Iterable[Node]) -> Iterable[Node]:
    key = '-'.join(sorted(node.name for node in nodes))
    return st.session_state['routes'][key]


def set_current_route(nodes: Iterable[Node]):
    st.session_state['current_route'] = nodes


def get_current_route() -> Iterable[Node]:
    return st.session_state.get('current_route', [])


def main():
    initialize_app()
    nodes, edges = load_data(cost_type='duration')

    with st.sidebar:
        st.markdown('### Step 1. 訪問対象の選択')
        selected_nodes = select_nodes(nodes)

        st.markdown('### Step 2. 初期ルートの設定')
        saved_routes = list_saved_routes(selected_nodes)
        strategy = st.radio(
            '初期ルートの設定手法',
            ['抽出順をそのまま利用', '数理最適化の結果を利用'] +  (['保存済みのルートから選択'] if len(saved_routes) > 0 else [])
        )
        if strategy == '抽出順をそのまま利用':
            route = selected_nodes
        if strategy == '数理最適化の結果を利用':
            route = get_optimal_route(selected_nodes, edges)
            set_current_route(route)
        elif strategy == '保存済みのルートから選択':
            route_name = st.selectbox(
                'ルートを選択',
                saved_routes.keys()
            )
            route = saved_routes[route_name]

        st.markdown('### Step 3. ルートの並べ替え')
        node_names = [node.name for node in route]
        node_names = sort_items(node_names, direction='vertical')
        route = [nodes[node_name] for node_name in node_names]

        with st.form('save_routee'):
                st.write('経路を保存する')
                route_name = st.text_input('経路名')
                if st.form_submit_button('保存'):
                    save_route(route_name, route)
                    st.experimental_rerun()

    # 可視化
    st.title('TSP')
    deck = Deck()
    total_cost = 0
    for i in range(len(route)):
        edge_key = (route[i].name, route[(i + 1)%len(route)].name)
        edge = edges[edge_key]
        total_cost += edge.cost
        deck.add_path_layer(edge.steps)
    st.write(f'Total Cost (訪問時間): {datetime.timedelta(seconds=int(total_cost))}')

    deck.add_icon_layer(selected_nodes)
    deck.show(center=Deck.get_center(nodes), zoom=Deck.get_zoom(nodes))


if __name__ == '__main__':
    main()