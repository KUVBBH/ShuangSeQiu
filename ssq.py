#!/data/data/com.termux/files/usr/bin/python
import random, math, sys, os, smtplib
from email.mime.text import MIMEText
from datetime import date, datetime, timezone, timedelta
from jinja2 import Environment, FileSystemLoader, select_autoescape

now = date.today().timetuple()[:3]
utc_now = datetime.now(timezone.utc)
bj_now = datetime.now(timezone(timedelta(hours=8)))

seed = math.prod(now)
random.seed(seed)

RED = range(1, 34)
BLUE = range(1, 16)

try:
    TOTAL = int(sys.argv[1])
except IndexError:
    TOTAL = 100


def shuangSeQiu():
    l = []
    for i in range(TOTAL):
        red = sorted(random.sample(RED, 6))
        blue = random.sample(BLUE, 1)
        result = red + blue
        seed = math.prod(result)
        random.seed(seed)
        l.append([f"{i:02d}" for i in result])
    return l


def push_email(title, lst, push=True):
    env = Environment(
        loader=FileSystemLoader("templates"),
        autoescape=select_autoescape(["html", "htm"]),
    )
    html_body = env.get_template("t.html").render(
        bj_now=bj_now,  # 直接传 datetime 对象，格式化交给模板
        utc_now=utc_now,
        lst=lst,  # 二维列表，每项：[红球..., 蓝球]
    )
    sender = os.environ.get("SENDER")  # 你的QQ邮箱
    auth_code = os.environ.get("MAIL_PASSWORD")  # 改为从环境变量获取，不再明文写密码
    receiver = os.environ.get("RECEIVER")  # 收件人
    msg = MIMEText(html_body, "html", "utf-8")
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = title
    if push:
        with smtplib.SMTP_SSL("smtp.qq.com", 465) as server:
            server.login(sender, auth_code)
            server.sendmail(sender, receiver, msg.as_string())

        # print("发送成功",lst)


ret = shuangSeQiu()
os.system("clear")
push_email("双色球定时任务", ret, True)
