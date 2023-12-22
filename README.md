# Bebe-Bot
Computer Vision + Raspberry Pi + Cats

This is Bebe, a standard issue cat: 

#Insert image of Bebe here

Bebe lives in my flat, where she mostly just eats and sleeps. To capture these unique phenomena I set up a **Raspberry Pi (4) with a PiCamera (v3)** with **Tensorflow Image Detection** to automatically detect Bebe and take a picture when she moves into the frame. Then using [*pedroslopez*'s **whatsapp.js**](https://wwebjs.dev/) service, this image is then sent via Whatsapp to our flat group chat, where my hard work and genius is immediately ignored in favor of my flatmates' inanites: 


#Insert image of whatsapp bebebot

Finally, I 3D printed a fancy casing for Bebebot, and _voilia!_ Bebe-Bot is born: 

#Insert image of Bebe-Bot

References: This project borrows and expands on [work by Evan Juras](https://github.com/EdjeElectronics/TensorFlow-Object-Detection-on-the-Raspberry-Pi/tree/master), and uses existing services like [whatsapp-web.js](https://wwebjs.dev/), tensorflow, etc. The 3D printed Casing was an [open source model downloaded off of Thingiverse](https://www.thingiverse.com/thing:3914319) by SageTechTeacher. As you can see, I am not very original. 


By following these steps, you'll be even less original, but you'll have a working Bebe-Bot of your own!

## 0. Requirements: 

1. A Raspberry Pi and Raspberry Pi Camera (I use the Raspberry Pi 4 with a PiCamera V3 but you can easily adjust the code to work with older PiCamera's or even USB cameras. If using an older Raspberry Pi you may want to use tensorflow-lite instead of tensorflow as I do).

2. Access to a 3d printer and roughly 50g of PLA to print the casing.

3. Something interesting to detect (ex: a cat). Note: By changing a single number in this code, you can turn Bebe-Bot into a dog detector, a people detector, a rabbit detector or more! 

## 1. Setup dependencies

### Python, Tensorflow and the Image Recognition Component

It's always a good idea to update your system before undertaking a project

```sudo apt-get upgrade```

We then install tensorflow and its associated dependencies for the image recognition component (if you have an older version of the Pi, it might be prudent to install tensorflow-lite for performance purposes). Run the following commands in the terminal:

```
pip3 install tensorflow
sudo pip3 install pillow lxml jupyter matplotlib cython
sudo apt-get install python-tk
sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get install libxvidcore-dev libx264-dev
sudo apt-get install qt4-dev-tools libatlas-base-dev
sudo pip3 install opencv-python
sudo apt-get install protobuf-compiler
```

As you can see there's quite a few dependencies and with service-side updates you may encounter errors about other dependencies not being met - in which case simply install what's being asked. 

Run ```protoc --version``` to verify the protobuf-compiler (last line above) was successfully installed. You should receive a response of the form ```libprotoc <version-number>```


#### Setting up the Tensorflow model zoo and directory structure

For ease of use, we'll go ahead and clone the entire tensorflow directory just so everything works out of the box. Run the following in your terminal:

```
cd ~
mkdir tensorflow1 && cd tensorflow1
git clone --depth 1 https://github.com/tensorflow/models.git
```

Add the Tensorflow repository to the PYTHONPATH (basically ensuring our system knows where to find the tensorflow component when we run our python script). We'll have to change the .bashrc file for this: 

```sudo nano ~/.bashrc```

This will open up a text editor inside the terminal. Move to the last line and add: 

```export PYTHONPATH=$PYTHONPATH:/home/pi/tensorflow1/models/research:/home/pi/tensorflow1/models/research/slim```

Save and exit the file (ctrl+X, then Y, then Enter). Close and reopen the terminal for these changes to set. 

Finally, run these commands in the terminal: 

```
cd /home/pi/tensorflow1/models/research
protoc object_detection/protos/*.proto --python_out=.
```

This uses the protobuffer we installed other to compile some .proto files into to .py files (honestly I don't really know what's happening here - just that we need to do it). 

Next, we download the actual model from the [Tensorflow Model Zoo](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md). I am using the SSDlite-MobileNet for Bebe Bot but there are surely better options out there- make sure you choose something your device can run!

```
wget http://download.tensorflow.org/models/object_detection/ssdlite_mobilenet_v2_coco_2018_05_09.tar.gz
tar -xzvf ssdlite_mobilenet_v2_coco_2018_05_09.tar.gz
```

And we're done with the python part of things. 


### Node.js, Whatsapp-web.js and the Whatsapp Client

Whatsapp is finnicky with no easy to use API forcing us to use an unnofficial javascript (🤮) client to send our cat images to our indiffernt flatmates. If your messaging service of choice is Telegram or Discord, you're in luck - their APIs are freely available and _much_ easier to use. Other alternatives (not neccessarily free) are Twilio and the Meta's API for Whatsapp. 

You'll need to install node.js and npm as it does not come with the Pi - refer to instructions [here](https://www.instructables.com/Install-Nodejs-and-Npm-on-Raspberry-Pi/). For convenience I also recommend installing nodemon (```npm install -g nodemon```). 

You'll also need chokidar - a file watcher service that serves as a (janky) bridge between our python and javascript components: 

```npm install chokidar```

Finally, you will need to install whatsapp-web.js: 

```npm i whatsapp-web.js```

Install dependencies for running headless: 

```
sudo apt install -y gconf-service libgbm-dev libasound2 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 ca-certificates fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils wget
```

Refer to the [github](https://github.com/pedroslopez/whatsapp-web.js) and the [website](https://wwebjs.dev/) for more usage info (for the purpose of this project you can just use my script however). 

#### Setting up Whatsapp on the Pi

You need a whatsapp account to actually send the pictures detected. This means you will essentially be logging into whatsapp web, with an account of your choice, on your Pi. 


You can use your personal whatsapp if you prefer. Whatsapp only requires a phone number (not neccessarily an active one) to create an account, so I bought a 1$ sim card and set up a new whatsapp account solely for Bebe Bot: 

#insert image of Bebe Bot whatsapp account

**Note on Privacy:** Whatever Whatsapp account you end up using, you will remain logged in on your Pi in order for the Whatsapp functionality to work. This means that if someone were to access your Pi, they would have access to this Whatsapp account and its chats. Keep your personal information and your Pi protected! 

You will log into Whatsapp on the Pi by scanning a QR code (the same way you log into Whatsapp web on your computer). To display a QR code on your terminal you need to install qrcode-terminal:

```npm i qrcode-terminal```

**The first time you run the .js script, you will be prompted with a qr code to scan (with the account you intend to use to send the images of from). If all goes well you will receive a message "Client Is Ready!". You will not lead to log on in the future ([persistent auth is enabled](https://wwebjs.dev/guide/authentication.html#localauth-strategy)**.


#### Phew! And we're done with the set up!

## 2. The python script


```bebebot-detector.py``` runs out of the box. **Place this file in the Object Detection subfolder of the tensorflow repo you downloaded** - the path to this is: ```cd /home/pi/tensorflow1/models/research/object_detection```.


This file has several parameters that can be tuned (through command line flags or tinkering with the code itself): 

(a) **Visualize** the image detection process using the '-v' flag 

#Insert image of visualization here

(b) **Confidence**: You can use the -c flag (or edit the script) to change how confident (on a scale of 0 to 1) the model has to be before capturing a picture. By default the confidence is 0.55 which has worked fine for me. Increase or decrease depending on results. 


(c) **Frequency**: To avoid spamming, you use the -f flag to set the frequency of messages sent. By default it sends one roughly every 5 hours

(d) **Wait**: Use the -w flag to wait a certain number of frames before capturing an image (to avoid motion blur or just to capture a wider variety of pictures)

(e) **Target**: If you'd like to detect a dog instead of a cat, etc, change the target label to detect for. Refer to [coco_labels.txt](https://gist.github.com/aallan/fbdf008cffd1e08a619ad11a02b74fa8) to find the label you are looking for (Person is 1, Cat is 17, Dog is 18, Car is 3, etc)

(f) **Testing**: Use the -t flag to enter testing mode which changes all the above parameters to something that fetches quicker results. (Detects humans instead of cats, frequency of 20 secs instead of 5 hours, etc)

Play with it!

## 3. The javascript script

```bebebot-messager.js``` runs out of the box as well. **As stated, on the first run you will need to scan the QR code to log into Whatsapp on your Pi**. 

You will need to edit the script to change the following: 

(a) Set the target chat name ```var target_chaht = <insert_chat_name_here>``` where you would like the images sent to. 

(b) Captions - The list ```captions``` contains funny captions to attach to the image that gets sent out. If for some inexplicable reason my humor isn't to your tastes, feel free to add your own captions. 

The code is fairly straightforward, and modifying it to send to additional chats, use something other than whatsapp-web.js should be simple enough. Play with it!

## 4. Putting it all together

In order for Bebebot to work, both the .py script and the .js script need to run together. 

The .py script will detect cats, take a picture and store it in a folder ```Results```. The .js script will watch this folder for changes, and when it finds a new image placed in the folder, it will send it off on whatsapp. 

**Note:** I wrote the code that images are not stored on the Pi itself _other than the very latest captured image_ (this was done for storage, privacy and laziness reasons). You'll have to tweak the code to keep the images for longer if you wish. 

```run_bebebot.sh``` is a bash script that runs both of these scripts for your convenience. **Place this script in your home (~) folder and run it from the terminal using:**

```sh run_bebebot.sh```

In the future you can SSH into your Pi on your laptop or your Android phone (Termux for the win!) and run bebebot with a single command as soon as you log in!

## 5. The 3d print

If you choose to house BebeBot in a worthy suit of armor, download the [model](lhttps://www.thingiverse.com/thing:3914319) and print it on your 3D printer of choice. In order to house my Pi4 and my PiCamera V3 snugly, I scaled down the model in every dimension to 67.32% - which required roughly 50g of PLA and ~3 hours of printing time on the Bambu X1 Carbon. 

The image detection and sending functionalities still works fine without a casing of course, but it won't look as cool. 

## 6. Celebrate!

And we're done! 

Bebe Bot _should_ theoretically run forever by itself the first time you run the script. However, the Whatsapp component is a bit finnicky (I know little to no JavaScript) and the Whatsapp connection seems to fail occasionally when the internet is choppy, and doesn't recover after that. 

If you notice that Bebe Bot has been a bit quiet for a while you can restart it by running the following commands:

```
pkill screen
sh run_bebebot.sh
```

If you wish to inspect each component separately first run 

```screen -d -r```

which should give you an output like: 


#Insert image of screen -d -r

If you see one (or no) lines instead, this means that one (or both, resp.) of the components have failed. 

Otherwise you can open the terminal running the respective script by running 

```screen -d -r <screen-id>..bebebot```

which will take you to the terminal corresponding to that program. You can leave this and return to the original menu with ctrl+A, and then D! 


And that's it! Place your pi+camera somewhere fun and watch as you get live pictures of whatever cat/person you own/stalk! 
