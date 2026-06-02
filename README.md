# preowned‑buy‑sell‑final  

A Django‑based marketplace that enables users to **buy, sell, and auction pre‑owned items** while leveraging a simple blockchain ledger for transparent voting and transaction verification.

---  

## Overview  

`preowned-buy-sell-final` is a full‑stack web application built with **Python 3.9+** and **Django**. It provides:

* User registration, profile management, and authentication.  
* Listings for pre‑owned goods with images, descriptions, and price negotiation.  
* An election‑style voting system (e.g., for featured items) that records votes on a lightweight blockchain implementation to ensure tamper‑proof results.  
* Commenting and sentiment analysis on listings.  

The project is structured as a single Django app (`myapp`) and includes a complete set of migrations, admin configuration, forms, and views.

---  

## Features  

| Feature | Description |
|---------|-------------|
| **User & Profile Management** | Sign‑up, login, edit profile (age, gender, address, picture). |
| **Item Listings** | Create, edit, delete listings with photos and optional auction dates. |
| **Blockchain‑Backed Voting** | Vote for items; votes are stored in a custom blockchain model (`BlockChainCodeVote`). |
| **Comment System** | Users can post comments; each comment is automatically labelled with a sentiment score. |
| **Admin Dashboard** | Full CRUD access for listings, profiles, votes, and comments via Django admin. |
| **Data Migrations** | 17 incremental migrations covering schema evolution from the initial model to the current state. |
| **Extensible Architecture** | Clean separation of models, forms, views, and URLs for easy future enhancements. |

---  

## Tech Stack  

| Layer | Technology |
|-------|------------|
| **Language** | Python 3.9+ |
| **Web Framework** | Django 4.x |
| **Database** | SQLite (default) – replace with PostgreSQL/MySQL in production |
| **Front‑end** | Django templates (Bootstrap optional) |
| **Blockchain** | Custom lightweight chain stored in the database (`myapp/blockchain.py`) |
| **Sentiment Analysis** | Placeholder – integrate with any external API (e.g., `YOUR_OWN_API_KEY`) |
| **Testing** | Django test framework (unit & integration) |
| **Version Control** | Git (GitHub) |

---  

## Installation  

> **Prerequisites**  
> * Python 3.9 or newer  
> * Git  

```bash
# 1️⃣ Clone the repository
git clone https://github.com/your‑username/preowned-buy-sell-final.git
cd preowned-buy-sell-final

# 2️⃣ Create a virtual environment
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate

# 3️⃣ Install dependencies
pip install --upgrade pip
pip install -r requirements.txt   # If a requirements file is not present, install Django manually:
pip install Django==4.*

# 4️⃣ Apply database migrations
python manage.py migrate

# 5️⃣ (Optional) Create a superuser for the admin site
python manage.py createsuperuser
```

> **Note**: If you plan to use a production‑grade database, update `preowned_buy_sell_final/settings.py` accordingly and run `python manage.py migrate` again.

---  

## Usage  

```bash
# Start the development server
python manage.py runserver
```

Visit **http://127.0.0.1:8000/** in your browser.

### Common commands  

| Command | Purpose |
|---------|---------|
| `python