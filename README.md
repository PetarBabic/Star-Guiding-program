# Star Guiding program
My high school graduation project from 2018 tackles one of the major astrophotography problems: star-tracking. When taking long exposures of the night sky, the stars leave a trail behind them because the Earth is constantly rotating, this is solved using a tracking mount and a small guiding camera that tracks the stars to finely correct the movement. I wrote a Python program that tracks the stars and minimizes the star elongation in long exposure photography. I also included [the thesis](https://github.com/PetarBabic/Star-Tracking-program/blob/f044b4efa4391ce307fae42533f43abbaafb36a9/Zavrsni.pdf) I wrote, but unfortunately, it's only available in Croatian.

## GUI
The program consists of a simple GUI where the user selects the tracking star and has the option to start and end the guiding, additionally it also necessary camera controls: exposure and gain.
![program interface](https://github.com/PetarBabic/Star-Tracking-program/blob/7ac6d23d80b91c5c4f0385d8dda91f2010262af4/Images/GUI.png)

## Setup
Everything was verified to be working correctly using a ground based telescope system:

| Imaging setup | Description |
| ----------- | ----------- |
| ![](https://github.com/PetarBabic/Star-Tracking-program/blob/feabd08bb900bf6d24f560926a969eba1fb9d739/Images/setup%20Medium.jpeg) | <ul><li>HEQ5 mount </li><li>ZWO-ASI 120mm-mini guide camera </li> <li>QHY163mm cooled cmos maing imaging camera</li> <li>Explore Scientific ED80 telescope</li> </ul> |


## Results
The results are shown below and as can be seen the stars stay round while taking long exposure pictures (5min) of stars and nebula:

| Image | Description | Exposure time (s) |
| ----------- | ----------- | ----------- |
| ![](https://github.com/PetarBabic/Star-Tracking-program/blob/7ac6d23d80b91c5c4f0385d8dda91f2010262af4/Images/America%20Large.jpeg) | America Nebula | 300 |
| ![](https://github.com/PetarBabic/Star-Tracking-program/blob/7ac6d23d80b91c5c4f0385d8dda91f2010262af4/Images/Elephant%20Large.jpeg) | Elephant's trunk Nebula | 300 |
| ![](https://github.com/PetarBabic/Star-Tracking-program/blob/7ac6d23d80b91c5c4f0385d8dda91f2010262af4/Images/Veil%202%20Large.jpeg) | HOO Veil Nebula | Ha: 300, OIII: 300 |
