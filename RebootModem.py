import selenium
from selenium import webdriver
ie = webdriver.Ie()
ie.get('http://192.168.1.1')
ie.find_element_by_id('txt_Username').send_keys("CMCCAdmin")
ie.find_element_by_id('txt_Password').send_keys("aDm8H%MdA")
ie.find_element_by_id('btnSubmit').click()
ie.get('http://192.168.1.1/html/ssmp/devmanage/cmccdevicereset.asp')
ie.find_element_by_id('Restart_button').click()
ie.switch_to.alert.accept()
