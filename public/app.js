const webdriver = require('selenium-webdriver');
const chrome = require('selenium-webdriver/chrome');
const firefox = require('selenium-webdriver/firefox');

let driver = new webdriver.Builder()
    .forBrowser('firefox')
    .withCapabilities(webdriver.Capabilities.chrome())
    .setChromeOptions(/* ... */)
    .setFirefoxOptions(/* ... */)
    .build();



var driver = new webdriver.Builder().
       withCapabilities(webdriver.Capabilities.chrome()).
       build();
     
driver.get('http://www.lambdatest.com');


driver.quit();