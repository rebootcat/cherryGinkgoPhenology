# -*- coding: UTF-8 -*-
"""
@author:rebootcat
@file:logisticGinkgo.py
@time:2022/07/01
@target: 
"""
from config import connect, cursor
import datetime
from config import lenovo_redis as r
import json
import calendar
import numpy as np
from logisticRegression.utils.timing import calc_timing


class Logistic:
    def __init__(self):
        self.key_words = "ginkgo"

        self.connect = connect
        self.cursor = cursor

        self.city_dic = self.form_city_dic()
        self.day_of_year = self.day_of_year_ginkgo()

        self.fail_record = []
        self.doubt_record = []
        self.count = 0

        file_name = 'filter/' + self.key_words + '.json'
        file = open(file_name, 'r', encoding='utf-8')
        self.select = json.load(file)

    def form_city_dic(self):
        city_dic = {}
        sql = "select id, province, city from analyse.cherry where id>0;"
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            code = str(row[1]) + '-' + str(row[2])
            city_dic[code] = []
        print('form city dict complete')
        return city_dic

    def day_of_year_ginkgo(self):
        day_of_year = {}
        for year in range(2009, 2019):
            dic = {}

            day = datetime.date(year=year, month=4, day=1)  # day = 2009/8/1
            count = day - datetime.date(year=year - 1, month=12, day=31)  # count = 2009/8/1 - 2008/12/31
            value = count.days

            for month in range(4, 13):
                cal = calendar.monthcalendar(year, month)
                for line in cal:
                    for day in line:
                        if day == 0:
                            continue
                        else:
                            date = str(year) + '-' + str(month).zfill(2) + '-' + str(day).zfill(2)
                            dic[date] = value
                            value += 1

            for month in range(1, 3):
                cal = calendar.monthcalendar(year + 1, month)
                for line in cal:
                    for day in line:
                        if day == 0:
                            continue
                        else:
                            date = str(year + 1) + '-' + str(month).zfill(2) + '-' + str(day).zfill(2)
                            dic[date] = value
                            value += 1

            day_of_year[str(year)] = dic
        return day_of_year

    def save_to_redis(self):

        year_range = range(2009, 2019)
        for year in year_range:
            redis_key = "%s_%s" % (self.key_words, year)
            start = str(year) + '-08-01'
            end = str(year + 1) + '-02-01'
            print('query: {}-{}'.format(start, end))
            sql = "select * from {}.weibo_data where create_time between '{}' and '{}' " \
                  "order by id;".format(
                self.key_words, start, end)

            cursor.execute(sql)
            results = cursor.fetchall()
            if len(results) == 0:
                print('no record matched\n')
                continue
            else:
                print('records: {}'.format(str(len(results))))
                for result in results:
                    data = json.dumps({
                        'create_time': result[2],
                        'provice': result[4],
                        'city': result[5],
                        'content': result[7],
                    })
                    r.hset(redis_key, result[0], data)
                print('data stored: {}\n'.format(str(r.hlen(redis_key))))

    def split_city(self, year):
        redis_key = "%s_%s" % (self.key_words, year)
        result = r.hgetall(redis_key)
        try:
            for k, v in result.items():
                result[k] = json.loads(v, encoding='utf-8')
        except BaseException as e:
            print(e)
            result = {}

        for key, value in result.items():
            code = str(value['provice']) + '-1000'
            self.city_dic[code].append(value)
        print('split city code complete')

    def white_list(self, content):
        white_list = self.select[0]['white_words']
        for word in white_list:
            if content.find(word) == -1:
                continue
            else:
                return 1
        return 0

    def black_list(self, content):
        black_list = self.select[0]['black_words']
        for word in black_list:
            if content.find(word) == -1:
                continue
            else:
                return 1
        return 0

    def logistic_regression(self, x_list, y_list):
        global b, c, d
        x_max = max(x_list)
        x_min = min(x_list)
        y_max = np.max(y_list)

        b_index = np.where(y_list == y_max)[0].tolist()
        bx = []
        for index in b_index:
            bx.append(x_list[index])
        b = -1 * (round(sum(bx) / len(bx)))
        c = max(y_list)
        d = min(y_list)
        print("b:{} c:{} d:{} x_max:{}".format(b, c, d, x_max))
        tl, tr = calc_timing(x_list=x_list, y_list=y_list)
        return tl, tr

    def compute(self):
        for year in range(2009, 2019):
            self.split_city(year=year)

            for code, city in self.city_dic.items():
                day_blog_num = {}
                ave_list = []
                std_record = []
                pro = code[:(code.find('-'))]
                cit = code[(code.find('-') + 1):]

                for record in city:
                    white = self.white_list(record['content'])
                    if white == 1:
                        black = self.black_list(record['content'])
                        if black == 0:
                            global trust
                            trust += 1
                            try:
                                day_of_year = self.day_of_year[str(year)][
                                    record['create_time'][:10]]
                            except:
                                continue
                            if day_of_year in day_blog_num.keys():
                                day_blog_num[day_of_year] += 1
                            else:
                                day_blog_num[day_of_year] = 1
                            ave_list.append(day_of_year)
                            std_record.append(record)
                        else:
                            continue
                    else:
                        continue

                if len(day_blog_num) < 20:
                    pass
                else:
                    x, y = [], []
                    for key in sorted(day_blog_num):
                        x.append(int(key))
                        y.append(int(day_blog_num[key]))

                    tl, tr = self.logistic_regression(x_list=x, y_list=y)
                    ave = sum(ave_list) / len(ave_list)
                    std = np.std(ave_list, ddof=1)
                    for day in ave_list:
                        if (day >= ave - 2 * std) and (day <= ave + 2 * std):
                            continue
                        else:
                            ave_list.remove(day)

                    up = round(tl)
                    low = round(tr)

                    try:
                        up_date = list(self.day_of_year[str(year)].keys())[
                            list(self.day_of_year[str(year)].values()).index(up)]
                    except:
                        print('no date matched')
                        up_date = ''
                    try:
                        low_date = list(self.day_of_year[str(year)].keys())[
                            list(self.day_of_year[str(year)].values()).index(low)]
                    except:
                        print('no date matched')
                        low_date = ''

                    mysql_date = str(up_date) + ',' + str(low_date)
                    if mysql_date == ',':
                        mysql_date = ''
                    print('status: analysed')

                    mysql_year = 'y' + str(year)
                    mysql_num = 'num' + str(year)

                    try:
                        sql = "update analyse.{} set {}='{}',{}='{}',{}=\"{}\" where province={} and city={}".format(
                            self.key_words, mysql_year, mysql_date, mysql_num, len(ave_list), pro, cit)
                        self.cursor.execute(sql)
                        self.connect.commit()
                        self.count += 1
                    except Exception as e:
                        self.fail_record.append(e)
                        print(e)
                        print(
                            'write failed===============\n')
                        continue
                    print('data:\n\trecords: {}\n\tdate: {}\n'.format(str(len(ave_list)), mysql_date))

                for key, value in self.city_dic.items():
                    self.city_dic[key] = []


if __name__ == '__main__':
    obj = Logistic()
    obj.save_to_redis()
    obj.compute()
