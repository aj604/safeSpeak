# safeVoice
RU Hacks 2018 repo

Created By: Nafeh Shoaib, Avery Jones, and Devin Owens

A framework designed, using a Deep Learning Model with Recurrent Neural Networks (RNN) and implemented as a Discord Bot, to monitor voice communication in online communities to identify sexism and harassment. Training data was compiled as a simple yes or no audio dataset converted to spectograph images to demonstrate the nueral network's ability to differentiate between audio patterns and identify words and understand meaning.

## To install:
1. Change to the discord bot directory
```shell
cd discordbot && cd node
```

2. Change discord bot app id in botsettings.json to your own from discordapp.com/developers/applications

3. Check if NodeJS is up to date:
```shell
node -v
```

4. Update Node to latest version:
```shell
sudo npm cache clean -f
sudo npm install -g n
```

5. Install and run discord bot
```shell
npm install
node bot
```

6. Copy-paste the printed invite link to your browser and add the bot to your Discord server.

7. Push to talk to see the magic!
