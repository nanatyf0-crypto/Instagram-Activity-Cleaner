"""
🧹 Instagram Complete Auto Cleaner Script
سكريبت شامل تلقائي كامل لتنظيف نشاط Instagram
يقوم بكل شيء من وحده بدون تفاعل يدوي
"""

import time
import json
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
import sys

# إعداد Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class InstagramCompleteAutoCleanerBot:
    def __init__(self, username, password, headless=False):
        """
        تهيئة البو�� الشامل
        
        Args:
            username (str): اسم المستخدم
            password (str): كلمة المرور
            headless (bool): تشغيل بدون واجهة رسومية
        """
        self.username = username
        self.password = password
        self.driver = None
        self.wait = None
        self.headless = headless
        self.actions = None
        
        # عدادات الإحصائيات
        self.stats = {
            'posts_deleted': 0,
            'comments_deleted': 0,
            'likes_removed': 0,
            'stories_deleted': 0,
            'messages_cleared': 0,
            'followers_unfollowed': 0,
            'errors': 0
        }
        
    def setup_driver(self):
        """إعداد متصفح Selenium بأفضل الخيارات"""
        logger.info("🚀 جاري إعداد المتصفح...")
        
        options = webdriver.ChromeOptions()
        
        if self.headless:
            options.add_argument('--headless')
        
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-popup-blocking')
        options.add_argument('start-maximized')
        options.add_argument('disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--disable-blink-features=AutomationControlled')
        
        try:
            self.driver = webdriver.Chrome(options=options)
            self.wait = WebDriverWait(self.driver, 20)
            self.actions = ActionChains(self.driver)
            logger.info("✅ تم إعداد المتصفح بنجاح")
            return True
        except Exception as e:
            logger.error(f"❌ خطأ في إعداد المتصفح: {e}")
            return False
    
    def login(self):
        """تسجيل الدخول إلى Instagram"""
        logger.info(f"🔐 جاري تسجيل الدخول باسم: {self.username}")
        
        try:
            self.driver.get("https://www.instagram.com/accounts/login/")
            time.sleep(4)
            
            # إدخال اسم المستخدم
            username_input = self.wait.until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            username_input.clear()
            username_input.send_keys(self.username)
            logger.info("✅ تم إدخال اسم المستخدم")
            time.sleep(1)
            
            # إدخال كلمة المرور
            password_input = self.driver.find_element(By.NAME, "password")
            password_input.clear()
            password_input.send_keys(self.password)
            logger.info("✅ تم إدخال كلمة المرور")
            time.sleep(1)
            
            # الضغط على زر تسجيل الدخول
            login_button = self.driver.find_element(
                By.XPATH, 
                "//button[@type='button' and contains(., 'Log in')]"
            )
            self.actions.move_to_element(login_button).click().perform()
            logger.info("⏳ جاري انتظار تحميل الصفحة...")
            time.sleep(6)
            
            # التحقق من نجاح تسجيل الدخول
            if "accounts/login" not in self.driver.current_url:
                logger.info("✅ تم تسجيل الدخول بنجاح")
                
                # رفض الإشعارات إن وجدت
                try:
                    not_now_button = self.driver.find_element(
                        By.XPATH, 
                        "//button[contains(text(), 'Not now')] | //button[contains(text(), 'نعم')]"
                    )
                    not_now_button.click()
                    time.sleep(1)
                except:
                    pass
                
                time.sleep(2)
                return True
            else:
                logger.error("❌ فشل تسجيل الدخول - تحقق من البيانات")
                return False
                
        except TimeoutException:
            logger.error("❌ انتهت مهلة الانتظار أثناء تسجيل الدخول")
            self.stats['errors'] += 1
            return False
        except Exception as e:
            logger.error(f"❌ خطأ في تسجيل الدخول: {e}")
            self.stats['errors'] += 1
            return False
    
    def delete_all_posts(self):
        """حذف جميع المنشورات"""
        logger.info("\n" + "="*60)
        logger.info("🗑️  بدء حذف المنشورات...")
        logger.info("="*60)
        
        try:
            # الذهاب إلى الملف الشخصي
            self.driver.get(f"https://www.instagram.com/{self.username}/")
            time.sleep(3)
            
            while True:
                try:
                    # البحث عن المنشورات
                    posts = self.driver.find_elements(By.XPATH, "//a[contains(@href, '/p/')]")
                    
                    if not posts:
                        logger.info("✅ لا توجد منشورات أخرى للحذف")
                        break
                    
                    # الضغط على أول منشور
                    posts[0].click()
                    time.sleep(2)
                    
                    # البحث عن زر الخيارات (ثلاث نقاط)
                    options_button = self.wait.until(
                        EC.element_to_be_clickable((
                            By.XPATH, 
                            "//button[contains(@aria-label, 'More')] | //button[.//svg[@aria-label='More']]"
                        ))
                    )
                    options_button.click()
                    time.sleep(1)
                    
                    # الضغط على "Delete"
                    delete_button = self.wait.until(
                        EC.element_to_be_clickable((
                            By.XPATH, 
                            "//*[contains(text(), 'Delete')] | //*[contains(text(), 'حذف')]"
                        ))
                    )
                    delete_button.click()
                    time.sleep(1)
                    
                    # تأكيد الحذف
                    confirm_button = self.wait.until(
                        EC.element_to_be_clickable((
                            By.XPATH, 
                            "//button[contains(text(), 'Delete')] | //button[contains(text(), 'حذف')]"
                        ))
                    )
                    confirm_button.click()
                    time.sleep(2)
                    
                    self.stats['posts_deleted'] += 1
                    logger.info(f"✅ تم حذف منشور ({self.stats['posts_deleted']})")
                    
                except TimeoutException:
                    logger.warning("⚠️ انتهت مهلة الانتظار")
                    break
                except Exception as e:
                    logger.warning(f"⚠️ خطأ: {e}")
                    break
            
            logger.info(f"✅ انتهى حذف المنشورات - تم حذف {self.stats['posts_deleted']} منشور")
            
        except Exception as e:
            logger.error(f"❌ خطأ في حذف المنشورات: {e}")
            self.stats['errors'] += 1
    
    def remove_all_likes(self):
        """إزالة جميع الإعجابات"""
        logger.info("\n" + "="*60)
        logger.info("❌ بدء إزالة الإعجابات...")
        logger.info("="*60)
        
        try:
            # الذهاب إلى صفحة النشاط
            self.driver.get("https://www.instagram.com/your/activity/")
            time.sleep(3)
            
            # البحث عن الفلتر
            filter_button = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Filter')]")
            
            if filter_button:
                filter_button[0].click()
                time.sleep(1)
                
                # اختيار الإعجابات فقط
                likes_filter = self.driver.find_elements(
                    By.XPATH, 
                    "//label[contains(text(), 'Likes')] | //*[contains(text(), 'Likes')]"
                )
                
                if likes_filter:
                    likes_filter[0].click()
                    time.sleep(1)
            
            # البحث عن زر Unlike
            while True:
                try:
                    unlike_buttons = self.driver.find_elements(
                        By.XPATH,
                        "//button[contains(text(), 'Unlike')] | //button[contains(., 'Unlike')]"
                    )
                    
                    if not unlike_buttons:
                        logger.info("✅ لا توجد إعجابات أخرى")
                        break
                    
                    # الضغط على زر Unlike
                    unlike_buttons[0].click()
                    time.sleep(1)
                    
                    self.stats['likes_removed'] += 1
                    logger.info(f"✅ تم إزالة إعجاب ({self.stats['likes_removed']})")
                    
                except Exception as e:
                    logger.warning(f"⚠️ خطأ: {e}")
                    break
            
            logger.info(f"✅ انتهت إزالة الإعجابات - تم إزالة {self.stats['likes_removed']} إعجاب")
            
        except Exception as e:
            logger.error(f"❌ خطأ في إزالة الإعجابات: {e}")
            self.stats['errors'] += 1
    
    def delete_all_comments(self):
        """حذف جميع التعليقات"""
        logger.info("\n" + "="*60)
        logger.info("💬 بدء حذف التعليقات...")
        logger.info("="*60)
        
        try:
            self.driver.get(f"https://www.instagram.com/{self.username}/")
            time.sleep(3)
            
            deleted_count = 0
            
            while deleted_count < 500:  # حد أقصى للأمان
                try:
                    # البحث عن المنشورات
                    posts = self.driver.find_elements(By.XPATH, "//a[contains(@href, '/p/')]")
                    
                    if not posts:
                        break
                    
                    # الضغط على أول منشور
                    posts[0].click()
                    time.sleep(2)
                    
                    # البحث عن التعليقات
                    comments = self.driver.find_elements(
                        By.XPATH, 
                        "//button[contains(text(), 'Delete')] | //button[contains(@aria-label, 'Delete comment')]"
                    )
                    
                    if comments:
                        for comment in comments[:5]:  # حذف 5 تعليقات في كل مرة
                            try:
                                comment.click()
                                time.sleep(1)
                                deleted_count += 1
                                self.stats['comments_deleted'] += 1
                            except:
                                pass
                    
                    # الرجوع للملف الشخصي
                    self.driver.back()
                    time.sleep(1)
                    
                except Exception as e:
                    logger.warning(f"⚠️ خطأ: {e}")
                    break
            
            logger.info(f"✅ انتهى حذف التعليقات - تم حذف {self.stats['comments_deleted']} تعليق")
            
        except Exception as e:
            logger.error(f"❌ خطأ في حذف التعليقات: {e}")
            self.stats['errors'] += 1
    
    def delete_all_stories(self):
        """حذف جميع الستوريز"""
        logger.info("\n" + "="*60)
        logger.info("📸 بدء حذف الستوريز...")
        logger.info("="*60)
        
        try:
            self.driver.get(f"https://www.instagram.com/{self.username}/")
            time.sleep(3)
            
            while True:
                try:
                    # البحث عن خيار الستوري
                    story_delete = self.driver.find_elements(
                        By.XPATH,
                        "//button[contains(@aria-label, 'Delete')] | //span[contains(text(), 'Delete story')]"
                    )
                    
                    if not story_delete:
                        logger.info("✅ لا توجد ستوريز أخرى للحذف")
                        break
                    
                    story_delete[0].click()
                    time.sleep(1)
                    
                    # تأكيد الحذف
                    confirm = self.driver.find_elements(
                        By.XPATH,
                        "//button[contains(text(), 'Delete')] | //button[contains(text(), 'حذف')]"
                    )
                    
                    if confirm:
                        confirm[0].click()
                        time.sleep(1)
                        self.stats['stories_deleted'] += 1
                        logger.info(f"✅ تم حذف ستوري ({self.stats['stories_deleted']})")
                    
                except:
                    break
            
            logger.info(f"✅ انتهى حذف الستوريز - تم حذف {self.stats['stories_deleted']} ستوري")
            
        except Exception as e:
            logger.error(f"❌ خطأ في حذف الستوريز: {e}")
            self.stats['errors'] += 1
    
    def clear_search_history(self):
        """مسح سجل البحث"""
        logger.info("\n" + "="*60)
        logger.info("🔍 بدء مسح سجل البحث...")
        logger.info("="*60)
        
        try:
            # الذهاب إلى صفحة البحث
            self.driver.get("https://www.instagram.com/explore/")
            time.sleep(2)
            
            # البحث عن زر مسح السجل
            clear_history = self.driver.find_elements(
                By.XPATH,
                "//button[contains(text(), 'Clear')] | //button[contains(text(), 'Clear all')]"
            )
            
            if clear_history:
                clear_history[0].click()
                time.sleep(1)
                
                # تأكيد مسح السجل
                confirm = self.driver.find_elements(
                    By.XPATH,
                    "//button[contains(text(), 'Clear')] | //button[contains(text(), 'Yes')]"
                )
                
                if confirm:
                    confirm[0].click()
                    time.sleep(1)
                    logger.info("✅ تم مسح سجل البحث")
            
        except Exception as e:
            logger.error(f"⚠️ خطأ في مسح سجل البحث: {e}")
    
    def unfollow_inactive_users(self, limit=100):
        """إلغاء متابعة المستخدمين غير النشطين"""
        logger.info("\n" + "="*60)
        logger.info(f"👥 بدء إلغاء متابعة {limit} مستخدم...")
        logger.info("="*60)
        
        try:
            # الذهاب إلى الملف الشخصي
            self.driver.get(f"https://www.instagram.com/{self.username}/")
            time.sleep(3)
            
            # الضغط على "Following"
            following_button = self.wait.until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//a[contains(@href, '/following/')] | //button[contains(text(), 'Following')]"
                ))
            )
            following_button.click()
            time.sleep(2)
            
            # إلغاء المتابعة
            unfollowed = 0
            for _ in range(limit):
                try:
                    # البحث عن زر "Following"
                    following_buttons = self.driver.find_elements(
                        By.XPATH,
                        "//button[contains(text(), 'Following')] | //button[contains(text(), 'Follow')]"
                    )
                    
                    if not following_buttons:
                        break
                    
                    following_buttons[0].click()
                    time.sleep(1)
                    
                    # تأكيد إلغاء المتابعة
                    unfollow_confirm = self.driver.find_elements(
                        By.XPATH,
                        "//button[contains(text(), 'Unfollow')]"
                    )
                    
                    if unfollow_confirm:
                        unfollow_confirm[0].click()
                        time.sleep(1)
                        unfollowed += 1
                        self.stats['followers_unfollowed'] += 1
                        logger.info(f"✅ تم إلغاء المتابعة ({unfollowed}/{limit})")
                    
                except:
                    break
            
            logger.info(f"✅ انتهى إلغاء المتابعة - تم إلغاء متابعة {unfollowed} مستخدم")
            
        except Exception as e:
            logger.error(f"❌ خطأ في إلغاء المتابعة: {e}")
            self.stats['errors'] += 1
    
    def print_final_report(self):
        """طباعة التقرير النهائي"""
        logger.info("\n" + "="*60)
        logger.info("📊 التقرير النهائي")
        logger.info("="*60)
        
        print("\n🎉 ملخص العمليات المنجزة:")
        print(f"  ✅ منشورات محذوفة: {self.stats['posts_deleted']}")
        print(f"  ✅ إعجابات مزالة: {self.stats['likes_removed']}")
        print(f"  ✅ تعليقات محذوفة: {self.stats['comments_deleted']}")
        print(f"  ✅ ستوريز محذوفة: {self.stats['stories_deleted']}")
        print(f"  ✅ متابعين ملغاة: {self.stats['followers_unfollowed']}")
        print(f"  ❌ أخطاء: {self.stats['errors']}")
        
        total_actions = (
            self.stats['posts_deleted'] +
            self.stats['likes_removed'] +
            self.stats['comments_deleted'] +
            self.stats['stories_deleted'] +
            self.stats['followers_unfollowed']
        )
        
        print(f"\n📈 إجمالي الإجراءات: {total_actions}")
        print("\n✅ تم الانتهاء من جميع العمليات بنجاح!\n")
        
        logger.info("="*60)
    
    def run_complete_cleanup(self):
        """تشغيل جميع العمليات بالكامل"""
        try:
            logger.info("\n" + "#"*60)
            logger.info("# 🧹 Instagram Complete Auto Cleaner")
            logger.info("# تنظيف شامل تلقائي كامل لحسابك")
            logger.info("#"*60 + "\n")
            
            # خطوات البدء
            if not self.setup_driver():
                return False
            
            if not self.login():
                return False
            
            time.sleep(2)
            
            # تشغيل جميع العمليات
            logger.info("\n🔄 جاري تشغيل جميع العمليات...\n")
            
            # 1. حذف الإعجابات (الأولوية الأولى - الأهم)
            self.remove_all_likes()
            time.sleep(3)
            
            # 2. حذف التعليقات
            self.delete_all_comments()
            time.sleep(3)
            
            # 3. حذف الستوريز
            self.delete_all_stories()
            time.sleep(3)
            
            # 4. مسح سجل البحث
            self.clear_search_history()
            time.sleep(2)
            
            # 5. حذف المنشورات (في النهاية)
            self.delete_all_posts()
            time.sleep(3)
            
            # 6. إلغاء المتابعة (اختياري)
            response = input("\n❓ هل تريد إلغاء متابعة 100 مستخدم? (yes/no): ").strip().lower()
            if response in ['yes', 'y', 'نعم']:
                self.unfollow_inactive_users(100)
                time.sleep(2)
            
            # طباعة التقرير
            self.print_final_report()
            
            # الانتظار قبل الإغلاق
            logger.info("⏳ سيتم إغلاق المتصفح خلال 10 ثوانٍ...")
            time.sleep(10)
            
            return True
            
        except Exception as e:
            logger.error(f"❌ خطأ عام: {e}")
            self.stats['errors'] += 1
            return False
        
        finally:
            self.close_driver()
    
    def close_driver(self):
        """إغلاق المتصفح"""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("🔒 تم إغلاق المتصفح")
            except:
                pass


def main():
    """الدالة الرئيسية"""
    
    print("\n" + "#"*60)
    print("# 🧹 Instagram Complete Auto Cleaner v2.0")
    print("# سكريبت شامل تلقائي كامل")
    print("#"*60 + "\n")
    
    print("⚠️  تحذيرات مهمة:")
    print("  • استخدم حسابك الشخصي فقط")
    print("  • قد يؤدي الاستخدام المكثف لحظر الحساب")
    print("  • احرص على توفر نسخة احتياطية من بياناتك")
    print("  • لا تشغل السكريبت على عدة حسابات معاً\n")
    
    # إدخال بيانات المستخدم
    username = input("📱 أدخل اسم المستخدم: ").strip()
    password = input("🔐 أدخل كلمة المرور: ").strip()
    
    if not username or not password:
        print("❌ يجب إدخال اسم المستخدم وكلمة المرور")
        return False
    
    print("\n✅ جاري بدء السكريبت...\n")
    
    # تشغيل البوت
    bot = InstagramCompleteAutoCleanerBot(username, password, headless=False)
    success = bot.run_complete_cleanup()
    
    if success:
        print("\n✅ انتهى السكريبت بنجاح!\n")
    else:
        print("\n❌ حدث خطأ أثناء تنفيذ السكريبت\n")
    
    return success


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  تم إيقاف السكريبت من قبل المستخدم\n")
    except Exception as e:
        print(f"\n\n❌ خطأ: {e}\n")
