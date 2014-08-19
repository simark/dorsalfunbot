DorsalFunBot
============

DorsalFunBot *a.k.a.* **WololoPiBot** is actually a not-so-evil bot which controls not just the virtual IRC world at `#dorsal-fun` but also real world activities in DORSAL lab. It helps the lab inhabitants in their day to day chores such as playing and scheduling music, notify mentions on IRC by blinking big-a** 40W lamps, get the day's menu on cafeteria, check if its raining, switch the lab lights on and off, quote the relevant xkcd, so on and so forth..

Oh, and yes, if the hard working grad students are under immense pressure to get results, it can use SCIgen to generate high quality research publications for them :) Boy oh boy! Such a hard working bot it is - and yet, never complains.

### Commands
The bot accepts the following commands on the channel :

`!meteo` : Shows the current weather conditions in Montreal retrieved from Weather Cananda

`!light [toggle | status]` : Used to control main lights in the lab or to see if somebody left them on in the evening

`!crazy` : Set craziness level of the channel [1-10]. Shown as [====----] in 'topic'

`!translate` : Translate last statement from French to English or vice versa, or from anything to English by default

`!music` : Play music from the connected HDD

`!publish Suchakra Sharma, Simon Marchi, Nikola Tesla` : Publish a SCIgen based randomly generated CS related paper for the authors and return the link 

`!xkcd` : Return the latest xkcd comic title and link

`!xkcd teach your kids linux` : Return the 3 most relevant xkcd comics related to that query

`!menu` : Return today's menu in the cafeteria. Yum yum!

`!amihot` : Show the current CPU temperature of the Pi

`!help` : Help on how to use the specific commands

Some other tasks of the bot include, getting title and duration of youtube videos, daily lunch reminder, silently strip audio from youtube videos and play it. Overall, the bot is like the faithful dog you take on an evening stroll - except that its with you the whole day. *Such happiness, much wow!*

### What Next
* Interface temperature sensor to get temperature conditions of lab
* Use webcam to detect if someone is in the other lab or not
* Make a list of people voting to go to a specific poutine place
