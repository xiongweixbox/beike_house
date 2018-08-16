# 参考网址：https://www.jianshu.com/p/9c266216957b

# ----------------------------------------引入模块------------------------------------------------
import requests
from bs4 import BeautifulSoup
import pymongo
from pymongo import MongoClient
import math
import datetime
import re

# ---------------------------------------设置IP池-------------------------------------------------
ip_pool = {
    "",
    "",
    "",
    ""
}

# -----------------------------------------设置数据库连接-------------------------------------------

client = pymongo.MongoClient("127.0.0.1", 27017)
db = client.myinfo


# ------------------------------------------基本变量设置-----------------------------------------
base_url = 'https://bj.ke.com/'  # 北京二手房基本页
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
city = '北京'

# 所有行政区设置为变量，指定url
dongcheng = {
    # 东城区所有商圈页urls
    '安定门': 'https://bj.ke.com/ershoufang/andingmen/',  # 安定门
    '安贞': 'https://bj.ke.com/ershoufang/anzhen1/',  # 安贞
    '朝阳门外': 'https://bj.ke.com/ershoufang/chaoyangmenwai1/',  # 朝阳门外
    '朝阳门内': 'https://bj.ke.com/ershoufang/chaoyangmennei1/',  # 朝阳门内
    '崇文门': 'https://bj.ke.com/ershoufang/chongwenmen/',  # 崇文门
    '东单': 'https://bj.ke.com/ershoufang/dongdan/',  # 东单
    '东直门': 'https://bj.ke.com/ershoufang/dongzhimen/',  # 东直门
    '地安门': 'https://bj.ke.com/ershoufang/dianmen/',  # 地安门
    '东花市': 'https://bj.ke.com/ershoufang/donghuashi/',  # 东花市
    '东四': 'https://bj.ke.com/ershoufang/dongsi1/',  # 东四
    '灯市口': 'https://bj.ke.com/ershoufang/dengshikou/',  # 灯市口
    '广渠门': 'https://bj.ke.com/ershoufang/guangqumen/',  # 广渠门
    '工体': 'https://bj.ke.com/ershoufang/gongti/',  # 工体
    '和平里': 'https://bj.ke.com/ershoufang/hepingli/',  # 和平里
    '交道口': 'https://bj.ke.com/ershoufang/jiaodaokou/',  # 交道口
    '建国门外': 'https://bj.ke.com/ershoufang/jianguomenwai/',  # 建国门外
    '建国门内': 'https://bj.ke.com/ershoufang/jianguomennei/',  # 建国门内
    '金宝街': 'https://bj.ke.com/ershoufang/jinbaojie/',  # 金宝街
    '六铺炕': 'https://bj.ke.com/ershoufang/liupukang/',  # 六铺炕
    '蒲黄榆': 'https://bj.ke.com/ershoufang/puhuangyu/',  # 蒲黄榆
    '前门': 'https://bj.ke.com/ershoufang/qianmen/',  # 前门
    '陶然亭': 'https://bj.ke.com/ershoufang/taoranting1/',  # 陶然亭
    '天坛': 'https://bj.ke.com/ershoufang/tiantan/',  # 天坛
    '西罗园': 'https://bj.ke.com/ershoufang/xiluoyuan/',  # 西罗园
    '西单': 'https://bj.ke.com/ershoufang/xidan/',  # 西单
    '永定门': 'https://bj.ke.com/ershoufang/yongdingmen/',  # 永定门
    '洋桥': 'https://bj.ke.com/ershoufang/yangqiao1/',  # 洋桥
    '左安门': 'https://bj.ke.com/ershoufang/zuoanmen1/'  # 左安门
}

xicheng = {
    # 西城区所有商圈页urls
    '白纸坊': 'https://bj.ke.com/ershoufang/baizhifang1/',
    '菜户营': 'https://bj.ke.com/ershoufang/caihuying/',
    '长椿街': 'https://bj.ke.com/ershoufang/changchunjie/',
    '崇文门': 'https://bj.ke.com/ershoufang/chongwenmen/',
    '车公庄': 'https://bj.ke.com/ershoufang/chegongzhuang1/',
    '地安门': 'https://bj.ke.com/ershoufang/dianmen/',
    '德胜门': 'https://bj.ke.com/ershoufang/deshengmen/',
    '阜成门': 'https://bj.ke.com/ershoufang/fuchengmen/',
    '广安门': 'https://bj.ke.com/ershoufang/guanganmen/',
    '官园': 'https://bj.ke.com/ershoufang/guanyuan/',
    '金融街': 'https://bj.ke.com/ershoufang/jinrongjie/',
    '六铺炕': 'https://bj.ke.com/ershoufang/liupukang/',
    '马甸': 'https://bj.ke.com/ershoufang/madian1/',
    '马连道': 'https://bj.ke.com/ershoufang/maliandao1/',
    '木樨地': 'https://bj.ke.com/ershoufang/muxidi1/',
    '牛街': 'https://bj.ke.com/ershoufang/niujie/',
    '陶然亭': 'https://bj.ke.com/ershoufang/taoranting1/',
    '太平桥': 'https://bj.ke.com/ershoufang/taipingqiao1/',
    '天宁寺': 'https://bj.ke.com/ershoufang/tianningsi1/',
    '西四': 'https://bj.ke.com/ershoufang/xisi1/',
    '宣武门': 'https://bj.ke.com/ershoufang/xuanwumen12/',
    '西直门': 'https://bj.ke.com/ershoufang/xizhimen1/',
    '新街口': 'https://bj.ke.com/ershoufang/xinjiekou2/',
    '西单': 'https://bj.ke.com/ershoufang/xidan/',
    '月坛': 'https://bj.ke.com/ershoufang/yuetan/',
    '右安门内': 'https://bj.ke.com/ershoufang/youanmennei11/'
}

chaoyang = {
    # 朝阳区所有商圈页urls
    '奥林匹克公园': 'https://bj.ke.com/ershoufang/aolinpikegongyuan11/',
    '北苑': 'https://bj.ke.com/ershoufang/beiyuan2/',
    '北工大': 'https://bj.ke.com/ershoufang/beigongda/',
    '百子湾': 'https://bj.ke.com/ershoufang/baiziwan/',
    '成寿寺': 'https://bj.ke.com/ershoufang/chengshousi1/',
    '常营': 'https://bj.ke.com/ershoufang/changying/',
    '朝阳门外': 'https://bj.ke.com/ershoufang/chaoyangmenwai1/',
    'CBD': 'https://bj.ke.com/ershoufang/cbd/',
    '朝青': 'https://bj.ke.com/ershoufang/chaoqing/',
    '朝阳公园': 'https://bj.ke.com/ershoufang/chaoyanggongyuan/',
    '东直门': 'https://bj.ke.com/ershoufang/dongzhimen/',
    '东坝': 'https://bj.ke.com/ershoufang/dongba/',
    '大望路': 'https://bj.ke.com/ershoufang/dawanglu/',
    '东大桥': 'https://bj.ke.com/ershoufang/dongdaqiao/',
    '大山子': 'https://bj.ke.com/ershoufang/dashanzi/',
    '豆各庄': 'https://bj.ke.com/ershoufang/dougezhuang/',
    '定福庄': 'https://bj.ke.com/ershoufang/dingfuzhuang/',
    '方庄': 'https://bj.ke.com/ershoufang/fangzhuang1/',
    '垡头': 'https://bj.ke.com/ershoufang/fatou/',
    '广渠门': 'https://bj.ke.com/ershoufang/guangqumen/',
    '工体': 'https://bj.ke.com/ershoufang/gongti/',
    '高碑店': 'https://bj.ke.com/ershoufang/gaobeidian/',
    '国展': 'https://bj.ke.com/ershoufang/guozhan1/',
    '甘露园': 'https://bj.ke.com/ershoufang/ganluyuan/',
    '管庄': 'https://bj.ke.com/ershoufang/guanzhuang/',
    '和平里': 'https://bj.ke.com/ershoufang/hepingli/',
    '欢乐谷': 'https://bj.ke.com/ershoufang/huanlegu/',
    '惠新西街': 'https://bj.ke.com/ershoufang/huixinxijie/',
    '红庙': 'https://bj.ke.com/ershoufang/hongmiao/',
    '华威桥': 'https://bj.ke.com/ershoufang/huaweiqiao/',
    '健翔桥': 'https://bj.ke.com/ershoufang/jianxiangqiao1/',
    '酒仙桥': 'https://bj.ke.com/ershoufang/jiuxianqiao/',
    '劲松': 'https://bj.ke.com/ershoufang/jinsong/',
    '建国门外': 'https://bj.ke.com/ershoufang/jianguomenwai/',
    '立水桥': 'https://bj.ke.com/ershoufang/lishuiqiao1/',
    '马甸': 'https://bj.ke.com/ershoufang/madian1/',
    '农展馆': 'https://bj.ke.com/ershoufang/nongzhanguan/',
    '南沙滩': 'https://bj.ke.com/ershoufang/nanshatan1/',
    '潘家园': 'https://bj.ke.com/ershoufang/panjiayuan1/',
    '三元桥': 'https://bj.ke.com/ershoufang/sanyuanqiao/',
    '芍药居': 'https://bj.ke.com/ershoufang/shaoyaoju/',
    '石佛营': 'https://bj.ke.com/ershoufang/shifoying/',
    '十里堡': 'https://bj.ke.com/ershoufang/shilibao/',
    '首都机场': 'https://bj.ke.com/ershoufang/shoudoujichang1/',
    '双井': 'https://bj.ke.com/ershoufang/shuangjing/',
    '十里河': 'https://bj.ke.com/ershoufang/shilihe/',
    '十八里店': 'https://bj.ke.com/ershoufang/shibalidian1/',
    '双桥': 'https://bj.ke.com/ershoufang/shuangqiao/',
    '三里屯': 'https://bj.ke.com/ershoufang/sanlitun/',
    '四惠': 'https://bj.ke.com/ershoufang/sihui/',
    '通州北苑': 'https://bj.ke.com/ershoufang/tongzhoubeiyuan/',
    '团结湖': 'https://bj.ke.com/ershoufang/tuanjiehu/',
    '太阳宫': 'https://bj.ke.com/ershoufang/taiyanggong/',
    '甜水园': 'https://bj.ke.com/ershoufang/tianshuiyuan/',
    '望京': 'https://bj.ke.com/ershoufang/wangjing/',
    '西坝河': 'https://bj.ke.com/ershoufang/xibahe/',
    '亚运村': 'https://bj.ke.com/ershoufang/yayuncun/',
    '亚运村小营': 'https://bj.ke.com/ershoufang/yayuncunxiaoying/',
    '燕莎': 'https://bj.ke.com/ershoufang/yansha1/',
    '朝阳其他': 'https://bj.ke.com/ershoufang/zhaoyangqita/'
}

haidian = {
    # 海淀区所有商圈页urls
    '奥林匹克公园': 'https://bj.ke.com/ershoufang/aolinpikegongyuan11/',
    '安宁庄': 'https://bj.ke.com/ershoufang/anningzhuang1/',
    '白石桥': 'https://bj.ke.com/ershoufang/baishiqiao1/',
    '北太平庄': 'https://bj.ke.com/ershoufang/beitaipingzhuang/',
    '昌平其他': 'https://bj.ke.com/ershoufang/changpingqita1/',
    '厂洼': 'https://bj.ke.com/ershoufang/changwa/',
    '定慧寺': 'https://bj.ke.com/ershoufang/dinghuisi/',
    '二里庄': 'https://bj.ke.com/ershoufang/erlizhuang/',
    '公主坟': 'https://bj.ke.com/ershoufang/gongzhufen/',
    '甘家口': 'https://bj.ke.com/ershoufang/ganjiakou/',
    '海淀其他': 'https://bj.ke.com/ershoufang/haidianqita1/',
    '海淀北部新区': 'https://bj.ke.com/ershoufang/haidianbeibuxinqu1/',
    '军博': 'https://bj.ke.com/ershoufang/junbo1/',
    '六里桥': 'https://bj.ke.com/ershoufang/liuliqiao1/',
    '牡丹园': 'https://bj.ke.com/ershoufang/mudanyuan/',
    '马甸': 'https://bj.ke.com/ershoufang/madian1/',
    '马连洼': 'https://bj.ke.com/ershoufang/malianwa/',
    '清河': 'https://bj.ke.com/ershoufang/qinghe11/',
    '苏州桥': 'https://bj.ke.com/ershoufang/suzhouqiao/',
    '上地': 'https://bj.ke.com/ershoufang/shangdi1/',
    '世纪城': 'https://bj.ke.com/ershoufang/shijicheng/',
    '四季青': 'https://bj.ke.com/ershoufang/sijiqing/',
    '双榆树': 'https://bj.ke.com/ershoufang/shuangyushu/',
    '田村': 'https://bj.ke.com/ershoufang/tiancun1/',
    '五道口': 'https://bj.ke.com/ershoufang/wudaokou/',
    '魏公村': 'https://bj.ke.com/ershoufang/weigongcun/',
    '五棵松': 'https://bj.ke.com/ershoufang/wukesong1/',
    '万柳': 'https://bj.ke.com/ershoufang/wanliu/',
    '万寿路': 'https://bj.ke.com/ershoufang/wanshoulu1/',
    '西山': 'https://bj.ke.com/ershoufang/xishan21/',
    '西三旗': 'https://bj.ke.com/ershoufang/xisanqi1/',
    '西北旺': 'https://bj.ke.com/ershoufang/xibeiwang/',
    '学院路': 'https://bj.ke.com/ershoufang/xueyuanlu1/',
    '小西天': 'https://bj.ke.com/ershoufang/xiaoxitian1/',
    '西直门': 'https://bj.ke.com/ershoufang/xizhimen1/',
    '新街口': 'https://bj.ke.com/ershoufang/xinjiekou2/',
    '西二旗': 'https://bj.ke.com/ershoufang/xierqi1/',
    '杨庄': 'https://bj.ke.com/ershoufang/yangzhuang1/',
    '玉泉路': 'https://bj.ke.com/ershoufang/yuquanlu11/',
    '圆明园': 'https://bj.ke.com/ershoufang/yuanmingyuan/',
    '颐和园': 'https://bj.ke.com/ershoufang/yiheyuan/',
    '知春路': 'https://bj.ke.com/ershoufang/zhichunlu/',
    '皂君庙': 'https://bj.ke.com/ershoufang/zaojunmiao/',
    '中关村': 'https://bj.ke.com/ershoufang/zhongguancun/',
    '紫竹桥': 'https://bj.ke.com/ershoufang/zizhuqiao/'
}

fengtai = {
    # 丰台区所有商圈页urls
    '北大地': 'https://bj.ke.com/ershoufang/beidadi/',
    '北京南站': 'https://bj.ke.com/ershoufang/beijingnanzhan1/',
    '成寿寺': 'https://bj.ke.com/ershoufang/chengshousi1/',
    '草桥': 'https://bj.ke.com/ershoufang/caoqiao/',
    '菜户营': 'https://bj.ke.com/ershoufang/caihuying/',
    '大红门': 'https://bj.ke.com/ershoufang/dahongmen/',
    '丰台其他': 'https://bj.ke.com/ershoufang/fengtaiqita1/',
    '方庄': 'https://bj.ke.com/ershoufang/fangzhuang1/',
    '广安门': 'https://bj.ke.com/ershoufang/guanganmen/',
    '和义': 'https://bj.ke.com/ershoufang/heyi/',
    '花乡': 'https://bj.ke.com/ershoufang/huaxiang/',
    '旧宫': 'https://bj.ke.com/ershoufang/jiugong1/',
    '角门': 'https://bj.ke.com/ershoufang/jiaomen/',
    '科技园区': 'https://bj.ke.com/ershoufang/kejiyuanqu/',
    '看丹桥': 'https://bj.ke.com/ershoufang/kandanqiao/',
    '丽泽': 'https://bj.ke.com/ershoufang/lize/',
    '刘家窑': 'https://bj.ke.com/ershoufang/liujiayao/',
    '卢沟桥': 'https://bj.ke.com/ershoufang/lugouqiao1/',
    '六里桥': 'https://bj.ke.com/ershoufang/liuliqiao1/',
    '木樨园': 'https://bj.ke.com/ershoufang/muxiyuan1/',
    '马家堡': 'https://bj.ke.com/ershoufang/majiabao/',
    '马连道': 'https://bj.ke.com/ershoufang/maliandao1/',
    '蒲黄榆': 'https://bj.ke.com/ershoufang/puhuangyu/',
    '青塔': 'https://bj.ke.com/ershoufang/qingta1/',
    '七里庄': 'https://bj.ke.com/ershoufang/qilizhuang/',
    '宋家庄': 'https://bj.ke.com/ershoufang/songjiazhuang/',
    '十里河': 'https://bj.ke.com/ershoufang/shilihe/',
    '太平桥': 'https://bj.ke.com/ershoufang/taipingqiao1/',
    '五里店': 'https://bj.ke.com/ershoufang/wulidian/',
    '西红门': 'https://bj.ke.com/ershoufang/xihongmen/',
    '西罗园': 'https://bj.ke.com/ershoufang/xiluoyuan/',
    '新宫': 'https://bj.ke.com/ershoufang/xingong/',
    '岳各庄': 'https://bj.ke.com/ershoufang/yuegezhuang/',
    '玉泉营': 'https://bj.ke.com/ershoufang/yuquanying/',
    '右安门外': 'https://bj.ke.com/ershoufang/youanmenwai/',
    '洋桥': 'https://bj.ke.com/ershoufang/yangqiao1/',
    '赵公口': 'https://bj.ke.com/ershoufang/zhaogongkou/'
}

shijingshan = {
    # 石景山区所有商圈页urls
    '八角': 'https://bj.ke.com/ershoufang/bajiao1/',
    '城子': 'https://bj.ke.com/ershoufang/chengzi/',
    '古城': 'https://bj.ke.com/ershoufang/gucheng/',
    '老山': 'https://bj.ke.com/ershoufang/laoshan1/',
    '鲁谷': 'https://bj.ke.com/ershoufang/lugu1/',
    '苹果园': 'https://bj.ke.com/ershoufang/pingguoyuan1/',
    '石景山其他': 'https://bj.ke.com/ershoufang/shijingshanqita1/',
    '杨庄': 'https://bj.ke.com/ershoufang/yangzhuang1/',
    '玉泉路': 'https://bj.ke.com/ershoufang/yangzhuang1/'
}

tongzhou = {
    # 通州区所有商圈页urls
    '北关': 'https://bj.ke.com/ershoufang/beiguan/',
    '大兴其他': 'https://bj.ke.com/ershoufang/daxingqita11/',
    '果园': 'https://bj.ke.com/ershoufang/guoyuan1/',
    '九棵树（家乐福）': 'https://bj.ke.com/ershoufang/jiukeshu12/',
    '潞苑': 'https://bj.ke.com/ershoufang/luyuan/',
    '梨园': 'https://bj.ke.com/ershoufang/liyuan/',
    '临河里': 'https://bj.ke.com/ershoufang/linheli/',
    '马驹桥': 'https://bj.ke.com/ershoufang/majuqiao1/',
    '乔庄': 'https://bj.ke.com/ershoufang/qiaozhuang/',
    '首都机场': 'https://bj.ke.com/ershoufang/shoudoujichang1/',
    '通州北苑': 'https://bj.ke.com/ershoufang/tongzhoubeiyuan/',
    '通州其他': 'https://bj.ke.com/ershoufang/tongzhouqita11/',
    '武夷花园': 'https://bj.ke.com/ershoufang/wuyihuayuan/',
    '新华大街': 'https://bj.ke.com/ershoufang/xinhuadajie/',
    '玉桥': 'https://bj.ke.com/ershoufang/yuqiao/'
}

changping = {
    # 昌平区所有商圈页urls
    '奥林匹克公园': 'https://bj.ke.com/ershoufang/aolinpikegongyuan11/',
    '安宁庄': 'https://bj.ke.com/ershoufang/anningzhuang1/',
    '百善镇': 'https://bj.ke.com/ershoufang/baishanzhen/',
    '北七家': 'https://bj.ke.com/ershoufang/beiqijia/',
    '昌平其他': 'https://bj.ke.com/ershoufang/changpingqita1/',
    '东关': 'https://bj.ke.com/ershoufang/dongguan/',
    '鼓楼大街': 'https://bj.ke.com/ershoufang/guloudajie/',
    '回龙观': 'https://bj.ke.com/ershoufang/huilongguan2/',
    '霍营': 'https://bj.ke.com/ershoufang/huoying/',
    '立水桥': 'https://bj.ke.com/ershoufang/lishuiqiao1/',
    '南邵': 'https://bj.ke.com/ershoufang/nanshao/',
    '南口': 'https://bj.ke.com/ershoufang/nankou/',
    '沙河': 'https://bj.ke.com/ershoufang/shahe2/',
    '天通苑': 'https://bj.ke.com/ershoufang/tiantongyuan1/',
    '西关环岛': 'https://bj.ke.com/ershoufang/xiguanhuandao/',
    '西三旗': 'https://bj.ke.com/ershoufang/xisanqi1/',
    '小汤山': 'https://bj.ke.com/ershoufang/xiaotangshan1/'
}

daxing = {
    # 大兴区所有商圈页urls
    '大兴其他': 'https://bj.ke.com/ershoufang/daxingqita11/',
    '大兴开发区': 'https://bj.ke.com/ershoufang/daxingkaifaqu/',
    '观音寺': 'https://bj.ke.com/ershoufang/guanyinsi/',
    '高米店南': 'https://bj.ke.com/ershoufang/gaomidiannan/',
    '黄村火车站': 'https://bj.ke.com/ershoufang/huangcunhuochezhan/',
    '黄村北': 'https://bj.ke.com/ershoufang/huangcunbei/',
    '黄村中': 'https://bj.ke.com/ershoufang/huangcunzhong/',
    '和义': 'https://bj.ke.com/ershoufang/heyi/',
    '旧宫': 'https://bj.ke.com/ershoufang/jiugong1/',
    '科技园区': 'https://bj.ke.com/ershoufang/kejiyuanqu/',
    '天宫院': 'https://bj.ke.com/ershoufang/tiangongyuan/',
    '西红门': 'https://bj.ke.com/ershoufang/xihongmen/',
    '瀛海': 'https://bj.ke.com/ershoufang/yinghai/',
    '郁花园': 'https://bj.ke.com/ershoufang/yuhuayuan/',
    '枣园': 'https://bj.ke.com/ershoufang/zaoyuan/'
}

yizhuang = {
    # 亦庄开发区区所有商圈页urls
    '大兴其他': 'https://bj.ke.com/ershoufang/daxingqita11/',
    '马驹桥': 'https://bj.ke.com/ershoufang/majuqiao1/',
    '亦庄': 'https://bj.ke.com/ershoufang/yizhuang1/',
    '亦庄开发区其他': 'https://bj.ke.com/ershoufang/yizhuangkaifaquqita1/'
}

shunyi = {
    # 顺义区所有商圈页urls
    '后沙峪': 'https://bj.ke.com/ershoufang/houshayu1/',
    '李桥': 'https://bj.ke.com/ershoufang/liqiao1/',
    '马坡': 'https://bj.ke.com/ershoufang/mapo/',
    '顺义城': 'https://bj.ke.com/ershoufang/shunyicheng/',
    '顺义其他': 'https://bj.ke.com/ershoufang/shunyiqita1/',
    '首都机场': 'https://bj.ke.com/ershoufang/shoudoujichang1/',
    '天竺': 'https://bj.ke.com/ershoufang/tianzhu1/',
    '中央别墅区': 'https://bj.ke.com/ershoufang/zhongyangbieshuqu1/'
}

fangshan = {
    # 房山区所有商圈页urls
    '长阳': 'https://bj.ke.com/ershoufang/changyang1/',
    '城关': 'https://bj.ke.com/ershoufang/chengguan/',
    '窦店': 'https://bj.ke.com/ershoufang/doudian/',
    '房山其他': 'https://bj.ke.com/ershoufang/fangshanqita/',
    '韩村河': 'https://bj.ke.com/ershoufang/hancunhe1/',
    '良乡': 'https://bj.ke.com/ershoufang/liangxiang/',
    '琉璃河': 'https://bj.ke.com/ershoufang/liulihe/',
    '燕山': 'https://bj.ke.com/ershoufang/yanshan/',
    '阎村': 'https://bj.ke.com/ershoufang/yancun/'
}

mentougou = {
    # 门头沟区所有商圈页urls
    '滨河西区': 'https://bj.ke.com/ershoufang/binhexiqu1/',
    '城子': 'https://bj.ke.com/ershoufang/chengzi/',
    '大峪': 'https://bj.ke.com/ershoufang/dayu/',
    '冯村': 'https://bj.ke.com/ershoufang/fengcun/',
    '门头沟其他': 'https://bj.ke.com/ershoufang/mentougouqita1/',
    '石门营': 'https://bj.ke.com/ershoufang/shimenying/',
    '石景山其他': 'https://bj.ke.com/ershoufang/shijingshanqita1/'
}

pinggu = {
    # 平谷区所有商圈页urls
    '平谷其他': 'https://bj.ke.com/ershoufang/pingguqita1/'
}

huairou = {
    # 怀柔区所有商圈页urls
    '昌平其他': 'https://bj.ke.com/ershoufang/changpingqita1/',
    '怀柔': 'https://bj.ke.com/ershoufang/huairouchengqu1/',
    '怀柔其他': 'https://bj.ke.com/ershoufang/huairouqita1/'
}

miyun = {
    # 密云区所有商圈页urls
    '密云其他': 'https://bj.ke.com/ershoufang/miyunqita11/'
}

yanqing = {
    # 延庆区所有商圈页urls
    '延庆其他': 'https://bj.ke.com/ershoufang/yanqingqita1/'
}


# 将北京市所有行政区组成字典
district_lists = {
    '东城': dongcheng,
    '西城': xicheng,
    '朝阳': chaoyang,
    '海淀': haidian,
    '丰台': fengtai,
    '石景山': shijingshan,
    '通州': tongzhou,
    '昌平': changping,
    '大兴': daxing,
    '亦庄开发区': yizhuang,
    '顺义': shunyi,
    '房山': fangshan,
    '门头沟': mentougou,
    '平谷': pinggu,
    '怀柔': huairou,
    '密云': miyun,
    '延庆': yanqing
}


# -------------------------------------自定义函数-----------------------------------------


def get_info():                                     # 从当前页面获得信息的函数
    try:
        info_title = soup1.select(
            'ul > li > div > div.title > a.CLICKDATA.maidian-detail')[j].get_text()
    except Exception:
        info_title = '未知'

    try:
        info_code_pre = soup1.select(
            'ul > li > div > div.title > a.CLICKDATA.maidian-detail')[j].get('href')
        info_code = str(re.findall(
            r'\d+', info_code_pre)[0])           # 正则取出href中的房源编号
    except Exception:
        info_code = '未知'

    info_city = city
    info_district = dis_name
    info_section = key
    try:
        info_community_pre = soup1.select(
            'ul > li > div > div > div.houseInfo > a')[j].get_text()
        info_community = info_community_pre.strip()
    except Exception:
        info_community = '未知'

    try:
        info_room_pre = soup1.select('ul > li > div > div > div.houseInfo')[
            j].get_text()
        info_room = info_room_pre.split(
            '|')[1].strip()  # 取出分割字符串，去掉头尾空格
    except Exception:
        info_room = '未知'

    try:
        info_area_pre = soup1.select('ul > li > div > div > div.houseInfo')[
            j].get_text()
        info_area_pre2 = re.findall(
            r'\d+', info_area_pre.split('|')[2].strip())  # 匹配到数字
        info_area = int(info_area_pre2[0])  # 转换为整数类型，省略小数点后数字
    except Exception:
        info_area = '未知'

    try:
        info_toward_pre = soup1.select(
            'ul > li > div > div > div.houseInfo')[j].get_text()
        info_toward = info_toward_pre.split('|')[3].strip()
    except Exception:
        info_toward = '未知'

    try:
        info_deco_pre = soup1.select('ul > li > div > div > div.houseInfo')[
            j].get_text()
        info_deco = info_deco_pre.split('|')[4].strip()
    except Exception:
        info_deco = '未知'

    try:  # 使用异常处理，因为有些信息没有录入电梯情况
        info_lift_pre = soup1.select('ul > li > div > div > div.houseInfo')[
            j].get_text()
        info_lift = info_lift_pre.split('|')[5].strip()
    except Exception:
        info_lift = '未知'

    try:  # 使用异常处理，因为有些信息没有建筑年份情况
        info_age_pre = soup1.select('ul > li > div > div > div.positionInfo')[
            j].get_text()
        info_age = int(re.findall(
            r'\d+', info_age_pre)[1])           # 正则取出房龄的数字,转成整数
    except Exception:
        info_age = '未知'

    try:
        info_price_pre = soup1.select(
            'div > div > div.totalPrice > span')[j].get_text()
        info_price = round(float(info_price_pre))  # 四舍五入，小数点后0位
    except Exception:
        info_price = '未知'

    try:
        info_unitprice_pre = soup1.select(
            'div > div.unitPrice > span')[j].get_text()
        info_unitprice = int(re.findall(
            r'\d+', info_unitprice_pre)[0])           # 正则取出单价的数字,转成整数
    except Exception:
        info_unitprice = '未知'

    try:
        info_follow_pre = soup1.select(
            'div > div.followInfo')[j].get_text()
        info_follow = int(re.findall(
            r'\d+', info_follow_pre)[0])  # 正则直接取出数字
    except Exception:
        info_follow = 0

    try:
        info_view_pre = soup1.select('div > div.followInfo')[
            j].get_text()
        info_view = int(re.findall(
            r'\d+', info_view_pre)[1])  # 正则直接取出数字
    except Exception:
        info_view = 0
    info_datetime = str(datetime.datetime.now().date())  # 信息更新时间

    print('取得房源数据>>>>>' + ' 商圈：' + info_section + ' 编号：' + info_code +
          ' 小区：' + info_community + ' 价格：' + str(info_price) + '万 ' + ' 面积：' + str(info_area) + '平米')  # 输出显示

    # 准备插入到数据库的数据

    # 待办：下一步加入判断，如果有相同数据，则提示和比较信息
    try:
        one_data = {
            '标题': info_title,
            '房源编号': info_code,
            '城市': info_city,
            '行政区': info_district,
            '商圈': info_section,
            '小区': info_community,
            '房型': info_room,
            '面积': info_area,
            '朝向': info_toward,
            '装修': info_deco,
            '电梯': info_lift,
            '房龄': info_age,
            '报价': info_price,
            '单价': info_unitprice,
            '关注人数': info_follow,
            '带看次数': info_view,
            '抓取时间': info_datetime,
        }
        # 插入一条数据数据
        db["user"].insert_one(one_data)  # 向数据表posts中插入数据
        print('-----------------   成功保存到数据库    -------------------')
    except Exception:
        print('!!!!!!!!!!!!!!!!!!  房源:' + info_community +
              '存入数据库失败！    !!!!!!!!!!!!!!!!!!!!!!!!!')
# 创建保存到数据库的函数


# -----------------------------------------流程逻辑代码-----------------------------------------------
# 遍历本市所有的行政区列表，取出字典中的key和value
for (dis_name, dis_urls) in district_lists.items():

    # 遍历每区商圈的URL
    for (key, value) in dis_urls.items():
        # 获得HTML，进行解析
        res = requests.get(value, headers=headers)  # 获得HTML
        soup = BeautifulSoup(res.content, 'lxml')  # 解析
        section_info_nums = int(soup.select('h2 > span')[
                                0].get_text())  # 找到该商圈房源信息总数量。
        max_pages = math.ceil(section_info_nums / 30)  # 最大页码数，向上取整
        lastpage_info_nums = math.ceil(
            section_info_nums % 30)  # 信息余数，作为最后一页的信息数，可能是0
        # 判断，如果信息为0，跳过此商圈。
        if section_info_nums == 0:
            print('当前商圈房源数为0，搜索下一商圈')
            continue
        else:  # 如果信息不为0
            print('当前商圈房源数为: ' + str(section_info_nums) +
                  '条，共' + str(max_pages) + '页')  # 输出

            # 总信息不为0，开始遍历本商圈每页房源
            for page in range(1, max_pages+1):
                # 判断余数是否为0
                # 如果余数为0,显示每页有30条房源信息
                if lastpage_info_nums == 0:
                    print('第' + str(page) + '页有30条房源信息')
                    # 判断最大页是否只有1页,显示和抓取30条信息数
                    if max_pages == 1:
                        print('该商圈只有一页，共30条房源信息')  # 输出
                        # 先构建1页的url
                        url = str(value) + 'pg' + str(page)
                        print('只有1页，正在分析数据：' + str(url))  # 输出
                        # 获取html，解析
                        res1 = requests.get(url, headers=headers)
                        soup1 = BeautifulSoup(res1.content, 'lxml')
                        # 遍历1页，获得该页30条数据
                        for j in range(0, 30):
                            get_info()                          # 自定义函数，取得当前页数据
                    else:  # 不止1页
                        # 先构建n页的url
                        url = str(value) + 'pg' + str(page)
                        print('正在分析数据：' + str(url))  # 输出
                        # 开始抓取n页30条
                        # 获取html，解析
                        res1 = requests.get(url, headers=headers)
                        soup1 = BeautifulSoup(res1.content, 'lxml')
                        # 遍历n页，获得每页30条数据
                        for j in range(0, 30):
                            get_info()                          # 自定义函数，取得当前页数据

                # 如果余数不为0，区分是否最后一页来显示房源信息数目
                else:
                    # 判断，最大页是否只有1页
                    if max_pages == 1:
                        # 如果最大页只有1页，显示和抓取余数信息数
                        print('该商圈只有一页，共' + str(lastpage_info_nums) + '条房源信息')  # 输出
                        # 抓取1页的余数条数据
                        # 先构建1页的url
                        url = str(value) + 'pg' + str(page)
                        print('只有1页，正在分析数据：' + str(url))  # 输出
                        # 获取html，解析
                        res1 = requests.get(url, headers=headers)
                        soup1 = BeautifulSoup(res1.content, 'lxml')
                        # 遍历1页，获得该页余数条数据
                        for j in range(0, lastpage_info_nums):
                            get_info()                          # 自定义函数，取得当前页数据
                    else:
                        # 判断，如果最大页不止1页，当前页是不是最大页
                        if page == max_pages:
                            # 如果当前页是最大页（最后一页），抓取余数条信息。
                            print('第' + str(page) + '页有' +
                                  str(lastpage_info_nums) + '条房源信息')  # 输出
                            # 先构建url
                            url = str(value) + 'pg' + str(page)
                            print('正在分析数据：' + str(url))  # 输出
                            # 获取html，解析
                            res1 = requests.get(url, headers=headers)
                            soup1 = BeautifulSoup(res1.content, 'lxml')
                            # 遍历第max页获得的该页余数条数据
                            for j in range(0, lastpage_info_nums):
                                get_info()                      # 自定义函数，取得当前页数据
                        else:
                            # 如果当前页不是最大页，抓取30条信息
                            print('第' + str(page) + '页有30条房源信息')  # 输出
                            # 先构建第n页的url
                            url = str(value) + 'pg' + str(page)
                            print('正在分析数据：' + str(url))  # 输出
                            # 获取html，解析
                            res1 = requests.get(url, headers=headers)
                            soup1 = BeautifulSoup(res1.content, 'lxml')
                            # 遍历第n页获得的该页30条数据
                            for j in range(0, 30):
                                get_info()                      # 自定义函数，取得当前页数据


print('本程序全部执行完成！共找到' + '条房源信息！')

# -------------------------------------------其他------------------------------------------

# -------------------------------------------待实现功能------------------------------------------
# 增加一个程序运行时间计时器
# 增加一个保存信息的计数器
# 保存到数据库增加一个判断，如果存在编号相同数据，则不保存
# 把扫描到的待爬网址存入数据库
# 从数据库读取出待爬网址
# 将其他城市加入其中
