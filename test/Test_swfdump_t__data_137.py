'''
Created on Oct 29, 2015

@author: yangke
'''
from model.TaintVar import TaintVar
from TraceTrackTest import TraceTrackTest
class Test_swfdump_t__data_137:
    
    '''
    This is a test for the trace generated by exploit_137_0 of swfdump which is caused by null pointer t->data.
    Note that the root cause is the negative value initiated in 'for' statement of function swf_GetBits.
    -----------------------------------------------------------------
    U32 swf_GetBits(TAG * t,int nbits):lib/rfxswf.c:202
    
    211      int i,m=t->len>10?10:t->len;
    212      for(i=-1;i<m;i++) {
                    ^ 
    213        fprintf(stderr, "(%d)%02x ", i, t->data[i]);
                                                    ^
    ------------------------------------------------------------------
    Stack Trace:
    #0  0x08064e35 in swf_GetBits (t=0x80fe008, nbits=5) at rfxswf.c:214
    #1  0x080660b9 in swf_GetRect (t=0x80fe008, r=0xbfffe3f0) at rfxswf.c:693
    #2  0x0804af20 in handleEditText (tag=0x80fe008) at swfdump.c:494
    #3  0x0804ee31 in main (argc=3, argv=0xbfffe804) at swfdump.c:1496
    '''
    
    def test(self):
        passed_message="SWFTOOLS-0.9.2 't->data' in 't->data[i]' TEST PASSED!"
        not_pass_message="ERRORS FOUND DURING SWFTOOLS-0.9.2 't->data' in 't->data[i]' TEST!"
        answer_path='answers/swftools-0.9.2/swfdump/'
        name='swftools-0.9.2_swfdump_t-data_137'
        logfile_path="gdb_logs/swftools-0.9.2/swfdump/gdb-swfdump_t-data_i_137.txt"
        c_proj_path='gdb_logs/swftools-0.9.2/swftools-0.9.2'
        taintVars=[TaintVar("t->data",["*"])]
        test=TraceTrackTest(answer_path,name,logfile_path,taintVars,passed_message,not_pass_message)
        test.set_c_proj_path(c_proj_path)
        passed=test.test()
        return passed
if __name__ == '__main__':
    test=Test_swfdump_t__data_137()
    test.test()