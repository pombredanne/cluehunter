'''
Created on Oct 7, 2015

@author: yangke
'''
import re
import subprocess
from model.TaintGraph import TaintGraph
from parse.parse import LogParser
from model.TaintJob import TaintJob
from model.TaintVar import TaintVar
from parse.FunctionCallInfo import FunctionCallInfo
from parse.LineOfCode import LineOfCode
from utils.Filter import Filter
from Tracker import Tracker
import filecmp
import time
from TraceTrackTest import TraceTrackTest
class Test_foomoo_a:
    def test(self):
        passed_message="FOOMOO 'a' TEST PASSED!"
        not_pass_message="ERRORS FOUND IN FOOMOO 'a' TEST!"
        answer_path='answers/foomoo/'
        name='foomoo_a'
        logfile_path="gdb_logs/foomoo/gdb-foomoo.txt"
        taintVars=[TaintVar("a",[])]
        test=TraceTrackTest(answer_path,name,logfile_path,taintVars,passed_message,not_pass_message)
        passed=test.test()
        return passed
           
if __name__ == '__main__':
    test=Test_foomoo_a()
    test.test()
    