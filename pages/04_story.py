import solara
import leafmap.maplibregl as leafmap # 改回使用與 01 頁面相同的庫

# --- 1. 定義故事資料 ---
# ⚠️ 重要修正：這裡改用 [經度 Lon, 緯度 Lat] 格式，與 01 頁面保持一致
STORY_STEPS = [
    {
        "title": "起點：馬太鞍溪流域概況",
        "text": "馬太鞍溪是花蓮縣光復鄉的重要河川，源自中央山脈。在地圖上，我們可以看見其沖積扇地形與下游的馬太鞍濕地，是當地農業與生態的核心區域。",
        "location": [121.40, 23.50], # [經度, 緯度]
        "zoom": 12,
        "marker": False
    },
    {
        "title": "背景：人為的「截彎取直」",
        "text": "為了防洪與增加農地，政府過去對河道進行了大規模的「截彎取直」工程。請注意地圖中心，原本蜿蜒的河道被改造成筆直的堤防。這雖然加速了排水，卻也改變了河流的能量平衡。",
        "location": [121.425, 23.485], 
        "zoom": 13,
        "marker": True,
        "marker_color": "#3388ff", # 藍色
        "marker_text": "截彎取直河段"
    },
    {
        "title": "災害：堤防潰決與氾濫",
        "text": "在颱風帶來的極端降雨中，筆直河道導致水流速度過快，強大的能量衝擊堤防脆弱點。此處模擬了當時的潰堤位置，洪水夾帶大量泥沙衝入周邊農田，造成嚴重淹水災情。",
        "location": [121.430, 23.490], 
        "zoom": 14,
        "marker": True,
        "marker_color": "#ff3333", # 紅色
        "marker_text": "潰堤模擬點"
    },
    {
        "title": "省思：馬太鞍濕地的復育",
        "text": "災後，人們開始反思「人定勝天」的工程思維。如今，下游的馬太鞍濕地成為生態復育的示範區，強調「還地於河」與水共存的理念。",
        "location": [121.433, 23.467],
        "zoom": 13,
        "marker": True,
        "marker_color": "#33ff33", # 綠色
        "marker_text": "濕地復育區"
    }
]

# --- 2. Solara 狀態管理 ---
current_step = solara.reactive(0)

# --- 3. 地圖創建函數 ---
def create_story_map(step_index):
    step_data = STORY_STEPS[step_index]
    
    # 使用 leafmap.maplibregl (與 01 頁面相同)
    m = leafmap.Map(
        center=step_data["location"], # [Lon, Lat]
        zoom=step_data["zoom"],
        style="positron", # 使用簡潔的底圖
        height="500px",
        pitch=0, # 敘事地圖使用平面視角較清楚
        bearing=0,
    )
    
    # 如果需要標記
    if step_data["marker"]:
        # 修正：移除不被支援的 color 參數
        # leafmap.maplibregl 的 add_marker 比較簡單，暫時使用預設樣式以確保運行
        m.add_marker(
            lng_lat=step_data["location"],
            popup=step_data["marker_text"]
        )
        
    m.add_layer_control()
    return m

# --- 4. 頁面組件 ---
@solara.component
def Page():
    step_data = STORY_STEPS[current_step.value]
    
    # 建立地圖組件
    # 注意：這裡回傳的是 Map 對象，稍後用 m.to_solara() 顯示
    m = solara.use_memo(
        lambda: create_story_map(current_step.value), 
        dependencies=[current_step.value]
    )
    
    with solara.Card(title="04. 馬太鞍溪事件：地理敘事地圖", elevation=5):
        
        with solara.Columns([2, 1]):
            
            # --- 左側：地圖區 ---
            with solara.Column():
                # 使用 to_solara() 來顯示 leafmap 對象
                m.to_solara()
                
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