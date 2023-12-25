// Bebe-Bot Whatsapp Messager
// Author: Nirmay Sriharsha Singaram
//Simple JavaScript Process that will log into whatsapp*, monitor a folder for changes and send images to a chat when changes are detected. 
//*WE USE LOCAL AUTH TO STORE WHATSAPP SESSION INFO. THIS IS A PRIVACY RISK AND YOU SHOULD USE/MODIFY AT YOUR OWN DISCRETION

//This script uses Whatsapp-Web.js to hook into whatsapp via the whatsapp web interface. 

//Setting up
const { Client, LocalAuth, MessageMedia } = require('whatsapp-web.js');
//FIRST time set up will require qr code login. We will store session info so that this will be a one time thing only. 
const qrcode = require('qrcode-terminal');
//Chokidar watches the Results folder for changes when the python script deposits images into them
const chokidar = require('chokidar');
//Path to folder being watched
const path = "./Results/output.png";
const chat_name = 'insert_chat_name_here';
const watcher = chokidar.watch(path, {
    persistent: true,
    awaitWriteFinish: true, //Waits till python is done writing the new image file.  
})

//Just an array of cute captions for our images
var captions = new Array(
    "Beep Boop",
    "Meow", 
    "Bebe Detected", 
    "🐱", 
    "🐈",
    "🐾",
    " /|、\n(˚ˎ。7\n|、˜〵\nじしˍ,)ノ", 
    "ᓚᘏᗢ",
    "•⩊•",
    "Bebebot Activated",
    "Who dat",
    "≽^•⩊•^≼",
    "I SeeSee a BeBe",
    "Cat Burglar Alert!",
);
var caption_ = captions[0];

const client = new Client({
    puppeteer: {
        headless: true, 
        args: ['--no-sandbox'],
    },
    //Local Auth to not have to log in (via qr code) to whatsapp every time. 
    authStrategy: new LocalAuth({
        clientId: "BEBEBOT_ID",
    })
});

//QR Code fetching and generation for first time log in via whatsapp linking
client.on('qr', (qr) => {
    qrcode.generate(qr, {small:true});
});

client.on('ready', () => {
    console.log("Client is ready!");
    //checks for the python script to change the directory
    watcher.on('change', async (path) => {
        //Get whatsapp chats by chat name.
        client.getChats().then((chats) => {
            destination_chat = chats.find((chat) => chat.name === chat_name);
            const catpic = MessageMedia.fromFilePath(path);
            caption_ = captions[Math.floor(Math.random() * captions.length)];
            destination_chat.sendMessage(catpic, {caption: caption_});
        });
    });
});

client.initialize();
