

# Server-Temperature-Notifier

### A Python script that takes the servers core temperature and notify when it surpasses a certain threshold

---

#### Description

This script uses hwmon to capture all the core temperatures, then calculate their average and compare it to a certain threshold, if it was higher an email will be sent to the employees to sort the problem out and an IOT device will turn on the AC.

---

#### Dependancies

This is a python3 script and assumes you have python3 & pip3 installed

For this script to work you have to install the packages in `requirements.txt` this can be done using

```python
pip3 install -r requirements.txt
```

This script depends on

- logzero
- hwmon

---

#### Installation 

This script was meant to be run by a cron job on a linux server, just add :

```bash
1 * * * * python3 /path/to/script/main.py
```

to your crontab file

---

#### Notes

make a `mail_setup.json` from the `mail_setup_template.json` file and edit to setup your mail server and ensure that the server allows less secure apps.

the threshold temperature for sending a notification can be changed in the `main.py` script

