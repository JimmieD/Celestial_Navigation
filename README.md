# Celestial Navigation Using Python

## What is This and What's It's Purpose?

This is simple celestial navigation using python.  Navigation relies heavily on two primary methods of obtaining fixes: Visual and GPS.  Along with Dead Reckoning, Running Fixes, and Radar Fixes, Celestial navigation is simply another tool for obtaining one's position. This becomes especially useful when there are no visual or radar navigation aids and GPS is unavailable (perhaps dead batteries, GPS denied environments, or some sort of emergency).  

Though it takes practice, using a sextant to obtain a sight is straight forward.  What makes celestial navigation rather difficult is the necessity of using the Nautical Almanac and Sight Reduction Tables - a process that quickly becomes slow and cumbersome even with a working knowledge on how to use the tables.  But using these tables is less prone to error than hand calculating the spherical trigonometry required for solving the celestial triangle.  But why not calculate the spherical trig, and solve the celestial triangle directly without having to manually resort to the tables?  That's what this script attempts to do.  It attempts to simplify and speed up the process by solving the celestial triangle and cutting out the need for manual table look-ups.

This script relies mostly on doing the spherical trig (though there are a couple of included tables from Pub 249 for calculating the sun's position that will need to be updated in 2036) for solving the celestial triangle.  It is a standalone script that doesn't rely on anything other than the power/battery of the machine running the script and the ability of one to either obtain an azimuth and elevation or obtain an azimuth and the ratio of the height of an object to the length of it's shadow.  

## How Does This Work?

This is based in part on a similar concept to that of A'Hearn and Rossano[1].

[1] Navigation: Journal of the Institute of Navigation.  "Two Body Fixes by Calculator," M. F. A'Hearn and G. S. Rossano, Vol 24, No. 1, Spring 1977.

## What is the Current Status of This Project?

2/4/19: There are two methods that can be used to calculate your celestial fix.  You can use a method based on that of Eratosthenes where you measure the ratio of the height of an object to the length of it's shadow.  Alternatively, you can obtain a sight using a sextant.  The script is only working with the sun at the present time.

## Limitations

- Only works with the sun at the present time
- There is a margin of error, especially with longitude and when taking a fix at on or close to 5th minute of every 10 minutes.  This is due to the sun tables rounding to the nearest 10th minute.  Latitude errors seem to consistently be between 2-5 nm.
- Sextant sights will only work when shooting the center of the sun - not the limbs. 
- Does not include sight corrections for altitude, refraction, or sextant error.  

## Where Might This Project be Heading?

- Add corrections for limb sights. (next on my to do)
- "Clean up" the code
- Would like to do the same for the moon.
- Would like to add navigational stars.   
- Would like to improve accuracy.  (will probably always be an ongoing effort)
- Add corrections for a moving observer
- Add altitude corrections.
- Add corrections for refraction and sextant error.

## Installation

Simply download celnav.py to your directory.

## Running/Executing

Execute celnav.py and follow the prompts.

## What tools Do You Need?

You will need either some object of arbitrary length (and enough sun to cast a shadow) or a sextant (with sun filters).  Additionally you will need a magnetic compass and a way to obtain an azimuth to the sun without burning your eyes out (eg, make use of the shadow cast by the sun).  

## Feedback

Feedback, comments and suggestions are appreciated.  Also note that this is a side project of mine so future updates and added features are dependent on my free time.

## DISCLAIMER

Don't use this for navigation.  It's jsut a python and math project.
