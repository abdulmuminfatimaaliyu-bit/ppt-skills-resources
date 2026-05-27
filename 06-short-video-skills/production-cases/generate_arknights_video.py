"""
Arknights Promotional Video Generator
基于生产文档的技术参数自动生成75秒动画分镜视频（Animatic）
Compatible with moviepy v2.x
"""

import numpy as np
from moviepy import (
    VideoClip, ColorClip, TextClip, ImageClip,
    CompositeVideoClip, AudioArrayClip
)
from moviepy.video.fx import FadeIn, FadeOut
import math

# ============================================================
# 配置参数（来自生产文档）
# ============================================================
W, H = 1920, 1080
FPS = 30
TOTAL_DURATION = 75.0

# 色彩方案 - 文档第四节
BG_DARK = (10, 14, 26)
BG_PANEL = (42, 48, 64)
GOLD = (200, 168, 78)
BLUE = (79, 195, 247)
RED = (229, 57, 53)
TEXT_WHITE = (220, 222, 228)
TEXT_GRAY = (140, 145, 158)
GREEN = (0, 200, 150)
PURPLE = (140, 80, 200)

# 字体
FONT = r'C:\Windows\Fonts\msyh.ttc'
FONT_BOLD = r'C:\Windows\Fonts\msyhbd.ttc'

# ============================================================
# 分镜数据（来自文档第三节 - 逐镜详细分镜表）
# ============================================================
SHOTS = [
    # 镜1-4: P1 悬念建立 (0-12s)
    {'id': 1, 'start': 0, 'end': 3, 'type': '极特写', 'scene': '源石晶体脉动发光',
     'narration': '', 'action': '缓慢推近+旋转', 'transition': '硬切成黑闪',
     'mood': '震撼、悬念', 'visual': 'crystal'},
    {'id': 2, 'start': 3, 'end': 5, 'type': '特写', 'scene': '罗德岛LOGO从源石中心显现',
     'narration': '', 'action': '拉远至LOGO居中', 'transition': '交叉溶解',
     'mood': '震撼、悬念', 'visual': 'logo'},
    {'id': 3, 'start': 5, 'end': 8, 'type': '远景', 'scene': '泰拉大陆全景俯瞰，灰暗色调',
     'narration': '"当源石病席卷大地，文明在废墟中挣扎求生。"',
     'action': '由俯瞰缓慢下摇', 'transition': '交叉溶解',
     'mood': '压抑、史诗', 'visual': 'landscape'},
    {'id': 4, 'start': 8, 'end': 12, 'type': '中景', 'scene': '整合运动旗帜在废墟中飘动',
     'narration': '"这不是末日后的安宁，而是暴风雨前的寂静。"',
     'action': '横向平移', 'transition': '硬切',
     'mood': '压抑、史诗', 'visual': 'flag'},
    # 镜5-8: P2 角色展示 (12-25s)
    {'id': 5, 'start': 12, 'end': 15, 'type': '特写', 'scene': '阿米娅正面，兔耳微动',
     'narration': '"罗德岛的领袖阿米娅，将带领我们冲破黑暗。"',
     'action': '由眼部特写拉至半身', 'transition': '硬切+白闪过渡',
     'mood': '希望、坚定', 'visual': 'amiya_face'},
    {'id': 6, 'start': 15, 'end': 18, 'type': '中景', 'scene': '阿米娅佩戴指环、拔出短剑',
     'narration': '', 'action': '跟随手部动作', 'transition': '硬切',
     'mood': '希望、坚定', 'visual': 'amiya_sword'},
    {'id': 7, 'start': 18, 'end': 22, 'type': '中景', 'scene': '博士触控战术终端（第一人称）',
     'narration': '"而你，作为博士，指挥罗德岛迎战危机。"',
     'action': '模拟第一人称手部', 'transition': '硬切',
     'mood': '专业、沉浸', 'visual': 'terminal'},
    {'id': 8, 'start': 22, 'end': 25, 'type': '特写', 'scene': '战术地图上干员图标逐个亮起',
     'narration': '', 'action': '推近至地图', 'transition': '匹配剪辑',
     'mood': '专业、沉浸', 'visual': 'tactical_map'},
    # 镜9-13: P3 系统演示卡点 (25-35s)
    {'id': 9, 'start': 25, 'end': 27, 'type': '快速切', 'scene': '先锋干员·推进之王冲锋',
     'narration': '"八大职业，百位干员，每场战斗都是策略的博弈。"',
     'action': '跟随动作', 'transition': '硬切',
     'mood': '明快、丰富', 'visual': 'vanguard'},
    {'id': 10, 'start': 27, 'end': 29, 'type': '快速切', 'scene': '近卫干员·银灰真银斩',
     'narration': '', 'action': '慢动作+回弹', 'transition': '硬切',
     'mood': '明快、丰富', 'visual': 'guard'},
    {'id': 11, 'start': 29, 'end': 31, 'type': '快速切', 'scene': '重装干员·塞雷娅举盾',
     'narration': '', 'action': '固定镜头', 'transition': '硬切',
     'mood': '明快、丰富', 'visual': 'defender'},
    {'id': 12, 'start': 31, 'end': 33, 'type': '快速切', 'scene': '狙击干员·能天使扫射',
     'narration': '', 'action': '跟随弹道轨迹', 'transition': '匹配剪辑',
     'mood': '明快、丰富', 'visual': 'sniper'},
    {'id': 13, 'start': 33, 'end': 35, 'type': '快速切', 'scene': '术师干员·艾雅法拉火山爆发',
     'narration': '', 'action': '拉远展示AOE范围', 'transition': '模糊转场',
     'mood': '明快、丰富', 'visual': 'caster'},
    # 镜14-16: P4 战斗高潮 (35-45s)
    {'id': 14, 'start': 35, 'end': 37, 'type': '全景', 'scene': '敌人大军从蓝色入口涌入',
     'narration': '"部署阻挡，释放技能，用智慧击败源源不断的敌人。"',
     'action': '横摇跟随敌军', 'transition': '硬切',
     'mood': '紧张、热血', 'visual': 'enemy_wave'},
    {'id': 15, 'start': 37, 'end': 40, 'type': '中景', 'scene': '干员部署动画，技能条蓄力',
     'narration': '', 'action': '推近至技能图标', 'transition': '硬切',
     'mood': '紧张、热血', 'visual': 'skill_charge'},
    {'id': 16, 'start': 40, 'end': 45, 'type': '全景', 'scene': '源石技艺爆炸+敌人清场',
     'narration': '', 'action': '慢动作+镜头震动', 'transition': '白闪过渡',
     'mood': '紧张、热血', 'visual': 'explosion'},
    # 镜17-18: P5a 基地舒缓 (45-50s)
    {'id': 17, 'start': 45, 'end': 47, 'type': '中景', 'scene': '基建主界面全景',
     'narration': '"建立基地，发展科技，为罗德岛提供坚实后盾。"',
     'action': '由上至下俯拍', 'transition': '交叉溶解',
     'mood': '充实、成就', 'visual': 'base_overview'},
    {'id': 18, 'start': 47, 'end': 50, 'type': '快速切', 'scene': '制造站/贸易站/会客室',
     'narration': '', 'action': '横向滑动转场', 'transition': '滑动转场',
     'mood': '充实、成就', 'visual': 'base_rooms'},
    # 镜19-21: P5b 挑战展示 (50-58s)
    {'id': 19, 'start': 50, 'end': 53, 'type': '中景', 'scene': '危机合约高难副本',
     'narration': '"危机合约、集成战略、年度限时活动，内容不断更新。"',
     'action': '由选关到进入战斗', 'transition': '硬切',
     'mood': '挑战、兴奋', 'visual': 'cc_select'},
    {'id': 20, 'start': 53, 'end': 56, 'type': '全景', 'scene': '集成战略肉鸽模式探索',
     'narration': '', 'action': '模拟鼠标探索', 'transition': '推拉转场',
     'mood': '挑战、兴奋', 'visual': 'rogue_map'},
    {'id': 21, 'start': 56, 'end': 58, 'type': '组合', 'scene': '年度活动LOGO轮播',
     'narration': '', 'action': '快速旋转切换', 'transition': '旋转转场+BPM卡点',
     'mood': '挑战、兴奋', 'visual': 'event_logos'},
    # 镜22-23: P6 情感收束 (58-65s)
    {'id': 22, 'start': 58, 'end': 61, 'type': '中景', 'scene': '角色档案界面翻开',
     'narration': '"每一位干员，都有属于自己的故事。"',
     'action': '模拟翻页动画', 'transition': '推拉转场',
     'mood': '动容、沉浸', 'visual': 'character_file'},
    {'id': 23, 'start': 61, 'end': 65, 'type': '组合', 'scene': '精美立绘画廊横向滚动',
     'narration': '', 'action': '横向平移', 'transition': '滑动转场',
     'mood': '动容、沉浸', 'visual': 'art_gallery'},
    # 镜24-26: P7 行动号召 (65-75s)
    {'id': 24, 'start': 65, 'end': 68, 'type': '全景', 'scene': '游戏下载页面展示',
     'narration': '"现在加入罗德岛，开启你的战术征程。立即下载明日方舟！"',
     'action': '固定镜头', 'transition': '交叉溶解',
     'mood': '号召、期待', 'visual': 'download_page'},
    {'id': 25, 'start': 68, 'end': 72, 'type': '特写+文字', 'scene': 'App Store评分+下载按钮闪光',
     'narration': '', 'action': '缓慢推近', 'transition': '硬切',
     'mood': '号召、期待', 'visual': 'rating'},
    {'id': 26, 'start': 72, 'end': 75, 'type': '全屏', 'scene': '罗德岛LOGO+下载引导二维码',
     'narration': '', 'action': '由小至大弹出', 'transition': '淡入',
     'mood': '号召、期待', 'visual': 'end_logo'},
]

# 标题字幕动画（来自文档第四节）
TITLE_CARDS = [
    {'time': 5, 'text': '泰拉大陆', 'duration': 3},
    {'time': 25, 'text': '8大职业', 'duration': 2},
    {'time': 50, 'text': '持续更新', 'duration': 2.5},
    {'time': 65, 'text': '立即下载', 'duration': 3},
]


def make_scene_frame(shot, t):
    """为单个镜头生成一帧图像（numpy array）"""
    from PIL import Image, ImageDraw
    visual_type = shot['visual']

    # 基础画布
    arr = np.zeros((H, W, 3), dtype=np.uint8)
    arr[:] = BG_DARK

    if visual_type == 'crystal':
        # 源石晶体
        img = Image.fromarray(arr)
        draw = ImageDraw.Draw(img)
        cx, cy = W // 2, H // 2
        # 主晶体
        points = 6
        phase = t * 2
        for i in range(points):
            a1 = 2 * math.pi * i / points + phase
            a2 = 2 * math.pi * (i + 1) / points + phase
            r = 160 * (0.7 + 0.3 * math.sin(phase + i))
            x1 = int(cx + r * math.cos(a1))
            y1 = int(cy + r * math.sin(a1))
            x2 = int(cx + r * math.cos(a2))
            y2 = int(cy + r * math.sin(a2))
            shade = 0.5 + 0.5 * (i / points)
            c = tuple(int(ch * shade) for ch in GOLD)
            draw.polygon([(cx, cy), (x1, y1), (x2, y2)], fill=c)
        # 小晶体
        for _ in range(15):
            sx = np.random.randint(100, W - 100)
            sy = np.random.randint(100, H - 100)
            ss = np.random.randint(8, 25)
            sp = t * 3 + sx * 0.1
            for j in range(4):
                a1 = 2 * math.pi * j / 4 + sp
                a2 = 2 * math.pi * (j + 1) / 4 + sp
                r = ss * (0.6 + 0.4 * math.sin(sp))
                x1 = int(sx + r * math.cos(a1))
                y1 = int(sy + r * math.sin(a1))
                x2 = int(sx + r * math.cos(a2))
                y2 = int(sy + r * math.sin(a2))
                draw.polygon([(sx, sy), (x1, y1), (x2, y2)],
                             fill=tuple(int(ch * 0.6) for ch in BLUE))
        arr[:] = np.array(img)

    elif visual_type == 'logo':
        img = Image.fromarray(arr)
        draw = ImageDraw.Draw(img)
        cx, cy = W // 2, H // 2
        scale = min(t / 2 + 0.3, 1.0)
        size = 140 * scale
        draw.polygon([(cx, cy - size), (cx + size * 0.7, cy),
                      (cx, cy + size), (cx - size * 0.7, cy)], fill=GOLD)
        draw.ellipse([cx - 25, cy - 25, cx + 25, cy + 25], fill=BG_DARK)
        draw.text((cx - 90, cy + size + 30), "RHODES ISLAND", fill=GOLD)
        arr[:] = np.array(img)

    elif visual_type == 'landscape':
        img = Image.fromarray(arr)
        draw = ImageDraw.Draw(img)
        horizon_y = int(H * 0.6)
        draw.rectangle([(0, horizon_y), (W, H)], fill=(15, 20, 35))
        draw.rectangle([(0, horizon_y - 2), (W, horizon_y)], fill=BG_PANEL)
        for i in range(18):
            x = i * 110 + int(math.sin(i) * 20)
            bh = 50 + int(math.sin(i * 2.5) * 35)
            draw.rectangle([(x, horizon_y - bh), (x + 40, horizon_y)],
                           fill=(20 + i * 2, 25 + i, 38))
        for _ in range(25):
            lx = np.random.randint(0, W)
            ly = np.random.randint(0, horizon_y)
            draw.ellipse([lx - 1, ly - 1, lx + 1, ly + 1], fill=(50, 48, 38))
        arr[:] = np.array(img)

    elif visual_type == 'flag':
        img = Image.fromarray(arr)
        draw = ImageDraw.Draw(img)
        draw.rectangle([(W // 2 - 3, 180), (W // 2 + 3, 750)], fill=(90, 90, 95))
        wave = math.sin(t * 3) * 25
        flag_points = [(W // 2 + 3, 200)]
        for dx in range(0, 220, 8):
            px = W // 2 + 3 + dx
            py = 220 + math.sin((dx + t * 120) * 0.03) * 18
            flag_points.append((int(px), int(py)))
        for dx in range(220, 0, -8):
            px = W // 2 + 3 + dx
            py = 380 + math.sin((dx + t * 120) * 0.03) * 18
            flag_points.append((int(px), int(py)))
        draw.polygon(flag_points, fill=(170, 38, 32))
        # 标志
        draw.ellipse([W // 2 + 60, 260, W // 2 + 130, 330], fill=(45, 48, 55))
        arr[:] = np.array(img)

    elif visual_type == 'amiya_face':
        img = Image.fromarray(arr)
        draw = ImageDraw.Draw(img)
        cx, cy = W // 2, H // 2
        draw.ellipse([cx - 90, cy - 110, cx + 90, cy + 130], fill=(58, 52, 62))
        # 眼睛
        draw.ellipse([cx - 35, cy - 25, cx - 10, cy + 5], fill=BLUE)
        draw.ellipse([cx + 10, cy - 25, cx + 35, cy + 5], fill=BLUE)
        draw.ellipse([cx - 32, cy - 22, cx - 13, cy + 2], fill=(200, 220, 255))
        draw.ellipse([cx + 13, cy - 22, cx + 32, cy + 2], fill=(200, 220, 255))
        draw.ellipse([cx - 25, cy - 15, cx - 17, cy - 5], fill=(20, 25, 40))
        draw.ellipse([cx + 17, cy - 15, cx + 25, cy - 5], fill=(20, 25, 40))
        # 兔耳
        draw.polygon([(cx - 60, cy - 65), (cx - 40, cy - 150), (cx - 20, cy - 75)], fill=(65, 58, 68))
        draw.polygon([(cx + 20, cy - 75), (cx + 40, cy - 150), (cx + 60, cy - 65)], fill=(65, 58, 68))
        # 瞳孔中的金芒
        glow = int(20 + 15 * math.sin(t * 3))
        draw.ellipse([cx - 23, cy - 12, cx - 19, cy - 7], fill=(200, 168, 78))
        draw.ellipse([cx + 19, cy - 12, cx + 23, cy - 7], fill=(200, 168, 78))
        arr[:] = np.array(img)

    elif visual_type == 'amiya_sword':
        img = Image.fromarray(arr)
        draw = ImageDraw.Draw(img)
        cx, cy = W // 2, H // 2 + 30
        sword_progress = min(t / 2, 1)
        draw.ellipse([cx - 50, cy, cx + 50, cy + 80], fill=(62, 52, 57))
        draw.ellipse([cx - 18, cy + 5, cx + 18, cy + 35], fill=GOLD)
        draw.ellipse([cx - 12, cy + 10, cx + 12, cy + 30], fill=BG_DARK)
        blade_top = cy - 200 * sword_progress
        draw.polygon([(cx - 6, cy + 5), (cx - 2, blade_top),
                      (cx, blade_top - 8), (cx + 2, blade_top),
                      (cx + 6, cy + 5)], fill=(170, 172, 180))
        draw.rectangle([(cx - 25, cy - 5), (cx + 25, cy + 5)], fill=GOLD)
        if sword_progress > 0.3:
            alpha = min((sword_progress - 0.3) * 2, 0.4)
            glow_c = tuple(int(c * alpha) for c in BLUE)
            y_top = int(blade_top)
            y_bot = cy + 30
            if y_bot > y_top:
                draw.rectangle([(cx - 40, y_top), (cx + 40, y_bot)], fill=glow_c)
        arr[:] = np.array(img)

    elif visual_type == 'terminal':
        img = Image.fromarray(arr)
        draw = ImageDraw.Draw(img)
        draw.rectangle([(80, 40), (W - 80, H - 40)], fill=(14, 18, 32), outline=BG_PANEL, width=2)
        for i in range(10):
            y = 80 + i * 100
            draw.line([(100, y), (W - 100, y)], fill=(28, 35, 50), width=1)
        for i in range(14):
            x = 100 + i * 120
            draw.line([(x, 60), (x, H - 60)], fill=(28, 35, 50), width=1)
        for i in range(6):
            dx = 160 + i * 280
            dy = 200 + int(math.sin(t + i) * 15)
            draw.ellipse([dx - 28, dy - 28, dx + 28, dy + 28], fill=(28, 38, 58), outline=BLUE, width=2)
            draw.text((dx - 6, dy - 8), str(i + 1), fill=(200, 200, 210))
        scan_y = int((t % 2) * H)
        draw.rectangle([(80, scan_y), (W - 80, scan_y + 4)], fill=(20, 50, 80, 50))
        arr[:] = np.array(img)

    elif visual_type == 'tactical_map':
        img = Image.fromarray(arr)
        draw = ImageDraw.Draw(img)
        arr[:] = (8, 12, 22)
        for i in range(18):
            x = i * 110
            draw.line([(x, 0), (x, H)], fill=(14, 20, 35), width=1)
        for i in range(10):
            y = i * 110
            draw.line([(0, y), (W, y)], fill=(14, 20, 35), width=1)
        icons = [(250, 350), (550, 280), (850, 480), (380, 680),
                 (720, 580), (1050, 330), (1280, 520), (1500, 380)]
        for i, (ix, iy) in enumerate(icons):
            progress = min(max((t * 3.5 - i * 0.25), 0), 1)
            if progress > 0:
                a = int(100 * progress)
                draw.ellipse([ix - 24, iy - 24, ix + 24, iy + 24], fill=(25, 45, a))
                draw.ellipse([ix - 18, iy - 18, ix + 18, iy + 18], outline=GOLD, width=2)
        arr[:] = np.array(img)

    elif visual_type in ('vanguard', 'guard', 'defender', 'sniper', 'caster'):
        class_info = {
            'vanguard': ('先锋', GOLD, 0), 'guard': ('近卫', RED, 1),
            'defender': ('重装', BLUE, 2), 'sniper': ('狙击', GREEN, 3),
            'caster': ('术师', PURPLE, 4),
        }
        cn, cc, _ = class_info[visual_type]
        img = Image.fromarray(arr)
        draw = ImageDraw.Draw(img)
        cx, cy = W // 2, H // 2
        pulse = 0.5 + 0.5 * math.sin(t * 5)
        for r in range(180, 140, -5):
            a_val = int(25 * (1 - (180 - r) / 40))
            draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                         fill=tuple(min(ch * a_val // 255 + 10, 255) for ch in cc))
        draw.ellipse([cx - 70, cy - 70, cx + 70, cy + 70], fill=(18, 22, 38), outline=cc, width=4)
        draw.text((cx - 35, cy - 18), cn, fill=cc)
        draw.rectangle([(cx - 110, cy + 100), (cx + 110, cy + 150)], fill=(0, 0, 0, 100))
        draw.text((cx - 35, cy + 112), "■" * 6, fill=GOLD)
        arr[:] = np.array(img)

    elif visual_type == 'enemy_wave':
        img = Image.fromarray(arr)
        draw = ImageDraw.Draw(img)
        draw.ellipse([20, H // 2 - 120, 160, H // 2 + 120], fill=(8, 16, 40))
        draw.ellipse([30, H // 2 - 100, 150, H // 2 + 100], fill=(4, 8, 25))
        for i in range(30):
            progress = ((t * 4 + i * 0.2) % 4) / 4
            x = 160 + progress * (W - 220)
            y = H // 2 - 250 + i * 35 + int(math.sin(t + i) * 15)
            if 0 < x < W:
                draw.ellipse([int(x) - 9, y - 9, int(x) + 9, y + 9], fill=(170, 35, 35))
                draw.ellipse([int(x) - 6, y - 6, int(x) + 6, y + 6], fill=(200, 55, 45))
        arr[:] = np.array(img)

    elif visual_type == 'skill_charge':
        img = Image.fromarray(arr)
        draw = ImageDraw.Draw(img)
        cx, cy = W // 2, H // 2
        draw.ellipse([cx - 90, cy - 90, cx + 90, cy + 90], fill=(28, 32, 48), outline=BLUE, width=3)
        charge = min((t % 3) / 3, 1)
        for i in range(8):
            a = math.radians(i * 45)
            rx = 75 * math.cos(a)
            ry = 75 * math.sin(a)
            active = i / 8 <= charge
            c = BLUE if active else BG_PANEL
            draw.ellipse([int(cx + rx - 10), int(cy + ry - 10),
                          int(cx + rx + 10), int(cy + ry + 10)], fill=c)
        draw.ellipse([cx - 24, cy - 24, cx + 24, cy + 24], fill=GOLD)
        arr[:] = np.array(img)

    elif visual_type == 'explosion':
        img = Image.fromarray(arr)
        draw = ImageDraw.Draw(img)
        cx, cy = W // 2, H // 2
        expand = min(t * 2.5, 1)
        for r in range(int(60 + expand * 450), 0, -12):
            v = int(255 * (1 - r / 550))
            if r > 220:
                c = (v, int(v * 0.6), 25)
            elif r > 120:
                c = (int(v * 0.9), int(v * 0.4), 8)
            else:
                c = (255, 255, 200)
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)
        shock = (t * 6) % 3
        for sr in [int(350 + shock * 60)]:
            draw.ellipse([cx - sr, cy - sr, cx + sr, cy + sr], outline=(200, 180, 150), width=3)
        np.random.seed(42)
        for _ in range(80):
            angle = np.random.random() * 2 * math.pi
            dist = expand * 350 * np.random.random()
            px = int(cx + dist * math.cos(angle))
            py = int(cy + dist * math.sin(angle))
            if 0 <= px < W and 0 <= py < H:
                draw.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 200, 40))
        arr[:] = np.array(img)

    elif visual_type in ('base_overview', 'base_rooms', 'cc_select',
                         'rogue_map', 'event_logos', 'character_file',
                         'art_gallery', 'download_page', 'rating', 'end_logo'):
        # 简化渲染 - 显示场景名称
        img = Image.fromarray(arr)
        draw = ImageDraw.Draw(img)
        # 场景标题
        titles = {
            'base_overview': '罗德岛基建 - 制造/贸易/发电',
            'base_rooms': '基建功能区',
            'cc_select': '危机合约 - 风险等级选择',
            'rogue_map': '集成战略 - 迷雾探索',
            'event_logos': '年度限时活动',
            'character_file': '干员档案系统',
            'art_gallery': '精美角色立绘',
            'download_page': '游戏下载页',
            'rating': 'App Store 评分 4.8',
            'end_logo': '立即下载明日方舟',
        }
        title = titles.get(visual_type, '')
        # 居中显示标题
        draw.text((W // 2 - 120, H // 2 - 30), title, fill=GOLD)
        # 装饰线
        draw.rectangle([(W // 2 - 150, H // 2 + 30), (W // 2 + 150, H // 2 + 33)], fill=GOLD)
        # 场景编号
        draw.text((W // 2 - 30, H // 2 + 50), f"SCENE {shot['id']:02d}", fill=TEXT_GRAY)
        arr[:] = np.array(img)

    return arr


def make_shot_clip(shot):
    """为单个镜头创建VideoClip"""
    duration = shot['end'] - shot['start']

    def frame_func(t):
        return make_scene_frame(shot, t)

    clip = VideoClip(frame_func, duration=duration)

    # 添加HUD叠加层
    time_range = f"{shot['start']:.0f}-{shot['end']:.0f}"

    overlay_items = []

    # 左上角 - 镜号和时间
    info = TextClip(
        text=f"SHOT {shot['id']:02d}  |  {time_range}s  |  {shot['type']}",
        font_size=22, color=TEXT_GRAY, font=FONT,
        stroke_color=BG_DARK, stroke_width=1
    ).with_position((60, 25)).with_duration(duration)

    # 右上角 - 情绪标签
    mood_text = TextClip(
        text=f"「{shot['mood']}」",
        font_size=20, color=GOLD, font=FONT,
        stroke_color=BG_DARK, stroke_width=1
    ).with_position(('right', 25)).with_duration(duration)

    # 底部场景名称
    scene_bg = (ColorClip(color=(0, 0, 0), size=(W, 45))
                .with_opacity(0.4)
                .with_position((0, H - 95))
                .with_duration(duration))
    scene_text = TextClip(
        text=shot['scene'],
        font_size=20, color=TEXT_WHITE, font=FONT
    ).with_position(('center', H - 90)).with_duration(duration)

    # 旁白字幕
    subtitle = None
    if shot['narration']:
        subtitle = TextClip(
            text=shot['narration'],
            font_size=26, color=TEXT_WHITE, font=FONT,
            stroke_color=BG_DARK, stroke_width=2,
            method='caption', size=(W - 300, None)
        ).with_position(('center', H - 160)).with_duration(duration)

    overlay_items.extend([info, mood_text, scene_bg, scene_text])
    if subtitle:
        overlay_items.append(subtitle)

    # 合成
    all_parts = [clip] + overlay_items
    composite = CompositeVideoClip(all_parts, size=(W, H))

    return composite


def make_title_card(title_text, appear_time, duration):
    """创建标题字幕卡"""
    title = (TextClip(text=title_text, font_size=56, color=GOLD,
                      font=FONT_BOLD, stroke_color=BG_DARK, stroke_width=3)
             .with_duration(duration).with_start(appear_time)
             .with_position(('center', 130)))
    line = (ColorClip(color=GOLD, size=(300, 3))
            .with_duration(duration).with_start(appear_time + 0.3)
            .with_position(('center', 180)))
    return [title, line]


def create_bgm_track():
    """创建合成BGM音频轨道（placeholder）"""
    sample_rate = 44100
    total_samples = int(TOTAL_DURATION * sample_rate)
    t = np.linspace(0, TOTAL_DURATION, total_samples, endpoint=False)

    # 背景氛围音
    ambient = 0.06 * np.sin(2 * np.pi * 55 * t) + 0.04 * np.sin(2 * np.pi * 82 * t)

    # P1: 悬念 (0-12s)
    p1 = np.zeros_like(t)
    m1 = t < 12
    p1[m1] = 0.10 * np.sin(2 * np.pi * 65 * t[m1])

    # P2: 希望上升 (12-25s)
    p2 = np.zeros_like(t)
    m2 = (t >= 12) & (t < 25)
    f2 = (t[m2] - 12) / 13
    p2[m2] = f2 * 0.12 * np.sin(2 * np.pi * (130 + f2 * 60) * t[m2])

    # P3: 节奏驱动 (25-35s)
    p3 = np.zeros_like(t)
    m3 = (t >= 25) & (t < 35)
    beat = np.sin(2 * np.pi * 2.13 * t[m3]) > 0.4
    p3[m3] = 0.16 * np.sin(2 * np.pi * 220 * t[m3]) * (0.5 + 0.5 * beat)

    # P4: 战斗高潮 (35-45s)
    p4 = np.zeros_like(t)
    m4 = (t >= 35) & (t < 45)
    i4 = (t[m4] - 35) / 10
    p4[m4] = i4 * 0.22 * np.sin(2 * np.pi * (250 + i4 * 100) * t[m4])

    # P5: 过渡 (45-58s)
    p5 = np.zeros_like(t)
    m5 = (t >= 45) & (t < 58)
    p5[m5] = 0.08 * np.sin(2 * np.pi * 95 * t[m5])

    # P6: 情感 (58-65s)
    p6 = np.zeros_like(t)
    m6 = (t >= 58) & (t < 65)
    p6[m6] = 0.12 * (np.sin(2 * np.pi * 261.63 * t[m6]) * 0.5 +
                     np.sin(2 * np.pi * 329.63 * t[m6]) * 0.3)

    # P7: 号召结尾 (65-75s)
    p7 = np.zeros_like(t)
    m7 = t >= 65
    f7 = (t[m7] - 65) / 10
    p7[m7] = f7 * 0.18 * (np.sin(2 * np.pi * 196 * t[m7]) +
                           np.sin(2 * np.pi * 294 * t[m7]))

    audio = ambient + p1 + p2 + p3 + p4 + p5 + p6 + p7
    audio = audio / np.max(np.abs(audio)) * 0.25

    # 淡入淡出
    fl = int(0.3 * sample_rate)
    audio[:fl] *= np.linspace(0, 1, fl)
    audio[-fl:] *= np.linspace(1, 0, fl)

    return AudioArrayClip(audio.reshape(-1, 1), fps=sample_rate)


def build_video():
    """构建完整视频"""
    print("=" * 60)
    print("  明日方舟（Arknights）推广短片 - Animatic 生成")
    print("=" * 60)
    print(f"  分辨率: {W}x{H} | FPS: {FPS} | 时长: {TOTAL_DURATION}s")
    print(f"  镜头数: {len(SHOTS)} | 使用字体: Microsoft YaHei")
    print("-" * 60)

    # 生成每个镜头的clip
    shot_clips = []
    for i, shot in enumerate(SHOTS):
        print(f"  [镜头 {shot['id']:02d}/{len(SHOTS)}] "
              f"{shot['start']:02.0f}s-{shot['end']:02.0f}s | "
              f"{shot['type']:<5s} | {shot['scene'][:20]}...")
        clip = make_shot_clip(shot)
        shot_clips.append(clip)

    # 拼接所有镜头
    print("-" * 60)
    print("  拼接时间线...")
    from moviepy import concatenate_videoclips
    timeline = concatenate_videoclips(shot_clips, method='compose')

    # 添加标题字幕
    print("  添加标题卡...")
    title_items = []
    for tc in TITLE_CARDS:
        items = make_title_card(tc['text'], tc['time'], tc['duration'])
        title_items.extend(items)

    final = CompositeVideoClip([timeline] + title_items, size=(W, H))

    # 添加音频
    print("  生成背景音乐...")
    bgm = create_bgm_track()
    final = final.with_audio(bgm)

    # 导出
    output_path = r'd:\Trae CN\代码\06-short-video-skills\production-cases\arknights_promo_animatic.mp4'
    print(f"  导出视频到: {output_path}")
    print("  渲染中（可能需要几分钟）...")
    final.write_videofile(
        output_path,
        fps=FPS,
        codec='libx264',
        audio_codec='aac',
        bitrate='4000k',
        preset='medium',
        threads=2,
        logger='bar'
    )

    print("-" * 60)
    print("  [完成] 视频生成完成！")
    print(f"  输出: {output_path}")
    print(f"  时长: {TOTAL_DURATION}s")
    print(f"  分辨率: {W}x{H}")
    print("=" * 60)
    return output_path


if __name__ == '__main__':
    build_video()