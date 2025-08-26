#!/usr/bin/env python3
"""
Telegram Bot 通知功能
用于发送签到结果通知
"""

import os
import json
import logging
from datetime import datetime
from typing import Optional, Dict, Any
import requests

from config.settings import TELEGRAM_CONFIG

logger = logging.getLogger(__name__)


class TelegramNotifier:
    """Telegram通知器"""
    
    def __init__(self):
        self.bot_token = TELEGRAM_CONFIG.get("bot_token") or os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = TELEGRAM_CONFIG.get("chat_id") or os.getenv("TELEGRAM_CHAT_ID")
        self.enabled = TELEGRAM_CONFIG.get("enabled", False) and self.bot_token and self.chat_id
        
        if self.enabled:
            logger.info("Telegram通知已启用")
        else:
            logger.info("Telegram通知未启用或配置不完整")
    
    def send_message(self, message: str, parse_mode: str = "Markdown") -> bool:
        """
        发送消息到Telegram
        """
        if not self.enabled:
            logger.debug("Telegram通知未启用，跳过发送")
            return False
        
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            data = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": parse_mode
            }
            
            response = requests.post(url, data=data, timeout=10)
            response.raise_for_status()
            
            logger.info("✅ Telegram消息发送成功")
            return True
            
        except Exception as e:
            logger.error(f"❌ Telegram消息发送失败: {e}")
            return False
    
    def send_signin_success(self, details: Optional[Dict[str, Any]] = None) -> bool:
        """
        发送签到成功通知
        """
        if not TELEGRAM_CONFIG.get("send_success", True):
            return False
        
        now = datetime.now()
        message = f"""
🎉 *老王论坛签到成功*

📅 *时间*: {now.strftime('%Y-%m-%d %H:%M:%S')}
✅ *状态*: 签到完成
🎯 *结果*: 验证码解决 + 提交成功

"""
        
        if details:
            if details.get("attempts"):
                message += f"🔄 *尝试次数*: {details['attempts']}\n"
            if details.get("refresh_count"):
                message += f"🔄 *刷新次数*: {details['refresh_count']}\n"
            if details.get("points"):
                message += f"💰 *获得积分*: {details['points']}\n"
        
        message += "\n🤖 *自动签到系统*"
        
        return self.send_message(message)
    
    def send_signin_failure(self, error: str, details: Optional[Dict[str, Any]] = None) -> bool:
        """
        发送签到失败通知
        """
        if not TELEGRAM_CONFIG.get("send_failure", True):
            return False
        
        now = datetime.now()
        message = f"""
❌ *老王论坛签到失败*

📅 *时间*: {now.strftime('%Y-%m-%d %H:%M:%S')}
❌ *状态*: 签到失败
🔍 *原因*: {error}

"""
        
        if details:
            if details.get("attempts"):
                message += f"🔄 *尝试次数*: {details['attempts']}\n"
            if details.get("refresh_count"):
                message += f"🔄 *刷新次数*: {details['refresh_count']}\n"
            if details.get("error_type"):
                message += f"🏷️ *错误类型*: {details['error_type']}\n"
        
        message += "\n🤖 *自动签到系统*"
        
        return self.send_message(message)
    
    def send_cookie_expired(self) -> bool:
        """
        发送Cookie过期通知
        """
        now = datetime.now()
        message = f"""
🔑 *Cookie已过期*

📅 *时间*: {now.strftime('%Y-%m-%d %H:%M:%S')}
⚠️ *状态*: 需要更新Cookie
🔧 *操作*: 请重新获取并更新cookies.json文件

*获取Cookie步骤:*
1. 浏览器登录老王论坛
2. F12 → Application → Cookies
3. 复制所有cookie数据
4. 更新GitHub Secrets中的COOKIES_JSON

🤖 *自动签到系统*
"""
        
        return self.send_message(message)
    
    def send_daily_report(self, report_data: Dict[str, Any]) -> bool:
        """
        发送每日报告
        """
        if not TELEGRAM_CONFIG.get("send_daily_report", True):
            return False
        
        now = datetime.now()
        success_count = report_data.get("success_count", 0)
        failure_count = report_data.get("failure_count", 0)
        total_attempts = report_data.get("total_attempts", 0)
        
        status_emoji = "✅" if success_count > 0 else "❌"
        
        message = f"""
📊 *老王论坛签到日报*

📅 *日期*: {now.strftime('%Y-%m-%d')}
{status_emoji} *今日状态*: {'成功' if success_count > 0 else '失败'}

📈 *统计数据*:
• 成功次数: {success_count}
• 失败次数: {failure_count}
• 总尝试次数: {total_attempts}

"""
        
        if report_data.get("points_earned"):
            message += f"💰 *今日积分*: +{report_data['points_earned']}\n"
        
        if report_data.get("consecutive_days"):
            message += f"🔥 *连续签到*: {report_data['consecutive_days']} 天\n"
        
        message += "\n🤖 *自动签到系统*"
        
        return self.send_message(message)
    
    def test_connection(self) -> bool:
        """
        测试Telegram连接
        """
        if not self.enabled:
            logger.warning("Telegram通知未启用")
            return False
        
        test_message = f"""
🧪 *Telegram通知测试*

📅 *时间*: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
✅ *状态*: 连接正常
🤖 *系统*: 老王论坛自动签到
"""
        
        return self.send_message(test_message)


# 全局通知器实例
notifier = TelegramNotifier()


def send_signin_result(success: bool, error: str = "", details: Optional[Dict[str, Any]] = None):
    """
    发送签到结果通知的便捷函数
    """
    if success:
        return notifier.send_signin_success(details)
    else:
        return notifier.send_signin_failure(error, details)


def send_cookie_expired_notification():
    """
    发送Cookie过期通知的便捷函数
    """
    return notifier.send_cookie_expired()


if __name__ == "__main__":
    # 测试Telegram通知
    notifier = TelegramNotifier()
    if notifier.test_connection():
        print("✅ Telegram通知测试成功")
    else:
        print("❌ Telegram通知测试失败")
