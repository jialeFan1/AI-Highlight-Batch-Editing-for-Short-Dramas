import subprocess
import os
import sys

# 获取虚拟环境路径
venv_python = os.path.join(os.environ['VIRTUAL_ENV'], 'Scripts', 'python.exe')

# 执行提取音频的脚本
subprocess.call([venv_python, "scripts/extract_audio.py"])

# 执行分割音频的脚本
subprocess.call([venv_python, "scripts/split_audio.py"])

# 执行音频转文本的脚本
subprocess.call([venv_python, "scripts/transcribe_audio.py"])

# 执行生成高光片段文案的脚本
subprocess.call([venv_python, "scripts/create_highlight_script.py"])

# 执行提取视频片段的脚本
subprocess.call([venv_python, "scripts/extract_clips.py"])

# 执行合并视频片段的脚本
subprocess.call([venv_python, "scripts/merge_clips.py"])
