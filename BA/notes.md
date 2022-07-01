# BA

Thesis:
https://www.dropbox.com/s/g654q9dujep5nbd/SA_TobiasModschiedler.pdf?dl=0

Links:

- http://i80misc01.ira.uka.de/coffee/kasse.php?token=C0FFEE

- [BA](#ba)
  - [1. Make new KIT-Card work](#1-make-new-kit-card-work)
  - [2. Sound system](#2-sound-system)
    - [Q: Which speakers?](#q-which-speakers)
  - [3. Warm-up out of energy saving mode (needs to unlock several times)](#3-warm-up-out-of-energy-saving-mode-needs-to-unlock-several-times)
  - [4. Implement proper logging](#4-implement-proper-logging)
  - [5. Potential 'free coffee' bug when you refill the water tank](#5-potential-free-coffee-bug-when-you-refill-the-water-tank)
    - [Q: What about the sensors. Current ones used are different from the ones listed in the first thesis](#q-what-about-the-sensors-current-ones-used-are-different-from-the-ones-listed-in-the-first-thesis)
  - [6. Milk setting (with milk/without milk) not properly saved](#6-milk-setting-with-milkwithout-milk-not-properly-saved)
  - [7. DONE Turn-off the screen-saver](#7-done-turn-off-the-screen-saver)
    - [Changed](#changed)
  - [8. When trying to log in with an unregistered card, message should be confirmed](#8-when-trying-to-log-in-with-an-unregistered-card-message-should-be-confirmed)
  - [9. Whenever one of the 'worst milk guys' logs in, he/she should get bad milk warning message...](#9-whenever-one-of-the-worst-milk-guys-logs-in-heshe-should-get-bad-milk-warning-message)
  - [10. Maybe we could send automatic eMails to the worst milk guys...](#10-maybe-we-could-send-automatic-emails-to-the-worst-milk-guys)
  - [11. Every then-and-when there is a bug in the GUI and it hangs...](#11-every-then-and-when-there-is-a-bug-in-the-gui-and-it-hangs)
  - [12. The Snoopy comic with the football is already displayed since 100 years. Something is wrong with the update there.](#12-the-snoopy-comic-with-the-football-is-already-displayed-since-100-years-something-is-wrong-with-the-update-there)
    - [Q: Is this still the case?](#q-is-this-still-the-case)
  - [13. The 3D-printed case should be finished and used](#13-the-3d-printed-case-should-be-finished-and-used)
    - [TODO: split 3d model with blender](#todo-split-3d-model-with-blender)
  - [4. offline mode](#4-offline-mode)
    - [Q: what's the server side code?](#q-whats-the-server-side-code)
  - [14. Is there actually a proper backup of the server-side data-base? It](#14-is-there-actually-a-proper-backup-of-the-server-side-data-base-it)
  - [15. Rinsing is detected as hot water and the user is charged. It should not charge the user.](#15-rinsing-is-detected-as-hot-water-and-the-user-is-charged-it-should-not-charge-the-user)
    - [Q: When can this happen?](#q-when-can-this-happen)
  - [16. Android app](#16-android-app)
  - [TODO](#todo)
  - [Questions](#questions)
  - [Model](#model)
  - [Challenges](#challenges)
  - [Icons Credit](#icons-credit)
- [Libraries](#libraries)

## 1. Make new KIT-Card work

- Protocol ISO 14443-4
- Drivers

## 2. Sound system

### Q: Which speakers?

Can speakers present at the office be used?

## 3. Warm-up out of energy saving mode (needs to unlock several times)

40 second session, after that machine is locked
when machine is locked,
machine doesn't warm up when it's locked

## 4. Implement proper logging

- use logger.debug(), warn, info, error
- print to terminal
- use systemd to archive and run the job: https://wiki.archlinux.org/index.php/Systemd/User

## 5. Potential 'free coffee' bug when you refill the water tank

### Q: What about the sensors. Current ones used are different from the ones listed in the first thesis

## 6. Milk setting (with milk/without milk) not properly saved

Maybe it is saved system-wide instead of per-user (as stored in the database)?

## 7. DONE Turn-off the screen-saver

It is not needed and it often fails in properly showing whether or not water is really empty.

### Changed

`/etc/lightdm/lightdm.conf:82`
from

    xserver-command=X -nocursor
to

    xserver-command=X -nocursor -s 0 -dpms

`.config/lxsession/LXDE-pi/autostart:3`
comment out

## 8. When trying to log in with an unregistered card, message should be confirmed

 the message what to do to get it registered is shown too short. It should actually stay
there, till someone presses a 'OK' button or so.

## 9. Whenever one of the 'worst milk guys' logs in, he/she should get bad milk warning message...

and what they should do against it. More aggressive form (maybe later): increase the
coffee price for them, e.g. if the received the warning at least 10
times and still didn't buy any milk.

## 10. Maybe we could send automatic eMails to the worst milk guys...

...and those with a negative balance every month. Therefore, we have to collect
their mail addresses first. We should use ira.uka addresses, as that
simplifies sending mails via 'sendmail'.

## 11. Every then-and-when there is a bug in the GUI and it hangs...

...showing no user that is logged in, but showing a log-out button that does not do
anything. Normally, restarting the application solves the problem, but
for restarting you need to know the Admin password. We should add a 'GUI
restart button' to the GUI for these cases.

## 12. The Snoopy comic with the football is already displayed since 100 years. Something is wrong with the update there.

### Q: Is this still the case?
maybe api changed
no new data, but old still there

## 13. The 3D-printed case should be finished and used

### TODO: split 3d model with blender
  
## 4. offline mode

device should work independtently

### Q: what's the server side code?

buffering

## 14. Is there actually a proper backup of the server-side data-base? It

maybe store it on other disk


should be tested to be functional. If there is none, then it should be
created.

seems to be working


## 15. Rinsing is detected as hot water and the user is charged. It should not charge the user.

### Q: When can this happen?

After waking up,
currently just an estimated number of cleaning
could sleep be detected by sensor input? no logging appeared to take place.

## 16. Android app

## TODO

- pull comics regularly
- synchronize orders if failed
- remember when user does not refill water
- after detect sleep, what happens if not rinsing, but ordering water
- cheat detection, if coffee ground within certain threashold after order
- longer timeout for got user

## Questions

## Model

16.47mm - 6.21mm

## Challenges

- running the right version of pyqt
- installing new packages for python, because of deprecetad version
- dealing with unexpected signal glitches from coffeemachine, had to measure average deltas
- rfid reader would stop working without any apparent reason

## Icons Credit
https://www.flaticon.com/free-icon/ink-cartridge_2012071
https://www.flaticon.com/free-icon/moon_865779

coffee screen chair door

# Libraries

- gpiozero
- pigpio
- pymysql
- transitions
- mfrc522 



- lock after complete and ok timer start
- buzzer, certain change stop function
- screensaver
- water alert
- check transitions into coffee_ground with other thesis
- coffee ground triggered out of nothing

water flow stop, 5 seconds, then start again


wrong token:
- dee46
- d22f9

Water flow signal

        ___      ___
  ______| |______| |_____
  35-38ms  5-6ms

water flow signal water flowing, measured in microsecond ticks pigpio
high ~66.5ms, low ~11.5ms

water flow signal coffee flowing, measured in microsecond ticks pigpio
high ~40ms, low ~7ms

20.02.20
Idee für IoT: Erklären, warum dieses Gerät nicht wirklich den anforderungen an IoT entspricht. Es benutzt zwar IoT enabler wie NFC..., aber letztendlich ist es nicht stark vernetzt. Auch hohe verfügbarkeit. Pervasive, not limited
IoT elements, like rfid tags attached to the cups. Had support for an android application, which was removed.

28.02.20 TODe
Implementation of limitations
Debugging the RFID reader
+Describe what's new in the GUI
+Say that support for the app was dropped
Describe exact problems with former case
user feedback countdown for coffee

Der größte Punkt wo ich mir noch nicht ganz sicher bin ist, wie ich die Problemanalyse bzw. die "bugs" von der vorherigen Arbeit einbaue. Aktuell ist es ja eher ne Auflistung von Problemen, mit den Lösungen separat an anderer stelle. Aber vielleicht wäre es schöner, die Probleme und dann direkt dazu im Vergleich die Lösung zu präsentieren.
Dann wäre aber eventuell der Architektur-Teil der aktuellen Implementierung aufgesplittet.

26.03.2020
grinder signal:
normally high,
trigger valid when low for > than 0.5 seconds, typically ~1s
ringing effect?
debounce
stable
