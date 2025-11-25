import solara
import ipyleaflet as leaflet
from ipywidgets import HTML

# --- 1. 定義故事資料 (劇本) ---
# 每一個步驟包含標題、文字、地圖中心點 (緯度, 經度)、縮放層級與標記資訊
STORY_STEPS = [
    {
        "title": "起點：馬太鞍溪流域概況",
        "text": "馬太鞍溪是花蓮縣光復鄉的重要河川，源自中央山脈。在地圖上，我們可以看見其沖積扇地形與下游的馬太鞍濕地，是當地農業與生態的核心區域。",
        "location": (23.50, 121.40), # 較廣的視角
        "zoom": 12,
        "marker": False
    },
    {
        "title": "背景：人為的「截彎取直」",
        "text": "為了防洪與增加農地，政府過去對河道進行了大規模的「截彎取直」工程。請注意地圖中心，原本蜿蜒的河道被改造成筆直的堤防。這雖然加速了排水，卻也改變了河流的能量平衡，增加了流速與沖刷力。",
        "location": (23.485, 121.425), # 聚焦河道
        "zoom": 14,
        "marker": True,
        "marker_color": "blue",
        "marker_text": "截彎取直河段"
    },
    {
        "title": "災害：堤防潰決與氾濫",
        "text": "在颱風帶來的極端降雨中，筆直河道導致水流速度過快，強大的能量衝擊堤防脆弱點。此處模擬了當時的潰堤位置，洪水夾帶大量泥沙衝入周邊農田，造成嚴重淹水災情。",
        "location": (23.490, 121.430), # 模擬潰堤點
        "zoom": 15,
        "marker": True,
        "marker_color": "red",
        "marker_text": "潰堤模擬點"
    },
    {
        "title": "省思：馬太鞍濕地的復育",
        "text": "災後，人們開始反思「人定勝天」的工程思維。如今，下游的馬太鞍濕地成為生態復育的示範區，強調「還地於河」與水共存的理念，利用濕地作為洪水的緩衝區。",
        "location": (23.467, 121.433), # 濕地位置
        "zoom": 14,
        "marker": True,
        "marker_color": "green",
        "marker_text": "濕地復育區"
    }
]

# --- 2. Solara 狀態管理 ---
# 記錄當前看到第幾步 (預設從第 0 步開始)
current_step = solara.reactive(0)

# --- 3. 地圖創建函數 ---
def create_story_map(step_index):
    """
    根據步驟索引，回傳一張設定好中心點與標記的地圖。
    """
    step_data = STORY_STEPS[step_index]
    
    # 建立地圖
    m = leaflet.Map(
        center=step_data["location"], 
        zoom=step_data["zoom"], 
        scroll_wheel_zoom=False, # 關閉滾輪縮放，避免干擾閱讀
        layout={'height': '500px'}
    )
    m.add_layer(leaflet.TileLayer(name="OpenStreetMap"))
    
    # 如果這一步需要標記
    if step_data["marker"]:
        marker = leaflet.Marker(
            location=step_data["location"],
            draggable=False,
            icon=leaflet.Icon(
                icon_url=f'https://placehold.co/30x30/{step_data["marker_color"]}/ffffff?text=!', 
                icon_size=[30, 30]
            )
        )
        # 使用 ipywidgets.HTML 製作 Popup，避免錯誤
        popup_html = HTML(value=f"<b>{step_data['marker_text']}</b>")
        marker.popup = leaflet.Popup(child=popup_html, close_button=False, auto_close=False)
        m.add_layer(marker)
        
    m.add_control(leaflet.ScaleControl(position="bottomleft"))
    
    return m

# --- 4. 頁面組件 ---
@solara.component
def Page():
    
    # 取得當前步驟的資料
    step_data = STORY_STEPS[current_step.value]
    
    # 建立地圖組件 (當 current_step 改變時，這裡會重新執行)
    map_widget = solara.use_memo(
        lambda: create_story_map(current_step.value), 
        dependencies=[current_step.value]
    )
    
    with solara.Card(title="04. 馬太鞍溪事件：地理敘事地圖", elevation=5):
        
        # 使用分欄：左邊地圖 (2份寬)，右邊文字 (1份寬)
        with solara.Columns([2, 1]):
            
            # --- 左側：地圖區 ---
            with solara.Column():
                leaflet.Map.element(m=map_widget)
                
                # 導航按鈕
                with solara.Row(justify="center", gap="20px", style={"margin-top": "15px"}):
                    solara.Button(
                        "⬅️ 上一步", 
                        on_click=lambda: current_step.set(max(0, current_step.value - 1)),
                        disabled=(current_step.value == 0),
                        color="primary", 
                        outlined=True
                    )
                    
                    solara.Text(f"步驟 {current_step.value + 1} / {len(STORY_STEPS)}", style={"font-weight": "bold", "margin-top": "10px"})
                    
                    solara.Button(
                        "下一步 ➡️", 
                        on_click=lambda: current_step.set(min(len(STORY_STEPS) - 1, current_step.value + 1)),
                        disabled=(current_step.value == len(STORY_STEPS) - 1),
                        color="primary"
                    )

            # --- 右側：故事文字區 ---
            with solara.Column(style={"padding": "0 20px"}):
                solara.Markdown(f"### 📖 {step_data['title']}")
                solara.Markdown("---")
                solara.Markdown(f"{step_data['text']}")
                
                # 地理觀點小卡片
                with solara.Card(style={"background-color": "#f0f8ff", "margin-top": "30px"}):
                    solara.Markdown("**🌍 地理觀點**")
                    if current_step.value == 0:
                        solara.Markdown("觀察沖積扇扇端與湧泉帶的自然分佈。")
                    elif current_step.value == 1:
                        solara.Markdown("河道型態改變對輸沙平衡的影響。")
                    elif current_step.value == 2:
                        solara.Markdown("攻擊坡與堤防脆弱點的空間關係。")
                    else:
                        solara.Markdown("濕地作為洪水滯留區的功能性。")