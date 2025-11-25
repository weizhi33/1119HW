import solara
import leafmap.maplibregl as leafmap

# 馬太鞍溪周邊中心坐標 (花蓮縣光復鄉一帶，靠近馬太鞍濕地與光復車站)
# Lat: 23.48, Lon: 121.42
MATAAN_CENTER = [121.42, 23.48]

def create_map():
    """
    根據頁面要求建立 Leafmap (MapLibre GL) 地圖。
    - 使用 CartoDB Positron 底圖 (style="positron")。
    - 實作花蓮光復鄉 3D 建築圖層。
    """
    
    # 使用 style="positron" 設置 CartoDB Positron 底圖
    m = leafmap.Map(
        center=MATAAN_CENTER, 
        zoom=16,          # 稍微放大，以清楚顯示建築物
        pitch=60,         # 俯仰角 60 度，展現 3D 效果
        bearing=-20,      # 旋轉角度，以獲得較好的視角
        style="positron", 
        height="750px",
        sidebar_visible=False,
    )
    
    # 實作 3D 建築圖層 (Overture Maps Data)
    # 由於光復鄉的建築密度不如台北，可能需要調整 zoom level 來觀察效果
    m.add_overture_3d_buildings(
        template="simple",
        name="Overture 3D Buildings"
    )
    
    # 加入圖層控制
    m.add_layer_control() 
    
    return m

# ⭐ Solara 頁面組件 ⭐
@solara.component
def Page():
    """
    Solara 頁面組件，用於顯示 Leafmap 地圖和相關說明。
    """
    m = create_map()
    
    # 使用 Solara.Card 包裹地圖，增加標題和視覺效果
    with solara.Card(title="馬太鞍溪事件周邊：3D 建築環境", elevation=5):
        # 將 Leafmap 對象轉換為 Solara 組件
        m.to_solara() 
        
        solara.Markdown(
            f"""
            ### 地理環境分析
            本地圖聚焦於花蓮光復鄉（坐標：{MATAAN_CENTER[1]:.2f}, {MATAAN_CENTER[0]:.2f}）周邊地區。
            利用 3D 建築模型，可以視覺化馬太鞍溪中下游地區的聚落與人造環境分佈，
            有助於評估事件發生時，聚落與基礎設施受影響的潛在風險。
            """
        )
        