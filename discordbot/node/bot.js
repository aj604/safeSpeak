const botSettings = require("./botsettings.json");

// Discord bot
const Discord = require("discord.js");

// Writing to Files
const fs = require("fs");
var FileWriter = require('wav').FileWriter;

var PythonShell = require('python-shell');

// Calling Python script
var spawn = require("child_process").spawn;

// Discord bot instance
const bot = new Discord.Client({

});

// general Text Channel
var textChannel = bot.channels.find("name", "general");

var currentFileName = "";

// save audio as wav file
function generateOutputFile(channel, member) {
    // use IDs instead of username cause some people have stupid emojis in their name
    //const fileName = `../../newNet/spoken-language-identification/liveResults/${channel.id}-${member.id}-${Date.now()}.wav`;
    const fileName = `../../newNet/spoken-language-identification/liveResults/predictFile.wav`;
    currentFileName = fileName;
    var outputFileStream = new FileWriter(fileName);
    return outputFileStream;
    //return fs.createWriteStream(fileName);
}

// run python script
async function runPythonScript(path) {
    var options = {
        args:
        [
            path// audioFilePath
        ]
    }

    PythonShell.run('../../botTestFile.py', options, function (err, data) {
        if (err) {
            console.log(err);
        }
        console.log(data.toString());
    });
}

bot.on('message', async (message) => {
    let messageArr = message.split(" ");
    let pre = messageArr[0];
    let command = messageArr[1];
    let channelName = messageArr[2];
    
    //if ((pre === bot.user.username) && (command === "start")) {
        /* const voiceChannel = message.guild.channels.find("name", channelName.join(" "));

        if (!voiceChannel || voiceChannel.type !== 'voice') {
            return message.reply(`I couldn't find the channel ${channelName}. Can you spell?`);
        }
        voiceChannel.join().then(bot => {
            message.reply('ready!');
            const receiver = bot.createReceiver();

            bot.on('speaking', (user, speaking) => {
                if (speaking) {
                    message.channel.sendMessage(`I'm listening to ${user}`);

                    const audioStream = receiver.createPCMStream(user);

                    const outputStream = generateOutputFile(voiceChannel, user);

                    audioStream.pipe(outputStream);
                    outputStream.on("data", console.log);

                    audioStream.on('end', () => {
                        message.channel.sendMessage(`I'm no longer listening to ${user}`);
                    });
                }
            });
        }).catch(console.log); */
    //}
    /* //if ((pre === bot.user.username) && (command === "leave")) {
        let voiceChannel = message.guild.channels.find("name", channelName.join(" "));
        voiceChannel.leave();
    } */
});



// bot start up code
bot.on("ready", async () => {
    console.log("bot is ready, user is: " + bot.user.username);
    try {
        let link = await bot.generateInvite(["ADMINISTRATOR"]);
        console.log(link);
    } catch(error) {
        console.log(error.stack);
    }

    const channelName = "General";
    const voiceChannel = bot.channels.find("name", channelName);

    if (!voiceChannel || voiceChannel.type !== 'voice') {
        //return message.reply(`I couldn't find the channel ${channelName}. Can you spell?`);
    }
    voiceChannel.join().then(bot => {
        //message.reply('ready!');
        const receiver = bot.createReceiver();

        bot.on('speaking', (user, speaking) => {
            if (speaking) {
                //message.channel.sendMessage(`I'm listening to ${user}`);

                const audioStream = receiver.createPCMStream(user);

                const outputStream = generateOutputFile(voiceChannel, user);

                audioStream.pipe(outputStream);
                outputStream.on("data", console.log);

                audioStream.on('end', () => {
                    
                    runPythonScript(currentFileName);
                    //textChannel.sendMessage(result);
                    //message.channel.sendMessage(`I'm no longer listening to ${user}`);
                });
            }
        });
    }).catch(console.log);
});

bot.login(botSettings.token);