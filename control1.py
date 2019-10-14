#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shutil,os

os.system('rostopic pub -1 /command std_msgs/String \"land\"')


