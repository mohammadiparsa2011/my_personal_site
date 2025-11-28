# استفاده از تصویر رسمی پایتون
FROM python:3.12-slim

# تنظیم مسیر کاری
WORKDIR /app

# کپی فایل requirements و نصب پکیج‌ها
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# کپی کل پروژه داخل کانتینر
COPY . .

# اعمال متغیر محیطی
ENV PYTHONUNBUFFERED=1

# اجرای سرور Django (توسعه)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
