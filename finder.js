const {Builder, By, Key, util}  = require('selenium-webdriver');
const fs = require('fs')

async function getTable(){
    let driver = new Builder()
  .forBrowser('chrome')
  .build();
    await driver.get("https://unitedopt.com/Home/blogdetail/top-companies-offering-opt-jobs-to-international-students-in-2021");  
    const table = await driver.findElement(By.className("mrd-blog-table")).getText();
    const arr = table.split('\n')
    for(let i = 0; i < arr.length; i++){
        arr[i] = arr[i].split(" ")
    }
    driver.quit();
    fs.writeFile("text.json", JSON.stringify(arr) , function(err) {
        if (err) {
            console.log(err);
        }
    });
}

getTable();


