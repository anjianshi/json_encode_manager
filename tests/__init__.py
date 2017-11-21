# -*- coding: utf-8 -*-
# 确保测试时载入的类库是本地的而不是通过 pip 安装到全局范围的
import sys
sys.path.insert(1, sys.path[0] + '/../')

import unittest
from json_encode_manager import JSONEncodeManager, CantEncodeObjException
import json
from datetime import datetime
import time
from decimal import Decimal


class JSONEncoderTestCase(unittest.TestCase):
    def setUp(self):
        self.encode_manager = JSONEncodeManager()

    def verify(self, data, expect_result=None, loads_before_compare=False):
        '''
        把 data 转换成 JSON 字符串，然后和 expect_result 对比。

        若 loads_before_compare 为 True，则会把 JSON 字符串解析回 Python 对象后，再进行对比。
        对于 dict 类型的 data，必须这样进行对比。因为最终生成的字符串中，key 的出现顺序是随机的，同样的 dict 可能生成出不同的字符串。
        '''
        result = json.dumps(data, default=self.encode_manager)
        if loads_before_compare:
            result = json.loads(result)
        self.assertEqual(result, expect_result)

    def test_basic_type(self):
        samples = [
            (1, '1'),
            (500, '500'),
            (105.132, '105.132'),
            ('abc', '"abc"'),
            (True, 'true'),
            (None, 'null'),
        ]

        for data, result in samples:
            self.verify(data, result)

    def test_composite_data_type(self):
        samples = [
            ([1, 'a', 10.5], '[1, "a", 10.5]'),
            (('b', 5, True, 1.2), '["b", 5, true, 1.2]'),
        ]
        for data, result in samples:
            self.verify(data, result)

        self.verify(dict(c=1, b=[1, 'a', True]), dict(c=1, b=[1, 'a', True]), loads_before_compare=True)

    def test_predefined_encoder(self):
        def gen():
            l = [1, 2, 3]
            for i in l:
                yield i

        now = datetime.now()

        samples = [
            (now, str(time.mktime(now.timetuple()))),
            (Decimal(10.5), '10.5'),
            (gen(), '[1, 2, 3]'),
        ]

        for data, result in samples:
            self.verify(data, result)

    def test_custom_encoder(self):
        # specialized
        class CustomDataType(object):
            def __init__(self, a, b):
                self.a = a
                self.b = b

        self.encode_manager.register(lambda obj: dict(a=obj.a, b=obj.b), CustomDataType)

        # test if exception throw in common_encoder can be handle well
        def custom_common_encoder1(obj):
            raise CantEncodeObjException()

        self.encode_manager.register(custom_common_encoder1)

        # common_encoder
        class CustomDataType2(object):
            def __init__(self, c, d):
                self.c = c
                self.d = d

        def custom_common_encoder(obj):
            if isinstance(obj, CustomDataType2):
                return dict(c=obj.c, d=obj.d)
            else:
                raise CantEncodeObjException()

        self.encode_manager.register(custom_common_encoder)

        samples = [
            (CustomDataType(Decimal(10.5), 1), {'a': 10.5, 'b': 1}),
            (CustomDataType2(Decimal(20.0), 'a'), {'c': 20.0, 'd': 'a'}),
        ]

        for data, result in samples:
            self.verify(data, result, loads_before_compare=True)

if __name__ == '__main__':
    unittest.main()
