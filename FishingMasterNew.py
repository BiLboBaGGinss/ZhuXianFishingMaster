import cv2
import pygetwindow as gw
import pyautogui
import time
import numpy as np
import random

#  pip install opencv-python
#  pip install pygetwindow.
#  pip install pyautogui
#  pip install --upgrade Pillow
#  pyinstaller --onefile FishingMaster.py

# 获取窗口
windows = gw.getWindowsWithTitle('ZhuxianClient')
space = False
fishing = False
if not windows:
    print("窗口未找到")
else:
    print("窗口已找到")
    window = windows[0]

    # 确保窗口是激活的
    window.activate()

    # 获取窗口的位置和大小
    left, top, width, height = window.left, window.top, window.width, window.height

    # 读取模板图像
    templatepaogan = cv2.imread('paogan.png', cv2.IMREAD_COLOR)
    template_qigan = cv2.imread('qigan.png', cv2.IMREAD_COLOR)
    template_diaoyu = cv2.imread('diaoyu.png', cv2.IMREAD_COLOR)
    template_cancel = cv2.imread('cancel.png', cv2.IMREAD_COLOR)
    template_yugan = cv2.imread('gan.png', cv2.IMREAD_COLOR)

    # 获取模板图像的宽度和高度
    wpaogan, hpaogan = templatepaogan.shape[1:]
    w_qigan, h_qigan = template_qigan.shape[1:]
    w_diaoyu, h_diaoyu = template_diaoyu.shape[1:]
    w_cancel, h_cancel = template_cancel.shape[1:]
    w_yugan, h_yugan = template_yugan.shape[1:]

    # 设置匹配阈值
    threshold = 0.85
    yugan_threshold = 0.95

    # 捕获窗口内容
    while True:
        # 获取窗口截图
        screenshot = pyautogui.screenshot(region=(left, top, width, height))
        screenshot = np.array(screenshot)

        # 转换颜色通道顺序（从 BGR 到 RGB）
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB)

        # 进行模板匹配
        res_cancel = cv2.matchTemplate(screenshot, template_cancel,  cv2.TM_CCOEFF_NORMED)
        min_val_cancel, max_val_cancel, min_loc_cancel, max_loc_cancel = cv2.minMaxLoc(res_cancel)


        if max_val_cancel >= threshold:
            fishing = True
            res_diaoyu = cv2.matchTemplate(screenshot, template_diaoyu, cv2.TM_CCOEFF_NORMED)

            min_val_diaoyu, max_val_diaoyu, min_loc_diaoyu, max_loc_diaoyu = cv2.minMaxLoc(res_diaoyu)

            if max_val_diaoyu >= threshold and not space:
                pyautogui.keyDown('space')
                space = True
                print("钓鱼")

            if max_val_diaoyu < threshold and space:
                pyautogui.keyUp('space')
                interval = random.uniform(0.01, 0.03)
                time.sleep(interval)
                for i in range(10):
                    pyautogui.keyDown('space')
                    interval = random.uniform(0.01, 0.03)
                    time.sleep(interval)
                    pyautogui.keyUp('space')
                    interval = random.uniform(0.01, 0.03)
                    time.sleep(interval)
                space = False
                print("放鱼")

            if max_val_diaoyu < threshold and not space:
                res_paogan = cv2.matchTemplate(screenshot, templatepaogan, cv2.TM_CCOEFF_NORMED)
                res_qigan = cv2.matchTemplate(screenshot, template_qigan, cv2.TM_CCOEFF_NORMED)
                min_va_paogan, max_val_paogan, min_loc_paogan, max_loc_paogan = cv2.minMaxLoc(res_paogan)
                min_val_qigan, max_val_qigan, min_loc_qigan, max_loc_qigan = cv2.minMaxLoc(res_qigan)

                # 抛杆
                if max_val_paogan >= threshold:
                    # 模拟按下空格键
                    pyautogui.keyDown('space')
                    interval = random.uniform(0.01, 0.03)
                    pyautogui.sleep(interval)
                    # 模拟释放空格键
                    pyautogui.keyUp('space')
                    print("找到抛杆模板，自动按下空格键")
                    pyautogui.sleep(3)

                # 起杆
                if max_val_qigan >= threshold:
                    interval = random.uniform(0.01, 0.03)
                    # 模拟按下空格键
                    pyautogui.keyDown('space')
                    pyautogui.sleep(interval)
                    # 模拟释放空格键
                    pyautogui.keyUp('space')
                    print("找到起杆模板，自动按下空格键")

        else:
            fishing = False
            print("未找到取消抛竿按钮， 换鱼竿")
            pyautogui.keyDown("B")
            pyautogui.keyUp("B")
            time.sleep(2)

            # 重新获取窗口截图，因为在按键操作后界面可能已经更新
            screenshot = pyautogui.screenshot(region=(left, top, width, height))
            screenshot = np.array(screenshot)

            # 转换颜色通道顺序（从 BGR 到 RGB）
            screenshot_rgb = cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB)

            # 进行模板匹配
            res_yugan = cv2.matchTemplate(screenshot_rgb, template_yugan, cv2.TM_SQDIFF_NORMED)
            min_val_yugan, max_val_yugan, min_loc_yugan, _ = cv2.minMaxLoc(res_yugan)

            print(max_val_yugan)  # 应该使用min_val_yugan因为使用的是TM_SQDIFF_NORMED方法
            if min_val_yugan <= (1 - threshold):  # TM_SQDIFF_NORMED 的最佳匹配是最小值
                # 找到匹配，计算其中心点
                top_left = min_loc_yugan
                bottom_right = (top_left[0] + w_yugan, top_left[1] + h_yugan)

                # 在原图上绘制矩形框
                cv2.rectangle(screenshot_rgb, top_left, bottom_right, (0, 0, 255), 2)  # 使用红色框标记

                target_center_x = top_left[0] + w_yugan // 2
                target_center_y = top_left[1] + h_yugan // 2

                # 显示处理后的图像，用于调试
                # cv2.imshow('Detected', screenshot_rgb)
                # cv2.waitKey(0)

                # 移动鼠标到目标中心并点击右键
                pyautogui.moveTo(left + target_center_x, top + target_center_y)
                pyautogui.click(button='right')
                print("自动执行-找到鱼竿并右键点击")