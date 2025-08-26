#!/usr/bin/env python3
"""
老王论坛自动签到 - 主入口文件
Laowang Forum Auto Sign-in - Main Entry Point
"""

import sys
import argparse
from pathlib import Path

# 添加src目录到Python路径
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from laowang_signin import PrecisionCaptchaSolver


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="老王论坛自动签到工具")
    parser.add_argument(
        "--cookies", 
        type=str, 
        help="指定cookies文件路径 (默认: config/cookies.json)"
    )
    parser.add_argument(
        "--debug", 
        action="store_true", 
        help="启用调试模式"
    )
    parser.add_argument(
        "--headless", 
        action="store_true", 
        help="无头模式运行浏览器"
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🎯 老王论坛自动签到工具")
    print("=" * 60)
    
    try:
        # 创建解决器实例
        solver = PrecisionCaptchaSolver(cookies_file=args.cookies)
        
        # 运行签到
        success = solver.run()
        
        if success:
            print("\n" + "=" * 60)
            print("✅ 签到成功完成!")
            print("=" * 60)
            return 0
        else:
            print("\n" + "=" * 60)
            print("❌ 签到失败!")
            print("=" * 60)
            return 1
            
    except KeyboardInterrupt:
        print("\n用户中断操作")
        return 1
    except Exception as e:
        print(f"\n程序运行出错: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
