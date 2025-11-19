# 檔名: 03_TAIPEI_BUILD.py (請確保你的檔名與 Solara 偵測到的檔名一致)
import solara
import leafmap.maplibregl as leafmap

# 台北市中心坐標 (接近信義區/市政府)
TAIPEI_CENTER = [121.56, 25.03] 

def create_map():
    """
    根據頁面要求建立 Leafmap (MapLibre GL) 地圖。
    - 使用 CartoDB Positron 底圖 (style="positron")。
    - 實作台北 3D 建築圖層。
    """
    
    # 使用 style="positron" 設置 CartoDB Positron 底圖，無需 Mapbox Token
    m = leafmap.Map(
        center=TAIPEI_CENTER, 
        zoom=15.5, 
        pitch=60, 
        bearing=-17, 
        style="positron", 
        height="750px",
        sidebar_visible=False,
    )
    
    # 實作台北 3D 建築圖層 (Overture Maps Data)
    m.add_overture_3d_buildings(
        template="simple",
        name="Overture 3D Buildings"
    )
    
    # 加入圖層控制
    m.add_layer_control() 
    
    return m

# ⭐⭐⭐ 關鍵修復處： Solara 必須找到這個名為 Page 的組件 ⭐⭐⭐
@solara.component
def Page():
    """
    Solara 頁面組件，用於顯示 Leafmap 地圖。
    """
    m = create_map()
    
    # 將 Leafmap 對象轉換為 Solara 組件
    return m.to_solara()