#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from wxpy import *
import threading
import os
import time

class wechatInfo (object):
    # 初始化微信
    def __init__ (self):
        self.bot = Bot()
        self.myself = self.bot.self
        self.friends = self.bot.friends()
        # self.tuling = Tuling(api_key='ad68c7fe6caf4d29bb78fe36cbbf1b63')

    def main (self):
        if not os.path.exists('./info/' + wechat.myself.name):
            filepath = os.getcwd()
            os.makedirs(filepath + '/info/' + wechat.myself.name + '/headImg')
            self.getFriendsList()

    # 获取微信好友列表
    def getFriendsList (self):
        for i in range(len(self.friends)):
            if i == 0:
                writeType = 'w'
            else:
                writeType = 'a'

            t = threading.Thread(target=self.writeWechatInfo, args=(self.friends[i], writeType, 'f',))
            t1 = threading.Thread(target=self.saveHeadImg, args=(self.friends[i],))
            t.start()
            t1.start()
        
        self.getGroupsList()

        print('共有好友: %s 人 \n' %(len(self.friends)))

    # 创建txt文本 写入微信好友名称
    def writeWechatInfo (self, info, writeType, fType):
        if fType == 'f':
            url = 'info/' + self.myself.name + '/好友列表.txt'
        else:
            url = 'info/' + self.myself.name + '/' + fType+ '的群友列表.txt'

        with open(url, writeType) as f:           
            print('正在写入 备注名为：%s 的信息' % (info.name))
            
            if fType == 'f':
                if writeType == 'w':
                    f.write('共有好友: %s 人' %(len(self.friends)))

                if info.raw['Sex'] == 1:
                    sex = '男'
                elif info.raw['Sex'] == 2:
                    sex = '女'
                else:
                    sex = '未知'
                address = info.raw['Province'] + ' ' + info.raw['City']
                f.write('微信备注名：%s 昵称：%s 性别：%s 位置：%s \n' % (info.name, info.nick_name, sex, address))
            else:
                f.write('微信昵称：%s \n' % (info.name))

    # 保存好友头像
    def saveHeadImg (self, friend):
        print('正在保存 %s 的头像...' % friend.name)
        friend.get_avatar('info/%s/headImg/%s_%s.jpg' % (self.myself.name, friend.name[:20], time.time()))

    # 获取群列表
    def getGroupsList (self):
        groups = self.bot.groups()
        
        for i in range(len(groups)):
            group = groups[i]
            for f in range(len(group.members)):
                if f == 0:
                    writeType = 'w'
                else:
                    writeType = 'a'
                    
                t = threading.Thread(target=self.writeWechatInfo, args=(group.members[f], writeType, group.name,))
                t.start()
        
        self.bot.logout()

    # def reply_msg(self, msg):
    #     self.tuling(msg)

if __name__ == "__main__":
    wechat = wechatInfo()
    wechat.main()