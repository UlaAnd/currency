# Project Currency

This Django project can be easily run using Docker.

## Prerequisites

Make sure you have the following installed:

- Docker: [Docker Installation](https://docs.docker.com/get-docker/)


## Getting Started with Docker 

1. **Build and Run Docker Containers**
   ```bash
   docker-compose up --build
   ```

2. **Apply Migrations**
   Open a new terminal and run:
   ```bash
   docker-compose run web python manage.py migrate
   ```

3. **Create a Superuser (Optional)**
   If needed for admin access:
   ```bash
   docker-compose run web python manage.py createsuperuser
   ```
   Follow the prompts to set up the superuser account.

4. **Access the Django Application**
   Open your web browser and go to http://localhost:8000.

5. **Stop Docker Containers**
   When you are done, stop the Docker containers:
   ```bash
   docker-compose down
   ```

## Additional Commands ! Important to run first time 

1. **Populate Project with Currency Data for the Last 90 Days**

   ```bash
   docker-compose run web python manage.py create_exchange_rates
   ```
2. **Command that Runs Every Day at 12 PM to Update Data and Update .csv File**

   ```bash
   docker-compose run web python manage.py crontab add
   ```
2. **Command that Runs Every Day at 12 PM to Update Data and Update .csv File**

   ```bash
   docker-compose run web python manage.py schedule_task
   ```
3. **Linting - Help Keep Code Clean**

   - Make the lint script executable:
   
   ```bash
   chmod +x ./formats 
   ```

   - Run the lints:
   
   ```bash
   ./formats lint
   ```
## Traditional Installation

1. **Create a Virtual Environment (Optional)**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  
   ```

2. **Install Project Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Perform Database Migration**
   ```bash
   python manage.py migrate
   ```

4. **Create a Superuser (Optional)**
   If needed for admin access:
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to set up the superuser account.

5. **Run the Application**
   ```bash
   python manage.py runserver
   ```

6. **Access the Django Application**
   Open your web browser and go to http://localhost:8000.