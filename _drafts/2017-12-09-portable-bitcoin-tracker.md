Goal: Developing a small pocket device with a display that shows the current BTC/crypto-of-the-week price in USD/EUR and a chart
Xebia-branded, giveaway
Ideally priced below 10 euros, but it's an iterative process

V1: Raspberry Pi 2 model b with PiFace HAT

* Built at Innovation Day, 8th dec 2017
* Based on web radio player kit
* Uses pifacecad library (python) to operate screen
* Uses simple coindesk api to get current price, updated once per minute (but app checks every 10s)
  * downside: no price history. Didn't check if they offer it
* Is able to work on one of the Xebia branded power banks
  * found them in a magazine, looks like LogiLink Powerbank, 2200 mAh.
* Worked all throughout the demo, with led backlight on. No internet connection though. Wonder how long it lasts. Might be able to do some maths.
* Major power drop when charging, so no charging while using - although it didn't crash, so short term low power might work.
* Should measure power usage. Power bank can deliver 1A, should be enough for this application.
  * [this list](https://www.raspberrypi.org/help/faqs/#powerReqs) indicates power usage for the full sized pis are at 700mA to 2.5A.
  * [this list](http://raspi.tv/2017/how-much-power-does-pi-zero-w-use) shows it's under 500mA for tasks up to viewing / making HD video, with the Zero W staying under 250mA.
 * Some power can be saved by disabling hdmi, underclocking the device, tuning the software, etc.
 * Ideally I'd be able to load a microkernel or something that only does this thing (+ low power stuff)


PARTS LIST:

* Raspberry Pi 2 Model b: €35 (cheapest on google shopping) - €45 (conrad)
* (branded) LogiLink 2000 mAh powerbank - €5,80 (Reichelt) (includes short usb cable)
* PiFace Control & Display 2 - €35 (google shopping) €36.10 (reichelt)
* PiFace compatible case (model: http://www.vesalia.de/e_pifaceenclosure.htm): €12,50 - €15,30
* 4GB micro-SD card - €6,00. The 8GB one is only 60 cents more expensive, might be worth pursuing to enable GUI interface and have a bit of playing room. Would be neat if you could hook it up to a display for a full screen view.
* bit of ethernet cable - negligible
* bit of tape - optional, negligible

Total: €100-110 ish.

## ITERATION 2

 * Use a Raspberry Pi Zero W
  * challenge: setting up wifi
 * Use an OLED or graphical screen (someone mentioned a nokia phone screen?)
  * e-ink €33+: https://www.pi-supply.com/product/papirus-zero-epaper-screen-phat-pi-zero/
  * e-ink €17: https://nl.aliexpress.com/item/250x122-2-13inch-E-Ink-display-HAT-for-Raspberry-Pi-supports-partial-refresh/32809858088.html
  * tiny oled €15 on adafruit: https://www.adafruit.com/product/3527
 * custom 3d printed enclosure (two-tone with xebia logo \o/)

## OTHER THINGS

 * is LoRa plausible to use? For permanent intenret connection at low / no price
 * Custom or small model battery pack that fits in the enclosure

## Iteration 3

 * use a cheaper EPC32 or something
 * probably no cheaper screens
 * idk

## Iteration 4

Custom board. Probably hard to be cheaper than iteration 2 or 3.
