from pyecharts.charts import Geo
from pyecharts import options as opts
from pyecharts.globals import GeoType
import pymysql

def task():
    city = '北京'
    g = Geo(init_opts=opts.InitOpts(width = '1600px', height='800px'))
    g.add_schema(maptype=city)

    # 数据库连接
    db = pymysql.connect(host = 'localhost', user='root', password='123456', port=3306, db = 'educationalResource_bj')
    cursor = db.cursor()
    sql = 'select * from educationalResourceMap'
    cursor.execute(sql)
    results = cursor.fetchall()
    db.close()
    #print(results[0][1])

    for result in results:
        g.add_coordinate(result[1], result[6], result[7])

    data_pair = []
    for result in results:
        judge = 0
        if result[3] == 'gbyey':
            judge = 10
        elif result[3] == 'xx':
            judge = 20
        elif result[3] == 'zx':
            judge = 30
        elif result[3] == 'zyjyxx':
            judge = 50
        elif result[3] == 'gdyx':
            judge = 80
        else :
            judge = 101
        data_pair.append((result[1], judge))

    #print(data_pair)

    # Geo 图类型，有 scatter, effectScatter, heatmap, lines 4 种，建议使用
    # from pyecharts.globals import GeoType
    # GeoType.GeoType.EFFECT_SCATTER，GeoType.HEATMAP，GeoType.LINES

    # 将数据添加到地图上
    g.add('', data_pair, type_=GeoType.EFFECT_SCATTER, symbol_size=5)
    # 设置样式
    g.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    # 自定义分段 color 可以用取色器取色
    pieces = [
        {'min': 1, 'max': 10, 'label': '幼儿园', 'color': '#3700A4'},
        {'min': 10, 'max': 20, 'label': '小学', 'color': '#81AE9F'},
        {'min': 20, 'max': 30, 'label': '中学', 'color': '#E2C568'},
        {'min': 30, 'max': 50, 'label': '职业技术学校', 'color': '#FCF84D'},
        {'min': 50, 'max': 100, 'label': '高等院校', 'color': '#DD0200'},
        {'min': 100, 'max': 200, 'label': '特殊教育学校', 'color': '#DD675E'},
    ]
    #  is_piecewise 是否自定义分段， 变为true 才能生效
    g.set_global_opts(
        visualmap_opts=opts.VisualMapOpts(is_piecewise=True, pieces=pieces),
        title_opts=opts.TitleOpts(title="{}-学校分布".format(city)),
    )
    return g



if __name__ == "__main__":
    g = task()
    # 渲染成html, 可用浏览器直接打开
    g.render('beijingDemo.html')