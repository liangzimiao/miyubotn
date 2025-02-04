from typing import Optional
from pathlib import Path
from pydantic import Extra, BaseModel
import os
from nonebot.log import logger
import copy


def check_character(name, valid_names, tts_gal):
    index = None
    model_name = ""
    for names, model in tts_gal.items():
        if names in valid_names and ((isinstance(names,str) and names == name) or name in names):
            model_name= model[0] 
            index = None if len(model) == 1 else int(model[1])
            break
    return  model_name, index

async def checkFile(tts_gal,plugin_meta,valid_names):
    '''添加目前检测出来的可以使用的角色语音'''
    valid_character_names_list = [name for name,model in tts_gal.items()]
    valid_names += valid_character_names_list
    valid_character_names = []
    for name in valid_character_names_list:
        if isinstance(name,str):
            valid_character_names.append(name)
        else:
            valid_character_names.append("/".join(name))
    if len(valid_character_names):
        plugin_meta.usage = plugin_meta.usage + "\n目前可使用的语音角色：\n" + "\n".join(valid_character_names)
    else:
        plugin_meta.usage = plugin_meta.usage + "\n目前无可使用的语音角色\n"


tts_gal = {
    ("亚托莉","ATRI","atri",): ["ATRI",0],
    ("绫地宁宁", "宁宁",): ["YuzuSoft",0],
    ("因幡爱瑠", "爱瑠"): ["YuzuSoft",1],
    ("朝武芳乃", "芳乃"): ["YuzuSoft",2],
    ("常陸茉子", "茉子"): ["YuzuSoft",3],
    ("丛雨", "幼刀"): ["YuzuSoft",4],
    ("鞍马小春", "鞍馬小春", "小春"): ["YuzuSoft",5],
    ("在原七海", "七海"): ["YuzuSoft",6],
    ("特别周",): ["uma87",0],
    ("无声铃鹿",): ["uma87",1],
    ("东海帝皇",): ["uma87",2],
    ("丸善斯基",): ["uma87",3],
    ("富士奇迹",): ["uma87",4],
    ("小栗帽",): ["uma87",5],
    ("黄金船",): ["uma87",6],
    ("伏特加",): ["uma87",7],
    ("大和赤骥",): ["uma87",8],
    ("大树快车",): ["uma87",9],
    ("草上飞",): ["uma87",10],
    ("菱亚马逊",): ["uma87",11],
    ("目白麦昆",): ["uma87",12],
    ("神鹰",): ["uma87",13],
    ("好歌剧",): ["uma87",14],
    ("成田白仁",): ["uma87",15],
    ("鲁道夫象征",): ["uma87",16],
    ("气槽",): ["uma87",17],
    ("爱丽数码",): ["uma87",18],
    ("青云天空",): ["uma87",19],
    ("玉藻十字",): ["uma87",20],
    ("美妙姿势",): ["uma87",21],
    ("琵琶晨光",): ["uma87",22],
    ("摩耶重炮",): ["uma87",23],
    ("曼城茶座",): ["uma87",24],
    ("美浦波旁",): ["uma87",25],
    ("目白赖恩",): ["uma87",26],
    ("菱曙",): ["uma87",27],
    ("雪之美人",): ["uma87",28],
    ("米浴",): ["uma87",29],
    ("艾尼斯风神",): ["uma87",30],
    ("爱丽速子",): ["uma87",31],
    ("爱慕织姬",): ["uma87",32],
    ("稻荷一",): ["uma87",33],
    ("胜利奖券",): ["uma87",34],
    ("空中神宫",): ["uma87",35],
    ("荣进闪耀",): ["uma87",36],
    ("真机伶",): ["uma87",37],
    ("川上公主",): ["uma87",38],
    ("黄金城",): ["uma87",39],
    ("樱花进王",): ["uma87",40],
    ("采珠",): ["uma87",41],
    ("新光风",): ["uma87",42],
    ("东商变革",): ["uma87",43],
    ("超级小海湾",): ["uma87",44],
    ("醒目飞鹰",): ["uma87",45],
    ("荒漠英雄",): ["uma87",46],
    ("东瀛佐敦",): ["uma87",47],
    ("中山庆典",): ["uma87",48],
    ("成田大进",): ["uma87",49],
    ("西野花",): ["uma87",50],
    ("春乌拉拉",): ["uma87",51],
    ("青竹回忆",): ["uma87",52],
    ("微光飞驹",): ["uma87",53],
    ("美丽周日",): ["uma87",54],
    ("待兼福来",): ["uma87",55],
    ("千明代表",): ["uma87",56],
    ("名将怒涛",): ["uma87",57],
    ("目白多伯",): ["uma87",58],
    ("优秀素质",): ["uma87",59],
    ("帝王光辉",): ["uma87",60],
    ("待兼诗歌剧",): ["uma87",61],
    ("生野狄杜斯",): ["uma87",62],
    ("目白善信",): ["uma87",63],
    ("大拓太阳神",): ["uma87",64],
    ("双涡轮",): ["uma87",65],
    ("里见光钻",): ["uma87",66],
    ("北部玄驹",): ["uma87",67],
    ("樱花千代王",): ["uma87",68],
    ("天狼星象征",): ["uma87",69],
    ("目白阿尔丹",): ["uma87",70],
    ("八重无敌",): ["uma87",71],
    ("鹤丸刚志",): ["uma87",72],
    ("目白光明",): ["uma87",73],
    ("樱花桂冠",): ["uma87",74],
    ("成田路",): ["uma87",75],
    ("也文摄辉",): ["uma87",76],
    ("吉兆",): ["uma87",77],
    ("谷野美酒",): ["uma87",78],
    ("第一红宝石",): ["uma87",79],
    ("真弓快车",): ["uma87",80],
    ("骏川手纲","绿帽"): ["uma87",81],
    ("凯斯奇迹",): ["uma87",82],
    ("小林历奇",): ["uma87",83],
    ("北港火山",): ["uma87",84],
    ("奇锐骏",): ["uma87",85],
    ("秋川理事长","理事长"): ["uma87",86],
    
    ("特别周_zh",): ["genshin_honkai",0],
    ("无声铃鹿_zh",): ["genshin_honkai",1],
    ("东海帝王_zh",): ["genshin_honkai",2],
    ("丸善斯基_zh",): ["genshin_honkai",3],
    ("富士奇迹_zh",): ["genshin_honkai",4],
    ("小栗帽_zh",): ["genshin_honkai",5],
    ("黄金船_zh",): ["genshin_honkai",6],
    ("伏特加_zh",): ["genshin_honkai",7],
    ("大和赤骥_zh",): ["genshin_honkai",8],
    ("大树快车_zh",): ["genshin_honkai",9],
    ("草上飞_zh",): ["genshin_honkai",10],
    ("菱亚马逊_zh",): ["genshin_honkai",11],
    ("目白麦昆_zh",): ["genshin_honkai",12],
    ("神鹰_zh",): ["genshin_honkai",13],
    ("好歌剧_zh",): ["genshin_honkai",14],
    ("成田白仁_zh",): ["genshin_honkai",15],
    ("鲁道夫象征_zh",): ["genshin_honkai",16],
    ("气槽_zh",): ["genshin_honkai",17],
    ("爱丽数码_zh",): ["genshin_honkai",18],
    ("星云天空_zh",): ["genshin_honkai",19],
    ("玉藻十字_zh",): ["genshin_honkai",20],
    ("美妙姿势_zh",): ["genshin_honkai",21],
    ("琵琶晨光_zh",): ["genshin_honkai",22],
    ("摩耶重炮_zh",): ["genshin_honkai",23],
    ("曼城茶座_zh",): ["genshin_honkai",24],
    ("美浦波旁_zh",): ["genshin_honkai",25],
    ("目白赖恩_zh",): ["genshin_honkai",26],
    ("菱曙_zh",): ["genshin_honkai",27],
    ("雪中美人_zh",): ["genshin_honkai",28],
    ("米浴_zh",): ["genshin_honkai",29],
    ("艾尼斯风神_zh",): ["genshin_honkai",30],
    ("爱丽速子_zh",): ["genshin_honkai",31],
    ("爱慕织姬_zh",): ["genshin_honkai",32],
    ("稻荷一_zh",): ["genshin_honkai",33],
    ("胜利奖券_zh",): ["genshin_honkai",34],
    ("空中神宫_zh",): ["genshin_honkai",35],
    ("荣进闪耀_zh",): ["genshin_honkai",36],
    ("真机伶_zh",): ["genshin_honkai",37],
    ("川上公主_zh",): ["genshin_honkai",38],
    ("黄金城_zh",): ["genshin_honkai",39],
    ("樱花进王_zh",): ["genshin_honkai",40],
    ("采珠_zh",): ["genshin_honkai",41],
    ("新光风_zh",): ["genshin_honkai",42],
    ("东商变革_zh",): ["genshin_honkai",43],
    ("超级小海湾_zh",): ["genshin_honkai",44],
    ("醒目飞鹰_zh",): ["genshin_honkai",45],
    ("荒漠英雄_zh",): ["genshin_honkai",46],
    ("东瀛佐敦_zh",): ["genshin_honkai",47],
    ("中山庆典_zh",): ["genshin_honkai",48],
    ("成田大进_zh",): ["genshin_honkai",49],
    ("西野花_zh",): ["genshin_honkai",50],
    ("春丽乌拉拉_zh",): ["genshin_honkai",51],
    ("青竹回忆_zh",): ["genshin_honkai",52],
    ("微光飞驹_zh",): ["genshin_honkai",53],
    ("美丽周日_zh",): ["genshin_honkai",54],
    ("待兼福来_zh",): ["genshin_honkai",55],
    ("千明代表_zh",): ["genshin_honkai",56],
    ("名将怒涛_zh",): ["genshin_honkai",57],
    ("目白多伯_zh",): ["genshin_honkai",58],
    ("优秀素质_zh",): ["genshin_honkai",59],
    ("帝王光辉_zh",): ["genshin_honkai",60],
    ("待兼诗歌剧_zh",): ["genshin_honkai",61],
    ("生野狄杜斯_zh",): ["genshin_honkai",62],
    ("目白善信_zh",): ["genshin_honkai",63],
    ("大拓太阳神_zh",): ["genshin_honkai",64],
    ("双涡轮_zh",): ["genshin_honkai",65],
    ("里见光钻_zh",): ["genshin_honkai",66],
    ("北部玄驹_zh",): ["genshin_honkai",67],
    ("樱花千代王_zh",): ["genshin_honkai",68],
    ("天狼星象征_zh",): ["genshin_honkai",69],
    ("目白阿尔丹_zh",): ["genshin_honkai",70],
    ("八重无敌_zh",): ["genshin_honkai",71],
    ("鹤丸刚志_zh",): ["genshin_honkai",72],
    ("目白光明_zh",): ["genshin_honkai",73],
    ("成田路_zh",): ["genshin_honkai",74],
    ("也文摄辉_zh",): ["genshin_honkai",75],
    ("小林历奇_zh",): ["genshin_honkai",76],
    ("北港火山_zh",): ["genshin_honkai",77],
    ("奇锐骏_zh",): ["genshin_honkai",78],
    ("苦涩糖霜_zh",): ["genshin_honkai",79],
    ("小小蚕茧_zh",): ["genshin_honkai",80],
    ("骏川手纲_zh",): ["genshin_honkai",81],
    ("秋川弥生_zh",): ["genshin_honkai",82],
    ("乙名史悦子_zh",): ["genshin_honkai",83],
    ("桐生院葵_zh",): ["genshin_honkai",84],
    ("安心泽刺刺美_zh",): ["genshin_honkai",85],
    ("樫本理子_zh",): ["genshin_honkai",86],
    ("真弓快车_zh",): ["genshin_honkai",148],


    ("佩可莉姆","pecorine",): ["pecorine",10],
    ("可可萝","kokoro",): ["kokoro",0],
    ("凯露","kyaru",): ["kyaru",10],
    ("美空","misora",): ["misora",0],
    ("爱梅斯","ameth",): ["ameth",0],
    ("日和莉","hiyori",): ["hiyori",0],
    ("柏崎初音","hatsune","星法"): ["hatsune",10],
    ("惠理子","eriko",): ["eriko",0],
    ("镜华","kyoka"): ["kyoka",0],
    ("优妮",
        "ユニ",
        "Yuni",
        "真行寺由仁",
        "由仁",
        "优尼",
        "u2",
        "优妮辈先",
        "辈先",
        "书记",
        "uni",
        "先辈",
        "仙贝",
        "油腻",
        "优妮先辈",
        "学姐",
        "18岁黑丝学姐"): ["bzd4567",0],
    ("琪爱儿",
        "チエル",
        "Chieru",
        "千爱瑠",
        "切露",
        "茄露",
        "茄噜",
        "切噜"): ["bzd4567",1],
    ("克萝依",
        "クロエ",
        "Kuroe",
        "克罗依",
        "华哥",
        "黑江",
        "黑江花子",
        "花子"): ["bzd4567",2],
    
    
    ("天童爱丽丝","alice","爱丽丝",): ["ba",0],
    ("一之濑明日奈","asuna","明日奈", ): ["ba",1],
    ("白洲梓","azusa","阿梓","梓", ): ["ba",2],
    ("空崎日奈","hina","日奈", ): ["ba",3],
    ("小鸟游星野","hoshino","星野","大叔", ): ["ba",4],
    ("银镜伊织","iori","伊织", ): ["ba",5],
    ("伊吕波","iroha","168", ): ["ba",6],
    ("久田泉奈","itsuna","泉奈", ): ["ba",7],
    ("角楯花凛","karin","花凛", ): ["ba",8],
    ("圣园未花","mika","未花", ): ["ba",9],
    ("霞泽美游","miyu","美游", ): ["ba",10],
    ("砂狼白子","shiroko","白子", ): ["ba",11],
    ("早濑优香","youka","优香",): ["ba",12],

    ("天童爱丽丝_zh","alice_zh","爱丽丝_zh",): ["ba_zh",0],
    ("一之濑明日奈_zh","asuna_zh","明日奈_zh", ): ["ba_zh",1],
    ("白洲梓_zh","azusa_zh","阿梓_zh","梓_zh", ): ["ba_zh",2],
    ("空崎日奈_zh","hina_zh","日奈_zh", ): ["ba_zh",3],
    ("小鸟游星野_zh","hoshino_zh","星野_zh","大叔_zh", ): ["ba_zh",4],
    ("银镜伊织_zh","iori_zh","伊织_zh", ): ["ba_zh",5],
    ("伊吕波_zh","iroha_zh","168_zh", ): ["ba_zh",6],
    ("久田泉奈_zh","itsuna_zh","泉奈_zh", ): ["ba_zh",7],
    ("角楯花凛_zh","karin_zh","花凛_zh", ): ["ba_zh",8],
    ("圣园未花_zh","mika_zh","未花_zh", ): ["ba_zh",9],
    ("霞泽美游_zh","miyu_zh","美游_zh", ): ["ba_zh",10],
    ("砂狼白子_zh","shiroko_zh","白子_zh", ): ["ba_zh",11],
    ("早濑优香_zh","youka_zh","优香_zh",): ["ba_zh",12],


    #("刻晴","keqing",): ["keqing",115],
    #("优菈","eula",): ["eula",124],
    ("神里绫华",): ["genshin_honkai",87],
    ("琴",): ["genshin_honkai",88],
    ("空",): ["genshin_honkai",89],
    ("丽莎",): ["genshin_honkai",90],
    ("荧",): ["genshin_honkai",91],
    ("芭芭拉",): ["genshin_honkai",92],
    ("凯亚",): ["genshin_honkai",93],
    ("迪卢克",): ["genshin_honkai",94],
    ("雷泽",): ["genshin_honkai",95],
    ("安柏",): ["genshin_honkai",96],
    ("温迪",): ["genshin_honkai",97],
    ("香菱",): ["genshin_honkai",98],
    ("北斗",): ["genshin_honkai",99],
    ("行秋",): ["genshin_honkai",100],
    ("魈",): ["genshin_honkai",101],
    ("凝光",): ["genshin_honkai",102],
    ("可莉",): ["genshin_honkai",103],
    ("钟离",): ["genshin_honkai",104],
    ("菲谢尔","皇女",): ["genshin_honkai",105],
    ("班尼特",): ["genshin_honkai",106],
    ("达达利亚","公子",): ["genshin_honkai",107],
    ("诺艾尔","女仆",): ["genshin_honkai",108],
    ("七七",): ["genshin_honkai",109],
    ("重云",): ["genshin_honkai",110],
    ("甘雨","椰羊",): ["genshin_honkai",111],
    ("阿贝多",): ["genshin_honkai",112],
    ("迪奥娜",): ["genshin_honkai",113],
    ("莫娜",): ["genshin_honkai",114],
    ("刻晴",): ["genshin_honkai",115],
    ("砂糖",): ["genshin_honkai",116],
    ("辛焱",): ["genshin_honkai",117],
    ("罗莎莉亚",): ["genshin_honkai",118],
    ("胡桃",): ["genshin_honkai",119],
    ("枫原万叶","万叶",): ["genshin_honkai",120],
    ("烟绯",): ["genshin_honkai",121],
    ("宵宫",): ["genshin_honkai",122],
    ("托马",): ["genshin_honkai",123],
    ("优菈",): ["genshin_honkai",124],
    ("雷电将军","雷神",): ["genshin_honkai",125],
    ("早柚",): ["genshin_honkai",126],
    ("珊瑚宫心海","心海",): ["genshin_honkai",127],
    ("五郎",): ["genshin_honkai",128],
    ("九条裟罗",): ["genshin_honkai",129],
    ("荒泷一斗","一斗",): ["genshin_honkai",130],
    ("埃洛伊",): ["genshin_honkai",131],
    ("申鹤",): ["genshin_honkai",132],
    ("八重神子","神子",): ["genshin_honkai",133],
    ("神里绫人","绫人",): ["genshin_honkai",134],
    ("夜兰",): ["genshin_honkai",135],
    ("久岐忍",): ["genshin_honkai",136],
    ("鹿野院平藏",): ["genshin_honkai",137],
    ("提纳里",): ["genshin_honkai",138],
    ("柯莱",): ["genshin_honkai",139],
    ("多莉",): ["genshin_honkai",140],
    ("云堇",): ["genshin_honkai",141],
    ("纳西妲","草神"): ["genshin_honkai",142],
    ("深渊使徒",): ["genshin_honkai",143],
    ("妮露",): ["genshin_honkai",144],
    ("赛诺",): ["genshin_honkai",145],
    ("债务处理人",): ["genshin_honkai",146],
    ("坎蒂丝",): ["genshin_honkai",147],
    ("戴因斯雷布",): ["genshin_honkai",220],
    ("特瓦林",): ["genshin_honkai",234],

    ("派蒙",): ["genshin_honkai",202],
    #("布洛妮娅","bronya","理之律者","板鸭"): ["bronya",193],
    #("德莉莎","delisha","德丽莎"): ["delisha",205],
    ("丽塔",): ["genshin_honkai",175],
    ("失落迷迭",): ["genshin_honkai",176],
    ("缭乱星棘",): ["genshin_honkai",177],
    ("伊甸",): ["genshin_honkai",178],
    ("伏特加女孩",): ["genshin_honkai",179],
    ("狂热蓝调",): ["genshin_honkai",180],
    ("莉莉娅",): ["genshin_honkai",181],
    ("萝莎莉娅",): ["genshin_honkai",182],
    ("八重樱",): ["genshin_honkai",183],
    ("八重霞",): ["genshin_honkai",184],
    ("卡莲",): ["genshin_honkai",185],
    ("第六夜想曲",): ["genshin_honkai",186],
    ("卡萝尔",): ["genshin_honkai",187],
    ("姬子",): ["genshin_honkai",188],
    ("极地战刃",): ["genshin_honkai",189],
    ("布洛妮娅","bronya","板鸭"): ["genshin_honkai",190],
    ("次生银翼",): ["genshin_honkai",191],
    ("理之律者%26希儿",): ["genshin_honkai",192],
    ("理之律者",): ["genshin_honkai",193],
    ("迷城骇兔",): ["genshin_honkai",194],
    ("希儿",): ["genshin_honkai",195],
    ("魇夜星渊",): ["genshin_honkai",196],
    ("黑希儿",): ["genshin_honkai",197],
    ("帕朵菲莉丝",): ["genshin_honkai",198],
    ("不灭星锚",): ["genshin_honkai",199],
    ("天元骑英",): ["genshin_honkai",200],
    ("幽兰黛尔",): ["genshin_honkai",201],
    ("爱酱",): ["genshin_honkai",203],
    ("绯玉丸",): ["genshin_honkai",204],
    ("德丽莎","德莉莎","delisha",): ["genshin_honkai",205],
    ("月下初拥",): ["genshin_honkai",206],
    ("朔夜观星",): ["genshin_honkai",207],
    ("暮光骑士",): ["genshin_honkai",208],
    ("格蕾修",): ["genshin_honkai",209],
    ("梅比乌斯",): ["genshin_honkai",211],
    ("仿犹大",): ["genshin_honkai",212],
    ("克莱因",): ["genshin_honkai",213],
    ("圣剑幽兰黛尔",): ["genshin_honkai",214],
    ("妖精爱莉",): ["genshin_honkai",215],
    ("特斯拉zero",): ["genshin_honkai",216],
    ("苍玄",): ["genshin_honkai",217],
    ("若水",): ["genshin_honkai",218],
    ("西琳",): ["genshin_honkai",219],
    ("贝拉",): ["genshin_honkai",221],
    ("赤鸢",): ["genshin_honkai",222],
    ("镇魂歌",): ["genshin_honkai",223],
    ("渡鸦",): ["genshin_honkai",224],
    ("人之律者",): ["genshin_honkai",225],
    ("爱莉希雅",): ["genshin_honkai",226],
    ("天穹游侠",): ["genshin_honkai",227],
    ("琪亚娜",): ["genshin_honkai",228],
    ("空之律者",): ["genshin_honkai",229],
    ("薪炎之律者",): ["genshin_honkai",230],
    ("云墨丹心",): ["genshin_honkai",231],
    ("符华",): ["genshin_honkai",232],
    ("识之律者",): ["genshin_honkai",233],
    ("维尔薇",): ["genshin_honkai",235],
    ("芽衣",): ["genshin_honkai",236],
    ("雷之律者",): ["genshin_honkai",237],
    ("断罪影舞",): ["genshin_honkai",238],
    ("阿波尼亚",): ["genshin_honkai",239],


    ("锦木千束","chisato","千束"): ["chisato",0],
    ("井上泷奈","takina","泷奈"): ["takina",0],


    ("日语阿贝多",): ["genshin_honkai_2",300],
    ("日语埃洛伊",): ["genshin_honkai_2",301],
    ("日语安柏",): ["genshin_honkai_2",302],
    ("日语神里绫华",): ["genshin_honkai_2",303],
    ("日语神里绫人",): ["genshin_honkai_2",304],
    ("日语白术",): ["genshin_honkai_2",305],
    ("日语芭芭拉",): ["genshin_honkai_2",306],
    ("日语北斗",): ["genshin_honkai_2",307],
    ("日语班尼特",): ["genshin_honkai_2",308],
    ("日语坎蒂丝",): ["genshin_honkai_2",309],
    ("日语重云",): ["genshin_honkai_2",310],
    ("日语柯莱",): ["genshin_honkai_2",311],
    ("日语赛诺",): ["genshin_honkai_2",312],
    ("日语戴因斯雷布",): ["genshin_honkai_2",313],
    ("日语迪卢克",): ["genshin_honkai_2",314],
    ("日语迪奥娜",): ["genshin_honkai_2",315],
    ("日语多莉",): ["genshin_honkai_2",316],
    ("日语优菈",): ["genshin_honkai_2",317],
    ("日语菲谢尔",): ["genshin_honkai_2",318],
    ("日语甘雨",): ["genshin_honkai_2",319],
    ("日语五郎",): ["genshin_honkai_2",320],
    ("日语鹿野院平藏",): ["genshin_honkai_2",321],
    ("日语空",): ["genshin_honkai_2",322],
    ("日语荧",): ["genshin_honkai_2",323],
    ("日语胡桃",): ["genshin_honkai_2",324],
    ("日语一斗",): ["genshin_honkai_2",325],
    ("日语凯亚",): ["genshin_honkai_2",326],
    ("日语万叶",): ["genshin_honkai_2",327],
    ("日语刻晴",): ["genshin_honkai_2",328],
    ("日语可莉",): ["genshin_honkai_2",329],
    ("日语心海",): ["genshin_honkai_2",330],
    ("日语九条裟罗",): ["genshin_honkai_2",331],
    ("日语丽莎",): ["genshin_honkai_2",332],
    ("日语莫娜",): ["genshin_honkai_2",333],
    ("日语纳西妲",): ["genshin_honkai_2",334],
    ("日语妮露",): ["genshin_honkai_2",335],
    ("日语凝光",): ["genshin_honkai_2",336],
    ("日语诺艾尔",): ["genshin_honkai_2",337],
    ("日语奥兹",): ["genshin_honkai_2",338],
    ("日语派蒙",): ["genshin_honkai_2",339],
    ("日语琴",): ["genshin_honkai_2",340],
    ("日语七七",): ["genshin_honkai_2",341],
    ("日语雷电将军",): ["genshin_honkai_2",342],
    ("日语雷泽",): ["genshin_honkai_2",343],
    ("日语罗莎莉亚",): ["genshin_honkai_2",344],
    ("日语早柚",): ["genshin_honkai_2",345],
    ("日语散兵",): ["genshin_honkai_2",346],
    ("日语申鹤",): ["genshin_honkai_2",347],
    ("日语久岐忍",): ["genshin_honkai_2",348],
    ("日语女士",): ["genshin_honkai_2",349],
    ("日语砂糖",): ["genshin_honkai_2",350],
    ("日语达达利亚",): ["genshin_honkai_2",351],
    ("日语托马",): ["genshin_honkai_2",352],
    ("日语提纳里",): ["genshin_honkai_2",353],
    ("日语温迪",): ["genshin_honkai_2",354],
    ("日语香菱",): ["genshin_honkai_2",355],
    ("日语魈",): ["genshin_honkai_2",356],
    ("日语行秋",): ["genshin_honkai_2",357],
    ("日语辛焱",): ["genshin_honkai_2",358],
    ("日语八重神子",): ["genshin_honkai_2",359],
    ("日语烟绯",): ["genshin_honkai_2",360],
    ("日语夜兰",): ["genshin_honkai_2",361],
    ("日语宵宫",): ["genshin_honkai_2",362],
    ("日语云堇",): ["genshin_honkai_2",363],
    ("日语钟离",): ["genshin_honkai_2",364],
   
}