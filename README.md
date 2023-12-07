# astrotools

Repository containing a few regularly-used tools. 

Free to use but not guaranteed. 

---
## Install
### Clone the repo

```
git clone https://github.com/GregS1t/astrotools.git
```

### Dependancies

| [numpy](https://numpy.org/) | [scipy](https://www.scipy.org/) | [matplotlib](https://matplotlib.org/) | [pandas](https://pandas.pydata.org/) | [astropy](https://www.astropy.org/) 
| :-----: | :-----: | :----------: | :------: | :--------: |  

### Paths

Don't forget to add `$ASTROCODE` to your `$PATH` so you can use it to call python codes from scripts.

Next, you can add another path to the scripts so you can run them from anywhere. It's up to you.

Example : 

```
# Path to ASTROTOOLS
export ASTROCODE=[PATH/TO]/astrotools/src
export ASTROSCRIPTS=[PATH/TO]/scripts

# Add path to python scripts
export PATH=$PATH:$ASTROSCRIPTS
```

Obviously, you change `[PATH/TO]` to the correct path for you.

---
## pfits GUI
### Purpose
`pfits`  is a program for plotting a FITS file with very basic options for zooming anywhere in the main image.

### How to use is
You can play with sliders to adjust contrast. 

Right-click to center in the zoom window and use the mouse wheel to zoom in. That's all there is to it! 

### GUI

![pfits screen shot](./img/pfits_screenshot_1.png)


