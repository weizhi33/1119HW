import solara
import ipyleaflet as leaflet

# 馬太鞍溪橋的精確坐標 (約 23.6891°N, 121.4089°E)
# 確保坐標點在馬太鞍濕地與光復鄉一帶
MATAAN_LAT = 23.69  # 緯度：北緯 23.69 度 (更精確)
MATAAN_LON = 121.41 # 經度：東經 121.41 度 (更精確)

# 調整縮放級別至 14，能更清楚顯示溪流細節
DEFAULT_ZOOM = 14 

def create_location_map():
    """創建一個 ipyleaflet 地圖，中心設定在馬太鞍溪附近。"""

    # 創建基礎地圖
    # 確保 center 參數是明確的 (緯度, 經度) tuple
    m = leaflet.Map(
        center=(MATAAN_LAT, MATAAN_LON), # 修正為更精確的坐標
        zoom=DEFAULT_ZOOM,              # 放大至 14
        scroll_wheel_zoom=True,
        layout={'height': '650px'}
    )

    # 添加底圖 (使用 OpenStreetMap 作為基礎)
    m.add_layer(leaflet.TileLayer(name="OpenStreetMap"))

    # 添加比例尺和圖層控制
    m.add_control(leaflet.ScaleControl(position="bottomleft"))
    m.add_control(leaflet.LayersControl(position="topright"))

    return m

# ⭐ Solara 頁面組件 ⭐
@solara.component
def Page():
    """Solara 頁面，用於展示基礎地理環境地圖。"""

    # 確保地圖元件只初始化一次
    map_widget = solara.use_memo(create_location_map, dependencies=[])

    with solara.Card(title="02. 馬太鞍溪地理環境概覽 (基礎地圖 - 修正版)", elevation=5):
        solara.Markdown("## 🌐 馬太鞍溪流域中心地圖")
        solara.Markdown(
            """
            此頁面僅展示馬太鞍溪事件周邊的基礎地理環境。地圖中心已設定在花蓮縣光復鄉一帶，
            您可以透過拖曳與縮放來查看詳細地形。
            """
        )
        # 將 ipyleaflet 地圖組件嵌入 Solara
        leaflet.Map.element(m=map_widget)