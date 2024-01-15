
## Installation

1. **Install Required Modules**
    ```bash
    pip install -r requirements.txt
    ```
2. **Perform Database Migration**
    ```bash
    python manage.py migrate
    ```
3. **Create Django Superuser**
   ```bash
   python manage.py createsuperuser
   ```

4. **Give Execute Permissions to linter scripts**
    ```bash
    chmod +x ./formats
    ```
5. **Run Scripts**
    ```bash
    ./formats lint
    ```
