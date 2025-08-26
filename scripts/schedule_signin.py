#!/usr/bin/env python3
"""
定时签到脚本
用于本地定时执行签到任务
"""

import sys
import time
import schedule
import logging
from datetime import datetime, timedelta
from pathlib import Path

# 添加项目根目录到Python路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from laowang_signin import PrecisionCaptchaSolver
from telegram_bot import send_signin_result, send_cookie_expired_notification

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(PROJECT_ROOT / "logs" / "schedule.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class SigninScheduler:
    """签到调度器"""
    
    def __init__(self):
        self.solver = PrecisionCaptchaSolver()
        self.last_signin_date = None
        self.consecutive_days = 0
        self.total_attempts = 0
        self.success_count = 0
        self.failure_count = 0
    
    def run_signin(self):
        """执行签到任务"""
        logger.info("=" * 60)
        logger.info("开始执行定时签到任务")
        logger.info("=" * 60)
        
        try:
            # 检查是否已经签到过
            today = datetime.now().date()
            if self.last_signin_date == today:
                logger.info("今日已经签到过，跳过执行")
                return
            
            self.total_attempts += 1
            
            # 执行签到
            success = self.solver.run()
            
            details = {
                "attempts": self.total_attempts,
                "consecutive_days": self.consecutive_days
            }
            
            if success:
                self.success_count += 1
                self.last_signin_date = today
                self.consecutive_days += 1
                
                logger.info("✅ 定时签到成功")
                send_signin_result(True, details=details)
                
            else:
                self.failure_count += 1
                logger.error("❌ 定时签到失败")
                send_signin_result(False, "签到流程执行失败", details)
                
        except Exception as e:
            self.failure_count += 1
            error_msg = f"定时签到异常: {str(e)}"
            logger.error(error_msg)
            send_signin_result(False, error_msg, {"attempts": self.total_attempts})
    
    def send_daily_report(self):
        """发送每日报告"""
        from telegram_bot import notifier
        
        report_data = {
            "success_count": self.success_count,
            "failure_count": self.failure_count,
            "total_attempts": self.total_attempts,
            "consecutive_days": self.consecutive_days
        }
        
        notifier.send_daily_report(report_data)
        
        # 重置每日统计
        self.success_count = 0
        self.failure_count = 0
        self.total_attempts = 0
    
    def start_scheduler(self):
        """启动调度器"""
        logger.info("启动签到调度器...")
        
        # 每天上午10点执行签到
        schedule.every().day.at("10:00").do(self.run_signin)
        
        # 每天晚上23点发送日报
        schedule.every().day.at("23:00").do(self.send_daily_report)
        
        logger.info("调度器已启动，等待执行...")
        logger.info("签到时间: 每天 10:00")
        logger.info("日报时间: 每天 23:00")
        
        while True:
            try:
                schedule.run_pending()
                time.sleep(60)  # 每分钟检查一次
            except KeyboardInterrupt:
                logger.info("用户中断，停止调度器")
                break
            except Exception as e:
                logger.error(f"调度器运行异常: {e}")
                time.sleep(300)  # 出错后等待5分钟再继续


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="老王论坛定时签到")
    parser.add_argument("--now", action="store_true", help="立即执行一次签到")
    parser.add_argument("--test", action="store_true", help="测试Telegram通知")
    
    args = parser.parse_args()
    
    scheduler = SigninScheduler()
    
    if args.test:
        # 测试Telegram通知
        from telegram_bot import notifier
        if notifier.test_connection():
            print("✅ Telegram通知测试成功")
        else:
            print("❌ Telegram通知测试失败")
        return
    
    if args.now:
        # 立即执行签到
        scheduler.run_signin()
        return
    
    # 启动定时调度
    scheduler.start_scheduler()


if __name__ == "__main__":
    main()
