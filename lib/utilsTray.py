#!/usr/bin/env python2
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import dbTrayServer
import os
import sys
import uuid
import debug
import MySQLdb
import socket






if(sys.platform.find("win") >= 0):
  try:
    username = os.environ['USERNAME']
  except:
    username = "nobody"
if(sys.platform.find("linux") >= 0):
  try:
    username = os.environ['USER']
  except:
    username = "nobody"


def getNotifications():
  dbcon = dbTrayServer.dbTray()
  try:
    rows = dbcon.execute("select * from notify where toUsers=\""+ username +"\" and afterTime<=now()",dictionary=True)
    if(rows):
      if(not isinstance(rows,int)):
        return (rows)
  except:
    debug.error(sys.exc_info())
  return (0)

def seeNotification(id):
  dbcon = dbTrayServer.dbTray()
  try:
    rows = dbcon.execute("delete from notify where id=\""+ id +"\"")
    return (1)
  except:
    debug.error(sys.exc_info())
  return (0)


def markAsChecked(id):
  dbcon = dbTrayServer.dbTray()
  try:
    rows = dbcon.execute("update notify set isChecked=1 where id=\"" + id + "\"")
    return (1)
  except:
    debug.error(sys.exc_info())
  return (0)


def updateUserData():
  dbcon = dbTrayServer.dbTray()
  hostname = socket.gethostname()
  try:
    dbcon.execute("insert into users (user,host) values (\""+ username +"\",\""+ hostname +"\") "
                  "on duplicate key update "
                  "host=\""+ hostname +"\", "
                  "lastUpdated=now()")
  except:
    debug.error(sys.exc_info())

def deleteUserData():
  dbcon = dbTrayServer.dbTray()
  try:
    dbcon.execute("delete from users where user=\""+ username +"\"")
  except:
    debug.error(sys.exc_info())


if(__name__ == "__main__"):
  debug.info(getNotifications())