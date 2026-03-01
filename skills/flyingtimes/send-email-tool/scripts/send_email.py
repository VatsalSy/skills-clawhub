#!/usr/bin/env python3
"""
Send Email - 邮件发送工具
支持 SMTP 邮件发送，包括 HTML、附件等功能
支持 keyring 密钥管理
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

# 尝试导入 keyring，失败则使用备用方案
try:
    import keyring
    KEYRING_AVAILABLE = True
except ImportError:
    KEYRING_AVAILABLE = False
    print("⚠️  keyring 未安装，将使用备用存储方案")
    print("   安装 keyring: pip install keyring")


# ============================================================================
# 密钥管理
# ============================================================================

class KeyringManager:
    """密钥管理器 - 使用 keyring 或备用方案"""

    def __init__(self):
        self.service_name = "send_email_tool"
        self.password_backup_file = Path.home() / ".send_email_password"
        self.username_backup_file = Path.home() / ".send_email_username"

    def get_password(self, username: str) -> Optional[str]:
        """获取密码"""
        if KEYRING_AVAILABLE:
            try:
                password = keyring.get_password(self.service_name, username)
                if password:
                    return password
            except Exception as e:
                print(f"⚠️  keyring 读取失败: {str(e)}")

        # 备用方案：从文件读取
        return self._read_from_backup(self.password_backup_file)

    def get_username(self) -> Optional[str]:
        """获取发件人邮箱（用户名）"""
        if KEYRING_AVAILABLE:
            try:
                username = keyring.get_password(self.service_name, "username")
                if username:
                    return username
            except Exception as e:
                print(f"⚠️  keyring 读取失败: {str(e)}")

        # 备用方案：从文件读取
        return self._read_from_backup(self.username_backup_file)

    def set_password(self, username: str, password: str) -> None:
        """保存密码"""
        if KEYRING_AVAILABLE:
            try:
                keyring.set_password(self.service_name, username, password)
                print(f"✓ 密码已保存到 keyring (用户名: {username})")
                return
            except Exception as e:
                print(f"⚠️  keyring 保存失败: {str(e)}，使用备用方案")

        # 备用方案：保存到文件
        self._save_to_backup(self.password_backup_file, password)
        print(f"✓ 密码已保存到备用文件 (用户名: {username})")

    def set_username(self, username: str) -> None:
        """保存发件人邮箱（用户名）"""
        if KEYRING_AVAILABLE:
            try:
                keyring.set_password(self.service_name, "username", username)
                print(f"✓ 发件人邮箱已保存到 keyring: {username}")
                return
            except Exception as e:
                print(f"⚠️  keyring 保存失败: {str(e)}，使用备用方案")

        # 备用方案：保存到文件
        self._save_to_backup(self.username_backup_file, username)
        print(f"✓ 发件人邮箱已保存到备用文件: {username}")

    def delete_password(self, username: str) -> None:
        """删除密码"""
        if KEYRING_AVAILABLE:
            try:
                keyring.delete_password(self.service_name, username)
                print(f"✓ 密码已从 keyring 删除 (用户名: {username})")
                return
            except Exception as e:
                print(f"⚠️  keyring 删除失败: {str(e)}")

        # 备用方案：删除文件
        if self.password_backup_file.exists():
            self.password_backup_file.unlink()
            print("✓ 备用密码文件已删除")

    def delete_username(self) -> None:
        """删除发件人邮箱"""
        if KEYRING_AVAILABLE:
            try:
                keyring.delete_password(self.service_name, "username")
                print("✓ 发件人邮箱已从 keyring 删除")
                return
            except Exception as e:
                print(f"⚠️  keyring 删除失败: {str(e)}")

        # 备用方案：删除文件
        if self.username_backup_file.exists():
            self.username_backup_file.unlink()
            print("✓ 备用用户名文件已删除")

    def _save_to_backup(self, backup_file: Path, content: str) -> None:
        """保存到备用文件（加密或编码）"""
        # 使用 base64 简单编码（注意：这不是加密，仅避免明文存储）
        import base64
        encoded = base64.b64encode(content.encode('utf-8')).decode('utf-8')

        # 设置文件权限为仅用户可读写
        backup_file.write_text(encoded)
        backup_file.chmod(0o600)

    def _read_from_backup(self, backup_file: Path) -> Optional[str]:
        """从备用文件读取"""
        if not backup_file.exists():
            return None

        try:
            import base64
            encoded = backup_file.read_text()
            return base64.b64decode(encoded).decode('utf-8')
        except Exception:
            return None


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
                    "host": "smtp.gd.chinamobile.com",
                    "port": 465,
                    "use_tls": False
                },
                "sender": {
                    "name": "中国移动用户"
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

    def get_sender_config(self, username: Optional[str] = None) -> Dict[str, Any]:
        """获取发件人配置"""
        sender_config = self.config.get('sender', {})

        # 如果提供了 username，使用它；否则尝试从 keyring 读取
        if username:
            sender_config['email'] = username
        elif 'email' not in sender_config:
            # 从 keyring 读取邮箱
            keyring = KeyringManager()
            stored_username = keyring.get_username()
            if stored_username:
                sender_config['email'] = stored_username
            else:
                # 使用默认邮箱
                sender_config['email'] = "user@gd.chinamobile.com"

        return sender_config

    def update_smtp(self, host: str, port: int, use_tls: bool = True) -> None:
        """更新 SMTP 配置"""
        if 'smtp' not in self.config:
            self.config['smtp'] = {}
        self.config['smtp']['host'] = host
        self.config['smtp']['port'] = port
        self.config['smtp']['use_tls'] = use_tls
        self._save_config(self.config)
        print(f"✓ SMTP 配置已更新: {host}:{port}")

    def update_sender(self, name: str) -> None:
        """更新发件人配置"""
        if 'sender' not in self.config:
            self.config['sender'] = {}
        self.config['sender']['name'] = name
        self._save_config(self.config)
        print(f"✓ 发件人名称已更新: {name}")

        # 提示使用 keyring 保存邮箱
        print(f"\n⚠️  邮箱地址需通过 keyring 保存：")
        print(f"   python send_email.py username --save --email your-email@gd.chinamobile.com")


# ============================================================================
# 邮件发送器
# ============================================================================

class EmailSender:
    """邮件发送器"""

    def __init__(self, config: EmailConfig, username: Optional[str] = None):
        self.config = config
        self.keyring = KeyringManager()
        self.smtp_config = config.get_smtp_config()
        self.sender_config = config.get_sender_config(username)

        # 从 keyring 读取发件人邮箱
        if not username:
            stored_username = self.keyring.get_username()
            if stored_username:
                self.sender_config['email'] = stored_username

        # 从 keyring 读取密码
        email = self.sender_config.get('email', '')
        self.password = self.keyring.get_password(email)

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
            host = self.smtp_config.get('host', 'smtp.gd.chinamobile.com')
            port = self.smtp_config.get('port', 587)
            use_tls = self.smtp_config.get('use_tls', True)

            print(f"正在连接 SMTP 服务器: {host}:{port}")

            if use_tls:
                server = smtplib.SMTP(host, port)
                server.starttls()
            else:
                server = smtplib.SMTP_SSL(host, port)

            # 登录
            email = self.sender_config.get('email', '')
            print(f"正在登录 (发件人: {email})...")
            server.login(email, self.password)

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
    sender_parser = subparsers.add_parser('sender', help='配置发件人名称')
    sender_parser.add_argument('--name', required=True, help='发件人名称')

    # 发件人邮箱管理命令
    username_parser = subparsers.add_parser('username', help='发件人邮箱管理')
    username_parser.add_argument('--save', action='store_true', help='保存发件人邮箱到 keyring')
    username_parser.add_argument('--delete', action='store_true', help='删除保存的发件人邮箱')
    username_parser.add_argument('--email', help='发件人邮箱地址')

    # 密码管理命令
    password_parser = subparsers.add_parser('password', help='密码管理')
    password_parser.add_argument('--save', action='store_true', help='保存密码到 keyring')
    password_parser.add_argument('--delete', action='store_true', help='删除保存的密码')
    password_parser.add_argument('--password', help='密码内容')

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
    # 移除 --password 和 --save-pwd 参数，强制使用 keyring

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

        # 显示 keyring 中的邮箱
        keyring = KeyringManager()
        stored_username = keyring.get_username()
        if stored_username:
            print(f"\nkeyring 中的发件人邮箱: {stored_username}")
        else:
            print(f"\nkeyring 中的发件人邮箱: 未设置")

        print("\n使用以下命令配置:")
        print("  python send_email.py smtp --host smtp.gd.chinamobile.com --port 587")
        print("  python send_email.py sender --name 'Your Name'")
        print("  python send_email.py username --save --email your-email@gd.chinamobile.com")
        print("  python send_email.py password --save")

    elif args.command == 'smtp':
        config.update_smtp(args.host, args.port, not args.no_tls)

    elif args.command == 'sender':
        config.update_sender(args.name)

    elif args.command == 'username':
        keyring = KeyringManager()

        if args.save:
            email = args.email
            if not email:
                print("请输入发件人邮箱:")
                email = input().strip()
            if email:
                keyring.set_username(email)
            else:
                print("✗ 邮箱不能为空")

        elif args.delete:
            keyring.delete_username()

        else:
            # 显示当前邮箱状态
            stored_username = keyring.get_username()
            if stored_username:
                print(f"✓ 已保存发件人邮箱到 keyring: {stored_username}")
            else:
                print(f"✗ 未保存发件人邮箱到 keyring")
                print(f"默认邮箱: user@gd.chinamobile.com")

    elif args.command == 'password':
        keyring = KeyringManager()
        email = keyring.get_username() or "user@gd.chinamobile.com"

        if args.save:
            password = args.password
            if not password:
                print(f"请输入密码 (邮箱: {email}):")
                password = input().strip()
            if password:
                keyring.set_password(email, password)
            else:
                print("✗ 密码不能为空")

        elif args.delete:
            keyring.delete_password(email)

        else:
            # 显示当前密码状态
            stored_pwd = keyring.get_password(email)
            if stored_pwd:
                print(f"✓ 已保存密码到 keyring (邮箱: {email})")
            else:
                print(f"✗ 未保存密码 (邮箱: {email})")

    elif args.command == 'send':
        # 创建发送器（自动从 keyring 获取邮箱和密码）
        sender = EmailSender(config)

        # 检查发件人邮箱和密码
        email = sender.sender_config.get('email', '')
        if not email:
            print("\n✗ 未找到发件人邮箱，请先运行以下命令：")
            print("   python send_email.py username --save")
            sys.exit(1)

        if not sender.password:
            print(f"\n✗ 未找到密码，请先运行以下命令：")
            print(f"   python send_email.py password --save")
            print(f"\n发件人邮箱: {email}")
            sys.exit(1)

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
