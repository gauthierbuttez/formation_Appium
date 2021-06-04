#coding:utf-8
import html
import os
import pdb
import sys
from datetime import time
from datetime import datetime
import time
import sqlite3
from appium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import mymodules
import random
import logging
import unidecode



# ================================================================================================================
#=========================================== PREPARING LOG =======================================================
logger = logging.getLogger('Instagram_bot')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(process)d:%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s')
file_handler = logging.FileHandler(mymodules.LoadFile('log.log'))
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
logger.addHandler(file_handler)
logger.addHandler(console_handler)




# ==========================================================================================================
# =================================        FUNCTION TO GET THE EMAIL      =================================
# ==========================================================================================================
def get_email_from_mail_client_field_to(p_driver,p_udid,lock):
    try:
        logger.info(f"{p_udid}|||==================== FUNCTION GET EMAIL OF PROFILE ============================")
        logger.info(f"{p_udid}|||Bot will sleep to be sure the email client is loaded..........")
        time.sleep(random.uniform(16.5, 18.3))
        p_email = ''
        p_app = ''
        sqliteConnection = sqlite3.connect(os.path.join(os.path.dirname(sys.argv[0]),'db.db'))  # we prepare db
        p_cursor1 = sqliteConnection.cursor()
        p_app_email_client = p_cursor1.execute("SELECT app_email_client FROM smartphones WHERE udid=?",(p_udid,)).fetchone()
        print(f"p_app_email_client : {p_app_email_client}")
        sqliteConnection.commit()
        if p_app_email_client :
            logger.info(f"{p_udid}|||str(p_app_email_client[0]) = {str(p_app_email_client[0])}")
            logger.info(f"{p_udid}|||p_app_email_client[0] = {p_app_email_client[0]}")
            logger.info(f"{p_udid}|||We found the app email client of smartphone {p_udid} => {p_app_email_client[0]}.")
            if p_app_email_client[0] == 'gmail':
                email_fields_to= p_driver.find_elements_by_id("com.google.android.gm:id/to")
            elif p_app_email_client[0] == 'aquamail':
                email_fields_to = p_driver.find_elements_by_id("org.kman.AquaMail:id/new_message_to")
            elif p_app_email_client[0] == 'bluemail':
                email_fields_to = p_driver.find_elements_by_id("me.bluemail.mail:id/RecipientEditTextView_to")
            elif p_app_email_client[0] == 'email':
                email_fields_to = p_driver.find_elements_by_id("com.android.email:id/to")
            elif p_app_email_client[0] == 'appple':
                email_fields_to = p_driver.find_elements_by_id("com.appple.app.email:id/to")
            elif p_app_email_client[0] == 'easilydo':
                email_fields_to = p_driver.find_elements_by_id("com.easilydo.mail:id/contacts_to_field")
            elif p_app_email_client[0] == 'yandex':
                email_fields_to = p_driver.find_elements_by_id("com.emailfantect.mailbox.allmail:id/rlt_top")
            elif p_app_email_client[0] == 'easymail':
                email_fields_to = p_driver.find_elements_by_id("com.mail.emailapp.easymail2018:id/searchView")
            elif p_app_email_client[0] == 'tohsoft':
                email_fields_to = p_driver.find_elements_by_id("com.mail.hotmail.outlook.email:id/searchView")
            elif p_app_email_client[0] == 'hotmail':
                email_fields_to = p_driver.find_elements_by_id("park.hotm.email.app:id/edit_text_to")
            elif p_app_email_client[0] == 'outlook':
                email_fields_to = p_driver.find_elements_by_id("park.outlook.sign.in.client:id/edit_text_to")
            elif p_app_email_client[0] == 'emailfantext':
                email_fields_to = p_driver.find_elements_by_id("com.emailfantect.mailbox.allmail:id/searchView")
            elif p_app_email_client[0] == 'gmx':
                email_fields_to = p_driver.find_elements_by_id("com.emailfantect.mailbox.allmail:id/searchView")
            elif p_app_email_client[0] == 'orange':
                email_fields_to = p_driver.find_elements_by_id("com.orange.mail.fr:id/autocomplete_to")
            elif p_app_email_client[0] == 'mailwise':
                email_fields_to = p_driver.find_elements_by_id("com.syntomo.email:id/to")
            elif p_app_email_client[0] == 'mymail':
                email_fields_to = p_driver.find_elements_by_id("com.my.mail:id/edit_text_to")
            elif p_app_email_client[0] == 'outlook2':
                email_fields_to = p_driver.find_elements_by_id("com.microsoft.office.outlook:id/compose_to_field")
            elif p_app_email_client[0] == 'yahoomail':
                email_fields_to = p_driver.find_elements_by_id("ymail_toLozengeContainer")
            else:
                logger.critical(f"{p_udid}|||We couldn't get the 'mail to' field! :-(")
                logger.critical(
                    "Please contact support@phonebot.co, send the log.log file and the name of your email client (i.e.: outlook, gmail, yandex,...???) installed on your smartphone! :-(")
            try:
                p_app=p_app_email_client[0]
                p_email=email_fields_to[0].text
            except Exception as ex:
                logger.critical(f"{p_udid}|||{ex} --> ERROR because we couldn't get the 'mail to' field! :-(")


        else:
            logger.info(f"{p_udid}|||We didn't find the app email client of smartphone {p_udid}. Let's identify it as the email client supposed to have been opened and it is displayed right now on the screen of smartphone.")

            try:
                gmail_fields_to = p_driver.find_element_by_id("com.google.android.gm:id/to")
                logger.info(f"{p_udid}||| PhoneBot found gmail_fields_to.")
            except:
                try:
                    aquamail_fields_to = p_driver.find_element_by_id("org.kman.AquaMail:id/new_message_to")
                    logger.info(f"{p_udid}||| PhoneBot found aquamail_fields_to.")
                except:
                    try:
                        bluemail_fields_to = p_driver.find_element_by_id("me.bluemail.mail:id/RecipientEditTextView_to")
                        logger.info(f"{p_udid}||| PhoneBot found bluemail_fields_to.")

                    except:
                        try:
                            email_fields_to = p_driver.find_element_by_id("com.android.email:id/to")
                            logger.info(f"{p_udid}||| PhoneBot found email_fields_to.")

                        except:
                            try:

                                appple_fields_to = p_driver.find_element_by_id("com.appple.app.email:id/to")
                                logger.info(f"{p_udid}||| PhoneBot found appple_fields_to.")
                            except:
                                try:
                                    easilydo_fields_to = p_driver.find_element_by_id(
                                        "com.easilydo.mail:id/contacts_to_field")
                                    logger.info(f"{p_udid}||| PhoneBot found easilydo_fields_to.")
                                except:
                                    try:
                                        yandex_fields_to = p_driver.find_element_by_id(
                                            "com.emailfantect.mailbox.allmail:id/rlt_top")
                                        logger.info(f"{p_udid}||| PhoneBot found yandex_fields_to.")
                                    except:
                                        try:
                                            easymail_fields_to = p_driver.find_element_by_id(
                                                "com.mail.emailapp.easymail2018:id/searchView")
                                            logger.info(f"{p_udid}||| PhoneBot found easymail_fields_to.")
                                        except:
                                            try:
                                                tohsoft_fields_to = p_driver.find_element_by_id(
                                                    "com.mail.hotmail.outlook.email:id/searchView")
                                                logger.info(f"{p_udid}||| PhoneBot found tohsoft_fields_to.")
                                            except:
                                                try:
                                                    hotmail_fields_to = p_driver.find_element_by_id(
                                                        "park.hotm.email.app:id/edit_text_to")
                                                    logger.info(f"{p_udid}||| PhoneBot found hotmail_fields_to.")
                                                except:
                                                    try:
                                                        outlook_fields_to = p_driver.find_element_by_id(
                                                            "park.outlook.sign.in.client:id/edit_text_to")
                                                        logger.info(f"{p_udid}||| PhoneBot found outlook_fields_to.")
                                                    except:
                                                        try:
                                                            emailfantext_fields_to = p_driver.find_element_by_id(
                                                                "com.emailfantect.mailbox.allmail:id/searchView")
                                                            logger.info(
                                                                f"{p_udid}||| PhoneBot found emailfantext_fields_to.")
                                                        except:
                                                            try:
                                                                gmx_fields_to = p_driver.find_element_by_id(
                                                                    "com.emailfantect.mailbox.allmail:id/searchView")
                                                                logger.info(
                                                                    f"{p_udid}||| PhoneBot found gmx_fields_to.")
                                                            except:
                                                                try:
                                                                    orange_fields_to = p_driver.find_element_by_id(
                                                                        "com.orange.mail.fr:id/autocomplete_to")
                                                                    logger.info(
                                                                        f"{p_udid}||| PhoneBot found orange_fields_to.")
                                                                except:
                                                                    try:
                                                                        mailwise_fields_to = p_driver.find_element_by_id(
                                                                            "com.syntomo.email:id/to")
                                                                        logger.info(
                                                                            f"{p_udid}||| PhoneBot found mailwise_fields_to.")
                                                                    except:
                                                                        try:
                                                                            mymail_fields_to = p_driver.find_element_by_id(
                                                                                "com.my.mail:id/edit_text_to")
                                                                            logger.info(
                                                                                f"{p_udid}||| PhoneBot found mymail_fields_to.")
                                                                        except:
                                                                            try:
                                                                                outlook2_fields_to = p_driver.find_element_by_id(
                                                                                    "com.microsoft.office.outlook:id/compose_to_field")
                                                                                logger.info(
                                                                                    f"{p_udid}||| PhoneBot found outlook2_fields_to.")
                                                                            except:
                                                                                try:
                                                                                    yahoomail_fields_to = p_driver.find_element_by_id(
                                                                                        "ymail_toLozengeContainer")
                                                                                    logger.info(
                                                                                        f"{p_udid}||| PhoneBot found yahoomail_fields_to.")
                                                                                except:
                                                                                    logger.info(
                                                                                        f"{p_udid}|||Phonebot didn't find any mail client. Please download Gmail app to fix this issue!")

            try:
                p_email = gmail_fields_to.text
                p_app = 'gmail'
            except:

                try:
                    p_email = aquamail_fields_to.text
                    p_app = 'aquamail'

                except:
                    try:
                        p_email = bluemail_fields_to.text
                        p_app = 'bluemail'
                    except:
                        try:
                            p_email = email_fields_to.text
                            p_app = 'email'
                        except:
                            try:
                                p_email = appple_fields_to.text
                                p_app = 'appple'
                            # elif len(bsoft_fields_to)!=0:
                            #   p_email = bsoft_fields_to.text
                            #  p_app = 'bsoft'
                            except:
                                try:
                                    p_email = easilydo_fields_to.text
                                    p_app = 'easilydo'
                                except:
                                    try:
                                        p_email = yandex_fields_to.text
                                        p_app = 'yandex'
                                    except:
                                        try:
                                            p_email = easymail_fields_to.text
                                            p_app = 'easymail'
                                        except:
                                            try:
                                                p_email = tohsoft_fields_to.text
                                                p_app = 'tohsoft'
                                            except:
                                                try:
                                                    p_email = hotmail_fields_to.text
                                                    p_app = 'hotmail'
                                                except:
                                                    try:
                                                        p_email = outlook_fields_to.text
                                                        p_app = 'outlook'
                                                    except:
                                                        try:
                                                            p_email = emailfantext_fields_to.text
                                                            p_app = 'emailfantext'
                                                        except:
                                                            try:
                                                                p_email = gmx_fields_to.text
                                                                p_app = 'gmx'
                                                            except:
                                                                try:
                                                                    p_email = orange_fields_to.text
                                                                    p_app = 'orange'
                                                                except:
                                                                    try:
                                                                        p_email = mailwise_fields_to.text
                                                                        p_app = 'mailwise'
                                                                    except:
                                                                        try:
                                                                            p_email = mymail_fields_to.text
                                                                            p_app = 'mymail'
                                                                        except:
                                                                            try:
                                                                                p_email = outlook2_fields_to.text
                                                                                p_app = 'outlook2'
                                                                            except:
                                                                                try:
                                                                                    p_email = yahoomail_fields_to.text
                                                                                    p_app = 'yahoomail'
                                                                                except:

                                                                                    logger.critical(
                                                                                        f"{p_udid}||| We couldn't get the email from the email client opened by Instagram! :-(")
                                                                                    logger.critical(
                                                                                        "Please contact support@phonebot.co, send the log.log file and the name of your email client installed on your smartphone! :-(")


            with lock:
                p_cursor1.execute("UPDATE smartphones set app_email_client=? where udid=?",(p_app,p_udid))
                sqliteConnection.commit()

        logger.info(f"{p_udid}|||p_email : {p_email}, p_app : {p_app}")
        return p_email,p_app
    except Exception as ex:
        logger.critical(f"{p_udid}|||{ex} --> ERROR get_email_from_mail_client_field_to")


# ========================================================================================================
# ================================  METHOD TAP ON GO BACK BUTTON ON FACEBOOK   ===========================
# ========================================================================================================
def GoBackButtonInstagram(p_driver,p_udid):

    while True:
        try:
            try:
                back_button=p_driver.find_element_by_id("com.instagram.android:id/action_bar_button_back")
                logger.info(f"{p_udid}|||We found the 'Back' button by 'id'. Let's click on it!")
                back_button.click()
                break
            except:
                try:
                    back_button = p_driver.find_element_by_xpath(
                        "//*[@class='android.widget.ImageView' and contains(@content-desc, 'Back')]")
                    logger.info(f"{p_udid}|||We found the English 'Back' button. Let's click on it!")
                    back_button.click()
                    break
                except:
                    try:
                        logger.info(f"{p_udid}|||We couldn't find the English 'Back' button. Let's search for the French one.")
                        back_button = p_driver.find_element_by_xpath(
                            "//*[@class='android.widget.ImageView' and contains(@content-desc, 'Retour')]")
                        logger.info(
                            f"{p_udid}|||PhoneBot found the French 'Back' button.")
                        back_button.click()
                        break
                    except:

                        logger.info(
                            f"{p_udid}|||PhoneBot didn't find the Englsih 'back' button. Let's try the Android back button.")
                        # === ANDROID BACK BUTTON ============================================
                        p_driver.press_keycode(keycode=4)
                        break

        #except ValueError :
        except Exception as ex:
            logger.critical(f"{p_udid}||| {ex} -> PhoneBot couldn't find the 'Back' button.")
            break

    logger.info(f"{p_udid}|||The bot will sleep just a few seconds..............................")
    time.sleep(random.uniform(0.9, 2.3))

# ==============================================================================================================
# ======================== METHOD TO LIKE SOME PICTURES FROM A HASHTAG SEARCH RESULT ===========================
# ==============================================================================================================
def LikeSearchPictures(p_driver, p_udid, myprofile_username,instagram_list_hashtags_liking_pictures,p_bug,lock):
    logger.info(f"{p_udid}|||# ================= METHOD TO LIKE SOME RANDOM PICTURES FROM HASH TAGS ==================")
    try:
        # ======================== [1] GET THE HASHTAG ====================================================

        hashtag = str(Pick_Up_Hashtag(p_udid,instagram_list_hashtags_liking_pictures)).strip()

        # ======================== [2] Let's make a search for this hashtag ===============================


        try:
            hashtag_found, p_bug = Insta_Search(p_driver, p_udid, hashtag, p_bug,lock)
        except:
            logger.error(f"{p_udid}|||There wasn't any result for the search of {hashtag}.")
            p_bug = True
            hashtag_found = False

        # =============== [3] We can now like follow this hashtag in order to like some pictures ==========
        '''
        button_follow = p_driver.find_element_by_id("com.instagram.android:id/follow_button")
        logger.info(f"{p_udid}|||button_follow.text : {button_follow.text}")
        if button_follow.text == "S’abonner":
            logger.info(f"{p_udid}|||The Follow button is in French and we can click on it")
            button_follow.click()
        elif button_follow.text == "Follow":
            logger.info(f"{p_udid}|||The Follow button is in English and we can click on it")
            button_follow.click()
        else:
            logger.info(f"{p_udid}|||The Follow button is not in French, neither in English, it means we already followed this hashtag {hashtag}!")
        '''
        swap_times = random.randint(1, 4)
        mymodules.Scroll_Down(p_driver, swap_times)
        image_buttons = p_driver.find_elements_by_id("com.instagram.android:id/image_button")
        logger.info(f"{p_udid}|||image_buttons : {image_buttons}")
        n = random.randint(0, len(image_buttons) - 1)
        logger.info(f"{p_udid}|||We click on any image of hashtag {hashtag} search results")
        while True:
            try:
                image_buttons[n].click()
                logger.info(f"{p_udid}|||image_buttons[n] : {image_buttons[n]}")
                logger.info(f"{p_udid}|||The bot will sleep just a few seconds..............................")
                p_driver.implicitly_wait(15)
                time.sleep(random.uniform(2.9, 6.3))
                if p_driver.find_element_by_id("com.instagram.android:id/row_feed_photo_profile_name"):
                    logger.info(f"{p_udid}|||We clicked on picture because we can see the picture's username on top of screen! :-)")
                    break
            except Exception as ex:
                logger.critical(
                    f"{ex} --> We couldn't click on the first image of hashtag {hashtag} search results! Let's try again!")

        logger.info(f"{p_udid}|||The bot will sleep just a few seconds..............................")
        time.sleep(random.uniform(2.9, 6.3))

        # =============== We arrive on a feed of picutres to like
        quantity_pictures_liked = random.randint(1, 4)
        counter_like = 0

        logger.info(f"{p_udid}|||counter_like : {counter_like}")
        logger.info(f"{p_udid}|||quantity_pictures_liked : {quantity_pictures_liked}")

        while counter_like != quantity_pictures_liked:

            try:
                like_buttons = p_driver.find_element_by_id("com.instagram.android:id/row_feed_button_like")

                like_buttons.click()
                counter_like += 1
                logger.info(f"{p_udid}|||We like a picture!")
                logger.info(f"{p_udid}|||counter_like : {counter_like}/{quantity_pictures_liked}")
            except:
                print("No 'Like button' found!")

            logger.info(f"{p_udid}|||The bot will sleep just a few seconds..............................")
            time.sleep(random.uniform(2.9, 6.3))

            # ==================== WE NEED TO SCROLL ========================================
            swap_times = random.randint(1, 4)
            mymodules.Scroll_Down(p_driver, swap_times,3)

        logger.info(f"{p_udid}|||We finished the task 'Liking pictures from search result of hashtag : {hashtag}'. :-)")
    except Exception as ex:
        logger.critical(f"{p_udid}|||{ex} --> ERROR LikeSearchPictures")



#==============================================================================================================
#======================== FUNCTION GET AN HASHTAG FROM TABLE 'sources' for Instagram===========================
#==============================================================================================================

def Pick_Up_Hashtag(p_udid,instagram_list_hashtags_liking_pictures):
    logger.info(f"{p_udid}|||# ===================== FUNCTION TO PICK UP A HASHTAG FROM A LIST =====================")
    try:

        hashtags_list = instagram_list_hashtags_liking_pictures.split('\\n')

        logger.info(f"{p_udid}|||hashtags: {hashtags_list}")
        hashtag_index = random.randint(0, len(hashtags_list) - 1)
        hashtag = hashtags_list[hashtag_index]

        return hashtag
    except Exception as ex:
        logger.critical(f"{p_udid}|||{ex} --> ERROR Pick_Up_Hashtag")



#==============================================================================================================
#============================ FUNCTION MAKE A SEARCH O INSTAGRAM FOR A HASHTAG ================================
#==============================================================================================================
def Insta_Search_Keyword(p_driver,p_hashtag,instagram_list_hashtags_liking_pictures,p_udid='',p_bug=False):
    logger.info(f"{p_udid}|||# =========================== FUNCTION TO SEARCH FOR HASHTAG IN INSTAGRAM ====================")
    try:

        cpt=0
        while True:
            try:
                #======================== [1] WE CLICK ON SEARCH BUTTON ==============================
                WebDriverWait(p_driver, 30).until(
                    EC.presence_of_element_located((By.ID, "com.instagram.android:id/tab_icon")))

                search_button = p_driver.find_elements_by_id("com.instagram.android:id/tab_icon")
                logger.info(f"{p_udid}|||search_button was found!")
                search_button[1].click()
                logger.info(f"{p_udid}|||We click on search button!")
                logger.info(f"{p_udid}|||The bot will sleep just a few seconds..............................")
                time.sleep(random.uniform(4.9, 8.3))

                break  # Only triggered if input is valid...
            except Exception as ex:
                cpt += 1
                if cpt > 4:
                    logger.critical(f"{p_udid}|||{ex} --> We tried several times to tap on search icon without success. You better restart your smartphone ID: {p_udid}.")
                    break
                elif cpt==2:
                    GoBackButtonInstagram(p_driver, p_udid)
                    logger.critical(f"{p_udid}|||{ex} --> PhoneBot still can't maclick on the search button. Let's try by going back.")
                    
                else:
                    logger.critical(f"{p_udid}|||{ex} --> We can't click on search icon of Instagram")
                logger.info(f"{p_udid}|||The bot will sleep just a few seconds..............................")
                time.sleep(random.uniform(1.5, 2.3))

        # ============================ [2] GET THE SEARCH FIELD ========================================
        WebDriverWait(p_driver, 30).until(
            EC.presence_of_element_located((By.ID, "com.instagram.android:id/action_bar_search_edit_text")))
        search_field = p_driver.find_element_by_id('com.instagram.android:id/action_bar_search_edit_text')
        search_field.click()
        logger.info(f"{p_udid}|||String to search : {p_hashtag}")
        while len(p_hashtag) > 20:  # Because of ActionChains Xoffset, we must limit the lenght of string to search to 20
            logger.error(
                f"This hashtag {p_hashtag} has more than 20 characters. Unfortunately we can't search for it! Let's pick up another one")
            p_hashtag = Pick_Up_Hashtag(p_udid,instagram_list_hashtags_liking_pictures)
            logger.info(f"{p_udid}|||")

        # ======================= [3] TYPE THE HASHTAG IN SEARCHFIELD ===================================

        found_it, p_bug = mymodules.send_keys_hashtag_delay_random(p_driver, p_udid, search_field, p_hashtag, p_bug,
                                                                   0.25, 0.55)
        if p_bug:
            found_it,p_bug = mymodules.send_keys_hashtag_delay_random(p_driver,p_udid, search_field, p_hashtag,p_bug, 0.25, 0.55)
        print(f"found_it : {str(found_it)}")
        p_driver.implicitly_wait(15)
        time.sleep(random.uniform(3.5, 5.3))

        # ======================= [4] SCENARIO : We didn't get results ===================================

        if not found_it:
            logger.info(
                "====== We will start the while search_field.text != hashtag and not found_it: ==========")
            try:
                while search_field.text != p_hashtag and not found_it:
                    logger.error(
                        f"The search didn't succeed : search_field({search_field.text}) <> hashtag({p_hashtag})")
                    logger.info(f"{p_udid}|||Let's try again!")
                    search_field.clear()
                    time.sleep(random.uniform(0.05, 0.3))
                    found_it,p_bug = mymodules.send_keys_hashtag_delay_random(p_driver,p_udid, search_field, p_hashtag,p_bug, 0.25, 0.55)
                    p_driver.implicitly_wait(15)
                    time.sleep(random.uniform(3.5, 5.3))
                    if found_it:
                        print(f"found_it N°2 : {str(found_it)}")
                        p_driver.implicitly_wait(15)
                        time.sleep(random.uniform(3.5, 5.3))
                        break

                    if len(p_driver.find_elements_by_id("com.instagram.android:id/row_no_results_textview")) > 0:
                        logger.error(f"{p_udid}|||This hashtag {p_hashtag} doesn't give any results! Let's pick up another one")
                        p_hashtag = Pick_Up_Hashtag(p_udid,instagram_list_hashtags_liking_pictures)


            except Exception as ex:
                logger.error(f"{p_udid}|||{ex} --> Something went wrong (maybe a popup appears?).... Let's try again.")
        else:
            p_driver.implicitly_wait(15)
            time.sleep(random.uniform(3.5, 5.3))
            return True, p_bug
    except Exception as ex:
        logger.critical(f"{p_udid}|||{ex} --> ERROR Insta_Search_Keyword")



#==============================================================================================================
#======================================== METHOD PUBLISH PICTURE ==============================================
#==============================================================================================================
def PublishPics(p_driver,p_udid,p_myprofile,lock,p_bug):
    number_actions_last_24H = mymodules.HowManyActions_Last24H(p_myprofile, 'instagram', 'post_picture')
    if number_actions_last_24H > 1:
        logger.info(f"{p_udid}|||Sorry. Phonebot already publish 2 pics in the last 24H for account {p_myprofile}!")
    else:
        logger.info(f"{p_udid}|||Phonebot didn't publish 2 pics in the last 24H for account {p_myprofile}. It can publish a picture on Instagram!")


        try:
            # ===================== [0] We prepare the DATABASE ==================================================
            sqliteConnection = sqlite3.connect(os.path.join(os.path.dirname(sys.argv[0]),'db.db')) # we prepare db
            p_cursor1 = sqliteConnection.cursor()



            # ===================== [0] We prepare the options ====================================================
            instagram_publish_pictures_facebook = mymodules.GetValueFromCustomField(p_udid,'instagram', p_myprofile,
                                                                                    'instagram_publish_pictures_facebook')
            instagram_publish_pictures_tumblr = mymodules.GetValueFromCustomField(p_udid,'instagram', p_myprofile,
                                                                                  'instagram_publish_pictures_tumblr')
            instagram_publish_pictures_twitter = mymodules.GetValueFromCustomField(p_udid,'instagram', p_myprofile,
                                                                                   'instagram_publish_pictures_twitter')

            # ===================== [1] We type on '+' button instagram button ==========================================
            while True:
                try:
                    p_driver.implicitly_wait(20)
                    try:
                        WebDriverWait(p_driver, 15).until(EC.presence_of_all_elements_located((By.ID,"com.instagram.android:id/tab_icon")))
                        add_photo= p_driver.find_elements_by_id("com.instagram.android:id/tab_icon")
                        add_photo[2].click()
                    except Exception as ex:
                        try:
                            WebDriverWait(p_driver, 15).until(EC.element_to_be_clickable((By.XPATH,"//*[@class='android.widget.FrameLayout' and contains(@content-desc, 'Appareil photo')]")))

                        except Exception as ex:
                            WebDriverWait(p_driver, 15).until(EC.element_to_be_clickable((By.XPATH,
                                                                                          "//*[@class='android.widget.FrameLayout' and contains(@content-desc, 'photo')]")))


                    logger.info(f"{p_udid}|||Bot will sleep a bit before to tap on gallery button..........")
                    time.sleep(random.uniform(6.2, 9.1))
                    break
                except Exception as ex:
                    logger.error(f"{p_udid}|||{ex} --> Error. We couldn't click on the '+' add picture button. Let's try again!")
                    logger.info(f"{p_udid}|||Bot will sleep a bit before to tap on gallery button..........")
                    time.sleep(random.uniform(5.2, 8.1))
            # ===================== [2] We tap on 'gallery' instagram button ==========================================
            p_driver.implicitly_wait(20)
            try:
                allow_access_to_gallery=p_driver.find_element_by_id("com.android.packageinstaller:id/permission_allow_button")
                allow_access_to_gallery.click()

            except Exception as ex:
                logger.error(f"{p_udid}|||{ex} --> We failed to click on 'Allow access' to phone gallery")

            while True:
                try:
                    try:
                        button_gallery = p_driver.find_element(By.XPATH,
                                                                    "//android.widget.TextView[@text='galerie']")
                        logger.info(f"{p_udid}|||We found the button 'galerie', we click on it! :-)")
                        button_gallery.click()
                        break
                    except:
                        try:
                            button_gallery = p_driver.find_element(By.XPATH,
                                                              "//android.widget.TextView[@text='gallery']")
                            logger.info(f"{p_udid}|||We found the button 'gallery', we click on it! :-)")
                            button_gallery.click()
                            break
                        except:
                            try:
                                button_gallery = p_driver.find_element(By.XPATH,
                                                                "//android.widget.TextView[@text='GALLERY']")
                                logger.info(f"{p_udid}|||We found the button 'GALLERY', we click on it! :-)")
                                button_gallery.click()
                                break
                            except:
                                try:
                                    button_gallery = p_driver.find_element(By.XPATH,
                                                                        "//android.widget.TextView[@text='GALERIE']")
                                    logger.info(f"{p_udid}|||We found the button 'GALERIE', we click on it! :-)")
                                    button_gallery.click()
                                    break
                                except:
                                    try:
                                        button_gallery = p_driver.find_element(By.XPATH,
                                                                            "//android.widget.TextView[@text='Galerie']")
                                        logger.info(f"{p_udid}|||We found the button 'Galerie', we click on it! :-)")
                                        button_gallery.click()
                                        break
                                    except:
                                        try:
                                            button_gallery = p_driver.find_element(By.XPATH,
                                                                                "//android.widget.TextView[@text='Gallery']")
                                            logger.info(
                                                f"{p_udid}|||We found the button 'Gallery', we click on it! :-)")
                                            button_gallery.click()
                                            break
                                        except:
                                            try:
                                                button_gallery = p_driver.find_element(By.XPATH,
                                                                                   "//android.widget.TextView[@text='gallery']")

                                                logger.info(
                                                    f"{p_udid}|||We found the button 'gallery', we click on it! :-)")
                                                button_gallery.click()
                                                break
                                            except:
                                                logger.error(
                                                    f"{p_udid}||| We couldn't tap on 'gallery' button! Let's try again!")


                except Exception as ex:
                    logger.error(f"{p_udid}|||{ex} --> We couldn't tap on 'Gallery' button! Let's try again!")

                logger.info(f"{p_udid}|||Bot will sleep a bit ..........")
                time.sleep(random.uniform(2.2, 3.1))

            # ===================== [3] We prepare 1rst list of pictures ==========================================

            WebDriverWait(p_driver, 15).until(
                EC.presence_of_all_elements_located((By.XPATH, "//*[@resource-id='com.instagram.android:id/media_picker_container']//*[@class='android.widget.CheckBox']")))
            field_gallery = p_driver.find_elements_by_xpath(
                "//*[@resource-id='com.instagram.android:id/media_picker_container']//*[@class='android.widget.CheckBox']")
            logger.info(f"{p_udid}|||len(field_gallery) : {len(field_gallery)}")


            while True:
                try:
                    #--- We loop the first serie of pictures and we will check if picture has been already publish or not
                    counter_insert_picture = 0
                    for n in range(1, len(field_gallery)):
                        counter_insert_picture = 0
                        picture = field_gallery[n].screenshot_as_base64
                        # =============================== WE TEST IF THIS PICTURE WAS ALREADY PUBLISHED ==================
                        if not p_cursor1.execute(
                                "SELECT * FROM actions WHERE picture=? and id_social_account=? and platform=? and type_action=?",
                                (picture, p_myprofile, 'instagram','post_picture')).fetchone():
                            # =============================== WE TEST WHEN WAS LAST TIME WE PUBLISH PICTURE (MAX=2 pic/day) ========

                            # --- We click on picture in order to publish it on instagram account
                            while True:
                                try:
                                    #============= We click on picture
                                    field_gallery[n].click()
                                    logger.info(f"{p_udid}|||We click on picture :-)")
                                    logger.info(f"{p_udid}|||Bot will sleep a bit ..........")
                                    time.sleep(random.uniform(1.2, 3.1))
                                    break
                                except Exception as ex:
                                    logger.error(f"{p_udid}|||{ex} --> We couldn't click on picture in order to publish it. Let's try again")
                            while True:
                                try:
                                    #============= We click on NEXT button
                                    WebDriverWait(p_driver, 15).until(
                                        EC.element_to_be_clickable((By.ID,"com.instagram.android:id/next_button_textview")))
                                    p_driver.find_element_by_id("com.instagram.android:id/next_button_textview").click()
                                    logger.info(f"{p_udid}|||Bot will sleep a bit ..........")
                                    time.sleep(random.uniform(1.2, 3.1))
                                    break
                                except Exception as ex:
                                    logger.error(f"{p_udid}|||{ex} --> We couldn't click on 'NEXT' button. Let's try again")

                            while True:
                                try:
                                    # ============= We click on NEXT button AGAIN (it is the 'image filters' part we want to skip
                                    WebDriverWait(p_driver, 15).until(
                                        EC.element_to_be_clickable((By.ID, "com.instagram.android:id/next_button_textview")))
                                    p_driver.find_element_by_id("com.instagram.android:id/next_button_textview").click()
                                    logger.info(f"{p_udid}|||Bot will sleep a bit ..........")
                                    time.sleep(random.uniform(1.2, 3.1))
                                    break
                                except Exception as ex:
                                    logger.error(f"{p_udid}|||{ex} --> We couldn't click on 'NEXT' button of 'pictures filter'. Let's try again")

                            while True:
                                try:

                                    # ============= Now we have to decide to share it on Facebook, Tumblr and Twitter also
                                    # ============= This depends of config.ini
                                    WebDriverWait(p_driver, 15).until(
                                        EC.presence_of_all_elements_located(
                                            (By.ID, "com.instagram.android:id/share_switch")))
                                    check_boxes_options = p_driver.find_elements_by_id("com.instagram.android:id/share_switch")
                                    # ============= FACEBOOK

                                    if instagram_publish_pictures_facebook == 1:
                                        logger.info(f"{p_udid}|||check_box Facebook = {check_boxes_options[0].get_attribute('checked')}")
                                        if check_boxes_options[0].get_attribute("checked")== 'false':
                                            logger.info(f"{p_udid}|||The checkbox 'Publish on facebook' is not checked. So we can checked it!")
                                            check_boxes_options[0].click()
                                            logger.info(f"{p_udid}|||Bot will sleep a bit ..........")
                                            time.sleep(random.uniform(1.2, 3.1))
                                    else:
                                        if check_boxes_options[0].get_attribute("checked")== 'true':
                                            logger.info(f"{p_udid}|||The checkbox 'Publish on facebook' is checked. So we can unchecked it!")
                                            check_boxes_options[0].click()
                                            logger.info(f"{p_udid}|||Bot will sleep a bit ..........")
                                            time.sleep(random.uniform(1.2, 3.1))
                                    # ============= TWITTER

                                    if instagram_publish_pictures_twitter == 1:
                                        logger.info(f"{p_udid}|||check_box Twitter = {check_boxes_options[1].get_attribute('checked')}")

                                        if check_boxes_options[1].get_attribute("checked")== 'false':
                                            logger.info(f"{p_udid}|||The checkbox 'Publish on Twitter' is not checked. So we can checked it!")
                                            check_boxes_options[1].click()
                                            logger.info(f"{p_udid}|||Bot will sleep a bit ..........")
                                            time.sleep(random.uniform(1.2, 3.1))
                                    else:
                                        if check_boxes_options[1].get_attribute("checked")== 'true':
                                            logger.info(f"{p_udid}|||The checkbox 'Publish on Twitter' is checked. So we can unchecked it!")
                                            check_boxes_options[1].click()
                                            logger.info(f"{p_udid}|||Bot will sleep a bit ..........")
                                            time.sleep(random.uniform(1.2, 3.1))
                                    # ============= TUMBLR

                                    if instagram_publish_pictures_tumblr == 1:
                                        logger.info(f"{p_udid}|||check_box Tumblr = {check_boxes_options[2].get_attribute('checked')}")

                                        if check_boxes_options[2].get_attribute("checked")== 'false':
                                            logger.info(f"{p_udid}|||The checkbox 'Publish on Tumblr' is not checked. So we can checked it!")
                                            check_boxes_options[2].click()
                                            logger.info(f"{p_udid}|||Bot will sleep a bit ..........")
                                            time.sleep(random.uniform(1.2, 3.1))
                                    else:
                                        if check_boxes_options[2].get_attribute("checked")== 'true':
                                            logger.info(f"{p_udid}|||The checkbox 'Publish on Tumblr' is checked. So we can unchecked it!")
                                            check_boxes_options[2].click()
                                            logger.info(f"{p_udid}|||Bot will sleep a bit ..........")
                                            time.sleep(random.uniform(1.2, 3.1))
                                    break
                                except Exception as ex:
                                    logger.error(f"{p_udid}|||{ex} --> We couldn't click on the share options. Let's try again")

                            # ============ Now we need to fill the label of pictures with a label and some hashtags
                            # ============ So let's first take the title of our pic from table 'sources'
                            # ========== We extract the necessary values from table 'sources'
                            while True:
                                try:



                                    list_of_labels_pictures=mymodules.GetValueFromCustomField(p_udid,'instagram', p_myprofile, 'list_of_labels_pictures')
                                    labels = list_of_labels_pictures.split('\\n')

                                    list_hashtags_publish_pictures=mymodules.GetValueFromCustomField(p_udid,'instagram', p_myprofile, 'list_hashtags_publish_pictures')


                                    label = labels[random.randint(0, len(labels) - 1)]
                                    #list_hashtags = [item[0] for item in hashtags_tuple]
                                    list_hashtags = list_hashtags_publish_pictures.split(' \\n')
                                    print(f"labels : {labels}")
                                    print(f"label : {label}")
                                    print(f"list_hashtags : {list_hashtags}")

                                    # ===== We generate the hashtags
                                    # https://stackoverflow.com/questions/3996904/generate-random-integers-between-0-and-9

                                    quantity_hashtags = random.randint(20, 25)

                                    if len(list_hashtags) < 20:
                                        logger.info(
                                            f"You should add more hashtags in the configuration of your PhoneBot in 'Account details' on https://phonebot.co.. You have only {len(list_hashtags)} hashtags. It is recommanded to publish post on instagram with around 20-25 hashtags!")
                                        size = len(list_hashtags)
                                    else:
                                        size = quantity_hashtags
                                    list_hashtags_index = random.sample(range(len(list_hashtags)), size)
                                    print(f"list_hashtags_index : {list_hashtags_index}")

                                    # =================== We built the string of hashtags ==========================================
                                    #n = 0
                                    string_list_hashtags = ''
                                    for n2 in range(0, len(list_hashtags_index) - 1):
                                        string_list_hashtags += list_hashtags[list_hashtags_index[n2]] + ' '

                                    print(f"string_list_hashtags : {string_list_hashtags}")

                                    # ============== We can now prepare the string to be sent to our method send_keys
                                    insta_label = label + "|||" + string_list_hashtags

                                    print(f"insta_label : {insta_label}")
                                    insta_label = unidecode.unidecode(insta_label)
                                    break
                                except Exception as ex:
                                    logger.error(f"{p_udid}|||{ex} --> We couldn't prepare the hashtags and label. Please check your sources.csv.")

                            # =============================== WE SEND_KEYS THE LABEL OF PICTURE ===========================
                            while True:
                                try:
                                    label_field = p_driver.find_element_by_id("com.instagram.android:id/caption_text_view")
                                    label_field.click()
                                    logger.info(f"{p_udid}|||The bot will sleep just a few seconds..............................")
                                    time.sleep(random.uniform(1.9, 3.3))

                                    break
                                except Exception as ex:
                                    logger.error(f"{p_udid}|||{ex} --> We couldn't type the label field of the picture you want to publish. Let's try again")

                            print(f"PhoneBot will send Instagram message through smartphone N° {p_udid}")
                            
                            p_bug = mymodules.send_keys_message_delay_random('Instagram',p_driver, label_field, insta_label,p_bug, 0.5, 0.75,300,p_udid)



                            # =============================== WE CLICK ON SHARE BUTTON ===========================
                            while True:
                                try:
                                    WebDriverWait(p_driver, 15).until(
                                        EC.element_to_be_clickable((By.ID, "com.instagram.android:id/next_button_textview")))
                                    p_driver.find_element_by_id("com.instagram.android:id/next_button_textview").click()
                                    logger.info(f"{p_udid}|||Bot will sleep a bit ..........")
                                    time.sleep(random.uniform(1.2, 3.1))
                                    break
                                except Exception as ex:
                                    logger.error(f"{p_udid}|||{ex} --> We couldn't click on 'Share' button. Let's try again")

                            # =============================== WE UPDATE TABLE ACTIONS ===========================

                            now = datetime.now()
                            date_n_time = str(now.strftime("%d/%m/%Y %H:%M:%S"))
                            with lock:
                                p_cursor1.execute(
                                    "INSERT INTO actions (picture,id_social_account, platform,id_smartphone,type_action,date) VALUES (?,?,?,?,?,?)", \
                                    (picture, p_myprofile, 'instagram', p_udid,'post_picture',date_n_time))
                                sqliteConnection.commit()
                            p_cursor1.close()
                            sqliteConnection.close()
                            logger.info(f"{p_udid}|||We updated table 'actions'! :-)")
                            counter_insert_picture +=1
                            break

                    #---- If the counter of inserting pictures = 0, it means we insert all the pictures
                    if counter_insert_picture == 0:
                        logger.info(f"{p_udid}|||We already upload all these pictures. Let's scroll down to search for unpublished pictures!")
                        n=0
                        #=========================================== SCROLL ===========================================
                        # --- We scroll once ------------------------------------------------------------------------------------
                        p_driver.scroll(field_gallery[n + 5], field_gallery[n + 1])
                        logger.info(f"{p_udid}|||We scroll once.")
                        # --- We need to reload elements otherwise we can't scroll ----------------------------------------------
                        field_gallery = p_driver.find_elements_by_xpath(
                            "//*[@resource-id='com.instagram.android:id/media_picker_container']//*[@class='android.widget.CheckBox']")
                        logger.info(f"{p_udid}|||len(gallery) in the loop after 1rst scroll : {len(field_gallery)}")

                        # --- We scroll a second time ---------------------------------------------------------------------------
                        logger.info(f"{p_udid}|||Bot will sleep a bit ..........")
                        time.sleep(random.uniform(1.2, 2.1))
                        p_driver.scroll(field_gallery[n + 5], field_gallery[n + 1])
                        logger.info(f"{p_udid}|||We scroll a second time.")
                        logger.info(f"{p_udid}|||Bot will sleep a bit ..........")
                        time.sleep(random.uniform(2.2, 3.1))

                        # --- We need to reload elements otherwise we can't scroll ----------------------------------------------
                        field_gallery = p_driver.find_elements_by_xpath(
                            "//*[@resource-id='com.instagram.android:id/media_picker_container']//*[@class='android.widget.CheckBox']")
                        logger.info(f"{p_udid}|||len(gallery) in the loop after 1rst scroll : {len(field_gallery)}")

                    else:



                        logger.info(f"{p_udid}|||We publish a picture, we did our job. We can exit the loop 'while'!")
                        break
                except Exception as ex:
                    logger.error(f"{p_udid}|||{ex} --> Error while publishing a picture!")
        except Exception as ex:
            logger.critical(f"{p_udid}|||{ex} --> ERROR PublishPics")



#==============================================================================================================
#==========================================  METHOD UNFOLLOW ==================================================
#==============================================================================================================
def InstagramUnFollow(p_driver,p_udid,myprofile_username,quantity_tasks_per_hit):
    while True:

        try:
            sqliteConnection = sqlite3.connect(mymodules.LoadFile('db.db'))  # we prepare db
            cursor1 = sqliteConnection.cursor()

            logger.info(f"{p_udid}|||==================== STARTING TASK UNFOLLOW Instagram old following ===============================")
            try_counter=0
            #=================================== CLICK ON PROFILE BUTTON =========================================
            while True:
                # =================================================================================
                # =========================== PLAY STOP OR PAUSE ? ================================
                # =================================================================================
                mymodules.PlayStopPause(p_udid, 'Intagram unfollow')
                # =================================================================================
                # =================================================================================
                # =================================================================================
                try:
                    logger.info(f"{p_udid}|||The bot will sleep just a few seconds..............................")
                    time.sleep(random.uniform(0.9, 2.3))

                    WebDriverWait(p_driver, 15).until(
                        EC.element_to_be_clickable((By.ID, "com.instagram.android:id/profile_tab")))
                    profile_button = p_driver.find_element_by_id("com.instagram.android:id/profile_tab")
                    ActionChains(p_driver).move_to_element(profile_button).perform()
                    profile_button.click()
                    logger.info(f"{p_udid}|||My Profile_button was found!")
                    break
                except Exception as ex:
                    try_counter+=1
                    logger.error(f"{p_udid}|||{ex} --> We didn't click on my profile page! :-(. Let's try again!")
                    if try_counter > 5:
                        logger.info (
                            f"{p_udid}|||This is the {try_counter} times we tried to tap on 'My profile' icon. Instagram seems to have issue. We skip this task!")
                        break
                        '''
                        logger.info(f"{p_udid}|||This is the {try_counter} times we tried to tap on 'My profile' icon. Instagram seems to have issue. We need to restart instagram!")
                        p_driver.quit()
                        logger.info(f"{p_udid}|||The bot will sleep just a few seconds..............................")
                        time.sleep(random.uniform(1.9, 4.3))
                        p_driver = Initialisation_Driver('Unfollow', p_udid, p_systemPort, p_deviceName, p_version,p_os)
                        logger.info(f"{p_udid}|||The bot will sleep just a few seconds..............................")
                        time.sleep(random.uniform(8.9, 16.3))
                        '''
            # ================================================================================================================


            logger.info(f"{p_udid}|||We click on Profile button!")
            logger.info(f"{p_udid}|||The bot will sleep just a few seconds..............................")
            time.sleep(random.uniform(5.1, 9.2))
            # ===================================================================================================
            # =============================== TAP THE FOLLOWING BUTTON ==========================================
            # ===================================================================================================
            while True:
                try:
                    WebDriverWait(p_driver, 30).until(
                    EC.element_to_be_clickable((By.ID, "com.instagram.android:id/row_profile_header_textview_following_count")))

                    following_button = p_driver.find_element_by_id("com.instagram.android:id/row_profile_header_textview_following_count")
                    following_button.click()
                    break
                except Exception as ex:
                    logger.critical(f"{p_udid}|||{ex} --> We didn't find the counter of 'Following'. We couldn't display the list of 'Following'!")
                    logger.critical(
                        "We will try again'!")
                    mymodules.Scroll_Up(p_driver,p_udid)


            p_driver.implicitly_wait(30)
            time.sleep(random.uniform(2.9, 6.3))
            # ================================================================================================================

            # ============================== Then we need to order by the oldest one first ===================================
            following_order_button = p_driver.find_element_by_id("com.instagram.android:id/sorting_entry_row_icon")
            following_order_button.click()
            p_driver.implicitly_wait(30)
            time.sleep(random.uniform(1.9, 3.3))
            logger.info(f"{p_udid}|||following_order_button was found!")
            logger.info(f"{p_udid}|||We click on following_order_button!")

            '''
            THIS IS ANOTHER TECHNIC TO CHECK THE FILTERS BY NAME
            following_order_list = p_driver.find_elements_by_id("com.instagram.android:id/follow_list_sorting_option")
            i=0
            while i<len(following_order_list):
                if str(following_order_list[i].get_attribute("text")).find('Latest')!=-1 or str(following_order_list[i].get_attribute("text")).find('Dernier')!=-1:
                    following_order_list[i].click()
                i+=1
            '''
            #--- A popup will appear, we need to check the last one
            following_order_list = p_driver.find_elements_by_id("com.instagram.android:id/follow_list_sorting_option_radio_button")
            following_order_list[2].click()

            #--- We wait a bit to display the list by Oldest ones first
            p_driver.implicitly_wait(10)
            time.sleep(random.uniform(0.9, 2.3))

            # ============================ Ok now we need to make a first scroll  ========================================
            #--- So we need to get the bottom point and top point to make a scroll from bottom to top
            counter_action_unfollow = 0
            #WebDriverWait(driver, 30).until(
                #EC.presence_of_element_located((By.ID, "com.instagram.android:id/title")))
            #header_following = driver.find_element_by_id("com.instagram.android:id/title")
            WebDriverWait(p_driver, 30).until(
             EC.presence_of_element_located((By.ID, "com.instagram.android:id/row_search_edit_text")))
            search_filed_following = p_driver.find_element_by_id("com.instagram.android:id/row_search_edit_text")


            WebDriverWait(p_driver, 30).until(
                EC.presence_of_element_located((By.ID, "com.instagram.android:id/sorting_entry_row_option")))
            header_order = p_driver.find_element_by_id("com.instagram.android:id/sorting_entry_row_option")

            #-- We can now make the scroll
            p_driver.scroll(header_order, search_filed_following)
            #--- Then we prepare our first list of following
            n = 0
            x = 5

            time.sleep(random.uniform(1.1, 3.9))
            WebDriverWait(p_driver, 30).until(
                EC.presence_of_element_located((By.ID, "com.instagram.android:id/follow_list_username")))

            list_following = p_driver.find_elements_by_id("com.instagram.android:id/follow_list_username")
            while counter_action_unfollow < quantity_tasks_per_hit + 1:  # We have to respect the limit per task
                # =================================================================================
                # =========================== PLAY STOP OR PAUSE ? ================================
                # =================================================================================
                mymodules.PlayStopPause(p_udid, 'Intagram unfollow')
                # =================================================================================
                # =================================================================================
                # =================================================================================
                logger.info(f"{p_udid}|||n = {n}")
                logger.info(f"{p_udid}|||counter_action_unfollow = {counter_action_unfollow}")

                if n == x:  # We work on 5 users of a short list. We need to scroll down and reset the counter 'n'
                        p_driver.scroll(list_following[4], list_following[0])
                        time.sleep(random.uniform(1.1, 3.9))
                        WebDriverWait(p_driver, 30).until(
                            EC.presence_of_element_located((By.ID, "com.instagram.android:id/follow_list_username")))

                        list_following = p_driver.find_elements_by_id("com.instagram.android:id/follow_list_username")
                        n=0
                WebDriverWait(p_driver, 30).until(
                    EC.presence_of_element_located((By.ID, "com.instagram.android:id/button")))

                buttons_unfollow = p_driver.find_elements_by_id("com.instagram.android:id/button")


                if buttons_unfollow[n].get_attribute('text')== 'Following' or buttons_unfollow[n].get_attribute('text')== 'Abonné(e)':
                    unfollow_account = list_following[n].text
                    buttons_unfollow[n].click() #We click on button unfollow

                    time.sleep(random.uniform(1.2, 2.8))

                    # === Instagram may ask to confirm the Unfollow
                    try:
                        confirm_unfollow = p_driver.find_element_by_id("com.instagram.android:id/primary_button")

                        confirm_unfollow.click()
                        time.sleep(random.uniform(1.2, 2.8))
                    except:
                        logger.info(f"{p_udid}|||PhoneBot couldn't click on 'Confirm Unfollow' button.")



                    # ============================ ADD USERNAME OF FOLLOWING IN TABLE 'contacts' ============================

                    # ======================================================================================================


                    if cursor1.execute("select * from contacts where username=? and platform=?",
                                       (unfollow_account, 'instagram')).fetchone():
                        logger.info(f"{p_udid}|||Username {unfollow_account} already exist in table 'contacts'. We can skip it")

                    else:
                        logger.info(f"{p_udid}|||Username {unfollow_account} doesn't exist in table 'contacts'. Let's insert it in table!")
                        cursor1.execute("INSERT INTO contacts (username,platform) VALUES (?,?)", \
                                        (unfollow_account, 'instagram'))
                        sqliteConnection.commit()

                    # ============================ INSERT ACTION IN TABLE ACTIONS ==============================
                    # --- First we need to know the id_contacts of the followers (We added him/her previously in table 'contacts'
                    id_unfollow_tuple = cursor1.execute("SELECT id FROM contacts WHERE username=? AND platform=?",
                                                       (unfollow_account, 'instagram')).fetchone()
                    id_unfollow = int(id_unfollow_tuple[0])  # We transform the id_contact in integer in order to store it in table
                    sqliteConnection.commit()

                    # --- Secondly, we can insert a ROW in table 'actions' =================================================
                    logger.info(f"{p_udid}|||p_udid : {p_udid}")
                    logger.info(f"{p_udid}|||myprofile_username : {myprofile_username}")
                    logger.info(f"{p_udid}|||id_contact : {id_unfollow}")
                    now = datetime.now()
                    date_n_time = str(now.strftime("%d/%m/%Y %H:%M:%S"))
                    cursor1.execute("INSERT INTO actions (platform,type_action, date, id_smartphone, id_social_account, id_contact)  \
                                                            VALUES (?,?,?,?,?,?)",
                                    ('instagram', 'unfollow', date_n_time, p_udid, str(myprofile_username), id_unfollow))
                    sqliteConnection.commit()
                    counter_action_unfollow += 1
                n+=1

                # =============================[11] LET'STOP EVERYTHING IF LIMIT IS REACHED ========================
                if counter_action_unfollow == quantity_tasks_per_hit:
                    break
            logger.info(f"{p_udid}|||The Task Unfollow is finished! :-). PhoneBot will continue with another task!")
            return counter_action_unfollow
        #except ValueError:
        except Exception as ex:
            logger.critical(f"{p_udid}|||{ex} --> ERROR WITH FUNCTION UNFOLLOW!!!!")


#==========================================================================================================
#==============================     METHOD SCROLL UP PICS     =================================
#==========================================================================================================

def Scroll_up_pic(p_driver,p_udid):
    try:


        profile_avatar = p_driver.find_element_by_id("com.instagram.android:id/row_feed_photo_profile_imageview")
        head_publication = p_driver.find_element_by_id("com.instagram.android:id/feed_title")
        p_driver.scroll(profile_avatar, head_publication)
        '''
        pictures = p_driver.find_elements_by_class_name("android.widget.FrameLayout")
        p_bounds = pictures[0].get_attribute('bounds')
        p_bounds = p_bounds[1:len(p_bounds) - 1]
        p_bounds = p_bounds.replace('][', ',').replace('[', ',').replace(']', ',')
        # conver to the list
        list_xy = p_bounds.split(",")
        # print(p_bounds)
        # print(list_xy)
        p_bounds_x1 = int(list_xy[0])
        p_bounds_y1 = int(list_xy[1])
        p_bounds_x2 = int(list_xy[2])
        p_bounds_y2 = int(list_xy[3])
        # print(f"bounds_x1 : {bounds_x1}")
        # print(f"bounds_y1 : {bounds_y1}")
        # print(f"bounds_x2 : {bounds_x2}")
        # print(f"bounds_y2 : {bounds_y2}")


        p_offset_x = (p_bounds_x2 - p_bounds_x1)/2
        p_offset_y = (p_bounds_y2 - p_bounds_y1)
        actions = TouchAction(p_driver)
        actions.tap_and_hold(p_offset_x, p_offset_y)
        actions.move_to(p_offset_y, p_offset_y + 100)
        actions.release()
        actions.perform()
        '''
        logger.info(f"{p_udid}|||We scroll the picture :-)")
    except Exception as ex:
        logger.error(f"{p_udid}|||{ex} --> There was an error while scrolling the picture!")


def Scroll_up_profile(p_driver,p_udid):
    try:
        profile_tab = p_driver.find_elements_by_id("com.instagram.android:id/profile_tab_icon_view")
        profile_avatar = p_driver.find_element_by_id("com.instagram.android:id/row_profile_header_imageview")
        see_all_button= p_driver.find_elements_by_id("com.instagram.android:id/netego_carousel_cta")
        if len(profile_tab)!=0:
            p_driver.scroll(profile_tab[0],profile_avatar)
            logger.info(f"{p_udid}|||We scroll the profile :-)")
        elif len(see_all_button)!=0:
            p_driver.scroll(see_all_button[0], profile_avatar)
            logger.info(f"{p_udid}|||We scroll the profile :-)")
        else:
            logger.error(f"{p_udid}|||We couldn't scoll the profile :-(")


        '''
        p_bounds = profile_tab[0].get_attribute('bounds')
        p_bounds = p_bounds[1:len(p_bounds) - 1]
        p_bounds = p_bounds.replace('][', ',').replace('[', ',').replace(']', ',')
        # conver to the list
        list_xy = p_bounds.split(",")
        # print(p_bounds)
        # print(list_xy)
        p_bounds_x1 = int(list_xy[0])
        p_bounds_y1 = int(list_xy[1])
        p_bounds_x2 = int(list_xy[2])
        p_bounds_y2 = int(list_xy[3])
        # print(f"bounds_x1 : {bounds_x1}")
        # print(f"bounds_y1 : {bounds_y1}")
        # print(f"bounds_x2 : {bounds_x2}")
        # print(f"bounds_y2 : {bounds_y2}")


        p_offset_x = (p_bounds_x2 - p_bounds_x1)/2
        p_offset_y = p_bounds_y2 - (p_bounds_y2 - p_bounds_y1)/2
        actions = TouchAction(p_driver)
        actions.long_press(p_offset_x, p_offset_y)
        actions.move_to(p_offset_y, p_offset_y + 100)
        actions.release()
        actions.perform()
        
        '''

    except Exception as ex:
        logger.error(f"{p_udid}|||{ex} --> There was an error while scrolling the profile!")


#==========================================================================================================
#==============================     FUNCTION INITIALISATION OF DRIVER     =================================
#==========================================================================================================
def Initialisation_Driver(p_name_action, p_udid, p_systemPort, p_deviceName, p_version,p_os):
    while True:
        try:

            # ======================== INITIALISATION OF DRIVER ================================
            logger.info(f"{p_udid}|||============== INITIALISATION OF DRIVER for Smartphone {p_udid} for action {p_name_action} ==========")
            logger.info(f"{p_udid}|||p_udid : {p_udid}")
            logger.info(f"{p_udid}|||p_systemPort : {p_systemPort}")
            logger.info(f"{p_udid}|||p_deviceName : {p_deviceName}")
            logger.info(f"{p_udid}|||p_version : {p_version}")
            logger.info(f"{p_udid}|||p_os : {p_os}")
            logger.info(f"{p_udid}|||===============================================================================================")

            desired_caps = {}
            desired_caps['automationName'] = 'UiAutomator2'
            desired_caps['platformName'] = p_os
            desired_caps['platformVersion'] = p_version
            desired_caps['deviceName'] = p_deviceName
            desired_caps['udid'] = p_udid
            desired_caps['noReset'] = 'true'
            desired_caps['systemPort'] = p_systemPort
            desired_caps['chromeDriverPort'] = p_systemPort
            desired_caps['appWaitDuration'] = 100000
            desired_caps['newCommandTimeout'] = 0
            desired_caps['wdaStartupRetries'] = 4
            desired_caps['wdaStartupRetryInterval'] = 20000
            desired_caps['uiautomator2ServerLaunchTimeout'] = 100000
            desired_caps['remoteAppsCacheLimit'] = 0
            desired_caps['noSign'] = 'true'
            desired_caps['appWaitPackage'] = 'com.instagram.android'
            desired_caps['appWaitActivity'] = 'com.instagram.mainactivity.MainActivity'
            desired_caps['appPackage'] = 'com.instagram.android'
            desired_caps['appActivity'] = 'com.instagram.mainactivity.MainActivity'

            while True:
                try:
                    driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
                    time.sleep(random.uniform(10.5, 15.3))
                    # driver.start_activity("com.instagram.android", "com.instagram.mainactivity.MainActivity")
                    return driver
                except Exception as ex:
                #except Exception as ex:
                    logger.critical(f"{p_udid}|||{ex} --> Something went wrong! PLease contact support@phonebot.co")
                    logger.critical(f"{p_udid}|||{ex} --> We can't open Instagram. Please check if device is connected. Let's try again!")
        except Exception as ex:
            logger.critical(f"{p_udid}|||{ex} --> ERROR ")










#==========================================================================================================
#==============================     FUNCTION MAKE A SEARCH ON INSTAGRAM   =================================
#==========================================================================================================
def Insta_Search(driver,p_udid,p_string_to_search,p_bug,lock):
    try:
        logger.info(f"{p_udid}|||========================= FUNCTION Insta_Search ===================================")
        cpt=0
        while True:
            try:
                # search_button = driver.find_element(By.XPATH,"//android.widget.ImageView[@bounds='[126,800][162,836]']")
                #WebDriverWait(driver, 30).until(
                #    EC.presence_of_element_located((By.ID, "com.instagram.android:id/tab_icon")))

                search_button = driver.find_elements_by_id("com.instagram.android:id/tab_icon")
                logger.info(f"{p_udid}|||search_button was found!")
                search_button[1].click()
                logger.info(f"{p_udid}|||We click on search button!")
                logger.info(f"{p_udid}|||The bot will sleep just a few seconds..............................")
                time.sleep(random.uniform(0.5, 1.3))
                search_button[1].click()

                break  # Only triggered if input is valid...
            except Exception as ex:
                cpt += 1
                if cpt > 4:
                    logger.critical(
                        f"{p_udid}|||{ex} --> We tried several times to tap on search icon without success. You better restart your smartphone ID: {p_udid}.")
                    logger.critical(
                        f"{p_udid}|||PhoneBot will raise an error in order to quit Instagram Bot.")
                    search_button[1].click() # this is for creating an error and raise exception and leave Instagram bot

                    break
                elif cpt == 2:
                    GoBackButtonInstagram(driver, p_udid)

                    logger.critical(
                        f"{p_udid}|||{ex} --> PhoneBot still can't click on the search button. Let's try by going back.")
                else:
                    logger.critical(f"{p_udid}|||{ex} --> We can't click on search icon of Instagram")
                logger.info(f"{p_udid}|||The bot will sleep just a few seconds..............................")
                time.sleep(random.uniform(1.5, 2.3))
        # search_button = driver.find_element(By.XPATH,"//android.widget.FrameLayout[@bounds='[126,800][162,836]']")

        driver.implicitly_wait(30)
        # ============================ GET THE SEARCH FIELD ========================================
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "com.instagram.android:id/action_bar_search_edit_text")))
        search_field = driver.find_element_by_id('com.instagram.android:id/action_bar_search_edit_text')
        search_field.click()
        logger.info(f"{p_udid}|||String to search : {p_string_to_search}")
        if len(p_string_to_search) > 20:  # Because of ActionChains Xoffset, we must limit the lenght of username to 20
            logger.error(
                f"This username {p_string_to_search} has more than 20 characters. We will copy-paste the username directly in search field!")
            #return False,p_bug
            # ================ LITTLE CHANGE, WE ADD THESE LINES ============================================================
            search_field.clear()
            search_field.send_keys(p_string_to_search)
            p_bug = True

            # === Le's click on results
            try:
                search_results = driver.find_elements_by_id('com.instagram.android:id/row_search_user_username')
            except:
                logger.error(f"{p_udid}|||There wasn't any result for the search of {p_string_to_search}.")
                return False, p_bug


            for search_result in search_results:
                print(f"search_result.text = {search_result.text}")
                while True:
                    try:
                        if search_result.text == p_string_to_search:
                            time.sleep(random.uniform(1.2, 3.3))
                            logger.info(
                                f"{p_udid}|||Yahoo!!! We found it in search results! Let's go for it right now!!!")
                            logger.info(
                                f"{p_udid}|||The bot will sleep just a few seconds..............................")
                            time.sleep(random.uniform(0.9, 3.3))

                            search_result.click()
                            found_it = True
                            break

                        else:
                            found_it = False
                            break
                    except Exception as ex:
                        logger.error(
                            f"{p_udid} -- {ex} --> Something went wrong when we compare search_result.text with p_keys. Let's try again!")
                if found_it:
                    break



        else:

            # ======================= TYPE THE CONTACT USERNAME IN SEARCHFIELD ===================================
            logger.info(f"p_bug : {p_bug} - type : {type(p_bug)}")

            found_it=mymodules.send_keys_delay_random_instagram(driver,p_udid, search_field, p_string_to_search,p_bug, 0.25, 0.55)
            # ====================== WE CHECK IF THE WORD WAS TYPED CORRECTLY =============================
            if not found_it:
                if str(search_field.get_attribute('text')).strip() != p_string_to_search:
                    logger.error(
                        f"send_keys_delay_random_instagram ||| PhoneBot detect an issue when the smartphone is typing some characters. This smartphone is bugging.")
                    search_field.clear()
                    search_field.send_keys(p_string_to_search)
                    p_bug = True

                    # === Le's click on results
                    try:
                        search_results = driver.find_elements_by_id('com.instagram.android:id/row_search_user_username')
                    except:
                        logger.error(f"{p_udid}|||There wasn't any result for the search of {p_string_to_search}.")
                        return False, p_bug
                    if len(search_results)!=0:
                        for search_result in search_results:
                            print(f"search_result.text = {search_result.text}")
                            while True:
                                try:
                                    if search_result.text == p_string_to_search:
                                        time.sleep(random.uniform(1.2, 3.3))
                                        logger.info(
                                            f"{p_udid}|||Yahoo!!! We found it in search results! Let's go for it right now!!!")
                                        logger.info(
                                            f"{p_udid}|||The bot will sleep just a few seconds..............................")
                                        time.sleep(random.uniform(0.9, 3.3))

                                        search_result.click()
                                        found_it=True
                                        break

                                    else:
                                        found_it=False
                                        break
                                except Exception as ex:
                                    logger.error(f"{p_udid} -- {ex} --> Something went wrong when we compare search_result.text with p_keys. Let's try again!")
                            if found_it:
                                break


                else:

                    logger.error(
                        f"send_keys_delay_random_instagram ||| This smartphone is working fine.")

                    try:
                        search_results = driver.find_elements_by_id('com.instagram.android:id/row_search_user_username')
                    except:
                        logger.error(f"{p_udid}|||There wasn't any result for the search of {p_string_to_search}.")
                        return False, p_bug
                    if len(search_results) != 0:
                        for search_result in search_results:
                            print(f"search_result.text = {search_result.text}")
                            while True:
                                try:
                                    if search_result.text == p_string_to_search:
                                        time.sleep(random.uniform(1.2, 3.3))
                                        logger.info(
                                            f"{p_udid}|||Yahoo!!! We found it in search results! Let's go for it right now!!!")
                                        logger.info(
                                            f"{p_udid}|||The bot will sleep just a few seconds..............................")
                                        time.sleep(random.uniform(0.9, 3.3))

                                        search_result.click()
                                        found_it = True
                                        break

                                    else:
                                        found_it = False
                                        break
                                except Exception as ex:
                                    logger.error(
                                        f"{p_udid} -- {ex} --> Something went wrong when we compare search_result.text with p_keys. Let's try again!")
                            if found_it:
                                break




            print(f"found_it : {str(found_it)}")
            driver.implicitly_wait(10)
            time.sleep(random.uniform(2.5, 3.3))
            if not found_it:
                try:

                    logger.info(f"{p_udid}|||We didn't find '{p_string_to_search}'. So we will remove it from table 'contacts'")
                    with lock:
                        sqliteConnection = sqlite3.connect(mymodules.LoadFile('db.db'))  # we prepare db
                        p_cursor1 = sqliteConnection.cursor()
                        p_cursor1.execute("DELETE FROM contacts WHERE platform=? AND username=?",('instagram',p_string_to_search))
                        sqliteConnection.commit()
                        p_cursor1.close()
                        sqliteConnection.close()
                except Exception as ex:
                    logger.error(f"{p_udid}|||{ex} --> Something went wrong when PhoneBOt tried to remove {p_string_to_search} from database.")
            else:
                return True,p_bug
    #except ValueError:
        #print("error instasearch")
    except Exception as ex:
        logger.critical(f"{p_udid}|||{ex} --> ERROR Insta_Search")




#==========================================================================================================
#===================================        METHOD TO START THE BOT       =================================
#==========================================================================================================
def StartBot(p_name_action='', p_udid='', p_systemPort='', p_deviceName='', p_version='',
                                        p_os='', p_Daily_limit_Instagram_Scrap_profile_details=1,    \
                                        p_Daily_limit_Instagram_Scrap_email=1, \
                                        p_Daily_limit_Instagram_Send_message=1, \
                                        p_Daily_limit_Instagram_Like_pics_of_member=1, \
                                        p_Daily_limit_Instagram_Follow_members=1, \
                                        p_Daily_limit_Instagram_UnFollow_members=1,lock=''):
    # =================================================================================
    # =========================== PLAY STOP OR PAUSE ? ================================
    # =================================================================================
    mymodules.PlayStopPause(p_udid, p_name_action)
    # =================================================================================
    # =================================================================================
    # =================================================================================
    try:
        logger.info(f"{p_udid}|||================= STARTING TASK {p_name_action} for Smartphone {p_udid} =========================")

        logger.info(f"{p_udid}|||# ======================== [1] INITIALISATION OF DRIVER ================================")
        driver = Initialisation_Driver(p_name_action, p_udid, p_systemPort, p_deviceName, p_version,p_os)
        logger.info(f"{p_udid}|||The bot will sleep just a few seconds..............................")
        time.sleep(random.uniform(10.9, 15.3))
        driver.implicitly_wait(30)

        # ==================================== WE COMMENT THE Initialisation_Driver BECAUSE WE INITIATE IT IN THE RunSMartphone function
        # ============ and we passed the driver as parameter. So we simply need to startactivity now
        #driver.start_activity("com.instagram.android", "com.instagram.mainactivity.MainActivity")


        logger.info(f"{p_udid}|||# ======================== [2] INITIALISATION OF DATABASE db.db ============================")
        sqliteConnection = sqlite3.connect(mymodules.LoadFile('db.db'))  # we prepare db
        cursor1 = sqliteConnection.cursor()
        logger.info(f"{p_udid}|||INITIALISATION OF DATABASE db.db")

        logger.info(f"{p_udid}|||# ==================== [3] GET INSTA ACCOUNT USERNAME OF THE PHONE =========================")
        #                     We need to know WHO will do the automation tasks
        # ==========================================================================================
        while True:
            # =================================================================================
            # =========================== PLAY STOP OR PAUSE ? ================================
            # =================================================================================
            mymodules.PlayStopPause(p_udid, p_name_action)
            # =================================================================================
            # =================================================================================
            # =================================================================================
            try:
                logger.info(f"{p_udid}|||The bot will sleep just a few seconds..............................")
                time.sleep(random.uniform(8.9, 15.3))
                driver.implicitly_wait(30)
                try_counter=0
                while True:
                    # =================================================================================
                    # =========================== PLAY STOP OR PAUSE ? ================================
                    # =================================================================================
                    mymodules.PlayStopPause(p_udid, p_name_action)
                    # =================================================================================
                    # =================================================================================
                    # =================================================================================
                    try:
                        logger.info(f"{p_udid}|||The bot will sleep just a few seconds..............................")
                        time.sleep(random.uniform(0.9, 2.3))
                        profile_buttons = driver.find_elements_by_id("com.instagram.android:id/profile_tab")
                        logger.info(f"{p_udid}|||len(profile_buttons) = {profile_buttons}")
                        WebDriverWait(driver, 15).until(
                            EC.element_to_be_clickable((By.ID, "com.instagram.android:id/profile_tab")))
                        profile_button = driver.find_element_by_id("com.instagram.android:id/profile_tab")
                        ActionChains(driver).move_to_element(profile_button).perform()
                        profile_button.click()
                        logger.info(f"{p_udid}|||My Profile_button was found!")
                        break
                    except Exception as ex:
                        try_counter+=1
                        logger.error(f"{p_udid}|||{ex} --> We didn't click on my profile page! :-(. Let's try again!")
                        if try_counter > 5:
                            logger.info(f"{p_udid}|||This is the {try_counter} times we tried to tap on 'My profile' icon. Instagram seems to have issue. We need to restart instagram!")
                            driver.quit()
                            logger.info(f"{p_udid}|||The bot will sleep just a few seconds..............................")
                            time.sleep(random.uniform(1.9, 4.3))
                            driver = Initialisation_Driver(p_name_action, p_udid, p_systemPort, p_deviceName, p_version,
                                                           p_os)
                            logger.info(f"{p_udid}|||The bot will sleep just a few seconds..............................")
                            time.sleep(random.uniform(8.9, 16.3))

                logger.info(f"{p_udid}|||We click on Profile button!")
                logger.info(f"{p_udid}|||The bot will sleep just a few seconds..............................")
                time.sleep(random.uniform(5.1, 9.2))
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.ID, "com.instagram.android:id/title_view")))
                myprofile = driver.find_element_by_id("com.instagram.android:id/title_view")
                myprofile_username = myprofile.text
                logger.info(f"{p_udid}|||My profile is : {myprofile_username}.")
                get_id_social_account = True  # We get the Instagram id account, so we change the flag
                break  # Only triggered if input is valid...
            except Exception as ex:

                logger.critical(f"{p_udid}|||{ex} --> We can't click on 'My Profile' icon of Instagram!")
                logger.critical(f"{p_udid}|||{ex} --> Let's try again!")


        # ===================================== GET THE PARAMETERS OF INSTAGRAM ============================================
        logger.info(f"{p_udid}|||# ======= [4] WE GET THE PARAMETERS OF INSTAGRAM BOT for '{myprofile_username}' FROM 'Account details' ON Phonebot.co =============")


        instagram_follow=int(mymodules.GetValueFromCustomField(p_udid,'instagram', myprofile_username, 'instagram_follow'))
        instagram_like_pictures_of_followers=int(mymodules.GetValueFromCustomField(p_udid,'instagram', myprofile_username, 'instagram_like_pictures_of_followers'))
        instagram_like_random_pictures=int(mymodules.GetValueFromCustomField(p_udid,'instagram', myprofile_username, 'instagram_like_random_pictures'))
        instagram_list_hashtags_liking_pictures=mymodules.GetValueFromCustomField(p_udid,'instagram', myprofile_username, 'instagram_list_hashtags_liking_pictures')

        instagram_message=html.unescape(mymodules.GetValueFromCustomField(p_udid,'instagram', myprofile_username, 'instagram_message'))
        instagram_publish_pictures=int(mymodules.GetValueFromCustomField(p_udid,'instagram', myprofile_username, 'instagram_publish_pictures'))
        instagram_scrap_details=int(mymodules.GetValueFromCustomField(p_udid,'instagram', myprofile_username, 'instagram_scrap_details'))

        instagram_send_message=int(mymodules.GetValueFromCustomField(p_udid,'instagram', myprofile_username, 'instagram_send_message'))
        instagram_unfollow=int(mymodules.GetValueFromCustomField(p_udid,'instagram', myprofile_username, 'instagram_unfollow'))
        list_hashtags_publish_pictures=mymodules.GetValueFromCustomField(p_udid,'instagram', myprofile_username, 'list_hashtags_publish_pictures')
        list_of_instagram_influencers_or_competitors=mymodules.GetValueFromCustomField(p_udid,'instagram', myprofile_username, 'list_of_instagram_influencers_or_competitors')
        list_of_labels_pictures=mymodules.GetValueFromCustomField(p_udid,'instagram', myprofile_username, 'list_of_labels_pictures')
        logger.info(f"{p_udid}|||instagram_follow : {instagram_follow} {type(instagram_follow)}")
        logger.info(f"{p_udid}|||instagram_like_pictures_of_followers : {instagram_like_pictures_of_followers} {type(instagram_like_pictures_of_followers)}")
        logger.info(f"{p_udid}|||instagram_like_random_pictures : {instagram_like_random_pictures} {type(instagram_like_random_pictures)}")
        logger.info(f"{p_udid}|||instagram_list_hashtags_liking_pictures : {instagram_list_hashtags_liking_pictures} {type(instagram_list_hashtags_liking_pictures)}")

        logger.info(f"{p_udid}|||instagram_message : {instagram_message} {type(instagram_message)}")
        logger.info(f"{p_udid}|||instagram_publish_pictures : {instagram_publish_pictures} {type(instagram_publish_pictures)}")

        logger.info(f"{p_udid}|||instagram_scrap_details : {instagram_scrap_details} {type(instagram_scrap_details)}")

        logger.info(f"{p_udid}|||instagram_send_message : {instagram_send_message} {type(instagram_send_message)}")
        logger.info(f"{p_udid}|||instagram_unfollow : {instagram_unfollow} {type(instagram_unfollow)}")
        logger.info(f"{p_udid}|||list_hashtags_publish_pictures : {list_hashtags_publish_pictures} {type(list_hashtags_publish_pictures)}")
        logger.info(f"{p_udid}|||list_of_instagram_influencers_or_competitors : {list_of_instagram_influencers_or_competitors} {type(list_of_instagram_influencers_or_competitors)}")
        logger.info(f"{p_udid}|||list_of_labels_pictures : {list_of_labels_pictures} {type(list_of_labels_pictures)}")
        logger.info("# =========================================================================================================")
        # ==============================================================================================================
        driver.implicitly_wait(10)
        logger.info(f"{p_udid}|||The bot will sleep just a few seconds..............................")
        time.sleep(random.uniform(1.9, 3.3))

        logger.info(
            f"{p_udid}|||# ================= [6] WE INITIALISE THE COUNTERS WHICH CAN'T GO OVER THE DAILY LIMIT PARAMETERS =========")
        counter_Instagram_Scrap_profile_details = 0
        counter_Instagram_Scrap_email = 0
        counter_Instagram_Send_message = 0
        counter_Instagram_Like_pics_of_member = 0
        counter_Instagram_Follow_members = 0


        # ============================= WE START THE TASKS FOLLOW OR SCRAP OR MESSAGE IF ONE OF THESE OPTIONS ARE ACTIVATED IN 'Account details'
        if instagram_follow or instagram_scrap_details or instagram_send_message:
            logger.info(f"{p_udid}|||# ======================== [4] GET SOME CONTACTS =================================================")
            #       We need to feed the database table 'contacts' in order to make some actions a bit later
            # ================================================================================================
            logger.info(f"{p_udid}|||# ==================== [4.1] GET THE SOURCE MASTER ACCOUNTS FROM table 'sources' ============")
            # --- We can now extract from table sources, the Master Instagram accounts we want to target
            #master_accounts_tuple = cursor1.execute(
            #    "Select name from sources where status IS NULL and type='followers' and platform='instagram'").fetchall()
            #sqliteConnection.commit()
            logger.info(f"{p_udid}|||master_accounts_tuple: {list_of_instagram_influencers_or_competitors}")
            master_accounts_list = str(list_of_instagram_influencers_or_competitors).split('\\n')

            logger.info(f"{p_udid}|||master_accounts_list: {master_accounts_list}")
            # --- Let's make a break ----
            logger.info(f"{p_udid}|||The bot will sleep just a few seconds..............................")
            time.sleep(random.uniform(2.9, 6.3))
            driver.implicitly_wait(30)

            # ============================================================================================
            #       We have to go slowly. Anyway, this method will be run several times per day and will do
            #       a few tasks per run. So we suppose to get always more contacts than we do tasks
            #       We scroll all the sources in case one source doesn't have contacts for us anymore
            #       This make another problem: the bot will always attack the same source because an
            #       Insta master account will always have new followers, so this method will always have
            #       same source of target contacts (his followers).
            #
            #                          WE LOOP IN THE LIST OF MASTER INSTA ACCOUNTS
            #               We extracted the list of Master Insta Account, lt's loop the list
            # ============================================================================================
            p_bug=False
            for master_account in master_accounts_list:
                
                logger.info(f"{p_udid}|||# ===================== [4.3] WE SEARCH ON INSTAGRAM FOR THIS MASTER ACCOUNT =====================")



                try:
                    insta_account_found, p_bug = Insta_Search(driver, p_udid, master_account, p_bug,lock)
                except:
                    logger.error(f"{p_udid}|||There wasn't any result for the search of {master_account}.")
                    p_bug = True
                    insta_account_found = False


                logger.info(f"{p_udid}|||The bot will sleep just a few seconds..............................")
                time.sleep(random.uniform(2.9, 6.3))
                driver.implicitly_wait(10)
                counter_extract_follower = 0
                if insta_account_found:
                    logger.info(f"{p_udid}|||# =========================== [4.4] DISPLAY LIST OF FOLLOWERS ==============================")
                    #                                We display the list of followers
                    # ====================================================================================================
                    while True:
                        # =================================================================================
                        # =========================== PLAY STOP OR PAUSE ? ================================
                        # =================================================================================
                        mymodules.PlayStopPause(p_udid, p_name_action)
                        # =================================================================================
                        # =================================================================================
                        # =================================================================================
                        try:
                            logger.info(f"{p_udid}|||We will now scrap the usernames of the followers of {master_account}!")
                            driver.implicitly_wait(30)
                            logger.info(f"{p_udid}|||The bot will sleep just a few seconds..............................")
                            time.sleep(random.uniform(2.9, 6.3))
                            cpt=0
                            while True:
                                try:
                                    button_followers = driver.find_element_by_id(
                                        "com.instagram.android:id/row_profile_header_textview_followers_count")
                                    driver.implicitly_wait(30)
                                    button_followers.click()
                                    break
                                except Exception as ex:
                                    if cpt == 3:
                                        logger.critical(f"{p_udid}|||{ex} --> We failed too many times. We guess PhoneBot had issue to display the list of followers. So it started the loop again!")
                                        logger.critical(f"{p_udid}|||{ex} --> So let's make the search again for {master_account}!")
                                        try:
                                            insta_account_found, p_bug = Insta_Search(driver, p_udid, master_account,
                                                                                      p_bug,lock)
                                        except:
                                            logger.error(
                                                f"{p_udid}|||There wasn't any result for the search of {master_account}.")
                                            p_bug = True
                                            insta_account_found = False
                                        break
                                    else:
                                        cpt += 1
                                        logger.critical(
                                            f"{p_udid}|||We failed {cpt} time(s) to click on the 'Followers' counter tab. Let's try again!")


                            driver.implicitly_wait(30)
                            logger.info(f"{p_udid}|||The bot will sleep just a few seconds..............................")
                            time.sleep(random.uniform(1.1, 6.2))
                            logger.info(f"{p_udid}|||# ======================= [4.5] EXTRACT 10 FOLLOWERS ==============================")
                            n = 0 #These 2 variables are necessary to scroll 5 followers by 5 followers
                            x = 5
                            counter_extract_follower = 0
                            WebDriverWait(driver, 30).until(
                                EC.presence_of_element_located((By.ID, "com.instagram.android:id/follow_list_username")))
                            list_followers = driver.find_elements_by_id("com.instagram.android:id/follow_list_username")
                            break
                        except Exception as ex:
                            logger.critical(f"{p_udid}|||{ex} --> Something went wrong when PhoneBot tried to display list of followers of '{master_account}'. Let's try again!")

                    while counter_extract_follower < 11:  # We will scrap only 10 followers
                        # =================================================================================
                        # =========================== PLAY STOP OR PAUSE ? ================================
                        # =================================================================================
                        mymodules.PlayStopPause(p_udid, p_name_action)
                        # =================================================================================
                        # =================================================================================
                        # =================================================================================
                        logger.info(f"{p_udid}|||n = {n}")
                        logger.info(f"{p_udid}|||counter_extract_follower = {counter_extract_follower}")

                        if n == x:  # We work on 5 users of a short list. We need to scroll down and reset the counter 'n'
                            driver.scroll(list_followers[4], list_followers[0])
                            logger.info(f"{p_udid}|||The bot will sleep just a few seconds..............................")
                            time.sleep(random.uniform(1.1, 3.9))
                            driver.implicitly_wait(30)
                            WebDriverWait(driver, 30).until(
                                EC.presence_of_element_located((By.ID, "com.instagram.android:id/follow_list_username")))

                            list_followers = driver.find_elements_by_id("com.instagram.android:id/follow_list_username")
                            n = 0
                            # ======================= [5.6] ADD USERNAME OF FOLLOWER IN TABLE 'contacts' ======================
                            #     We need to add the followers in our table in order to scrap them on next job
                            #     And also because we need first to add in 'contacts' table before to add rows in 'actions' table
                            # =================================================================================================
                        contact = list_followers[n].text
                        if cursor1.execute("select * from contacts where username=? and platform=?",
                                           (contact, 'instagram')).fetchone():
                            logger.info(f"{p_udid}|||Username {contact} already exist in table 'contacts'. We can skip it")

                        else:
                            logger.info(f"{p_udid}|||Username {contact} doesn't exist in table 'contacts'. Let's insert it in table!")
                            cursor1.execute("INSERT INTO contacts (username,platform,source) VALUES (?,?,?)", \
                                            (contact, 'instagram',master_account))
                            sqliteConnection.commit()
                            counter_extract_follower+=1
                        n+=1

                else:
                    logger.critical(f"{p_udid}|||Sorry, we couldn't find this account {master_account}! :-(.   \
                    \nCheck your sources.csv or contact support@phonebot.co.")

                if counter_extract_follower>=10:
                    logger.info(f"{p_udid}|||We extracted 10 contacts and insert them in database, we can go on next task! :-)")
                    break

            logger.info(f"{p_udid}|||# =================================================================================================================")
            logger.info(f"{p_udid}|||#                                        THE COLLECT OF 10 CONTACTS IS FINISHED")
            logger.info(f"{p_udid}|||#                                              NOW, LET'S START THE JOBS")
            logger.info(f"{p_udid}|||# =================================================================================================================")

            logger.info(f"{p_udid}|||The bot will sleep just a few seconds....")
            time.sleep(random.uniform(2.9, 6.3))

            logger.info(f"{p_udid}|||#======== FOLLOW OR SCRAP OR MESSAGE IS ACTIVATED IN 'Account details' =============")

            logger.info(f"{p_udid}|||# =============================== [5] WE PREPARE LIST OF CONTACTS ===================================")
            contacts_tuple = cursor1.execute(
                "SELECT username from contacts WHERE platform='instagram'")
            sqliteConnection.commit()
            logger.info(f"{p_udid}|||contacts_tuple: {contacts_tuple}")
            contacts_list = [item[0] for item in contacts_tuple]
            logger.info(f"{p_udid}|||contacts_list: {contacts_list}")





            logger.info(f"{p_udid}|||# ================= [7] WE INTIALISE THE FLAGS ================================")
            Flag_Instagram_Follow_members = True
            Flag_Instagram_Like_pics_of_member = True
            Flag_Instagram_Send_message = True
            Flag_Instagram_Scrap_profile_details = True
            Flag_Instagram_Scrap_email = True

            scrap_email=False
            scrap_phone=False




            logger.info(f"{p_udid}|||# ========================= [8] WE LOOP IN THE LIST OF contacts ====================================")
            #               We extracted the list of contacts, let's loop the list
            # =====================================================================================================
            #if we want to avoid 2 smartphones pick up same contact, we need to shuffle
            random.shuffle(contacts_list)
            for contact in contacts_list:
                # =================================================================================
                # =========================== PLAY STOP OR PAUSE ? ================================
                # =================================================================================
                mymodules.PlayStopPause(p_udid, p_name_action)
                # =================================================================================
                # =================================================================================
                # =================================================================================
                logger.info(
                    f"{p_udid}|||# ================== [ 8.1] WE INITIALISE 'this_contact_was.....' ====================")

                this_contact_was_scrapped = False
                this_contact_was_followed = False
                this_contact_was_unfollowed = False
                this_contact_was_messaged = False
                this_contact_get_his_pics_liked = False

                this_contact_impossible_picture = False
                this_contact_impossible_message = False

                # =================================================================================================
                logger.info(f"{p_udid}|||# ========= [8.2] LET'S GET THE ID NUMBER OF THIS CONTACT FROM OUR TABLE 'contacts' ==========")
                id_contact=mymodules.Get_ID_from_Username(contact,p_udid,'instagram')
                logger.info(f"{p_udid}|||contact : {contact} and ID : {id_contact}")





                logger.info(
                    f"{p_udid}|||# ================ [8.4] WE CHECK IF PROFILE WAS ALREADY SCRAPPED,FOLLOWED, UNFOLLOWED OR MESSAGED? ===========================")
                print(f"id_contact : {id_contact} - {type(id_contact)}")
                print(f"myprofile_username : {myprofile_username} - {type(myprofile_username)}")
                print(f"contact : {contact} - {type(contact)}")
                if cursor1.execute("SELECT * FROM actions WHERE id_contact=? AND type_action=? AND platform=?",(id_contact,'scrap','instagram')).fetchone():
                    this_contact_was_scrapped= True
                    logger.info(f"{p_udid}|||The contact {contact} - {id_contact} was already scrapped!")
                if cursor1.execute("SELECT * FROM actions WHERE id_contact=? AND type_action=? AND platform=? AND id_social_account=?",(id_contact,'follow_member','instagram',myprofile_username)).fetchone():
                    this_contact_was_followed = True
                    logger.info(f"{p_udid}|||The contact {contact} - {id_contact} was already followed!")
                if cursor1.execute("SELECT * FROM actions WHERE id_contact=? AND type_action=? AND platform=?",(id_contact,'message_sent','instagram')).fetchone():
                    this_contact_was_messaged = True
                    logger.info(f"{p_udid}|||The contact {contact} - {id_contact} received already a message!")
                if cursor1.execute("SELECT * FROM actions where platform=? and type_action=? and id_social_account=? and   \
                                            id_contact=?",('instagram', 'like_picture_profile', myprofile_username, id_contact)).fetchone():
                    this_contact_get_his_pics_liked = True


                if cursor1.execute("SELECT * FROM actions WHERE id_contact=? AND type_action=? AND platform=?",(id_contact,'impossible_message','instagram')).fetchone():
                    this_contact_impossible_message = True
                    logger.info(f"{p_udid}|||The contact {contact} - {id_contact} received already a message!")
                if cursor1.execute("SELECT * FROM actions WHERE id_contact=? AND type_action=? AND platform=?",(id_contact,'impossible_picture','instagram')).fetchone():
                    this_contact_impossible_picture = True
                    logger.info(f"{p_udid}|||The contact {contact} - {id_contact} received already a message!")
                if cursor1.execute(
                        "SELECT * FROM actions WHERE id_contact=? AND type_action=? AND platform=? AND id_social_account=?",
                        (id_contact, 'unfollow', 'instagram', myprofile_username)).fetchone():
                    this_contact_was_unfollowed = True
                    logger.info(f"{p_udid}|||The contact {contact} - {id_contact} was already unfollowed!")




                logger.info(
                    f"{p_udid}|||# ==== [8.5] IF CONTACT WAS NOT ONE OF THE ACTION (follow, msg, scrap) AND ONE OF THE OPTIONS IS ACTIVATED ===========================")
                logger.info(
                    f"{p_udid}|||# ================ WE GO FOR THE TASKS ===========================")

                logger.info(
                    f""""{p_udid}|||# What are the flags for {contact} ?
                ---------------------------------------
                instagram_follow = {instagram_follow}
                this_contact_was_followed = {this_contact_was_followed}
                ---------------------------------------
                instagram_scrap_details  = {instagram_scrap_details}
                this_contact_was_scrapped = {this_contact_was_scrapped}
                ---------------------------------------
                instagram_send_message = {instagram_send_message}
                this_contact_was_messaged = {this_contact_was_messaged}
                this_contact_impossible_message = {this_contact_impossible_message}
                ---------------------------------------
                instagram_like_pictures_of_followers = {instagram_like_pictures_of_followers}
                this_contact_impossible_picture = {this_contact_impossible_picture}
                this_contact_get_his_pics_liked = {this_contact_get_his_pics_liked}
                ---------------------------------------
                instagram_unfollow = {instagram_unfollow}
                this_contact_was_unfollowed = {this_contact_was_unfollowed}
                ---------------------------------------
                """)

                if (instagram_follow and not this_contact_was_followed and not this_contact_was_unfollowed) or (instagram_scrap_details and not this_contact_was_scrapped)  \
                        or (instagram_send_message and not this_contact_was_messaged and not this_contact_impossible_message) \
                        or (instagram_like_pictures_of_followers and not this_contact_impossible_picture and not this_contact_get_his_pics_liked):
                    logger.info(
                        f"instagram_follow and not this_contact_was_followed and not this_contact_was_unfollowed : {instagram_follow and not this_contact_was_followed and not this_contact_was_unfollowed}")
                    logger.info(
                        f"instagram_scrap_details and not this_contact_was_scrapped : {instagram_scrap_details and not this_contact_was_scrapped}")
                    logger.info(
                        f"instagram_send_message and not this_contact_was_messaged and not this_contact_impossible_message : {instagram_send_message and not this_contact_was_messaged and not this_contact_impossible_message}")
                    logger.info(
                        f"instagram_like_pictures_of_followers and not this_contact_impossible_picture and not this_contact_get_his_pics_liked : {instagram_like_pictures_of_followers and not this_contact_impossible_picture and not this_contact_get_his_pics_liked}")

                    logger.info(f"{p_udid}|||# ================ [8.5.1] WE SEARCH FOR CONTACT PROFILE PAGE ===========================")

                    try:
                        insta_account_found, p_bug = Insta_Search(driver, p_udid, contact, p_bug,lock)
                    except:
                        logger.error(f"{p_udid}|||There wasn't any result for the search of {contact}.")
                        p_bug = True
                        insta_account_found = False

                    logger.info(f" =============== p_bug : {p_bug} ************************")
                    logger.info(f"{p_udid}|||The bot will sleep just a few seconds..............................")
                    time.sleep(random.uniform(2.9, 6.3))
                    driver.implicitly_wait(30)
                    logger.info(f"{p_udid}|||# ================ [8.5.2] IF WE FOUND THE CONTACT, WE DO THE TASKS ======================")
                    if insta_account_found:
                        logger.info(f"{p_udid}|||VERIFICATION 1 CORRECT => Function 'Insta_Search found the contact '{contact}'. :-)")
                        if instagram_follow == 1:
                            logger.info(f"{p_udid}|||VERIFICATION 2 CORRECT => The feature 'follow' is activated in 'Account details' on Phonebot.co")
                            if counter_Instagram_Follow_members < p_Daily_limit_Instagram_Follow_members:
                                logger.info(f"{p_udid}|||VERIFICATION 3 CORRECT => PhoneBot didn't reach the limit yet for the task 'follow'")
                                if not this_contact_was_followed:
                                    logger.info(f"{p_udid}|||VERIFICATION 4 CORRECT => This contact was not followed")
                                    if Flag_Instagram_Follow_members :
                                        logger.info(f"{p_udid}|||VERIFICATION 5 CORRECT => Flag_Instagram_Follow_members is TRUE")
                                        # =================================================================================
                                        # =========================== PLAY STOP OR PAUSE ? ================================
                                        # =================================================================================
                                        mymodules.PlayStopPause(p_udid, p_name_action)
                                        # =================================================================================
                                        # =================================================================================
                                        # =================================================================================
                                        if p_Daily_limit_Instagram_Follow_members !=0:
                                            logger.info(
                                                f"{p_udid}|||# ================ [8.5.2.1] WE FOLLOW THE CONTACT  =================")
                                            # =================================================================================================

                                            logger.info(f"{p_udid}|||We will follow '{contact}' because 'Instagram_Follow_members' = True")

                                            logger.info(f"{p_udid}|||# ============ [8.5.2.1.1] WE SEARCH THE BUTTON FOLLOW IN ENGLISH OR IN FRENCH =================")
                                            # ============ AND WE FOLLOW THIS CONTACT ==================================================
                                            try:
                                                try:
                                                    logger.info(
                                                        f"{p_udid}|||Let's search for the French button 'S'abonner'.")

                                                    # =================== S abonner ============================

                                                    follow_button = driver.find_element(By.XPATH,
                                                                                        "//android.widget.TextView[@text='S’abonner']")
                                                    logger.info(
                                                        f"{p_udid}|||Button 'S abonner' was found!")
                                                    follow_button.click()
                                                    logger.info(
                                                        f"{p_udid}|||We found the button 'S abonner', we clicked on it! :-)")
                                                    counter_Instagram_Follow_members += 1
                                                    follow_member = True
                                                    now = datetime.now()
                                                    date_n_time = str(
                                                        now.strftime("%d/%m/%Y %H:%M:%S"))
                                                    with lock:
                                                        cursor1.execute(
                                                            "INSERT INTO actions (platform,type_action,date,id_smartphone,id_social_account,id_contact) VALUES (?,?,?,?,?,?)",
                                                            ('instagram', 'follow_member',
                                                             date_n_time, p_udid,
                                                             myprofile_username,
                                                             id_contact))
                                                        sqliteConnection.commit()
                                                    logger.info(
                                                        f"{p_udid}|||We insert a row 'follow_member' in table 'actions' for {contact}.")


                                                except:
                                                    try:
                                                        logger.info(
                                                            f"{p_udid}|||There is not the button 'S'Abonner'. Let's search for the english button 'Follow'.")

                                                        # =================== Follow ============================

                                                        follow_button = driver.find_element(By.XPATH,
                                                                                            "//android.widget.TextView[@text='Follow']")
                                                        logger.info(
                                                            f"{p_udid}|||Button 'Follow' was found.")
                                                        follow_button.click()
                                                        logger.info(
                                                            f"{p_udid}|||We found the button 'Follow', we clicked on it! :-)")
                                                        counter_Instagram_Follow_members += 1
                                                        follow_member = True


                                                        now = datetime.now()
                                                        date_n_time = str(
                                                            now.strftime("%d/%m/%Y %H:%M:%S"))
                                                        with lock:
                                                            cursor1.execute(
                                                                "INSERT INTO actions (platform,type_action,date,id_smartphone,id_social_account,id_contact) VALUES (?,?,?,?,?,?)",
                                                                ('instagram', 'follow_member',
                                                                 date_n_time, p_udid,
                                                                 myprofile_username,
                                                                 id_contact))
                                                            sqliteConnection.commit()
                                                        logger.info(
                                                            f"{p_udid}|||We insert a row 'follow_member' in table 'actions' for {contact}.")

                                                    except:
                                                        try:
                                                            logger.info(
                                                                f"{p_udid}|||There is not the button 'Follow'. Let's search for the english button 'Following' in case we already Follow {contact} but we didn't update the table.")
                                                            follow_buttons = driver.find_element(By.XPATH,
                                                                                                       "//android.widget.TextView[@text='Following']")
                                                            # =================== Following ============================
                                                            logger.info(f"{p_udid}|||Button 'Following' was found.")
                                                            logger.info(
                                                                f"{p_udid}|||We found the button 'Following'.That means we already followed {contact}. Let's INSERT the row in database table 'actions'.")
                                                            now = datetime.now()
                                                            date_n_time = str(now.strftime("%d/%m/%Y %H:%M:%S"))
                                                            with lock:
                                                                cursor1.execute("INSERT INTO actions (platform,type_action,date,id_smartphone,id_social_account,id_contact) VALUES (?,?,?,?,?,?)",
                                                                                ('instagram', 'follow_member',
                                                                                 date_n_time, p_udid,
                                                                                 myprofile_username, id_contact))
                                                                sqliteConnection.commit()
                                                            logger.info(
                                                                f"{p_udid}|||We insert a row 'follow_member' in table 'actions' for {contact}.")
                                                        except:
                                                            try:
                                                                logger.info(
                                                                    f"{p_udid}|||There is not the button 'Following'. Let's search for the French button 'Abonné(e)' in case we already Follow {contact} but we didn't update the table.")
                                                                follow_button = driver.find_element(By.XPATH,
                                                                                                     "//android.widget.TextView[@text='Abonné(e)']")

                                                                # =================== Abonné(e) ============================
                                                                logger.info(f"{p_udid}|||Button 'Abonné(e)' was found.")
                                                                logger.info(
                                                                    f"{p_udid}|||We found the button 'Abonné(e)'.That means we already followed {contact}. Let's INSERT the row in database table 'actions'.")
                                                                now = datetime.now()
                                                                date_n_time = str(now.strftime("%d/%m/%Y %H:%M:%S"))
                                                                with lock:
                                                                    cursor1.execute("INSERT INTO actions (platform,type_action,date,id_smartphone,id_social_account,id_contact) VALUES (?,?,?,?,?,?)",
                                                                                    ('instagram', 'follow_member',
                                                                                     date_n_time,
                                                                                     p_udid,
                                                                                     myprofile_username, id_contact))
                                                                    sqliteConnection.commit()
                                                                    cursor1.execute(
                                                                        "INSERT INTO actions (platform,type_action,date,id_smartphone,id_social_account,id_contact) VALUES (?,?,?,?,?,?)",
                                                                        ('instagram', 'like_picture_profile', date_n_time,
                                                                         p_udid,
                                                                         myprofile_username, id_contact))
                                                                    sqliteConnection.commit()
                                                                logger.info(
                                                                    f"{p_udid}|||We insert a row 'follow_member' and a row 'like_picture_profile' in table 'actions' for {contact}.")

                                                            except:
                                                                try:


                                                                    logger.info(
                                                                        f"{p_udid}|||There is not the button 'Abonnée'. Let's search for the english button 'Requested'")
                                                                    follow_buttons = driver.find_element(By.XPATH,
                                                                                                         "//android.widget.TextView[@text='Requested']")
                                                                    # =================== Requested ============================
                                                                    logger.info(
                                                                        f"{p_udid}|||Button 'Requested' was found.")
                                                                    logger.info(
                                                                        f"{p_udid}|||We found the button 'Requested'.That means we already followed {contact}. Let's INSERT the row in database table 'actions'.")
                                                                    now = datetime.now()
                                                                    date_n_time = str(now.strftime("%d/%m/%Y %H:%M:%S"))
                                                                    with lock:
                                                                        cursor1.execute(
                                                                            "INSERT INTO actions (platform,type_action,date,id_smartphone,id_social_account,id_contact) VALUES (?,?,?,?,?,?)",
                                                                            ('instagram', 'follow_member', date_n_time,
                                                                             p_udid,
                                                                             myprofile_username, id_contact))
                                                                        sqliteConnection.commit()

                                                                        cursor1.execute(
                                                                            "INSERT INTO actions (platform,type_action,date,id_smartphone,id_social_account,id_contact) VALUES (?,?,?,?,?,?)",
                                                                            ('instagram', 'like_picture_profile', date_n_time,
                                                                             p_udid,
                                                                             myprofile_username, id_contact))
                                                                        sqliteConnection.commit()
                                                                    logger.info(
                                                                        f"{p_udid}|||We insert a row 'follow_member' and a row 'like_picture_profile' in table 'actions' for {contact}.")
                                                                except:
                                                                    try:
                                                                        logger.info(
                                                                            f"{p_udid}|||There is not the button 'Abonnée'. Let's search for the english button 'Deamnde envoyée'")

                                                                        follow_buttons = driver.find_element(By.XPATH,
                                                                                                             "//android.widget.TextView[@text='Demande envoyée']")
                                                                        # =================== Demande envoyée ============================
                                                                        logger.info(
                                                                            f"{p_udid}|||Button 'Demande envoyée' was found.")
                                                                        logger.info(
                                                                            f"{p_udid}|||We found the button 'Demande envoyée'. That means we already followed {contact}. Let's update database.")
                                                                        now = datetime.now()
                                                                        date_n_time = str(
                                                                            now.strftime("%d/%m/%Y %H:%M:%S"))
                                                                        with lock:
                                                                            cursor1.execute(
                                                                                "INSERT INTO actions (platform,type_action,date,id_smartphone,id_social_account,id_contact) VALUES (?,?,?,?,?,?)",
                                                                                ('instagram', 'follow_member',
                                                                                 date_n_time, p_udid,
                                                                                 myprofile_username, id_contact))
                                                                            sqliteConnection.commit()

                                                                            # We INSERT the row 'like_picture_profile' because for 'Requested' people, we will never be able to like pics. So it is a way to skip them for next loop
                                                                            cursor1.execute(
                                                                                "INSERT INTO actions (platform,type_action,date,id_smartphone,id_social_account,id_contact) VALUES (?,?,?,?,?,?)",
                                                                                ('instagram', 'like_picture_profile', date_n_time,
                                                                                 p_udid,
                                                                                 myprofile_username, id_contact))
                                                                            sqliteConnection.commit()
                                                                        logger.info(
                                                                            f"{p_udid}|||We insert a row 'follow_member' and a row 'like_picture_profile' in table 'actions' for {contact}.")


                                                                    except:

                                                                        logger.info(
                                                                            f"{p_udid}|||We didn't find anything. Let' create an error in order to exit this task.")
                                                                        follow_button = driver.find_element(By.XPATH,
                                                                                                              "//android.widget.TextView[@text='Follow']")


                                            except Exception as ex:
                                                logger.info(f"{p_udid}|||{ex} --> We couldn't find the button 'Follow'. So we skip the task Follow for this profile '{contact}!")

                                    else:
                                        logger.info(
                                            f"{p_udid}|||VERIFICATION 5 FAILED => Flag_Instagram_Follow_members is FALSE")

                                else:
                                    logger.info(
                                        f"{p_udid}|||VERIFICATION 4 FAILED => This contact was already followed")

                            else:
                                logger.info(f"{p_udid}|||VERIFICATION 3 FAILED => PhoneBot reach the limit yet for this task")
                                logger.info(
                                    f"{p_udid}|||counter_Instagram_Follow_members : {counter_Instagram_Follow_members}/{p_Daily_limit_Instagram_Follow_members}")
                                Flag_Instagram_Follow_members = False

                        else:
                            logger.info(f"{p_udid}|||VERIFICATION 2 FAILED => The feature 'follow' is NOT activated in 'Account details' on Phonebot.co")
                            Flag_Instagram_Follow_members=False

                        logger.info(f"{p_udid}|||The bot will sleep just a few seconds..............................")
                        time.sleep(random.uniform(2.9, 6.3))

                        if p_Daily_limit_Instagram_Like_pics_of_member != 0:


                            like_pics=False
                            if instagram_like_pictures_of_followers == 1:
                                logger.info(
                                    f"{p_udid}|||VERIFICATION 2 CORRECT => The feature 'like_picture_profile' is activated in 'Account details' on Phonebot.co")

                                if counter_Instagram_Like_pics_of_member < p_Daily_limit_Instagram_Like_pics_of_member:
                                    logger.info(
                                        f"{p_udid}|||VERIFICATION 3 CORRECT => PhoneBot didn't reach the limit yet for the task 'like_picture_profile'")

                                    if not this_contact_get_his_pics_liked:
                                        logger.info(f"{p_udid}|||VERIFICATION 4 CORRECT => {myprofile_username} didn't like yet the pics of {contact}.")

                                        if Flag_Instagram_Like_pics_of_member :
                                            logger.info(
                                                f"{p_udid}|||VERIFICATION 5 CORRECT => Flag_Instagram_Like_pics_of_member is TRUE")
                                            if not this_contact_impossible_picture:
                                                logger.info(
                                                    f"{p_udid}|||VERIFICATION 6 CORRECT => this_contact_impossible_picture is FALSE")
                                                # =================================================================================
                                                # =========================== PLAY STOP OR PAUSE ? ================================
                                                # =================================================================================
                                                mymodules.PlayStopPause(p_udid, p_name_action)
                                                # =================================================================================
                                                # =================================================================================
                                                # =================================================================================

                                                # =================================================================================================
                                                logger.info(
                                                    f"{p_udid}|||# ======= [8.5.2.2] WE LIKE SOME PICS OF THIS CONTACTS, IF Instagram_Like_pics_of_member = True =======")
                                                # =================================================================================================

                                                logger.info(f"{p_udid}|||We will like pics of '{contact}' because 'Instagram_Like_pics_of_member' = True")
                                                logger.info(f"{p_udid}|||# ========================= [8.5.2.2.1] WE NEED TO CHECK IF THERE IS A GALLERY OR NOT ==========")
                                                gallery_empty = driver.find_elements_by_id("com.instagram.android:id/empty_state_view_title")
                                                if len(gallery_empty) != 0:
                                                    logger.error(f"{p_udid}|||There is no gallery of pics, we can go for next task!")

                                                else:


                                                    logger.info(f"{p_udid}|||# ============================ [8.5.2.2.2] WE SCROLL ============================")
                                                    #driver.scroll(profile_icon, avatar_profile)
                                                    Scroll_up_profile(driver,p_udid)
                                                    gallery_pics = driver.find_elements_by_xpath("//*[@class='android.widget.ImageView' and contains(@content-desc, 'hoto')]")
                                                    logger.info(f"{p_udid}|||len(gallery_pics) : {len(gallery_pics)}")
                                                    if len(gallery_pics) <1:
                                                        logger.info(f"{p_udid}|||There isn't any pictures to like!")
                                                        logger.error(
                                                            f"{p_udid}|||We couldn't like picture of '{contact}' because there si no 'gallery' .")
                                                        logger.error(
                                                            f"{p_udid}|||We will add a row in table 'actions' = >'impossible_picture' in order to skip him next time.")
                                                        now = datetime.now()
                                                        date_n_time = str(now.strftime("%d/%m/%Y %H:%M:%S"))
                                                        with lock:
                                                            cursor1.execute("INSERT INTO actions (platform,type_action,date,id_smartphone,id_social_account,id_contact) VALUES (?,?,?,?,?,?)",
                                                                            ('instagram', 'impossible_picture', date_n_time, p_udid,
                                                                             myprofile_username, id_contact))
                                                            sqliteConnection.commit()
                                                        logger.info(
                                                            f"{p_udid}|||# ======= [8.5.2.4] WE INSERT IN TABLE ACTIONS FOR TASK 'impossible_picture' ============")
                                                    else:
                                                        # =================================================================================
                                                        # =========================== PLAY STOP OR PAUSE ? ================================
                                                        # =================================================================================
                                                        mymodules.PlayStopPause(p_udid, p_name_action)
                                                        # =================================================================================
                                                        # =================================================================================
                                                        # =================================================================================
                                                        cpt=0
                                                        click_on_pic = False
                                                        while True:
                                                            try:
                                                                logger.info(
                                                                    f"{p_udid}|||# ======================= [8.5.2.2.5] WE CLICK ON FIRST PIC ==============================")
                                                                gallery_pics[1].click()
                                                                logger.info(
                                                                    "The bot will sleep just a few seconds..............................")
                                                                driver.implicitly_wait(10)
                                                                time.sleep(random.uniform(1.1, 2.3))
                                                                try:
                                                                    buttons_like=driver.find_element_by_id("com.instagram.android:id/row_feed_button_like")
                                                                    logger.info(
                                                                        "The bot will sleep just a few seconds..............................")
                                                                    click_on_pic = True
                                                                    break
                                                                except:
                                                                        logger.info("We didn't find the 'Like' button. Let's scroll down a bit")
                                                                        Scroll_up_pic(driver,p_udid)  # We need to move up a bit the pic for seeing the Like button
                                                                        buttons_like = driver.find_element_by_id("com.instagram.android:id/row_feed_button_like")
                                                                        logger.info(
                                                                            f"{p_udid}|||We click on first pic! :-)")
                                                                        click_on_pic = True
                                                                        break
                                                            except Exception as ex:
                                                                cpt+=1
                                                                logger.error(f"{p_udid}|||{ex} --> We didn't click on picture 1! :-(. Let's try again!")
                                                                if cpt>3:
                                                                    break
                                                                    click_on_pic=False
                                                        time.sleep(random.uniform(1.9, 3.3))
                                                                    #--- =======================================================================

                                                        # =================================================================================
                                                        # =========================== PLAY STOP OR PAUSE ? ================================
                                                        # =================================================================================
                                                        mymodules.PlayStopPause(p_udid, p_name_action)
                                                        # =================================================================================
                                                        # =================================================================================
                                                        # =================================================================================
                                                        if click_on_pic:
                                                            logger.info(f"{p_udid}|||# ================== [8.5.2.2.6] WE LIKE THE FIRST PIC ==================")
                                                            cpt=0
                                                            while True:
                                                                try:
                                                                    logger.info(f"{p_udid}|||The bot will sleep just a few seconds..............................")
                                                                    time.sleep(random.uniform(1.9, 5.3))
                                                                    driver.implicitly_wait(10)
                                                                    driver.find_element_by_id("com.instagram.android:id/row_feed_button_like").click()
                                                                    logger.info(f"{p_udid}|||We like the first pic! :-)")
                                                                    counter_Instagram_Like_pics_of_member += 1
                                                                    like_pics = True
                                                                    break
                                                                except Exception as ex:
                                                                    cpt+=1
                                                                    logger.critical(f"We couldn't like the first pic! Let's try again!")
                                                                    if cpt>3:
                                                                        break
                                                        # ================================== WE COME BACK TO GALLERY ==================================
                                                        # --- If we see the profile name in the header,it means we are still in picture page
                                                        if len(driver.find_elements_by_id("com.instagram.android:id/row_feed_photo_profile_name"))!= 0 :
                                                            while True:
                                                                try:
                                                                    logger.info(f"{p_udid}|||The bot will sleep just a few seconds..............................")
                                                                    logger.info(
                                                                        f"{p_udid}|||The bot will sleep just a few seconds..............................")
                                                                    time.sleep(random.uniform(1.9, 5.3))
                                                                    driver.implicitly_wait(10)
                                                                    # --- Let's come back to gallery
                                                                    button_back = driver.find_element_by_id("com.instagram.android:id/row_feed_photo_profile_name")
                                                                    #ActionChains(driver).move_to_element(button_back).perform()
                                                                    button_back.click()
                                                                    driver.implicitly_wait(10)
                                                                    logger.info(f"{p_udid}|||The bot will sleep just a few seconds..............................")
                                                                    time.sleep(random.uniform(1.9, 3.3))
                                                                    logger.info(f"{p_udid}|||We came back to profile! :-)")
                                                                    break
                                                                except Exception as ex:
                                                                    logger.critical(f"{p_udid}|||{ex} --> We couldn't come back to the profile! Let's try again!")
                                                                    # BACK BUTTON METHOD
                                                                    GoBackButtonInstagram(driver, p_udid)
                                                                    break

                                            else:
                                                logger.info(
                                                    f"{p_udid}|||VERIFICATION 6 FAILED => this_contact_impossible_picture is TRUE")

                                        else:
                                            logger.info(
                                                f"{p_udid}|||VERIFICATION 5 FAILED => Flag_Instagram_Like_pics_of_member is FALSE")
                                    else:
                                        logger.info(f"{p_udid}|||VERIFICATION 4 FAILED => {myprofile_username} already liked some pics of {contact}.")
                                else:
                                    logger.info(
                                        f"{p_udid}|||VERIFICATION 3 FAILED => PhoneBot reach the limit yet for the task 'like_pics'")
                                    logger.info(f"{p_udid}|||counter_Instagram_Like_pics_of_member : {counter_Instagram_Like_pics_of_member}/{p_Daily_limit_Instagram_Like_pics_of_member} ")
                                    Flag_Instagram_Like_pics_of_member = False
                            else:
                                logger.info(
                                    f"{p_udid}|||VERIFICATION 2 FAILED => The feature 'like_pics' is NOT activated in 'Account details' on Phonebot.co")
                                Flag_Instagram_Like_pics_of_member=False
                            #===========================================================================================================
                            if like_pics:
                                now = datetime.now()
                                date_n_time = str(now.strftime("%d/%m/%Y %H:%M:%S"))
                                with lock:
                                    cursor1.execute("INSERT INTO actions (platform,type_action,date,id_smartphone,id_social_account,id_contact)  \
                                                                           VALUES (?,?,?,?,?,?)",
                                                    ('instagram', 'like_picture_profile', date_n_time, p_udid,
                                                     myprofile_username, id_contact))
                                    logger.info(
                                        f"{p_udid}|||# ======= [8.5.2.3] WE INSERT IN TABLE ACTIONS FOR TASK 'like_pics' ============")

                                    sqliteConnection.commit()













                        logger.info(f"{p_udid}|||The bot will sleep just a few seconds..............................")
                        time.sleep(random.uniform(2.9, 6.3))
                        message_sent=False


                        if p_Daily_limit_Instagram_Send_message!=0:

                            if instagram_send_message == 1:
                                logger.info(
                                    f"{p_udid}|||VERIFICATION 2 CORRECT => The feature 'send_message' is activated in 'Account details' on Phonebot.co")

                                if not this_contact_was_messaged:
                                    logger.info(f"{p_udid}|||VERIFICATION 3 CORRECT => This contact didn't receive a message yet.")

                                    if counter_Instagram_Send_message < p_Daily_limit_Instagram_Send_message:
                                        logger.info(
                                            f"{p_udid}|||VERIFICATION 4 CORRECT => PhoneBot didn't reach the limit yet for the task 'send_message'.")

                                        if Flag_Instagram_Send_message :
                                            logger.info(
                                                f"{p_udid}|||VERIFICATION 5 CORRECT => Flag_Instagram_Send_message is TRUE")
                                            if not this_contact_impossible_message:
                                                logger.info(
                                                    f"{p_udid}|||VERIFICATION 6 CORRECT => this_contact_impossible_message is FALSE")
                                                # =================================================================================
                                                # =========================== PLAY STOP OR PAUSE ? ================================
                                                # =================================================================================
                                                mymodules.PlayStopPause(p_udid, p_name_action)
                                                # =================================================================================
                                                # =================================================================================
                                                # =================================================================================
                                                # =================================================================================================
                                                logger.info(
                                                    f"{p_udid}|||# ======================= [8.5.2.4] WE SEND A DIRECT MESSAGE =========================")
                                                # =================================================================================================

                                                logger.info(f"{p_udid}|||We will send message to '{contact}' because 'Instagram_Send_message' = True")
                                                # --- 1rst, we need to format the message with the function random_abc()
                                                # --- in order to create various messages and NOT always the same

                                                logger.info(
                                                    f"{p_udid}|||# ======================= [8.5.2.4.1] WE PREPARE THE MESSAGE ==================")

                                                insta_msg = instagram_message
                                                insta_msg = mymodules.random_abc(insta_msg)
                                                print(f"instagram_message:{instagram_message}")
                                                print (f"insta_msg : {insta_msg}")
                                                # --- Now we have issue with ActionChains and '\n' if we want to write a text with several lines
                                                # --- So we will transform the '\n' in '|' and say to our method send_keys_delay_random_instagram
                                                # to replace the \n by | and make a new line for each |
                                                insta_msg = str(insta_msg)

                                                insta_msg = insta_msg.replace('{username}', contact).replace('\\n', '|').replace('{firstname}', contact)
                                                insta_msg = unidecode.unidecode(insta_msg)  # we remove haracters with accent

                                                # ==============================================================================================
                                                logger.info(
                                                    f"{p_udid}|||# =============== [8.5.2.4.2] First we need to check if message was already sent to this user ===========")
                                                # ==============================================================================================
                                                if cursor1.execute("SELECT * from actions where id_contact=? and platform=? and type_action=? and message=?",
                                                                   (id_contact, 'instagram', 'message_sent', insta_msg)).fetchone():
                                                    logger.error(f"{p_udid}|||This message was already sent to '{contact}'' . We will skip it!")

                                                else:
                                                    logger.info(
                                                        f"User '{contact}' never received this message. We can send it to him/her!")

                                                    # --- Ok, the message is ready, let's search for the button "Write" and send the message
                                                    try:
                                                        try:
                                                            button_write_message = driver.find_element(By.XPATH,
                                                                                                        "//android.widget.TextView[@text='Écrire']")

                                                            print("button_write_message was found!")
                                                            button_write_message.click()
                                                        except:
                                                            try:
                                                                button_write_message = driver.find_element(By.XPATH,
                                                                                                            "//android.widget.TextView[@text='Message']")

                                                                print("button_write_message was found!")
                                                                button_write_message.click()
                                                            except:

                                                                logger.error(f"{p_udid}|||We couldn't send a message to '{contact}' because there si no 'message' button.")
                                                                logger.error(
                                                                    f"{p_udid}|||We will add a row in table 'actions' = >'impossible_message' in order to skip him next time.")
                                                                now = datetime.now()
                                                                date_n_time = str(now.strftime("%d/%m/%Y %H:%M:%S"))
                                                                with lock:
                                                                    cursor1.execute("INSERT INTO actions (platform,type_action,date,id_smartphone,id_social_account,id_contact)  \
                                                                                                                                       VALUES (?,?,?,?,?,?)",
                                                                                    ('instagram', 'impossible_message', date_n_time, p_udid,
                                                                                     myprofile_username, id_contact,master_account))
                                                                    sqliteConnection.commit()
                                                                logger.info(
                                                                    f"{p_udid}|||# ======= [8.5.2.4] WE INSERT IN TABLE ACTIONS FOR TASK 'impossible_message' ============")







                                                        driver.implicitly_wait(30)
                                                        logger.info(f"{p_udid}|||The bot will sleep just a few seconds..............................")
                                                        time.sleep(random.uniform(1.9, 3.3))
                                                        # --- We can now send the message
                                                        message_field = driver.find_element_by_id(
                                                            "com.instagram.android:id/row_thread_composer_edittext")
                                                        message_field.click()

                                                        logger.info(f"{p_udid}|||The bot will sleep just a few seconds..............................")
                                                        time.sleep(random.uniform(1.9, 3.3))
                                                        # =================================================================================
                                                        # =========================== PLAY STOP OR PAUSE ? ================================
                                                        # =================================================================================
                                                        mymodules.PlayStopPause(p_udid, p_name_action)
                                                        # =================================================================================
                                                        # =================================================================================
                                                        # =================================================================================

                                                        logger.info(
                                                            f"{p_udid}|||# ======================= [8.5.2.4.3] SENDING MESSAGE =======================================")
                                                        logger.info(f"{p_udid}|||p_bug : {p_bug}")
                                                        print (
                                                            f"PhoneBot will send Instagram message through smartphone N° {p_udid}")
                                                        
                                                        p_bug = mymodules.send_keys_message_delay_random('Instagram',driver, message_field, insta_msg,p_bug, 0.5, 0.75,300,p_udid)


                                                        # ======================================================================================
                                                        # The message was typed, we can click on send button ------------------
                                                        logger.info(f"{p_udid}|||The bot will sleep just a few seconds..............................")
                                                        time.sleep(random.uniform(0.8, 3.3))
                                                        insta_send_msg_button = driver.find_element_by_id(
                                                            "com.instagram.android:id/row_thread_composer_button_send")
                                                        insta_send_msg_button.click()
                                                        logger.info(f"{p_udid}|||The bot will sleep just a few seconds..............................")
                                                        time.sleep(random.uniform(3.8, 6.3))
                                                        driver.implicitly_wait(15)
                                                        counter_Instagram_Send_message += 1
                                                        message_sent = True
                                                        logger.info(
                                                            f"{p_udid}|||# =========== [8.5.2.4.4] WE UPDATE DATABASE TO INSERT 'message_sent' IN 'actions' table =========")
                                                        now = datetime.now()
                                                        date_n_time = str(now.strftime("%d/%m/%Y %H:%M:%S"))
                                                        with lock:
                                                            cursor1.execute("INSERT INTO actions (platform,type_action,date,message,id_smartphone,id_social_account,id_contact)  \
                                                                                                                                                                    VALUES (?,?,?,?,?,?,?)",
                                                                            (
                                                                            'instagram', 'message_sent', date_n_time, insta_msg,
                                                                            p_udid,
                                                                            myprofile_username, id_contact))
                                                            sqliteConnection.commit()
                                                        logger.info(
                                                            f"{p_udid}|||The bot will sleep just a few seconds..............................")
                                                        time.sleep(random.uniform(2.2, 4.3))
                                                        # ---- We need to come back to profile page
                                                        # driver.find_element_by_id("com.instagram.android:id/action_bar_button_back").click()

                                                        # We need to go back to profile page ---------------------------------

                                                        # =================================================================================
                                                        # =========================== PLAY STOP OR PAUSE ? ================================
                                                        # =================================================================================
                                                        mymodules.PlayStopPause(p_udid, p_name_action)
                                                        # =================================================================================
                                                        # =================================================================================
                                                        # =================================================================================


                                                        # BACK BUTTON METHOD
                                                        GoBackButtonInstagram(driver, p_udid)

                                                        # CLICK ON USERNAME METHOD 1
                                                        # 1rst we need to scroll up in case the picture was too height and we scrolled down
                                                        mymodules.Scroll_Up(driver, p_udid)
                                                        try:
                                                            username_button = driver.find_element_by_id("com.instagram.android:id/thread_title")
                                                            logger.info(
                                                                f"{p_udid}|||We found the username head bar in message frame. Let's click on it!")
                                                            username_button.click()
                                                        except:
                                                            logger.info(
                                                                f"{p_udid}|||We couldn't find the username head bar in message frame. :-(")



                                                        # CLICK ON USERNAME METHOD 2
                                                        # 1rst we need to scroll up in case the picture was too height and we scrolled down
                                                        mymodules.Scroll_Up(driver,p_udid)
                                                        try:
                                                            username_button = driver.find_element_by_id("com.instagram.android:id/row_feed_photo_profile_name")
                                                            logger.info(
                                                                f"{p_udid}|||We found the username head bar. Let's click on it!")
                                                            username_button.click()

                                                        except:
                                                            logger.info(
                                                                f"{p_udid}|||We couldn't find the username head bar. :-(")





                                                        # ---------------------------------------------------------------------
                                                        logger.info(f"{p_udid}|||The bot will sleep just a few seconds..............................")
                                                        time.sleep(random.uniform(1.8, 3.3))


                                                    except Exception as ex:
                                                        logger.error(f"{p_udid}|||{ex} --> We couldn't send a message to '{contact}'. We go for next task.")

                                            else:
                                                logger.info(
                                                    f"{p_udid}|||VERIFICATION 6 FAILED => this_contact_impossible_message is TRUE")

                                        else:
                                            logger.info(
                                                f"{p_udid}|||VERIFICATION 5 FAILED => Flag_Instagram_Send_message is FALSE")
                                    else:
                                        logger.info(
                                            f"{p_udid}|||VERIFICATION 4 FAILED => PhoneBot reach the limit yet for the task 'send_msg'.")

                                        Flag_Instagram_Send_message = False

                                else:
                                    logger.info(
                                        f"{p_udid}|||VERIFICATION 3 FAILED => This contact already received a message.")

                            else:

                                logger.info(
                                    f"{p_udid}|||VERIFICATION 2 FAILED => The feature 'send_msg' is NOT activated in 'Account details' on Phonebot.co")
                                Flag_Instagram_Send_message=False

                        # =================================================================================
                        # =========================== PLAY STOP OR PAUSE ? ================================
                        # =================================================================================
                        mymodules.PlayStopPause(p_udid, p_name_action)
                        # =================================================================================
                        # =================================================================================
                        # =================================================================================

                        logger.info(
                            f"{p_udid}|||counter_Instagram_Send_message : {counter_Instagram_Send_message}/{p_Daily_limit_Instagram_Send_message}")

                        logger.info(f"{p_udid}|||The bot will sleep just a few seconds..............................")
                        time.sleep(random.uniform(2.9, 6.3))
                        driver.implicitly_wait(15)
                        scrap_profile=False
                        email_contact = ''
                        phone_number=''





                        if p_Daily_limit_Instagram_Scrap_profile_details!=0:

                            if instagram_scrap_details == 1:
                                logger.info(
                                    f"{p_udid}|||VERIFICATION 2 CORRECT => The feature 'scrap' is activated in 'Account details' on Phonebot.co")
                                if counter_Instagram_Scrap_profile_details < p_Daily_limit_Instagram_Scrap_profile_details:
                                    logger.info(
                                        f"{p_udid}|||VERIFICATION 3 CORRECT => PhoneBot didn't reach the limit yet for the task 'scrap'.")

                                    if not this_contact_was_scrapped:
                                        logger.info(f"{p_udid}|||VERIFICATION 4 CORRECT => This contact was not scrapped")

                                        if Flag_Instagram_Scrap_profile_details :
                                            logger.info(
                                                f"{p_udid}|||VERIFICATION 5 CORRECT => Flag_Instagram_Scrap_profile_details is TRUE")

                                            # =================================================================================
                                            # =========================== PLAY STOP OR PAUSE ? ================================
                                            # =================================================================================
                                            mymodules.PlayStopPause(p_udid, p_name_action)
                                            # =================================================================================
                                            # =================================================================================
                                            # =================================================================================



                                            # =================================================================================================


                                            logger.info(
                                                f"{p_udid}|||# ============== [8.5.2.5] WE SCRAP PROFILE DETAILS ===========")
                                            # =================================================================================================
                                            logger.info(f"{p_udid}|||We will scrap the profile details of '{contact}' because 'counter_Instagram_Scrap_profile_details' = True")
                                            # =================================================================================================
                                            logger.info(
                                                f"{p_udid}|||# ============== [8.5.2.5.1] INTIALISATION OF VARIABLES TO SCRAP ======================")
                                            insta_header_full_name = ''
                                            insta_header_biz_category = ''
                                            insta_bio = ''
                                            website = ''
                                            email = ''

                                            logger.info(
                                                f"{p_udid}|||# ============== [8.5.2.5.2] WE START THE SCRAPING ===========================")

                                            driver.implicitly_wait(15)

                                            try:
                                                insta_header_full_name = driver.find_element_by_id(
                                                    "com.instagram.android:id/profile_header_full_name").text
                                                logger.info(f"{p_udid}|||insta_header_full_name of {contact} : {insta_header_full_name}")
                                            except Exception as ex:
                                                logger.info(f"{p_udid}||| {ex} We can't find insta_header_full_name")

                                            try:
                                                insta_header_biz_category = driver.find_element_by_id(
                                                    "com.instagram.android:id/profile_header_business_category").text
                                                logger.info(f"{p_udid}|||insta_header_biz_category of {contact} : {insta_header_biz_category}")
                                            except Exception as ex:
                                                logger.info(f"{p_udid}||| {ex} We can't find insta_header_biz_category")

                                            try:
                                                insta_bio = driver.find_element_by_id(
                                                    "com.instagram.android:id/profile_header_bio_text").text
                                                logger.info(f"{p_udid}|||insta_bio of {contact} : {insta_bio}")
                                            except Exception as ex:
                                                logger.info(f"{p_udid}||| {ex} We can't find insta_bio")

                                            try:
                                                website = driver.find_element_by_id(
                                                    "com.instagram.android:id/profile_header_website").text
                                                logger.info(f"{p_udid}|||website of {contact} : {website}")
                                            except Exception as ex:
                                                logger.info(f"{p_udid}||| {ex} We can't find website")

                                            counter_Instagram_Scrap_profile_details+=1

                                            logger.info(
                                                f"{p_udid}|||# ============== [8.5.2.5.3]  UPDATE TABLE CONTACTS & ACTIONS FOR SCRAPING ==========")
                                            # --- We can now insert the extracted values in table 'contacts' ============================
                                            with lock:
                                                cursor1.execute("UPDATE contacts set insta_header_full_name=?, \
                                                                                                    insta_header_biz_category=?,insta_bio=?, \
                                                                                                    website=?,email=?,platform=? where username=?", \
                                                                (insta_header_full_name, \
                                                                 insta_header_biz_category, insta_bio, website, email,
                                                                 'instagram', contact))
                                                sqliteConnection.commit()
                                            # --- We can now insert a row in the table 'actions' ============================
                                            now = datetime.now()
                                            date_n_time = str(now.strftime("%d/%m/%Y %H:%M:%S"))
                                            cursor1.execute("INSERT INTO actions (platform,type_action,date,id_smartphone,id_social_account,id_contact)  \
                                                             VALUES (?,?,?,?,?,?)",
                                                            ('instagram', 'scrap', date_n_time, p_udid, myprofile_username, id_contact))
                                            sqliteConnection.commit()

                                            # =================================================================================
                                            # =========================== PLAY STOP OR PAUSE ? ================================
                                            # =================================================================================
                                            mymodules.PlayStopPause(p_udid, p_name_action)
                                            # =================================================================================
                                            # =================================================================================
                                            # =================================================================================

                                            #============================================================================================
                                            logger.info(
                                                f"{p_udid}|||# ============== [8.5.2.6] WE SCRAP EMAIL ===================")
                                            # ================= There are 2 solutions: By 'Contact" button or by 'Email' button
                                            # =============================================================================================
                                            logger.info(
                                                f"We will scrap the email of '{contact}' because 'counter_Instagram_Scrap_email' = True")
                                            logger.info(f"{p_udid}|||First we try with 'Contact' button.")

                                            logger.info(
                                                f"{p_udid}|||# ============== [8.5.2.6.1] SCRAP THE CONTACT BUTTON ========================")
                                            try:
                                                try:
                                                    button_contacts = driver.find_element(By.XPATH,
                                                                                           "//android.widget.TextView[@text='Contacts']")  # Contact in english

                                                except:
                                                    # --- We have to check in Frech and English buttons 'Contacts' or 'Contact'
                                                    # If we didn't find in French language, we try in english
                                                    try:
                                                        button_contacts = driver.find_element(By.XPATH,
                                                                                               "//android.widget.TextView[@text='Contact']")
                                                    except:
                                                        # If we didn't find in english, we create the error to got to 'except
                                                        button_contacts = driver.find_element(By.XPATH,
                                                                                                  "//android.widget.TextView[@text='Contact']")


                                                # =================================================================================
                                                # =========================== PLAY STOP OR PAUSE ? ================================
                                                # =================================================================================
                                                mymodules.PlayStopPause(p_udid, p_name_action)
                                                # =================================================================================
                                                # =================================================================================
                                                # =================================================================================

                                                # =================================================================================
                                                # === SCRAPING EMAIL FROM CONTACT BUTTON AND ALSO PHONE NUMBER ====================
                                                # =================================================================================

                                                logger.info(f"{p_udid}|||button_contacts was found!")

                                                button_contacts.click()
                                                driver.implicitly_wait(15)

                                                buttons_contact_email = driver.find_elements_by_id("com.instagram.android:id/contact_option_sub_text")
                                                if len(buttons_contact_email)==0:
                                                    logger.error("PhoneBot couldn't fin the email field. :-(")
                                                elif len(buttons_contact_email)==1:
                                                    tmp= str(buttons_contact_email[0].get_attribute('text'))
                                                    if tmp.find('@')!=-1:
                                                        logger.info(f"{p_udid}|||PhoneBot found email.")
                                                        email_contact=tmp
                                                        logger.info(f"{p_udid}|||email_contact : {email_contact}")
                                                        scrap_email = True
                                                        GoBackButtonInstagram(driver, p_udid)
                                                    else:
                                                        logger.info(f"{p_udid}|||PhoneBot found Phone Number.")
                                                        phone_number=tmp
                                                        logger.info(f"{p_udid}|||phone_number : {phone_number}")
                                                        scrap_phone = True
                                                        GoBackButtonInstagram(driver, p_udid)
                                                else:
                                                    tmp = str(buttons_contact_email[0].get_attribute('text'))
                                                    if tmp.find('@') != -1:
                                                        logger.info(f"{p_udid}|||PhoneBot found email & Phone Number.")
                                                        email_contact = tmp
                                                        phone_number=str(buttons_contact_email[1].get_attribute('text'))
                                                        logger.info(f"{p_udid}|||email_contact : {email_contact}")
                                                        logger.info(f"{p_udid}|||phone_number : {phone_number}")
                                                        scrap_phone = True
                                                        scrap_email = True
                                                        GoBackButtonInstagram(driver, p_udid)

                                                    else:
                                                        logger.info(f"{p_udid}|||PhoneBot found Phone Number")
                                                        phone_number = tmp
                                                        phone_number = str(buttons_contact_email[0].get_attribute('text'))
                                                        logger.info(f"{p_udid}|||phone_number : {phone_number}")
                                                        scrap_phone = True
                                                        email_contact = str(buttons_contact_email[1].get_attribute('text'))
                                                        if email_contact.find('@') != -1:
                                                            logger.info(f"{p_udid}|||PhoneBot found Email")
                                                            logger.info(f"{p_udid}|||email_contact : {email_contact}")
                                                            scrap_email = True
                                                        else:
                                                            logger.info(f"{p_udid}|||PhoneBot found a 2nd element in the 'contact' button of profile {contact}, but it doesn't know what is it. Obviously it is not a mail.")

                                                        GoBackButtonInstagram(driver, p_udid)

                                            except Exception as ex:
                                                logger.info(
                                                    f"{p_udid}||| {ex} button_contacts was not found :-(. Let's try 'Email' button.")
                                                scrap_email = False
                                                scrap_phone = False
                                                Flag_Instagram_Scrap_email = False

                                            # =================================================================================
                                            # =========================== PLAY STOP OR PAUSE ? ================================
                                            # =================================================================================
                                            mymodules.PlayStopPause(p_udid, p_name_action)
                                            # =================================================================================
                                            # =================================================================================
                                            # =================================================================================


                                            if not scrap_email:
                                                logger.info(
                                                    f"{p_udid}|||# ============== [8.5.2.6.2] SCRAP THE EMAIL BUTTON =======================")
                                                logger.info(
                                                    f"{p_udid}|||Scraping email from 'Contact' button didn't work. We'll try now from 'Email' button.")
                                                logger.info(
                                                    f"We will scrap the email of '{contact}' from 'Email' button.")
                                                logger.info(f"{p_udid}|||Let's try with 'Email' button.")

                                                try:
                                                    try:
                                                        # --- We try for french language


                                                        button_email = driver.find_element(By.XPATH,
                                                                                           "//android.widget.TextView[@text='Adresse e-mail']")  # Email in French
                                                        logger.info(
                                                            f"{p_udid}|||We found 'Email' button in French. :-)")

                                                    except:
                                                        try:
                                                            # If we didn't find in French language, we try in english
                                                            logger.info(
                                                                f"{p_udid}|||We didn't find 'Email' button in French, we will try in English.")



                                                            button_email = driver.find_element(By.XPATH,
                                                                                               "//android.widget.TextView[@text='Email']")  # Email in english
                                                            logger.info(
                                                                f"{p_udid}|||We found 'Email' button in English. :-)")
                                                        except:

                                                            # If we didn't find in english, we create the error to got to 'except'
                                                            logger.info(
                                                                f"{p_udid}|||We didn't find 'Email' button in English, we will provoc an error to call the except!")
                                                            button_email=None




                                                    # =================================================================================
                                                    # =========================== PLAY STOP OR PAUSE ? ================================
                                                    # =================================================================================
                                                    mymodules.PlayStopPause(p_udid, p_name_action)
                                                    # =================================================================================
                                                    # =================================================================================
                                                    # =================================================================================


                                                    button_text = button_email.text
                                                    logger.info(f"{p_udid}|||button_text is :" + str(button_text))
                                                    while True:
                                                        try:
                                                            button_email.click()
                                                            logger.info(
                                                                f"{p_udid}|||The bot will sleep just a few seconds..............................")
                                                            time.sleep(random.uniform(1.3, 3.6))
                                                            break
                                                        except Exception as ex:
                                                            logger.info(
                                                                f"{p_udid}||| {ex} We tried to click on 'Email' button and something went wrong. Let's try again.")


                                                    logger.info(
                                                        f"{p_udid}|||The bot will sleep just a few seconds..............................")
                                                    time.sleep(random.uniform(1.3, 2.6))

                                                    # ===================== IF ANDROID ASK FOR WHICH EMAIL CLIENT TO USE ===========================
                                                    try:
                                                        # Case when Android ask for which email client to use? Becuase user has many email client and he/she
                                                        # didn't define which one is the one by Activities

                                                        if len(driver.find_elements_by_id('android:id/button_always')) != 0:
                                                            which_email_client_button_always = driver.find_elements_by_id(
                                                                'android:id/button_always')
                                                            # === Let's search for Gmail ==========================
                                                            email_clients=driver.find_elements_by_id("android:id/text1")
                                                            if len(email_clients)==0:
                                                                logger.info("There was no choice of email clients. Your smartphone didn't propose any email clients.")

                                                            elif len(email_clients)==1:
                                                                if email_clients[0].get_attribute("text") == "Gmail":
                                                                    logger.info("PhoneBot found Gmail client option.")
                                                                    email_clients[0].click()

                                                                    with lock:
                                                                        cursor1.execute("UPDATE smartphones set app_email_client=? WHERE udid=?",('gmail',p_udid))
                                                                        sqliteConnection.commit()
                                                                else:
                                                                    logger.error("PhoneBot didn't find Gmail client option. You need to install Gmail to scrap email of Instagram users.")
                                                            else:
                                                                i=0

                                                                while i<len(email_clients):
                                                                    if email_clients[i].get_attribute("text") == "Gmail":
                                                                        logger.info("PhoneBot found Gmail client option.")

                                                                        with lock:
                                                                            cursor1.execute(
                                                                                "UPDATE smartphones set app_email_client=? WHERE udid=?",
                                                                                ('gmail', p_udid))
                                                                            sqliteConnection.commit()
                                                                        email_clients[i].click()
                                                                        break
                                                                    i+=1


                                                            which_email_client_button_always[0].click()
                                                    except Exception as ex:
                                                        logger.info(
                                                            f"{p_udid}||| {ex} We didn't have Android asking for Which email client to choose!")
                                                    # ==============================================================================================
                                                    # =================================================================================
                                                    # =========================== PLAY STOP OR PAUSE ? ================================
                                                    # =================================================================================
                                                    mymodules.PlayStopPause(p_udid, p_name_action)
                                                    # =================================================================================
                                                    # =================================================================================
                                                    # =================================================================================
                                                    driver.implicitly_wait(15)
                                                    logger.info(
                                                        f"{p_udid}|||The bot will sleep just a few seconds..............................")
                                                    time.sleep(random.uniform(6.1, 15.4))
                                                    current_context = driver.current_context
                                                    print(f"context : {current_context}")
                                                    driver.switch_to.context(current_context)
                                                    logger.info(
                                                        f"{p_udid}|||The bot will sleep just a few seconds..............................")
                                                    time.sleep(random.uniform(10.2, 15.3))
                                                    driver.implicitly_wait(15)
                                                    mail_app_details = get_email_from_mail_client_field_to(driver, p_udid,lock)
                                                    email_contact = mail_app_details[0]
                                                    logger.info(f"{p_udid}|||email_contact : {email_contact}")
                                                    counter_Instagram_Scrap_email += 1
                                                    scrap_email = True
                                                    # === We come back to Instagram as email client opened and get the focus
                                                    try:
                                                        driver.press_keycode(keycode=187)
                                                        apps_open = driver.find_elements_by_id(
                                                            "com.android.systemui:id/title")
                                                        for app_open in apps_open:
                                                            if app_open.get_attribute(
                                                                    'content-desc') == 'Instagram':
                                                                app_open.click()
                                                                break
                                                                logger.info(
                                                                    f"{p_udid}|||The bot will sleep just a few seconds..............................")
                                                                time.sleep(random.uniform(0.9, 2.3))
                                                                driver.implicitly_wait(5)
                                                    except Exception as ex:
                                                        logger.info(
                                                            f"{p_udid}||| {ex} Error when we tried to come back to Instagram")

                                                except Exception as ex:
                                                    logger.info(
                                                        f"{p_udid}||| {ex} Something went wrong while scraping 'Email' button  :-(")
                                                    logger.info(f"{p_udid}|||We couldn't scrap email from 'Email' button! :-(")
                                                    scrap_email = False
                                                    Flag_Instagram_Scrap_email = False

                                            # =================================================================================
                                            # =========================== PLAY STOP OR PAUSE ? ================================
                                            # =================================================================================
                                            mymodules.PlayStopPause(p_udid, p_name_action)
                                            # =================================================================================
                                            # =================================================================================
                                            # =================================================================================
                                            # ========================= LET'S INSERT THE EMAIL IN TABLE CONTACT ========================
                                            # --- We can now insert the extracted values in table 'contacts' ============================
                                            if scrap_email:
                                                print("email_contact was found!")
                                                clean_email = email_contact.replace("<", "").replace(">", "").replace(",",
                                                                                                                      "").replace(
                                                    ";",
                                                    "").replace(
                                                    "(", "") \
                                                    .replace(")", "").replace("[", "").replace("]", "")
                                                email = clean_email
                                                logger.info(f"{p_udid}|||Email : {email}")
                                                with lock:
                                                    cursor1.execute("UPDATE contacts set email=? where id=?", (email, id_contact))
                                                    sqliteConnection.commit()
                                                    counter_Instagram_Scrap_email += 1
                                                logger.info(f"{p_udid}|||We add the email {email} of contact.")



                                            # ========================= LET'S INSERT THE PHONE NUMBER IN TABLE CONTACT ========================
                                            # --- We can now insert the extracted values in table 'contacts' ============================
                                            if scrap_phone:
                                                print("phone_number was found!")

                                                logger.info(f"{p_udid}|||Phone : {phone_number}")
                                                with lock:
                                                    cursor1.execute("UPDATE contacts set phone=? where id=?",
                                                                    (phone_number, id_contact))
                                                    sqliteConnection.commit()

                                                logger.info(f"{p_udid}|||We add the phone {phone_number} of contact.")

                                            logger.info(
                                                f"{p_udid}|||The bot will sleep just a few seconds..............................")
                                            time.sleep(random.uniform(1.9, 3.3))

                                        else:
                                            logger.info(
                                                f"{p_udid}|||VERIFICATION 5 FAILED => Flag_Instagram_Scrap_profile_details is FALSE")
                                    else:
                                        logger.info(f"{p_udid}|||VERIFICATION 4 FAILED => This contact was already scrapped!")

                                else:
                                    logger.info(
                                        f"{p_udid}|||VERIFICATION 3 FAILED => PhoneBot reach the limit yet for the task 'scrap'.")



                            else:
                                logger.info(
                                    f"{p_udid}|||VERIFICATION 2 FAILED => The feature 'scrap' is NOT activated in 'Account details' on Phonebot.co")
                                Flag_Instagram_Scrap_email=False

                        # =============================================================================================












                        logger.info(
                            f"{p_udid}|||counter_Instagram_Scrap_profile_details : {counter_Instagram_Scrap_profile_details}/{p_Daily_limit_Instagram_Scrap_profile_details}")

                        logger.info(f"{p_udid}|||The bot will sleep just a few seconds..............................")
                        time.sleep(random.uniform(2.9, 6.3))
                        # =================================================================================================

                        # =================================================================================
                        # =========================== PLAY STOP OR PAUSE ? ================================
                        # =================================================================================
                        mymodules.PlayStopPause(p_udid, p_name_action)
                        # =================================================================================
                        # =================================================================================
                        # =================================================================================

                    else:
                        logger.info(
                            f"{p_udid}|||VERIFICATION 1 FAILED => Function 'Insta_Search DIDN'T find the contact '{contact}'. :-)")

                        logger.critical(f"{p_udid}|||Sorry, we couldn't find this account {contact}! :-(.")

                    logger.info(
                        f"{p_udid}|||# ================== [ 8.6] WE NEED TO CHECK IF WE DIDN'T REACH THE LIMITS PARAMETERS ====================")

                    if counter_Instagram_Send_message < p_Daily_limit_Instagram_Send_message and instagram_send_message:
                        Flag_Instagram_Send_message=True
                    else:
                        Flag_Instagram_Send_message =False

                    if counter_Instagram_Scrap_profile_details < p_Daily_limit_Instagram_Scrap_profile_details and instagram_scrap_details:
                       Flag_Instagram_Scrap_profile_details=True
                    else:
                        Flag_Instagram_Scrap_profile_details = False

                    if counter_Instagram_Follow_members < p_Daily_limit_Instagram_Follow_members and instagram_follow:
                        Flag_Instagram_Follow_members=True
                    else:
                        Flag_Instagram_Follow_members = False

                    if counter_Instagram_Like_pics_of_member < p_Daily_limit_Instagram_Like_pics_of_member and instagram_like_pictures_of_followers:
                        Flag_Instagram_Like_pics_of_member=True
                    else:
                        Flag_Instagram_Like_pics_of_member = False

                    logger.info(
                        f"{p_udid}|||# ================== [ 8.7] IF WE EXCEED ALL THE LIMITS, WE GO OUT OF THE LOOP ====================")

                    if Flag_Instagram_Follow_members==False and Flag_Instagram_Like_pics_of_member==False and   \
                            Flag_Instagram_Send_message==False and Flag_Instagram_Scrap_profile_details==False:
                        break

                    # =================================================================================
                    # =========================== PLAY STOP OR PAUSE ? ================================
                    # =================================================================================
                    mymodules.PlayStopPause(p_udid, p_name_action)
                    # =================================================================================
                    # =================================================================================
                    # =================================================================================
                else:
                    logger.info(f"{p_udid}|||The profile {contact} has been already scrapped! We go for next profile.")

                # =================================================================================
                # =========================== PLAY STOP OR PAUSE ? ================================
                # =================================================================================
                mymodules.PlayStopPause(p_udid, p_name_action)
                # =================================================================================
                # =================================================================================
                # =================================================================================

                logger.info(f"{p_udid}|||=====================================================================================")
                logger.info(f"{p_udid}|||End of the loop for this contact '{contact}'")
                logger.info(
                    f"{p_udid}|||counter_Instagram_Scrap_profile_details = {counter_Instagram_Scrap_profile_details}/{p_Daily_limit_Instagram_Scrap_profile_details}")
                logger.info(f"{p_udid}|||Flag_Instagram_Scrap_profile_details  = {Flag_Instagram_Scrap_profile_details  }")
                logger.info(f"{p_udid}|||***")
                logger.info(
                    f"{p_udid}|||counter_Instagram_Scrap_email = {counter_Instagram_Scrap_email}/{p_Daily_limit_Instagram_Scrap_email}")
                logger.info(f"{p_udid}|||Flag_Instagram_Scrap_email  = {Flag_Instagram_Scrap_email }")
                logger.info(f"{p_udid}|||***")
                logger.info(
                    f"{p_udid}|||counter_Instagram_Send_message = {counter_Instagram_Send_message}/{p_Daily_limit_Instagram_Send_message}")
                logger.info(f"{p_udid}|||Flag_Instagram_Send_message  = {Flag_Instagram_Send_message }")
                logger.info(f"{p_udid}|||***")
                logger.info(
                    f"{p_udid}|||counter_Instagram_Like_pics_of_member = {counter_Instagram_Like_pics_of_member}/{p_Daily_limit_Instagram_Like_pics_of_member}")
                logger.info(f"{p_udid}|||Flag_Instagram_Like_pics_of_member  = {Flag_Instagram_Like_pics_of_member }")
                logger.info(f"{p_udid}|||***")
                logger.info(
                    f"{p_udid}|||counter_Instagram_Follow_members = {counter_Instagram_Follow_members}/{p_Daily_limit_Instagram_Follow_members}")
                logger.info(f"{p_udid}|||Flag_Instagram_Follow_members = {Flag_Instagram_Follow_members}")
                logger.info(f"{p_udid}|||***")

                logger.info(f"{p_udid}|||=====================================================================================")

        if instagram_unfollow == 1 and p_Daily_limit_Instagram_UnFollow_members!=0:
            counter_Instagram_UnFollow_members=InstagramUnFollow(driver,p_udid,myprofile_username,p_Daily_limit_Instagram_UnFollow_members)


        #if instagram_publish_pictures == 1:
            #PublishPics(driver,p_udid,myprofile_username,lock,p_bug)

        if instagram_like_random_pictures == 1:
            LikeSearchPictures(driver, p_udid,myprofile_username, instagram_list_hashtags_liking_pictures,p_bug,lock)

        total_counter_tasks_of_hit = counter_Instagram_Follow_members + counter_Instagram_UnFollow_members + \
                                     counter_Instagram_Scrap_profile_details + counter_Instagram_Like_pics_of_member + \
                                     counter_Instagram_Send_message
        return total_counter_tasks_of_hit
    except ValueError:
        print("ERROR EROOR")


    #except Exception as ex:
    #except:
        #logger.critical(f"{p_udid}||| Error with Instagram_bot.Start_bot()!!! We try again later!")

        #logger.critical(f"{p_udid}|||{ex} --> Error with Instagram_bot.Start_bot()!!! We try again later!")
    #except ValueError:
        #print("--> Error with Instagram_bot.Start_bot()!!! We try again later!")
    try:
        if driver:
            driver.quit()
    except:
        logger.error("Phonebot could'nt close the driver.")
    try:
        if cursor1:
            cursor1.close()
    except:
        logger.error("Phonebot could'nt close cursor1.")

    try:
        if sqliteConnection:
            sqliteConnection.close()
    except:
        logger.error("Phonebot could'nt close sqliteConnection.")

'''

import multiprocessing


if __name__ == '__main__':
    multiprocessing.freeze_support()
    m = multiprocessing.Manager()
    lock = m.Lock()
    list_arguments_smartphones = []
    StartBot('INSTAGRAM', 'OUKIC16PRO37851','4729','C16_Pro_EEA','9.0','Android',3,3,3,3,3,3,lock)
    #StartBot("INSTAGRAM ", "0123456789ABCDEF", "4728", "i11", "8.1", "Android",0,3,3,0,0,2,lock)
    #StartBot('INSTAGRAM', 'A60ProEEA0112572', '4723', 'A60Pro', '9.0', 'Android',15,15,0,0,0,0,lock)
'''


