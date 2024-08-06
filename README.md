<p align="center">
  <a href="https://github.com/Kolyn090/mhfu-db/blob/main/assets/MHFU_MainTitle.PNG">
    <img alt="Main title of game Monster Hunter Freedom Unite, taken in my PPSSPP." src="./assets/MHFU_MainTitle.PNG" width="400" />
  </a>
</p>

<h1 align="center">
  Monster Hunter Freedom Unite Database
</h1>

Welcome to this dedicated repo for a 15 years-old game! If you have played the MH series before, 
I shall remind you that this is not about MHGU, MHW, MHR, or MH Wild... It's MHFU! 
(or MHP2G in Japan) 

<h3 align="center">
Current valid number of lines in DB: 201395
</h3>

### ❓What is this
This is a database repo for game Monster Hunter Freedom Unite by CAPCOM. My current plan is to 
store data in JSON format. I try to make sure that the data are organized in a way that it is 
easy to read and understand (at least by someone who has played the game before). Each JSON file
will store an array of objects, and each object has the *same* properties, so a JSON file is really 
a table. 

### ❓What is 'id'
The 'id' field is manufactured by me (not existing in the actual game) mainly for a better debugging purpose, 
and every object has some kind of 'id' field. The 'id' will only be unique in the JSON file storing 
it so it is insufficient to use 'id' alone to identify a particular object in this database. In some cases, 
you might want to use two JSON files together, a great example would be weapon, which I imagine could be
very focusing for someone who just started looking at it. Don't worry. I will guide you through it!

Firstly, this is where our example located:
```
Root
  - Weapon
    - Hammer
      - hammer-create.json
      - hammer-upgrade.json
      - hammer-tree.json
```
Secondly, the above JSON files (tables) have the belowing structures (unimportant properties omitted)
```
--- hammer-create.json ---
{
  "id": number,
}

--- hammer-upgrade.json ---
{
  "id": number,
}

--- hammer-tree.json ---
{
  "upgrade-id": number REFERENCES hammer-upgrade(id),
  "upgrade-from" : [
    {
      "id": number REFERENCES a weapon's id
      "craft-type": "create"/"upgrade"
    }
  ]
}
```
(hammer-create.json & hammer-upgrade.json)
Here, the hammer-create.json stores all hammers obtained through direct creating (from the blacksmith,
no upgrade). The hammer-upgrade.json stores all hammers obtained through upgrading (you pay some money
and materials to upgrade). Some weapons can be obtained through both creating and upgrading. 

(hammer-tree.json)
I refer this upgrade as a tree because a weapon can be continously upgraded by following a certain
route (like leading to a leaf through the tree root and branches, hope this helped a little if you are
not a CS major). That's the idea behind hammer-tree.json. Also, you see that 'REFERENCES' keyword? It
means that this property called 'upgrade-id' is referencing the id from hammer-upgrade, which means
that all hammers existing in hammer-tree must be also existing in hammer-upgrade. Moreover, in this
case, they have a one-to-one correspondence to each other.

(upgrade-from)
This property in hammer-tree is really just the weapons before upgrade. The weapon can be upgraded
to the weapon with the 'upgrade-id' if it is under 'upgrade-from'. Notice that we have a 'REFERENCES' 
keyword behind 'id' here. This means that the id is referencing a weapon's id. In this case, it 
could be a hammer🔨 or a hunting horn🎺 because a hammer or a hunting horn can be upgraded to a 
hammer in this game (weird?) Lastly, we have the 'craft-type', this property stores a flag, used to
indicate whether this weapon came from the create or upgrade side. ❗️This is important because as 
discussed before, the 'id' is not unique acorss JSON files. We rely on this flag to know where this
weapon came from and help us to locate it.

### 🔅Contributing
Feel free to send an issue if you spot any typo/mistake. Of course, you are free to fork this repo 
and contribute as well! ❗️Please note that your contribution must be from a crediable source and 
it's not violating any copyright.

### ❓Why am I creating a database for MHFU
First of all, I have played this particular MH version for a long time - probably the longest 
time I have spent on a game. It all started on the iOS version ($15 USD but definitely worth it).
I had continued to play this game at my leisure since then! Until the game was taken down from
App Store. It was sad to see it go! However, recently, with PPSSPP being introduced to iOS, I
was able to revive this game on my phone! It really brightened my mood and I decided to do something
I have been thinking for a long time - to create a DB for this game.

Secondly, it's hard to find accurate information about this game because it's old (and thus less
people care) and there isn't a complete decrypted game file available online (to my knowledge). 
Most information available online were manually gathered by the community, and data obtained in this 
way might contain errors if not done carefully. Thus we need someone willing to verify and maintain
all those data! That's why this repo will be for providing complete, accurate data about MHFU. 

### 🧶Attributions
To gather everything from scratch is extremely time-consuming. That's why I decided to borrow some
help from online communities. Yes, I know it is not perfect but I will manually verify them. Also,
I cite all sources I used in the 
[Attributions.txt](https://github.com/Kolyn090/mhfu-db/blob/main/Attributions.txt) file. Here, I
also want to say Thank you🤗 to those selfless authors for making them available!

