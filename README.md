<div align="center">

# 👔 Outfit Generator Web

### Your wardrobe, remixed—anywhere.

A private, responsive web application for cataloging clothes, generating style-and-weather-aware combinations, and saving the looks worth wearing again.

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![HTMX](https://img.shields.io/badge/HTMX-2.x-3366CC?logo=htmx&logoColor=white)](https://htmx.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

## ✨ Features

- Secure registration, login, and user-owned wardrobes
- Garment photo uploads with file type and size validation
- Clothing categories, colors, styles, and weather preferences
- Search and filterable visual wardrobe
- Random outfit generation with one matching item per category
- Persistent saved outfits
- Responsive phone, tablet, and desktop layouts
- HTMX-powered outfit generation without a full page refresh
- SQLite for local development and PostgreSQL-ready production settings
- Optional Cloudinary media storage for production uploads

## 🚀 Local setup

```powershell
git clone https://github.com/PachVsus/Outfit-Generator-Application-Web.git
cd Outfit-Generator-Application-Web
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py migrate
python manage.py runserver
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000).

## 🧪 Tests

```powershell
python manage.py test
```

The test suite covers outfit filtering, category uniqueness, authentication, and cross-user authorization boundaries.

## 🗂️ Structure

```text
├── accounts/           Registration and authentication routes
├── config/             Django settings and root URLs
├── wardrobe/           Models, forms, views, generator service, and tests
├── templates/          Responsive Django templates
├── static/             Application styling
├── render.yaml         Render infrastructure blueprint
└── requirements.txt    Runtime dependencies
```

## ☁️ Deployment

The included `render.yaml` provisions a Django web service and PostgreSQL database on Render.

Before deploying:

1. Push this repository to GitHub.
2. Create a Cloudinary account for durable garment-image storage.
3. In Render, create a Blueprint from the repository.
4. Add `CLOUDINARY_URL`, `ALLOWED_HOSTS`, and `CSRF_TRUSTED_ORIGINS` as environment variables.
5. Update the generated hostname values after Render assigns the service URL.

Production media should not use the service's local filesystem because it can be ephemeral.

## 🔐 Privacy and security

Every wardrobe and outfit query is scoped to the authenticated user. Uploaded files are validated by size and type, production cookies are secure, and application secrets are read from environment variables.

Never commit `.env`, database files, private wardrobe photos, or service credentials.

## 🛣️ Roadmap

- Password reset and email verification
- Outfit calendar and occasion tags
- Image cropping and optimized thumbnails
- Wardrobe import from the desktop edition
- Accessible drag-and-drop outfit editor
- Shareable outfit cards with explicit privacy controls

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">Made for anyone who has ever looked at a full closet and thought, <strong>“I have nothing to wear.”</strong> ✨</div>
