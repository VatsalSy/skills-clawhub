#!/usr/bin/env python3
"""
Send Email - 邮件发送工具
支持 SMTP 邮件发送，包括 HTML、附件等功能
"""

import smtplib
import sys
import json
import os
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from email.utils import formataddr, formatdate
from typing import Optional, List, Dict, Any
import argparse


# ============================================================================
# 配置管理
# ============================================================================

class EmailConfig:
    """邮件配置"""

    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or Path.home() / ".send_email_config.json"
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if not self.config_path.exists():
            # 创建默认配置模板
            default_config = {
                "smtp": {
                    "host": "smtp.gmail.com",
                    "port": 587,
                    "use_tls": True
                },
                "sender": {
                    "email": "your-email@gmail.com",
                    "name": "Your Name"
                }
            }
            self._save_config(default_config)
            return default_config

        with open(self.config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _save_config(self, config: Dict[str, Any]) -> None:
        """保存配置文件"""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

    def get_smtp_config(self) -> Dict[str, Any]:
        """获取 SMTP 配置"""
        return self.config.get('smtp', {})

    def get_sender_config(self) -> Dict[str, Any]:
        """获取发件人配置"""
        return self.config.get('sender', {})

    def update_smtp(self, host: str, port: int, use_tls: bool = True) -> None:
        """更新 SMTP 配置"""
        if 'smtp' not in self.config:
            self.config['smtp'] = {}
        self.config['smtp']['host'] = host
        self.config['smtp']['port'] = port
        self.config['smtp']['use_tls'] = use_tls
        self._save_config(self.config)
        print(f"✓ SMTP 配置已更新: {host}:{port}")

    def update_sender(self, email: str, name: str) -> None:
        """更新发件人配置"""
        if 'sender' not in self.config:
            self.config['sender'] = {}
        self.config['sender']['email'] = email
        self.config['sender']['name'] = name
        self._save_config(self.config)
        print(f"✓ 发件人配置已更新: {name} <{email}>")


# ============================================================================
# 邮件发送器
# ============================================================================

class EmailSender:
    """邮件发送器"""

    def __init__(self, config: EmailConfig, password: str):
        self.config = config
        self.password = password
        self.smtp_config = config.get_smtp_config()
        self.sender_config = config.get_sender_config()

    def create_message(
        self,
        to_email: str,
        subject: str,
        body: str,
        to_name: str = "",
        is_html: bool = False,
        attachments: Optional[List[str]] = None,
        cc_emails: Optional[List[str]] = None,
        bcc_emails: Optional[List[str]] = None
    ) -> MIMEMultipart:
        """创建邮件消息"""
        msg = MIMEMultipart('related')
        msg['Subject'] = subject
        msg['From'] = formataddr((
            self.sender_config.get('name', ''),
            self.sender_config.get('email', '')
        ))
        msg['To'] = formataddr((to_name, to_email)) if to_name else to_email

        # 添加 CC 和 BCC
        if cc_emails:
            msg['Cc'] = ', '.join(cc_emails)
        # BCC 不添加到头部，只在发送时使用

        msg['Date'] = formatdate(localtime=True)

        # 创建正文部分
        if is_html:
            msg_text = MIMEText(body, 'html', 'utf-8')
        else:
            msg_text = MIMEText(body, 'plain', 'utf-8')
        msg.attach(msg_text)

        # 添加附件
        if attachments:
            for filepath in attachments:
                self._add_attachment(msg, filepath)

        return msg

    def _add_attachment(self, msg: MIMEMultipart, filepath: str) -> None:
        """添加附件"""
        path = Path(filepath)
        if not path.exists():
            print(f"⚠️  附件不存在，跳过: {filepath}")
            return

        try:
            with open(path, 'rb') as f:
                part = MIMEApplication(f.read())

            # 判断文件类型
            maintype, subtype = self._get_mime_type(path)

            part.set_type(f'{maintype}/{subtype}')
            part.add_header('Content-Disposition', 'attachment', filename=path.name)
            msg.attach(part)
            print(f"✓ 已添加附件: {path.name}")
        except Exception as e:
            print(f"✗ 添加附件失败 {path.name}: {str(e)}")

    def _get_mime_type(self, path: Path) -> tuple:
        """获取文件的 MIME 类型"""
        ext = path.suffix.lower()

        # 常见文件类型映射
        mime_types = {
            '.pdf': ('application', 'pdf'),
            '.doc': ('application', 'msword'),
            '.docx': ('application', 'vnd.openxmlformats-officedocument.wordprocessingml.document'),
            '.xls': ('application', 'vnd.ms-excel'),
            '.xlsx': ('application', 'vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
            '.ppt': ('application', 'vnd.ms-powerpoint'),
            '.pptx': ('application', 'vnd.openxmlformats-officedocument.presentationml.presentation'),
            '.jpg': ('image', 'jpeg'),
            '.jpeg': ('image', 'jpeg'),
            '.png': ('image', 'png'),
            '.gif': ('image', 'gif'),
            '.zip': ('application', 'zip'),
            '.txt': ('text', 'plain'),
            '.csv': ('text', 'csv'),
            '.json': ('application', 'json'),
            '.xml': ('application', 'xml'),
        }

        return mime_types.get(ext, ('application', 'octet-stream'))

    def send(
        self,
        to_email: str,
        subject: str,
        body: str,
        to_name: str = "",
        is_html: bool = False,
        attachments: Optional[List[str]] = None,
        cc_emails: Optional[List[str]] = None,
        bcc_emails: Optional[List[str]] = None
    ) -> bool:
        """发送邮件"""
        try:
            # 创建消息
            msg = self.create_message(
                to_email=to_email,
                to_name=to_name,
                subject=subject,
                body=body,
                is_html=is_html,
                attachments=attachments,
                cc_emails=cc_emails,
                bcc_emails=bcc_emails
            )

            # 准备收件人列表
            recipients = [to_email]
            if cc_emails:
                recipients.extend(cc_emails)
            if bcc_emails:
                recipients.extend(bcc_emails)

            # 连接 SMTP 服务器
            host = self.smtp_config.get('host', 'smtp.gmail.com')
            port = self.smtp_config.get('port', 587)
            use_tls = self.smtp_config.get('use_tls', True)

            print(f"正在连接 SMTP 服务器: {host}:{port}")

            if use_tls:
                server = smtplib.SMTP(host, port)
                server.starttls()
            else:
                server = smtplib.SMTP_SSL(host, port)

            # 登录
            print(f"正在登录...")
            server.login(self.sender_config.get('email', ''), self.password)

            # 发送
            print(f"正在发送邮件到: {to_email}")
            server.send_message(msg, to_addrs=recipients)
            server.quit()

            print("✓ 邮件发送成功！")
            return True

        except Exception as e:
            print(f"✗ 邮件发送失败: {str(e)}")
            return False


# ============================================================================
# 命令行界面
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description='Send Email - 邮件发送工具')
    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # 配置命令
    config_parser = subparsers.add_parser('config', help='配置邮件设置')

    # SMTP 配置
    smtp_parser = subparsers.add_parser('smtp', help='配置 SMTP 服务器')
    smtp_parser.add_argument('--host', required=True, help='SMTP 服务器地址')
    smtp_parser.add_argument('--port', type=int, required=True, help='SMTP 服务器端口')
    smtp_parser.add_argument('--no-tls', action='store_true', help='不使用 TLS')

    # 发件人配置
    sender_parser = subparsers.add_parser('sender', help='配置发件人信息')
    sender_parser.add_argument('--email', required=True, help='发件人邮箱')
    sender_parser.add_argument('--name', required=True, help='发件人名称')

    # 发送命令
    send_parser = subparsers.add_parser('send', help='发送邮件')
    send_parser.add_argument('--to', required=True, help='收件人邮箱')
    send_parser.add_argument('--to-name', default='', help='收件人名称')
    send_parser.add_argument('--subject', required=True, help='邮件主题')
    send_parser.add_argument('--body', required=True, help='邮件正文')
    send_parser.add_argument('--html', action='store_true', help='使用 HTML 格式')
    send_parser.add_argument('--attachments', nargs='*', help='附件文件路径（多个）')
    send_parser.add_argument('--cc', nargs='*', help='抄送邮箱（多个）')
    send_parser.add_argument('--bcc', nargs='*', help='密送邮箱（多个）')
    send_parser.add_argument('--password', help='邮箱密码或应用专用密码')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # 初始化配置
    config = EmailConfig()

    if args.command == 'config':
        print("配置文件位置:", config.config_path)
        print("\n当前配置:")
        print(json.dumps(config.config, indent=2, ensure_ascii=False))
        print("\n使用以下命令配置:")
        print("  python send_email.py smtp --host smtp.gmail.com --port 587")
        print("  python send_email.py sender --email your-email@gmail.com --name 'Your Name'")

    elif args.command == 'smtp':
        config.update_smtp(args.host, args.port, not args.no_tls)

    elif args.command == 'sender':
        config.update_sender(args.email, args.name)

    elif args.command == 'send':
        # 获取密码
        password = args.password or os.environ.get('EMAIL_PASSWORD')
        if not password:
            print("请提供邮箱密码或应用专用密码:")
            password = input().strip()

        if not password:
            print("✗ 密码不能为空")
            sys.exit(1)

        # 创建发送器
        sender = EmailSender(config, password)

        # 发送邮件
        sender.send(
            to_email=args.to,
            to_name=args.to_name,
            subject=args.subject,
            body=args.body,
            is_html=args.html,
            attachments=args.attachments,
            cc_emails=args.cc,
            bcc_emails=args.bcc
        )


if __name__ == '__main__':
    main()
