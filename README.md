dAIlogue is a voiced AI that listens to your microphone input or reads your text input and replies using its own voice.

The AI writer is powered by EleitherAI's GPT-NEO model, a replication of GPT-3.
The suggested model has 2.7 billion parameters
and was fine-tuned to write light novels, including dialogues.

## Features
* [Not yet implemented] State-of-the-art Speech To Text AI that listens to your microphone,
* State-of-the-art Artificial Intelligence that follows the conversation and generates human-like sentences,
* State-of-the-art Text To Speech AI that reads the outputs out loud.
* Pick from multiple speakers, affecting their behaviour: a self-aware AI, a man, a woman, a robot, your cat/dog, or an idiot.


## Local Installation
0. Set up CUDA 11.1 to enable hardware acceleration (need a good GPU).
1. Install python 3.7, [Visual C++ 14.0 (or later)](https://visualstudio.microsoft.com/visual-cpp-build-tools/), portaudio v19 and [eSpeak-ng](https://github.com/espeak-ng/espeak-ng).
2. Set the PHONEMIZER_ESPEAK_PATH environment variable to `C:\Program Files\eSpeak NG\espeak-ng.exe` or wherever you installed it.
3. Download or clone this repository.
4. Run `install.ps1` (windows powershell) or `install.sh` (shell script).
5. Install pyaudio (for windows get it from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)).
6. Download a GPT-NEO model and put its content in `./models/[model name]/`. Here's a link to [finetuneanon's light novel model](https://drive.google.com/file/d/1M1JY459RBIgLghtWDRDXlD4Z5DAjjMwg/view?usp=sharing). 
7. Play by running `play.ps1` (windows powershell) or `play.sh` (shell script). You can also launch `main.py` directly with your own launch options (model selection, gpu/cpu).


## FAQ
_What kind of hardware do I need?_
CPU inference is currently broken for text generation, and enabled by default for text-to-speech (launch option).
So you'll need a GPU with at least 8 GB of VRAM. If you run into video memory issues, you can lower `max_history`
in `./generator/generator.py` (maximum number of "words" that the AI can read before writing text).

_Does the AI learn from my inputs?_

While the AI remembers the last thousand words of the conversation, it doesn't learn from it.
Playing or saving a discussion won't affect the way it plays another.

_Does the AI forget parts of the conversation?_

Yes. Because the model can only take 1024 words in the input, the oldest events can be dropped to make the story fit.
However, the context of the conversation (your choice of its identity) is never "forgotten".

Until you hit 1024 words, longer stories yield progressively better results.

_Can I fine-tune the AI on a corpus of my choice?_

I didn't bother with fine-tuning with GPT-NEO. The model is just too large to fit into my machine or any free cloud GPU.
So you're on your own.

_dAIlogue is a terrible name._

Yes it is.

_Does this thing respect my privacy?_

Yes, dAIlogue only needs to connect to the internet to download the TTS model and to install python packages.
It doesn't upload anything, and only saves conversations on your hard drive if you explicitly ask it to.
To play sound, the last played wave file is also stored on your machine.

_I read an article about AIdungeon and profanity. Doesn't this have the same issues?_

No. First, dAIlogue doesn't adjust based on your or other players' inputs. The model runs on your machine,
so tempering with it would only affect your own experience. Second, a censor is enabled by default, trashing and
regenerating entire paragraphs if the model outputs a single banned word. It can be disabled in the launch options,
giving you the freedom of choice.


## Credits
* [EleutherAI](https://www.eleuther.ai/projects/gpt-neo/) for GPT-NEO,
* [coqui-ai](https://github.com/coqui-ai) for the TTS and STT models.
