import cv2
import pygetwindow as gw
import pyautogui
import time
import numpy as np
import random

# 获取窗口
windows = gw.getWindowsWithTitle('图片查看')
space = False
if not windows:
    print("窗口未找到")
else:
    print("窗口已找到")
    window = windows[0]

    # 确保窗口是激活的
    window.activate()

    time.sleep(2)

    # 获取窗口的位置和大小
    left, top, width, height = window.left, window.top, window.width, window.height

    # 读取模板图像
    template_yugan = cv2.imread('cancel_7.png', cv2.IMREAD_COLOR)

    # 获取模板图像的宽度和高度
    w_yugan, h_yugan = template_yugan.shape[1], template_yugan.shape[0]

    # 设置匹配阈值
    threshold = 0.85

    # 获取窗口截图
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
        cv2.imshow('Detected', screenshot_rgb)
        cv2.waitKey(0)

        # # 移动鼠标到目标中心并点击右键
        # pyautogui.moveTo(left + target_center_x, top + target_center_y)
        # pyautogui.click(button='right')
        # print("自动执行-找到鱼竿并右键点击")