import solara
import leafmap.maplibregl as leafmap # 改用 leafmap，確保與 01/04 頁面一致

# 馬太鞍溪周邊中心坐標 (花蓮縣光復鄉，接近濕地)
# 格式: [經度 Lon, 緯度 Lat] <--- 關鍵修正：這是 leafmap (MapLibre) 的格式
MATAAN_CENTER = [121.42, 23.48]

def create_location_map():
    """創建一個最簡單的 leafmap 地圖，中心設定在馬太鞍溪附近。"""
    
    # 創建基礎地圖
    m = leafmap.Map(
        center=MATAAN_CENTER, 
        zoom=14, # 設定合適的縮放級別
        style="positron", # 與其他頁面統一風格 (CartoDB Positron)
        height="650px",
        pitch=0,
        bearing=0,
    )
    
    # 添加圖層控制
    m.add_layer_control()
    
    # (可選) 您也可以在這裡加入標記，如果需要的話取消下方註解即可
    # m.add_marker(lng_lat=MATAAN_CENTER, popup={"html": "馬太鞍溪中心點"})
    
    return m

# ⭐ Solara 頁面組件 ⭐
@solara.component
def Page():
    """Solara 頁面，用於展示基礎地理環境地圖。"""
    
    # 創建地圖實例
    m = solara.use_memo(create_location_map, dependencies=[])
    
    with solara.Card(title="02. 馬太鞍溪地理環境概覽 (基礎地圖)", elevation=5):
        solara.Markdown("## 🌐 馬太鞍溪流域中心地圖")
        solara.Markdown(
            """
            此頁面展示馬太鞍溪事件周邊的基礎地理環境。地圖中心已修正並設定在花蓮縣光復鄉一帶。
            使用的是與 Story Map 相同的地圖技術，確保定位準確。
            """
        )

        # 將 leafmap 地圖組件嵌入 Solara (使用 to_solara 方法)
        m.to_solara()