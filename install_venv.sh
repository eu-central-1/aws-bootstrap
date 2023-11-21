#! /bin/bash
# This file must be used with "source bin/activate" *from bash*
# you cannot run it directly


# Bash allows return statements only from functions
# and, in a script's top-level scope, if the script is sourced
if (return 0 2>/dev/null) ; then
    test -d .venv || python3.9 -m venv .venv
    source .venv/bin/activate && pip3 install -r requirements-dev.txt

    if [ "$(which python)" = "$(pwd)/.venv/bin/python" ]
    then
        echo -e "\n"
        echo -e "'\033[0;32mvenv\033[0m' and '\033[32msam\033[0m' installed successfully."
        echo -e "For exit venv please use '\033[0;32mdeactivate\033[0m'."
    else
        echo -e "\033[0;31m'venv'\033[0m setup could be completed successfully."
    fi
else
    echo -e "Please run script with '\033[0;31msource $0\033[0m'"
fi