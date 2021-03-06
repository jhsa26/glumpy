# The MIT License (MIT)
#
# Copyright (c) 2014 Zulko
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# File from the MoviePy project - released under licence MIT
# See https://github.com/Zulko/moviepy

import os
import subprocess as sp
try:
    from subprocess import DEVNULL  # py3k
except ImportError:
    DEVNULL = open(os.devnull, 'wb')
    
if os.name == 'nt':
    try:    
        import winreg as wr # py3k
    except:
        import _winreg as wr # py2k

from .ffmpeg_config_defaults import (FFMPEG_BINARY, IMAGEMAGICK_BINARY)

def try_cmd(cmd):
        try:
            popen_params = { "stdout": sp.PIPE,
                             "stderr": sp.PIPE,
                              "stdin": DEVNULL
                            }

            
            # This was added so that no extra unwanted window opens on windows
            # when the child process is created
            if os.name == "nt":
                popen_params["creationflags"] = 0x08000000

            proc = sp.Popen(cmd, **popen_params)
            proc.communicate()
        except Exception as err:
            return False, err
        else:
            return True, None

if FFMPEG_BINARY=='ffmpeg-imageio':
    from imageio.plugins.ffmpeg import get_exe
    FFMPEG_BINARY = get_exe()

elif FFMPEG_BINARY=='auto-detect':

    if try_cmd(['ffmpeg'])[0]:
        FFMPEG_BINARY = 'ffmpeg'
    elif try_cmd(['ffmpeg.exe'])[0]:
        FFMPEG_BINARY = 'ffmpeg.exe'
    else:
        FFMPEG_BINARY = 'unset'
else:
    success, err = try_cmd([FFMPEG_BINARY])
    if not success:
        raise IOError(err.message +
                 "The path specified for the ffmpeg binary might be wrong")



if IMAGEMAGICK_BINARY=='auto-detect':
    if os.name == 'nt':    
        try:
            key = wr.OpenKey(wr.HKEY_LOCAL_MACHINE, 'SOFTWARE\\ImageMagick\\Current')
            IMAGEMAGICK_BINARY = wr.QueryValueEx(key, 'BinPath')[0] + r"\convert.exe"
            key.Close()
        except:
            IMAGEMAGICK_BINARY = 'unset'
    elif try_cmd(['convert'])[0]:
        IMAGEMAGICK_BINARY = 'convert'
    else:
        IMAGEMAGICK_BINARY = 'unset'
else:
    success, err = try_cmd([IMAGEMAGICK_BINARY])
    if not success:
        raise IOError(err.message +
                 "The path specified for the ImageMagick binary might be wrong")



def get_setting(varname):
    """ Returns the value of a configuration variable. """ 
    gl = globals()
    if varname not in gl.keys():
        raise ValueError("Unknown setting %s"%varname)
    # Here, possibly add some code to raise exceptions if some
    # parameter isn't set set properly, explaining on how to set it.
    return gl[varname]


def change_settings(new_settings={}, file=None):
    """ Changes the value of configuration variables."""
    gl = globals()
    if file is not None:
        execfile(file)
        gl.update(locals())
    gl.update(new_settings)
    # Here you can add some code  to check that the new configuration
    # values are valid.

if __name__ == "__main__":
    if try_cmd([FFMPEG_BINARY])[0]:
        print( "MoviePy : ffmpeg successfully found." )
    else:
        print( "MoviePy : can't find or access ffmpeg." )

    if try_cmd([IMAGEMAGICK_BINARY])[0]:
        print( "MoviePy : ImageMagick successfully found." )
    else:
        print( "MoviePy : can't find or access ImageMagick." )


