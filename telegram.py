import telepot
token = '2102327904:AAFsSJ8zLe8VOzdAH36nio0qh2VypyEKwbM' # telegram token
receiver_id = 989221812 # https://api.telegram.org/bot<TOKEN>/getUpdates
bot = telepot.Bot(token)
bot.sendMessage(receiver_id, 'hmm1') # send a activation message to telegram receiver id

def send_message(strg):
    bot.sendMessage(receiver_id, strg)
    
#bot.sendPhoto(receiver_id, photo=open('test_img.png', 'rb'))