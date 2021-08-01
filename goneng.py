# 功能
import numpy
from PIL import Image
from setting import *


def chessName_get_data(chess, hero_name):
    '''
    根据棋子的name返回棋子数据
    :param chess:
    :param hero_name:
    :return:
    '''
    for item in chess:
        if hero_name == item['displayName']:
            return item


def chessId_get_data(chess, hero_id):
    '''
    根据棋子的id返回棋子数据
    :param chess:
    :param hero_id:
    :return:
    '''
    for item in chess:
        if hero_id == item['chessId']:
            return item


def equipId_get_data(equip, equip_id):
    '''
    根据装备的id返回装备数据
    :param equip:
    :param equip_id:
    :return:
    '''

    for item in equip:
        if equip_id == item['equipId']:
            return item


def equip_get_dj_Data(equip, xj1, xj2):
    '''
    找到符合合成路线的装备
    :param equip: 装备数据
    :param xj1: 小件1
    :param xj2: 小件2
    :return: 返回找到装备数据
    '''

    for item in equip:
        # 找到合成符合的大件装备
        if item['type'] == '2':
            formula = item['formula'].split(',')

            if xj1 == xj2:
                if xj1 == formula[0] and xj2 == formula[1]:
                    return item
            else:
                if xj1 in formula and xj2 in formula:
                    return item


def jobId_get_data(job, job_id):
    '''
    根据职业的id返回职业数据
    :param job:
    :param job_id:
    :return:
    '''
    for item in job:
        if job_id == item['jobId']:
            return item


def raceId_get_data(race, race_id):
    '''
    根据羁绊的id返回羁绊数据
    :param race:
    :param race_id:
    :return:
    '''
    for item in race:
        if race_id == item['raceId']:
            return item


def jobName_get_data(job, job_name):
    '''
    根据职业的name返回职业数据
    :param job:
    :param job_name:
    :return:
    '''
    for item in job:
        if job_name == item['name']:
            return item


def raceName_get_data(race, race_name):
    '''
    根据羁绊的name返回羁绊数据
    :param race:
    :param race_name:
    :return:
    '''
    for item in race:
        if race_name == item['name']:
            return item


def CreateNewImage(current_filename, new_filename, new_color):
    '''
    将指定图片转换颜色
    :param current_filename: 图片路径
    :param new_filename: 保存路径
    :param new_color: 转换颜色 []
    :return:
    '''
    image = Image.open(current_filename)

    image_values = numpy.array(image)

    new_image_values = NewSolidImage(image_values, new_color)
    new_image = Image.fromarray(new_image_values)

    new_image.save(new_filename)


def NewSolidImage(rgba_array, new_color):
    '''
    将图片转换成特定颜色,透明除外!
    :param rgba_array: 图片矩阵 numpy.array(image)获取
    :param new_color: 颜色值 例如:[255,255,255]
    :return: 返回新image
    '''
    new_r, new_g, new_b = new_color
    rows, cols, rgba_size = rgba_array.shape
    if rgba_size != 4:
        raise ValueError('Bad size')

    for row in range(rows):
        for col in range(cols):
            pixel = rgba_array[row][col]
            transparency = pixel[3]
            if transparency != 0:
                new_pixel = pixel.copy()
                new_pixel[0] = new_r
                new_pixel[1] = new_g
                new_pixel[2] = new_b

                rgba_array[row][col] = new_pixel

    return rgba_array


def tanChudataForm(chessData, job, race):
    '''
    返回英雄详细资料的text
    :param chessData:
    :param job:
    :param race:
    :return:
    '''
    # ----------------------
    jobtxt = ''
    racetxt = ''
    try:
        for item in chessData['jobIds'].split(','):
            try:
                jobtxt = jobtxt + jobId_get_data(job, item)['name'] + '&nbsp;'
            except:
                pass
    except:
        pass
    try:
        for item in chessData['raceIds'].split(','):
            try:
                racetxt = racetxt + raceId_get_data(race, item)['name'] + '&nbsp;'
            except:
                pass
    except:
        pass
    return f'''
                        <h2 style="color:#FFFFFF;text-align:center;">{chessData['title']}  {chessData['displayName']}</h2>
                        <span style="color:#E7E7E9;">
                        <p><b>职业:{jobtxt}</b></p>
                        <p><b>羁绊:{racetxt}</b></p>
                        <p><b>费用:{chessData['price']}</b></p>
                        <p><b>技能:{chessData['skillName']}</b></p>
                        <p><b>{chessData['skillIntroduce']}</b></p>
                        </span>
                        '''


def tanChu_EquipData(equip, quipData):
    '''
    返回装备详细资料的text
    :param quipData:
    :return:
    '''
    # ----------------------
    zb_xj = []
    try:
        for item in quipData['formula'].split(','):
            img = Path_equip + equipId_get_data(equip, item)['imagePath'].split('/')[-1]
            zb_xj.append(img)

        return f'''
                            <h2 style="color:#FFFFFF;text-align:center;">{quipData['name']}</h2><br>
                            <img src='{zb_xj[0]}' > 
                            <img src='{zb_xj[1]}' ><b>{quipData['effect']}</b>
                            '''
    except:
        return f'''
                            <h2 style="color:#FFFFFF;text-align:center;">{quipData['name']}</h2><br>
                            <b>{quipData['effect']}</b>
                            '''


def Hero_filter(chess, price='0', jobId='0', raceId='0', keyword=''):
    '''
    根据条件筛选数据 分析chess数据然后绘制列表,注意所有的参数必须为str字符串 '0'表示不考虑这个条件
    :param chess: 字典数据
    :param price: 费用条件
    :param jobId:职业id
    :param raceId:羁绊id
    :param keyword:关键字 搜索
    :return:
    '''
    try:
        tj_list = []  # 条件列表
        # 先判断是否有这个 有的话就加入条件列表
        if price != '0':
            tj_list.append('''x['price'] == price''')
        if jobId != '0':
            tj_list.append('''jobId in x['jobIds'].split(',') ''')
        if raceId != '0':
            tj_list.append('''raceId in x['raceIds'].split(',') ''')
        if keyword != '':
            tj_list.append('''keyword in x['displayName'] or keyword in x['title'] ''')
        length = len(tj_list)
        if length == 0:
            return chess
        tj = ''
        # 将需要用到的条件都拼接起来,骚操作
        for i, item in enumerate(tj_list):
            if i == length - 1:  # 最后一个就不加and了
                tj = tj + item
            else:
                tj = tj + item + ' and '

        # 用最强大的方式检索返回符合条件的棋子列表,后面的字典就是给eval中的字符串代码传输变量(非常方便,可以用各种骚操作)
        ls_chess = eval(f'''list(filter(lambda x: {tj}, chess))''',
                        {'chess': chess, 'raceId': raceId, 'jobId': jobId, 'price': price, 'keyword': keyword})

        return ls_chess
    except:

        return chess


def job_get_background_sf(job, job_id, s, sftx=False):
    '''
    返回职业背景图片地址,以及羁绊图标'
    :param job: job数据
    :param job_id: 需要查询的id
    :param s: 羁绊数量
    :param sftx: 是否天选
    :return:返回3个数据 背景图,图标,job数据  返回None表示没达成
    '''
    try:
        itemJob = jobId_get_data(job, job_id)
        level = len(itemJob['level'])
        # 如果有天选
        if sftx == True:
            # 直接返回最华丽的背景图
            return Path_img + 'bg4.png', Path_job2 + itemJob['alias'], itemJob
        else:
            # 将key取出来
            sss = []
            for item in itemJob['level'].keys():
                sss.append(item)
            if level == 1:  # 只分1个等级时
                return Path_img + 'bg3.png', Path_job + itemJob['alias'], itemJob
            elif level == 2:  # 分2个阶段时
                if s >= int(sss[0]) and s < int(sss[1]):
                    return Path_img + 'bg2.png', Path_job + itemJob['alias'], itemJob
                elif s >= int(sss[1]):
                    return Path_img + 'bg4.png', Path_job2 + itemJob['alias'], itemJob
                else:
                    return None
            elif level == 3:  # 分3个阶段时
                if s >= int(sss[0]) and s < int(sss[1]):
                    return Path_img + 'bg2.png', Path_job + itemJob['alias'], itemJob
                elif s >= int(sss[1]) and s < int(sss[2]):
                    return Path_img + 'bg3.png', Path_job + itemJob['alias'], itemJob
                elif s >= int(sss[2]):
                    return Path_img + 'bg4.png', Path_job2 + itemJob['alias'], itemJob
                else:
                    return None

            elif level == 4:  # 分4个阶段时
                if s >= int(sss[0]) and s < int(sss[1]):
                    return Path_img + 'bg2.png', Path_job + itemJob['alias'], itemJob
                elif s >= int(sss[1]) and s < int(sss[2]):
                    return Path_img + 'bg1.png', Path_job + itemJob['alias'], itemJob
                elif s >= int(sss[2]) and s < int(sss[3]):
                    return Path_img + 'bg3.png', Path_job + itemJob['alias'], itemJob
                elif s >= int(sss[3]):
                    return Path_img + 'bg4.png', Path_job2 + itemJob['alias'], itemJob
                else:
                    return None
    except:
        return None


def race_get_background_sf(race, race_id, s, sftx=False):
    '''
    返回羁绊背景图片地址,以及羁绊图标'
    :param race: race数据
    :param race_id: 需要查询的id
    :param s: 羁绊数量
    :param sftx: 是否天选
    :return:返回3个数据 背景图,图标,race数据  返回None表示没达成
    '''
    try:
        itemRace = raceId_get_data(race, race_id)
        level = len(itemRace['level'])
        # 如果有天选
        # 将key取出来
        sss = []
        for item in itemRace['level'].keys():
            sss.append(item)
        if sftx == True:
            # 直接返回最华丽的背景图
            if s >= int(sss[0]):
                return Path_img + 'bg4.png', Path_race2 + itemRace['alias'], itemRace
        else:
            if level == 1:  # 只分1个等级时
                if s >= int(sss[0]):
                    return Path_img + 'bg3.png', Path_race + itemRace['alias'], itemRace
            elif level == 2:  # 分2个阶段时
                if s >= int(sss[0]) and s < int(sss[1]):
                    return Path_img + 'bg2.png', Path_race + itemRace['alias'], itemRace
                elif s >= int(sss[1]):
                    return Path_img + 'bg3.png', Path_race + itemRace['alias'], itemRace
                else:
                    return None
            elif level == 3:  # 分3个阶段时
                if s >= int(sss[0]) and s < int(sss[1]):
                    return Path_img + 'bg2.png', Path_race + itemRace['alias'], itemRace
                elif s >= int(sss[1]) and s < int(sss[2]):
                    return Path_img + 'bg3.png', Path_race + itemRace['alias'], itemRace
                elif s >= int(sss[2]):
                    return Path_img + 'bg4.png', Path_race2 + itemRace['alias'], itemRace
                else:
                    return None

            elif level == 4:  # 分4个阶段时
                if s >= int(sss[0]) and s < int(sss[1]):
                    return Path_img + 'bg2.png', Path_race + itemRace['alias'], itemRace
                elif s >= int(sss[1]) and s < int(sss[2]):
                    return Path_img + 'bg1.png', Path_race + itemRace['alias'], itemRace
                elif s >= int(sss[2]) and s < int(sss[3]):
                    return Path_img + 'bg3.png', Path_race + itemRace['alias'], itemRace
                elif s >= int(sss[3]):
                    return Path_img + 'bg4.png', Path_race2 + itemRace['alias'], itemRace
                else:
                    return None
    except:
        return None


if __name__ == '__main__':
    current_filename = r'C:\Users\Administrator\Desktop\4012.png'
    new_filename = r'C:\Users\Administrator\Desktop\4012.png'
    CreateNewImage(current_filename, new_filename, [255, 255, 255])
