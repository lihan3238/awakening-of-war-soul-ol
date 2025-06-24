import time
import pytesseract
from PIL import ImageGrab
import pyautogui

# 可根据实际路径设置
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# 是否开启调试模式
DEBUG = False


# firefox浏览器打开游戏 右侧半屏
def get_boss_hp_ratio():
    # 替换为你实际的血条区域坐标
    bbox = (1185, 279, 1287, 298)
    img = ImageGrab.grab(bbox=bbox)

    if DEBUG:
        timestamp = int(time.time())
        img.save(f"debug_hp_{timestamp}.png")  # 保存截图到本地

    text = pytesseract.image_to_string(img, config="--psm 7")

    if DEBUG:
        print(f"[DEBUG] OCR识别文本：{text.strip()}")

    try:
        now, total = map(int, text.strip().split("/"))
        return now / total
    except Exception as e:
        if DEBUG:
            print(f"[DEBUG] 解析失败：{e}")
        return None


def click_change_equipment(equipment_type):
    # 点击当前套装标签
    pyautogui.click(x=1309, y=373)  # 装备栏按钮位置

    time.sleep(0.5)
    if equipment_type == "锤子":
        # 点击锤子套装
        pyautogui.click(x=1342, y=647)
    elif equipment_type == "纯伤":
        # 点击纯伤套装
        pyautogui.click(x=1376, y=439)


def main():
    last_switch = None
    while True:
        ratio = get_boss_hp_ratio()
        if ratio is not None:
            print(f"当前血量百分比: {ratio:.2%}")
            if ratio >= 0.7 and last_switch != "锤子":
                print("切换到锤子")
                click_change_equipment("锤子")
                last_switch = "锤子"
            elif ratio < 0.7 and last_switch != "纯伤":
                print("切换到纯伤")
                click_change_equipment("纯伤")
                last_switch = "纯伤"
        else:
            print("识别失败，跳过一次")
        time.sleep(3)


if __name__ == "__main__":
    main()
