# pitt

an extremely simple terminal-based password manager

## installation

pip
```bash
pip install pitt
```

uv
```bash
uv tool install pitt
```

# demo
[![pitt demo](https://img.youtube.com/vi/g3S1TFWb2uU/maxresdefault.jpg)](https://www.youtube.com/watch?v=g3S1TFWb2uU)
(click)

## workflow

1. initializing the password manager:
    - new:
        - `pitt init` and follow the instructions
    - import from csv (exported pitt passwords):
        * `pitt init -i /path/to/.csv` and follow the instructions

2. adding a password:
    - randomly generated password:
        - you'd have to specify a service, username or a note that'll be attached with the newly generated password when saved.
        * `pitt add -s service_example -u username_example -n "note example"`
    - custom password:
        - you'd have to still specify one of the three things (username, service, note)
        * `pitt add -s service_example -u username_example -n "note example" -c` (note the added -c flag)

3. deleting a password:
    - you need to specify the service or username (can be both but cannot be the note) that is affiliated with the saved password you want to delete.
    * `pitt del -s service_example -f` (the -f or --force flag will disgard the 'are you sure' confirmations and straight up just deletes the password. use -f with caution)

4. getting a password:
    - you need to specify the service or username (can be both) but cannot be the note that is affiliated with the saved password you want to get (copy to clipboard).
    * `pitt get -s service_example`

5. listing all the saved passwords' information:
    * `pitt list` (this will only list all the information that's attached to each password, not the passwords themselves.)

6. export all the saved passwords:
    - interactive mode:
        * `pitt exp` 
    - manual mode:
        * `pitt exp -p /path/to/wherever`

## license

this project is licensed under the MIT License - see the LICENSE file for details

## credits

inspired by: themohitnair's sfnx | (https://github.com/themohitnair/sfnx)

---

curated by me alongside some rubber ducks
