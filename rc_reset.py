#!/usr/bin/python

import sys, string, os
import commands
import re
import argparse

DEFAULT_NUM_RC_FILE_1 = "./Num.rc"
DEFAULT_NUM_RC_FILE_2 = "./Num_2.rc"
DEFAULT_FONT_RC_FILE = "./Font.rc"
DEFAULT_TARGET_FILE = "./FactoryModeFrame.cpp"
DEFAULT_NUM_RC_SPLIT_FLAG = ";,"

class NumRcManager:

    def InitNumDictionary(self, file_name):
        with open(file_name) as rc_file:
            for line in rc_file:
                line = line.strip('\n')
                result = line.split(DEFAULT_NUM_RC_SPLIT_FLAG)
                key = result[0];
                value = result[1].strip('"')
                if value:
                    self.num_dictionary_[result[0]] = int(result[1].strip('"'))

    def ReplaceRcEngin(self, source_file_name, target_file_name):
        file_rc_dic = {}
        with open(source_file_name) as source_file:
            for line in source_file:
                findIteObj = re.finditer('GetRcEngine::RcGetNum\((.*?)\)', line)
                for findObj in findIteObj: 
                    file_rc_dic[findObj.group(1)] = findObj.group()
            
        #replace 
        with open(target_file_name, 'r+') as target_file:
            file_content=target_file.read() 
            for key in file_rc_dic:
                print(str(key)+"="+str(self.num_dictionary_[key]))
                file_content=file_content.replace(str(file_rc_dic[key]), str(self.num_dictionary_[key]))
            target_file.seek(0)
            target_file.truncate()
            target_file.write(file_content)

    num_dictionary_ = {}
    target_file_name = DEFAULT_TARGET_FILE
    source_file_name = DEFAULT_TARGET_FILE

class StrRcManager:
    def InitStrDictionary(self, file_name):
        with open(file_name) as rc_file:
            for line in rc_file:
                line = line.strip('\n')
                result = line.split(DEFAULT_NUM_RC_SPLIT_FLAG)
                key = result[0]
                value = result[1]
                if value:
                    self.str_dictionary_[key] = str(value)

    def DefineStr(self, source_file_name, declare_target_file_name, define_target_file_name):
        file_rc_dic = {}
        with open(source_file_name) as source_file:
            for line in source_file:
                findIteObj = re.finditer('ID_STR_([^\)\;\,\}\ \:]*)', line)
                for findObj in findIteObj: 
                    print(findObj.group())
                    file_rc_dic[findObj.group(1)] = findObj.group()
            
        #write 
        with open(declare_target_file_name, 'w+r') as declare_file:
            with open(define_target_file_name, 'w+r') as define_file:
                for key in file_rc_dic:
                    if file_rc_dic.get(key):
                        str_name = file_rc_dic[key]
                        if self.str_dictionary_.get(str_name):
                            declare_str = "string %s;\n" % (str(str_name))
                            define_str = "%s = %s;\n" % (str(str_name), str(self.str_dictionary_[str_name]))
                            declare_file.write(declare_str)
                            define_file.write(define_str)
                            print(define_str)

    def ReplaceRcEngin(self, source_file_name, target_file_name):
        file_rc_dic = {}
        with open(source_file_name) as source_file:
            for line in source_file:
                findIteObj = re.finditer('GetRcEngine::RcGetString\((.*?)\)', line)
                for findObj in findIteObj: 
                    file_rc_dic[findObj.group(1)] = findObj.group()
        #sort, make sure the long string ahead of the short string to be replaced.
        file_rc_dic_list = sorted(file_rc_dic.items(), key=lambda item:item[1], reverse=True)

        #replace 
        with open(target_file_name, 'r+') as target_file:
            file_content=target_file.read() 
            for item in file_rc_dic_list:
                print(str(item[0])+"="+str(self.str_dictionary_[item[0]]))
                file_content=file_content.replace(str(item[1]), str(self.str_dictionary_[item[0]]))
            target_file.seek(0)
            target_file.truncate()
            target_file.write(file_content)

        file_rc_dic = {}
        with open(source_file_name) as source_file:
            for line in source_file:
                findIteObj = re.finditer('ID_STR_([^\)\;\,\}\ \:]*)', line)
                for findObj in findIteObj: 
                    file_rc_dic[findObj.group(1)] = findObj.group()
        #sort, make sure the long string ahead of the short string to be replaced.
        file_rc_dic_list = sorted(file_rc_dic.items(), key=lambda item:item[1], reverse=True)
        #replace 
        with open(target_file_name, 'r+') as target_file:
            file_content=target_file.read() 
            for item in file_rc_dic_list:
                str_name = item[1]
                print(str(str_name)+"="+str(self.str_dictionary_[str_name]))
                file_content=file_content.replace(str(str_name), str(self.str_dictionary_[str_name]))
            target_file.seek(0)
            target_file.truncate()
            target_file.write(file_content)
        
    str_dictionary_ = {}


def main(parser):
    argv = parser.parse_args()
    if argv.rtype == "num":
        num_rc_manager = NumRcManager()
        rc_files = argv.rc.split(',')
        for rc_file in rc_files:
            num_rc_manager.InitNumDictionary(rc_file)

        num_rc_manager.ReplaceRcEngin(argv.source, argv.target)
    elif argv.rtype == "str":
        str_rc_manager = StrRcManager()
        rc_files = argv.rc.split(',')
        for rc_file in rc_files:
            str_rc_manager.InitStrDictionary(rc_file)

        str_rc_manager.ReplaceRcEngin(argv.source, argv.target)

if __name__ == "__main__":
    parse = argparse.ArgumentParser(description='manual to this script')
    parse.add_argument('--rtype', type=str, default=None)
    parse.add_argument('--rc', type=str, default=None)
    parse.add_argument('--target', type=str, default=None)
    parse.add_argument('--source', type=str, default=None)
    main(parse)
