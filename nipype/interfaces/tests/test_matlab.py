import os
from tempfile import mkdtemp
from shutil import rmtree

from nipype.testing import (assert_equal, assert_true, assert_false, 
                            assert_raises, skipif)
import nipype.interfaces.matlab as mlab
from nipype.interfaces.base import CommandLine, Bunch

try:
    matlab_cmd = os.environ['MATLABCMD']
except:
    matlab_cmd = 'matlab'

res = CommandLine(command='which', args=matlab_cmd).run()
matlab_path = res.runtime.stdout.strip()

matlab_command = ''
no_matlab = True
if matlab_path != '':
    matlab_command = '%s -nodesktop -nosplash' % \
        matlab_path.split(os.path.sep)[-1]
    no_matlab = False
    
# If a test requires matlab, prefix it with the skipif decorator like
# below.  Must import skipif from nipype.testing
#
#@skipif(no_matlab)
# def test_func():
#     pass

def test_init():
    mi = mlab.MatlabCommand()
    yield assert_equal, mi._cmdline, None
    yield assert_equal, mi._cmdline_inputs, None
    mi = mlab.MatlabCommand(matlab_cmd='foo')
    yield assert_equal, mi.matlab_cmd, 'foo'

def test_cmdline():
    basedir = mkdtemp()

    mi = mlab.MatlabCommand(script='whos',
                            script_file='testscript')
                                
    yield assert_equal, mi.cmdline, \
        'matlab -nodesktop -nosplash -singleCompThread -r "fprintf(1,\'Executing code at %s:\\n\',datestr(now));ver,try,whos,catch ME,ME,ME.stack,fprintf(\'%s\\n\',ME.message);fprintf(2,\'<MatlabScriptException>\');fprintf(2,\'%s\\n\',ME.message);fprintf(2,\'File:%s\\nName:%s\\nLine:%d\\n\',ME.stack.file,ME.stack.name,ME.stack.line);fprintf(2,\'</MatlabScriptException>\');end;;exit"'
 
    yield assert_equal, mi.inputs.script, 'whos'
    yield assert_equal, mi.inputs.script_file, 'testscript'
    yield assert_equal, mi.inputs.environ, {}
    path_exists = os.path.exists(os.path.join(basedir,'testscript.m'))
    yield assert_false, path_exists
    rmtree(basedir)


if matlab_path != '':
    matlab_command = matlab_path.split(os.path.sep)[-1]
    no_matlab = False

def test_mlab_inputspec():
    spec = mlab.MatlabInputSpec()
    for k in ['paths', 'script', 'nosplash', 'mfile', 'logfile', 'script_file',
              'nodesktop']:
        yield assert_true, k in spec.copyable_trait_names()
    yield assert_true, spec.nodesktop
    yield assert_true, spec.nosplash
    yield assert_false, spec.mfile
    yield assert_equal, spec.script_file, 'pyscript.m'

def test_init():
    yield assert_equal, mlab.MatlabCommand._cmd, 'matlab'
    yield assert_equal, mlab.MatlabCommand.input_spec, mlab.MatlabInputSpec

    yield assert_equal, mlab.MatlabCommand().cmd, mlab.MatlabCommand._cmd
    mc = mlab.MatlabCommand(matlab_cmd='foo_m')
    yield assert_equal, mc.cmd, 'foo_m'
    
@skipif(no_matlab)
def test_run_interface():
    mc = mlab.MatlabCommand(matlab_cmd='foo_m')
    yield assert_raises, ValueError, mc.run # script is mandatory
    mc.inputs.script = 'a=1;'
    yield assert_raises, IOError, mc.run # foo_m is not an executable
    cwd = os.getcwd()
    basedir = mkdtemp()
    os.chdir(basedir)
    res = mlab.MatlabCommand(script='foo', paths=[basedir], mfile=True).run() # bypasses ubuntu dash issue
    yield assert_equal, res.runtime.returncode, 1
    res = mlab.MatlabCommand(script='a=1;', paths=[basedir], mfile=True).run() # bypasses ubuntu dash issue
    yield assert_equal, res.runtime.returncode, 0
    os.chdir(cwd)
    rmtree(basedir)
    
def test_set_matlabcmd():
    mi = mlab.MatlabCommand()
    mi.set_default_matlab_cmd('foo')
    yield assert_equal, mi._default_matlab_cmd, 'foo'
    mi.set_default_matlab_cmd(matlab_command)
    mi.inputs.
