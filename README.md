# EcoBot
A Economy Bot made using py-cord (Currently - Rewriting from scratch)

-------------------------

## Usage

Install the required modules

```
pip install -r requirements.txt
```

Create a file `data.json` with these contents

```
{
    "name" : "Bot Name",
    "token" : "Bot Token",
    "mongo" : "Mongo Url"
}
```

Edit `market.json` for items/products

-------------------------

## Setup of mongodb

- Go to https://www.mongodb.com

- From there register/Try Free ( Fill up the details or register via google )

- Verify Email

- [Here for img](https://i.imgur.com/yPXOrcR.png)

Click on project 0 , then click on new project

- Name your project ( anything ), then add members ( if any ). After that click create.

- [Here for img](https://i.imgur.com/BeA2t9P.png)

Click on build database, select Free (for starters), let the default settings be there, but you can chnage the last field of cluster name.

- Then let the default things be selected and enter your username/password ( remember them ).

- In the IP access list enter `0.0.0.0/0` (allow from everywhere).

- Finish and clear

- After that it will take some time to create. Once its finished go to Connect and select Connect your application. Select python and 3.6 or later. Then copy the link and paste in data.json. Edit the password (remove < > too). And done

- Now go to Browse Collections and click `Add My Own Data` . Enter whatever db and collection name you want to use.
Later to connect to that db you can do `foo = cluster["database"]["collection"]` in the code. Like `ecomoney = cluster["eco"]["money"]`.

- That's it for db setup.