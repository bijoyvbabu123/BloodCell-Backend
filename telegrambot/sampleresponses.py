# ========= response of /start ============
"""    
    {
    "update_id":734997090,
    "message":{
        "message_id":51,
        "from":{
            "id":996202131,
            "is_bot":false,
            "first_name":"Bijoy",
            "username":"bijoyvbabu123",
            "language_code":"en"
        },
        "chat":{
            "id":996202131,
            "first_name":"Bijoy",
            "username":"bijoyvbabu123",
            "type":"private"
        },
        "date":1686207037,
        "text":"/start YnZiMTIzbWlzY0BnbWFpbC5jb20=",
        "entities":[
            {
                "offset":0,
                "length":6,
                "type":"bot_command"
            }
        ]
    }
    }
better to go with entities-type-bot_command for proper /start command
""" 


# =========== inline keyboard response ===========
"""
{
   "update_id":734997099,
   "callback_query":{
      "id":"4278655576057498272",
      "from":{
         "id":996202131,
         "is_bot":false,
         "first_name":"Bijoy",
         "username":"bijoyvbabu123",
         "language_code":"en"
      },
      "message":{
         "message_id":60,
         "from":{
            "id":6097692400,
            "is_bot":true,
            "first_name":"BloodLink",
            "username":"bloodlink_bot"
         },
         "chat":{
            "id":996202131,
            "first_name":"Bijoy",
            "username":"bijoyvbabu123",
            "type":"private"
         },
         "date":1686214500,
         "text":"Hello! Please choose an option:",
         "reply_markup":{
            "inline_keyboard":[
               [
                  {
                     "text":"Button 1",
                     "callback_data":"button1_bijoy"
                  },
                  {
                     "text":"Button 2",
                     "callback_data":"button2_bijoy"
                  }
               ]
            ]
         }
      },
      "chat_instance":"-2291384178539442901",
      "data":"button2_bijoy"
   }
}
better to add encoded callbackdata to get proper response
"""
