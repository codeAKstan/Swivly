# Swivly

**Swivly** is a marketplace platform tailored for students, enabling them to find accommodations, buy and sell items, and connect seamlessly. The platform fosters a trusted environment with advanced features like in-app communication, user reviews, and an admin moderation panel.

---

## Features and Functionality

### 1. User Authentication and Profile Management
- **User Roles**:  
  - Student Buyer  
  - Student Seller  
  - Student Agent  
- **Authentication**:  
  - Sign up and log in using email and password.  
- **Profiles**:  
  - Update profile picture and contact information.  

### 2. Accommodation Listings
- **Search Filters**:  
  - Filter by price, location, and property type.  
- **Detailed Listings**:  
  - Each property has a dedicated page displaying rent, location, and images.  

### 3. Marketplace for Buying and Selling
- **Categories**:  
  - Browse items by predefined categories.  
- **Search Filter**:  
  - Find items quickly with intuitive search options. 
- **Detailed Listings**:  
  - Each product has a dedicated page displaying details  
- **Purchase Methods**:  
  - Integrated payment gateways using **Flutterwave** and **Paystack**.  

### 4. Communication and Chat
- **In-App Messaging**:  
  - Communication between buyers and sellers or landlords and tenants.  
- **Notifications**:  
  - Keep users informed of updates and messages.  

### 5. Reviews and Ratings
- **For Landlords/Tenants**:  
  - Tenants can leave reviews and ratings for landlords or properties.  
- **For Buyers/Sellers**:  
  - A rating system builds trust and promotes transparency.  

### 6. Admin Panel
- **Admin Dashboard**:  
  - Manage user accounts, property listings, and user reports.  
- **Moderation**:  
  - Review and approve listings before they are made public.  

---

## Technologies Used
- **Frontend**: HTML5  
- **Backend**: Python-Django 
- **Database**: postgresql  
- **Payment Integration**:  Paystack  

---

## Installation and Setup


### Prerequisites

- Python 3.8+
- Django 4.0+
- Virtualenv
- Paystack account (for payment integration)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/codeAKstan/Swivly.git
   cd Swivly
   ```
2.  Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate # On Windows: venv\Scripts\activate
   ```   

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add the following:
   ```env
   DEBUG=True
   SECRET_KEY=your_django_secret_key
   PAYSTACK_SECRET_KEY=your_paystack_secret_key
   PAYSTACK_PUBLIC_KEY=your_paystack_public_key
   ```

5. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

7. Start the development server:
   ```bash
   python manage.py runserver
   ```

8. Access the application in your browser at `http://127.0.0.1:8000/`.

## Contribution

Contributions are welcome! Feel free to fork the repository, create a feature branch, and submit a pull request.

---

## License

This project is licensed under the MIT License.

---

## Acknowledgments

- [Django Documentation](https://docs.djangoproject.com/)
- [Paystack Integration Guide](https://paystack.com/docs/)
