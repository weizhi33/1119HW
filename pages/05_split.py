import solara
import leafmap.leafmap as leafmap

# 馬太鞍溪周邊中心坐標 (花蓮縣光復鄉)
# ⚠️ 注意：此頁面使用 ipyleaflet 後端，座標順序為 [緯度 Lat, 經度 Lon]
# 這與 01, 02, 04 頁面的 [Lon, Lat] 相反
MATAAN_CENTER_LAT_LON = [23.48, 121.42]

def create_split_map():
    """
    創建一個帶有滑動卷簾 (Split Control) 的地圖。
    左側顯示衛星影像，右側顯示街道地圖。
    """
    # 建立分割地圖
    # leafmap.split_map 會自動建立一個帶有 split control 的地圖物件
    m = leafmap.split_map(
        left_layer="Esri.WorldImagery",  # 左側：衛星影像
        right_layer="OpenStreetMap",     # 右側：街道地圖
        left_label="衛星影像 (地貌)",
        right_label="街道地圖 (路網)",
        center=MATAAN_CENTER_LAT_LON,    # [Lat, Lon]
        zoom=14,
        control_position="bottomleft"
    )
    
    # 調整地圖高度
    m.layout.height = "700px"
    
    # 加入其他控制項
    m.add_control(leafmap.ScaleControl(position="bottomright"))
    
    return m

@solara.component
def Page():
    """Solara 頁面組件：軸拉式比對地圖"""
    
    # 使用 use_memo 確保地圖只會被建立一次，避免重繪閃爍
    split_map_widget = solara.use_memo(create_split_map, dependencies=[])
    
    with solara.Card(title="05. 馬太鞍溪地貌比對 (軸拉式地圖)", elevation=5):
        solara.Markdown("## ↔️ 衛星影像 vs 街道地圖")
        solara.Markdown(
            """
            請**左右拖曳**地圖中間的滑桿，比對馬太鞍溪流域的真實地貌（衛星影像）與道路規劃（街道地圖）。
            這有助於觀察河道周邊的土地利用情況與自然環境的差異。
            """
        )
        
        # 顯示地圖組件
        # 因為這是 ipyleaflet 物件，我們可以直接在 element 中顯示
        solara.Column(children=[split_map_widget], style={"width": "100%", "height": "750px"})