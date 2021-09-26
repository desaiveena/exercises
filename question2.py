from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from mailosaur import MailosaurClient
from mailosaur.models import SearchCriteria
import string
import random

tb_url = "http://jt-dev.azurewebsites.net/#/SignUp"

lang_xpath = """//*[@id='language']/div[1]/span/span[2]"""
eng_lang_xpath = """//*[@id="ui-select-choices-row-1-0"]/a/div"""
dutch_lang_xpath = """//*[@id="ui-select-choices-row-1-1"]/a/div"""
t_n_c_xpath = """//*[@id='content']/div/div[3]/div/section/div[1]/form/fieldset/div[4]/label/span"""
submit_xpath = """//*[@id='content']/div/div[3]/div/section/div[1]/form/fieldset/div[5]"""

name_id = "name"
org_id = "orgName"
email_id = "singUpEmail"
email_suffix = "@m2jf6kzc.mailosaur.net"


name_value = "ABC"
org_value = "ABCDE"

api_key = "DKct7yPAYwYNw7ne"
server_id = "m2jf6kzc"
server_domain = "m2jf6kzc.mailosaur.net"

def wait_for_mail(email_value, timeout = 20):

    # Available in the API tab of a server

    mailosaur = MailosaurClient(api_key)

    criteria = SearchCriteria()
    criteria.sent_to = email_value

    email = mailosaur.messages.get(server_id, criteria, timeout*1000) #timeout in ms

    print("Subject: " + email.subject)
    print("Text: " + email.text.body)


def gen_rand_id():
    letters = string.ascii_lowercase
    return(''.join(random.choice(letters) for i in range(8)))


def main():
    # using Chrome
    driver = webdriver.Chrome()
    driver.get(tb_url)
    print(driver.title)
    print(driver.current_url)

    driver.find_element_by_xpath(lang_xpath).click()
    assert(driver.find_element_by_xpath(eng_lang_xpath).text == "English")
    assert (driver.find_element_by_xpath(dutch_lang_xpath).text == "Dutch")
    driver.find_element_by_xpath(eng_lang_xpath).click()


    name_element=driver.find_element_by_id(name_id)
    assert (name_element.is_displayed())
    assert (name_element.is_enabled())

    orgName_element=driver.find_element_by_id(org_id)
    assert (orgName_element.is_displayed())
    assert (orgName_element.is_enabled())

    signup_element=driver.find_element_by_id(email_id)
    assert (signup_element.is_displayed())
    assert (signup_element.is_enabled() )

    name_element.send_keys(name_value)
    orgName_element.send_keys(org_value)

    email_value = gen_rand_id() + email_suffix
    signup_element.send_keys(email_value)

    driver.find_element_by_xpath(t_n_c_xpath).click()

    driver.find_element_by_xpath(submit_xpath).click()

    wait_for_mail(email_value, 20)
    driver.close()

if __name__ == "__main__":
    main()
