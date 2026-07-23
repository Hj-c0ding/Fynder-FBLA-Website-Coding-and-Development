# Fynder: School Lost and Found Website

Fynder is a polished Django web application for reporting found items, browsing approved listings, and managing claim requests through a staff moderation workflow. It was developed for the FBLA Website Coding and Development competition with a focus on usability, accessibility, and clean project organization.

## Project Highlights

- Purpose-built school lost-and-found platform with a clean public-to-admin workflow
- Django-based architecture with clear separation of templates, views, forms, models, and static assets
- Demo-ready setup with seeded sample data and automated tests
- Responsive interface designed for mobile, tablet, and desktop viewing

## FBLA Competition Information

This project was built for the FBLA Website Coding and Development competition and demonstrates full-stack development, database design, form handling, moderation workflows, and a polished user experience tailored to a school environment.

## Features That Stand Out

- Item reporting, approval, and claim review all live in one coherent workflow
- Search and filtering make it easy to find approved items quickly
- Staff moderation tools support approving, rejecting, and marking claims or items
- Shared templates and static assets keep the interface consistent across pages
- Seeded demo data makes the project ready to present right after setup
- Automated tests cover the core user flows

## Tech Stack

- Backend: Django 6.0.3
- Database: SQLite for development
- Frontend: HTML templates, Bootstrap, custom CSS, and JavaScript
- Image uploads: Django `ImageField` with Pillow installed for image support

## Code Architecture

### Database Models

The application uses Django ORM with two primary models:

- `Item`: stores each found-item listing, including title, category, description, location, date found, upload image, submitter details, moderation status, and admin notes.
- `ClaimRequest`: stores ownership claims for approved items, including claimant details, proof of ownership, additional message, and claim review status.

### Frontend Architecture

- Shared layout: `lostfound/templates/lostfound/base.html` provides the common navigation, messaging, footer, and page shell used across the site.
- Page templates: the home, report, browse, detail, claim, and moderation pages each have their own template under `lostfound/templates/lostfound/`.
- Styling and scripting: custom CSS and JavaScript live in `lostfound/static/lostfound/` to support the theme toggle, responsive layout, and interactive filtering.
- Admin presentation: `templates/admin/` and `static/admin/` provide the branded Django admin overrides used for the custom dashboard appearance.
- Supporting structure: `school_lost_found/` holds project-level routing and settings.

## Core User Flow

1. A student or staff member reports a found item.
2. The item enters a pending review state.
3. Staff members approve the listing so it appears publicly.
4. A user can browse approved items, filter results, and open item details.
5. If the item belongs to them, they submit a claim request with ownership proof.
6. Staff review the claim and update the item status accordingly.

## Getting Started

### Prerequisites

- Python 3.14 or compatible Python 3 environment
- `pip`

### Install and Run

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo_data --reset
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

### Optional Admin Access

```powershell
python manage.py createsuperuser
```

If you are using the provided account, the username and password are both `admin`.

Then visit `http://127.0.0.1:8000/admin/`.

## Testing

```powershell
python manage.py test
```

## Project Structure

```text
Fynder-FBLA-Website-Coding-and-Development/
|-- manage.py
|-- requirements.txt
|-- README.md
|-- docs/
|-- lostfound/
|   |-- forms.py
|   |-- models.py
|   |-- views.py
|   |-- admin.py
|   |-- tests/
|   |-- management/
|   |-- templates/
|   `-- static/
|-- school_lost_found/
|   |-- settings.py
|   |-- urls.py
|   |-- asgi.py
|   `-- wsgi.py
|-- templates/
|   `-- admin/
```

## Sources

- Django documentation: https://docs.djangoproject.com/
- Bootstrap documentation: https://getbootstrap.com/docs/5.3/
- WCAG quick reference: https://www.w3.org/WAI/WCAG21/quickref/
- Google Fonts: https://fonts.google.com/

## Project Demo Video
https://github.com/user-attachments/assets/abe2b7dd-6d40-43be-b720-8fba25e08548
