#!/data/data/com.termux/files/usr/bin/python
import random, math, sys, os, smtplib
from email.mime.text import MIMEText
from datetime import date, datetime, timezone, timedelta
from jinja2 import Environment, FileSystemLoader, select_autoescape
import subprocess
from weasyprint import HTML
from itertools import batched

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


def html2img(inx, lst):
    env = Environment(
        loader=FileSystemLoader("templates"),
        autoescape=select_autoescape(["html", "htm"]),
    )
    html_body = env.get_template("t2.html").render(
        lst=lst,  # 二维列表，每项：[红球..., 蓝球]
    )
    # return html_body
    # 1. HTML → PDF
    HTML(string=html_body).write_pdf(f"/storage/emulated/0/SSQ/.data/{inx}.pdf")

    # 2. PDF → PNG（用 mutool draw，Termux 预编译好的）
    subprocess.run(
        [
            "mutool",
            "draw",
            "-o",
            f"/storage/emulated/0/SSQ/.data/{inx}.png",
            "-r",
            "200",
            f"/storage/emulated/0/SSQ/.data/{inx}.pdf",
        ],
        check=True,
    )


lst = shuangSeQiu()
groups = list(batched(lst, 5))
for i, v in enumerate(groups, 1):
    ret = html2img(i, v)
    for j in v:
        print(j)

# print("完成，生成 page_1.png")
# os.system("clear")
