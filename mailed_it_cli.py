from mailed_it import (login_with_creds, read_csv, read_template_file,
                       send_mail, generate_messages_from_template, clear_screen)
from time import sleep


BANNER = '''
                                                                                
                             .---.                   _______                    
 __  __   ___            .--.|   |      __.....__    \  ___ `'.   .--.          
|  |/  `.'   `.          |__||   |  .-''         '.   ' |--.\  \  |__|          
|   .-.  .-.   '         .--.|   | /     .-''"'-.  `. | |    \  ' .--.     .|   
|  |  |  |  |  |    __   |  ||   |/     /________\   \| |     |  '|  |   .' |_  
|  |  |  |  |  | .:--.'. |  ||   ||                  || |     |  ||  | .'     | 
|  |  |  |  |  |/ |   \ ||  ||   |\    .-------------'| |     ' .'|  |'--.  .-' 
|  |  |  |  |  |`" __ | ||  ||   | \    '-.____...---.| |___.' /' |  |   |  |   
|__|  |__|  |__| .'.''| ||__||   |  `.             .'/_______.'/  |__|   |  |   
                / /   | |_   '---'    `''-...... -'  \_______|/          |  '.' 
                \ \._,\ '/                                               |   /  
                 `--'  `"                                                `'-'   
Version 0.0.1 @r1jf4s @h4d1 @sh4d4
'''


print(BANNER)
sleep(1)

input('Press any key to authenticate the user.')
creds = login_with_creds()
input('Authentication Completed, press any key to continue.')
clear_screen()
if creds is None:
    print('ERROR: Authentication Error.')
print('+--------------------------------+')
print('|          MailedIT              |')
print('+--------------------------------+')
csv_file_name = input('| Enter CSV file name: ')
data_list = read_csv(csv_file_name)
email_list = [d['email'] for d in data_list]
template_file_name = input('| Enter template file name: ')
email_subject = input('| Enter email subject: ')
_, template_str = read_template_file(template_file_name)

messages = generate_messages_from_template(template_str, data_list)
for to, content in zip(email_list, messages):
    print('| Sending email to:', to, '✅')
    send_mail(creds, to, email_subject, content)
print('+--------------------------------+')
