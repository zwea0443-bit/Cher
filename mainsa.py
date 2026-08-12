import requests
import telebot, time, os
from telebot import types
import json

# Your bot token
token = '7599807676:AAGKSDlxdy6hrmcG_L-1rVv0YMFSejyAh5o'
bot = telebot.TeleBot(token, parse_mode="HTML")

# Simple gate function (replacing missing import)
def Tele(card):
    # This is a placeholder - replace with actual gate logic
    # For demo, returning success
    return "succeeded"

@bot.message_handler(commands=["start"])
def start(message):
    if not str(message.chat.id) == '5916610832':
        bot.reply_to(message, "You cannot use the bot to contact developers to purchase a bot subscription @strawhatchannel96")
        return
    bot.reply_to(message, "Send the file now")

@bot.message_handler(content_types=["document"])
def main(message):
    if not str(message.chat.id) == '5916610832':  # Fixed: was 7954343626
        bot.reply_to(message, "You cannot use the bot to contact developers to purchase a bot subscription @strawhatchannel96")
        return
    
    dd = 0
    live = 0
    ch = 0
    ccn = 0
    cvv = 0
    lowfund = 0
    
    # Send initial message
    ko = bot.reply_to(message, "CHECKING....⌛").message_id
    
    # Download file
    file_info = bot.get_file(message.document.file_id)
    ee = bot.download_file(file_info.file_path)
    
    with open("combo.txt", "wb") as w:
        w.write(ee)
    
    try:
        with open("combo.txt", 'r', encoding='utf-8') as file:
            lino = file.readlines()
            total = len(lino)
            
            for cc in lino:
                cc = cc.strip()  # Clean the card
                
                # Check stop file
                if os.path.exists("stop.stop"):
                    bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text='STOP ✅\nBOT BY ➜ @strawhatchannel96')
                    os.remove('stop.stop')
                    return
                
                # Get BIN info
                try:
                    data = requests.get(f'https://bins.antipublic.cc/bins/{cc[:6]}', timeout=5).json()
                    brand = data.get('brand', 'Unknown')
                    card_type = data.get('type', 'Unknown')
                    country = data.get('country_name', 'Unknown')
                    country_flag = data.get('country_flag', 'Unknown')
                    bank = data.get('bank', 'Unknown')
                except:
                    brand = 'Unknown'
                    card_type = 'Unknown'
                    country = 'Unknown'
                    country_flag = 'Unknown'
                    bank = 'Unknown'
                
                start_time = time.time()
                
                # Check card
                try:
                    last = str(Tele(cc))
                except Exception as e:
                    print(f"Error: {e}")
                    last = 'missing payment form'
                
                # Create inline keyboard
                mes = types.InlineKeyboardMarkup(row_width=1)
                cm1 = types.InlineKeyboardButton(f"• {cc} •", callback_data='u8')
                status = types.InlineKeyboardButton(f"• STATUS ➜ {last[:20]} •", callback_data='u8')  # Truncate long status
                cm3 = types.InlineKeyboardButton(f"• CHARGED ➜ [ {ch} ] •", callback_data='x')
                cm4 = types.InlineKeyboardButton(f"• CCN ➜ [ {ccn} ] •", callback_data='x')
                cm5 = types.InlineKeyboardButton(f"• CVV ➜ [ {cvv} ] •", callback_data='x')
                cm6 = types.InlineKeyboardButton(f"• LOW FUNDS ➜ [ {lowfund} ] •", callback_data='x')
                cm7 = types.InlineKeyboardButton(f"• DECLINED ➜ [ {dd} ] •", callback_data='x')
                cm8 = types.InlineKeyboardButton(f"• TOTAL ➜ [ {total} ] •", callback_data='x')
                stop = types.InlineKeyboardButton(f"[ STOP ]", callback_data='stop')
                mes.add(cm1, status, cm3, cm4, cm5, cm6, cm7, cm8, stop)
                
                end_time = time.time()
                execution_time = end_time - start_time
                
                # Update status message
                bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text='Wait For Processing\nby ➜ @strawhatchannel96', reply_markup=mes)
                
                msg = f''' 
𝐂𝐀𝐑𝐃: <code>{cc}</code>
𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: <code>Hit $1.00 🔥</code>

𝐁𝐢𝐧 𝐈𝐧𝐟𝐨: <code>{cc[:6]}-{card_type} - {brand}</code>
𝐁𝐚𝐧𝐤: <code>{bank}</code>
𝐂𝐨𝐮𝐧𝐭𝐫𝐲: <code>{country} - {country_flag}</code>

𝐓𝐢𝐦𝐞: <code>1{"{:.1f}".format(execution_time)} second</code> 
𝐁𝐨𝐭 𝐀𝐛𝐨𝐮𝐭: @strawhatchannel96'''
                
                print(f"Response: {last}")
                
                # Process responses
                if 'succeeded' in last.lower():
                    ch += 1
                    bot.reply_to(message, msg)
                    
                elif 'security code is incorrect' in last.lower() or 'security code is invalid' in last.lower():
                    ccn += 1
                    
                elif 'insufficient funds' in last.lower():
                    msg = f'''			
𝐂𝐀𝐑𝐃: <code>{cc}</code>
𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: <code>Insufficient funds 🔥</code>

𝐁𝐢𝐧 𝐈𝐧𝐟𝐨: <code>{cc[:6]}-{card_type} - {brand}</code>
𝐁𝐚𝐧𝐤: <code>{bank}</code>
𝐂𝐨𝐮𝐧𝐭𝐫𝐲: <code>{country} - {country_flag}</code>

𝐓𝐢𝐦𝐞: <code>1{"{:.1f}".format(execution_time)} second</code> 
𝐁𝐨𝐭 𝐀𝐛𝐨𝐮𝐭: @strawhatchannel96'''
                    lowfund += 1
                    bot.reply_to(message, msg)
                    
                elif 'additional action' in last.lower():
                    msg = f'''			
𝐂𝐀𝐑𝐃: <code>{cc}</code>
𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: <code>3ds ✅</code>

𝐁𝐢𝐧 𝐈𝐧𝐟𝐨: <code>{cc[:6]}-{card_type} - {brand}</code>
𝐁𝐚𝐧𝐤: <code>{bank}</code>
𝐂𝐨𝐮𝐧𝐭𝐫𝐲: <code>{country} - {country_flag}</code>

𝐓𝐢𝐦𝐞: <code>1{"{:.1f}".format(execution_time)} second</code> 
𝐁𝐨𝐭 𝐀𝐛𝐨𝐮𝐭: @strawhatchannel96'''
                    cvv += 1
                    bot.reply_to(message, msg)
                    
                else:
                    dd += 1
                
                time.sleep(1)  # Small delay to avoid rate limiting
                
    except Exception as e:
        print(f"Main error: {e}")
        bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=f'ERROR ❌\n{e}')
    
    bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text='CHECKED ✅\nBOT BY ➜ @strawhatchannel96')

@bot.callback_query_handler(func=lambda call: call.data == 'stop')
def menu_callback(call):
    with open("stop.stop", "w") as file:
        pass
    bot.answer_callback_query(call.id, "Stopping...")

# Start the bot
print("Bot is running...")
bot.polling(none_stop=True)						bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text='STOP ✅\nBOT BY ➜ @strawhatchannel96')
						os.remove('stop.stop')
						return
				try: data = requests.get('https://bins.antipublic.cc/bins/'+cc[:6]).json()
				except: pass
				try:
					brand = data['brand']
				except:
					brand = 'Unknown'
				try:
					card_type = data['type']
				except:
					card_type = 'Unknown'
				try:
					country = data['country_name']
					country_flag = data['country_flag']
				except:
					country = 'Unknown'
					country_flag = 'Unknown'
				try:
					bank = data['bank']
				except:
					bank = 'Unknown'
				
				start_time = time.time()
				try:
					last = str(Tele(cc))
				except Exception as e:
					print(e)
					last = 'missing payment form'
				mes = types.InlineKeyboardMarkup(row_width=1)
				cm1 = types.InlineKeyboardButton(f"• {cc} •", callback_data='u8')
				status = types.InlineKeyboardButton(f"• STATUS ➜ {last} •", callback_data='u8')
				cm3 = types.InlineKeyboardButton(f"• CHARGED ➜ [ {ch} ] •", callback_data='x')
				cm4 = types.InlineKeyboardButton(f"• CCN ➜ [ {ccn} ] •", callback_data='x')
				cm5 = types.InlineKeyboardButton(f"• CVV ➜ [ {cvv} ] •", callback_data='x')
				cm6 = types.InlineKeyboardButton(f"• LOW FUNDS ➜ [ {lowfund} ] •", callback_data='x')
				cm7 = types.InlineKeyboardButton(f"• DECLINED ➜ [ {dd} ] •", callback_data='x')
				cm8 = types.InlineKeyboardButton(f"• TOTAL ➜ [ {total} ] •", callback_data='x')
				stop=types.InlineKeyboardButton(f"[ STOP ]", callback_data='stop')
				mes.add(cm1,status, cm3, cm4, cm5, cm6, cm7, cm8, stop)
				end_time = time.time()
				execution_time = end_time - start_time
				bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text='''Wait For Processing   
by ➜ @strawhatchannel96 ''', reply_markup=mes)
				msg = f''' 
𝐂𝐀𝐑𝐃: <code>{cc}</code>
𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: <code>Hit $1.00 🔥</code>

𝐁𝐢𝐧 𝐈𝐧𝐟𝐨: <code>{cc[:6]}-{card_type} - {brand}</code>
𝐁𝐚𝐧𝐤: <code>{bank}</code>
𝐂𝐨𝐮𝐧𝐭𝐫𝐲: <code>{country} - {country_flag}</code>

𝐓𝐢𝐦𝐞: <code>1{"{:.1f}".format(execution_time)} second</code> 
𝐁𝐨𝐭 𝐀𝐛𝐨𝐮𝐭: @strawhatchannel96'''
				
				print(last)
				if 'succeeded' in last:
					ch += 1
					bot.reply_to(message, msg)
					
				elif 'Your card does not support this type of purchase' in last:
				    cvv += 1
				    				    
				elif 'security code is incorrect' in last or 'security code is invalid' in last:
					ccn += 1
					
				elif 'insufficient funds' in last:
					msg = f'''			
𝐂𝐀𝐑𝐃: <code>{cc}</code>
𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: <code>Insufficient funds 🔥</code>

𝐁𝐢𝐧 𝐈𝐧𝐟𝐨: <code>{cc[:6]}-{card_type} - {brand}</code>
𝐁𝐚𝐧𝐤: <code>{bank}</code>
𝐂𝐨𝐮𝐧𝐭𝐫𝐲: <code>{country} - {country_flag}</code>

𝐓𝐢𝐦𝐞: <code>1{"{:.1f}".format(execution_time)} second</code> 
𝐁𝐨𝐭 𝐀𝐛𝐨𝐮𝐭: @strawhatchannel96'''
					lowfund += 1
					bot.reply_to(message, msg)
					
				elif 'The payment needs additional action before completion!' in last:
					msg = f'''			
𝐂𝐀𝐑𝐃: <code>{cc}</code>
𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: <code>3ds ✅</code>

𝐁𝐢𝐧 𝐈𝐧𝐟𝐨: <code>{cc[:6]}-{card_type} - {brand}</code>
𝐁𝐚𝐧𝐤: <code>{bank}</code>
𝐂𝐨𝐮𝐧𝐭𝐫𝐲: <code>{country} - {country_flag}</code>

𝐓𝐢𝐦𝐞: <code>1{"{:.1f}".format(execution_time)} second</code> 
𝐁𝐨𝐭 𝐀𝐛𝐨𝐮𝐭: @strawhatchannel96'''
					cvv += 1
					bot.reply_to(message, msg)
				    	
				else:
					dd += 1
					time.sleep(5)
	except Exception as e:
		print(e)
	bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text='CHECKED ✅\nBOT BY ➜ @strawhatchannel96')
@bot.callback_query_handler(func=lambda call: call.data == 'stop')
def menu_callback(call):
	with open("stop.stop", "w") as file:
		pass
bot.polling()
