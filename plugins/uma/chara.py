import importlib
import os
from nonebot import logger
from nonebot.plugin import on_command
import pygtrie
from fuzzywuzzy import fuzz
from nonebot.adapters.onebot.v11 import Bot
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11.event import MessageEvent
from plugins.uma.plugins.uma_gacha import gacha
import utils
from utils import R
import difflib
from nonebot.adapters.onebot.v11 import  MessageSegment
from .uma_res_data import UMA_DATA
from .import uma_res_data 

UNKNOWN = 1000
UnavailableChara = {
}

class Roster:

    def __init__(self):
        self._roster = pygtrie.CharTrie()
        self.update()

    def update(self):
        importlib.reload(uma_res_data)
        self._roster.clear()
        for idx, names in uma_res_data.CHARA_NAME.items():
            names_list=[]
            names_list.append(names)
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
        if score==0:
            return UNKNOWN, name, score
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
        a = a[0]
        b = fuzz.ratio(query,a)
    else :
        a = "未知角色"
        b = 0
    logger.info(f'匹配结果 {a} 相似度{b}')
    return a,b

def name2id(name):
    return roster.get_id(name)

def fromid(id_ ):
    return Chara(id_)

def fromname(name):
    id_ = name2id(name)
    return Chara(id_)

def guess_id(name):
    """@return: id, name, score"""
    return roster.guess_id(name)

class Chara:

    def __init__(self, id_):
        self.id = id_


    @property
    def name(self):
        names_list=[]
        names_list.append(uma_res_data.CHARA_NAME[self.id])
        return uma_res_data.CHARA_NAME[self.id][0] if self.id in uma_res_data.CHARA_NAME else uma_res_data.CHARA_NAME[UNKNOWN][0]


    @property
    def icon(self):
        icon_path=f'resources\\uma\\img\\unit\\icon_unit_{self.id}.png'
        UMA_DATA.chara_icon_download(self.id)
        try:
            f = open(icon_path,"rb")
            img= f.read()   
            f.close()
            res = MessageSegment.image(file =img ,cache=False,)
        except:
            logger.error("No such file or directory")
            res = R.img(f'priconne/unit/icon_unit_{UNKNOWN}31.png')
        return res




matcher = on_command("下载马娘角色头像", permission=SUPERUSER, priority=5)

@matcher.handle()
async def download_pcr_chara_icon(bot: Bot,event:MessageEvent):
    try:
        id = roster.get_id(event.message.extract_plain_text().strip("下载马娘角色头像 "))
        assert id != UNKNOWN, '未知角色名'
        UMA_DATA.chara_icon_download(id)
        await matcher.send(f'ok')
    except Exception as e:
        logger.exception(e)
        await matcher.send(f'Error: {type(e)}')


matcher = on_command("更新马娘资源", permission=SUPERUSER, priority=5)

@matcher.handle()
async def update_uma_data():
    try:
        UMA_DATA.update_chara_res()
        UMA_DATA.update_card_res()
        UMA_DATA.update_pool2()
        UMA_DATA.update_uma_alias()
        roster.update()
        importlib.reload(gacha)
        path = os.path.join(os.path.join(os.path.dirname(__file__), '__pycache__'),'temp.py')
        with open(path, "w",encoding="utf-8") as f:
            f.write("m")
            f.close
        await matcher.send('ok')
    except Exception as e:
        logger.exception(e)
        await matcher.send(f'Error: {type(e)}')
