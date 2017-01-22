# Alexa Fitness
**Personal Trainer for Amazon Alexa.**

Built during PennApps 2017 Spring in approximately four hours (check the Git commits if you don't believe me :P).

### Video Demonstration!
[![https://youtu.be/d93TALLqmsU](https://i.imgur.com/q28wLsc.jpg)](https://youtu.be/d93TALLqmsU)

### Instructions

1. Clone this repo and `cd` to into it
2. Run `python fitness_skill.py`
3. In another Terminal window, run `ngrok http 5000`
  - If you do not have ngrok installed, you can [download it here](https://ngrok.com/download)
4. Create a new Amazon Alexa Skill in the [Amazon Developer Console](https://developer.amazon.com/edw/home.html#/skills/list)
  - AWS account required
5. When filling out the Interaction Model information, copy the Intent Schema and Sample Utterances from the `speechAssets` directory
6. Under Configuration, check HTTPS and paste the https link obtained from the output of the ngrok command
7. Under SSL Certificate, check "My development endpoint is a sub-domain of a domain that has a wildcard certificate from a certificate authority."
8. Wait a few seconds and then say "Alexa, start personal trainer."


### Project Members
Palmer Paul (palmerpa@seas.upenn.edu)
