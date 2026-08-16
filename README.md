# pitt

an extremely simple terminal-based password manager

## installation

```bash
pip install pitt
```

# demo
![pitt demo video](assets/pitt_demonstration.mp4)

## usage

### commands

1. `pitt init`:
    * asks for a master password
    * when given, hashes it using Argon2id and stores it in the database

    example:
    ```bash
    pitt init
    ```

2. `pitt add`:
    * create random password
    * encrypts the random password using Fernet
    * stores the encrypted password with the specified username, service or note in the database

    example:
    ```bash
    pitt add --service github --username quandelaa --note "this is my song"
    ```

3. `pitt get`:
    * gets the password that is saved with the given service or username
    * decrypts the password
    * copies it to user's clipboard

    example:
    ```bash
    pitt get --service github --username quandelaa
    ```

4. `pitt list`:
    * lists only the details (service, username and note) of all the saved passwords

    example:
    ```bash
    pitt list
    ```

4. `pitt del`:
    * gets the password that is saved with the given service or username
    * asks for confirmation
    * deletes the found password 

    example:
    ```bash
    pitt del --service github --username quandelaa
    ```

## license

this project is licensed under the MIT License - see the LICENSE file for details

## credits

inspired by: themohitnair's sfnx | (https://github.com/themohitnair/sfnx)

---

curated by me alongside some rubber ducks
