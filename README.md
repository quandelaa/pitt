# pitt

an extremely simple terminal-based password manager (work in progress)

## installation

```bash
pip install git+https://github.com/quandelaa/pitt.git
```

## usage

### commands

1. `pitt init`:
    * asks for a master password
    * when given, encrypts it using Argon2id and stores it in the database

    example:
    ```bash
    pitt init
    ```

2. `pitt add`:
    * create random password
    * encrypts the random password using Fernet
    * stores the encrypted password with a specified username or service or note in the database

    example:
    ```bash
    pitt add --service github --username quandelaa --note "this is my song"
    ```

3. `pitt get`:
    * gets the password that is saved with the given service or username (case sensitive)
    * decrypts the password
    * copies it to user's clipboard

    example:
    ```bash
    pitt get --service github --username quandelaa"
    ```

4. `pitt list`:
    * lists only the details (service, username and notes) of all the saved passwords

    example:
    ```bash
    pitt list"
    ```

## license

this project is licensed under the MIT License - see the LICENSE file for details

## credits

inspired by: themohitnair's sfnx | (https://github.com/themohitnair/sfnx)

---

by `quandela` or `quandelaa` with the purest of joy and a little hint of confusion
