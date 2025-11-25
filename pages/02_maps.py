import solara
import ipyleaflet as leaflet
import pandas as pd
from IPython.display import display

# 馬太鞍溪周邊中心坐標 (花蓮縣光復鄉，接近濕地)
# 格式: (Lat, Lon)
MATAAN_CENTER = (23.48, 121.42)

# 模擬的關鍵地點數據 (地理系風格的標註)
KEY_LOCATIONS = [
    {"name": "事件核心沖刷區 (模擬)", "lat": 23.490, "lon": 121.425, "color": "red", "info": "河川改道與侵蝕最嚴重區域。"},
    {"name": "馬太鞍濕地入口", "lat": 23.467, "lon": 121.433, "color": "green", "info": "重要的生態保育區。"},
    {"name": "水文觀測站 (模擬)", "lat": 23.500, "lon": 121.415, "color": "blue", "info": "提供降雨量與水位數據。"},
]

def create_location_map():
    """創建並設定包含關鍵標記的 ipyleaflet 地圖。"""
    
    # 創建基礎地圖
    m = leaflet.Map(
        center=MATAAN_CENTER, 
        zoom=13, 
        scroll_wheel_zoom=True,
        layout={'height': '650px'}
    )
    
    # 添加底圖 (使用 OpenStreetMap 作為基礎)
    m.add_layer(leaflet.TileLayer(name="OpenStreetMap"))
    
    # 遍歷關鍵位置並添加標記 (Marker)
    for loc in KEY_LOCATIONS:
        # 創建彈出式視窗 (Popup) 內容
        popup_html = solara.HTML(tag="div", unsafe_innerHTML=f"<strong>{loc['name']}</strong><br>{loc['info']}")
        
        # 創建標記
        marker = leaflet.Marker(
            location=(loc['lat'], loc['lon']),
            draggable=False,
            icon=leaflet.Icon(icon_url=f'https://placehold.co/30x30/{loc["color"].replace("#", "")}/ffffff?text=P', icon_size=[30, 30])
        )
        
        # 將 Popup 綁定到 Marker
        marker.popup = leaflet.Popup(child=popup_html, close_button=False, auto_close=False, close_on_escape_key=True)
        
        m.add_layer(marker)
    
    # 添加比例尺和圖層控制
    m.add_control(leaflet.ScaleControl(position="bottomleft"))
    m.add_control(leaflet.LayersControl(position="topright"))
    
    return m

# ⭐ Solara 頁面組件 ⭐
@solara.component
def Page():
    """Solara 頁面，用於展示標記地點的地圖。"""
    
    # 創建地圖實例
    map_widget = solara.use_memo(create_location_map, dependencies=[])
    
    with solara.Card(title="02. 馬太鞍溪事件關鍵地點標註", elevation=5):
        solara.Markdown("## 📍 事件地理分析標註")
        solara.Markdown(
            """
            此地圖標註了馬太鞍溪事件周邊幾個重要的地理位置，包括模擬的沖刷區域中心、
            馬太鞍濕地及水文觀測站。點擊標記 (P 點) 可以查看該地點的簡要說明。
            """
        )

        # 將 ipyleaflet 地圖組件嵌入 Solara
        leaflet.Map.element(m=map_widget)
        
        solara.Markdown("---")

        solara.Markdown("### 標記清單")
        
        # 顯示標記點的數據表格
        df_locations = pd.DataFrame(KEY_LOCATIONS).drop(columns=['color'])
        solara.DataFrame(
            df_locations,
            scrollable=False,
            style={"maxWidth": "100%", "margin": "10px 0"}