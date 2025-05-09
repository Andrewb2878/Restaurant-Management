# Code Standards

### Project Structure:

Restaurant-Management/
│
├── manage.py
├── requirements.txt
├── RMS/                   # Django project folder (settings, urls)
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── core/                  # Core app (UI, base logic)
│   ├── templates/
│   ├── static/
│   ├── views.py
│   └── ...
│
├── reservation/           # Reservations app
│   ├── models.py
│   ├── views.py
│   └── ...
│
├── staff_scheduling/      # Scheduling app
│   ├── models.py
│   ├── views.py
│   └── ...

### App Purpose Guidelines:

#### core/:
Responsible for global templates, authentication, and landing pages.

#### reservation/:
Handles all booking-related functionality — table availability, customer booking requests, and reservation management.

#### staff_scheduling/:
Contains logic for managing staff rosters, shift assignments, and availability.

### Recommended Files Per App:

| File					|		Purpose										|
|-----------------------|---------------------------------------------------|
| models.py				|	Define data models related to the app domain	|
| views.py				|	Handle requests and return responses			|
| urls.py				|	Route app-specific URL patterns					|
| forms.py (optional)	|	Custom Django forms for user input				|
| templates/ folder		|	App-specific HTML templates						|
| static/ folder		|	App-specific static files (optional)			|
| admin.py				|	Register models with the admin site (if used)	|
| tests.py				|	Unit tests for the app logic					|

### Naming Conventions:
- App folder and file names should use lowercase with underscores only when necessary (e.g., staff_scheduling).
- Avoiding use of CamelCase in folder names.

### Code Style:
#### Python:
- Use PEP8 styling: 4-space indentation, no trailing whitespace.
- Use descriptive variable names (reservation_date, not rd).

#### Django:
- Class-based views preferred for complex pages.

### Models:
- Use Meta to set ordering where needed.
- Related fields: Always use related_name.

### Forms:
- All form fields must use labels.
- Custom validation should raise ValidationError.

### Routing:
- Use name= for all URLs to support reverse lookup

### Templates:
- Use Tailwind for all styling.

### Security:
- Use Django’s built-in auth system.
- Use decorators like @login_required or mixins like LoginRequiredMixin.