# CustomEmailPython

Sends a short multipart email (plain text and HTML) over SMTP. The default
connection is Gmail on port 465 with SSL, using an app password.

The subject is `multipart test`. The body is a short greeting that includes a
link to https://github.com/dpradeep42.

## Requirements

- Python 3
- A Gmail account with 2-Step Verification enabled, and an app password

## Setup

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env`:

1. Set `SENDER_EMAIL` to the Gmail address that sends the message. That address is also the SMTP username.
2. Create an app password. Open <https://myaccount.google.com/apppasswords> while signed in to the sender account (2-Step Verification has to be on), create a password for Mail, and paste the 16-character value into `SMTP_PASSWORD`. This is an app password, not the normal Gmail password.
3. Set `RECEIVER_EMAIL` to the recipient.
4. Leave `SMTP_HOST` as `smtp.gmail.com`, `SMTP_PORT` as `465`, and `SMTP_USE_SSL` as `true` for Gmail.

`.env` is listed in `.gitignore`. Keep it out of git.

Values already present in the environment take precedence over `.env`.

## Environment variables

| Variable | Required | Default | Purpose |
| --- | --- | --- | --- |
| `SENDER_EMAIL` | yes | | From address and SMTP username |
| `SMTP_PASSWORD` | yes | | Gmail app password, or the SMTP password |
| `RECEIVER_EMAIL` | yes | | To address |
| `SMTP_HOST` | no | `smtp.gmail.com` | SMTP server hostname |
| `SMTP_PORT` | no | `465` | SMTP server port |
| `SMTP_USE_SSL` | no | `true` | `true` opens an implicit TLS connection (`SMTP_SSL`). `false` uses plain SMTP, which is what a local debugging server expects. |

With `SMTP_USE_SSL=false`, the script calls `LOGIN` only when the server advertises `AUTH`.

## Usage

From the project directory, with the virtual environment active:

```bash
python main.py
```

A successful send exits with status 0 and prints nothing. If a required variable is missing, the script prints the variable name and exits with status 1. SMTP failures are raised by `smtplib`.

## Local debugging server

`aiosmtpd` is only needed for this check. It is not part of `requirements.txt`.

```bash
pip install aiosmtpd
python -m aiosmtpd -n -l localhost:1025
```

In another shell:

```bash
SENDER_EMAIL=sender@example.com \
RECEIVER_EMAIL=recipient@example.com \
SMTP_PASSWORD=unused \
SMTP_HOST=localhost \
SMTP_PORT=1025 \
SMTP_USE_SSL=false \
python main.py
```

The debugging server prints the message it accepted, between `MESSAGE FOLLOWS` and `END MESSAGE`.

## License

MIT. See [LICENSE](LICENSE).
