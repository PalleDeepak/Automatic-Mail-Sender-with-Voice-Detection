from voice import listen_for_phrase, listen_for_text
from emailer import send_email
import json, os, sys

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config.json")
CONFIG_PATH = os.path.abspath(CONFIG_PATH)

def load_config(path):
    if not os.path.exists(path):
        print("Missing config.json. Please copy config.example.json to config.json and fill the SMTP credentials.")
        sys.exit(1)
    with open(path, "r") as f:
        return json.load(f)

def spoken_confirm(prompt="Say 'yes' to confirm"):
    print(prompt)
    resp = listen_for_text(timeout=8)
    return resp and resp.strip().lower() in ("yes", "yeah", "yup", "confirm", "correct")

def main():
    cfg = load_config(CONFIG_PATH)
    print("Listening for trigger phrase: 'send email' or 'send mail' (say 'quit' to exit)")
    while True:
        phrase = listen_for_phrase(timeout=None)
        if not phrase:
            continue
        p = phrase.lower()
        print("Heard:", p)
        if "quit" in p or "exit" in p:
            print("Exiting.")
            break
        if "send email" in p or "send mail" in p or "send email to" in p:
            print("Trigger detected — collecting email details by voice.")
            print("Say recipient email address (speak slowly, e.g. 'alice at example dot com')")
            to_addr = listen_for_text(timeout=10)
            if not to_addr:
                print("No recipient detected — returning to listening.")
                continue
            print("Recipient (raw):", to_addr)

            print("Say subject now:")
            subject = listen_for_text(timeout=8) or "(no subject)"
            print("Subject:", subject)

            print("Say body (you can say 'stop' when finished):")
            body = listen_for_text(timeout=20) or ""
            print("Body (raw):", body)

            print("\nPlease confirm sending the email. Say 'yes' to send.")
            if spoken_confirm():
                print("Sending email...")
                ok, err = send_email(cfg, to_addr, subject, body)
                if ok:
                    print("Email sent successfully.")
                else:
                    print("Failed to send email:", err)
            else:
                print("Not confirmed — email not sent.")
        else:
            print("Trigger phrase not recognized. Keep listening...")

if __name__ == '__main__':
    main()
