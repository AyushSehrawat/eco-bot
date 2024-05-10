> [!IMPORTANT]  
> This project was originally created in 2021 and has recently been updated by a contributor. However, I don’t plan to continue improving this bot, so I’m archiving it.


# EcoBot
An Economy Bot made using discord.py and mongoDB

-------------------------

## Usage

### **Install the required modules**

```
pip install -r requirements.txt
```

### **Create a file `.env` with these contents**

```
TOKEN=your_bot_token
mongo=your_mongo_link
```

### **Edit `market.json` for items/products**

**Format**

`[display_name, price, item-name-without-spaces]`

```
{
    "IoT" : [
        ["Smart Watch", 100, "smart-watch"]
    ],
    "Food" : [
        ["Water", 5, "water"]
    ],
    "Cars" : [
        ["Car", 10000, "car"]
    ]
}
```

For MongoDB, create
```
Database -> eco
            Collection -> money, bag
```

-------------------------

## Setting Up MongoDB

1. Visit [MongoDB](https://www.mongodb.com) and sign up.

2. Verify your email address.

3. Navigate to project 0, then select "New Project".

   ![New project](https://i.imgur.com/yPXOrcR.png)

5. Name your project (anything you like), add any members if needed, then hit "create".

   ![New database](https://i.imgur.com/BeA2t9P.png)

6. Click on "Build Database", choose the Free option (ideal for beginners), and stick with the default settings, except if you want to customize the cluster name.

7. Keep the default options selected, and input your username/password (make sure to remember them).

8. In the IP access list, allow access from everywhere by entering `0.0.0.0/0`.

9. Complete the setup and clear any prompts.

10. It might take a while to create your database. Once it's done, head to "Connect" and select "Connect your application". Choose Python and version 3.6 or later. Copy the provided link and paste it into your `data.json` file. Remember to edit the password (remove `< >` too).

11. Go to "Browse Collections" and click "Add My Own Data". Enter your desired database and collection names. Later, to connect to this database, you can simply use `foo = cluster["database"]["collection"]` in your code, like `ecomoney = cluster["eco"]["money"]`.

That's all you need to set up your MongoDB database.


---

## Contributors

![Contributors](https://contrib.rocks/image?repo=AyushSehrawat/eco-bot)
