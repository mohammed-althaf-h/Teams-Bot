from discord_webhooks import DiscordWebhooks

#Put your discord webhook url here.

webhook_url = ''


def send_msg(class_name,status,start_time,end_time):

    WEBHOOK_URL = webhook_url 

    mah = DiscordWebhooks(WEBHOOK_URL)
    # Attaches a footer
    mah.set_footer(text='✍ Mohammed Althaf H ✌')

    if(status=="joined"):

      mah.set_content(title='Class Joined Succesfully',
                          description="Here's your report with :heart:")

      # Appends a field
      mah.add_field(name='Class', value=class_name)
      mah.add_field(name='Status', value=status)
      
      mah.add_field(name='Joined at', value=start_time)
      mah.add_field(name='Leaving at', value=end_time)

    elif(status=="left"):
      mah.set_content(title='Class left Succesfully',
                          description="Here's your report with :heart:")

      # Appends a field
      mah.add_field(name='Class', value=class_name)
      mah.add_field(name='Status', value=status)
      
      mah.add_field(name='Joined at', value=start_time)
      mah.add_field(name='Left at', value=end_time)


    elif(status=="noclass"):
      mah.set_content(title='Seems like no class today',
                          description="No join button found! Assuming no class.")

      # Appends a field
      mah.add_field(name='Class', value=class_name)
      mah.add_field(name='Status', value=status)
      
      mah.add_field(name='Expected Join time', value=status)
      mah.add_field(name='Expected Leave time', value=end_time)

    mah.send()

    print("Sent message to discord")
