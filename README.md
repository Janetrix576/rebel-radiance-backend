 💄 Rebel Radiance 

**Rebel Radiance** is a sleek, modern e-commerce platform dedicated to offering a wide variety of beauty products to users who want to look and feel their best. Whether you're shopping for skincare, makeup, or grooming essentials, Rebel Radiance provides a seamless way to discover, shop, and have products delivered right to your doorstep.

🧠 Project Overview

In today’s image-conscious world, both women and men are increasingly focused on their appearance, wellness, and self-expression. Rebel Radiance aims to meet this demand by making beauty products accessible at any time, from anywhere, through a convenient and user-friendly online shopping experience.

🧾 Project Goal

To develop a fully functional beauty-focused e-commerce website where customers can:

* Browse products categorized by type
* Add items to a shopping cart
* Complete simulated purchases
* Receive product deliveries

The platform also includes powerful admin tools for managing inventory, users, and analytics.

---

## ✨ MVP Features

### 🧍 Customer Features

* **Login / Signup**: Secure user authentication
* **Product Catalog**: Browse beauty items by category (e.g., Skincare, Haircare, Makeup)
* **Shopping Cart**: Add/remove/view items in cart
* **Checkout**: Simulate a full checkout experience with auto-generated address, billing info, and order invoice
* **Order Confirmation**: View summaries and details of completed purchases

---

### 🛠️ Admin Features

* **Product Management**: Full CRUD operations for beauty items
* **User Management**: Assign user roles for managing products and handling customer orders
* **Order Analytics**: Dashboard showing:

  * Popular beauty products
  * Sales metrics over time
  * Order trends by category or user behavior

---

## 🔧 Technical Stack

### 🖥 Backend

* **Framework**: Python Flask
* **Database**: PostgreSQL
* **API**: RESTful endpoints

### 🌐 Frontend

* **Framework**: ReactJS
* **State Management**: Redux Toolkit
* **UI/UX Design**: Built from responsive **Figma** wireframes (mobile-friendly first)

### 🧪 Testing

* **Frontend Tests**: Jest
* **Backend Tests**: MiniTest (or equivalent testing for Flask)

---

## 📱 Wireframes

Wireframes are designed in **Figma** with mobile responsiveness and intuitive UX in mind. They emphasize clean layout, fast access to categories, and an elegant checkout flow.

---

## 🚀 Getting Started

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run Flask server
flask run
```

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install frontend dependencies
npm install

# Start development server
npm start
```

---

## 🔐 Environment Variables

Make sure to configure your `.env` files for both frontend and backend.

**Backend (`.env`):**

```env
DATABASE_URL=postgresql://username:password@localhost:5432/rebelradiance
SECRET_KEY=your_secret_key_here
```

**Frontend (`.env`):**

```env
REACT_APP_API_URL=http://localhost:5000/api
```

---

## 🔮 Future Enhancements

* Integration with real payment gateways (Stripe, PayPal)
* Customer reviews and ratings on products
* Wishlist and favorites functionality
* Email notifications for order confirmation and delivery
* Promotions and discount codes

---

## 📊 Project Status

> MVP development is underway. Core features are being implemented, with admin dashboard and user-facing interfaces in progress.

---

## 🤝 Contributing

We welcome contributors! If you'd like to contribute:

1. Fork this repository
2. Create a feature branch
3. Commit your changes
4. Open a pull request with a detailed description

---

## 📝 License

This project is licensed under the **MIT License**. See the `LICENSE` file for more details.

---

