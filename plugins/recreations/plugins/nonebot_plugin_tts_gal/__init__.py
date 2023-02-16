from pathlib import Path
from nonebot import on_message, get_driver, on_command
from nonebot.plugin import PluginMetadata
from nonebot.adapters.onebot.v11.message import MessageSegment
from nonebot.adapters.onebot.v11 import Bot, MessageEvent

from nonebot.log import logger

import hashlib
import random
import string
from nonebot.exception import ActionFailed, NetworkError
from .depends import *
from .initial import *
from .config import *
from torch import no_grad, LongTensor
from .utils import *
from .models import SynthesizerTrn
from .function import *
from .text.symbols import symbols_ja, symbols_zh_CHS
from scipy.io.wavfile import write
import asyncio
import traceback
from plugins.uma import chara

__plugin_meta__ = PluginMetadata(
    name="gal角色语音",
    description="部分gal角色文本转语音",
    usage="触发方式：@机器人 [角色名][发送|说][文本内容]",
    extra={
        "example": "@机器人 宁宁说おはようございます.",
        "author": "dpm12345 <1006975692@qq.com>",
        "version": "0.3.6",
    },
)

symbols_dict = {
    "zh-CHS": symbols_zh_CHS,
    "ja": symbols_ja
}

plugin_config = Config.parse_obj(get_driver().config)
auto_delete_voice = plugin_config.auto_delete_voice if not plugin_config.auto_delete_voice == None else True
tts_gal = eval(plugin_config.tts_gal if plugin_config.tts_gal else '{():[""]}')
driver = get_driver()
__valid_names__ = []


@driver.on_startup
def _():
    logger.info("正在检查目录是否存在...")
    asyncio.ensure_future(checkDir(data_path, base_path, voice_path))
    filenames = []
    [filenames.append(model[0])
     for model in tts_gal.values() if not model[0] in filenames]
    logger.info("正在检查配置文件是否存在...")
    asyncio.ensure_future(checkFile(model_path, config_path, filenames, tts_gal, __plugin_meta__, __valid_names__))
    logger.info("正在检查配置项...")
    asyncio.ensure_future(checkEnv(Config.parse_obj(get_driver().config)))


async def voice_async(text,index,net_g_ms,filename,hps_ms):
    try:
        logger.info("正在生成中22")
        with no_grad():
            logger.info("正在生成中33")
            x_tst = text.unsqueeze(0)
            logger.info("正在生成中44")
            x_tst_lengths = LongTensor([text.size(0)])
            logger.info("正在生成中55")
            sid = LongTensor([index]) if not index == None else None
            logger.info("正在生成中66")
            #loop2 = asyncio.get_event_loop()
            #audio = loop2.create_task(net_g_ms.infer(x_tst, x_tst_lengths, sid=sid, noise_scale=.667,noise_scale_w=0.8, length_scale=1))
            #loop2.run_until_complete(audio)
            #logger.info("正在生成中666")
            audio = await net_g_ms.infer(x_tst, x_tst_lengths, sid=sid, noise_scale=.667,noise_scale_w=0.8, length_scale=1)
            logger.info("正在生成中666")
            audio = audio[0][0, 0].data.cpu().float().numpy()

            #audio = net_g_ms.infer(x_tst, x_tst_lengths, sid=sid, noise_scale=.667,noise_scale_w=0.8, length_scale=1)[0][0, 0].data.cpu().float().numpy()
            logger.info("正在生成中77")
        write(voice_path / filename, hps_ms.data.sampling_rate, audio)
        logger.info("正在生成中88")
        new_voice = Path(change_by_decibel(voice_path / filename, voice_path, plugin_config.decibel))
        logger.info("正在生成中99")
        return new_voice
    except IndexError as e:
        logger.error(str(e))
        return None



voice = on_message(
    regex(r"(?P<name>\S+?)(?:说|发送)(?P<text>.*?)$"), block=True, priority=5)


@voice.handle()
async def voicHandler(
    bot: Bot, event: MessageEvent,
    name: str = RegexArg("name"),
    text: str = RegexArg("text")
):
    # 预处理

    id_ = chara.name2id(name)
    confi = 100
    if id_ == chara.UNKNOWN:
        id_, guess_name, confi = chara.guess_id(name)
    c = chara.fromid(id_)
    if confi < 80:
        name = name
    else:
        name = c.name

    config_file, model_file, index = check_character(name, __valid_names__, tts_gal)
    if config_file == "":
        return
        #await voice.finish(MessageSegment.at(event.get_user_id()) + "暂时还未有该角色")
    if len(text)>50:
        await voice.finish(MessageSegment.at(event.get_user_id()) + "要说的话太长了哦~")

    first_name = "".join(random.sample([x for x in string.ascii_letters + string.digits], 8))
    filename = hashlib.md5(first_name.encode()).hexdigest() + ".mp3"
    # 加载配置文件
    hps_ms = get_hparams_from_file(config_path / config_file)

    # 翻译的目标语言
    lang = load_language(hps_ms)
    symbols = load_symbols(hps_ms, lang, symbols_dict)

    # 文本处理
    text = changeE2C(text) if lang == "zh-CHS" else changeC2E(text)
    text = await translate_youdao(text, lang)
    text = get_text(text, hps_ms, symbols, lang, False)

    try:
        logger.info("加载模型中...")
        net_g_ms = SynthesizerTrn(
            len(symbols),
            hps_ms.data.filter_length // 2 + 1,
            hps_ms.train.segment_size // hps_ms.data.hop_length,
            n_speakers=hps_ms.data.n_speakers,
            **hps_ms.model)
        _ = net_g_ms.eval()
        load_checkpoint(model_path / model_file, net_g_ms)
    except:
        traceback.print_exc()
        await voice.finish("加载模型失败")

    try:
        logger.info("正在生成中...")
        '''
        task = asyncio.create_task(voice_async(text,index,net_g_ms,filename,hps_ms))
        logger.info("正在生成中11")
        task_voice = await task 
        new_voice = task_voice'''

        new_voice = await voice_async(text,index,net_g_ms,filename,hps_ms)
    except:
        traceback.print_exc()
        await voice.finish('生成失败')

    try:
        await voice.send(MessageSegment.record(file=new_voice))
    except ActionFailed:
        traceback.print_exc()
        await voice.send("发送失败,请重试")
    except NetworkError:
        traceback.print_exc()
        await voice.send("发送超时,也许等等就好了")
    finally:
        if auto_delete_voice:
            os.remove(new_voice)


