'''
Created on Dec 13, 2015

@author: yangke
'''
from model.TaintJob import TaintJob
from model.TaintVar import TaintVar
import re
num_pattern=re.compile(r"\s*[0-9]|([1-9][0-9]+)\s*")
class read_handler(object):
    @staticmethod
    def gen_match_str(variable):
        access=variable.accessStr()
        if '|' not in access:
            return r"(?<![_A-Za-z0-9])read\s*\(\s*([^,\(]*),\s*&\s*"+access+r"([^,\(]*),([^,\(]*)\s*\)"
        else:
            pointerstr=variable.pointerStr()
            return r"(?<![_A-Za-z0-9])read\s*\(\s*([^,\(]*),"+pointerstr+r"([^,\(]*),([^,\(]*)\s*\)"        
    @staticmethod
    def isArgDef(variable,codestr):
        lib_definition=read_handler.gen_match_str(variable)
        m=re.search(lib_definition,codestr)
        if m is None:
            return False
        else:
            return True
    @staticmethod
    def getJobs(i,varstr,codestr):
        syscall_definition=read_handler.gen_match_str(varstr)
        m=re.search(syscall_definition,codestr)
        jobs=[]
        if m:
            fp=m.group(1)
            jobs.append(TaintJob(i,TaintVar(fp,['*'])))
            count=m.group(3)
            if "sizeof" not in count and num_pattern.match(count) is not None:
                jobs.append(TaintJob(i,TaintVar(count,[])))
            print "read is handled!"
        return jobs