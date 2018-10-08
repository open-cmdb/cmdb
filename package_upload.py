#!/usr/bin/env python
#coding: utf-8

import subprocess
import datetime


def run_cmd(cmd):
    code = subprocess.call(cmd, shell=True)
    if code > 1:
        raise Exception("'{}' 执行失败，返回code：{}".format(cmd, code))


def get_current_branch():
    p = subprocess.Popen("git branch -a", shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    out, err = p.communicate()
    rows = out.decode().split("\n")
    for row in rows:
        if row[0] == "*":
            return row.split("* ")[1]


if __name__ == '__main__':
    dt = datetime.datetime.now()
    msg = dt.strftime("%Y%m%d%H%M")
    current_branch = get_current_branch()

    run_cmd("git add *")
    run_cmd("git commit -a -m {}".format(msg))
    run_cmd("git push origin {}".format(current_branch))