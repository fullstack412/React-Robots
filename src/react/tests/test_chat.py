#!/usr/bin/env python
# PKG = 'react'
#import roslib; roslib.load_manifest(PKG)

import sys
import unittest

from react.examples.chat.chat_model import *
from react.api.model import * 
from react.api.metamodel import * 
from react.helpers.test.model_test_helper import ModelTestHelper

class TestChat(unittest.TestCase, ModelTestHelper):
    def test_msg(self): self.assert_record_cls(Msg, RecordMeta)


if __name__ == '__main__':
    import rosunit
    rosunit.unitrun('react', 'test_chat', TestChat)