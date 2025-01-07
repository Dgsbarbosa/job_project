# Final Project - Harvard CS50W

## **Project Description**

This project is a job vacancy management platform that allows candidates and companies to interact efficiently. Companies can register vacancies, manage them, open and close vacancies, and candidates can create personalized profiles, save vacancies of interest, and apply.

The application offers filtering features by location (country, state, city) and type of contract, with a focus on usability and scalability.

## **Distinctiveness and Complexity**

### **Distinctiveness**
This project addresses a practical and real solution in the job market, integrating profile management, job registration and personalized interactions between candidates and companies. It stands out for its use of external APIs (such as CountryStateCity) for real-time location management, a high level of user interactivity and the application of modern web development standards with Django.

### **Complexity**
The project incorporates:
- **API Integration**: Consumption of an external API to automatically fill in location data, ensuring an optimized user experience.
- **Advanced Relational Models**: Use of inheritance in models to simplify the reuse of common fields, such as `Contact` and `Location`.
- **Dynamic Filtering and Grouping**: Jobs are grouped by date and company, optimizing the presentation of information to users.
- **Authentication and Permissions**: Critical actions (such as saving jobs and managing profiles) require authentication and implement differentiated permission levels.
- **Dynamic Interface**: Enhanced interactivity with contextual messages and forms that adapt to specific conditions, such as dynamic field visibility.

## **Project Structure**

### **Apps Created**

#### **1. App: user**

##### Structure:
- **`admin.py`**: Admin settings for managing user profiles.
- **`apps.py`**: Django app configuration.
- **`forms.py`**: Forms for authentication and editing profiles.
- **`models.py`**: User models and custom profiles.
- **`tests.py`**: Tests for validating functionality.
- **`urls.py`**: Specific routes for authentication, editing, and viewing profiles.
- **`utils.py`**: Auxiliary functions, such as data validation and sending confirmation emails.
- **`views.py`**: User management, including:
- Registering new users.
- Logging in and out.
- Editing candidate and company profiles.
- **`templates/`**: Contains HTML pages for registering, logging in, logging out, and editing profiles.

##### Features:
- Candidate and company registration.
- Login and logout.
- Editing user profiles.
- Password reset with email validation.

---
#### **2. App: job**
This app manages job registration and interactions between companies and candidates.

##### Structure:
- **`admin.py`**: Settings for managing job vacancies and company profiles.
- **`apps.py`**: Django app configuration.
- **`forms.py`**: Forms for creating and editing job vacancies.
- **`models.py`**: Models for job vacancies, companies and applications.
- **`tests.py`**: Tests for validating features.
- **`urls.py`**: Specific routes for viewing and managing job vacancies.
- **`views.py`**: Job management, including:
- Registering and editing job vacancies. - Filtering by location and contract type.
- Dynamic display of vacancies grouped by date and company.
- **`templates/`**: Contains HTML pages for registering, editing and displaying vacancies.

- **`requirements.txt`**: List of required packages:
- Includes dependencies such as `Django`, `requests` and `python-decouple`.

### **Future Features**

1. **Version 2**
- Register resume
- Compatible vacancies

2. **Version 3**
- Courses and Certifications
- Blog

3. **Version 4**
- Login with Facebook, Google, LinkedIn
- Resume generator

## **How ​​to Run the Application**

1. **Clone the repository**:
```bash
git clone <REPOSITORY_URL>
cd <PROJECT_DIRECTORY>
```

2. **Create a virtual environment**:
```bash
python -m venv venv
source venv/bin/activate # On Unix systems
venv\Scripts\activate # On Windows systems
```

3. **Install the dependencies**:
```bash
pip install -r requirements.txt
```

4. **Configuration of the API key**:
- Create a `.env` file in the root of the project with the following variable:
```
DJANGO_SECRET_KEY=YOUR_SECRET_KEY
COUNTRYSTATECITY_API_KEY=API_KEY
DEBUG=True
```

5. **Apply the database migrations**:
```bash
python manage.py migrate
```

6. **Run the local server**:
```bash
python manage.py runserver
```

7. **Access the application**:
- Open the browser and go to `http://127.0.0.1:8000`.

## **Additional Information