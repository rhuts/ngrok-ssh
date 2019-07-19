# ngrok-ssh
setup ngrok ssh from anywhere and get the port emailed to you

## Usage
1. Edit crontab

`sudo crontab -e`

---

2. Add below line (modify to your environment):

`@reboot /usr/bin/python3 /<path>/repos/ngrok-ssh/ngrok_on_login.py &`

---

3. Edit configs for:
    - email info
    - Ngrok account authtoken

`vim /<path>/repos/ngrok-ssh/config.py`

---

4. Reboot and you're good