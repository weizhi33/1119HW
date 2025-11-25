import solara
import ipyleaflet as leaflet
# 移除 pandas 導入，因為不再需要數據表格

# 馬太鞍溪周邊中心坐標 (花蓮縣光復鄉，接近濕地)
# ipyleaflet 標準格式: (緯度 Lat, 經度 Lon)
MATAAN_LAT = 23.48  # 緯度：北緯 23.48 度
MATAAN_LON = 121.42 # 經度：東經 121.42 度


def create_location_map():
    """創建一個最簡單的 ipyleaflet 地圖，中心設定在馬太鞍溪附近。"""
    
    # 創建基礎地圖
    m = leaflet.Map(
        # 確保以 (緯度, 經度) 順序傳入
        center=(MATAAN_LAT, MATAAN_LON), 
        zoom=13, # 設定合適的縮放級別
        scroll_wheel_zoom=True,
        layout={'height': '650px'}
    )
    
    # 添加底圖 (使用 OpenStreetMap 作為基礎)
    m.add_layer(leaflet.TileLayer(name="OpenStreetMap"))
    
    # 移除標記和 Popup 邏輯
    
    # 添加比例尺和圖層控制 (可選，但保留以便使用者查看坐標)
    m.add_control(leaflet.ScaleControl(position="bottomleft"))
    m.add_control(leaflet.LayersControl(position="topright"))
    
    return m

# ⭐ Solara 頁面組件 ⭐
@solara.component
def Page():
    """Solara 頁面，用於展示基礎地理環境地圖。"""
    
    # 創建地圖實例
    map_widget = solara.use_memo(create_location_map, dependencies=[])
    
    with solara.Card(title="02. 馬太鞍溪地理環境概覽 (基礎地圖)", elevation=5):
        solara.Markdown("## 🌐 馬太鞍溪流域中心地圖")
        solara.Markdown(
            """
            此頁面僅展示馬太鞍溪事件周邊的基礎地理環境。地圖中心已設定在花蓮縣光復鄉一帶，
            您可以透過拖曳與縮放來查看詳細地形。
            """
        )

        # 將 ipyleaflet 地圖組件嵌入 Solara
        leaflet.Map.element(m=map_widget)