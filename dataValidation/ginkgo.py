# -*- coding: UTF-8 -*-
"""
@author:rebootcat
@file:ginkgo.py
@time:2022/06/30
@target: 
"""
from config import ginkgo, ginkgoVariable
from collections import OrderedDict
import scipy.stats as stats
import pandas as pd
import calendar
import datetime
import pickle


class Ginkgo:
    def __init__(self):
        self.dayOfYear = self.day_of_year_ginkgo()
        self.tem_data = None

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

    def calc_variable(self):
        ginkgoVariable.drop()
        tem_file_path = "weather/TEM_0901_1911.pkl"
        with open(tem_file_path, 'rb') as file:
            self.tem_data = pickle.load(file)

        result = ginkgo.aggregate([
            {
                '$match': {
                    'yd2009': {
                        '$ne': None
                    }
                }
            },
            {
                '$lookup': {
                    'from': 'cityInfo',
                    'localField': '_id',
                    'foreignField': '_id',
                    'as': 'result'
                }
            },
            {
                '$project': {
                    'station': {
                        '$arrayElemAt': [
                            '$result.station', 0
                        ]
                    },
                    'yd2009': 1,
                    'yd2010': 1,
                    'yd2011': 1,
                    'yd2012': 1,
                    'yd2013': 1,
                    'yd2014': 1,
                    'yd2015': 1,
                    'yd2016': 1,
                    'yd2017': 1,
                    'yd2018': 1,
                }
            }
        ])

        for record in result:
            station_list = record["station"]
            del record["station"]

            record["florescence"] = []
            record["v_ave_tem_m8"] = []
            record["v_ave_tem_m9"] = []
            record["v_ave_tem_m10"] = []

            for year in range(2009, 2019):
                nameDOY = "yd%s" % year
                record["florescence"].append(record[nameDOY])

                v_ave_tem_m8 = self.calc_tem_var(year=year, start_day=243,
                                                 station_list=station_list, back_days=31, method='ave')
                record["v_ave_tem_m8"].append(v_ave_tem_m8)

                v_ave_tem_m9 = self.calc_tem_var(year=year, start_day=273,
                                                 station_list=station_list, back_days=30, method='ave')
                record["v_ave_tem_m9"].append(v_ave_tem_m9)

                v_ave_tem_m10 = self.calc_tem_var(year=year, start_day=304,
                                                  station_list=station_list, back_days=31, method='ave')
                record["v_ave_tem_m10"].append(v_ave_tem_m10)

            ginkgoVariable.insert_one(record)
            print("%s ok" % record["_id"])

    def calc_tem_var(self, year, start_day, back_days, station_list, method):
        station_tem_list = {}
        start_date = list(self.dayOfYear[str(year)].keys())[
            list(self.dayOfYear[str(year)].values()).index(start_day)]

        start_date_format = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        back_date_format = start_date_format - datetime.timedelta(days=back_days - 1)
        back_date = str(back_date_format)[:10]

        date_list = pd.date_range(start=back_date, end=start_date, normalize=True)

        for station in station_list:
            tem_list = []
            for date in date_list:
                query_date = str(date)[:10]
                try:
                    tem = int(self.tem_data[query_date][station]['TEM'][0])
                    if tem == 32766:
                        print("station:{} data:{} no data".format(station, query_date))
                    else:
                        tem_list.append(tem)

                except:
                    tem_list = []
                    break

            if len(tem_list) == 0:
                continue
            else:
                station_tem_list[station] = tem_list

        result = 0
        if len(station_tem_list) == 0:
            result = 0
        else:
            if method == 'acc':
                sum_list = []
                for station, tem in station_tem_list.items():
                    tem_sum = sum(tem)
                    sum_list.append(tem_sum)
                result = round(sum(sum_list) / len(sum_list))

            if method == 'ave':
                ave_list = []
                for station, tem in station_tem_list.items():
                    tem_sum = sum(tem) / len(tem)
                    ave_list.append(tem_sum)
                result = round(sum(ave_list) / len(ave_list))

        return result

    def temperature_validation(self):
        x_value_dic = OrderedDict()
        x_value_dic["flo_start"] = []
        x_value_dic["flo_end"] = []

        y_value_dic = OrderedDict()
        y_value_dic["v_ave_tem_m8"] = []
        y_value_dic["v_ave_tem_m9"] = []
        y_value_dic["v_ave_tem_m10"] = []
        result_dic = OrderedDict()

        result = ginkgoVariable.find()
        missingMeteorologyCount = 0
        for record in result:
            missing_tem = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0],
                           [0, 0], [0, 0], [0, 0]]
            if record["v_ave_tem_m8"] == missing_tem or record["v_ave_tem_m8"] is None:
                missingMeteorologyCount += 1
                continue
            for year in record["florescence"]:
                start = year[0]
                end = year[1]
                x_value_dic["flo_start"].append(start)
                x_value_dic["flo_end"].append(end)
            for year in record["v_ave_tem_m8"]:
                value = int(year)
                y_value_dic["v_ave_tem_m8"].append(value)
            for year in record["v_ave_tem_m9"]:
                value = int(year)
                y_value_dic["v_ave_tem_m9"].append(value)
            for year in record["v_ave_tem_m10"]:
                value = int(year)
                y_value_dic["v_ave_tem_m10"].append(value)

        for x_var, x_value in x_value_dic.items():
            for y_var, y_value in y_value_dic.items():
                result_list = []
                result_tuple = stats.pearsonr(x=x_value, y=y_value)
                for result in result_tuple:
                    result_list.append('{:.3f}'.format(result))
                result_dic_key = x_var + ' -- ' + y_var
                result_dic[result_dic_key] = result_list
        for x in ["flo_start", "flo_end"]:
            for y in ["v_ave_tem_m8", "v_ave_tem_m9", "v_ave_tem_m10"]:
                key = "%s -- %s_%s" % (x, y, x.split("_")[1]) if y.find("tem_m") == -1 else "%s -- %s" % (x, y)
                value = str(result_dic[key])
                print("%s: %s" % (key, value))
            print("-" * 20)
        print("missing meteorology data count: %s" % missingMeteorologyCount)
        print("temperature validation ok")


if __name__ == '__main__':
    obj = Ginkgo()
    obj.calc_variable()
    obj.temperature_validation()
