Final Project - CS50 Web

Job Vacancy Management Platform

Overview
This project is a job vacancy management platform that connects candidates and companies efficiently. Companies can create and manage job vacancies, while candidates can build personalized profiles, save jobs, and apply for open positions. The platform includes dynamic filtering by location (country, state, city) and contract type, ensuring a smooth user experience.
Distinctiveness & Complexity
Distinctiveness
This project stands out due to its real-world applicability and advanced features beyond a simple CRUD application. Unlike basic job board implementations, this platform:
•	Implements dynamic job filtering using API-based location data.
•	Uses authentication with different permission levels to separate candidates and companies.
•	Introduces model inheritance to efficiently differentiate between user roles.
•	Incorporates an intuitive user experience, with dynamically generated forms and real-time feedback.
Complexity
The project involves multiple technical challenges:
•	API Integration: Fetches and auto-fills location data dynamically from the CountryStateCity API, reducing manual input errors.
•	Advanced Database Models: Uses model inheritance to create a structured database where candidates and companies share attributes but have distinct functionalities.
•	Dynamic UI Elements: Forms and elements adjust based on user roles, ensuring companies and candidates have unique experiences.
•	Authentication & Authorization: Implements Django's authentication system with additional permission levels to restrict actions like job posting or application viewing.
•	Job Filtering & Grouping: Optimized job vacancy presentation through search parameters and date-based sorting.
By combining these features, the project provides a robust and scalable solution that mimics real-world job market operations.
________________________________________

Project Structure

Applications

1. User Management (user app)

Handles user authentication, profile management, and permissions.

Key Files:
•	models.py – Defines user profiles, implementing model inheritance to differentiate candidates and companies.
•	views.py – Manages user authentication, login/logout, and profile editing logic.
•	forms.py – Handles user registration and profile editing, ensuring form validation.
•	urls.py – Routes for login, registration, and profile management.
•	templates/user/ – Contains authentication-related pages.
•	static/user/ – Stylesheets and JavaScript files for frontend interactions.

Features:
•	Candidate & Company registration with role-based profiles.
•	Profile editing with validation and real-time form feedback.
•	Password recovery via email using Django's built-in authentication tools.
________________________________________

2. Job Management (jobs app)

Handles job postings, applications, and filtering features.

Key Files:
•	models.py – Defines job postings, applications, and companies, utilizing ForeignKey relationships for structured data handling.
•	views.py – Implements logic for job creation, editing, filtering, and application processing.
•	forms.py – Contains forms for posting jobs and submitting applications.
•	urls.py – Routes for job listings, job details, and application processing.
•	templates/jobs/ – Contains job-related HTML pages, ensuring a responsive layout.
•	static/jobs/ – Includes JavaScript and CSS files for dynamic job search and filtering.

Features:
•	Job vacancy creation & management, restricted to company users.
•	Filtering system allowing users to search jobs by location and contract type.
•	Grouping vacancies by company and posting date for better organization.
________________________________________
Installation & Setup
1. Clone the Repository

git clone <REPOSITORY_URL>

cd <PROJECT_DIRECTORY>

2. Set Up Virtual Environment

python -m venv venv

source venv/bin/activate  # Mac/Linux

venv\Scripts\activate     # Windows

3. Install Dependencies

pip install -r requirements.txt

4. Configure Environment Variables

Create a .env file and add:

DJANGO_SECRET_KEY=your_secret_key

COUNTRYSTATECITY_API_KEY=your_api_key

DEBUG=True

5. Apply Migrations

python manage.py migrate

6. Run the Development Server

python manage.py runserver

7. Access the Application

Open http://127.0.0.1:8000 in your browser.
________________________________________

Future Enhancements

Version 2

•	Resume Upload & Parsing for automated CV analysis.
•	Job Compatibility Suggestions based on user profiles and experience.

Version 3

•	Online Courses & Certifications for skill improvement.
•	Career Blog with industry insights and job search tips.

Version 4

•	OAuth Login (Google, LinkedIn, Facebook) for seamless authentication.
•	AI-Based Resume Generator to help candidates build effective CVs.
________________________________________

Technologies Used

•	Backend: Django, SQLite
•	Frontend: HTML, CSS, JavaScript
•	APIs: CountryStateCity API for location-based job filtering.
•	Authentication: Django Authentication System with custom role-based permissions.

