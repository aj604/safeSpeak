const botSettings = require("./botsettings.json");
const Discord = require("discord.js");

const fs = require("fs");

const bot = new Discord.Client({

});

function generateOutputFile(channel, member) {
    // use IDs instead of username cause some people have stupid emojis in their name
    const fileName = `./recordings/${channel.id}-${member.id}-${Date.now()}.pcm`;
    return fs.createWriteStream(fileName);
}

bot.on('message', async (message) => {
    let messageArr = message.split(" ");
    let pre = messageArr[0];
    let command = messageArr[1];
    let channelName = messageArr[2];
    
    if ((pre === bot.user.username) && (command === "start")) {
        const voiceChannel = message.guild.channels.find("name", channelName.join(" "));

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
        }).catch(console.log);
    }
    if ((pre === bot.user.username) && (command === "leave")) {
        let voiceChannel = message.guild.channels.find("name", channelName.join(" "));
        voiceChannel.leave();
    }
})

bot.on("ready", async () => {
    console.log("bot is ready, user is: " + bot.user.username);
    try {
        let link = await bot.generateInvite(["ADMINISTRATOR"]);
        console.log(link);
    } catch(error) {
        console.log(error.stack);
    }
});

bot.login(botSettings.token);