# پروژه Flecta MQL

Flecta MQL یک وب‌سایت شرکتی و محتوایی برای معرفی خدمات طراحی و توسعه ابزارهای معاملاتی در پلتفرم‌های MetaTrader است. هدف کسب‌وکار، معرفی نمونه‌کارها، دریافت درخواست مشتری برای ساخت اکسپرت و اندیکاتور اختصاصی و انتشار محتوای آموزشی مرتبط با معامله‌گری الگوریتمی و زبان MQL است.

**نسخه آنلاین:** [https://flectamql.ir/](https://flectamql.ir/)

## امکانات اصلی

- صفحات خانه، درباره ما و تماس با ما
- نمایش خدمات و نمونه‌کارها به همراه لینک مخزن GitHub
- وبلاگ دارای دسته‌بندی، برچسب، نویسنده، جستجو و RSS
- صفحه جزئیات مطلب، مطالب قبلی و بعدی و شمارش بازدید
- ثبت و مدیریت دیدگاه‌های وبلاگ
- ثبت‌نام، ورود، خروج و بازیابی رمز عبور
- کپچا در فرم ثبت‌نام، تماس و دیدگاه‌ها
- پنل مدیریت Django و ویرایشگر محتوای Summernote
- صفحات اختصاصی خطاهای 400، 403، CSRF، 404 و 500

## خلاصه بک‌اند

بک‌اند پروژه با **Python و Django 5.2** پیاده‌سازی شده و از معماری چند اپلیکیشنی استفاده می‌کند:

- `website`: صفحات عمومی و ثبت پیام‌های تماس
- `blog`: مدیریت مطالب، دسته‌بندی‌ها، برچسب‌ها، دیدگاه‌ها و شمارش بازدید
- `accounts`: احراز هویت، ثبت‌نام و بازیابی رمز عبور
- Django Admin برای مدیریت کاربران و محتوای سایت
- Django Sites، Sitemap و Robots برای تنظیمات فنی سئو
- JSON-LD، canonical، Open Graph و Twitter Card برای داده‌های ساختاریافته و اشتراک‌گذاری صفحات
- Django Compressor و تنظیمات کش و فشرده‌سازی سرور برای بهینه‌سازی فایل‌های استاتیک
- تنظیمات جداگانه توسعه و تولید و بارگذاری متغیرهای محیطی از فایل `.env`

## دیتابیس

در محیط توسعه از **SQLite** استفاده می‌شود. نسخه آنلاین روی Vercel با **PostgreSQL (Supabase)** و از طریق `DATABASE_URL` اجرا می‌شود. تنظیمات MySQL برای هاست‌های سنتی هم با متغیرهای `DB_NAME`، `DB_USER`، `DB_PASSWORD`، `DB_HOST` و `DB_PORT` در `flectasite.setting.prod` پشتیبانی می‌شود. هیچ رمزی در کد ذخیره نمی‌شود.

## متغیرهای محیطی در Vercel

این متغیرها را در Project Settings → Environment Variables برای Production و Preview تنظیم کنید:

| متغیر | ضروری | توضیح |
| --- | --- | --- |
| `SECRET_KEY` | بله | کلید امنیتی Django |
| `DATABASE_URL` | بله | رشته اتصال Supabase (poller پورت 6543) |
| `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USE_SSL`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` | بله | SMTP برای فرم تماس و بازیابی رمز |
| `DEFAULT_FROM_EMAIL`, `CONTACT_RECIPIENT_EMAIL` | خیر | فرستنده و گیرنده پیام‌های تماس |
| `SUPABASE_URL`, `SUPABASE_STORAGE_BUCKET` | خیر | فعال‌سازی ذخیره دائمی مدیا در Supabase Storage |
| `SUPABASE_STORAGE_ACCESS_KEY`, `SUPABASE_STORAGE_SECRET_KEY` | خیر | کلیدهای S3 مربوط به Supabase Storage |
| `SUPABASE_S3_REGION`, `SUPABASE_STORAGE_PUBLIC_URL` | خیر | منطقه و دامنه عمومی باکت |

بدون فایل‌سیستم دائمی، آپلودهای Vercel با هر دیپلوی پاک می‌شوند. برای ذخیره دائمی، یک bucket عمومی در Supabase Storage بسازید، کلیدهای S3 آن را تنظیم کنید و سپس فایل‌های موجود را یک‌بار منتقل کنید:

```powershell
python manage.py upload_media --settings=flectasite.setting.vercel
```

## اجرای پروژه در محیط توسعه

پیش‌نیاز پروژه Python 3.11 یا نسخه سازگار است. پس از استخراج فایل‌ها، در ویندوز دستورات زیر را اجرا کنید:

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

فایل `.env` باید کنار `manage.py` قرار داشته و حداقل متغیر `SECRET_KEY` را در خود داشته باشد. فایل `.env.example` نیز قالب متغیرهای موردنیاز را نشان می‌دهد.

سپس پروژه از نشانی زیر در دسترس است:

```text
http://127.0.0.1:8000/
```

## سئو و کارایی

آخرین نتایج ثبت‌شده برای نسخه آنلاین در تاریخ 20 اوت 2026:

- **Seobility SEO Checker:** امتیاز On-page برابر 84٪؛ متادیتا 100٪، ساختار صفحه 100٪ و سرور 98٪
- **GTmetrix:** رتبه B؛ Performance برابر 74٪ و Structure برابر 97٪
- **Web Vitals:** مقدار LCP برابر 2.4 ثانیه، TBT برابر 71 میلی‌ثانیه و CLS برابر صفر

[مشاهده گزارش GTmetrix](https://gtmetrix.com/reports/flectamql.ir/n38uCSWQ/)

## فناوری‌ها و پکیج‌های مهم

- Python 3.11 و Django 5.2
- SQLite در توسعه و MySQL در تولید
- PyMySQL
- django-simple-captcha
- django-taggit
- django-summernote
- django-robots
- django-compressor
- HTML، CSS و JavaScript

## فایل‌های استاتیک

فایل‌های اصلی پروژه در پوشه `statics` قرار دارند. پوشه `static` خروجی نهایی Django است و در صورت نیاز با دستور زیر ساخته می‌شود:

```powershell
python manage.py collectstatic --noinput