#!/usr/bin/env python3
import json
import os

import story.story

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from PyInquirer import style_from_dict, Token, prompt

from story.story import Story
from story.story import SAVE_PATH
from generator.generator import Generator
import argparse
import re


class Game:
    def __init__(self):
        self.gen = Generator(model_name=args.model[0], gpu=not args.cpugpt)
        self.tts = None if args.jupyter else Dub(gpu=not args.cputts)
        self.style = style_from_dict({
            Token.Separator: '#cc5454',
            Token.QuestionMark: '#673ab7 bold',
            Token.Selected: '#cc5454',  # default
            Token.Pointer: '#673ab7 bold',
            Token.Instruction: '',  # default
            Token.Answer: '#f44336 bold',
            Token.Question: '',
        })
        self.story = Story(self.gen, censor=args.censor)
        self.voice = 1.05
        self.loop = self.loop_speech
        self.sample_hashes = []

    def play(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')

            print("""
▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
███████████████████████████░▄▀█░▄▄▀█▄░▄█░██▀▄▄▀█░▄▄▄█░██░█░▄▄██████████████████████████
███████████████████████████░█░█░▀▀░██░██░██░██░█░█▄▀█░██░█░▄▄██████████████████████████
███████████████████████████▄▄██░██░█▀░▀█▄▄██▄▄██▄▄▄▄██▄▄▄█▄▄▄██████████████████████████
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀""")

            choices = []
            if len([f for f in os.listdir(SAVE_PATH) if f.endswith('.json')]) > 0 or len(self.story.events) > 0:
                choices.append('continue')
            if len([f for f in os.listdir(SAVE_PATH) if f.endswith('.json')]) > 0:
                choices.append('load')

            choices.append('new')
            if not args.jupyter:
                choices.append('voice')

            choices += ['switch to speech input' if self.loop == self.loop_text else 'switch to text input']
            if len(self.story.events) > 2:
                choices.insert(1, 'save')
                choices.insert(2, 'revert')

            main_menu = [{
                'type': list_input_type,
                'message': 'Choose an option',
                'name': 'action',
                'choices': choices
            }]

            action = prompt(main_menu, style=self.style)['action']

            if action == 'new':
                self.new_prompt()
            elif action == 'continue':
                if len(self.story.events) == 0:
                    self.story.cont()
            elif action == 'save':
                self.save_prompt()
            elif action == 'load':
                self.load_prompt()
            elif action == 'voice':
                self.voice_prompt()
            elif action == 'switch to speech input':
                self.loop = self.loop_speech
            elif action == 'switch to text input':
                self.loop = self.loop_text
            elif action == 'revert':
                if len(self.story.events) < 4:
                    self.story.new(ai_name=self.story.ai_name, context=self.story.events[0])
                else:
                    self.story.events = self.story.events[:-2]
            else:
                print('invalid input')

            self.loop()

    def new_prompt(self):
        contexts = {  # display name: (hidden name, hidden context (can be empty))
            'An artificial intelligence': (
                'The computer', 'I was in front of the computer and started talking to an artificial intelligence.'),
            'A robot': ('It', 'A robot was standing in front of me.'),
            'A man': ('He', ''),
            'A woman': ('She', ''),
            'Your dog': ('My dog', 'I was sitting on the couch when my dog suddenly started talking.'),
            'Your cat': ('My cat', 'I was sitting on the couch when my cat suddenly started talking.'),
            'An idiot': ('The idiot', 'I had never met someone more stupid than this person.'),
        }

        menu = [{
            'type': list_input_type,
            'message': 'Who do you want to talk to?',
            'name': 'action',
            'choices': ['< Back'] + [c for c in contexts.keys()]
        }]

        action = prompt(menu, style=self.style)['action']

        if action == '< Back':
            return

        if self.loop == self.loop_text:
            print("Start typing: (\"/help\" to get a list of commands)")

        self.story.new(ai_name=contexts[action][0], context=contexts[action][1])


    def load_prompt(self):
        menu = [{
            'type': list_input_type,
            'message': 'Choose a file to load',
            'name': 'action',
            'choices': ['< Back'] + sorted([f[:-5] for f in os.listdir(SAVE_PATH) if f.endswith('.json')],
                                           key=lambda name: os.path.getmtime(os.path.join(SAVE_PATH, name + '.json')))
        }]

        action = prompt(menu, style=self.style)['action']

        if action != '< Back':
            self.story.load(action)

    def save_prompt(self):
        questions = [{
            'type': 'input',
            'message': "Type a name for your save file.",
            'name': 'user_input'
        }]
        user_input = prompt(questions, style=self.style)['user_input']
        try:
            self.story.save(user_input)
            print(f'Successfully saved {user_input}')
        except:
            print(f'Failed to save the game as {user_input}')

    def loop_text(self):
        self.pprint()

        while True:
            self.pprint()
            user_input = input('> ').strip()

            if user_input in ['/menu', '/m']:
                return
            elif user_input in ['/revert', '/r']:
                self.tts.stop()
                if len(self.story.events) < 4:
                    self.story.new(ai_name=self.story.ai_name, context=self.story.events[0])
                else:
                    self.story.events = self.story.events[:-2]
            elif user_input.startswith('/'):
                print('Known commands:\n'
                      '/h   /help     display this help\n'
                      '/m   /menu     go to main menu (it has a save option)\n'
                      '/r   /revert   revert last action and response (if there are none, regenerate an intro)\n'
                      'Tips:          Press Enter without typing anything to let the AI continue for you.')
                input('Press enter to continue.')
            else:
                action = user_input.strip()
                action = self.punctuate_and_capitalize(action)
                action = '\nI said "' + action + f'"\n{self.story.ai_name} said "'

                result = self.story.act(action)
                self.pprint()
                if result is None:
                    print("--- The model failed to produce an decent output after multiple tries. Try something else.")
                else:
                    if not args.jupyter:
                        self.tts.deep_play(result, self.voice)

    def loop_speech(self):
        self.pprint()

        while True:
            self.pprint()
            try:
                user_input = listen()
            except KeyboardInterrupt:
                return

            action = user_input.strip()
            action = self.punctuate_and_capitalize(action)

            self.pprint()
            print(f"– {action}")

            action = '\nI said "' + action + f'"\n{self.story.ai_name} said "'

            result = self.story.act(action)
            self.pprint()
            if result is None:
                print("--- The model failed to produce an decent output after multiple tries. Try something else.")
            else:
                if not args.jupyter:
                    self.tts.deep_play(result, self.voice)

    def punctuate_and_capitalize(self, action: str):
        # punctuate
        if action[-1] not in ('.', '!', '?'):
            if '?' not in action and '!' not in action and '.' not in action and re.search(
                    r'^\w+', action.lower()).group(0) in [
                'why', 'what', 'where', 'who', 'how', 'did', "didn", 'is', 'are', 'isn', "aren", 'am', 'can', 'could',
                'couldn', 'should', 'shouldn', 'would', 'wouldn', 'may']:
                # don't include 'do' and 'don't' as they are likely to be imperatives
                action = action + '?'
            else:
                action = action + '.'

        # capitalize
        action = re.sub(r'\bi\b', 'I', action)  # capitalize lone 'I'
        action = re.sub('^([a-z])|[\.|\?|\!]\s*([a-z])|\s+([a-z])(?=\.)',
                        lambda matchobj: matchobj.group(0).upper(), action)  # capitalize start of sentences
        return action

    def pprint(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        if args.jupyter:
            print('\n' * 25)  # dirty output clear for jupyter

        text = str(self.story)
        lines = re.findall(r'"(.*?)"', text)  # capture only what's in quotation marks
        lines = ['– ' + l.strip('"') for l in lines]
        text = '\n'.join(lines)

        if text:
            print(text)

    def voice_prompt(self):
        question = [
            {
                'type': 'input',
                'name': 'voice',
                'message': f'Chose a voice speed multiplier (0 to mute sound, 1 for normal speed):',
                'default': str(self.voice),
                'validate': lambda val: val.replace('.', '', 1).isdigit()
            }
        ]

        self.voice = float(prompt(question, style=self.style)['voice'])


if __name__ == "__main__":
    # declare command line arguments
    parser = argparse.ArgumentParser(description='wrAIter: AI writing assistant with a voice')
    parser.add_argument('-j', '--jupyter', action='store_true',
                        default=False,
                        help='jupyter compatibility mode (replaces arrow key selection, disables audio)')
    parser.add_argument('-c', '--censor', action='store_true',
                        default=False,
                        help='adds a censor to the generator')
    parser.add_argument('-m', '--model', action='store',
                        default=['gpt-neo-2.7B'], nargs=1, type=str,
                        help='gpt model name')
    parser.add_argument('-t', '--cputts', action='store_true',
                        default=False,
                        help='force TTS to run on CPU')
    parser.add_argument('-g', '--cpugpt', action='store_true',
                        default=False,
                        help='(broken) force text generation to run on CPU')
    parser.add_argument('-s', '--sttmodel', action='store',
                        default=['stt'], nargs=1, type=str,
                        help='stt model name')

    args = parser.parse_args()

    list_input_type = 'rawlist' if args.jupyter else 'list'

    if not args.jupyter:
        from audio.tts import Dub
        from audio.stt import listen, load_model
        load_model(args.sttmodel[0])

    if not os.path.exists('./saved_stories'):
        os.mkdir('./saved_stories')

    g = Game()
    g.play()
