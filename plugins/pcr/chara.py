import importlib
from io import BytesIO
import os
from nonebot.adapters.onebot.v11.event import MessageEvent
from nonebot import logger
from nonebot.plugin import on_command
import pygtrie
import requests
from fuzzywuzzy import process,fuzz
from PIL import Image
from nonebot.adapters.onebot.v11 import Bot
from nonebot.permission import SUPERUSER
import utils
from . import pcr_data
from utils import R
import difflib

UNKNOWN = 1000
UnavailableChara = {
    1067,  # 穗希
    1069,  # 霸瞳
    1072,  # 可萝爹
    1073,  # 拉基拉基
    1102,  # 泳装大眼
    1183,  # 星弓星
    1184,  # 星弓栞
    1204,1205,1206,#(小小甜心)
    1164,1194,1195,1196,1197,1200,1201,1202,1203#(未实装)
}

try:
    gadget_equip = R.img('priconne/gadget/equip.png').open()
    gadget_star = R.img('priconne/gadget/star.png').open()
    gadget_star_dis = R.img('priconne/gadget/star_disabled.png').open()
    gadget_star_pink = R.img('priconne/gadget/star_pink.png').open()
    unknown_chara_icon = R.img(f'priconne/unit/icon_unit_{UNKNOWN}31.png').open()
except Exception as e:
    print(e)


class Roster:

    def __init__(self):
        self._roster = pygtrie.CharTrie()
        self.update()

    def update(self):
        importlib.reload(pcr_data)
        self._roster.clear()
        for idx, names in pcr_data.CHARA_NAME.items():
            for n in names:
                n = utils.normalize_str(n)
                if n not in self._roster:
                    self._roster[n] = idx
                else:
                    logger.warning(f'priconne.chara.Roster: 出现重名{n}于id{idx}与id{self._roster[n]}')
        self._all_name_list = self._roster.keys()

    def get_id(self, name):
        name = utils.normalize_str(name)
        return self._roster[name] if name in self._roster else UNKNOWN

    def guess_id(self, name):
        """@return: id, name, score"""
        #name, score = process.extractOne(name, self._all_name_list, processor=utils.normalize_str)
        name, score = match(name, self._all_name_list)
        return self._roster[name], name, score

    def parse_team(self, namestr):
        """@return: List[ids], unknown_namestr"""
        namestr = utils.normalize_str(namestr.strip())
        team = []
        unknown = []
        while namestr:
            item = self._roster.longest_prefix(namestr)
            if not item:
                unknown.append(namestr[0])
                namestr = namestr[1:].lstrip()
            else:
                team.append(item.value)
                namestr = namestr[len(item.key):].lstrip()
        return team, ''.join(unknown)


roster = Roster()

def match(query, choices):
    query=utils.normalize_str(query)
    a = difflib.get_close_matches(query,choices,1,cutoff=0.6)
    if a  :
        a=a[0]
    else :
        a=choices[0]
    b=fuzz.ratio(query,a)
    logger.info(f'匹配结果 {a} 相似度{b}')
    return a,b

def name2id(name):
    return roster.get_id(name)


def fromid(id_, star=0, equip=0):
    return Chara(id_, star, equip)


def fromname(name, star=0, equip=0):
    id_ = name2id(name)
    return Chara(id_, star, equip)


def guess_id(name):
    """@return: id, name, score"""
    return roster.guess_id(name)


def is_npc(id_):
    if id_ in UnavailableChara:
        return True
    else:
        return not ((1000 < id_ < 1214) or (1700 < id_ < 1900))


def gen_team_pic(team, size=64, star_slot_verbose=True):
    num = len(team)
    des = Image.new('RGBA', (num * size, size), (255, 255, 255, 255))
    for i, chara in enumerate(team):
        src = chara.render_icon(size, star_slot_verbose)
        des.paste(src, (i * size, 0), src)
    return des


def download_chara_icon(id_, star):
    url = f'https://redive.estertion.win/icon/unit/{id_}{star}1.webp'
    save_path = R.img(f'priconne/unit/icon_unit_{id_}{star}1.png').path
    if os.path.exists(save_path):
            logger.info(f'chara icon {save_path}已存在')
            return
    logger.info(f'Downloading chara icon from {url}')
    try:
        rsp = requests.get(url, stream=True, timeout=20)
        if 200 == rsp.status_code:
            img = Image.open(BytesIO(rsp.content))
            img.save(save_path)
            logger.info(f'Saved to {save_path}')
        else:
            logger.error(f'Failed to download {url}. HTTP {rsp.status_code}')
    except Exception as e:
        logger.error(f'Failed to download {url}. {type(e)}')
        #logger.exception(e)
    


def download_chara_card(id_, star):
    url = f'https://redive.estertion.win/card/full/{id_}{star}1.webp'
    save_path = R.img(f'priconne/card/{id_}{star}1.png').path
    if os.path.exists(save_path):
            logger.info(f'chara card {save_path}已存在') 
            return
    logger.info(f'Downloading chara card from {url}')
    try:
        rsp = requests.get(url, stream=True, timeout=10)
        if 200 == rsp.status_code:
            img = Image.open(BytesIO(rsp.content))
            img.save(save_path)
            logger.info(f'Saved to {save_path}')
        else:
            logger.error(f'Failed to download {url}. HTTP {rsp.status_code}')
    except Exception as e:
        logger.error(f'Failed to download {url}. {type(e)}')
        #logger.exception(e)

class Chara:

    def __init__(self, id_, star=0, equip=0):
        self.id = id_
        self.star = star
        self.equip = equip

    @property
    def name(self):
        return pcr_data.CHARA_NAME[self.id][0] if self.id in pcr_data.CHARA_NAME else pcr_data.CHARA_NAME[UNKNOWN][0]

    @property
    def is_npc(self) -> bool:
        return is_npc(self.id)

    @property
    def icon(self):
        star = '3' if 1 <= self.star <= 5 else '6'
        res = R.img(f'priconne/unit/icon_unit_{self.id}{star}1.png')
        if not res.exist:
            res = R.img(f'priconne/unit/icon_unit_{self.id}31.png')
        if not res.exist:
            res = R.img(f'priconne/unit/icon_unit_{self.id}11.png')
        if not res.exist:  # FIXME: 不方便改成异步请求
            download_chara_icon(self.id, 6)
            download_chara_icon(self.id, 3)
            download_chara_icon(self.id, 1)
            res = R.img(f'priconne/unit/icon_unit_{self.id}{star}1.png')
        if not res.exist:
            res = R.img(f'priconne/unit/icon_unit_{self.id}31.png')
        if not res.exist:
            res = R.img(f'priconne/unit/icon_unit_{self.id}11.png')
        if not res.exist:
            res = R.img(f'priconne/unit/icon_unit_{UNKNOWN}31.png')
        return res

    @property
    def card(self):
        star = '3' if 1 <= self.star <= 5 else '6'
        res = R.img(f'priconne/card/{self.id}{star}1.png')
        if not res.exist:
            res = R.img(f'priconne/card/{self.id}31.png')
        if not res.exist:
            res = R.img(f'priconne/card/{self.id}11.png')
        if not res.exist:  # FIXME: 不方便改成异步请求
            download_chara_card(self.id, 6)
            download_chara_card(self.id, 3)
            download_chara_card(self.id, 1)
            res = R.img(f'priconne/card/{self.id}{star}1.png')
        if not res.exist:
            res = R.img(f'priconnecard/{self.id}31.png')
        if not res.exist:
            res = R.img(f'priconne/card/{self.id}11.png')
        if not res.exist:
            res = R.img(f'priconne/card/{self.id}31.png')
        if not res.exist:
            res = R.img(f'priconne/card/{self.id}11.png')
        return res

    def render_icon(self, size, star_slot_verbose=True) -> Image:
        try:
            pic = self.icon.open().convert('RGBA').resize((size, size), Image.LANCZOS)
        except FileNotFoundError:
            logger.error(f'File not found: {self.icon.path}')
            pic = unknown_chara_icon.convert('RGBA').resize((size, size), Image.LANCZOS)

        l = size // 6
        star_lap = round(l * 0.15)
        margin_x = (size - 6 * l) // 2
        margin_y = round(size * 0.05)
        if self.star:
            for i in range(5 if star_slot_verbose else min(self.star, 5)):
                a = i * (l - star_lap) + margin_x
                b = size - l - margin_y
                s = gadget_star if self.star > i else gadget_star_dis
                s = s.resize((l, l), Image.LANCZOS)
                pic.paste(s, (a, b, a + l, b + l), s)
            if 6 == self.star:
                a = 5 * (l - star_lap) + margin_x
                b = size - l - margin_y
                s = gadget_star_pink
                s = s.resize((l, l), Image.LANCZOS)
                pic.paste(s, (a, b, a + l, b + l), s)
        if self.equip:
            l = round(l * 1.5)
            a = margin_x
            b = margin_x
            s = gadget_equip.resize((l, l), Image.LANCZOS)
            pic.paste(s, (a, b, a + l, b + l), s)
        return pic


matcher = on_command("重载花名册", permission=SUPERUSER, priority=5)


@matcher.handle()
async def reload_pcr_chara():
    try:
        roster.update()
        await matcher.send('ok')
    except Exception as e:
        logger.exception(e)
        await matcher.send(f'Error: {type(e)}')


matcher = on_command("下载角色头像", permission=SUPERUSER, priority=5)


@matcher.handle()
async def download_pcr_chara_icon(bot: Bot,event:MessageEvent):
    try:
        id_ = roster.get_id(event.message.extract_plain_text().strip("下载角色头像 "))
        assert id_ != UNKNOWN, '未知角色名'
        download_chara_icon(id_, 6)
        download_chara_icon(id_, 3)
        download_chara_icon(id_, 1)
        await matcher.send('ok')
    except Exception as e:
        logger.exception(e)
        await matcher.send(f'Error: {type(e)}')
