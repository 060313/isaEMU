# -*- coding: utf-8 -*-
"""实现框架生成器 —— 主入口。运行：python _gen/gen.py"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import data_common
import data_layers
import gen_frontend

data_common.gen_common()
data_layers.gen_all()
gen_frontend.gen_frontend()
print("生成完成：", data_common.__file__)
