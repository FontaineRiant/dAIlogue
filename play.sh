source ./venv/Scripts/activate
python main.py --censor --model gpt-neo-2.7B-horni-ln --cputts --sttmodel stt
read -sn 1 -p "Press any key to continue..."