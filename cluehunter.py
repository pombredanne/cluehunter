'''
Created on Dec 19, 2015

@author: yangke
'''
import logging
import argparse
import os
import subprocess
from parse.parse import LogParser
from model.TaintVar import TaintVar
from Tracker import Tracker
from parse.RedundancyFixer import RedundancyFixer

DESCRIPTION = """ClueHunter is a auxiliary crash analysis tools.
It draws data flow graph according to the gdb debug log.
Taint data of the last line executed should be specified."""
DEFAULT_GDB_LOG="test/gdb_logs/swfmill-0.3.3/gdb-swfmill-0.3.3.txt"
DEFAULT_OUTPUT_PATH="."
DEFAULT_NAME="output"
class ClueHunter:
    def __init__(self):
        self._init_arg_parser()
        self.args = self.arg_parser.parse_args()
        self.checkArguments()
        self._config_logger()
        
        self._create_output_dir()
        #self.args.logging_level==logging.DEBUG or self.args.logging_level==logging.INFO)
        
    def checkArguments(self):
        err=''
        if len(self.args.patterns)==0 and len(self.args.variables)==0:
            err='At least one sink variable should be provided.\nUse --variable [VARIABLE_NAME_LIST] --patterns [DATA_ACCES_PATTERNS_LIST]'
        elif len(self.args.patterns)!=len(self.args.variables):
            err='Variables and patterns number must be same!'
        else:
            for p in self.args.patterns:
                if p!='*' and p!='N':
                    err='The specified pattern must be "*" or "N".'
                    break
        if self.args.level!=RedundancyFixer.REMOVE_INLINE_REDUNDANT and self.args.level!=RedundancyFixer.REMOVE_INTERPROCEDURAL_REDUNDANT:
            err='Redundancy level should be 0 or 1'
            
        if err!='':
            self.arg_parser.error(err)
            
    def _init_arg_parser(self):
        self.arg_parser = argparse.ArgumentParser(description=DESCRIPTION)
        source_sink_group=self.arg_parser.add_argument_group('sinks')
        source_sink_group.add_argument(
                '-ps','--patterns',
                action='store',
                dest='patterns',
                required=True,
                nargs='+',
                default=['N'],
                help='''Specify the access pattern list of the sink identifiers. 
                Patterns must be "*" or "N" separated with blanks.
                "N" means direct access, "*" means this is a pointer of the cared data.
                ''')
        
        source_sink_group.add_argument(
                '-vs','--variables',
                action='store',
                dest='variables',
                required=True,
                nargs='+',
                default=['length'],
                help='Specify the identifier name of the sink variable. Example:father->baby.toy')
        
        self.arg_parser.add_argument(
                '-l', '--level',
                action = 'store',
                default = 1,
                type = int,
                help = """Redundancy level of the parsing.
0 means just remove inline or innner function redundancy; 1 means remove  both of the inline and interprocedural reduandancy.""")
        self.arg_parser.add_argument(
                '-t', '--trace',
                action = 'store',
                dest='trace',
                required=True,
                default = DEFAULT_GDB_LOG,
                help = """The file path of gdb trace log, for example, ./gdb.txt. This log should be generated by robot_dbg.exp.""")
        self.arg_parser.add_argument(
                '-o', '--output-directory',
                action = 'store',
                dest="output_path",
                default = DEFAULT_OUTPUT_PATH,
                help = """The output directory in which .dot and .png files will be dumped in this path.""")
        self.arg_parser.add_argument(
                '-n', '--name',
                action = 'store',
                dest = "name",
                default = DEFAULT_NAME,
                help = """The prefix name of the generated .dot and .png files.""")
        
        group = self.arg_parser.add_mutually_exclusive_group()
        group.add_argument(
                '-d', '--debug',
                action = 'store_const',
                const = logging.DEBUG,
                dest = 'logging_level',
                default = logging.WARNING,
                help = """Enable debug output.""")
        group.add_argument(
                '-v', '--verbose',
                action = 'store_const',
                const = logging.INFO,
                dest = 'logging_level',
                default = logging.WARNING,
                help = """Increase verbosity.""")
        group.add_argument(
                '-q', '--quiet',
                action = 'store_const',
                const = logging.ERROR,
                dest = 'logging_level',
                default = logging.WARNING,
                help = """Be quiet during processing.""")
    def build_tiantvars_list(self):
        vs=[]
        for i in range(0,len(self.args.variables)):
            if self.args.patterns[i]=='N':
                p=[]
            else:
                p=['*']
            vs.append(TaintVar(self.args.variables[i],p))
        return vs
            
    def _analysis(self):
        parser=LogParser()
        parser.setRedundantLevel(self.args.level)
        l=parser.parse(self.args.trace)
        tracker=Tracker(l)
        traceIndex=len(l)-1
        vs=self.build_tiantvars_list()
        tracker.setStartJobs(traceIndex, vs)
        
        TG=tracker.track()
        output=file(self.args.output_path+"/"+self.args.name+".dot", 'w')
        print TG.serialize2dot()
        output.write(TG.serialize2dot())
        output.close()
        subprocess.call("dot -Tpng "+self.args.output_path+"/"+self.args.name+".dot -o "+self.args.output_path+"/"+self.args.name+".png", shell = True)
        #print str(TG)
    def execute(self):
        self._analysis()
    def _create_output_dir(self):
        output_path = self.args.output_path
        if not os.path.isdir(output_path):
            self.logger.debug('Creating directory %s.', os.path.abspath(output_path))
            os.makedirs(output_path)
        self.logger.info('Output directory is %s.', os.path.abspath(output_path))

    
    def _config_logger(self):
        self.logger = logging.getLogger('cluehunter')
        self.logger.setLevel('DEBUG')
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.args.logging_level)
        file_handler = logging.FileHandler('cluehunter.log', 'w+')
        file_handler.setLevel('DEBUG')
        #console_formatter = logging.Formatter('%(message)s')
        console_formatter = logging.Formatter('[%(levelname)s] %(message)s')
        file_formatter = logging.Formatter('[%(levelname)s] %(message)s')
        console_handler.setFormatter(console_formatter)
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
        
if __name__=="__main__":
    c=ClueHunter()
    c.execute()
    
