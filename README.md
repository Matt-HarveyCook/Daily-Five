# Daily-Five
## An application for distributing personalised headlines to users via email.

![image](https://github.com/Matt-HarveyCook/Daily-Five/assets/136710826/3d457842-b796-456f-9938-e4172855fe28)

This project was producing during my first year of university while working in a team of 6. We worked on it together, however my primary role was on the backend and managing access to the different APIs.
More information surrounding the process of working as a team can be found in the pdf within the repo.

### Project Objectives:
1. Distribute news to users on a daily basis through email
2. Allow users to modify the news that they are sent to reflect their interests
3. Source reliable news stories which allow users to remain up to date in a quick daily update

### My Personal Role Within the Team:
* Interfacing with NewsAPI which is an API for collating links to news articles. I performed pull requests from this REST API and used the corresponding JSON response to form lists of URLs which could then be accessed.

* Once I had collected the URLs, I had to retreieve the web page content based on the classes of different elements. To achieve this I had to use the DOM model to inspect the tags of parent elements.

* After all the content from the pages had been collected it had to be distributed to users in the form of an email which I formatted using HTML, this allowed a template to be used with the content filled in.

* Finally the emails must be delivered to the end user, I decided to manage user emails through the use of the Mail Chimp API as it allowed for easy and free access.

### Home Page:
![image](https://github.com/Matt-HarveyCook/Daily-Five/assets/136710826/142907cd-61d4-41a7-a777-f45d141879ff)


### Registation:
![image](https://github.com/Matt-HarveyCook/Daily-Five/assets/136710826/deda400f-ddb5-4b57-942e-cb9e17236231)


### Main Page:
![image](https://github.com/Matt-HarveyCook/Daily-Five/assets/136710826/b2e6c4a5-0642-4211-affe-2e9f0a419aa8)


### System Structure:
![image](https://github.com/Matt-HarveyCook/Daily-Five/assets/136710826/79e543f5-07c5-47ae-ae24-107bb8c617c4)

