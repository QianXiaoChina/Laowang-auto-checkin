#!/usr/bin/env python3
"""
老王论坛自动签到 - 配置文件
Laowang Forum Auto Sign-in - Configuration Settings
"""

import os
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent

# 网站配置
WEBSITE_CONFIG = {
    "base_url": "https://laowang.vip",
    "signin_home_url": "https://laowang.vip/plugin.php?id=k_misign:sign",
    "signin_url": "https://laowang.vip/plugin.php?id=k_misign:sign&operation=qiandao&formhash=44e9d846&format=empty",
    "login_check_url": "https://laowang.vip/member.php?mod=logging&action=login"
}

# 文件路径配置
PATHS = {
    "cookies_file": PROJECT_ROOT / "config" / "cookies.json",
    "logs_dir": PROJECT_ROOT / "logs",
    "data_dir": PROJECT_ROOT / "data",
    "debug_images_dir": PROJECT_ROOT / "data" / "debug_images"
}

# 浏览器配置
BROWSER_CONFIG = {
    "headless": False,
    "viewport": {"width": 1280, "height": 720},
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "args": [
        "--disable-blink-features=AutomationControlled",
        "--disable-web-security",
        "--disable-features=VizDisplayCompositor"
    ]
}

# 验证码配置
CAPTCHA_CONFIG = {
    "max_attempts_per_image": 2,
    "max_refresh_count": 8,
    "refresh_wait_time": 2,
    "min_confidence_threshold": 0.4,
    "distance_calibration": {
        240: 80,   # 远距离目标
        190: 157,  # 中距离目标  
        170: 170,  # 接近距离目标
        150: 120,  # 中等距离
    }
}

# 时间配置
TIMING_CONFIG = {
    "page_load_wait": 3,
    "element_wait": 2,
    "verification_wait": 3,
    "submit_wait": 3,
    "thinking_time_base": 2.0,
    "thinking_time_variance": 1.0
}

# 日志配置
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(levelname)s - %(message)s",
    "file_encoding": "utf-8",
    "max_file_size": 10 * 1024 * 1024,  # 10MB
    "backup_count": 5
}

# Telegram Bot 配置
TELEGRAM_CONFIG = {
    "enabled": False,
    "bot_token": os.getenv("TELEGRAM_BOT_TOKEN", ""),
    "chat_id": os.getenv("TELEGRAM_CHAT_ID", ""),
    "send_success": True,
    "send_failure": True,
    "send_daily_report": True
}

# GitHub Actions 配置
GITHUB_ACTIONS_CONFIG = {
    "enabled": False,
    "schedule_cron": "0 2 * * *",  # 每天凌晨2点执行
    "timezone": "Asia/Shanghai"
}

# 调试配置
DEBUG_CONFIG = {
    "save_debug_images": True,
    "save_page_screenshots": True,
    "detailed_logging": True,
    "keep_browser_open": False,
    "browser_open_time": 15  # 秒
}

# 确保必要的目录存在
def ensure_directories():
    """确保必要的目录存在"""
    for path in PATHS.values():
        if isinstance(path, Path):
            if path.suffix:  # 如果是文件路径
                path.parent.mkdir(parents=True, exist_ok=True)
            else:  # 如果是目录路径
                path.mkdir(parents=True, exist_ok=True)

# 初始化时创建目录
ensure_directories()
