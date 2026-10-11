#!/data/data/com.termux/files/usr/bin/python
import random, math, sys, os, smtplib
from email.mime.text import MIMEText
from datetime import date

now = date.today().timetuple()[:3]
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
    html_table = """
        <table border="1" cellpadding="6" cellspacing="0" style="border-collapse: collapse;">
          <tr><th>序号</th><th>红球</th><th>蓝球</th></tr>

"""
    for index, value in enumerate(lst, start=1):
        bgc = "#fff3cd" if index % 2 == 0 else "#f2f2f2"
        s = f"          <tr style='background-color: {bgc};'><td><span style='display:inline-block; background-color:#000000; color:#fff; text-decoration: none; padding:3px 10px; border-radius:12px; font-size:14px; font-weight:bold;'>第{index}注</span></td><td><span style='display:inline-block; background-color:#E41E31; color:#fff; text-decoration: none; padding:3px 10px; border-radius:12px; font-size:14px; font-weight:bold;'>{',  '.join(value[:-1])}</span></td><td><span style='display:inline-block; background-color:#0055AA; color:#fff; text-decoration: none; padding:3px 10px; border-radius:12px; font-size:14px; font-weight:bold;'>{''.join(value[-1])}</span></td>\n"
        html_table += s
    html_table += "      </table>"

    html_body = f"""
<html>
  <body>
    <h3>{date.today()}</h3>
    <div style="text-align: center;">
      {html_table}
    </div>
  </body>
</html>"""

    #print(html_body)
    sender = os.environ.get('SENDER')  # 你的QQ邮箱
    auth_code = os.environ.get('MAIL_PASSWORD') # 改为从环境变量获取，不再明文写密码
    receiver = os.environ.get('RECEIVER')  # 收件人
    print(sender, auth_code, receiver)
    msg = MIMEText(html_body, "html", "utf-8")
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = title
    if push:
        with smtplib.SMTP_SSL("smtp.qq.com", 465) as server:
            server.login(sender, auth_code)
            server.sendmail(sender, receiver, msg.as_string())

        #print("发送成功",lst)


ret = shuangSeQiu()
os.system("clear")
push_email("双色球定时任务", ret, True)
