# Star Tracking program

![program interface](https://github.com/PetarBabic/Star-Tracking-program/blob/7ac6d23d80b91c5c4f0385d8dda91f2010262af4/Images/GUI.png)

My high school graduation project from 2018 tackles one of the major astrophotography problems: star-tracking. When taking long exposures of the night sky, the stars leave a trail behind them because the Earth is constantly rotating, this is solved using a tracking mount and a small guiding camera that tracks the stars to finely correct the movement. I wrote a Python program that tracks the stars and minimizes the star elongation in long exposures photography. Everything was verified to be working correctly using a ground based telescope system:
- HEQ5 mount
- ZWO-ASI 120mm-mini guide camera
- QHY163mm cooled cmos maing imaging camera
- Explore Scientific ED80 telescope

![setup]()

The program consists of a GUI where the user selects the tracking star and has the option to start and end the guiding. The results are shown below and as can be seen the stars stay  round:


| Image | Description | Exposure time (s) |
| ----------- | ----------- | ----------- |
| ![](https://github.com/PetarBabic/Star-Tracking-program/blob/7ac6d23d80b91c5c4f0385d8dda91f2010262af4/Images/America%20Large.jpeg) | America Nebula | 300 |
| ![](https://github.com/PetarBabic/Star-Tracking-program/blob/7ac6d23d80b91c5c4f0385d8dda91f2010262af4/Images/Elephant%20Large.jpeg) | Elephant's trunk Nebula | 300 |
| ![](https://github.com/PetarBabic/Star-Tracking-program/blob/7ac6d23d80b91c5c4f0385d8dda91f2010262af4/Images/Veil%202%20Large.jpeg) | HOO Veil Nebula | Ha: 300, OIII: 300 |
