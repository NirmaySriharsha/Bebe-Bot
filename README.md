# Bebe-Bot
Computer Vision + Raspberry Pi + Cats

This is Bebe, a standard issue cat: 

#Insert image of Bebe here

Bebe lives in my flat, where she mostly just eats and sleeps. To capture these unique phenomena I set up a **Raspberry Pi (4) with a PiCamera (v3)** with **Tensorflow Image Detection** to automatically detect Bebe and take a picture when she moves into the frame. Then using *insert name*'s **whatsapp.js** service, this image is then sent via Whatsapp to our flat group chat, where my hard work and genius gets ignored: 


#Insert image of whatsapp bebebot


Finally, I 3D printed a fancy casing for Bebebot, and _voilia!_ Bebe-Bot is born: 

#Insert image of Bebe-Bot

References: This project borrows and expands on work by Evan Juras, and uses existing packages like whatsapp.js, tensorflow, etc. The 3D printed Casing was an open source model. As you can see, I am not very original. 


By following these steps, you'll be even less original, but you'll have a working Bebebot of your own!

## 0. Requirements: 

1. A Raspberry Pi and Raspberry Pi Camera (I use the Raspberry Pi 4 with a PiCamera V3 but you can easily adjust the code to work with older PiCamera's or even USB cameras. If using an older Raspberry Pi you may want to use tensorflow-lite instead of tensorflow as I do).

2. Access to a 3d printer and roughly 50g of PLA to print the casing.

3. Something interesting to detect (ex: a cat). Note: By changing a single number in this code, you can turn Bebe-Bot into a dog detector, a people detector, a rabbit detector or more! 

## 1. Setup dependencies

You'll need python and node.js on your pi. 

Install tensorflow, protobuf, clone the tensorflow repo, and more. Refer to Evan Juras for this. 

## 2. The python script

## 3. The javascript script

## 4. The bash scripts

## 5. The 3d print models

## 6. Putting it all together
