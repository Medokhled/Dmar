# TelegramBotV1

<a id="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![Telegram][telegram-shield]][telegram-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://t.me/zlaxtert">
    <img src="img/darkxcode.PNG" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Telegram Bot V1 PHP</h3>

  <p align="center">
    Telegram Bot V1 PHP for check card with gateway!
    <br />
    <a href="https://t.me/DarkxcodeBot">View Demo</a>
    &middot;
    <a href="https://t.me/zlaxtert">Report Bug</a>
    &middot;
    <a href="https://t.me/zlaxtert">Request Feature</a>
  </p>
</div>


## Features

Features:
* Check card with gate stripe
* Check card with gate Braintree
* Check card with gate VBV Check
* Check BIN


<!-- GETTING STARTED -->


### Installation

_Here's how to install the bot._

* Hosting on Server 
* Download the Files from Here
* Upload it to your Server and Extract it
* Set Webhook to index.php in root folder of bot

WEBHOOK URL
   ```sh
   https://api.telegram.org/bot{my_bot_token}/setWebhook?url={url_to_send_updates_to}
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Commands
   ```sh
   /info -> for check information 
   /bin -> for check BIN Card 
   /stripe -> for check card gate Stripe 
   /braintree for check card gate Braintree 
   /vbv -> for check card gate VBV Check 
   /sk -> for check SK key 
   /help -> for help information
   ```

**Format:** `card|month|year|cvv` → `4532123456789012|12|2025|123`

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- OUTPUT -->
## Output

[![Product Name Screen Shot][product-screenshot]](https://t.me/DarkxcodeBot)

This is the result if the code is successfully deployed.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTACT -->
## Contact

* Telegram - [@zlaxtert](https://t.me/zlaxtert)
* Github - [@zlaxtertdev](https://github.com/zlaxtertdev)
* Stackoverflow - [@zlaxtert](https://stackoverflow.com/users/31033623)

<p align="right">(<a href="#readme-top">back to top</a>)</p>




<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/zlaxtertdev/TelegramBotV1.svg?style=for-the-badge
[contributors-url]: https://github.com/zlaxtertdev/TelegramBotV1/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/zlaxtertdev/TelegramBotV1.svg?style=for-the-badge
[forks-url]: https://github.com/zlaxtertdev/TelegramBotV1/network/members
[stars-shield]: https://img.shields.io/github/stars/zlaxtertdev/TelegramBotV1.svg?style=for-the-badge
[stars-url]: https://github.com/zlaxtertdev/TelegramBotV1/stargazers
[issues-shield]: https://img.shields.io/github/issues/zlaxtertdev/TelegramBotV1.svg?style=for-the-badge
[issues-url]: https://github.com/zlaxtertdev/TelegramBotV1/issues
[telegram-shield]: https://img.shields.io/badge/telegram-blue.svg?style=for-the-badge&logo=telegram&colorB=555
[telegram-url]: https://t.me/zlaxtert
[product-screenshot]: img/ress.png
