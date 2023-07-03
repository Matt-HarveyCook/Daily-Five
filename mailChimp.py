# pip install mailchimp-marketing
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
import time

class mailChimp ():
  def __init__(self):

    self.client = MailchimpMarketing.Client()
    self.client.set_config({
      "api_key": "64c80e39d973c00a65c2f458d7e7e0cf-us11",
      "server": "us11"
    })

    # The unique value which is assigned to the daily five mail chimp account 
    self.list_id = "c1dbd4836b"

  # adds a user to the email list
  # category is used to determine the tag placed on the user
  # select a single value from the list of article categories
  # ensure the first character of category is capitalised
  def addUser (self, email, category):
    if (category=="General" or category=="Technology" or category=="Environment" or category=="Politics" or category=="Sports"): 
      # Assigns the characteristics for the user in the mailchimp database
      member_info = {
          "email_address":str(email),
          "status": "subscribed",
          "tags":[str(category)]
        }

      try:
        self.client.lists.add_list_member(self.list_id, member_info)
        print("user has been added")
      except ApiClientError as error:
        print("An exception occurred: {}".format(error.text))
    else:
      print("Invalid Category")

  # Mail chimp uses campaigns which represent unique mail content to be sent
  # A campaign must be made for every category email we send
  # The campaign is also considered used once the email is sent
  # This means that one must be generated for every email we send 
  def createCampaign (self, category):
    campaignID = 0

    # Determines the contents for the email based on the category
    match category:
      case "General":
        segmentID = 9273481 
        settings = {
          "from_name":"Daily Five",
          "reply_to":"dailyfive@gmail.com",
          "subject_line":"Your Daily General Headlines!",
          "title":"General Campaign"
        }
      case "Politics":
        segmentID = 9273477
        settings = {
          "from_name":"Daily Five",
          "reply_to":"dailyfive@gmail.com",
          "subject_line":"Your Daily Politics Headlines!",
          "title":"Politics Campaign"
        }
      case "Environment":
        segmentID = 9273489 
        settings = {
          "from_name":"Daily Five",
          "reply_to":"dailyfive@gmail.com",
          "subject_line":"Your Daily Environment Headlines!",
          "title":"Environment Campaign"
        }
      
      case "Technology":
        segmentID = 9273485 
        settings = {
          "from_name":"Daily Five",
          "reply_to":"dailyfive@gmail.com",
          "subject_line":"Your Daily Technology Headlines!",
          "title":"Technology Campaign"
        }
      
      case "Sports":
        segmentID =9273493 
        settings = {
          "from_name":"Daily Five",
          "reply_to":"dailyfive@gmail.com",
          "subject_line":"Your Daily Sports Headlines!",
          "title":"Sports Campaign"
        }

    # Only segments can be used when creating a new campaign
    # This means that segments are created which only include users based on tag 
    # These segments are referred to by segment id 
    recipients = {
      "list_id":self.list_id,
      "segment_opts":{"saved_segment_id" : segmentID}
    }

    response = self.client.campaigns.create({"type": "regular", "recipients":recipients, "settings":settings})
    campaignID = response["id"]
    return campaignID
    

  # this uploads the contents of [category].html to the mail chimp site
  # This allows the contents of the emails to change when new articles are accessed
  # Once the contents have been uploaded, it sends the email for the given category
  # The campaign is then deleted once sent to prevent duplicate campaigns
  def setEmailContent (self, category):
    htmlString = ""
    campaignID = ""

    if (category=="General" or category=="Technology" or category=="Environment" or category=="Politics" or category=="Sports"):
      match category:
        case "General":
            with open('general.html', 'r') as f:
              htmlString = f.read()
            campaignID = self.createCampaign(category)

        case "Technology":
            with open('technology.html', 'r') as f:
              htmlString = f.read()
            campaignID = self.createCampaign(category)
        
        case "Environment":
            with open('environment.html', 'r') as f:
              htmlString = f.read()
            campaignID = self.createCampaign(category)

        case "Politics":
            with open('politics.html', 'r') as f:
              htmlString = f.read()
            campaignID = self.createCampaign(category)

        case "Sports":
            with open('sports.html', 'r') as f:
              htmlString = f.read()
            campaignID = self.createCampaign(category)

      # This block updates, sends and deletes the campaign
      # The sleep timer is required to allow the campaign to fully send before deleting
      # Currently sleeps for 10 seconds but that can be changed
      try:
        self.client.campaigns.set_content(campaignID, {"html":htmlString})
        self.client.campaigns.send(campaignID) 
        time.sleep(10)
        self.client.campaigns.remove(campaignID)
        print("email content has been set and sent")
      except ApiClientError as error:
        print("An exception occurred: {}".format(error.text))
    else:
      print("Invalid Category")

  # This inserts the content from the final articles array (2d array) into the html 
  # The code is then stored in a file called: [category].html 
  # This file is then used for the email of that category
  # The CSS is supposed to be inline to ensure accurate rendering / recommended by mail chimp
  def createHTML (self, final_articles, category):
    category = category.lower() # This ensures that all files are the same format
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <title>My Website</title>
      </head>
      <body style="margin: 0;">
        <main style="background-color:white;">
          <div style="width: 50%; margin: auto; "> 
            <div style="background-color:white;">
              <p style="text-align: center; margin: 0;">
            <img src="https://mcusercontent.com/787e6a76ea684391a37d1ce60/images/bb4fbaf8-fdcb-8b01-bc9e-47822f895913.png" alt="" style="width: 50%; padding: 3%;"> 
              </p> 
                      
            </div>        

            <div style="background-color: #FF9853;">
              <p style="text-align: center; margin: 0; font-size: 2vw; font-family: Open Sans, sans-serif; padding: 1%; color: #2963B3;">Good Morning!</p> 
              <p style="text-align: center; margin: 0; font-size: 1.7vw;  font-family:  Open Sans, sans-serif;padding: 1%;color: #2963B3;">Your {category} Headlines:</p> 
            </div>

            <div style="background-color:white;">
              <p style="font-size: 0.85vw;padding-right: 20%; padding-left: 5%; padding-bottom: 5%; margin: 0; padding-top: 5%; font-family:  Open Sans, sans-serif; color: #2963B3;">
                <b>1.{final_articles[0].title} </b>
                <br>
                {final_articles[0].content}
              </p>
              
              <p style="font-size: 0.85vw;padding-left: 20%; text-align: right; padding-right: 5%; padding-bottom: 5%; margin: 0; font-family:  Open Sans, sans-serif;color: #2963B3;">
                <b>2.{final_articles[1].title} </b>
                <br>
                {final_articles[1].content}
              </p>

              <p style="font-size: 0.85vw;padding-right: 20%; padding-left: 5%; padding-bottom: 5%; margin: 0;font-family:  Open Sans, sans-serif; color: #2963B3;">
                <b>3. {final_articles[2].title}</b>
                <br>
                {final_articles[2].content}
              </p>
              
              <p style="font-size: 0.85vw;padding-left: 20%; text-align: right; padding-right: 5%; padding-bottom: 5%; margin: 0; font-family:  Open Sans, sans-serif; color: #2963B3;">
                <b>4. {final_articles[3].title}</b>
                <br>
                {final_articles[3].content}
              </p>

              <p style="font-size: 0.85vw;padding-right: 20%; padding-left: 5%; padding-bottom: 5%; margin: 0;font-family:  Open Sans, sans-serif; color: #2963B3;">
                <b>5. {final_articles[4].title}</b>
                <br>
                {final_articles[4].content}
              </p>

            </div>

          </div>

        </main>
      </body>
    </html>

      """
      
    # Overwrites the file to change to the new html with correct content
    f = open(f"{category}.html", "w")
    f.write(html)
    f.close()


  # !!! The only function which needs to be called to send the email for a certain category !!!
  # Just calls the required functions in the right order
  # Updates the html files to match the parameter content and then sends to all users in that category
  def publishEmail (self, final_articles, category):
    self.createHTML(final_articles, category)
    self.setEmailContent(category)

# EXAMPLES OF METHOD USAGE:
# mc = mailChimp()
# mc.addUser("jemcook@ntlworld.com", "Politics")
# mc.publishEmail(content, "Politics")

