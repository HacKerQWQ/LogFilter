# -*- coding: utf-8 -*-
# Author: HackerQWQ
# Created Time: 23:19
import argparse
import urllib.parse
import re
import database

def generate_logs(db,logfile):
    with open(logfile, "r", encoding="utf-8") as log:
        lines = log.readlines()
        # 索引值
        count = 1
        records = []
        for line in lines:
            m = re.match(
                r"(?P<ip>.*) (?P<remote_log_name>.*) (?P<userid>.*) \[(?P<date>.*)(?= ) (?P<timezone>.*?)\] \"(?P<request_method>.*) (?P<path>.*)(?P<request_version> HTTP/.*)\" (?P<status>.*) (?P<length>.*) \"(?P<referrer>.*)\" \"(?P<user_agent>.*)\"",
                line)
            # 添加id
            record = tuple([str(count)]) + m.groups()
            # url解码字段
            record = tuple([urllib.parse.unquote(item) for item in list(record)])
            # 添加到总records中
            records.append(record)
            count += 1
        # 导入所有记录到sqlite
        db.insert_dataset(records)

def logic_boundary(rule):
    logic = re.compile("(\B\|\|)|(\|\|\B)|(\B\&\&)|(\&\&\B)")
    if logic.search(rule)!=None:
        return True
    else:
        return False
    
def logic_split(rule):
    sentence = re.split("\&\&|\|\|",rule)
    return sentence

def parse_rules(rules):
    condition = ""
    for rule in rules:
        condition = execute_exp(condition,rule)
    db.filter_data(condition)

def execute_exp(condition,rule):
    # print(rule)
    if "==" in rule:
        condition_name = rule[:(rule.index("=="))].upper()
        value = rule[(rule.index("==")) + 2:]
        condition+= f" AND {condition_name}=\"{value}\""
    elif "!=" in rule:
        condition_name = rule[:(rule.index("!="))].upper()
        value = rule[(rule.index("!=")) + 2:]
        condition += f" AND {condition_name} NOT LIKE \"%{value}%\""
    else:
        condition_name = rule[:(rule.index("="))].upper()
        value = rule[(rule.index("=")) + 1:]
        condition += f" AND {condition_name} LIKE \"%{value}%\""
    return condition

def output_result(data, filename):
    with open(filename, "w+",encoding="utf-8") as o:
        for line in data:
            o.write(line+"\n")
        for line in data:
            print(line)

if __name__=="__main__":
    banner='''
    
  _                _____ _ _ _            
 | |    ___   __ _|  ___(_) | |_ ___ _ __ 
 | |   / _ \ / _` | |_  | | | __/ _ \ '__|
 | |__| (_) | (_| |  _| | | | ||  __/ |   
 |_____\___/ \__, |_|   |_|_|\__\___|_|   
             |___/                        
                                                        介绍:一款Apache Log过滤工具
                                                        开发者:HackerQWQ
                                                        用法: analyzer.py -r [语法] access.log                                                   
    '''
    print(banner)
    # 读取变量
    parser = argparse.ArgumentParser()
    # group = parser.add_mutually_exclusive_group()
    parser.add_argument("-r","--rules", type=str,
                        help="input rule to filter")
    parser.add_argument("logfile", type=str,
                        help="input a access logfile to handle")
    args = parser.parse_args()
    logfile = args.logfile
    print("过滤规则为: "+args.rules)
    # 声明数据库连接
    db = database.db()
    # 生成日志数据库
    generate_logs(db,logfile)

    # 解析用户输入语法，进行查询
    raw_rule = args.rules
    raw_rules = logic_split(raw_rule)
    # print(raw_rules)
    parse_rules(raw_rules)

    # 获取过滤后的数据
    result = db.get_filter()
    filter_data = []
    for item in result:
        item = list(item)
        lists = []
        for column in item:
            column = str(column)
            lists.append(column)
        filter_data.append(" ".join(lists))
    output_result(filter_data,"./output/result.log")
